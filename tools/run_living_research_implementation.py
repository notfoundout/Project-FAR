#!/usr/bin/env python3
"""Create a separate PR for exact protected-authorized living-research implementation bytes."""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any

from tools.living_implementation_contract import ImplementationContractError, build_plan, load_json, sha256
from tools.materialize_living_implementation import materialize

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PR = 490
SOURCE_BRANCH = "automation/living-research-inbox"
BASE_BRANCH = "main"
POLICY = Path("research/living/implementation-policy-v1.0.json")


class RunnerError(RuntimeError):
    pass


def run(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(list(args), cwd=ROOT, text=text, capture_output=True)
    if check and result.returncode:
        stderr = result.stderr.decode() if isinstance(result.stderr, bytes) else result.stderr
        stdout = result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout
        raise RunnerError(f"{' '.join(args)} failed: {(stderr or stdout or '').strip()}")
    return result


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def gh(*args: str, check: bool = True) -> str:
    return run("gh", *args, check=check).stdout.strip()


def source_snapshot() -> str:
    raw = gh(
        "pr", "view", str(SOURCE_PR), "--repo", os.environ["GITHUB_REPOSITORY"],
        "--json", "state,isDraft,baseRefName,headRefName,headRefOid",
    )
    data = json.loads(raw)
    expected = {"state": "OPEN", "isDraft": True, "baseRefName": BASE_BRANCH, "headRefName": SOURCE_BRANCH}
    for key, wanted in expected.items():
        if data.get(key) != wanted:
            raise RunnerError(f"PR #490 identity invariant failed: {key}")
    head = data.get("headRefOid")
    if not isinstance(head, str) or len(head) != 40 or any(ch not in "0123456789abcdef" for ch in head):
        raise RunnerError("PR #490 did not return an exact lowercase 40-hex head SHA")
    return head


def fetch_inputs() -> None:
    git(
        "fetch", "--no-tags", "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        f"+refs/heads/{SOURCE_BRANCH}:refs/remotes/origin/{SOURCE_BRANCH}",
    )


def export_source(commit: str, destination: Path) -> None:
    archive = run("git", "archive", "--format=tar", commit, text=False).stdout
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as handle:
        handle.extractall(destination, filter="data")


def branch_name(policy: dict[str, Any], source_sha: str, base_sha: str) -> str:
    return f"{policy['branch_prefix']}{source_sha}-{base_sha}"


def planned_paths(plan: dict[str, Any]) -> set[str]:
    paths = {op["path"] for proposal in plan["proposals"] for op in proposal["operations"]}
    paths.add(plan["manifest_path"])
    return paths


def expected_sealed_rows(plan: dict[str, Any]) -> list[dict[str, str]]:
    rows = [
        {"path": op["path"], "sha256": op["result_sha256"], "proposal_id": proposal["proposal_id"]}
        for proposal in plan["proposals"]
        for op in proposal["operations"]
    ]
    return sorted(rows, key=lambda row: row["path"])


def changed_paths() -> set[str]:
    modified = {x for x in git("diff", "--name-only", "--").splitlines() if x}
    untracked = {x for x in git("ls-files", "--others", "--exclude-standard").splitlines() if x}
    return modified | untracked


def verify_existing(branch: str, plan: dict[str, Any]) -> str:
    git("fetch", "--no-tags", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
    head = git("rev-parse", f"origin/{branch}^{{commit}}")
    ancestry = git("rev-list", "--parents", "-n", "1", head).split()
    if len(ancestry) != 2 or ancestry[1] != plan["base_main_sha"]:
        raise RunnerError("existing implementation branch must be exactly one single-parent commit on its frozen base")
    if int(git("rev-list", "--count", f"{plan['base_main_sha']}..{head}")) != 1:
        raise RunnerError("existing implementation branch contains more than one commit")
    raw = run("git", "show", f"{head}:{plan['manifest_path']}", text=False).stdout
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise RunnerError(f"existing implementation manifest is invalid JSON: {exc}") from exc
    required_keys = {
        "schema_version", "program_id", "source_pr", "source_branch", "source_head_sha",
        "base_main_sha", "proposals", "sealed_files",
    }
    if not isinstance(manifest, dict) or set(manifest) != required_keys:
        raise RunnerError("existing implementation manifest fields are malformed")
    identity = {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-IMPLEMENTATION-001",
        "source_pr": 490,
        "source_branch": plan["source_branch"],
        "source_head_sha": plan["source_head_sha"],
        "base_main_sha": plan["base_main_sha"],
    }
    if any(manifest.get(key) != value for key, value in identity.items()):
        raise RunnerError("existing implementation manifest identity mismatch")
    if manifest.get("proposals") != plan["proposals"]:
        raise RunnerError("existing implementation manifest proposals differ from protected plan")
    expected_rows = expected_sealed_rows(plan)
    if manifest.get("sealed_files") != expected_rows:
        raise RunnerError("existing implementation manifest seal set differs from protected plan")
    expected_paths = {row["path"] for row in expected_rows} | {plan["manifest_path"]}
    changed = {
        x for x in git("diff", "--name-only", "--no-renames", plan["base_main_sha"], head, "--").splitlines() if x
    }
    if changed != expected_paths:
        raise RunnerError("existing implementation branch has unsealed paths")
    for row in expected_rows:
        blob = run("git", "show", f"{head}:{row['path']}", text=False).stdout
        if sha256(blob) != row["sha256"]:
            raise RunnerError(f"existing implementation seal mismatch: {row['path']}")
    return head


def remote_branch_exists(branch: str) -> bool:
    return run("git", "ls-remote", "--exit-code", "--heads", "origin", branch, check=False).returncode == 0


def create_or_recover_pr(branch: str, plan: dict[str, Any], sensitive: bool) -> tuple[int, bool]:
    repo = os.environ["GITHUB_REPOSITORY"]
    existing = gh(
        "pr", "list", "--repo", repo, "--head", branch, "--base", BASE_BRANCH,
        "--state", "open", "--json", "number", "--jq", ".[0].number // empty",
    )
    if existing:
        return int(existing), False
    closed = gh(
        "pr", "list", "--repo", repo, "--head", branch, "--base", BASE_BRANCH,
        "--state", "closed", "--json", "number", "--jq", ".[0].number // empty",
    )
    if closed:
        raise RunnerError(f"implementation branch has a closed PR #{closed}; automation will not override that review decision")
    body = [
        "## Result",
        "",
        f"Automatic implementation PR for protected-authorized living research from permanent PR #490 head `{plan['source_head_sha']}` against protected `main` `{plan['base_main_sha']}`.",
        "",
        f"- implementation proposals: {len(plan['proposals'])}",
        f"- changed implementation files: {sum(len(x['operations']) for x in plan['proposals'])}",
        f"- merge-authority self-surface touched: {'yes' if sensitive else 'no'}",
        "",
        "## Trust boundary",
        "",
        "The write-scoped materializer executed only code already present on protected main. Inbox payload bytes were hash-checked, copied, sealed, and never executed by the materialization job. This PR does not write directly to main and does not bypass protected review.",
    ]
    if sensitive:
        body += [
            "",
            "Because this proposal changes merge-authority's own assurance surface, automation deliberately did not self-dispatch merge-authority from this branch. The PR requires independent protected review/validation of that self-change.",
        ]
    body_path = Path(tempfile.gettempdir()) / "living-implementation-pr.md"
    body_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    created = gh(
        "pr", "create", "--repo", repo, "--base", BASE_BRANCH, "--head", branch,
        "--title", "Implementation: protected living-research project correction",
        "--body-file", str(body_path),
    )
    number = int(gh("pr", "view", created, "--repo", repo, "--json", "number", "--jq", ".number"))
    return number, True


def assurance_sensitive(plan: dict[str, Any], policy: dict[str, Any]) -> bool:
    protected = set(policy.get("assurance_sensitive_exact_paths", []))
    return any(op["path"] in protected for proposal in plan["proposals"] for op in proposal["operations"])


def main() -> int:
    if not os.environ.get("GITHUB_REPOSITORY") or not os.environ.get("GH_TOKEN"):
        raise RunnerError("GITHUB_REPOSITORY and GH_TOKEN are required")
    first_source = source_snapshot()
    fetch_inputs()
    if git("rev-parse", f"origin/{SOURCE_BRANCH}^{{commit}}") != first_source:
        raise RunnerError("PR #490 head differs from fetched source")
    git("switch", "--detach", "origin/main")
    base_sha = git("rev-parse", "HEAD^{commit}")
    policy = load_json(ROOT / POLICY)

    with tempfile.TemporaryDirectory(prefix="far-living-implementation-") as tmp:
        source_root = Path(tmp) / "source"
        export_source(first_source, source_root)
        plan = build_plan(ROOT, source_root, source_sha=first_source, base_sha=base_sha)
        print(json.dumps({
            "source_head": first_source,
            "base_main": base_sha,
            "actionable": plan["actionable"],
            "proposals": len(plan["proposals"]),
        }, sort_keys=True))
        if not plan["actionable"]:
            return 0
        branch = branch_name(policy, first_source, base_sha)
        sensitive = assurance_sensitive(plan, policy)
        fresh = not remote_branch_exists(branch)
        if fresh:
            git("switch", "-c", branch, base_sha)
            materialize(ROOT, source_root, plan)
            observed = changed_paths()
            expected = planned_paths(plan)
            if observed != expected:
                raise RunnerError(f"materializer changed unexpected paths: observed={sorted(observed)} expected={sorted(expected)}")
            for path in sorted(expected):
                git("add", "--", path)
            staged = {x for x in git("diff", "--cached", "--name-only", "--").splitlines() if x}
            if staged != expected:
                raise RunnerError("staged implementation paths differ from sealed plan")
            second_source = source_snapshot()
            fetch_inputs()
            if second_source != first_source or git("rev-parse", f"origin/{SOURCE_BRANCH}^{{commit}}") != first_source:
                raise RunnerError("PR #490 advanced during implementation materialization")
            if git("rev-parse", "origin/main^{commit}") != base_sha:
                raise RunnerError("main advanced during implementation materialization")
            git("config", "user.name", "project-far-implementation-bot")
            git("config", "user.email", "project-far-implementation-bot@users.noreply.github.com")
            git("commit", "-m", f"implementation: materialize protected living-research correction {first_source}")
            local_head = git("rev-parse", "HEAD^{commit}")
            ancestry = git("rev-list", "--parents", "-n", "1", local_head).split()
            if len(ancestry) != 2 or ancestry[1] != base_sha:
                raise RunnerError("implementation branch is not exactly one single-parent commit on frozen main")
            git("push", "origin", f"HEAD:refs/heads/{branch}")
            head = verify_existing(branch, plan)
            if head != local_head:
                raise RunnerError("remote implementation head differs from exact locally sealed commit")
        else:
            head = verify_existing(branch, plan)
        pr_number, created = create_or_recover_pr(branch, plan, sensitive)
        if not sensitive:
            checks = gh(
                "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/commits/{head}/check-runs",
                "--jq", '[.check_runs[] | select(.name == "merge-authority")] | length',
            )
            if int(checks) == 0:
                gh("workflow", "run", "validator-assurance.yml", "--repo", os.environ["GITHUB_REPOSITORY"], "--ref", branch)
        print(f"Implementation PR #{pr_number} is open for exact head {head}; protected merge remains controlling. created={created} sensitive={sensitive}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RunnerError, ImplementationContractError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"living implementation runner failed closed: {exc}", file=sys.stderr)
        raise SystemExit(2)
