from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w3-contract-ladder-v1.0.json'
class SCW3ContractLadderTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_sc_w3_contract_ladder.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_full_contract_requires_all_components(self):
        data=self.load(); self.assertEqual(data['contract_ladder'][-1]['required_rccd'],['R1','R2','R3','R4','R5'])
    def test_weakest_contract_is_generic_only(self):
        first=self.load()['contract_ladder'][0]; self.assertEqual(first['required_rccd'],[]); self.assertEqual(first['classification'],'generic_only_commonality_at_this_contract')
    def test_each_component_drops_with_its_duty(self):
        data=self.load(); self.assertEqual({x['component_no_longer_forced'] for x in data['single_duty_ablations']},{'R1','R2','R3','R4','R5'})
    def test_result_is_contract_relative_not_construct_loaded(self):
        data=self.load(); self.assertEqual(data['terminal_result'],'rccd_is_contract_relative_but_not_shown_construct_loaded_under_independently_justified_full_contract'); self.assertIn('No P4 duty is justified merely by naming an RCCD component',data['neutrality_findings'])
    def test_final_answer_not_claimed(self):
        self.assertIn('the final internal answer has been issued',self.load()['nonclaims'])
if __name__=='__main__':unittest.main()
