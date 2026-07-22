from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-extension-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w1_continuous_dynamics.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ContinuousDynamicsExtensionTests(unittest.TestCase):
    def test_continuous_dynamics_checker_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_scope_is_candidate_independent_and_certificate_bounded(self) -> None:
        scope = load(SCOPE)
        admission = scope["admission_rule"]
        self.assertTrue(admission["candidate_independent"])
        self.assertEqual(scope["version"], "1.1")
        self.assertEqual(scope["source_class"], "S_cd_lip_eff")
        self.assertIn("computable finite event enumerator", admission["events"])
        self.assertIn("certified rational crossing brackets", admission["events"])
        self.assertIn("isolated guard crossings without computable completeness certificates", admission["exclusions"])
        self.assertIn("nonunique flows", admission["exclusions"])
        self.assertIn("Zeno event accumulation", admission["exclusions"])
        self.assertIn("actual-process correspondence", admission["exclusions"])

    def test_grid_and_oracle_controls_are_rejected(self) -> None:
        fixtures = {item["id"]: item for item in load(FIXTURES)["fixtures"]}
        result = load(RESULT)
        self.assertEqual(fixtures["CD-NEG-GRID-001"]["expected"], "rejected")
        self.assertEqual(fixtures["CD-NEG-ORACLE-001"]["expected"], "rejected")
        self.assertEqual(result["fixture_results"]["CD-NEG-GRID-001"], "rejected")
        self.assertEqual(result["fixture_results"]["CD-NEG-ORACLE-001"], "rejected")

    def test_nonunique_and_zeno_cases_remain_scope_boundaries(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["fixture_results"]["CD-BOUND-NONUNIQ-001"], "excluded")
        self.assertEqual(result["fixture_results"]["CD-BOUND-ZENO-001"], "excluded")
        self.assertEqual(result["terminal_outcome"], "proper_subclass_only")

    def test_broader_claims_remain_unresolved(self) -> None:
        result = load(RESULT)
        claims = result["claim_effect"]
        self.assertEqual(claims["all_continuous_dynamics_representation"], "unresolved")
        self.assertEqual(claims["S_IRD_representation"], "unresolved")
        self.assertEqual(claims["universal_structure"], "unresolved")
        self.assertEqual(claims["primitive_necessity"], "not_established")
        self.assertEqual(claims["minimality"], "not_established")
        self.assertEqual(claims["uniqueness"], "not_established")
        self.assertEqual(result["machine_check_status"], "not_mechanized")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
