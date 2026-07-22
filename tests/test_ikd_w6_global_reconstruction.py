from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w6-global-reconstruction-v1.0.json'
class IKDW6GlobalReconstructionTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w6_global_reconstruction.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_search_is_broad_but_not_overclaimed(self):
        data=self.load(); self.assertGreaterEqual(len(data['searched_bases']),14); self.assertIn('not mathematically exhaustive',data['scope'])
        self.assertIn('every logically possible vocabulary has been searched',data['nonclaims'])
    def test_successful_bases_reintroduce_rccd(self):
        data=self.load(); successful=[x for x in data['searched_bases'] if x['result']=='equivalent_reintroduction']
        self.assertGreaterEqual(len(successful),8)
    def test_countermodels_cover_core_losses(self):
        ids={x['id'] for x in self.load()['surviving_countermodels']}
        self.assertEqual(ids,{'CM-DEP','CM-HIST','CM-SEM','CM-OBS','CM-SCHED'})
    def test_terminal_result_and_next_workstream(self):
        data=self.load(); self.assertEqual(data['terminal_result'],'no_strictly_cheaper_non_equivalent_reconstruction_found_in_expanded_registered_search'); self.assertEqual(data['next_decisive_workstream'],'IKD-W7-LOWER-BOUNDS')
if __name__=='__main__':unittest.main()
