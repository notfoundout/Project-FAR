"""Exercise the reviewed inline one-shot without network or real credentials.

After protected cleanup, the receipt/absence gate replaces execution of the
removed one-shot; test identities remain stable across that lifecycle.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse

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
        self.assertEqual(receipt["accepted_receipt"]["credential_sha256"], receipt["authorized_credential_sha256"])
        self.assertEqual(receipt["accepted_receipt"]["branch_protection_sha256"],
                         receipt["identity_capture"]["receipt"]["branch_protection_sha256"])
        if receipt["accepted_receipt"]["secret_absent"]:
            self.assertTrue(receipt["accepted_receipt"]["secret_absent"])
        else:
            self.assertEqual(receipt["accepted_receipt"]["mode"], "issuer_revocation")
            self.assertIs(receipt["accepted_receipt"]["credential_usable"], False)
            self.assertEqual(receipt["accepted_receipt"]["revocation_http_status"], 202)
            self.assertEqual(receipt["accepted_receipt"]["credential_authentication_http_status"], 401)
            self.assertEqual(receipt["accepted_receipt"]["repository_secret_delete_http_status"], 403)
            self.assertEqual(receipt["accepted_receipt"]["workflow_token_secret_delete_http_status"], 403)
            self.assertTrue(receipt["accepted_receipt"]["post_revocation_protection_summary_enforced"])
            recovery = receipt["recovery_execution"]["receipt"]
            self.assertEqual(recovery["mode"], "invalidated_credential_recovery")
            self.assertEqual(recovery["credential_sha256"], receipt["authorized_credential_sha256"])
            self.assertEqual(recovery["credential_authentication_http_status"], 401)
            self.assertIs(recovery["credential_usable"], False)
            self.assertIs(receipt["residual_metadata"]["repository_secret_entry_absent"], False)
            self.assertIs(receipt["residual_metadata"]["value_is_usable_credential"], False)
        actual = receipt["accepted_receipt"]["branch_protection"]
        self.assertEqual(receipt["accepted_receipt"]["branch_protection_sha256"], hashlib.sha256(
            json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()).hexdigest())
        for key, expected in policy().items():
            if isinstance(expected, dict):
                for field, value in expected.items():
                    self.assertEqual(actual[key][field], value)
            else:
                self.assertEqual(actual.get(key), expected)
        self.assertTrue(receipt["accepted_receipt"]["branch_protection_unchanged_and_enforced"])
        self.assertEqual(receipt["accepted_receipt"]["privileged_workflow_states"],
                         {name: "disabled_manually" for name in LEGACY})
        return True

    def execute(self, *, token="fake-admin", before=None, after=None,
                state="disabled_manually", fail_request=None, repository=None,
                failure_status=500, issuer_auth_status=401, revocation_status=202,
                delete_statuses=None, identity_pin="synthetic", initial_state=None):
        workflow = yaml.safe_load(WORKFLOW.read_text())
        shell = workflow["jobs"]["retire"]["steps"][0]["run"]
        code = shell.split("python - <<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
        # Exercise activation against a synthetic identity, never a real credential.
        import re
        pin = hashlib.sha256(token.encode()).hexdigest() if identity_pin == "synthetic" else identity_pin
        code = re.sub(r'expected_credential_sha256 = "[a-f0-9]*"',
                      f'expected_credential_sha256 = "{pin}"', code)
        before = policy() if before is None else before
        after = copy.deepcopy(before) if after is None else after
        calls = []
        protection_reads = 0
        workflow_reads = {}
        delete_statuses = list(delete_statuses or [])

        class Response(io.BytesIO):
            def __init__(self, data, status=200):
                super().__init__(json.dumps(data).encode())
                self.status = status

        def urlopen(req):
            nonlocal protection_reads
            path = urllib.parse.urlparse(req.full_url).path.removeprefix('/repos/notfoundout/Project-FAR')
            calls.append((req.get_method(), path, req.headers.get("Authorization")))
            if path == '/credentials/revoke':
                self.assertEqual(req.get_method(), 'POST')
                self.assertNotIn('Authorization', req.headers)
                self.assertEqual(json.loads(req.data), {'credentials': [token]})
                return Response({}, revocation_status)
            if path == '/user':
                self.assertEqual(req.headers.get('Authorization'), f'Bearer {token}')
                if issuer_auth_status != 200:
                    raise urllib.error.HTTPError(req.full_url, issuer_auth_status, 'issuer', {}, io.BytesIO())
                return Response({}, 200)
            if req.get_method() == 'DELETE' and delete_statuses:
                status = delete_statuses.pop(0)
                if status != 204:
                    raise urllib.error.HTTPError(req.full_url, status, 'delete', {}, io.BytesIO())
                return Response({}, 204)
            if fail_request == (req.get_method(), path):
                raise urllib.error.HTTPError(req.full_url, failure_status, "Forbidden", {}, io.BytesIO(b"denied"))
            if path.endswith("/protection"):
                protection_reads += 1
                data = before if protection_reads == 1 else after
            elif path == "/branches/main":
                data = {"protected": True, "protection": {"enabled": True,
                    "required_status_checks": {"enforcement_level": "everyone",
                    "contexts": ["merge-authority"],
                    "checks": [{"context": "merge-authority", "app_id": 15368}]}}}
            elif req.get_method() == "GET" and "/actions/workflows/" in path:
                workflow_reads[path] = workflow_reads.get(path, 0) + 1
                data = {"state": initial_state if initial_state is not None and workflow_reads[path] == 1 else state}
            elif req.get_method() in ("PUT", "DELETE"):
                data = {}
            else:
                raise AssertionError((req.get_method(), path))
            return Response(data)

        env = {"GITHUB_REPOSITORY": repository or "notfoundout/Project-FAR",
               "GITHUB_REF": "refs/heads/main", "FAR_GITHUB_ADMIN_TOKEN": token,
               "GITHUB_WORKFLOW_TOKEN": "fake-workflow"}
        output = io.StringIO()
        exit_code = 0
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", urlopen), patch('time.sleep'), contextlib.redirect_stdout(output):
            try:
                exec(compile(code, str(WORKFLOW), "exec"), {})
            except SystemExit as exc:
                exit_code = exc.code
        self.assertNotIn("fake-admin", output.getvalue())
        self.assertNotIn("fake-workflow", output.getvalue())
        if token:
            self.assertNotIn(token, output.getvalue())
        return exit_code, output.getvalue(), calls

    def test_unpinned_identity_is_read_only_and_replacement_fails_before_api(self):
        if self.retired():
            return
        code, output, calls = self.execute(identity_pin="")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["mode"], "credential_identity_capture")
        self.assertIs(json.loads(output)["retirement_accepted"], False)
        self.assertEqual(json.loads(output)["credential_sha256"], hashlib.sha256(b'fake-admin').hexdigest())
        self.assertTrue(all(method == "GET" for method, _, _ in calls))
        code, output, calls = self.execute(identity_pin="0" * 64)
        self.assertNotEqual(code, 0)
        self.assertEqual(output, "")
        self.assertEqual(calls, [])

    def test_delete_forbidden_revokes_only_exact_pat_and_requires_issuer_rejection(self):
        if self.retired():
            return
        code, output, calls = self.execute(token='ghp_synthetic_obsolete', delete_statuses=[403, 403])
        self.assertEqual(code, 0)
        self.assertIn('"mode": "revocation_pending"', output)
        self.assertIn('"mode": "issuer_revocation"', output)
        self.assertIn('"secret_absent": false', output)
        self.assertIn('"credential_authentication_http_status": 401', output)
        self.assertIn(hashlib.sha256(b'ghp_synthetic_obsolete').hexdigest(), output)
        self.assertIn('"mode": "revocation_requested"', output)
        self.assertEqual(sum(path == '/credentials/revoke' for _, path, _ in calls), 1)
        self.assertEqual(calls[-1][:2], ('GET', '/branches/main'))

    def test_short_lived_deletion_is_attempted_before_revocation(self):
        if self.retired():
            return
        code, output, calls = self.execute(delete_statuses=[403, 204])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)['secret_absent'])
        self.assertEqual(calls[-1][2], 'Bearer fake-workflow')
        self.assertNotIn('/credentials/revoke', [path for _, path, _ in calls])

    def test_revocation_queue_or_unexpected_response_cannot_be_accepted(self):
        if self.retired():
            return
        for status in (200, 403):
            code, output, _ = self.execute(token='ghp_synthetic_obsolete', delete_statuses=[403, 403], issuer_auth_status=status)
            self.assertNotEqual(code, 0)
            self.assertNotIn('"mode": "issuer_revocation"', output)
        code, output, _ = self.execute(token='ghp_synthetic_obsolete', delete_statuses=[403, 403], revocation_status=422)
        self.assertNotEqual(code, 0)
        self.assertNotIn('"mode": "issuer_revocation"', output)

    def test_invalidated_credential_recovery_is_read_only_and_cannot_use_valid_pat(self):
        if self.retired():
            return
        code, output, calls = self.execute(fail_request=('GET', '/branches/main/protection'), failure_status=401)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)['mode'], 'invalidated_credential_recovery')
        self.assertEqual(json.loads(output)['credential_sha256'], hashlib.sha256(b'fake-admin').hexdigest())
        self.assertTrue(all(method == 'GET' for method, _, _ in calls))
        code, output, _ = self.execute(fail_request=('GET', '/branches/main/protection'), failure_status=401, issuer_auth_status=200)
        self.assertNotEqual(code, 0)
        self.assertEqual(output, '')

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
        code, _, calls = self.execute(initial_state="active")
        self.assertEqual(code, 0)
        self.assertEqual(sum(method == "PUT" for method, _, _ in calls), 2)

    def test_already_disabled_consumers_require_no_redundant_disable_permission(self):
        if self.retired():
            return
        operation = ("PUT", "/actions/workflows/canonical-branch-protection.yml/disable")
        code, output, calls = self.execute(fail_request=operation, failure_status=403)
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)["secret_absent"])
        self.assertFalse(any(method == "PUT" for method, _, _ in calls))
        code, output, calls = self.execute(fail_request=operation, failure_status=403, initial_state="active")
        self.assertNotEqual(code, 0)
        self.assertEqual(output, "")
        self.assertFalse(any(method == "DELETE" for method, _, _ in calls))

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
                code, output, calls = self.execute(fail_request=operation,
                    initial_state="active" if operation[0] == "PUT" else None)
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
