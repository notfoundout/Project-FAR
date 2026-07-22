from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w3-common-factor-v1.0.json'
class IKDW3CommonFactorTests(unittest.TestCase):
    def load(self): return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w3_common_factor.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_successful_input_set_is_preserved(self):
        self.assertEqual(self.load()['successful_architectures'],['FARA-001','LTS-PROV-001','COALG-DYN-001'])
    def test_generic_and_escape_hatch_factors_fail(self):
        factors={x['id']:x['classification'] for x in self.load()['tested_factor_candidates']}
        self.assertEqual(factors['CF-GRAPH'],'rejected_generic'); self.assertEqual(factors['CF-INTERPRETER'],'rejected_escape_hatch')
    def test_rccd_is_bounded_not_universal(self):
        result=self.load(); self.assertEqual(result['terminal_result'],'one_bounded_nontrivial_common_factor_candidate_supported')
        self.assertEqual(result['claim_effect']['universal_structure'],'unresolved')
        self.assertIn('RCCD-001 is globally universal',result['nonclaims'])
    def test_composition_is_next(self): self.assertEqual(self.load()['next_decisive_workstream'],'IKD-W4-CROSS-FEATURE-COMPOSITION')
if __name__=='__main__': unittest.main()
