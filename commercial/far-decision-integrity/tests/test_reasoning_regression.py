from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.evidence import verify_evidence_bundle
from far_decision_integrity.regression import RegressionDecision, RunResult, compare_corpus
from far_decision_integrity.regression_cli import main


def run(case_id: str, status: str = "justified", disposition: str = "allow", findings: tuple[str, ...] = ()) -> RunResult:
    return RunResult(case_id, status, disposition, findings)


class TestReasoningRegression(unittest.TestCase):
    def test_preserved_corpus_passes(self):
        baseline = [run("a"), run("b", "unsupported", "block", ("x",))]
        report = compare_corpus("suite-1", baseline, list(baseline))
        self.assertEqual(report.decision, RegressionDecision.PASS)

    def test_authorization_expansion_blocks(self):
        report = compare_corpus("suite-1", [run("a", "unsupported", "block")], [run("a")])
        self.assertEqual(report.decision, RegressionDecision.BLOCKED)
        self.assertEqual(report.cases[0].classification, "authorization-expanded")

    def test_integrity_degradation_blocks(self):
        report = compare_corpus("suite-1", [run("a")], [run("a", "unsupported", "block")])
        self.assertEqual(report.decision, RegressionDecision.BLOCKED)

    def test_restriction_requires_review(self):
        report = compare_corpus("suite-1", [run("a")], [run("a", "justified", "escalate")])
        self.assertEqual(report.decision, RegressionDecision.REVIEW)

    def test_reasoning_change_requires_review(self):
        report = compare_corpus("suite-1", [run("a", findings=("old",))], [run("a", findings=("new",))])
        self.assertEqual(report.cases[0].changed_findings, ("new", "old"))

    def test_mismatched_corpus_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "corpus case mismatch"):
            compare_corpus("suite-1", [run("a")], [run("b")])

    def test_cli_writes_bound_deterministic_bundle(self):
        payload = {
            "suite_id": "suite-cli",
            "baseline": [{"case_id": "a", "integrity_status": "unsupported", "disposition": "block", "finding_ids": []}],
            "candidate": [{"case_id": "a", "integrity_status": "justified", "disposition": "allow", "finding_ids": []}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "suite.json"
            output = root / "evidence"
            source.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(main([str(source), "--output-directory", str(output)]), 30)
            self.assertTrue(verify_evidence_bundle(output))
            report = json.loads((output / "regression-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["decision"], "blocked")
            self.assertEqual(report["schema_version"], "far-reasoning-regression/0.1")

    def test_manifest_detects_report_tampering(self):
        payload = {
            "suite_id": "suite-cli",
            "baseline": [{"case_id": "a", "integrity_status": "justified", "disposition": "allow", "finding_ids": []}],
            "candidate": [{"case_id": "a", "integrity_status": "justified", "disposition": "allow", "finding_ids": []}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "suite.json"
            output = root / "evidence"
            source.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(main([str(source), "--output-directory", str(output)]), 0)
            (output / "regression-report.json").write_text("{}\n", encoding="utf-8")
            self.assertFalse(verify_evidence_bundle(output))


if __name__ == "__main__":
    unittest.main()
