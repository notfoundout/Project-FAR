#!/usr/bin/env python3
"""Configure the canonical Project FAR merge queue after organization transfer."""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlencode

RULESET_NAME = "Project FAR Canonical Merge Queue"
PAGE_SIZE = 100


def request(method: str, url: str, token: str, payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2026-03-10",
            "Content-Type": "application/json",
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
    """Traverse every repository-ruleset page before deciding create vs update."""
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
        payload = request("GET", f"{api}/rulesets?{query}", token)
        if not isinstance(payload, list):
            raise SystemExit("GitHub rulesets list endpoint returned a non-list payload")
        collected.extend(payload)
        if len(payload) < PAGE_SIZE:
            return collected
        page += 1


def desired_ruleset() -> dict:
    # Conservative queue policy: one PR per merge group. This preserves the
    # latest-base retest/serialization benefit without batching unrelated PRs.
    return {
        "name": RULESET_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {
            "ref_name": {
                "include": ["~DEFAULT_BRANCH"],
                "exclude": [],
            }
        },
        "rules": [
            {
                "type": "merge_queue",
                "parameters": {
                    "check_response_timeout_minutes": 60,
                    "grouping_strategy": "ALLGREEN",
                    "max_entries_to_build": 5,
                    "max_entries_to_merge": 1,
                    "merge_method": "MERGE",
                    "min_entries_to_merge": 1,
                    "min_entries_to_merge_wait_minutes": 0,
                },
            }
        ],
    }


def require_organization(repository: dict) -> None:
    owner_type = repository.get("owner", {}).get("type")
    if owner_type != "Organization":
        raise SystemExit(
            "native merge queue blocked: repository owner type is "
            f"{owner_type!r}, expected 'Organization'"
        )


def select_existing_canonical_ruleset(rulesets: list[dict]) -> dict | None:
    matches = [
        item
        for item in rulesets
        if item.get("source_type") == "Repository"
        and item.get("name") == RULESET_NAME
    ]
    if len(matches) > 1:
        ids = [item.get("id") for item in matches]
        raise SystemExit(f"duplicate canonical merge-queue rulesets already exist: {ids}")
    return matches[0] if matches else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Project FAR canonical merge queue")
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY", "notfoundout/Project-FAR"),
    )
    parser.add_argument("--token-env", default="FAR_GITHUB_ADMIN_TOKEN")
    args = parser.parse_args()

    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"missing admin token in {args.token_env}")

    api = f"https://api.github.com/repos/{args.repository}"
    repository = request("GET", api, token)
    require_organization(repository)

    rulesets = list_repository_rulesets(api, token)
    existing = select_existing_canonical_ruleset(rulesets)
    payload = desired_ruleset()
    if existing is None:
        result = request("POST", f"{api}/rulesets", token, payload)
        action = "created"
    else:
        ruleset_id = existing.get("id")
        if not ruleset_id:
            raise SystemExit("existing canonical merge-queue ruleset has no id")
        result = request("PUT", f"{api}/rulesets/{ruleset_id}", token, payload)
        action = "updated"

    print(
        json.dumps(
            {
                "action": action,
                "repository": args.repository,
                "owner_type": repository.get("owner", {}).get("type"),
                "ruleset_id": result.get("id"),
                "ruleset_name": result.get("name", RULESET_NAME),
                "enforcement": result.get("enforcement"),
                "merge_queue_required": True,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
