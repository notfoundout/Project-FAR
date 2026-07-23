import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization/lean/FARCanonicalUniversalityDecision.lean"
REGISTRY = ROOT / "theory/evaluation/far-canonical-universality-decision-v1.0.json"
WORKFLOW = ROOT / ".github/workflows/lean.yml"


class FARCanonicalUniversalityDecisionAlignmentTests(unittest.TestCase):
    def test_registry_terminal_verdict_is_not_derivable(self) -> None:
        data = json.loads(REGISTRY.read_text())
        self.assertEqual(data["status"], "terminal_for_current_evidence")
        self.assertEqual(data["verdict"], "not_derivable")
        self.assertEqual(
            set(data["canonical_bridges"].values()), {"not_established"}
        )

    def test_registry_does_not_turn_absence_into_refutation(self) -> None:
        data = json.loads(REGISTRY.read_text())
        nonclaims = set(data["nonclaims"])
        self.assertIn("canonical universality is false", nonclaims)
        self.assertIn("a counterexample to FAR has been found", nonclaims)
        self.assertIn("missing bridge witnesses count as negative evidence", nonclaims)

    def test_lean_contains_terminal_nonderivability_and_sufficiency(self) -> None:
        text = LEAN.read_text()
        required = [
            "theorem base_does_not_entail_all_bridges",
            "theorem current_far_terminal_verdict",
            "theorem all_six_witnesses_are_sufficient",
            "theorem missing_witnesses_do_not_refute",
            ".notDerivable",
            ".canonicalProved",
            ".canonicalRefuted",
        ]
        for fragment in required:
            self.assertIn(fragment, text)

    def test_all_six_bridge_independence_theorems_are_present(self) -> None:
        text = LEAN.read_text()
        for name in (
            "unique_factorization_not_derivable_from_base",
            "representation_invariance_not_derivable_from_base",
            "quotient_minimality_not_derivable_from_base",
            "definitional_completeness_not_derivable_from_base",
            "conservative_extensibility_not_derivable_from_base",
            "maximal_knowability_not_derivable_from_base",
        ):
            self.assertIn(f"theorem {name}", text)

    def test_no_untrusted_proof_escape_hatches(self) -> None:
        text = LEAN.read_text().lower()
        for forbidden in ("axiom ", "sorry", "admit", "unsafe"):
            self.assertNotIn(forbidden, text)

    def test_protected_workflow_compiles_and_checks_decision(self) -> None:
        text = WORKFLOW.read_text()
        self.assertIn(
            "lean mechanization/lean/FARCanonicalUniversalityDecision.lean", text
        )
        self.assertIn(
            "python -m unittest tests.test_far_canonical_universality_decision", text
        )


if __name__ == "__main__":
    unittest.main()
