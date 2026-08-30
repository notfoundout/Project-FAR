from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/check_project_far_theory_closure.py"
SPEC = importlib.util.spec_from_file_location("project_far_theory_closure_check", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ProjectFARTheoryClosureTest(unittest.TestCase):
    # Historical regression identities are intentionally retained.  They remain
    # part of the validator-assurance contract even though v1.1 strengthens the
    # assertions they protect.
    def test_repository_conforms_to_terminal_theory(self):
        self.assertEqual([], MODULE.validate())

    def test_repository_conforms_to_corrected_terminal_theory(self):
        self.assertEqual([], MODULE.validate())

    def test_exact_claim_set_is_closed(self):
        historical = MODULE._load(
            ROOT / "theory/terminal/project-far-core-theory-v1.0.json"
        )
        current = MODULE._load(
            ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
        )
        expected = {f"FAR-CORE-{i:03d}" for i in range(1, 15)}
        self.assertEqual(expected, {row["id"] for row in historical["claims"]})
        self.assertEqual(expected, {row["id"] for row in current["claims"]})

    def test_v1_0_is_immutable_historical_evidence(self):
        data = (ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.0.md").read_bytes()
        self.assertEqual(MODULE.EXPECTED_V1_SHA256, hashlib.sha256(data).hexdigest())

    def test_exact_claim_set_is_preserved(self):
        ledger = MODULE._load(
            ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
        )
        self.assertEqual("PROJECT-FAR-CORE-THEORY-1.1", ledger["theory_id"])
        self.assertEqual(
            {f"FAR-CORE-{i:03d}" for i in range(1, 15)},
            {row["id"] for row in ledger["claims"]},
        )
        proved = {
            row["id"] for row in ledger["claims"] if row["status"] == "proved"
        }
        self.assertEqual({f"FAR-CORE-{i:03d}" for i in range(1, 14)}, proved)
        self.assertEqual(
            "supported_derived", MODULE._claim(ledger, "FAR-CORE-014")["status"]
        )

    def test_far_core_004_distinguishes_sufficiency_from_minimality(self):
        ledger = MODULE._load(
            ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
        )
        claim = MODULE._claim(ledger, "FAR-CORE-004")["claim"]
        self.assertIn("least-informative sufficient", claim)
        self.assertIn("universal sufficiency alone is not denied", claim)
        fixture = MODULE._load(
            ROOT / "theory/evaluation/project-far-core-theory-v1.1-regressions.json"
        )
        case = next(
            c
            for c in fixture["cases"]
            if c["id"] == "CE-CORE-004-IDENTITY-SUFFICES"
        )
        self.assertTrue(case["expected"]["representation_sufficient_for_constant"])
        self.assertTrue(case["expected"]["representation_sufficient_for_injective"])
        self.assertFalse(case["expected"]["representation_minimal_for_constant"])

    def test_far_core_010_separates_exact_theory_from_frame_residue(self):
        ledger = MODULE._load(
            ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
        )
        claim = MODULE._claim(ledger, "FAR-CORE-010")["claim"]
        self.assertIn("L,J,I", claim)
        self.assertIn("Γ", claim)
        fixture = MODULE._load(
            ROOT / "theory/evaluation/project-far-core-theory-v1.1-regressions.json"
        )
        case = next(
            c
            for c in fixture["cases"]
            if c["id"] == "CE-CORE-010-FRAME-DOES-NOT-INDEX-T"
        )
        self.assertTrue(case["expected"]["exact_theory_same_under_frames"])
        self.assertNotEqual(
            case["expected"]["residue_Gamma0"],
            case["expected"]["residue_Gamma1"],
        )

    def test_w1_independent_review_remains_open(self):
        """Historical regression identity: the old open gate may close only via the sealed promotion."""
        promotion = MODULE._load(
            ROOT / "theory/evaluation/pca-w1-independent-review-promotion-v1.0.json"
        )
        self.assertEqual("PCA-W1-INDEPENDENT-REVIEW", promotion["workstream_id"])
        self.assertEqual("ACCEPTED_COMPLETE", promotion["disposition"])
        self.assertTrue(promotion["effective_on_merge"])
        self.assertEqual(
            "14105775daf3c5713b134a728db2e1e53673af97",
            promotion["review_target"]["commit"],
        )
        self.assertFalse(promotion["findings"]["theorem_correction_required"])

    def test_w1_promotion_leads_through_w4_to_w5(self):
        """The assurance sequence must preserve completed W1–W4 and advance to W5."""
        program = MODULE._load(
            ROOT
            / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
        )
        workstreams = {row["id"]: row for row in program["workstreams"]}
        self.assertEqual("complete", workstreams["PCA-W1-INDEPENDENT-REVIEW"]["state"])
        self.assertEqual(
            "complete",
            workstreams["PCA-W2-PROOF-ASSISTANT-FORMALIZATION"]["state"],
        )
        self.assertEqual(
            "complete",
            workstreams["PCA-W3-CONTRACT-SCHEMA"]["state"],
        )
        self.assertEqual(
            "complete",
            workstreams["PCA-W4-DOMAIN-CONTRACTS"]["state"],
        )
        self.assertEqual(
            "PCA-W5-APPROXIMATION-AND-COST",
            program["next_action"]["workstream"],
        )
        self.assertEqual(
            "PROJECT-FAR-CORE-THEORY-1.1",
            program["next_action"]["theory_target"],
        )

    def test_historical_upp_is_not_current_authority(self):
        old = MODULE._load(
            ROOT
            / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json"
        )
        self.assertEqual("superseded", old["status"])
        self.assertEqual("POST-CLOSURE-001", old["superseded_by"])

    def test_historical_primitive_and_operator_results_are_reclassified(self):
        primitive = (
            ROOT / "frameworks/FARA/research/primitive-independence-w1-result.md"
        ).read_text()
        operator = (
            ROOT / "theory/evaluation/generated-fara-operator-w2-summary.md"
        ).read_text()
        self.assertIn(
            "global primitive-independence/minimality search is closed", primitive
        )
        self.assertIn("global finite-basis search is closed", operator)
        self.assertNotIn("remains only a candidate primitive", primitive)
        self.assertNotIn("**Global claim:** unresolved.", operator)

    def test_legacy_open_question_path_cannot_claim_current_status(self):
        old = (ROOT / "research/open-problems/open-questions.md").read_text()
        self.assertIn("Historical Open Questions Register (Superseded)", old)
        self.assertNotIn("**Status:** Active", old)
        self.assertNotIn("**Status:** Open", old)


if __name__ == "__main__":
    unittest.main()
