from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.regression import RegressionDecision, RunResult, compare_corpus
from far_decision_integrity.regression_cli import main


def run(case_id: str, status: str = "justified", disposition: str = "allow", findings: tuple[str, ...] = ()) -> RunResult:
    return RunResult(case_id, status, disposition, findings)


class TestReasoningRegression(unittest.TestCase):
    def test_preserved_corpus_passes(self):
        baseline = [run("a"), run("b", "unsupported", "block", ("x",))]
        report = compare_corpus("suite-1", baseline, list(baseline))
        self.assertEqual(report.decision, RegressionDecision.PASS)
        self.assertTrue(all(case.classification == "preserved" for case in report.cases))

    def test_authorization_expansion_blocks(self):
        report = compare_corpus("suite-1", [run("a", "unsupported", "block")], [run("a")])
        self.assertEqual(report.decision, RegressionDecision.BLOCKED)
        self.assertEqual(report.cases[0].classification, "authorization-expanded")

    def test_integrity_degradation_blocks(self):
        report = compare_corpus("suite-1", [run("a")], [run("a", "unsupported", "block")])
        self.assertEqual(report.decision, RegressionDecision.BLOCKED)
        self.assertEqual(report.cases[0].classification, "integrity-degraded")

    def test_restriction_requires_review(self):
        report = compare_corpus("suite-1", [run("a")], [run("a", "justified", "escalate")])
        self.assertEqual(report.decision, RegressionDecision.REVIEW)
        self.assertEqual(report.cases[0].classification, "authorization-restricted")

    def test_reasoning_change_requires_review(self):
        report = compare_corpus("suite-1", [run("a", findings=("old",))], [run("a", findings=("new",))])
        self.assertEqual(report.decision, RegressionDecision.REVIEW)
        self.assertEqual(report.cases[0].changed_findings, ("new", "old"))

    def test_mismatched_corpus_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "corpus case mismatch"):
            compare_corpus("suite-1", [run("a")], [run("b")])

    def test_cli_writes_deterministic_report_and_exit_code(self):
        payload = {
            "suite_id": "suite-cli",
            "baseline": [{"case_id": "a", "integrity_status": "unsupported", "disposition": "block", "finding_ids": []}],
            "candidate": [{"case_id": "a", "integrity_status": "justified", "disposition": "allow", "finding_ids": []}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source, output = root / "suite.json", root / "report.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(output)]), 30)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["decision"], "blocked")
            self.assertEqual(report["schema_version"], "far-reasoning-regression/0.1")


if __name__ == "__main__":
    unittest.main()
