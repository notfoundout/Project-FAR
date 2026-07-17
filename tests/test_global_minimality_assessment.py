import csv
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "independence" / "global-minimality" / "GMA-001"
SEARCH_SPACE = BASE / "search-space.json"
REPORT = BASE / "README.md"
AVC_RESULTS = ROOT / "theory" / "independence" / "alternative-vocabularies" / "AVC-001" / "results.csv"
PIE_ATTEMPTS = ROOT / "theory" / "independence" / "executions" / "PIE-001" / "attempts.csv"


class GlobalMinimalityAssessmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.search_space = json.loads(SEARCH_SPACE.read_text(encoding="utf-8"))
        self.report = REPORT.read_text(encoding="utf-8")
        with AVC_RESULTS.open(newline="", encoding="utf-8") as handle:
            self.avc_rows = list(csv.DictReader(handle))
        with PIE_ATTEMPTS.open(newline="", encoding="utf-8") as handle:
            self.pie_rows = list(csv.DictReader(handle))

    def test_search_space_is_explicitly_bounded(self) -> None:
        self.assertEqual("closed-bounded-search-space", self.search_space["status"])
        self.assertEqual(["CRE-001-REFERENCE-V1"], self.search_space["benchmark_ids"])
        self.assertEqual({"minimum": 3, "maximum": 5}, self.search_space["primitive_count_range_tested"])
        self.assertGreaterEqual(len(self.search_space["excluded_spaces"]), 5)

    def test_assessment_uses_completed_evidence_without_upgrading_it(self) -> None:
        self.assertEqual(25, len(self.pie_rows))
        self.assertEqual(10, len(self.avc_rows))
        self.assertFalse(any(row["attempt_outcome"] == "reduction-succeeded" for row in self.pie_rows))
        self.assertFalse(any(row["comparison_to_far"] == "dominates-far" for row in self.avc_rows))

    def test_unresolved_lower_cost_competitors_are_retained(self) -> None:
        unresolved_lower_cost = {
            row["vocabulary_id"]
            for row in self.avc_rows
            if int(row["A_used"]) < 5 and row["decision"] == "unresolved"
        }
        self.assertEqual({"AV-004", "AV-005", "AV-006", "AV-009", "AV-010"}, unresolved_lower_cost)

    def test_claim_boundary_is_exact(self) -> None:
        self.assertIn("Scientific conclusion: **global minimality unresolved**", self.report)
        self.assertIn("FAR global minimality: **not established**", self.report)
        self.assertIn("FAR global minimality falsified: **no**", self.report)
        prohibited_affirmative_claims = (
            "Scientific conclusion: **global minimality established**",
            "FAR global minimality: **established**",
            "FAR is globally minimal.",
        )
        for claim in prohibited_affirmative_claims:
            self.assertNotIn(claim, self.report, msg=f"prohibited affirmative claim present: {claim}")

    def test_primitive_count_bound_is_not_rewritten_as_necessity(self) -> None:
        self.assertIn("at most five and may be as low as three", self.report)
        self.assertIn("not a theorem that three primitives are sufficient or that five are necessary", self.report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
