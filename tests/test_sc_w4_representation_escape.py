from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w4-representation-escape-v1.0.json'
class SCW4RepresentationEscapeTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_sc_w4_representation_escape.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_broad_family_coverage_is_registered(self):
        data=self.load(); self.assertEqual(len(data['representation_families']),12); self.assertEqual(len(data['escape_attempts']),12)
    def test_no_registered_effective_family_escapes(self):
        self.assertTrue(all(x['result']!='escape' for x in self.load()['representation_families']))
    def test_hidden_machinery_is_charged(self):
        ledger=self.load()['hidden_machinery_ledger']; self.assertIn('source-specific codebooks',ledger); self.assertIn('schedulers and policy guards',ledger); self.assertIn('learned or hand-built decoders',ledger)
    def test_opaque_cases_remain_unresolved(self):
        unresolved=' '.join(self.load()['unresolved']); self.assertIn('opaque learned systems',unresolved)
    def test_final_answer_not_claimed(self):
        self.assertIn('the final internal answer has been issued',self.load()['nonclaims'])
if __name__=='__main__':unittest.main()
