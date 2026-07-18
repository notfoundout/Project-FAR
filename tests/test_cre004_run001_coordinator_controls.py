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


class CRE004Run001CoordinatorControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.intake = json.loads((RUN / "intake.json").read_text(encoding="utf-8"))
        self.key = json.loads(
            (RUN / "coordinator_candidate_key.json").read_text(encoding="utf-8")
        )
        self.randomization = json.loads(
            (RUN / "randomization_control.json").read_text(encoding="utf-8")
        )

    def test_candidate_key_is_complete_and_bijective(self) -> None:
        labels = self.intake["candidate_labels"]
        key = self.key["candidate_key"]
        self.assertEqual(set(labels), set(key))
        self.assertEqual(10, len(set(key.values())))
        self.assertEqual(
            {f"AV-{index:03d}" for index in range(1, 11)}, set(key.values())
        )

    def test_candidate_key_is_not_an_evaluator_artifact(self) -> None:
        policy = self.key["access_policy"]
        self.assertFalse(policy["included_in_evaluator_packet"])
        self.assertFalse(policy["available_to_evaluators"])
        self.assertFalse(policy["candidate_identity_may_be_used_during_scoring"])
        self.assertTrue(policy["unblinding_allowed_after_response_freeze_only"])

    def test_randomization_scope_matches_intake(self) -> None:
        self.assertEqual(self.intake["evaluator_slots"], self.randomization["evaluator_slots"])
        self.assertEqual(self.intake["case_labels"], self.randomization["case_labels"])
        self.assertEqual(
            self.intake["candidate_labels"], self.randomization["candidate_labels"]
        )
        self.assertEqual(40, self.randomization["expected_assignments_per_evaluator"])
        self.assertEqual(120, self.randomization["expected_total_assignments"])
        self.assertIsInstance(self.randomization["randomization_seed"], int)

    def test_only_completed_coordinator_gates_are_open(self) -> None:
        gates = self.intake["gates"]
        self.assertTrue(gates["candidate_key_frozen_outside_evaluator_packet"])
        self.assertTrue(gates["randomization_seed_frozen"])
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

    def test_run_still_contains_no_result(self) -> None:
        self.assertEqual("intake-open-not-executed", self.intake["status"])
        self.assertEqual(0, self.intake["response_count"])
        self.assertFalse(self.intake["result_artifacts_present"])
        self.assertIsNone(self.intake["scientific_result"])
        self.assertIsNone(self.randomization["assignment_artifact"])


if __name__ == "__main__":
    unittest.main()
