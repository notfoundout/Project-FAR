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
from far_decision_integrity.evidence import verify_evidence_bundle, write_evidence_bundle
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
        "authorization_requirements": ["rule"],
        "unknowns": [],
        "trace_completeness": 1.0,
        "metadata": {},
    }


class TestCore(unittest.TestCase):
    def test_accepts_and_justifies_complete_package(self):
        package = DecisionPackage.from_dict(payload())
        self.assertEqual(adjudicate(package).status, IntegrityStatus.JUSTIFIED)

    def test_requires_explicit_authorization_and_unknown_fields(self):
        for field in ("authorization_requirements", "unknowns"):
            with self.subTest(field=field):
                data = payload()
                del data[field]
                with self.assertRaisesRegex(PackageValidationError, f"{field} is required"):
                    DecisionPackage.from_dict(data)

    def test_rejects_dangling_dependency(self):
        data = payload()
        data["dependencies"][0]["source_id"] = "missing"
        with self.assertRaisesRegex(PackageValidationError, "dependency source"):
            DecisionPackage.from_dict(data)

    def test_rejects_dependency_cycles(self):
        data = payload()
        data["dependencies"].append(
            {"source_id": "conclusion", "target_id": "rule", "relation": "supports"}
        )
        with self.assertRaisesRegex(PackageValidationError, "cycle detected"):
            DecisionPackage.from_dict(data)

    def test_support_edge_does_not_satisfy_authorization(self):
        data = payload()
        data["dependencies"][1]["relation"] = "supports"
        result = adjudicate(DecisionPackage.from_dict(data))
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)
        self.assertIn("authorization-dependency-missing", {item.rule_id for item in result.findings})

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

    def test_evidence_bundle_verifies_report_and_all_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "source.json"
            bundle = root / "bundle"
            source.write_text('{"value":1}\n', encoding="utf-8")
            write_evidence_bundle(
                bundle,
                report_name="report.json",
                report_payload={"status": "ok"},
                source_files={"source": source},
            )
            self.assertTrue(verify_evidence_bundle(bundle))
            source.write_text('{"value":2}\n', encoding="utf-8")
            self.assertFalse(verify_evidence_bundle(bundle))


if __name__ == "__main__":
    unittest.main()
