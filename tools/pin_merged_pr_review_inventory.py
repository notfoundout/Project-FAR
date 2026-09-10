#!/usr/bin/env python3
"""Bind an exported merged-PR review inventory to one exact audited main commit.

The live GitHub API can advance while an export is running. This post-processor
keeps only PRs whose merge is both temporally no later than the audited commit
and reachable from that exact Git history. Objects observed after the audited
commit are excluded and recorded. Ambiguous missing history at or before the
cutoff fails closed.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections import Counter
from datetime import datetime
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write(path: pathlib.Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _commit_time(root: pathlib.Path, sha: str) -> datetime:
    result = _git(root, "show", "-s", "--format=%cI", sha)
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError(f"cannot resolve audited SHA {sha}: {result.stderr.strip()}")
    return datetime.fromisoformat(result.stdout.strip().replace("Z", "+00:00"))


def _is_ancestor(root: pathlib.Path, candidate: str, audited_sha: str) -> bool | None:
    result = _git(root, "merge-base", "--is-ancestor", candidate, audited_sha)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def pin_inventory(directory: pathlib.Path, repository_root: pathlib.Path, audited_sha: str) -> dict[str, Any]:
    prs_data = _load(directory / "raw-pr-inventory.json")
    comments_data = _load(directory / "raw-review-comments.json")
    reviews_data = _load(directory / "raw-review-submissions.json")
    threads_data = _load(directory / "raw-review-threads.json")
    manifest = _load(directory / "retrieval-manifest.json")

    if any(data.get("schema_version") != 2 for data in (prs_data, comments_data, reviews_data, threads_data, manifest)):
        raise ValueError("snapshot pinning requires schema_version 2 artifacts")
    prs = prs_data.get("pull_requests")
    comments = comments_data.get("comments")
    reviews = reviews_data.get("reviews")
    threads = threads_data.get("threads")
    retrievals = manifest.get("retrievals")
    if not all(isinstance(value, list) for value in (prs, comments, reviews, threads, retrievals)):
        raise ValueError("inventory arrays are malformed")

    cutoff = _commit_time(repository_root, audited_sha)
    retained: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for item in prs:
        if not isinstance(item, dict):
            raise ValueError("PR inventory contains a non-object record")
        number = item.get("number")
        merged_at = item.get("merged_at")
        merge_sha = item.get("merge_commit_sha")
        if not isinstance(number, int) or not isinstance(merged_at, str) or not isinstance(merge_sha, str):
            raise ValueError(f"PR record is missing merge identity: {number!r}")
        try:
            merged_time = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"PR {number} has malformed merged_at {merged_at!r}") from exc
        if merged_time > cutoff:
            excluded.append({"pr_number": number, "reason": "merged_after_audited_commit"})
            continue
        ancestry = _is_ancestor(repository_root, merge_sha, audited_sha)
        if ancestry is None:
            raise ValueError(
                f"PR {number} merged no later than the audited commit but merge object {merge_sha} "
                "is unavailable; exact snapshot membership cannot be established"
            )
        if not ancestry:
            excluded.append({"pr_number": number, "reason": "merge_not_reachable_from_audited_main"})
            continue
        retained.append(item)

    retained_numbers = {item["number"] for item in retained}
    comments = [item for item in comments if isinstance(item, dict) and item.get("pr_number") in retained_numbers]
    reviews = [item for item in reviews if isinstance(item, dict) and item.get("pr_number") in retained_numbers]
    threads = [item for item in threads if isinstance(item, dict) and item.get("pr_number") in retained_numbers]
    retrievals = [
        item for item in retrievals
        if isinstance(item, dict)
        and (item.get("pr_number") is None or item.get("pr_number") in retained_numbers)
    ]

    prs_data["pull_requests"] = retained
    comments_data["comments"] = comments
    reviews_data["reviews"] = reviews
    threads_data["threads"] = threads
    manifest["audited_sha"] = audited_sha
    manifest["counts"] = {
        "merged_pull_requests": len(retained),
        "issue_comments": sum(item.get("kind") == "issue_comment" for item in comments),
        "inline_review_comments": sum(item.get("kind") == "inline_review_comment" for item in comments),
        "review_submissions": len(reviews),
        "review_threads": len(threads),
    }
    manifest["retrievals"] = retrievals

    uniqueness = {
        "pull_requests": (retained, "number"),
        "review_comments": ([item for item in comments if item.get("kind") == "inline_review_comment"], "id"),
        "issue_comments": ([item for item in comments if item.get("kind") == "issue_comment"], "id"),
        "reviews": (reviews, "id"),
        "threads": (threads, "id"),
    }
    uniqueness_checks: dict[str, Any] = {}
    for name, (records, key) in uniqueness.items():
        values = [item.get(key) for item in records]
        duplicates = sorted(
            (value for value, count in Counter(values).items() if value is None or count > 1),
            key=lambda value: str(value),
        )
        uniqueness_checks[name] = {"ok": not duplicates, "duplicates_or_nulls": duplicates}

    inline_ids = {item.get("id") for item in comments if item.get("kind") == "inline_review_comment"}
    bad_replies = sorted({
        item.get("in_reply_to_id")
        for item in comments
        if item.get("kind") == "inline_review_comment"
        and item.get("in_reply_to_id") is not None
        and item.get("in_reply_to_id") not in inline_ids
    })
    mapping_errors: list[str] = []
    for label, records in (("comments", comments), ("reviews", reviews), ("threads", threads)):
        bad = sorted({item.get("pr_number") for item in records if item.get("pr_number") not in retained_numbers})
        if bad:
            mapping_errors.append(f"{label} reference unknown PRs: {bad}")
    manifest["integrity"] = {
        "mapping_errors": mapping_errors,
        "uniqueness_checks": uniqueness_checks,
        "invalid_reply_parent_ids": bad_replies,
    }
    manifest["snapshot_boundary"] = {
        "audited_sha": audited_sha,
        "audited_commit_time": cutoff.isoformat(),
        "membership_rule": "merged no later than audited commit and merge_commit_sha reachable from audited main",
        "excluded": sorted(excluded, key=lambda item: item["pr_number"]),
    }
    complete = (
        manifest.get("completeness_status") == "COMPLETE"
        and not mapping_errors
        and not bad_replies
        and all(item["ok"] for item in uniqueness_checks.values())
        and all(item.get("complete") is True and not item.get("errors") for item in retrievals)
    )
    manifest["completeness_status"] = "COMPLETE" if complete else "INCOMPLETE"

    _write(directory / "raw-pr-inventory.json", prs_data)
    _write(directory / "raw-review-comments.json", comments_data)
    _write(directory / "raw-review-submissions.json", reviews_data)
    _write(directory / "raw-review-threads.json", threads_data)
    _write(directory / "retrieval-manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--audited-sha", required=True)
    parser.add_argument("--inventory", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        manifest = pin_inventory(args.inventory, args.repository_root.resolve(), args.audited_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": manifest.get("completeness_status"), "audited_sha": manifest.get("audited_sha")}, sort_keys=True))
    return 0 if manifest.get("completeness_status") == "COMPLETE" else 2


if __name__ == "__main__":
    sys.exit(main())
