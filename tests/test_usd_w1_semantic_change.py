from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-semantic-change-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-semantic-change-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-semantic-change-extension-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w1_semantic_change.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SemanticChangeExtensionTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_scope_is_candidate_independent_and_versioned(self) -> None:
        scope = load(SCOPE)
        admission = scope["admission_rule"]
        self.assertTrue(admission["candidate_independent"])
        self.assertEqual(scope["source_class"], "S_sem_eff")
        self.assertIn("partial-correspondence map", admission["translation_contract"])
        self.assertIn("unresolved commitments", admission["translation_contract"])
        self.assertIn("retroactive erasure of prior semantic states", admission["exclusions"])

    def test_label_and_erasure_controls_are_rejected(self) -> None:
        fixtures = {item["id"]: item for item in load(FIXTURES)["fixtures"]}
        result = load(RESULT)["fixture_results"]
        for item in ("SC-NEG-LABEL-001", "SC-NEG-ERASE-001"):
            self.assertEqual(fixtures[item]["expected"], "rejected")
            self.assertEqual(result[item], "rejected")

    def test_oracle_and_global_rewrite_remain_boundaries(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["fixture_results"]["SC-BOUND-ORACLE-001"], "excluded")
        self.assertEqual(result["fixture_results"]["SC-BOUND-GLOBAL-001"], "excluded")
        self.assertEqual(result["terminal_outcome"], "proper_subclass_only")

    def test_broader_claims_remain_unresolved(self) -> None:
        result = load(RESULT)
        claims = result["claim_effect"]
        self.assertEqual(claims["all_semantic_change_representation"], "unresolved")
        self.assertEqual(claims["S_IRD_representation"], "unresolved")
        self.assertEqual(claims["universal_structure"], "unresolved")
        self.assertEqual(claims["primitive_necessity"], "not_established")
        self.assertEqual(claims["minimality"], "not_established")
        self.assertEqual(claims["uniqueness"], "not_established")
        self.assertEqual(result["machine_check_status"], "not_mechanized")
        self.assertEqual(result["independent_review_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
