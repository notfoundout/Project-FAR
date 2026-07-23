from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization" / "lean" / "UPPSemanticKernel.lean"
REGISTRY = ROOT / "theory" / "terminal" / "g1-semantic-kernel-v1.0.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"


class UPPSemanticKernelAlignmentTests(unittest.TestCase):
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

    def test_terminal_theorem_and_constructor_exist(self) -> None:
        self.assertIn("def constructSourceSemanticResult", self.lean)
        self.assertIn("theorem g1_end_to_end_relative_semantic_theorem", self.lean)
        self.assertIn("theorem faithful_candidate_equivalent_to_canonical", self.lean)

    def test_all_preservation_dimensions_are_explicit(self) -> None:
        for dimension in self.registry["preservation_dimensions"]:
            self.assertRegex(self.lean, rf"\b{re.escape(dimension)}\b")

    def test_all_rccd_components_are_explicit(self) -> None:
        for component in self.registry["rccd_component_fields"]:
            self.assertRegex(self.lean, rf"\b{re.escape(component)}\b")

    def test_unknown_and_failure_noninflation_theorems_exist(self) -> None:
        self.assertIn("unknown_semantic_dimension_not_all_pass", self.lean)
        self.assertIn("failed_operational_dimension_not_all_pass", self.lean)

    def test_registry_preserves_claim_boundary(self) -> None:
        self.assertEqual(self.registry["obligation"], "G1")
        self.assertEqual(self.registry["status"], "implemented_pending_validation")
        self.assertFalse(self.registry["claims"]["open_world_maximality"])
        self.assertFalse(self.registry["claims"]["metaphysical_universality"])
        self.assertFalse(self.registry["claims"]["inaccessible_reasoning_resolved"])
        self.assertTrue(self.registry["claims"]["single_kernel_semantic_composition"])

    def test_workflow_compiles_kernel_and_runs_alignment(self) -> None:
        self.assertIn("lean mechanization/lean/UPPSemanticKernel.lean", self.workflow)
        self.assertIn("python -m unittest tests.test_upp_semantic_kernel_alignment", self.workflow)


if __name__ == "__main__":
    unittest.main()
