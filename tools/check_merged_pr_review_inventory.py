#!/usr/bin/env python3
"""Fail-closed checks for the merged-pull-request review inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
REL = pathlib.Path("docs/audits/merged-pr-review-audit")
EXPECTED_SCHEMA_VERSION = 2
EVIDENCE_FILES = (
    "inventory-summary.md",
    "raw-pr-inventory.json",
    "raw-review-comments.json",
    "raw-review-submissions.json",
    "raw-review-threads.json",
    "retrieval-limitations.md",
)
PER_PR_ENDPOINTS = (
    "GET /repos/{owner}/{repo}/issues/{pr}/comments",
    "GET /repos/{owner}/{repo}/pulls/{pr}/reviews",
    "GET /repos/{owner}/{repo}/pulls/{pr}/comments",
    "GraphQL pullRequest.reviewThreads",
)


def _load(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _git_blob_sha1(path: pathlib.Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def _records(data: dict[str, Any], key: str, label: str, errors: list[str]) -> list[dict[str, Any]]:
    raw = data.get(key)
    if not isinstance(raw, list):
        errors.append(f"{label} must contain array field {key!r}")
        return []
    records: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
        else:
            records.append(item)
    return records


def _require_unique(records: list[dict[str, Any]], key: str, label: str, errors: list[str]) -> None:
    seen: set[Any] = set()
    for record in records:
        value = record.get(key)
        if value is None or value == "":
            errors.append(f"{label} lacks {key}")
        elif value in seen:
            errors.append(f"duplicate {label} {key}: {value}")
        else:
            seen.add(value)


def validate(root: pathlib.Path = ROOT, expected_main_sha: str | None = None) -> list[str]:
    errors: list[str] = []
    directory = root / REL
    try:
        prs_data = _load(directory / "raw-pr-inventory.json")
        comments_data = _load(directory / "raw-review-comments.json")
        reviews_data = _load(directory / "raw-review-submissions.json")
        threads_data = _load(directory / "raw-review-threads.json")
        manifest = _load(directory / "retrieval-manifest.json")
    except ValueError as exc:
        return [str(exc)]

    for label, data in (
        ("PR inventory", prs_data),
        ("comments", comments_data),
        ("reviews", reviews_data),
        ("threads", threads_data),
        ("manifest", manifest),
    ):
        if data.get("schema_version") != EXPECTED_SCHEMA_VERSION:
            errors.append(f"{label} schema_version must be {EXPECTED_SCHEMA_VERSION}")

    audited_sha = manifest.get("audited_sha")
    if not isinstance(audited_sha, str) or re.fullmatch(r"[0-9a-f]{40}", audited_sha) is None:
        errors.append("audited SHA is missing or malformed")
    if expected_main_sha and audited_sha != expected_main_sha:
        errors.append("audited SHA does not match expected main SHA")

    repository = manifest.get("repository")
    if not isinstance(repository, str) or repository.count("/") != 1:
        errors.append("repository identity is missing or malformed")

    pr_records = _records(prs_data, "pull_requests", "PR inventory", errors)
    comment_records = _records(comments_data, "comments", "comments", errors)
    review_records = _records(reviews_data, "reviews", "reviews", errors)
    thread_records = _records(threads_data, "threads", "threads", errors)

    _require_unique(pr_records, "number", "PR", errors)
    _require_unique(comment_records, "id", "comment", errors)
    _require_unique(review_records, "id", "review", errors)
    _require_unique(thread_records, "id", "thread", errors)

    pr_numbers = {record.get("number") for record in pr_records if isinstance(record.get("number"), int)}
    if len(pr_numbers) != len(pr_records):
        errors.append("every PR record must have a unique integer number")
    for record in pr_records:
        if not record.get("merged_at") or not record.get("merge_commit_sha"):
            errors.append(f"PR {record.get('number')} lacks merged_at or merge_commit_sha")
    for label, records in (("comment", comment_records), ("review", review_records), ("thread", thread_records)):
        for record in records:
            if record.get("pr_number") not in pr_numbers:
                errors.append(f"{label} is not mapped to an inventoried PR: {record.get('id')}")

    comments_by_pr_kind: Counter[tuple[int, str]] = Counter()
    for record in comment_records:
        pr_number = record.get("pr_number")
        kind = record.get("kind")
        if isinstance(pr_number, int) and isinstance(kind, str):
            comments_by_pr_kind[(pr_number, kind)] += 1
        if kind == "inline_review_comment" and record.get("in_reply_to_id") is not None:
            parent_ids = {item.get("id") for item in comment_records if item.get("kind") == "inline_review_comment"}
            if record.get("in_reply_to_id") not in parent_ids:
                errors.append(f"inline reply parent missing: {record.get('in_reply_to_id')}")

    reviews_by_pr = Counter(record.get("pr_number") for record in review_records)
    threads_by_pr = Counter(record.get("pr_number") for record in thread_records)

    counts = manifest.get("counts")
    if not isinstance(counts, dict):
        errors.append("manifest counts must be an object")
        counts = {}
    actual_counts = {
        "merged_pull_requests": len(pr_records),
        "issue_comments": sum(record.get("kind") == "issue_comment" for record in comment_records),
        "inline_review_comments": sum(record.get("kind") == "inline_review_comment" for record in comment_records),
        "review_submissions": len(review_records),
        "review_threads": len(thread_records),
    }
    for key, actual in actual_counts.items():
        if counts.get(key) != actual:
            errors.append(f"manifest count mismatch for {key}: {counts.get(key)!r} != {actual}")

    retrievals = manifest.get("retrievals")
    if not isinstance(retrievals, list):
        errors.append("manifest retrievals must be an array")
        retrievals = []
    valid_retrievals: list[dict[str, Any]] = []
    for index, item in enumerate(retrievals):
        if not isinstance(item, dict):
            errors.append(f"retrievals[{index}] must be an object")
            continue
        valid_retrievals.append(item)
        if item.get("complete") is not True or item.get("errors") not in ([], None):
            errors.append(f"retrieval incomplete: {item.get('endpoint')} PR {item.get('pr_number')}")
        if not isinstance(item.get("pages"), int) or item.get("pages", -1) < 0:
            errors.append(f"retrieval has invalid page count: {item.get('endpoint')} PR {item.get('pr_number')}")
        if not isinstance(item.get("items"), int) or item.get("items", -1) < 0:
            errors.append(f"retrieval has invalid item count: {item.get('endpoint')} PR {item.get('pr_number')}")

    global_retrievals = [item for item in valid_retrievals if item.get("pr_number") is None]
    if len(global_retrievals) != 1 or global_retrievals[0].get("endpoint") != "GET /repos/{owner}/{repo}/pulls?state=closed":
        errors.append("manifest must contain exactly one global closed-PR retrieval")

    per_pr: dict[int, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for item in valid_retrievals:
        pr_number = item.get("pr_number")
        endpoint = item.get("endpoint")
        if isinstance(pr_number, int) and isinstance(endpoint, str):
            per_pr[pr_number][endpoint].append(item)
    for pr_number in sorted(pr_numbers):
        endpoints = per_pr.get(pr_number, {})
        for endpoint in PER_PR_ENDPOINTS:
            items = endpoints.get(endpoint, [])
            if len(items) != 1:
                errors.append(f"PR {pr_number} must have exactly one retrieval for {endpoint}")
                continue
            expected = {
                PER_PR_ENDPOINTS[0]: comments_by_pr_kind[(pr_number, "issue_comment")],
                PER_PR_ENDPOINTS[1]: reviews_by_pr[pr_number],
                PER_PR_ENDPOINTS[2]: comments_by_pr_kind[(pr_number, "inline_review_comment")],
                PER_PR_ENDPOINTS[3]: threads_by_pr[pr_number],
            }[endpoint]
            if items[0].get("items") != expected:
                errors.append(
                    f"PR {pr_number} retrieval count mismatch for {endpoint}: "
                    f"{items[0].get('items')!r} != {expected}"
                )
        unknown = sorted(set(endpoints) - set(PER_PR_ENDPOINTS))
        if unknown:
            errors.append(f"PR {pr_number} has unexpected retrieval endpoints: {unknown}")
    extra_retrieval_prs = sorted(set(per_pr) - pr_numbers)
    if extra_retrieval_prs:
        errors.append(f"retrievals reference non-inventoried PRs: {extra_retrieval_prs}")

    integrity = manifest.get("integrity")
    if not isinstance(integrity, dict):
        errors.append("manifest integrity must be an object")
        integrity = {}
    if integrity.get("mapping_errors") not in ([], None):
        errors.append("manifest records mapping errors")
    if integrity.get("invalid_reply_parent_ids") not in ([], None):
        errors.append("manifest records invalid reply parent IDs")
    uniqueness = integrity.get("uniqueness_checks")
    if not isinstance(uniqueness, dict):
        errors.append("manifest uniqueness_checks must be an object")
    else:
        for name in ("pull_requests", "review_comments", "issue_comments", "reviews", "threads"):
            item = uniqueness.get(name)
            if not isinstance(item, dict) or item.get("ok") is not True or item.get("duplicates_or_nulls") not in ([], None):
                errors.append(f"manifest uniqueness check failed or missing: {name}")

    evidence_hashes = integrity.get("evidence_git_blob_sha1")
    if not isinstance(evidence_hashes, dict):
        errors.append("manifest evidence_git_blob_sha1 must be an object")
    else:
        expected_names = set(EVIDENCE_FILES)
        actual_names = set(evidence_hashes)
        if actual_names != expected_names:
            errors.append(
                "manifest evidence hash coverage mismatch: "
                f"expected {sorted(expected_names)}, got {sorted(actual_names)}"
            )
        for name in EVIDENCE_FILES:
            expected = evidence_hashes.get(name)
            path = directory / name
            if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{40}", expected) is None:
                errors.append(f"manifest evidence hash missing or malformed: {name}")
                continue
            try:
                actual = _git_blob_sha1(path)
            except OSError as exc:
                errors.append(f"cannot hash evidence file {name}: {exc}")
                continue
            if actual != expected:
                errors.append(f"frozen evidence mutation detected: {name}: {actual} != {expected}")

    if manifest.get("completeness_status") != "COMPLETE":
        errors.append("inventory does not assert COMPLETE")
    if errors and manifest.get("completeness_status") == "COMPLETE":
        errors.append("COMPLETE is inconsistent with validator-detected defects")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--expected-main-sha")
    args = parser.parse_args()
    failures = validate(args.root.resolve(), args.expected_main_sha)
    if failures:
        print("\n".join(f"ERROR: {failure}" for failure in failures))
        return 1
    print("Merged-PR review inventory validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
