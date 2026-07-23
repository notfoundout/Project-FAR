from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization" / "lean" / "G2OpenWorldLowerBound.lean"
REGISTRY = ROOT / "theory" / "terminal" / "g2-open-world-lower-bound-v1.0.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"


class G2OpenWorldLowerBoundAlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lean = LEAN.read_text(encoding="utf-8")
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_no_axioms_or_admissions(self) -> None:
        forbidden = [r"\baxiom\b", r"\bsorry\b", r"\badmit\b", r"\bunsafe\b"]
        code = re.sub(r"/-.*?-/", "", self.lean, flags=re.DOTALL)
        code = re.sub(r"--.*", "", code)
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, code), pattern)

    def test_open_world_quantifiers_are_not_finite_enumeration(self) -> None:
        self.assertIn("{Candidate : Type}", self.lean)
        self.assertIn("∀ candidate", self.lean)
        for forbidden in ["candidateLedger", "registeredCandidates", "finiteCases"]:
            self.assertNotIn(forbidden, self.lean)
        self.assertFalse(self.registry["quantification"]["finite_candidate_ledger_required"])
        self.assertFalse(self.registry["quantification"]["vocabulary_enumeration_required"])

    def test_all_preservation_dimensions_are_explicit(self) -> None:
        for field in self.registry["independent_preservation_dimensions"]:
            self.assertRegex(self.lean, rf"\b{re.escape(field)}\b")

    def test_all_rccd_obligations_are_derived(self) -> None:
        for field in self.registry["derived_rccd_obligations"]:
            self.assertRegex(self.lean, rf"\b{re.escape(field)}\b")

    def test_bridge_is_explicit(self) -> None:
        self.assertIn("structure IndependentLowerBoundBridge", self.lean)
        self.assertIn("full_faithfulness_implies_rccd_obligations", self.lean)
        self.assertIn("g2_open_world_structural_lower_bound", self.lean)

    def test_claim_boundary_preserves_g3(self) -> None:
        self.assertEqual(self.registry["obligation"], "G2")
        self.assertTrue(self.registry["claims"]["open_world_over_admissible_faithful_candidates"])
        self.assertFalse(self.registry["claims"]["metaphysical_universality"])
        self.assertFalse(self.registry["claims"]["inaccessible_reasoning_resolved"])
        self.assertEqual(self.registry["remaining_obligations"], ["G3"])

    def test_workflow_compiles_and_tests_g2(self) -> None:
        self.assertIn("lean mechanization/lean/G2OpenWorldLowerBound.lean", self.workflow)
        self.assertIn("python -m unittest tests.test_g2_open_world_lower_bound_alignment", self.workflow)


if __name__ == "__main__":
    unittest.main()
