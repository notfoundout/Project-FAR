import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-003"
SPEC = BASE / "preregistration.json"
REPORT = BASE / "README.md"

EXPECTED_CASES = {
    "CRE-003-I": "interpretation",
    "CRE-003-G": "investigation",
    "CRE-003-C": "reasoning_calculus",
    "CRE-003-R": "representation",
}
EXPECTED_DIMENSIONS = {
    "structural",
    "semantic",
    "operational",
    "dependency",
    "information",
    "historical",
}


class CRE003PreregistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = json.loads(SPEC.read_text(encoding="utf-8"))
        self.report = REPORT.read_text(encoding="utf-8")

    def test_protocol_was_frozen_before_mapping(self) -> None:
        self.assertEqual("CRE-003", self.spec["experiment_id"])
        self.assertEqual("frozen-before-mapping", self.spec["status"])
        self.assertIn("preregistration was merged before any candidate mappings or scores were added", self.report)
        self.assertIn("separate artifact", self.report)

    def test_all_four_discrimination_cases_are_registered_once(self) -> None:
        cases = self.spec["matched_cases"]
        observed = {case["case_id"]: case["variation"] for case in cases}
        self.assertEqual(EXPECTED_CASES, observed)
        self.assertEqual(4, len(cases))

    def test_each_case_freezes_changed_and_held_constant_commitments(self) -> None:
        for case in self.spec["matched_cases"]:
            self.assertTrue(case["changed"], msg=case["case_id"])
            self.assertTrue(case["held_constant"], msg=case["case_id"])
            self.assertTrue(case["required_discrimination"].strip(), msg=case["case_id"])
            self.assertTrue(set(case["changed"]).isdisjoint(case["held_constant"]), msg=case["case_id"])
            self.assertIn("system_a", case, msg=case["case_id"])
            self.assertIn("system_b", case, msg=case["case_id"])
            self.assertNotEqual(case["system_a"], case["system_b"], msg=case["case_id"])

    def test_preservation_and_complexity_rules_match_protocol(self) -> None:
        self.assertEqual(EXPECTED_DIMENSIONS, set(self.spec["dimensions"]))
        rules = self.spec["evaluation_rules"]
        self.assertEqual(3, rules["mapping_count_per_vocabulary"])
        self.assertFalse(rules["discard_divergent_mappings"])
        self.assertEqual(["A_used", "A_required", "D", "O", "L"], rules["complexity_metrics"])
        self.assertIn("Pareto", rules["comparison_rule"])

    def test_success_rules_separate_existential_and_reproducible_sufficiency(self) -> None:
        success = self.spec["success_conditions"]
        self.assertIn("at least one of three", success["existential_sufficiency"])
        self.assertIn("all three", success["reproducible_sufficiency"])
        self.assertIn("hidden reintroduction", success["merger_failure"])

    def test_report_prohibits_unbounded_claim_upgrade(self) -> None:
        required_boundaries = [
            "unrestricted primitive necessity",
            "global minimality",
            "unique optimality",
            "universal coverage of reasoning",
        ]
        for boundary in required_boundaries:
            self.assertIn(boundary, self.report)
        prohibited_affirmations = [
            "CRE-003 establishes global minimality",
            "CRE-003 proves universal coverage",
            "FAR is uniquely optimal",
        ]
        for claim in prohibited_affirmations:
            self.assertNotIn(claim, self.report)


if __name__ == "__main__":
    unittest.main()
