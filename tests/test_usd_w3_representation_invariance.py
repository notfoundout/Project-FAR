from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w3-representation-invariance-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w3_representation_invariance.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RepresentationInvarianceTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_all_registered_transformations_pass(self) -> None:
        contract, result = load(CONTRACT), load(RESULT)
        self.assertEqual(set(contract["transformations"]), set(result["transformation_results"]))
        self.assertTrue(all(value == "pass" for value in result["transformation_results"].values()))

    def test_non_equivalent_mutations_are_rejected(self) -> None:
        contract, result = load(CONTRACT), load(RESULT)
        self.assertEqual(set(contract["negative_controls"]), set(result["negative_control_results"]))
        self.assertTrue(all(value == "rejected" for value in result["negative_control_results"].values()))

    def test_pareto_relations_are_stable_without_a_winner(self) -> None:
        result = load(RESULT)
        self.assertIn("incomparability_preserved", result["comparison_effect"]["FARA_vs_LTS_PROV"])
        self.assertEqual(result["terminal_outcome"], "bounded_invariance_supported")

    def test_global_claims_remain_unresolved(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["claim_effect"]["THM-US-INV-001"], "bounded_support_only")
        self.assertEqual(result["claim_effect"]["THM-US-EXIST-001"], "unresolved")
        self.assertEqual(result["claim_effect"]["THM-US-NEC-001"], "unresolved")
        self.assertEqual(result["claim_effect"]["THM-US-MIN-001"], "unresolved")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
