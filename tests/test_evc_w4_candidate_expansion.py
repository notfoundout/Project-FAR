import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CandidateExpansionTests(unittest.TestCase):
    def test_checker(self):
        completed = subprocess.run([sys.executable, "tools/check_evc_w4_candidate_expansion.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_claim_boundary_and_controls(self):
        protocol = json.loads((ROOT / "theory/evaluation/evc-w4-candidate-expansion-protocol-v1.0.json").read_text())
        manifest = json.loads((ROOT / "theory/evaluation/evc-w4-candidate-expansion-manifest-v1.0.json").read_text())
        self.assertIn("failure to alter the frontier proves global minimality", protocol["nonclaims"])
        self.assertIn("failure-to-find converted into exhaustiveness", manifest["required_controls"])
        self.assertEqual(protocol["decision_rules"]["frontier"], "The frontier is recomputed componentwise with no scalar score and no preferred-vocabulary tie breaker.")

if __name__ == "__main__":
    unittest.main()
