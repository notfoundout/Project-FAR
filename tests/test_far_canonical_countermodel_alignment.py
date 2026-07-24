import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization" / "lean" / "FARCanonicalCountermodel.lean"
REGISTRY = ROOT / "theory" / "terminal" / "far-canonical-countermodel-v1.0.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"


class FARCanonicalCountermodelAlignmentTests(unittest.TestCase):
    def test_proof_contains_no_admissions(self):
        text = LEAN.read_text(encoding="utf-8")
        for forbidden in ("sorry", "admit", "axiom", "unsafe"):
            self.assertNotIn(forbidden, text)

    def test_countermodel_is_concrete_and_decisive(self):
        text = LEAN.read_text(encoding="utf-8")
        required = (
            "import UPPSemanticKernel",
            "def groundedModel : FrozenUPPSemantics",
            "PreservationVector",
            "commitmentEquivalent := groundedEquivalent",
            "faithfulCandidateEquivalent := by",
            "left_is_fully_qualified",
            "right_is_fully_qualified",
            "left_equivalent_to_canonical",
            "right_equivalent_to_canonical",
            "left_not_equivalent_to_right",
            "current_g1_semantics_do_not_entail_canonical_uniqueness",
        )
        for token in required:
            self.assertIn(token, text)

    def test_countermodel_does_not_use_boolean_proxy_fields(self):
        text = LEAN.read_text(encoding="utf-8")
        forbidden = (
            "structure FrozenModel",
            "g1RelativeSemantics : Bool",
            "fullyFaithful : Bool",
            "leftPreservesCommitments : Bool",
            "rightPreservesCommitments : Bool",
        )
        for token in forbidden:
            self.assertNotIn(token, text)

    def test_registry_records_scoped_refutation(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "grounded_refutation_of_g1_canonical_uniqueness")
        self.assertEqual(data["answer"], "No under the current G1 semantics")
        self.assertEqual(data["decisive_failure"], "pairwise_unique_recovery_up_to_registered_equivalence")
        counterexample = data["counterexample"]
        self.assertEqual(counterexample["model_type"], "FrozenUPPSemantics")
        self.assertTrue(counterexample["uses_actual_registered_predicates"])
        self.assertTrue(counterexample["both_candidates_fully_preserved"])
        self.assertTrue(counterexample["each_candidate_equivalent_to_canonical"])
        self.assertFalse(counterexample["candidates_equivalent_to_each_other"])
        boundaries = data["claim_boundaries"]
        self.assertTrue(boundaries["does_not_refute_strengthened_far"])
        self.assertTrue(boundaries["does_not_claim_metaphysical_nonuniversality"])

    def test_workflow_compiles_and_checks_countermodel(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("lean mechanization/lean/FARCanonicalCountermodel.lean", text)
        self.assertIn("tests.test_far_canonical_countermodel_alignment", text)


if __name__ == "__main__":
    unittest.main()
