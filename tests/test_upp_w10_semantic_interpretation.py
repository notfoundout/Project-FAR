import importlib.util
import sys
import unittest
from pathlib import Path

P = Path(__file__).parents[1] / "theory/foundation/upp_semantic_interpretation_v1.py"
spec = importlib.util.spec_from_file_location("upp_semantic_interpretation_v1", P)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def yes_assessment(**changes):
    i = mod.Interpretation("i1", "c1", "p", mod.SemanticRole.ASSERTION, "tc", *([mod.Truth.YES] * 6))
    data = dict(target_class_member=mod.Truth.YES, representation_admissible=mod.Truth.YES,
                machinery_closed=mod.Truth.YES, fully_faithful=mod.Truth.YES,
                equivalence_preserved=mod.Truth.YES, registered_query_total=mod.Truth.YES,
                failure_unknown_separated=mod.Truth.YES, interpretations=(i,))
    data.update(changes)
    return mod.SemanticAssessment(**data)


class TestSemanticInterpretation(unittest.TestCase):
    def test_valid_witness(self): self.assertEqual(mod.assess_semantic_interpretation(yes_assessment()), mod.Verdict.PROVED)
    def test_missing_interpretation_unknown(self): self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=())), mod.Verdict.UNKNOWN)
    def test_failed_premise_refuted(self): self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(fully_faithful=mod.Truth.NO)), mod.Verdict.REFUTED)
    def test_unknown_premise_unknown(self): self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(machinery_closed=mod.Truth.UNKNOWN)), mod.Verdict.UNKNOWN)
    def test_context_failure_refuted(self):
        i = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "tc", mod.Truth.YES, mod.Truth.NO, *([mod.Truth.YES] * 4))
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(i,))), mod.Verdict.REFUTED)
    def test_unknown_meaning_unknown(self):
        i = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "tc", mod.Truth.UNKNOWN, *([mod.Truth.YES] * 5))
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(i,))), mod.Verdict.UNKNOWN)
    def test_hidden_interpreter_refuted(self):
        i = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "tc", *([mod.Truth.YES] * 5), mod.Truth.NO)
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(i,))), mod.Verdict.REFUTED)
    def test_empty_truth_conditions_refuted(self):
        i = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "", *([mod.Truth.YES] * 6))
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(i,))), mod.Verdict.REFUTED)
    def test_inconsistent_function_refuted(self):
        a = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "tc", *([mod.Truth.YES] * 6))
        b = mod.Interpretation("i", "c", "q", mod.SemanticRole.DENIAL, "tc2", *([mod.Truth.YES] * 6))
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(a,b))), mod.Verdict.REFUTED)
    def test_equivalence_instability_refuted(self):
        i = mod.Interpretation("i", "c", "p", mod.SemanticRole.ASSERTION, "tc", *([mod.Truth.YES] * 4), mod.Truth.NO, mod.Truth.YES)
        self.assertEqual(mod.assess_semantic_interpretation(yes_assessment(interpretations=(i,))), mod.Verdict.REFUTED)


if __name__ == "__main__": unittest.main()
