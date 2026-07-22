from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w7-lower-bounds-v1.0.json'
class IKDW7LowerBoundTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w7_lower_bounds.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_scope_is_explicit(self):
        data=self.load(); self.assertEqual(data['universality_class']['id'],'C-EFFECTIVE-REASONING-001'); self.assertEqual(data['preservation_contract']['id'],'P-RCCD-FAITHFUL-001'); self.assertEqual(data['effective_representation_family']['id'],'E-EFFECTIVE-REP-001')
    def test_all_components_have_separation_bounds(self):
        bounds=self.load()['lower_bounds']; self.assertEqual(len(bounds),5)
        for bound in bounds:
            self.assertTrue(bound['paired_countermodel']); self.assertTrue(bound['indistinguishable_under_ablation']); self.assertTrue(bound['separating_query']); self.assertTrue(bound['theorem']); self.assertTrue(bound['classification'].startswith('conditionally_necessary'))
    def test_contract_is_not_rccd_by_definition(self):
        rule=self.load()['preservation_contract']['anti_circularity_rule']; self.assertIn('reasoning facts',rule); self.assertIn('not RCCD vocabulary',rule)
    def test_terminal_result_is_conditional_not_global(self):
        data=self.load(); self.assertEqual(data['terminal_result'],'all_five_rccd_components_have_conditional_lower_bounds_on_defined_class'); self.assertEqual(data['claim_effect']['global_necessity'],'not_supported'); self.assertEqual(data['claim_effect']['global_minimality'],'unresolved_pending_W8')
    def test_next_workstream_is_frontier(self):
        self.assertEqual(self.load()['next_decisive_workstream'],'IKD-W8-MINIMAL-FRONTIER')
if __name__=='__main__':unittest.main()
