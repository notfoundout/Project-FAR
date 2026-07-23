from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization" / "lean" / "G3EpistemicMaximality.lean"
REGISTRY = ROOT / "theory" / "terminal" / "g3-epistemic-maximality-v1.0.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"


class G3EpistemicMaximalityAlignmentTests(unittest.TestCase):
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

    def test_underdetermination_theorems_exist(self) -> None:
        for theorem in [
            "indistinguishable_incompatible_sources_block_joint_soundness",
            "incompatible_twin_refutes_discriminating_access",
            "g3_epistemic_maximality_theorem",
        ]:
            self.assertIn(f"theorem {theorem}", self.lean)

    def test_unknown_is_preserved_both_directions(self) -> None:
        self.assertIn("inaccessible_adjudicates_unknown", self.lean)
        self.assertIn("inaccessible_never_adjudicates_pass", self.lean)
        self.assertIn("inaccessible_never_adjudicates_fail", self.lean)
        self.assertEqual(self.registry["boundary"]["inaccessible_cases"], "unknown")
        self.assertFalse(self.registry["boundary"]["unknown_counts_as_support"])
        self.assertFalse(self.registry["boundary"]["unknown_counts_as_refutation"])

    def test_boundary_is_symmetric_not_rccd_loading(self) -> None:
        self.assertFalse(self.registry["claims"]["inaccessibility_is_evidence_for_rccd"])
        self.assertFalse(self.registry["claims"]["inaccessibility_is_evidence_against_rccd"])
        self.assertTrue(self.registry["result"]["symmetrical_for_fAR_and_competitors"])
        code = re.sub(r"/-.*?-/", "", self.lean, flags=re.DOTALL)
        self.assertNotIn("RCCD", code)

    def test_final_claim_taxonomy_is_exact(self) -> None:
        taxonomy = self.registry["final_claim_taxonomy"]
        self.assertFalse(taxonomy["unrestricted_metaphysical_universality"])
        self.assertTrue(taxonomy["open_world_universality_over_admissible_faithful_candidates"])
        self.assertTrue(taxonomy["maximal_epistemically_establishable_universality"])
        self.assertFalse(taxonomy["inaccessible_cases_resolved_as_rccd"])
        self.assertEqual(self.registry["remaining_obligations"], [])

    def test_workflow_compiles_and_tests_g3(self) -> None:
        self.assertIn("lean mechanization/lean/G3EpistemicMaximality.lean", self.workflow)
        self.assertIn("python -m unittest tests.test_g3_epistemic_maximality_alignment", self.workflow)


if __name__ == "__main__":
    unittest.main()
