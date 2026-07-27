#!/usr/bin/env python3
"""Fail-closed checks for the merged-pull-request review inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REL = pathlib.Path("docs/audits/merged-pr-review-audit")


def _load(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc


def _duplicates(records: list[dict], key: str, kind: str) -> list[str]:
    errors: list[str] = []
    seen: dict[object, dict] = {}
    for record in records:
        value = record.get(key)
        if value is None or value == "":
            errors.append(f"{kind} lacks {key}")
        elif value in seen and seen[value] != record:
            errors.append(f"duplicate conflicting {kind} {key}: {value}")
        else:
            seen[value] = record
    return errors


def validate(root: pathlib.Path = ROOT, expected_main_sha: str | None = None) -> list[str]:
    errors: list[str] = []
    directory = root / REL
    try:
        prs = _load(directory / "raw-pr-inventory.json")
        comments = _load(directory / "raw-review-comments.json")
        threads = _load(directory / "raw-review-threads.json")
        manifest = _load(directory / "retrieval-manifest.json")
    except ValueError as exc:
        return [str(exc)]

    sha = manifest.get("audited_main_sha")
    if not sha:
        errors.append("audited main SHA is missing")
    for name, data in (("PR inventory", prs), ("comments", comments), ("threads", threads)):
        if data.get("audited_main_sha") != sha:
            errors.append(f"{name} audited main SHA disagrees with manifest")
    if expected_main_sha and sha != expected_main_sha:
        errors.append("audited main SHA does not match expected main SHA")

    pr_records = prs.get("records", [])
    comment_records = comments.get("records", [])
    thread_records = threads.get("records", [])
    pr_numbers = [record.get("pr_number") for record in pr_records]
    if len(pr_numbers) != len(set(pr_numbers)):
        errors.append("duplicate PR number")
    for record in pr_records:
        if not record.get("retrieval_status"):
            errors.append(f"PR {record.get('pr_number')} lacks explicit retrieval status")

    counts = manifest.get("counts", {})
    reported = counts.get("merged_prs_reported_by_github")
    retrieved = counts.get("merged_prs_retrieved_from_github")
    if reported is not None and retrieved != reported:
        errors.append("merged PR reported/retrieved count mismatch (missing PR)")
    inferred = counts.get("merged_prs_inferred_from_git_history")
    if inferred != len(pr_records):
        errors.append("PR inventory count disagrees with manifest")

    errors += _duplicates(comment_records, "source_id", "comment")
    errors += _duplicates(thread_records, "thread_id", "thread")
    for record in comment_records:
        if record.get("pr_number") not in pr_numbers:
            errors.append(f"review object is not mapped to an inventoried PR: {record.get('source_id')}")
        if record.get("record_type") == "review_submission" and not record.get("review_id"):
            errors.append(f"review submission lacks review ID: {record.get('source_id')}")
    for record in thread_records:
        if record.get("pr_number") not in pr_numbers:
            errors.append(f"thread is not mapped to an inventoried PR: {record.get('thread_id')}")

    expected_comments = counts.get("review_submissions_retrieved", 0) + counts.get("inline_comments_retrieved", 0) + counts.get("issue_comments_inspected", 0)
    if expected_comments != len(comment_records):
        errors.append("comment count disagrees with raw inventory")
    if counts.get("threads_retrieved") != len(thread_records):
        errors.append("thread count disagrees with raw inventory")

    pagination = manifest.get("pagination", {})
    if pagination.get("complete"):
        pages = pagination.get("pages_or_cursors", [])
        if pagination.get("page_count") != len(pages) or pagination.get("skipped_pages"):
            errors.append("pagination is incomplete or a page was skipped")
    elif manifest.get("completeness_status") == "COMPLETE":
        errors.append("COMPLETE asserted with incomplete pagination")

    failed = any(
        status == "failed"
        for item in manifest.get("counts_per_pr", [])
        for endpoint in item.values() if isinstance(endpoint, dict)
        for status in [endpoint.get("status")]
    )
    if failed and not manifest.get("retrieval_errors"):
        errors.append("API failure is not reported")
    if manifest.get("retrieval_errors") and not manifest.get("api_or_permission_limitations"):
        errors.append("retrieval limitation is omitted")
    if manifest.get("completeness_status") not in {"COMPLETE", "INCOMPLETE", "REVIEW_REQUIRED"}:
        errors.append("invalid completeness status")
    if manifest.get("completeness_status") == "COMPLETE":
        if reported is None or reported != retrieved or manifest.get("retrieval_errors") or manifest.get("inaccessible_records"):
            errors.append("COMPLETE does not satisfy the completeness contract")

    for item in manifest.get("frozen_evidence_baseline", []):
        path = root / item.get("path", "")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item.get("sha256"):
            errors.append(f"frozen-evidence mutation detected: {item.get('path')}")
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
