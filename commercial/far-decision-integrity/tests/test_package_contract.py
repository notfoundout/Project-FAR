from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.model import (
    SCHEMA_VERSION,
    DecisionPackage,
    IntegrityStatus,
    PackageValidationError,
)


def valid_payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "decision_id": "refund-1042",
        "decision_type": "issue_refund",
        "policy_version": "refund-policy/2026-07",
        "decision_root": "approve-refund",
        "proposed_action": {
            "kind": "financial_action",
            "target": "order-8831",
            "amount": 480.0,
        },
        "nodes": [
            {
                "node_id": "payment-confirmed",
                "kind": "evidence",
                "statement": "Payment was confirmed.",
            },
            {
                "node_id": "refund-policy-rule",
                "kind": "rule",
                "statement": "Confirmed refunds up to $500 may be automatically approved.",
            },
            {
                "node_id": "approve-refund",
                "kind": "conclusion",
                "statement": "Approve the requested refund.",
            },
        ],
        "dependencies": [
            {
                "source_id": "payment-confirmed",
                "target_id": "approve-refund",
                "relation": "supports",
            },
            {
                "source_id": "refund-policy-rule",
                "target_id": "approve-refund",
                "relation": "authorizes",
            },
        ],
        "authorization_requirements": [
            "payment-confirmed",
            "refund-policy-rule",
        ],
        "unknowns": [],
        "trace_completeness": 1.0,
        "metadata": {"source": "contract-test"},
    }


class TestDecisionPackageContract(unittest.TestCase):
    def test_accepts_complete_package(self):
        package = DecisionPackage.from_dict(valid_payload())
        self.assertEqual(package.decision_root, "approve-refund")
        self.assertEqual(len(package.nodes), 3)
        self.assertEqual(IntegrityStatus.JUSTIFIED.value, "justified")
        self.assertEqual(IntegrityStatus.UNSUPPORTED.value, "unsupported")
        self.assertEqual(IntegrityStatus.UNDERDETERMINED.value, "underdetermined")
        self.assertEqual(IntegrityStatus.UNVERIFIABLE.value, "unverifiable")

    def test_rejects_unknown_schema_version(self):
        payload = valid_payload()
        payload["schema_version"] = "far-decision-package/9.9"
        with self.assertRaisesRegex(PackageValidationError, "unsupported schema_version"):
            DecisionPackage.from_dict(payload)

    def test_rejects_missing_decision_root(self):
        payload = valid_payload()
        payload["decision_root"] = "missing"
        with self.assertRaisesRegex(PackageValidationError, "does not identify"):
            DecisionPackage.from_dict(payload)

    def test_rejects_dangling_dependency(self):
        payload = valid_payload()
        payload["dependencies"][0]["source_id"] = "missing-evidence"
        with self.assertRaisesRegex(PackageValidationError, "dependency source"):
            DecisionPackage.from_dict(payload)

    def test_rejects_undeclared_authorization_requirement(self):
        payload = valid_payload()
        payload["authorization_requirements"].append("manager-approval")
        with self.assertRaisesRegex(PackageValidationError, "undeclared nodes"):
            DecisionPackage.from_dict(payload)

    def test_rejects_out_of_range_trace_completeness(self):
        payload = valid_payload()
        payload["trace_completeness"] = 1.1
        with self.assertRaisesRegex(PackageValidationError, "between 0.0 and 1.0"):
            DecisionPackage.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
