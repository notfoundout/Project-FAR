#!/usr/bin/env python3
"""Non-destructive branch/PR residue classifier with unique-evidence guards."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


CATEGORIES = (
    "active",
    "merged",
    "superseded",
    "frozen evidence",
    "unique unmerged evidence",
    "abandoned/divergent",
    "unknown",
)


class TriageError(ValueError):
    pass


def classify(record: dict[str, Any]) -> tuple[str, str]:
    required = {"name", "head", "unique_commit_count", "unique_paths", "frozen_evidence", "open_pr", "merged_pr", "closed_pr", "superseded_by"}
    missing = required - set(record)
    if missing:
        raise TriageError(f"{record.get('name', '<unknown>')}: missing fields {sorted(missing)}")
    if record["unique_commit_count"] is None:
        return "unknown", "unique commits were not computed; no cleanup recommendation is safe"
    if not isinstance(record["unique_commit_count"], int) or record["unique_commit_count"] < 0:
        raise TriageError(f"{record['name']}: unique_commit_count must be a non-negative integer or null")
    if record["frozen_evidence"]:
        return "frozen evidence", "retain: branch is an explicitly frozen evidence surface"
    if record["open_pr"]:
        return "active", "retain while the linked pull request is open"
    if record["merged_pr"]:
        return "merged", "eligible for later cleanup only after verifying no separate frozen-evidence policy"
    if record["superseded_by"]:
        if record["unique_commit_count"]:
            return "unique unmerged evidence", f"retain: superseded by {record['superseded_by']} but still has unique commits"
        return "superseded", f"candidate for later cleanup after review of successor {record['superseded_by']}"
    if record["unique_commit_count"]:
        return "unique unmerged evidence", "retain and adjudicate unique commits/paths before any deletion"
    if record["closed_pr"]:
        return "abandoned/divergent", "candidate for later cleanup; dry-run report is not deletion authority"
    return "unknown", "insufficient PR/evidence disposition; retain pending classification"


def classify_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("schema_version") != "far-branch-pr-snapshot/1.0":
        raise TriageError("unsupported snapshot schema")
    branches = snapshot.get("branches")
    if not isinstance(branches, list):
        raise TriageError("branches must be a list")
    names = [item.get("name") for item in branches]
    if len(names) != len(set(names)):
        raise TriageError("branch names must be unique")
    results = []
    for record in sorted(branches, key=lambda item: item["name"]):
        category, recommendation = classify(record)
        results.append({**record, "category": category, "recommendation": recommendation, "deletion_authorized": False})
    counts = {category: sum(item["category"] == category for item in results) for category in CATEGORIES}
    inventory_summary = snapshot.get("inventory_summary", {})
    if inventory_summary:
        observed = inventory_summary.get("observed_branch_count")
        if not isinstance(observed, int) or observed < len(branches):
            raise TriageError("inventory_summary.observed_branch_count must cover classified records")
        if inventory_summary.get("fully_classified_count") != len(branches):
            raise TriageError("inventory_summary.fully_classified_count must equal supplied branch records")
    return {
        "schema_version": "far-branch-pr-triage/1.0",
        "repository": snapshot.get("repository"),
        "base_commit": snapshot.get("base_commit"),
        "generated_from": snapshot.get("generated_from", "provided snapshot"),
        "destructive_actions_performed": False,
        "counts": counts,
        "inventory_summary": inventory_summary,
        "branches": results,
        "limitations": snapshot.get("limitations", []),
    }


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if completed.returncode:
        raise TriageError(completed.stderr.strip() or "git command failed")
    return completed.stdout.strip()


def local_snapshot(root: Path, base: str) -> dict[str, Any]:
    base_commit = _git(root, "rev-parse", f"{base}^{{commit}}")
    rows = _git(root, "for-each-ref", "--format=%(refname:short) %(objectname)", "refs/heads").splitlines()
    branches = []
    for row in rows:
        name, head = row.split(" ", 1)
        unique_count = int(_git(root, "rev-list", "--count", f"{base_commit}..{head}"))
        paths = _git(root, "diff", "--name-only", f"{base_commit}...{head}").splitlines()
        branches.append({"name":name,"head":head,"unique_commit_count":unique_count,"unique_paths":paths,"frozen_evidence":False,"open_pr":None,"merged_pr":None,"closed_pr":None,"superseded_by":None})
    return {"schema_version":"far-branch-pr-snapshot/1.0","repository":"local","base_commit":base_commit,"generated_from":"local git refs","branches":branches,"limitations":["Local refs do not expose GitHub PR disposition; unknown is fail-safe."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--local", action="store_true")
    parser.add_argument("--base", default="main")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.input.read_text(encoding="utf-8")) if args.input else local_snapshot(Path.cwd(), args.base)
        report = classify_snapshot(snapshot)
    except (OSError, json.JSONDecodeError, TriageError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    content = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        if args.check:
            if not args.output.is_file() or args.output.read_text(encoding="utf-8") != content:
                print(json.dumps({"error": f"stale triage report: {args.output}"}, sort_keys=True))
                return 1
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
