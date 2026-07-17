import csv
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "independence" / "alternative-vocabularies" / "AVC-001"
VOCABULARIES = BASE / "vocabularies.json"
RESULTS = BASE / "results.csv"
REPORT = BASE / "README.md"

PRESERVATION = {
    "structural",
    "semantic",
    "operational",
    "dependency",
    "information",
    "historical",
}


class AlternativeVocabularyCompetitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(VOCABULARIES.read_text(encoding="utf-8"))
        with RESULTS.open(newline="", encoding="utf-8") as handle:
            self.rows = list(csv.DictReader(handle))

    def test_candidate_set_is_frozen_and_complete(self) -> None:
        self.assertEqual("frozen-before-evaluation", self.registry["status"])
        vocabularies = self.registry["vocabularies"]
        self.assertEqual(10, len(vocabularies))
        identifiers = [item["id"] for item in vocabularies]
        self.assertEqual(10, len(set(identifiers)))
        self.assertEqual({f"AV-{index:03d}" for index in range(1, 11)}, set(identifiers))

    def test_every_primitive_has_independent_semantics_and_identity_conditions(self) -> None:
        for vocabulary in self.registry["vocabularies"]:
            self.assertGreaterEqual(len(vocabulary["primitives"]), 3)
            for primitive in vocabulary["primitives"]:
                self.assertTrue(primitive["name"].strip())
                self.assertTrue(primitive["semantics"].strip())
                self.assertTrue(primitive["identity_conditions"].strip())

    def test_every_vocabulary_has_exactly_one_result(self) -> None:
        identifiers = {item["id"] for item in self.registry["vocabularies"]}
        observed = [row["vocabulary_id"] for row in self.rows]
        self.assertEqual(10, len(observed))
        self.assertEqual(10, len(set(observed)))
        self.assertEqual(identifiers, set(observed))

    def test_result_values_are_well_formed(self) -> None:
        judgments = {"Pass", "Partial", "Fail", "Unknown"}
        for row in self.rows:
            for dimension in PRESERVATION:
                self.assertIn(row[dimension], judgments)
            for metric in ("A_used", "A_required", "D", "O", "L"):
                self.assertGreaterEqual(int(row[metric]), 0)
            self.assertIn(row["hidden_reintroduction"], {"present", "absent", "unknown"})

    def test_far_is_control_but_not_declared_global_winner(self) -> None:
        far = next(row for row in self.rows if row["vocabulary_id"] == "AV-001")
        self.assertTrue(all(far[dimension] == "Pass" for dimension in PRESERVATION))
        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("Scientific conclusion: **inconclusive**", report)
        self.assertIn("FAR dominance: not established", report)
        self.assertIn("global minimality: not established", report)
        self.assertNotIn("Scientific conclusion: **FAR is globally minimal**", report)
        self.assertNotIn("FAR dominance: established", report)
        self.assertNotIn("global minimality: established", report)

    def test_serious_competitors_remain_unresolved(self) -> None:
        unresolved = {
            row["vocabulary_id"]
            for row in self.rows
            if row["decision"] == "unresolved"
        }
        self.assertTrue({"AV-004", "AV-005", "AV-006", "AV-009", "AV-010"}.issubset(unresolved))


if __name__ == "__main__":
    unittest.main()
