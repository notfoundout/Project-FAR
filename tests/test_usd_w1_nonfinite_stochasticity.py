from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-nonfinite-stochasticity-extension-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w1_nonfinite_stochasticity.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class NonFiniteStochasticityExtensionTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_scope_requires_effective_tail_and_conditioning_certificates(self) -> None:
        admission = load(SCOPE)["admission_rule"]
        self.assertTrue(admission["candidate_independent"])
        self.assertIn("certified effective tail bounds", admission["kernels"])
        self.assertIn("certified positive probability", admission["conditioning"])
        self.assertTrue(any("conditioning on null" in item for item in admission["exclusions"]))

    def test_truncation_and_oracle_controls_are_rejected(self) -> None:
        fixtures = {item["id"]: item for item in load(FIXTURES)["fixtures"]}
        result = load(RESULT)["fixture_results"]
        for item in ("NFS-NEG-TRUNC-001", "NFS-NEG-ORACLE-001"):
            self.assertEqual(fixtures[item]["expected"], "rejected")
            self.assertEqual(result[item], "rejected")

    def test_boundary_cases_remain_excluded(self) -> None:
        result = load(RESULT)
        for item in ("NFS-BOUND-NULL-001", "NFS-BOUND-NONCOMP-001", "NFS-BOUND-UNBOUNDED-001"):
            self.assertEqual(result["fixture_results"][item], "excluded")
        self.assertEqual(result["terminal_outcome"], "proper_subclass_only")

    def test_broader_claims_remain_unresolved(self) -> None:
        result = load(RESULT)
        claims = result["claim_effect"]
        self.assertEqual(claims["all_stochastic_reasoning_representation"], "unresolved")
        self.assertEqual(claims["S_IRD_representation"], "unresolved")
        self.assertEqual(claims["universal_structure"], "unresolved")
        self.assertEqual(claims["primitive_necessity"], "not_established")
        self.assertEqual(claims["minimality"], "not_established")
        self.assertEqual(claims["uniqueness"], "not_established")
        self.assertEqual(result["machine_check_status"], "not_mechanized")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
