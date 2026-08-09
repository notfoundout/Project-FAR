from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "research/external-validation/swe-agent-v3/preregistration-v1.0.json"
SEED_PATH = ROOT / "research/external-validation/swe-agent-v3/bootstrap-seed-commitment-contract-v1.0.json"
HARM_PATH = ROOT / "research/external-validation/swe-agent-v3/critical-harm-thresholds-v1.0.json"
TASK_PATH = ROOT / "research/external-validation/swe-agent-v3/task-manifest-contract-v1.0.json"


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

    def test_decision_categories_are_ordered_nonoverlapping_and_harm_gated(self) -> None:
        analysis = self.load_analysis()
        self.assertEqual(
            analysis["decision_precedence"],
            ["inconclusive_due_to_missingness", "bounded_harm", "bounded_positive", "no_practical_advantage", "inconclusive"],
        )
        categories = analysis["decision_categories"]
        self.assertIn("upper bound < 0", categories["bounded_harm"])
        self.assertIn("0 <= 95% paired-task bootstrap upper bound < 0.10", categories["no_practical_advantage"])
        self.assertIn("critical-harm-thresholds-v1.0.json", categories["bounded_positive"])
        self.assertEqual(analysis["critical_harm_contract"], "critical-harm-thresholds-v1.0.json")
        harm = json.loads(HARM_PATH.read_text(encoding="utf-8"))
        self.assertEqual(harm["schema_version"], "1.1")
        self.assertEqual(harm["rate_harms"]["regression_introduction_rate"]["critical_threshold"], {"numerator": 1, "denominator": 10})
        self.assertEqual(harm["rate_harms"]["invalid_run_rate"]["critical_threshold"], {"numerator": 1, "denominator": 10})
        self.assertTrue(all(rule["trigger_rule"] == "slot_numerator > 0" for rule in harm["zero_tolerance_harms"].values()))
        self.assertTrue(all(rule["critical_threshold"] == {"allowed_occurrences": 0} for rule in harm["zero_tolerance_harms"].values()))
        self.assertIn("no causal-attribution override", harm["rate_harms"]["regression_introduction_rate"]["slot_numerator"])
        self.assertIn("frozen_task_identity_ledger_git_blob_sha1", harm["evidence_retention"]["required_provenance"])

    def test_bootstrap_interval_rng_order_strata_ledger_and_seed_are_fully_frozen(self) -> None:
        analysis = self.load_analysis()
        self.assertEqual(
            analysis["bootstrap_seed_status"],
            "frozen_by_bootstrap-seed-commitment-contract-v1.0.json_before_execution",
        )
        self.assertEqual(analysis["bootstrap_seed_contract"], "bootstrap-seed-commitment-contract-v1.0.json")
        commitment = json.loads(SEED_PATH.read_text(encoding="utf-8"))
        self.assertEqual(commitment["commitment_status"], "frozen_pre_execution")
        self.assertEqual(commitment["rng_contract"]["procedure_id"], "sha256_rejection_stream_v1")
        self.assertRegex(commitment["rng_contract"]["seed_hex"], r"^[0-9a-f]{64}$")
        self.assertEqual(commitment["commitment"]["method"], "direct_precommitted_value")
        self.assertFalse(commitment["commitment"]["mutable_launch_inputs_permitted"])
        self.assertTrue(commitment["timing"]["must_be_committed_and_integrity_rooted_before_any_confirmatory_execution"])
        self.assertTrue(commitment["timing"]["must_precede_any_pilot_or_confirmatory_outcome_reveal"])
        self.assertEqual(analysis["bootstrap_resamples"], 100000)
        self.assertEqual(analysis["uncertainty_method"], "paired_task_bootstrap")
        spec = analysis["bootstrap_interval_spec"]
        self.assertEqual(spec["method"], "percentile_equal_tailed")
        self.assertEqual(spec["confidence_level"], 0.95)
        self.assertEqual(spec["lower_tail_probability"], 0.025)
        self.assertEqual(spec["upper_tail_probability"], 0.975)
        self.assertEqual(spec["resample_count"], 100000)
        self.assertEqual(spec["resample_unit"], "task")
        self.assertEqual(spec["resample_size"], "number_of_complete_primary_tasks")
        self.assertTrue(spec["draws_with_replacement"])
        order = spec["task_order"]
        self.assertEqual(order["contract"], "task-manifest-contract-v1.0.json")
        self.assertIn("before any sacrificial pilot or confirmatory execution", order["source"])
        self.assertIn("sealed identity ledger", order["sealed_identity_ledger"])
        self.assertEqual(order["sequence_rule"], "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited")
        self.assertEqual(order["uniqueness_rule"], "blind identifiers and task-bundle roots must each be unique")
        self.assertIn("manifest-wide union must cover all five before execution", order["strata_rule"])
        task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
        self.assertEqual(task["schema_version"], "1.6")
        self.assertEqual(task["sealed_identity_ledger_contract"]["status"], "uninstantiated")
        self.assertFalse(task["sealed_identity_ledger_contract"]["execution_authorized"])
        rng = spec["rng_procedure"]
        self.assertEqual(
            rng,
            {
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
        )
        self.assertEqual(
            spec["quantile_convention"],
            {
                "id": "hyndman_fan_type_7",
                "sorted_values": "ascending bootstrap estimates including duplicates",
                "formula": "h=(m-1)*p; q=(1-f)*x[floor(h)] + f*x[ceil(h)], where f=h-floor(h), zero-based indices, and m=100000",
            },
        )
        self.assertEqual(spec["classification_uses_bounds"], "lower p=0.025 and upper p=0.975 from this exact procedure")


if __name__ == "__main__":
    unittest.main()
