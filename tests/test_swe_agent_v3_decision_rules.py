from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "research/external-validation/swe-agent-v3/preregistration-v1.0.json"
SEED_PATH = ROOT / "research/external-validation/swe-agent-v3/bootstrap-seed-commitment-contract-v1.0.json"


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

    def test_bootstrap_interval_rng_and_order_are_fully_frozen(self) -> None:
        analysis = self.load_analysis()
        self.assertEqual(
            analysis["bootstrap_seed_status"],
            "unfrozen_and_independently_committed_before_execution",
        )
        commitment = json.loads(SEED_PATH.read_text(encoding="utf-8"))
        self.assertEqual(commitment["commitment_status"], "frozen_pre_execution")
        self.assertEqual(commitment["rng_contract"]["procedure_id"], "sha256_rejection_stream_v1")
        self.assertRegex(commitment["rng_contract"]["seed_hex"], r"^[0-9a-f]{64}$")
        self.assertTrue(
            commitment["timing"]["must_be_committed_and_integrity_rooted_before_any_confirmatory_execution"]
        )
        self.assertTrue(commitment["timing"]["must_precede_any_pilot_or_confirmatory_outcome_reveal"])
        self.assertEqual(analysis["bootstrap_resamples"], 100000)
        self.assertEqual(analysis["uncertainty_method"], "paired_task_bootstrap")
        spec = analysis["bootstrap_interval_spec"]
        self.assertEqual(
            spec,
            {
                "method": "percentile_equal_tailed",
                "confidence_level": 0.95,
                "lower_tail_probability": 0.025,
                "upper_tail_probability": 0.975,
                "resample_count": 100000,
                "resample_unit": "task",
                "resample_size": "number_of_complete_primary_tasks",
                "draws_with_replacement": True,
                "task_order": {
                    "contract": "task-manifest-contract-v1.0.json",
                    "source": "exact frozen ordered task manifest committed before outcome reveal",
                    "blind_identifier_pattern": "^TASK-[0-9]{6}$",
                    "blind_identifier_encoding": "ASCII subset of UTF-8; Unicode and normalization-sensitive identifiers are prohibited",
                    "sequence_rule": "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited",
                    "uniqueness_rule": "blind identifiers must be unique",
                    "complete_case_rule": "remove tasks with missing primary cells while preserving manifest-relative order",
                    "bootstrap_vector_rule": "D_i vector indices are exactly the remaining manifest array positions in order",
                },
                "rng_procedure": {
                    "id": "sha256_rejection_stream_v1",
                    "seed_format": "exactly 64 lowercase hexadecimal characters strictly base16-decoded into 32 bytes; the ASCII hex characters are not hashed",
                    "counter_encoding": "decoded_seed_32_bytes || uint64_be(resample_index) || uint64_be(draw_index) || uint32_be(rejection_counter)",
                    "digest": "SHA-256",
                    "integer": "first 8 digest bytes interpreted as unsigned big-endian",
                    "unbiased_index_rule": "reject x >= 2^64 - (2^64 mod N); otherwise index = x mod N; increment rejection_counter from zero until accepted",
                    "resample_index_origin": 0,
                    "draw_index_origin": 0,
                    "rejection_counter_origin": 0,
                },
                "quantile_convention": {
                    "id": "hyndman_fan_type_7",
                    "sorted_values": "ascending bootstrap estimates including duplicates",
                    "formula": "h=(m-1)*p; q=(1-f)*x[floor(h)] + f*x[ceil(h)], where f=h-floor(h), zero-based indices, and m=100000",
                },
                "classification_uses_bounds": "lower p=0.025 and upper p=0.975 from this exact procedure",
            },
        )


if __name__ == "__main__":
    unittest.main()
