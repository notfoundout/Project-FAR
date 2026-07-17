import csv
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-003"
RESULTS = BASE / "results.csv"
REPORT = BASE / "execution.md"
DIMENSIONS = (
    "structural",
    "semantic",
    "operational",
    "dependency",
    "information",
    "historical",
)


class CRE003ExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        with RESULTS.open(newline="", encoding="utf-8") as handle:
            self.rows = list(csv.DictReader(handle))
        self.report = REPORT.read_text(encoding="utf-8")

    def test_all_ten_vocabularies_retain_three_mappings(self) -> None:
        self.assertEqual(30, len(self.rows))
        for index in range(1, 11):
            vocabulary_id = f"AV-{index:03d}"
            mappings = {
                row["mapping_id"]
                for row in self.rows
                if row["vocabulary_id"] == vocabulary_id
            }
            self.assertEqual({"M1", "M2", "M3"}, mappings, vocabulary_id)

    def test_values_and_complexity_are_well_formed(self) -> None:
        judgments = {"Pass", "Partial", "Fail", "Unknown"}
        for row in self.rows:
            for dimension in DIMENSIONS:
                self.assertIn(row[dimension], judgments, (row["vocabulary_id"], row["mapping_id"], dimension))
            for metric in ("A_used", "A_required", "D", "O", "L"):
                self.assertGreaterEqual(int(row[metric]), 0, (row["vocabulary_id"], row["mapping_id"], metric))
            self.assertIn(row["hidden_reintroduction"], {"present", "absent", "unknown"})
            self.assertIn(row["all_cases_all_pass"], {"yes", "no"})

    def test_far_has_existential_and_reproducible_internal_sufficiency(self) -> None:
        far = [row for row in self.rows if row["vocabulary_id"] == "AV-001"]
        self.assertEqual(3, len(far))
        self.assertTrue(all(row["all_cases_all_pass"] == "yes" for row in far))
        self.assertTrue(all(all(row[d] == "Pass" for d in DIMENSIONS) for row in far))

    def test_no_competing_mapping_is_all_pass(self) -> None:
        competitors = [row for row in self.rows if row["vocabulary_id"] != "AV-001"]
        self.assertTrue(all(row["all_cases_all_pass"] == "no" for row in competitors))

    def test_merger_failures_record_hidden_reintroduction(self) -> None:
        for vocabulary_id in ("AV-002", "AV-003"):
            rows = [row for row in self.rows if row["vocabulary_id"] == vocabulary_id]
            self.assertEqual(3, len(rows))
            self.assertTrue(all(row["hidden_reintroduction"] == "present" for row in rows))

    def test_unresolved_competitors_are_not_declared_defeated(self) -> None:
        for vocabulary_id in ("AV-004", "AV-005", "AV-006", "AV-009", "AV-010"):
            self.assertIn(vocabulary_id, self.report)
        self.assertIn("remain unresolved rather than defeated", self.report)

    def test_claim_boundary_blocks_evidence_upgrade(self) -> None:
        required = (
            "global minimality: not established",
            "universality: not established",
            "FAR dominance over the unrestricted vocabulary space: not established",
        )
        for statement in required:
            self.assertIn(statement, self.report)
        prohibited = (
            "Scientific conclusion: **FAR is globally minimal**",
            "global minimality: established",
            "universality: established",
        )
        for statement in prohibited:
            self.assertNotIn(statement, self.report)


if __name__ == "__main__":
    unittest.main()
