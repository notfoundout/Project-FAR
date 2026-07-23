from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.operations import (
    FixedWindowRateLimiter,
    OperationsError,
    OperationsStore,
    RuntimeMetrics,
    create_backup,
    verify_backup,
)
from far_decision_integrity.security import SecurityError, TenantSecurityStore


class TestProductionOperations(unittest.TestCase):
    def setup_runtime(self, directory: str):
        root = pathlib.Path(directory)
        security = TenantSecurityStore(root / "security.db")
        scopes = (
            "authorize",
            "policy:read",
            "policy:write",
            "evidence:read",
            "keys:write",
            "audit:read",
        )
        security.register_key("tenant-a", "admin-a", "secret-a", scopes)
        security.register_key("tenant-b", "admin-b", "secret-b", scopes)
        return root, security, OperationsStore(security), security.authenticate("admin-a.secret-a")

    def test_key_rotation_revokes_old_and_authenticates_new(self):
        with tempfile.TemporaryDirectory() as directory:
            _, security, operations, actor = self.setup_runtime(directory)
            record = operations.rotate_key(actor, "admin-a", "admin-a-2", "secret-2", actor.scopes)
            self.assertEqual(record.action, "key.rotated")
            with self.assertRaises(SecurityError):
                security.authenticate("admin-a.secret-a")
            principal = security.authenticate("admin-a-2.secret-2")
            self.assertEqual(principal.tenant_id, "tenant-a")

    def test_revocation_is_tenant_scoped_and_audited(self):
        with tempfile.TemporaryDirectory() as directory:
            _, security, operations, actor = self.setup_runtime(directory)
            security.register_key("tenant-a", "worker", "worker-secret", ("authorize",))
            operations.revoke_key(actor, "worker")
            with self.assertRaises(SecurityError):
                security.authenticate("worker.worker-secret")
            log = operations.audit_log(actor)
            self.assertEqual(log[0].action, "key.revoked")
            self.assertEqual(log[0].tenant_id, "tenant-a")

    def test_policy_admin_actions_write_audit_records(self):
        with tempfile.TemporaryDirectory() as directory:
            _, _, operations, actor = self.setup_runtime(directory)
            operations.register_policy(actor, "refund", "v1", {"limit": 100}, activate=False)
            operations.activate_policy(actor, "refund", "v1")
            self.assertEqual([r.action for r in operations.audit_log(actor, limit=2)], ["policy.activated", "policy.registered"])

    def test_rate_limiter_resets_on_new_window(self):
        now = [0.0]
        limiter = FixedWindowRateLimiter(2, 60, clock=lambda: now[0])
        self.assertTrue(limiter.allow("tenant-a"))
        self.assertTrue(limiter.allow("tenant-a"))
        self.assertFalse(limiter.allow("tenant-a"))
        now[0] = 60.0
        self.assertTrue(limiter.allow("tenant-a"))

    def test_metrics_snapshot_is_deterministic(self):
        metrics = RuntimeMetrics()
        metrics.increment("requests.total")
        metrics.increment("requests.denied", 2)
        self.assertEqual(
            metrics.snapshot()["counters"],
            {"requests.denied": 2, "requests.total": 1},
        )

    def test_backup_and_restore_verification_detects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _, _, _ = self.setup_runtime(directory)
            evidence_db = root / "evidence.db"
            import sqlite3
            with sqlite3.connect(evidence_db) as connection:
                connection.execute("CREATE TABLE evidence (id TEXT PRIMARY KEY)")
            blobs = root / "blobs"
            blobs.mkdir()
            (blobs / "sample.json").write_text("{}\n", encoding="utf-8")
            backup = root / "backup"
            create_backup(root / "security.db", evidence_db, blobs, backup)
            self.assertTrue(verify_backup(backup)["valid"])
            (backup / "blobs" / "sample.json").write_text("tampered", encoding="utf-8")
            report = verify_backup(backup)
            self.assertFalse(report["valid"])
            self.assertIn("blobs/sample.json", report["failures"])

    def test_invalid_audit_limit_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            _, _, operations, actor = self.setup_runtime(directory)
            with self.assertRaises(OperationsError):
                operations.audit_log(actor, limit=0)


if __name__ == "__main__":
    unittest.main()
