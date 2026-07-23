from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.model import SCHEMA_VERSION
from far_decision_integrity.service import ServiceRequestError, authorize_payload


def package_payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "decision_id": "refund-1042",
        "decision_type": "issue_refund",
        "policy_version": "refund-policy/2026-07",
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


def trace_payload() -> dict:
    root = {
        "trace_id": "trace-1",
        "span_id": "root",
        "attributes": {
            "far.decision.root_span": True,
            "far.decision.id": "refund-1042",
            "far.decision.type": "issue_refund",
            "far.policy.version": "refund-policy/2026-07",
            "far.decision.root": "approve-refund",
            "far.action.kind": "financial_action",
            "far.action.amount": 480,
            "far.trace.completeness": 1.0,
        },
    }
    payment = {
        "trace_id": "trace-1",
        "span_id": "payment",
        "attributes": {
            "far.node.id": "payment",
            "far.node.kind": "evidence",
            "far.node.statement": "Payment confirmed.",
            "far.dependency.target": "approve-refund",
            "far.dependency.relation": "supports",
            "far.authorization.required": True,
        },
    }
    policy = {
        "trace_id": "trace-1",
        "span_id": "policy",
        "attributes": {
            "far.node.id": "policy",
            "far.node.kind": "rule",
            "far.node.statement": "Refund is authorized.",
            "far.dependency.target": "approve-refund",
            "far.dependency.relation": "authorizes",
            "far.authorization.required": True,
        },
    }
    conclusion = {
        "trace_id": "trace-1",
        "span_id": "conclusion",
        "attributes": {
            "far.node.id": "approve-refund",
            "far.node.kind": "conclusion",
            "far.node.statement": "Approve refund.",
        },
    }
    return {"spans": [root, payment, policy, conclusion]}


class TestAuthorizationService(unittest.TestCase):
    def test_package_request_allows_and_writes_bound_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            result = authorize_payload(
                {"input_type": "decision_package", "payload": package_payload()}, directory
            )
            self.assertEqual(result.payload["disposition"], "allow")
            evidence = pathlib.Path(directory) / result.payload["evidence_id"]
            manifest = json.loads((evidence / "manifest.json").read_text())
            for filename, digest in manifest["files"].items():
                actual = hashlib.sha256((evidence / filename).read_bytes()).hexdigest()
                self.assertEqual(actual, digest)

    def test_trace_request_round_trips_to_allow(self):
        with tempfile.TemporaryDirectory() as directory:
            result = authorize_payload({"input_type": "trace", "payload": trace_payload()}, directory)
            self.assertEqual(result.payload["integrity_status"], "justified")
            evidence = pathlib.Path(directory) / result.payload["evidence_id"]
            package = json.loads((evidence / "decision-package.json").read_text())
            self.assertEqual(package["metadata"]["source_trace_id"], "trace-1")

    def test_unknown_package_escalates(self):
        data = package_payload()
        data["unknowns"] = ["delivery-status"]
        with tempfile.TemporaryDirectory() as directory:
            result = authorize_payload({"input_type": "decision_package", "payload": data}, directory)
            self.assertEqual(result.payload["disposition"], "escalate")

    def test_invalid_request_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ServiceRequestError):
                authorize_payload({"input_type": "other", "payload": {}}, directory)


if __name__ == "__main__":
    unittest.main()
