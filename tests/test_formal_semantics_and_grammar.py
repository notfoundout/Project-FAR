from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class FormalGrammarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = load_module("parse_far_formal_tests", ROOT / "tools" / "parse_far.py")

    def write(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "case.far.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_checked_in_example_conforms(self):
        far = self.parser.load_far_yaml(ROOT / "examples" / "far" / "syllogism.far.yaml")
        self.assertEqual(far.validate_well_formed(), [])

    def test_rejects_unknown_top_level_key(self):
        path = self.write("investigation: x\nrepresentations:\n  - {id: r1, kind: claim, content: x}\nextra: true\n")
        with self.assertRaisesRegex(ValueError, "unknown keys"):
            self.parser.load_far_yaml(path)

    def test_rejects_empty_representations(self):
        path = self.write("investigation: x\nrepresentations: []\n")
        with self.assertRaisesRegex(ValueError, "representations must be nonempty"):
            self.parser.load_far_yaml(path)

    def test_rejects_noninteger_transition_order(self):
        path = self.write("""investigation: x
representations:
  - {id: r1, kind: claim, content: x}
rules:
  - {id: q1, inputs: [r1], output: r1}
transitions:
  - {id: t1, source: s0, rule: q1, target: s1, order: '1'}
""")
        with self.assertRaisesRegex(ValueError, "order must be an integer"):
            self.parser.load_far_yaml(path)

    def test_rejects_unknown_record_key(self):
        path = self.write("investigation: x\nrepresentations:\n  - {id: r1, kind: claim, content: x, typo: y}\n")
        with self.assertRaisesRegex(ValueError, "unknown keys"):
            self.parser.load_far_yaml(path)


class ProofStepSemanticsTests(unittest.TestCase):
    def test_every_checker_rule_is_documented(self):
        checker = load_module("proof_checker_formal_tests", ROOT / "tools" / "check_proof_object.py")
        semantics = (ROOT / "theory" / "semantics" / "proof-step-semantics.md").read_text(encoding="utf-8")
        for rule in checker.ALLOWED_RULES:
            self.assertIn(f"`{rule}`", semantics, f"missing normative semantics for {rule}")

    def test_formal_grammar_declares_parser_contract(self):
        grammar = (ROOT / "spec" / "far-yaml-grammar.md").read_text(encoding="utf-8")
        self.assertIn("tools/parse_far.py", grammar)
        self.assertIn("Unknown top-level keys are rejected", grammar)
        self.assertIn("Syntax does not assign meaning", grammar)


if __name__ == "__main__":
    unittest.main()
