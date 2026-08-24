import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fara_w1", ROOT / "tools/check_fara_primitive_independence.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class FaraPrimitiveIndependenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(checker.DATA.read_text())

    def test_canonical_result_validates(self):
        checker.validate(self.data)

    def test_historical_coverage_and_fail_closed_outcomes(self):
        self.assertEqual([r["primitive"] for r in self.data["results"]], checker.EXPECTED)
        self.assertEqual({r["classification"] for r in self.data["results"]}, {"unresolved"})

    def test_terminal_reclassification_is_explicit(self):
        generated = checker.render(self.data)
        self.assertIn("PROJECT-FAR-CORE-THEORY-1.0", generated)
        self.assertIn("schema or contract roles", generated)
        self.assertIn("global primitive-independence/minimality search is closed", generated)
        self.assertNotIn("remains only a candidate primitive", generated)

    def test_missing_primitive_rejected(self):
        bad = copy.deepcopy(self.data); bad["results"].pop()
        with self.assertRaisesRegex(ValueError, "cover each primitive"):
            checker.validate(bad)

    def test_unsupported_positive_result_rejected(self):
        bad = copy.deepcopy(self.data); bad["results"][0]["classification"] = "independent"
        with self.assertRaisesRegex(ValueError, "separately registered formal proof"):
            checker.validate(bad)

    def test_hidden_assumption_rejected(self):
        bad = copy.deepcopy(self.data); bad["results"][1]["assumptions_used"] = ["Properties are unary relations"]
        with self.assertRaisesRegex(ValueError, "silently introduces assumptions"):
            checker.validate(bad)

    def test_downstream_proof_leakage_rejected(self):
        bad = copy.deepcopy(self.data); bad["results"][2]["attempt"] += " frameworks/FARO/operator.md"
        with self.assertRaisesRegex(ValueError, "downstream FAR/FARO"):
            checker.validate(bad)

    def test_generated_artifact_is_current(self):
        output = ROOT / self.data["generated_artifact"]
        self.assertEqual(output.read_text(), checker.render(self.data))


if __name__ == "__main__":
    unittest.main()
