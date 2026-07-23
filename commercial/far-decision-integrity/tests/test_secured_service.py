from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.store import EvidenceStore, EvidenceStoreError
from far_decision_integrity.model import SCHEMA_VERSION
from far_decision_integrity.secured_service import SecuredRuntime
from far_decision_integrity.security import Principal, SecurityError, TenantSecurityStore


def package_payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "decision_id": "refund-1042",
        "decision_type": "issue_refund",
        "policy_version": "2026-07",
        "decision_root": "approve-refund",
        "proposed_action": {"kind": "financial_action", "amount": 480},
        "nodes": [
            {"node_id": "payment", "kind": "evidence", "statement": "Payment confirmed."},
            {"node_id": "policy", "kind": "rule", "statement": "Refund is authorized."},
            {"node_id": "approve-refund", "kind": "conclusion", "statement": "Approve refund."},
        ],
        "dependencies": [
            {"source_id": "payment", "target_id": "approve-refund", "relation": "supports"},
            {"source_id": "policy", "target_id": "approve-refund", "relation": "authorizes"},
        ],
        "authorization_requirements": ["payment", "policy"],
        "unknowns": [],
        "trace_completeness": 1.0,
        "metadata": {},
    }


class TestSecuredService(unittest.TestCase):
    def runtime(self, directory: str) -> tuple[SecuredRuntime, Principal, Principal]:
        root = pathlib.Path(directory)
        security = TenantSecurityStore(root / "security.db")
        scopes = ("authorize", "policy:read", "policy:write", "evidence:read")
        security.register_key("tenant-a", "key-a", "secret-a", scopes)
        security.register_key("tenant-b", "key-b", "secret-b", scopes)
        a = security.authenticate("key-a.secret-a")
        b = security.authenticate("key-b.secret-b")
        security.register_policy(a, "refund", "2026-07", {"limit": 500}, activate=True)
        security.register_policy(b, "refund", "2026-07", {"limit": 200}, activate=True)
        runtime = SecuredRuntime(
            security,
            EvidenceStore(root / "evidence.db", root / "blobs"),
            root / "staging",
        )
        return runtime, a, b

    def test_authorization_uses_tenant_policy_and_persists_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal, _ = self.runtime(directory)
            result = runtime.authorize(principal, {"policy_id": "refund", "input_type": "decision_package", "payload": package_payload()})
            self.assertEqual(result["tenant_id"], "tenant-a")
            self.assertEqual(result["policy"]["version"], "2026-07")
            self.assertTrue(result["evidence_id"].startswith("tenant-a-"))
            self.assertTrue(runtime.evidence_record(principal, result["evidence_id"])["verification"]["valid"])

    def test_cross_tenant_evidence_access_is_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, tenant_a, tenant_b = self.runtime(directory)
            result = runtime.authorize(tenant_a, {"policy_id": "refund", "input_type": "decision_package", "payload": package_payload()})
            with self.assertRaises(EvidenceStoreError):
                runtime.evidence_record(tenant_b, result["evidence_id"])

    def test_policy_resolution_is_tenant_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, tenant_a, tenant_b = self.runtime(directory)
            self.assertEqual(runtime.policy(tenant_a, "refund", None)["payload"]["limit"], 500)
            self.assertEqual(runtime.policy(tenant_b, "refund", None)["payload"]["limit"], 200)

    def test_missing_authorize_scope_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, _, _ = self.runtime(directory)
            with self.assertRaises(SecurityError):
                runtime.authorize(Principal("tenant-a", "readonly", ("policy:read",)), {"policy_id": "refund", "input_type": "decision_package", "payload": package_payload()})

    def test_invalid_bearer_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, _, _ = self.runtime(directory)
            with self.assertRaises(SecurityError):
                runtime.authenticate("Basic abc", "authorize")

    def test_explicit_policy_version_is_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime, principal, _ = self.runtime(directory)
            result = runtime.authorize(principal, {"policy_id": "refund", "policy_version": "2026-07", "input_type": "decision_package", "payload": package_payload()})
            self.assertEqual(result["policy"]["sha256"], runtime.policy(principal, "refund", "2026-07")["sha256"])


if __name__ == "__main__":
    unittest.main()
