from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w2-boundary-reasoning-v1.0.json'
class SCW2BoundaryReasoningTests(unittest.TestCase):
    def load(self): return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_sc_w2_boundary_reasoning.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_membership_is_not_rccd_defined(self):
        d=self.load(); self.assertIn('normatively assessable',d['membership_rule']); self.assertNotIn('R1-R5',d['membership_rule'])
    def test_opaque_cases_are_not_forced_positive(self):
        d=self.load(); opaque=[c for c in d['cases'] if c['id']=='BR-05'][0]; self.assertEqual(opaque['classification'],'unassessable_not_disproved'); self.assertIsNone(opaque['primitive_extension'])
    def test_no_demonstrated_boundary_counterexample(self):
        c=self.load()['counterexample_search']; self.assertFalse(c['genuine_new_primitive_found']); self.assertFalse(c['rccd_component_evaded_by_assessable_faithful_case'])
    def test_claim_remains_provisional(self):
        d=self.load(); self.assertIn('final internal answer established',d['nonclaims']); self.assertEqual(d['next_decisive_workstream'],'SC-W3-CONTRACT-LADDER')
if __name__=='__main__': unittest.main()
