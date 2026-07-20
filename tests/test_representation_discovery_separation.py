from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class RepresentationDiscoverySeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = load("theory/evaluation/generic-relational-baseline-v1.0.json")
        cls.scope = load("theory/evaluation/reasoning-and-contrast-scope-v1.0.json")
        cls.target = load("theory/evaluation/universal-structure-discovery-target-v1.0.json")
        cls.w35 = load("theory/evaluation/w3-5-specificity-and-discovery-gate.json")
        cls.candidates = load("theory/evaluation/universal-structure-candidate-registry.json")
        cls.gates = load("theory/evaluation/research-gates.json")
        cls.claims = load("theory/evaluation/central-claim-registry.json")
        cls.rep_target = load("theory/evaluation/thm-target-001.json")

    def test_generic_baseline_is_reasoning_neutral(self) -> None:
        self.assertEqual(self.baseline["baseline_id"], "GREL-001")
        self.assertEqual(self.baseline["reasoning_specific_primitives"], [])

    def test_generic_baseline_has_no_result_yet(self) -> None:
        self.assertEqual(self.baseline["current_result"], "unresolved")

    def test_positive_scope_is_independent_of_fara(self) -> None:
        self.assertTrue(self.scope["admission_rules"]["positive_independent_of_fara"])

    def test_contrast_scope_is_not_selected_by_failure(self) -> None:
        self.assertTrue(self.scope["admission_rules"]["contrast_independent_of_fara_failure"])

    def test_universal_target_is_separate(self) -> None:
        self.assertEqual(self.target["target_id"], "THM-US-TARGET-001")
        self.assertEqual(self.target["representation_track_implication"], "none")

    def test_no_universal_theorem_is_preproved(self) -> None:
        self.assertTrue(all(item["status"] != "proved" for item in self.target["theorem_families"]))

    def test_w35_is_between_w3_and_w5(self) -> None:
        self.assertEqual(self.w35["position"], "after_W3_before_W5")
        self.assertFalse(self.w35["w5_authorized"])

    def test_w4_remains_parallel(self) -> None:
        self.assertTrue(self.w35["W4_parallel_execution_allowed"])

    def test_candidates_are_not_prejudged(self) -> None:
        self.assertTrue(all(item["current_classification"] == "unresolved" for item in self.candidates["candidates"]))

    def test_representation_target_is_rep_track(self) -> None:
        self.assertEqual(self.rep_target["program_track"], "REP")
        self.assertIn("universal_structure", self.rep_target["does_not_imply"])

    def test_w5_requires_w4_and_w35(self) -> None:
        blockers = set(self.rep_target["w5_authorization"]["blocked_by"])
        self.assertIn("OBS-SC-010", blockers)
        self.assertIn("W3.5-SDG-001", blockers)

    def test_research_gates_separate_freeze_from_results(self) -> None:
        by_name = {item["name"]: item for item in self.gates["gates"]}
        self.assertEqual(by_name["generic-baseline-frozen"]["status"], "satisfied")
        self.assertEqual(by_name["baseline-factorization-resolved"]["status"], "not_satisfied")

    def test_rep_capacity_does_not_imply_universal_structure(self) -> None:
        by_id = {item["id"]: item for item in self.claims["claims"]}
        self.assertIn("CLM-UNIVERSAL-STRUCTURE", by_id["CLM-REP-CAPACITY"]["does_not_imply"])

    def test_universal_structure_status_is_unresolved(self) -> None:
        by_id = {item["id"]: item for item in self.claims["claims"]}
        self.assertEqual(by_id["CLM-UNIVERSAL-STRUCTURE"]["current_status"], "unresolved")

    def test_makefile_runs_separation_checker_three_times(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertEqual(text.count("python tools/check_representation_discovery_separation.py"), 3)


if __name__ == "__main__":
    unittest.main()
