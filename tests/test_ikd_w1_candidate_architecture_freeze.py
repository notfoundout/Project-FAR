from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json"


class IKDW1CandidateArchitectureFreezeTests(unittest.TestCase):
    def load(self) -> dict:
        return json.loads(FREEZE.read_text(encoding="utf-8"))

    def test_validator_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_ikd_w1_candidate_architecture_freeze.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_six_materially_distinct_families_are_frozen(self):
        freeze = self.load()
        candidates = freeze["frozen_candidates"]
        self.assertEqual(len(candidates), 6)
        self.assertEqual(len({item["family"] for item in candidates}), 6)
        self.assertTrue(all(item["status"] == "admitted_frozen_unscored" for item in candidates))

    def test_hidden_reconstructions_are_rejected(self):
        freeze = self.load()
        novelty = set(freeze["admission_rule"]["material_novelty_tests"])
        rejected = set(freeze["admission_rule"]["automatic_rejection"])
        self.assertIn("not_a_hidden_commitment_equivalent_reconstruction", novelty)
        self.assertIn("undeclared_equivalent_reintroduction", rejected)
        self.assertIn("unrestricted_interpreter", rejected)

    def test_no_scoring_or_universal_claim_is_authorized(self):
        freeze = self.load()
        prohibited = set(freeze["execution_gate"]["prohibited_before_merge"])
        self.assertIn("candidate_scoring", prohibited)
        self.assertIn("frontier_update", prohibited)
        self.assertIn("common_factor_claim", prohibited)
        self.assertIn("universal_structure_claim", prohibited)

    def test_comparison_remains_pareto_and_dimensioned(self):
        contract = self.load()["comparison_contract"]
        self.assertEqual(contract["aggregation"], "pareto_only_no_scalar_score")
        self.assertEqual(len(contract["preservation_dimensions"]), 6)
        self.assertEqual(len(contract["cost_coordinates"]), 5)
        self.assertEqual(contract["unknown_rule"], "Unknown is unresolved and is not Pass")


if __name__ == "__main__":
    unittest.main()
