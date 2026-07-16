from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization/lean/FARCore.lean"
AUDIT = ROOT / "mechanization/lean/T003-ADEQUACY-AUDIT.md"


class T003AdequacyAuditTests(unittest.TestCase):
    def test_required_formal_results_exist(self):
        text = LEAN.read_text(encoding="utf-8")
        required = [
            "structure ProcessSpecification",
            "def StructuralPreservation",
            "def SemanticPreservation",
            "def OperationalPreservation",
            "def TracePreservation",
            "def FaithfulRepresentation",
            "theorem canonical_representation_is_faithful",
            "theorem unconditional_structural_existence",
            "theorem t003_existence_is_not_assumption_minimal",
            "theorem modus_ponens_instance_is_faithful",
            "theorem triage_instance_is_faithful",
            "theorem legal_instance_is_faithful",
            "theorem corrupted_mp_fails_structural_preservation",
            "theorem corrupted_mp_fails_semantic_preservation",
            "theorem corrupted_mp_fails_operational_preservation",
            "theorem structural_existence_does_not_imply_faithfulness",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_audit_states_the_limit_honestly(self):
        text = AUDIT.read_text(encoding="utf-8").lower()
        self.assertIn("a1-a5 are not necessary for bare structural existence", text)
        self.assertIn("does **not** prove model-theoretic independence", text)
        self.assertIn("bare tuple inhabitation does not imply faithful representation", text)
        self.assertIn("three examples", text)
        self.assertIn("do not establish universal scope", text)

    def test_no_new_axioms_or_admissions(self):
        text = LEAN.read_text(encoding="utf-8")
        forbidden = ["axiom ", "sorry", "admit"]
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
