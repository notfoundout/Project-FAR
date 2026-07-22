from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "theory/evaluation/usd-w6-independence-contract-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w6-independence-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w6_independence.py"

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

class USDW6IndependenceTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_independence_layers_are_not_collapsed(self) -> None:
        contract = load(CONTRACT)
        self.assertEqual(len(contract["layers"]), 5)
        self.assertEqual(contract["layers"]["internal_multi_implementation_robustness"]["status"], "executed")
        for layer in ("independent_proof_review", "R3_independent_technical_replication", "R4_adversarial_conceptual_replication", "R5_cross_context_replication"):
            self.assertEqual(contract["layers"][layer]["status"], "not_executed")

    def test_internal_robustness_controls_pass(self) -> None:
        result = load(RESULT)
        execution = result["internal_execution"]
        self.assertEqual(execution["isolated_implementations"], 3)
        self.assertFalse(execution["artifact_cross_access"])
        self.assertTrue(execution["separate_verifier"])
        self.assertEqual(execution["deterministic_comparison"], "pass")
        self.assertEqual(execution["mutation_campaign"], "pass")

    def test_external_claim_remains_prohibited(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["terminal_outcome"], "internal_robustness_only")
        self.assertEqual(result["claim_effect"]["independent_verification_claim"], "prohibited")
        self.assertEqual(result["claim_effect"]["independent_proof_review"], "unresolved")
        self.assertEqual(result["claim_effect"]["independent_technical_replication"], "unresolved")
        self.assertEqual(result["claim_effect"]["universal_structure"], "unresolved")

if __name__ == "__main__":
    unittest.main()
