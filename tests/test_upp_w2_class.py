from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "theory/class/upp_target_class_v1.py"


def load_model():
    spec = importlib.util.spec_from_file_location("upp_target_class_v1", MODEL)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class UPPW2ClassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = load_model()

    def evidence(self, **overrides):
        values = dict(
            has_alternative_options=True,
            options_can_be_appraised=True,
            appraisal_can_change_permitted_response=True,
            relevant_facts_are_finitely_specifiable=True,
            assessment_is_repeatable_in_principle=True,
            evidence_is_accessible=True,
        )
        values.update(overrides)
        return self.m.ClassEvidence(**values)

    def test_checker(self):
        cp = subprocess.run([sys.executable, str(ROOT / "tools/check_upp_w2_class.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_all_criteria_yield_in_scope(self):
        self.assertEqual(self.m.classify(self.evidence()).status, self.m.AssessmentStatus.IN_SCOPE)

    def test_each_failed_criterion_excludes(self):
        fields = [
            "has_alternative_options", "options_can_be_appraised",
            "appraisal_can_change_permitted_response",
            "relevant_facts_are_finitely_specifiable",
            "assessment_is_repeatable_in_principle",
        ]
        for field in fields:
            with self.subTest(field=field):
                self.assertEqual(self.m.classify(self.evidence(**{field: False})).status, self.m.AssessmentStatus.OUT_OF_SCOPE)

    def test_inaccessible_evidence_is_unknown(self):
        decision = self.m.classify(self.evidence(evidence_is_accessible=False))
        self.assertEqual(decision.status, self.m.AssessmentStatus.UNKNOWN)
        self.assertEqual(decision.unknown_criteria, self.m.CRITERIA)

    def test_rccd_terms_are_rejected(self):
        for term in self.m.FORBIDDEN_RCCD_TERMS:
            with self.subTest(term=term):
                self.assertFalse(self.m.criterion_text_is_rccd_independent(f"criterion requires {term}"))

    def test_neutral_text_is_accepted(self):
        self.assertTrue(self.m.criterion_text_is_rccd_independent("alternatives admit appraisal under an explicit standard"))


if __name__ == "__main__":
    unittest.main()
