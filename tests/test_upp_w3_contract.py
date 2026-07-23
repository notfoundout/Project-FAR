import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'theory/contract/upp_faithfulness_contract_v1.py'
s=importlib.util.spec_from_file_location('upp_contract_test',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)

class ContractTests(unittest.TestCase):
    def assessments(self, verdict=m.Verdict.PASS):
        return tuple(m.ClauseAssessment(c, verdict, frozenset({'e'}) if verdict is m.Verdict.PASS else frozenset(), 'unresolved' if verdict is m.Verdict.UNKNOWN else '') for c in m.ClauseId)
    def test_all_pass(self): self.assertEqual(m.FaithfulnessAssessment(self.assessments()).verdict,m.Verdict.PASS)
    def test_one_fail_dominates(self):
        xs=list(self.assessments()); xs[0]=m.ClauseAssessment(xs[0].clause,m.Verdict.FAIL)
        self.assertEqual(m.FaithfulnessAssessment(tuple(xs)).verdict,m.Verdict.FAIL)
    def test_unknown_is_not_pass(self): self.assertEqual(m.FaithfulnessAssessment(self.assessments(m.Verdict.UNKNOWN)).verdict,m.Verdict.UNKNOWN)
    def test_pass_requires_evidence(self):
        with self.assertRaises(ValueError): m.ClauseAssessment(m.ClauseId.STRUCTURAL,m.Verdict.PASS).validate()
    def test_unknown_requires_reason(self):
        with self.assertRaises(ValueError): m.ClauseAssessment(m.ClauseId.STRUCTURAL,m.Verdict.UNKNOWN).validate()
    def test_duplicate_clause_rejected(self):
        xs=list(self.assessments()); xs[-1]=xs[0]
        with self.assertRaises(ValueError): m.FaithfulnessAssessment(tuple(xs)).validate()
    def test_missing_clause_rejected(self):
        with self.assertRaises(ValueError): m.FaithfulnessAssessment(self.assessments()[:-1]).validate()
    def test_conclusion_terms_rejected(self): self.assertFalse(m.text_is_conclusion_neutral('RCCD is required'))
    def test_neutral_text_allowed(self): self.assertTrue(m.text_is_conclusion_neutral('preserve registered questions'))

if __name__=='__main__': unittest.main()
