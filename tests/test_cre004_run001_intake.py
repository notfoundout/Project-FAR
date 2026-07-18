from __future__ import annotations

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUN = (
    ROOT
    / "theory"
    / "evaluation"
    / "comparative-representation"
    / "experiments"
    / "CRE-004"
    / "runs"
    / "CRE-004-RUN-001"
)


class CRE004Run001IntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.intake = json.loads((RUN / "intake.json").read_text(encoding="utf-8"))

    def test_scope_matches_frozen_cre003_cases(self) -> None:
        self.assertEqual(
            ["CRE-003-I", "CRE-003-G", "CRE-003-C", "CRE-003-R"],
            self.intake["case_labels"],
        )
        self.assertEqual(10, len(self.intake["candidate_labels"]))
        self.assertEqual(3, len(self.intake["evaluator_slots"]))

    def test_intake_does_not_claim_execution(self) -> None:
        self.assertEqual("intake-open-not-executed", self.intake["status"])
        self.assertEqual(0, self.intake["response_count"])
        self.assertFalse(self.intake["result_artifacts_present"])
        self.assertIsNone(self.intake["scientific_result"])

    def test_all_execution_gates_begin_closed(self) -> None:
        gates = self.intake["gates"]
        self.assertTrue(gates)
        for gate in (
            "anonymized_candidate_packages_frozen",
            "evaluators_registered",
            "calibration_completed",
            "independence_claims_recorded",
            "assignment_order_generated",
            "protocol_lock_verified",
            "append_only_response_channel_verified",
        ):
            self.assertFalse(gates[gate])

    def test_no_result_files_exist_before_evaluator_submissions(self) -> None:
        for filename in ("results.csv", "summary.json", "execution_report.md"):
            self.assertFalse((RUN / filename).exists())


if __name__ == "__main__":
    unittest.main()
