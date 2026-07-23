from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.adjudicate import adjudicate
from far_decision_integrity.cli import main
from far_decision_integrity.model import DecisionPackage, IntegrityStatus, SCHEMA_VERSION


def payload() -> dict:
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


class TestAdjudication(unittest.TestCase):
    def test_justified(self):
        self.assertEqual(adjudicate(DecisionPackage.from_dict(payload())).status, IntegrityStatus.JUSTIFIED)

    def test_unsupported_has_precedence(self):
        data = payload()
        data["dependencies"] = data["dependencies"][:1]
        data["unknowns"] = ["manager-state"]
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNSUPPORTED)

    def test_underdetermined(self):
        data = payload()
        data["metadata"] = {"material_alternatives": ["approve", "deny"]}
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNDERDETERMINED)

    def test_unverifiable_for_unknowns(self):
        data = payload()
        data["unknowns"] = ["delivery-status"]
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNVERIFIABLE)

    def test_unverifiable_for_incomplete_trace(self):
        data = payload()
        data["trace_completeness"] = 0.9
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNVERIFIABLE)

    def test_invalid_node_is_unsupported(self):
        data = payload()
        data["nodes"][0]["attributes"] = {"valid": False}
        result = adjudicate(DecisionPackage.from_dict(data))
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)
        self.assertIn("required-node-invalid", {finding.rule_id for finding in result.findings})

    def test_cli_exit_codes_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "package.json"
            report = root / "report.json"
            source.write_text(json.dumps(payload()), encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(report)]), 0)
            self.assertEqual(json.loads(report.read_text())["status"], "justified")

            data = payload()
            data["unknowns"] = ["missing"]
            source.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(main([str(source)]), 32)

    def test_cli_invalid_package_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "bad.json"
            source.write_text("{}", encoding="utf-8")
            self.assertEqual(main([str(source)]), 40)


if __name__ == "__main__":
    unittest.main()
