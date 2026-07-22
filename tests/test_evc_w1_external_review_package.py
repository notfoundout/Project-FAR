from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/evc-w1-external-proof-review-protocol-v1.0.json"
MANIFEST = ROOT / "theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json"
TEMPLATE = ROOT / "theory/evaluation/evc-w1-external-review-result-template-v1.0.json"
CHECKER = ROOT / "tools/check_evc_w1_external_review_package.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ExternalReviewPackageTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(CHECKER)], cwd=ROOT, text=True,
            capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_external_review_is_not_predeclared(self) -> None:
        protocol = load(PROTOCOL)
        manifest = load(MANIFEST)
        self.assertEqual(protocol["status"], "frozen_unexecuted")
        self.assertFalse(protocol["claim_effect"]["external_review_completed"])
        self.assertFalse(protocol["claim_effect"]["independent_verification_established"])
        self.assertFalse(manifest["release_state"]["reviewer_accessed"])
        self.assertFalse(manifest["release_state"]["external_review_started"])

    def test_independence_and_freeze_rules_are_explicit(self) -> None:
        protocol = load(PROTOCOL)
        disqualifying = " ".join(protocol["reviewer_eligibility"]["disqualifying"])
        self.assertIn("shared generation", disqualifying)
        self.assertIn("substantive author coaching", disqualifying)
        self.assertTrue(protocol["author_response_boundary"]["initial_verdict_before_response"])
        self.assertIn("new package version", protocol["freeze_and_access"]["post_access_rule"])

    def test_result_template_preserves_initial_verdict(self) -> None:
        template = load(TEMPLATE)
        self.assertEqual(len(template["obligation_matrix"]), 10)
        self.assertIn("amendment may not erase the initial verdict", template["validation_rules"])
        self.assertIn("blocking_objection", template["allowed_verdicts"])
        self.assertIsNone(template["initial_verdict"])
        self.assertIsNone(template["amended_verdict"])

    def test_universal_claims_remain_blocked(self) -> None:
        protocol = load(PROTOCOL)
        excluded = set(protocol["review_target"]["excluded_claims"])
        self.assertIn("global universality", excluded)
        self.assertIn("global minimality", excluded)
        self.assertIn("actual-process correspondence", excluded)
        self.assertFalse(protocol["claim_effect"]["universal_structure_established"])


if __name__ == "__main__":
    unittest.main()
