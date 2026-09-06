"""Exercise the reviewed inline one-shot without network or real credentials.

After protected cleanup, the receipt/absence gate replaces execution of the
removed one-shot; test identities remain stable across that lifecycle.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/retire-far-github-admin-token.yml"
RECEIPT = ROOT / "theory/evaluation/privileged-token-retirement-v1.0.json"
LEGACY = ["canonical-branch-protection.yml", "configure-validation-protection.yml"]


def policy():
    result = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["merge-authority"],
            "checks": [{"context": "merge-authority", "app_id": 15368}],
        },
        "enforce_admins": {"enabled": True},
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
        },
        "restrictions": None,
    }
    for key in ("required_conversation_resolution", "required_linear_history",
                "allow_force_pushes", "allow_deletions", "block_creations",
                "required_signatures", "lock_branch", "allow_fork_syncing"):
        result[key] = {"enabled": key == "required_conversation_resolution"}
    return result


class PrivilegedTokenRetirementTests(unittest.TestCase):
    def retired(self):
        if WORKFLOW.exists():
            return False
        receipt = json.loads(RECEIPT.read_text())
        self.assertEqual(receipt["status"], "ACCEPTED_RETIRED")
        self.assertTrue(receipt["accepted_receipt"]["secret_absent"])
        self.assertTrue(receipt["accepted_receipt"]["branch_protection_unchanged_and_enforced"])
        self.assertEqual(receipt["accepted_receipt"]["privileged_workflow_states"],
                         {name: "disabled_manually" for name in LEGACY})
        return True

    def execute(self, *, token="fake-admin", before=None, after=None,
                state="disabled_manually", fail_request=None, repository=None):
        workflow = yaml.safe_load(WORKFLOW.read_text())
        shell = workflow["jobs"]["retire"]["steps"][0]["run"]
        code = shell.split("python - <<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
        before = policy() if before is None else before
        after = copy.deepcopy(before) if after is None else after
        calls = []
        protection_reads = 0

        def urlopen(req):
            nonlocal protection_reads
            path = req.full_url.split("/repos/notfoundout/Project-FAR", 1)[1]
            calls.append((req.method, path, req.headers.get("Authorization")))
            if fail_request == (req.method, path):
                raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, io.BytesIO(b"denied"))
            if path.endswith("/protection"):
                protection_reads += 1
                data = before if protection_reads == 1 else after
            elif path == "/branches/main":
                data = {"protected": True, "protection": {"enabled": True,
                    "required_status_checks": {"enforcement_level": "everyone",
                    "contexts": ["merge-authority"],
                    "checks": [{"context": "merge-authority", "app_id": 15368}]}}}
            elif req.method == "GET" and "/actions/workflows/" in path:
                data = {"state": state}
            elif req.method in ("PUT", "DELETE"):
                data = {}
            else:
                raise AssertionError((req.method, path))
            return io.BytesIO(json.dumps(data).encode())

        env = {"GITHUB_REPOSITORY": repository or "notfoundout/Project-FAR",
               "GITHUB_REF": "refs/heads/main", "FAR_GITHUB_ADMIN_TOKEN": token,
               "GITHUB_WORKFLOW_TOKEN": "fake-workflow"}
        output = io.StringIO()
        exit_code = 0
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", urlopen), contextlib.redirect_stdout(output):
            try:
                exec(compile(code, str(WORKFLOW), "exec"), {})
            except SystemExit as exc:
                exit_code = exc.code
        self.assertNotIn("fake-admin", output.getvalue())
        self.assertNotIn("fake-workflow", output.getvalue())
        return exit_code, output.getvalue(), calls

    def test_success_checks_policy_disables_then_deletes_last(self):
        if self.retired():
            return
        code, output, calls = self.execute()
        self.assertEqual(code, 0)
        receipt = json.loads(output)
        self.assertEqual(receipt["branch_protection"], policy())
        self.assertEqual(calls[-1][:2], ("DELETE", "/actions/secrets/FAR_GITHUB_ADMIN_TOKEN"))
        self.assertEqual(len(calls), 7)
        for method, path, credential in calls:
            self.assertEqual(credential, "Bearer fake-workflow" if "/workflows/" in path else "Bearer fake-admin")
            self.assertFalse(method in ("PUT", "DELETE") and "/protection" in path)

    def test_recovery_after_lost_deletion_receipt_needs_no_admin(self):
        if self.retired():
            return
        code, output, calls = self.execute(token="")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["mode"], "credentialless_recovery")
        self.assertTrue(all(method == "GET" for method, _, _ in calls))
        self.assertEqual(len(calls), 3)

    def test_recovery_cannot_accept_active_workflow(self):
        if self.retired():
            return
        code, output, calls = self.execute(token="", state="active")
        self.assertNotEqual(code, 0)
        self.assertEqual(output, "")
        self.assertTrue(all(method == "GET" for method, _, _ in calls))

    def test_weakened_policy_and_application_binding_fail_before_mutation(self):
        if self.retired():
            return
        for field, value in (("enforce_admins", {"enabled": False}),
                             ("required_pull_request_reviews", None),
                             ("required_status_checks", None),
                             ("allow_force_pushes", {"enabled": True}),
                             ("allow_deletions", {"enabled": True}),
                             ("required_conversation_resolution", {"enabled": False})):
            with self.subTest(field=field):
                weakened = policy()
                weakened[field] = value
                code, output, calls = self.execute(before=weakened)
                self.assertNotEqual(code, 0)
                self.assertEqual(output, "")
                self.assertEqual([c[0] for c in calls], ["GET"])
        weakened = policy()
        weakened["required_status_checks"]["checks"][0]["app_id"] = -1
        code, _, calls = self.execute(before=weakened)
        self.assertNotEqual(code, 0)
        self.assertEqual(len(calls), 1)

    def test_policy_drift_and_api_failure_preserve_deletion_recovery_path(self):
        if self.retired():
            return
        changed = policy()
        changed["new_control"] = True
        code, _, calls = self.execute(after=changed)
        self.assertNotEqual(code, 0)
        self.assertNotIn("DELETE", [c[0] for c in calls])
        for operation in (("PUT", "/actions/workflows/canonical-branch-protection.yml/disable"),
                          ("GET", "/actions/workflows/configure-validation-protection.yml"),
                          ("DELETE", "/actions/secrets/FAR_GITHUB_ADMIN_TOKEN")):
            with self.subTest(operation=operation):
                code, output, calls = self.execute(fail_request=operation)
                self.assertNotEqual(code, 0)
                self.assertEqual(output, "")
                self.assertEqual(calls[-1][:2], operation)

    def test_untrusted_repository_never_calls_api(self):
        if self.retired():
            return
        code, _, calls = self.execute(repository="other/fork")
        self.assertNotEqual(code, 0)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
