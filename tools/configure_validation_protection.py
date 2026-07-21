#!/usr/bin/env python3
"""Configure strict branch protection for the validator merge-authority check.

Native GitHub merge queues are not available for personal-account repositories.
This tool configures every enforceable branch-protection control and exits with
an explicit limitation when the repository is not organization-owned.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request


def request(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Project FAR validation branch protection")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", "notfoundout/Project-FAR"))
    parser.add_argument("--branch", default="main")
    parser.add_argument("--token-env", default="FAR_GITHUB_ADMIN_TOKEN")
    args = parser.parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"missing admin token in {args.token_env}")
    api = f"https://api.github.com/repos/{args.repository}"
    repository = request("GET", api, token)
    owner_type = repository.get("owner", {}).get("type")
    protection = {
        "required_status_checks": {"strict": True, "contexts": ["merge-authority"]},
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
        },
        "restrictions": None,
        "required_conversation_resolution": True,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_signatures": False,
        "lock_branch": False,
        "allow_fork_syncing": False,
    }
    result = request("PUT", f"{api}/branches/{args.branch}/protection", token, protection)
    print(json.dumps({
        "repository": args.repository,
        "branch": args.branch,
        "required_check": "merge-authority",
        "strict_up_to_date": True,
        "protection_url": result.get("url"),
        "native_merge_queue_eligible": owner_type == "Organization",
        "owner_type": owner_type,
    }, indent=2, sort_keys=True))
    if owner_type != "Organization":
        print(
            "Native GitHub merge-queue activation remains unavailable while the repository is personal-account owned. "
            "The workflow already handles merge_group events and becomes queue-ready after transfer to an eligible organization."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
