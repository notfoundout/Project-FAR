from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w1_actual_process_correspondence.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ActualProcessCorrespondenceTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_positive_correspondence_requires_external_evidence(self) -> None:
        scope = load(SCOPE)
        required = scope["admission_rule"]["required_for_positive_correspondence"]
        self.assertIn("independent process observations", required)
        self.assertIn("measurement model with error bounds", required)
        self.assertIn("registered alternative-process explanations", required)
        self.assertEqual(scope["observation_boundary"]["external_access"], "not supplied in this execution")

    def test_formal_and_generated_trace_evidence_are_insufficient(self) -> None:
        result = load(RESULT)["fixture_results"]
        self.assertEqual(result["APC-FORMAL-001"], "insufficient_for_correspondence")
        self.assertEqual(result["APC-TRACE-001"], "insufficient_nonindependent_evidence")
        self.assertEqual(result["APC-OBS-EQUIV-001"], "blocks_identity_inference")

    def test_invalid_identity_inferences_are_rejected(self) -> None:
        fixtures = {item["id"]: item for item in load(FIXTURES)["fixtures"]}
        result = load(RESULT)["fixture_results"]
        for item in ("APC-NEG-REP-001", "APC-NEG-LABEL-001"):
            self.assertEqual(fixtures[item]["expected"], "rejected")
            self.assertEqual(result[item], "rejected")

    def test_terminal_outcome_and_next_workstream(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["terminal_outcome"], "new_assumption_required")
        self.assertEqual(result["workstream_effect"]["USD-W1-SCOPE-EXT"], "all_registered_feature_families_executed")
        self.assertEqual(result["next_decisive_workstream"], "USD-W2-ALT-VOCAB")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
