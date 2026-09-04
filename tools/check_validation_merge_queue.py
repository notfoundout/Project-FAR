#!/usr/bin/env python3
"""Fail closed unless Project FAR's native merge queue is live and correctly wired."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlencode

RULESET_NAME = "Project FAR Canonical Merge Queue"
PAGE_SIZE = 100
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


def list_repository_rulesets(api: str, token: str) -> list[dict]:
    collected: list[dict] = []
    page = 1
    while True:
        query = urlencode(
            {
                "includes_parents": "false",
                "per_page": PAGE_SIZE,
                "page": page,
            }
        )
        payload = request(f"{api}/rulesets?{query}", token)
        if not isinstance(payload, list):
            raise SystemExit("GitHub rulesets list endpoint returned a non-list payload")
        collected.extend(payload)
        if len(payload) < PAGE_SIZE:
            return collected
        page += 1


def validate_merge_queue_parameters(parameters: dict) -> list[str]:
    errors: list[str] = []
    for key, expected in EXPECTED.items():
        actual = parameters.get(key)
        if actual != expected:
            errors.append(f"merge_queue.{key}: expected {expected!r}, got {actual!r}")
    return errors


def validate_canonical_ruleset(ruleset: dict) -> list[str]:
    errors: list[str] = []
    if ruleset.get("name") != RULESET_NAME:
        errors.append(f"ruleset name mismatch: {ruleset.get('name')!r}")
    if ruleset.get("target") != "branch":
        errors.append(f"ruleset target must be 'branch', got {ruleset.get('target')!r}")
    if ruleset.get("enforcement") != "active":
        errors.append(f"ruleset enforcement must be 'active', got {ruleset.get('enforcement')!r}")
    if ruleset.get("bypass_actors") not in ([], None):
        errors.append(f"ruleset bypass_actors must be empty, got {ruleset.get('bypass_actors')!r}")
    conditions = ruleset.get("conditions") or {}
    ref_name = conditions.get("ref_name") or {}
    if ref_name.get("include") != ["~DEFAULT_BRANCH"]:
        errors.append(
            "ruleset include scope must be exactly ['~DEFAULT_BRANCH'], "
            f"got {ref_name.get('include')!r}"
        )
    if ref_name.get("exclude") != []:
        errors.append(f"ruleset exclude scope must be empty, got {ref_name.get('exclude')!r}")

    rules = ruleset.get("rules") or []
    queue_rules = [rule for rule in rules if rule.get("type") == "merge_queue"]
    if len(queue_rules) != 1:
        errors.append(f"expected exactly one merge_queue rule in canonical ruleset, found {len(queue_rules)}")
    if len(rules) != 1:
        errors.append(f"canonical ruleset must contain exactly one rule, found {len(rules)}")
    if len(queue_rules) == 1:
        errors.extend(validate_merge_queue_parameters(queue_rules[0].get("parameters") or {}))
    return errors


def select_canonical_ruleset(rulesets: list[dict]) -> tuple[dict | None, list[str]]:
    matches = [
        item
        for item in rulesets
        if item.get("source_type") == "Repository"
        and item.get("name") == RULESET_NAME
    ]
    if len(matches) != 1:
        return None, [f"expected exactly one repository canonical ruleset, found {len(matches)}"]
    if not matches[0].get("id"):
        return None, ["canonical ruleset has no id"]
    return matches[0], []


def validate_active_branch_rules(rules: list[dict]) -> list[str]:
    queue_rules = [rule for rule in rules if rule.get("type") == "merge_queue"]
    if len(queue_rules) != 1:
        return [f"expected exactly one active merge_queue rule on main, found {len(queue_rules)}"]
    return validate_merge_queue_parameters(queue_rules[0].get("parameters") or {})


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

    rulesets = list_repository_rulesets(api, token)
    canonical_summary, selection_errors = select_canonical_ruleset(rulesets)
    errors.extend(selection_errors)
    ruleset_id = None
    if canonical_summary is not None:
        ruleset_id = canonical_summary["id"]
        canonical = request(f"{api}/rulesets/{ruleset_id}", token)
        errors.extend(validate_canonical_ruleset(canonical))

    active_rules = request(f"{api}/rules/branches/{args.branch}", token)
    errors.extend(validate_active_branch_rules(active_rules if isinstance(active_rules, list) else []))

    protection = request(f"{api}/branches/{args.branch}/protection", token)
    errors.extend(validate_branch_protection(protection))
    errors.extend(validate_workflow(Path(args.workflow)))

    payload = {
        "repository": args.repository,
        "branch": args.branch,
        "owner_type": owner_type,
        "ruleset_id": ruleset_id,
        "ruleset_name": RULESET_NAME,
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
