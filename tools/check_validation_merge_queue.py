#!/usr/bin/env python3
"""Fail closed unless Project FAR's native merge queue is live and correctly wired."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

EXPECTED = {
    "check_response_timeout_minutes": 60,
    "grouping_strategy": "ALLGREEN",
    "max_entries_to_build": 5,
    "max_entries_to_merge": 1,
    "merge_method": "MERGE",
    "min_entries_to_merge": 1,
    "min_entries_to_merge_wait_minutes": 0,
}


def request(url: str, token: str):
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2026-03-10",
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API {exc.code}: {detail}") from exc
    return json.loads(raw) if raw else {}


def validate_merge_queue_rule(rules: list[dict]) -> list[str]:
    errors: list[str] = []
    queue_rules = [rule for rule in rules if rule.get("type") == "merge_queue"]
    if len(queue_rules) != 1:
        return [f"expected exactly one active merge_queue rule, found {len(queue_rules)}"]
    parameters = queue_rules[0].get("parameters") or {}
    for key, expected in EXPECTED.items():
        actual = parameters.get(key)
        if actual != expected:
            errors.append(f"merge_queue.{key}: expected {expected!r}, got {actual!r}")
    return errors


def validate_workflow(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing workflow: {path}"]
    text = path.read_text(encoding="utf-8")
    required = ("merge_group:", "types: [checks_requested]", "merge-authority:")
    return [
        f"workflow missing required fragment: {fragment}"
        for fragment in required
        if fragment not in text
    ]


def validate_branch_protection(protection: dict) -> list[str]:
    errors: list[str] = []
    checks = protection.get("required_status_checks") or {}
    if checks.get("strict") is not True:
        errors.append("branch protection strict status checks are not enabled")
    contexts = set(checks.get("contexts") or [])
    if "merge-authority" not in contexts:
        errors.append("branch protection does not require merge-authority")
    if not (protection.get("required_conversation_resolution") or {}).get("enabled"):
        errors.append("conversation resolution is not required")
    if (protection.get("allow_force_pushes") or {}).get("enabled"):
        errors.append("force pushes are allowed")
    if (protection.get("allow_deletions") or {}).get("enabled"):
        errors.append("branch deletion is allowed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Project FAR canonical merge queue")
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY", "notfoundout/Project-FAR"),
    )
    parser.add_argument("--branch", default="main")
    parser.add_argument("--token-env", default="FAR_GITHUB_ADMIN_TOKEN")
    parser.add_argument("--workflow", default=".github/workflows/validator-assurance.yml")
    args = parser.parse_args()

    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"missing admin token in {args.token_env}")

    api = f"https://api.github.com/repos/{args.repository}"
    repository = request(api, token)
    errors: list[str] = []
    owner_type = repository.get("owner", {}).get("type")
    if owner_type != "Organization":
        errors.append(f"repository owner type is {owner_type!r}, expected 'Organization'")

    rules = request(f"{api}/rules/branches/{args.branch}", token)
    errors.extend(validate_merge_queue_rule(rules if isinstance(rules, list) else []))

    protection = request(f"{api}/branches/{args.branch}/protection", token)
    errors.extend(validate_branch_protection(protection))
    errors.extend(validate_workflow(Path(args.workflow)))

    payload = {
        "repository": args.repository,
        "branch": args.branch,
        "owner_type": owner_type,
        "merge_queue_enforced": not errors,
        "required_check": "merge-authority",
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
