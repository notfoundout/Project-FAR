"""The FAR-CORE v1.1 placeholder scan sees every placeholder in Lean code and none in prose or data.

Each "hidden" case compiled under Lean 4.19.0 (with only a `declaration uses 'sorry'` warning where
a placeholder is involved) while an earlier scanner counted nothing: a string holding `/-` opened a
fake comment, a character literal `'"'` opened a fake string, a raw string's backslash was read as
an escape, and `sorryAx` or `_root_.sorryAx` did not match `\\bsorry\\b`.
"""
from __future__ import annotations

import unittest

from tools import check_far_core_v11_formalization as checker

SORRY = "theorem t : False := by sorry\n"


def count(text: str) -> int:
    return len(checker.FORBIDDEN.findall(checker.lean_code(text)))


class LeanPlaceholderScanTests(unittest.TestCase):
    def test_placeholders_in_code_are_counted(self) -> None:
        cases = {
            "tactic": SORRY,
            "admit": "theorem t : False := by admit\n",
            "native_decide": "theorem t : 1 + 1 = 2 := by native_decide\n",
            "sorryAx term": "theorem t : False := sorryAx False false\n",
            "qualified sorryAx": "theorem t : False := _root_.sorryAx False false\n",
            "interpolated string code": 'def s : String := s!"{(sorry : Nat)}"\n',
            "unterminated comment": "/- never closed\n" + SORRY,
        }
        for name, text in cases.items():
            with self.subTest(name):
                self.assertGreaterEqual(count(text), 1)

    def test_literals_cannot_hide_later_code(self) -> None:
        cases = {
            "string holding a comment opener": 'def s : String := "/-"\n',
            "string holding a line comment": 'def s : String := "--"\n',
            "character literal quote": "def q : Char := '\"'\n",
            "raw string ending in backslash": 'def r : String := r"\\"\n',
            "raw string with hashes": 'def r : String := r#"a"b /-"#\n',
            "escaped quote": 'def s : String := "a\\"/-"\n',
        }
        for name, prefix in cases.items():
            with self.subTest(name):
                self.assertEqual(count(prefix + SORRY + 'def z : String := "x"\n'), 1)

    def test_trust_escaping_declarations_are_counted(self) -> None:
        for text in ("axiom a : False\n", "@[simp] axiom a : False\n", "private axiom a : False\n",
                     "noncomputable constant c : Nat\n", "unsafe def f : Nat := 0\n",
                     "@[implemented_by g] def f : Nat := 0\n", "@[extern \"c_f\"] def f : Nat := 0\n"):
            with self.subTest(text):
                self.assertGreaterEqual(count(text), 1)

    def test_prose_data_and_identifiers_are_not_counted(self) -> None:
        for text in ("-- by sorry\n", "/- sorry -/\n", "/- outer /- inner -/ sorry -/\n", "/-- uses sorry? no -/\n",
                     '/-! module doc: admit -/\n', 'def s : String := "sorry"\n', 'def r : String := r#"sorry"#\n',
                     "def c : Char := 's'\n", "theorem sorry_free (h' : True) : True := h'\n",
                     "def admitted : Nat := 0\n", "theorem t : True := by\n  -- native_decide\n  trivial\n"):
            with self.subTest(text):
                self.assertEqual(count(text), 0)

    def test_comment_removal_keeps_line_structure(self) -> None:
        text = "/- a\nb -/\ndef x := 1\n"
        self.assertEqual(checker.lean_code(text).count("\n"), text.count("\n"))


if __name__ == "__main__":
    unittest.main()
