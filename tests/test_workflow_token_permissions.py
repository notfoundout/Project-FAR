"""Repository code that a pull request can change must never run with a write token."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github/workflows").glob("*.yml"))

# Events whose jobs run code that the pull request, or its merge-queue entry, supplies.
CANDIDATE_EVENTS = {"pull_request", "pull_request_target", "merge_group"}

# Locked workflows that may still declare no permissions. They change only through owner-signed
# repins, and they receive the repository's default token (Contents, Metadata, Packages: read, as
# each job log's "GITHUB_TOKEN Permissions" group shows). PR #538 gives lean.yml a declaration.
LOCKED_WITHOUT_PERMISSIONS = {"lean.yml", "repo-health.yml", "specification-export.yml"}

EVENT_TEST = re.compile(r"github\.event_name\s*==\s*'([a-z_]+)'")


def _split(expr, op):
    parts, depth, start, i = [], 0, 0, 0
    while i < len(expr):
        char = expr[i]
        if char == "'":
            i = expr.index("'", i + 1)
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif depth == 0 and expr.startswith(op, i):
            parts.append(expr[start:i].strip())
            start = i = i + len(op)
            continue
        i += 1
    parts.append(expr[start:].strip())
    return parts


def _closing_paren(expr):
    depth, i = 0, 0
    while i < len(expr):
        char = expr[i]
        if char == "'":
            i = expr.index("'", i + 1)
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _strip_parens(expr):
    while expr.startswith("(") and _closing_paren(expr) == len(expr) - 1:
        expr = expr[1:-1].strip()
    return expr


def excludes_candidate_events(condition):
    """True only if every disjunct requires a non-candidate github.event_name (sufficient, not necessary)."""
    if not isinstance(condition, str):
        return False
    expr = condition.strip()
    if expr.startswith("${{") and expr.endswith("}}"):
        expr = expr[3:-2].strip()
    for disjunct in _split(_strip_parens(expr), "||"):
        conjuncts = [_strip_parens(c) for c in _split(_strip_parens(disjunct), "&&")]
        if not any(
            (match := EVENT_TEST.fullmatch(c)) and match.group(1) not in CANDIDATE_EVENTS
            for c in conjuncts
        ):
            return False
    return True


def _grants_write(permissions):
    if permissions == "write-all":
        return True
    return isinstance(permissions, dict) and "write" in permissions.values()


def _events(workflow):
    on = workflow.get("on", workflow.get(True))
    if isinstance(on, str):
        return {on}
    return set(on or [])


def write_jobs_reachable_from_candidate_code(workflow):
    if not _events(workflow) & CANDIDATE_EVENTS:
        return []
    top = workflow.get("permissions")
    return [
        name
        for name, job in workflow.get("jobs", {}).items()
        if _grants_write(job.get("permissions", top)) and not excludes_candidate_events(job.get("if"))
    ]


class WorkflowTokenPermissionTests(unittest.TestCase):
    def test_no_job_that_runs_for_a_pull_request_holds_a_write_token(self):
        offenders = {
            path.name: jobs
            for path in WORKFLOWS
            if (jobs := write_jobs_reachable_from_candidate_code(yaml.safe_load(path.read_text())))
        }
        self.assertEqual(offenders, {})

    def test_every_unlocked_workflow_declares_its_token_permissions(self):
        undeclared = []
        for path in WORKFLOWS:
            workflow = yaml.safe_load(path.read_text())
            if "permissions" in workflow:
                continue
            if all("permissions" in job for job in workflow.get("jobs", {}).values()):
                continue
            undeclared.append(path.name)
        self.assertLessEqual(set(undeclared), LOCKED_WITHOUT_PERMISSIONS)

    def test_a_workflow_wide_write_token_on_pull_request_is_rejected(self):
        workflow = {
            "on": {"pull_request": {}, "push": {}},
            "permissions": {"contents": "write"},
            "jobs": {
                "build": {"steps": []},
                "publish": {"if": "github.event_name == 'push'", "steps": []},
            },
        }
        self.assertEqual(write_jobs_reachable_from_candidate_code(workflow), ["build"])
        workflow["permissions"] = {"contents": "read"}
        workflow["jobs"]["publish"]["permissions"] = {"contents": "write"}
        self.assertEqual(write_jobs_reachable_from_candidate_code(workflow), [])
        workflow["jobs"]["build"]["permissions"] = "write-all"
        self.assertEqual(write_jobs_reachable_from_candidate_code(workflow), ["build"])

    def test_condition_is_accepted_only_when_every_branch_excludes_pull_requests(self):
        accepted = [
            "github.event_name == 'push'",
            "${{ github.event_name == 'push' }}",
            "always() && github.event_name == 'workflow_dispatch'",
            "github.event_name == 'schedule' || (github.event_name == 'workflow_dispatch' && inputs.mode == 'review')",
            "(github.event_name == 'workflow_dispatch' && inputs.stage == 'a || b')",
        ]
        rejected = [
            None,
            "always()",
            "github.event_name != 'pull_request'",
            "github.event_name == 'pull_request'",
            "github.event_name == 'merge_group'",
            "github.event_name == 'push' || inputs.force",
            "github.event_name == 'push' || github.event_name == 'pull_request_target'",
            "!(github.event_name == 'pull_request')",
            "(github.event_name == 'push') || (inputs.force)",
        ]
        for condition in accepted:
            self.assertTrue(excludes_candidate_events(condition), condition)
        for condition in rejected:
            self.assertFalse(excludes_candidate_events(condition), condition)


if __name__ == "__main__":
    unittest.main()
