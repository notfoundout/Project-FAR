from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_representation_discovery_separation import authorization_errors  # noqa: E402


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
        cls.ledger = load("theory/evaluation/s-core-construction-obstruction-ledger.json")

    def test_generic_baseline_is_reasoning_neutral(self) -> None:
        self.assertEqual(self.baseline["baseline_id"], "GREL-001")
        self.assertEqual(self.baseline["reasoning_specific_primitives"], [])

    def test_factorization_is_dimensioned(self) -> None:
        expected = {"expressiveness", "translation", "constraint_strength", "reasoning_specificity", "cost_relation", "overall_interpretation"}
        self.assertEqual(set(self.baseline["result_dimensions"]), expected)
        self.assertEqual(set(self.baseline["current_result"]), expected)
        self.assertTrue(self.baseline["single_scalar_classification_prohibited"])

    def test_generic_baseline_has_no_result_yet(self) -> None:
        self.assertTrue(all(value == "unresolved" for value in self.baseline["current_result"].values()))

    def test_positive_scope_is_independent_of_fara(self) -> None:
        self.assertTrue(self.scope["admission_rules"]["positive_independent_of_fara"])

    def test_contrast_scope_is_not_selected_by_failure(self) -> None:
        self.assertTrue(self.scope["admission_rules"]["contrast_independent_of_fara_failure"])

    def test_scope_framework_is_frozen_but_corpus_is_not(self) -> None:
        self.assertTrue(self.scope["framework_frozen"])
        self.assertEqual(self.scope["concrete_corpus_status"], "not_frozen")
        self.assertEqual(self.scope["positive_instances"], [])
        self.assertEqual(self.scope["contrast_instances"], [])
        self.assertEqual(self.scope["execution_status"], "blocked_until_concrete_corpus_frozen")

    def test_universal_target_is_separate(self) -> None:
        self.assertEqual(self.target["target_id"], "THM-US-TARGET-001")
        self.assertEqual(self.target["representation_track_implication"], "none")

    def test_no_universal_theorem_is_preproved(self) -> None:
        self.assertTrue(all(item["status"] != "proved" for item in self.target["theorem_families"]))

    def test_w35_is_between_w3_and_w5(self) -> None:
        self.assertEqual(self.w35["position"], "after_W3_before_W5")
        self.assertFalse(self.w35["w5_authorized"])

    def test_w4_completion_does_not_resolve_w35(self) -> None:
        by_id = {item["id"]: item for item in self.ledger["obligations"]}
        self.assertEqual(by_id["OBS-SC-010"]["status"], "obstruction_established")
        self.assertEqual(self.w35["status"], "frozen_not_executed")

    def test_w35_registers_immutable_evidence_fields(self) -> None:
        self.assertGreaterEqual(len(self.w35["required_result_artifacts"]), 8)
        for artifact in self.w35["required_result_artifacts"]:
            self.assertEqual(artifact["status"], "missing")
            self.assertIn("path", artifact)
            self.assertIn("artifact_id", artifact)
            self.assertIn("content_sha256", artifact)

    def test_candidates_are_not_prejudged(self) -> None:
        self.assertTrue(all(item["current_classification"] == "unresolved" for item in self.candidates["candidates"]))

    def test_representation_target_is_rep_track(self) -> None:
        self.assertEqual(self.rep_target["program_track"], "REP")
        self.assertIn("universal_structure", self.rep_target["does_not_imply"])

    def test_w5_now_requires_only_w35(self) -> None:
        self.assertEqual(self.rep_target["w5_authorization"]["blocked_by"], ["W3.5-SDG-001"])
        self.assertEqual(self.rep_target["w5_authorization"]["resolved_dependencies"], ["OBS-SC-010"])

    def test_rep_theorems_are_blocked_by_specificity_bridge(self) -> None:
        by_id = {item["id"]: item for item in self.rep_target["theorem_family"]}
        for theorem_id in ("THM-CORE-COMMON-001", "THM-CORE-REP-001", "THM-IMP-001"):
            self.assertIn("specificity_discovery_bridge", by_id[theorem_id]["blocked_by"])
            self.assertNotIn("formal_negative_controls", by_id[theorem_id]["blocked_by"])

    def test_research_gates_separate_framework_corpus_and_results(self) -> None:
        by_name = {item["name"]: item for item in self.gates["gates"]}
        self.assertEqual(by_name["generic-baseline-frozen"]["status"], "satisfied")
        self.assertEqual(by_name["reasoning-contrast-scope-framework-frozen"]["status"], "satisfied")
        self.assertEqual(by_name["reasoning-contrast-corpus-frozen"]["status"], "not_satisfied")
        self.assertEqual(by_name["baseline-factorization-resolved"]["status"], "not_satisfied")
        self.assertEqual(by_name["formal-negative-controls"]["status"], "satisfied")
        self.assertNotIn("reasoning-contrast-scope-frozen", by_name)

    def test_rep_capacity_does_not_imply_universal_structure(self) -> None:
        by_id = {item["id"]: item for item in self.claims["claims"]}
        self.assertIn("CLM-UNIVERSAL-STRUCTURE", by_id["CLM-REP-CAPACITY"]["does_not_imply"])

    def test_universal_structure_status_is_unresolved(self) -> None:
        by_id = {item["id"]: item for item in self.claims["claims"]}
        self.assertEqual(by_id["CLM-UNIVERSAL-STRUCTURE"]["current_status"], "unresolved")

    def test_current_unauthorized_state_is_valid(self) -> None:
        self.assertEqual(authorization_errors(self.w35, self.rep_target, self.scope, self.gates, self.ledger, ROOT), [])

    def test_status_only_authorization_is_rejected(self) -> None:
        w35 = copy.deepcopy(self.w35)
        target = copy.deepcopy(self.rep_target)
        w35["w5_authorized"] = True
        w35["status"] = "resolved"
        target["w5_authorization"]["authorized"] = True
        target["w5_authorization"]["blocked_by"] = []
        errors = authorization_errors(w35, target, self.scope, self.gates, self.ledger, ROOT)
        joined = "\n".join(errors)
        self.assertNotIn("OBS-SC-010 must have a terminal", joined)
        self.assertIn("concrete reasoning and contrast corpus", joined)
        self.assertIn("is not complete", joined)
        self.assertIn("factorization dimension", joined)

    def test_makefile_runs_separation_checker_three_times(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertEqual(text.count("python tools/check_representation_discovery_separation.py"), 3)


if __name__ == "__main__":
    unittest.main()
