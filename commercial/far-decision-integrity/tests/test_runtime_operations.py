from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.operations import FixedWindowRateLimiter, OperationsError, OperationsStore, RuntimeMetrics
from far_decision_integrity.secured_service import SecuredRuntime
from far_decision_integrity.security import SecurityError, TenantSecurityStore
from far_decision_integrity.store import EvidenceStore


class TestRuntimeOperationsIntegration(unittest.TestCase):
    def runtime(self, directory: str, *, limit: int = 10) -> tuple[SecuredRuntime, object]:
        root = pathlib.Path(directory)
        security = TenantSecurityStore(root / "security.db")
        scopes = ("authorize", "policy:read", "policy:write", "evidence:read", "keys:write", "audit:read", "metrics:read")
        security.register_key("tenant-a", "admin", "secret", scopes)
        principal = security.authenticate("admin.secret")
        operations = OperationsStore(security)
        runtime = SecuredRuntime(
            security,
            EvidenceStore(root / "evidence.db", root / "blobs"),
            root / "staging",
            operations,
            FixedWindowRateLimiter(limit, 60, clock=lambda: 100.0),
            RuntimeMetrics(),
        )
        return runtime, principal

    def test_key_rotation_revokes_old_key_and_audits(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory)
            result = runtime.administer(principal, "keys/rotate", {"old_key_id": "admin", "new_key_id": "admin-2", "new_secret": "next", "scopes": list(principal.scopes)})
            self.assertEqual(result["action"], "key.rotated")
            with self.assertRaises(SecurityError):
                runtime.security.authenticate("admin.secret")
            self.assertEqual(runtime.security.authenticate("admin-2.next").tenant_id, "tenant-a")
            self.assertEqual(runtime.audit(principal, 10)["records"][0]["action"], "key.rotated")

    def test_key_revocation_is_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory)
            runtime.security.register_key("tenant-a", "worker", "worker-secret", ("authorize",))
            runtime.administer(principal, "keys/revoke", {"key_id": "worker"})
            with self.assertRaises(SecurityError):
                runtime.security.authenticate("worker.worker-secret")

    def test_policy_registration_and_activation_are_audited(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory)
            registered = runtime.administer(principal, "policies/register", {"policy_id": "refund", "version": "v1", "payload": {"limit": 500}, "activate": True})
            self.assertEqual(registered["action"], "policy.registered")
            runtime.administer(principal, "policies/register", {"policy_id": "refund", "version": "v2", "payload": {"limit": 700}})
            activated = runtime.administer(principal, "policies/activate", {"policy_id": "refund", "version": "v2"})
            self.assertEqual(activated["action"], "policy.activated")
            self.assertEqual(runtime.policy(principal, "refund", None)["version"], "v2")

    def test_audit_log_is_tenant_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory)
            runtime.administer(principal, "policies/register", {"policy_id": "refund", "version": "v1", "payload": {"limit": 500}})
            runtime.security.register_key("tenant-b", "other", "secret", ("audit:read",))
            other = runtime.security.authenticate("other.secret")
            self.assertEqual(runtime.audit(other, 10)["records"], [])

    def test_rate_limit_is_enforced_and_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory, limit=1)
            runtime.enforce_rate_limit(principal)
            with self.assertRaises(OperationsError):
                runtime.enforce_rate_limit(principal)
            self.assertEqual(runtime.metrics.snapshot()["counters"]["requests.rate_limited"], 1)

    def test_metrics_record_authentication_and_admin_actions(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal = self.runtime(directory)
            runtime.authenticate("Bearer admin.secret", "keys:write")
            runtime.administer(principal, "policies/register", {"policy_id": "refund", "version": "v1", "payload": {"limit": 500}})
            counters = runtime.metrics.snapshot()["counters"]
            self.assertEqual(counters["authentication.succeeded"], 1)
            self.assertEqual(counters["admin.policy.registered"], 1)


if __name__ == "__main__":
    unittest.main()
