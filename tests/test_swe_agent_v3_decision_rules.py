from __future__ import annotations

import json
import unittest
from pathlib import Path

SPEC_PATH = (
    Path(__file__).resolve().parents[1]
    / "research/external-validation/swe-agent-v3/preregistration-v1.0.json"
)


class SweAgentV3DecisionRuleTests(unittest.TestCase):
    def load_analysis(self) -> dict:
        return json.loads(SPEC_PATH.read_text(encoding="utf-8"))["analysis"]

    def test_retained_invalid_repetition_makes_cell_missing(self) -> None:
        policy = self.load_analysis()["invalid_run_and_cell_policy"]
        self.assertEqual(policy["replacement_attempts_per_infrastructure_invalid_slot"], 1)
        self.assertTrue(policy["cell_valid_only_if_every_frozen_repetition_is_valid"])
        self.assertTrue(policy["retained_invalid_repetition_makes_entire_task_arm_cell_missing"])
        self.assertEqual(
            policy["primary_missingness_rule"],
            "if any FAR or placebo task-arm cell is missing, final confirmatory classification is inconclusive_due_to_missingness",
        )
        self.assertFalse(policy["sensitivity_results_are_confirmatory"])

    def test_decision_categories_are_ordered_and_nonoverlapping(self) -> None:
        analysis = self.load_analysis()
        self.assertEqual(
            analysis["decision_precedence"],
            [
                "inconclusive_due_to_missingness",
                "bounded_harm",
                "bounded_positive",
                "no_practical_advantage",
                "inconclusive",
            ],
        )
        categories = analysis["decision_categories"]
        self.assertIn("upper bound < 0", categories["bounded_harm"])
        self.assertIn("0 <= 95% paired-task bootstrap upper bound < 0.10", categories["no_practical_advantage"])
        self.assertIn("no primary cells are missing", categories["bounded_harm"])
        self.assertIn("no primary cells are missing", categories["no_practical_advantage"])

    def test_bootstrap_interval_and_rng_are_fully_frozen(self) -> None:
        spec = self.load_analysis()["bootstrap_interval_spec"]
        self.assertEqual(spec["method"], "percentile_equal_tailed")
        self.assertEqual(spec["lower_tail_probability"], 0.025)
        self.assertEqual(spec["upper_tail_probability"], 0.975)
        self.assertEqual(spec["resample_count"], 100000)
        self.assertEqual(spec["task_order"], "ascending frozen blind task identifier")
        self.assertEqual(spec["rng_procedure"]["id"], "sha256_rejection_stream_v1")
        self.assertIn("reject x >=", spec["rng_procedure"]["unbiased_index_rule"])
        self.assertEqual(spec["quantile_convention"]["id"], "hyndman_fan_type_7")


if __name__ == "__main__":
    unittest.main()
