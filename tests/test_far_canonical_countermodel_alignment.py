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
            "inductive Recovery",
            "| left",
            "| right",
            "both_recoveries_are_qualified",
            "recoveries_are_distinct",
            "unique_factorization_counterexample",
            "current_assumptions_refute_canonical_entailment",
            "full_canonical_bridge_fails_in_countermodel",
            "terminal_verdict_with_counterexample",
        )
        for token in required:
            self.assertIn(token, text)

    def test_registry_records_scoped_refutation(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "refuted_under_frozen_framework")
        self.assertEqual(data["answer"], "No")
        self.assertEqual(data["decisive_failure"], "unique_factorization")
        self.assertTrue(data["counterexample"]["base_evidence_satisfied"])
        self.assertTrue(data["counterexample"]["fully_faithful"])
        self.assertFalse(data["counterexample"]["recoveries_equal"])
        boundaries = data["claim_boundaries"]
        self.assertTrue(boundaries["does_not_refute_strengthened_far"])
        self.assertTrue(boundaries["does_not_claim_metaphysical_nonuniversality"])

    def test_workflow_compiles_and_checks_countermodel(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("lean mechanization/lean/FARCanonicalCountermodel.lean", text)
        self.assertIn("tests.test_far_canonical_countermodel_alignment", text)


if __name__ == "__main__":
    unittest.main()
