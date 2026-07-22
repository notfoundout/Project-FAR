from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w4-ablation-reconstruction-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w4_ablation_reconstruction.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AblationReconstructionTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_every_unit_is_load_bearing_or_equivalently_reintroduced(self) -> None:
        result = load(RESULT)
        allowed = {"locally_load_bearing", "equivalently_reintroduced"}
        for values in result["vocabulary_results"].values():
            self.assertTrue(all(value in allowed for value in values.values()))

    def test_no_cheaper_non_equivalent_reconstruction_succeeds(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["reconstruction_summary"]["successful_strictly_cheaper_non_equivalent_reconstructions"], [])
        self.assertTrue(result["reconstruction_summary"]["all_reintroduced_machinery_charged"])

    def test_incomparability_is_preserved(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["comparison_effect"]["FARA_vs_LTS_PROV"], "bounded_incomparability_preserved")
        self.assertEqual(result["comparison_effect"]["winner"], "none")

    def test_global_claims_remain_unresolved(self) -> None:
        contract, result = load(CONTRACT), load(RESULT)
        self.assertIn("not global necessity", contract["global_boundary"])
        self.assertEqual(result["claim_effect"]["H_N_global"], "unresolved")
        self.assertEqual(result["claim_effect"]["THM-US-MIN-001"], "unresolved")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
