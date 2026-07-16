from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization" / "lean" / "FARCore.lean"
DOC = ROOT / "mechanization" / "lean" / "T003-MECHANIZATION.md"
PROOF = ROOT / "theory" / "proof-objects" / "T-003.proof.yaml"


class T003LeanAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lean = LEAN.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.proof = yaml.safe_load(PROOF.read_text(encoding="utf-8"))

    def test_named_theorem_and_constructive_witness_exist(self):
        self.assertIn("theorem t003_representation_theorem", self.lean)
        self.assertIn("def constructFARRepresentation", self.lean)
        self.assertIn("Nonempty (FARRepresentation R)", self.lean)

    def test_six_components_are_encoded(self):
        structure = re.search(
            r"structure FARRepresentation.*?(?=\n/--|\nstructure T003Premises)",
            self.lean,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(structure)
        text = structure.group(0)
        for field in ("I :", "Rep :", "S :", "Int :", "C :", "T :"):
            self.assertIn(field, text)

    def test_scope_is_not_definitionally_true(self):
        self.assertNotIn("def InScope (_R : ReasoningProcess) : Prop := True", self.lean)
        self.assertIn("structure Scope", self.lean)
        self.assertIn("contains : ReasoningProcess → Prop", self.lean)

    def test_no_global_axiom_declarations_remain(self):
        declarations = [
            line.strip()
            for line in self.lean.splitlines()
            if line.strip().startswith("axiom ")
        ]
        self.assertEqual(declarations, [])

    def test_all_t003_axiom_sources_are_mapped(self):
        sources = {premise["source"] for premise in self.proof["premises"]}
        for axiom in ("A1", "A2", "A3", "A4", "A5"):
            self.assertIn(axiom, sources)
            self.assertIn(axiom, self.doc)

    def test_trace_is_constructed_without_extra_axiom(self):
        self.assertIn("def traceOf", self.lean)
        self.assertIn("R.specifiedTransitions", self.lean)
        self.assertIn("traceMatchesProcess", self.lean)

    def test_claim_boundary_is_documented(self):
        for phrase in (
            "does not independently prove those premises",
            "necessity, minimality, uniqueness",
            "whether a particular real-world process belongs",
        ):
            self.assertIn(phrase, self.doc)


if __name__ == "__main__":
    unittest.main()
