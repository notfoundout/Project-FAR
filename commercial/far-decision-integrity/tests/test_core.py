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
from far_decision_integrity.model import DecisionPackage, IntegrityStatus, PackageValidationError, SCHEMA_VERSION


def payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "decision_id": "case-001",
        "decision_type": "external_agent_action",
        "policy_version": "policy/1",
        "decision_root": "conclusion",
        "proposed_action": {"kind": "complete_task"},
        "nodes": [
            {"node_id": "evidence", "kind": "evidence", "statement": "Evidence observed."},
            {"node_id": "rule", "kind": "rule", "statement": "Evidence is required."},
            {"node_id": "conclusion", "kind": "conclusion", "statement": "Complete task."},
        ],
        "dependencies": [
            {"source_id": "evidence", "target_id": "conclusion", "relation": "supports"},
            {"source_id": "rule", "target_id": "conclusion", "relation": "authorizes"},
        ],
        "authorization_requirements": ["evidence", "rule"],
        "unknowns": [],
        "trace_completeness": 1.0,
        "metadata": {},
    }


class TestCore(unittest.TestCase):
    def test_accepts_and_justifies_complete_package(self):
        package = DecisionPackage.from_dict(payload())
        self.assertEqual(adjudicate(package).status, IntegrityStatus.JUSTIFIED)

    def test_rejects_dangling_dependency(self):
        data = payload()
        data["dependencies"][0]["source_id"] = "missing"
        with self.assertRaisesRegex(PackageValidationError, "dependency source"):
            DecisionPackage.from_dict(data)

    def test_unsupported_precedes_unknown(self):
        data = payload()
        data["dependencies"] = data["dependencies"][:1]
        data["unknowns"] = ["manager-state"]
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNSUPPORTED)

    def test_material_alternatives_are_underdetermined(self):
        data = payload()
        data["metadata"] = {"material_alternatives": ["allow", "deny"]}
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNDERDETERMINED)

    def test_unknown_or_incomplete_is_unverifiable(self):
        data = payload()
        data["trace_completeness"] = 0.5
        self.assertEqual(adjudicate(DecisionPackage.from_dict(data)).status, IntegrityStatus.UNVERIFIABLE)

    def test_cli_writes_deterministic_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "package.json"
            report = root / "report.json"
            source.write_text(json.dumps(payload()), encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(report)]), 0)
            first = report.read_bytes()
            self.assertEqual(main([str(source), "--output", str(report)]), 0)
            self.assertEqual(first, report.read_bytes())


if __name__ == "__main__":
    unittest.main()
