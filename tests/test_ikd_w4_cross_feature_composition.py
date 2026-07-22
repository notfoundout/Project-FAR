from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/ikd-w4-cross-feature-composition-v1.0.json"


class IKDW4CrossFeatureCompositionTests(unittest.TestCase):
    def load(self) -> dict:
        return json.loads(RESULT.read_text(encoding="utf-8"))

    def test_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_ikd_w4_cross_feature_composition.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("42 joint cases", completed.stdout)

    def test_complete_joint_matrix_is_registered(self):
        cases = self.load()["executed_case_classes"]
        self.assertEqual(cases["pairwise"]["count"], 15)
        self.assertEqual(cases["triple"]["count"], 20)
        self.assertEqual(cases["leave_one_out_five_feature"]["count"], 6)
        self.assertEqual(cases["all_six"]["count"], 1)
        all_ids = (
            cases["pairwise"]["case_ids"]
            + cases["triple"]["case_ids"]
            + cases["leave_one_out_five_feature"]["case_ids"]
            + cases["all_six"]["case_ids"]
        )
        self.assertEqual(len(all_ids), 42)
        self.assertEqual(len(set(all_ids)), 42)

    def test_all_six_preserves_every_rccd_commitment(self):
        preservation = set(self.load()["all_six_construction"]["rccd_preservation"])
        self.assertEqual(
            preservation,
            {
                "recoverable commitment content",
                "constrained admissible evolution",
                "dependency-preserving explicit revision",
                "queryable historical identity",
                "uniform bounded-query recovery",
            },
        )

    def test_compatibility_conditions_are_not_hidden(self):
        contract = self.load()["composition_contract"]
        self.assertTrue(contract["shared_state_identity_required"])
        self.assertTrue(contract["semantic_versions_total_on_reachable_states"])
        self.assertTrue(contract["observation_and_probability_interfaces_measurable_and_computable"])
        self.assertTrue(contract["history_queries_finite_and_prefix_coherent"])
        self.assertTrue(contract["continuous_and_discrete_events_use_declared_hybrid_semantics"])
        self.assertTrue(contract["all_adapters_schedulers_tail_certificates_and_canonicalizers_charged"])

    def test_negative_controls_block_false_composition(self):
        controls = set(self.load()["negative_controls"])
        self.assertIn("featurewise_passes_multiplied_without_joint_construction_rejected", controls)
        self.assertIn("nonmeasurable_observation_kernel_rejected", controls)
        self.assertIn("hidden_scheduler_or_adapter_rejected", controls)
        self.assertIn("future_history_access_rejected", controls)

    def test_claim_boundary_remains_bounded(self):
        result = self.load()
        self.assertEqual(
            result["terminal_result"],
            "bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions",
        )
        self.assertEqual(result["claim_effect"]["arbitrary_feature_conjunctions"], "not_supported")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")
        self.assertIn("RCCD-001 is globally universal", result["nonclaims"])


if __name__ == "__main__":
    unittest.main()
