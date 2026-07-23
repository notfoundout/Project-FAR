from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.security import SecurityError, TenantSecurityStore, tenant_evidence_id


class TestTenantSecurity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = TenantSecurityStore(pathlib.Path(self.temp.name) / "security.db")
        self.store.register_key(
            "tenant-a",
            "key-a",
            "secret-a",
            ("authorize", "policy:read", "policy:write", "evidence:read"),
        )
        self.store.register_key(
            "tenant-b",
            "key-b",
            "secret-b",
            ("authorize", "policy:read", "policy:write"),
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_authenticates_and_rejects_bad_secret(self):
        principal = self.store.authenticate("key-a.secret-a")
        self.assertEqual(principal.tenant_id, "tenant-a")
        with self.assertRaises(SecurityError):
            self.store.authenticate("key-a.wrong")

    def test_scope_enforcement(self):
        principal = self.store.authenticate("key-b.secret-b")
        with self.assertRaises(SecurityError):
            principal.require("evidence:read")

    def test_policy_versions_are_immutable_and_active_resolution_is_tenant_scoped(self):
        a = self.store.authenticate("key-a.secret-a")
        b = self.store.authenticate("key-b.secret-b")
        self.store.register_policy(a, "refund", "1", {"limit": 500}, activate=True)
        self.store.register_policy(a, "refund", "2", {"limit": 300})
        self.store.register_policy(b, "refund", "1", {"limit": 50}, activate=True)
        self.assertEqual(self.store.resolve_policy(a, "refund").payload["limit"], 500)
        self.assertEqual(self.store.resolve_policy(b, "refund").payload["limit"], 50)
        with self.assertRaises(SecurityError):
            self.store.register_policy(a, "refund", "1", {"limit": 700})

    def test_activation_switches_only_authenticated_tenant(self):
        a = self.store.authenticate("key-a.secret-a")
        b = self.store.authenticate("key-b.secret-b")
        self.store.register_policy(a, "refund", "1", {"limit": 500}, activate=True)
        self.store.register_policy(a, "refund", "2", {"limit": 300})
        self.store.register_policy(b, "refund", "1", {"limit": 50}, activate=True)
        self.store.activate_policy(a, "refund", "2")
        self.assertEqual(self.store.resolve_policy(a, "refund").version, "2")
        self.assertEqual(self.store.resolve_policy(b, "refund").version, "1")

    def test_tenant_evidence_ids_do_not_collide(self):
        self.assertNotEqual(
            tenant_evidence_id("tenant-a", "evidence-1"),
            tenant_evidence_id("tenant-b", "evidence-1"),
        )


if __name__ == "__main__":
    unittest.main()
