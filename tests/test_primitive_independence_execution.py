import csv
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
ATTEMPTS = ROOT / "theory" / "independence" / "executions" / "PIE-001" / "attempts.csv"
REPORT = ROOT / "theory" / "independence" / "executions" / "PIE-001" / "README.md"

PRIMITIVES = {
    "Investigation",
    "Representation",
    "Representational Structure",
    "Interpretation",
    "Reasoning Calculus",
}
TEST_TYPES = {"elimination", "derivability", "merger", "substitution", "recovery"}


class PrimitiveIndependenceExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        with ATTEMPTS.open(newline="", encoding="utf-8") as handle:
            self.rows = list(csv.DictReader(handle))

    def test_records_every_mandatory_attempt_exactly_once(self) -> None:
        observed = [(row["primitive"], row["test_type"]) for row in self.rows]
        expected = [(primitive, test) for primitive in PRIMITIVES for test in TEST_TYPES]
        self.assertEqual(25, len(observed))
        self.assertEqual(len(observed), len(set(observed)))
        self.assertEqual(set(expected), set(observed))

    def test_no_positive_independence_claim_is_recorded(self) -> None:
        self.assertTrue(all(row["decision"] == "unresolved" for row in self.rows))
        self.assertFalse(any(row["attempt_outcome"] == "reduction-succeeded" for row in self.rows))

    def test_completed_and_incomplete_attempt_counts_are_locked(self) -> None:
        failed = sum(row["attempt_outcome"] == "reduction-failed" for row in self.rows)
        incomplete = sum(row["attempt_outcome"] == "not-completed" for row in self.rows)
        self.assertEqual(15, failed)
        self.assertEqual(10, incomplete)

    def test_recovery_failures_record_hidden_reintroduction(self) -> None:
        recovery_rows = [row for row in self.rows if row["test_type"] == "recovery"]
        self.assertEqual(5, len(recovery_rows))
        self.assertTrue(all(row["hidden_reintroduction"] == "present" for row in recovery_rows))

    def test_report_preserves_claim_boundary(self) -> None:
        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("Scientific conclusion: unresolved", report)
        self.assertIn("does not establish local independence", report)
        self.assertNotIn("independence established", report.lower().replace('"independence established."', ''))


if __name__ == "__main__":
    unittest.main()
