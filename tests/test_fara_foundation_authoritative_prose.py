import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import check_fara_foundation_comparison as checker


class AuthoritativeProseValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof = json.loads(checker.PROOF.read_text())

    @staticmethod
    def mutate_outside_snapshot(text, mutation):
        start = checker._SNAPSHOT_START
        end = checker._SNAPSHOT_END
        prefix, remainder = text.split(start, 1)
        snapshot, suffix = remainder.split(end, 1)
        return mutation(prefix) + start + snapshot + end + mutation(suffix)

    def test_all_authoritative_claim_bearing_prose_matches_proof(self):
        for record in checker.AUTHORITATIVE_RECORDS:
            with self.subTest(record=record.relative_to(ROOT)):
                self.assertTrue(checker.validate_authoritative_text(record.read_text(), self.proof))

    def test_reversed_dominance_prose_is_rejected_with_snapshot_unchanged(self):
        replacements = (
            ("`many-sorted-relational` → `algebraic-state-transition`", "`algebraic-state-transition` → `many-sorted-relational`"),
            ("Many-sorted relational dominates algebraic/state-transition", "Algebraic/state-transition dominates many-sorted relational"),
            ("many-sorted relational → algebraic/state-transition", "algebraic/state-transition → many-sorted relational"),
        )
        snapshot = checker.authoritative_snapshot(self.proof)
        for record in checker.AUTHORITATIVE_RECORDS:
            original = record.read_text()

            def reverse(text):
                for old, new in replacements:
                    if old in text:
                        return text.replace(old, new, 1)
                return text

            changed = self.mutate_outside_snapshot(original, reverse)
            with self.subTest(record=record.relative_to(ROOT)):
                self.assertNotEqual(original, changed)
                self.assertEqual(1, changed.count(snapshot))
                self.assertFalse(checker.validate_authoritative_text(changed, self.proof))

    def test_incomparability_prose_mutation_is_rejected(self):
        for record in checker.AUTHORITATIVE_RECORDS:
            original = record.read_text()
            changed = self.mutate_outside_snapshot(
                original,
                lambda text: text.replace("incomparable", "equivalent"),
            )
            with self.subTest(record=record.relative_to(ROOT)):
                self.assertNotEqual(original, changed)
                self.assertFalse(checker.validate_authoritative_text(changed, self.proof))

    def test_stale_no_edge_claim_is_rejected_even_with_exact_snapshot(self):
        for record in checker.AUTHORITATIVE_RECORDS:
            changed = record.read_text() + "\nThe dominance graph has no edges.\n"
            with self.subTest(record=record.relative_to(ROOT)):
                self.assertFalse(checker.validate_authoritative_text(changed, self.proof))


if __name__ == "__main__":
    unittest.main()
