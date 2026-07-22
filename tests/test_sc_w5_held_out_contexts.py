from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'theory/evaluation/sc-w5-held-out-contexts-v1.0.json'
class SCW5HeldOutContextsTests(unittest.TestCase):
    def load(self): return json.loads(DATA.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_sc_w5_held_out_contexts.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_all_contexts_retained(self):
        d=self.load(); self.assertEqual(len(d['contexts']),12); self.assertEqual([x['id'] for x in d['contexts']],[f'HO-{i:02d}' for i in range(1,13)])
    def test_unknowns_not_counted_as_successes(self):
        d=self.load(); self.assertEqual(d['counts']['pass_no_new_primitive'],10); self.assertEqual(d['counts']['unresolved_evidential_boundary'],2); self.assertEqual(d['counts']['genuine_primitive_extension'],0)
    def test_every_case_tests_complete_kernel(self):
        for x in self.load()['contexts']: self.assertEqual(set(x['rccd_realization']),{'R1','R2','R3','R4','R5'})
    def test_final_adjudication_is_next(self):
        self.assertEqual(self.load()['next_decisive_workstream'],'SC-W6-FINAL-INTERNAL-ADJUDICATION')
if __name__=='__main__': unittest.main()
