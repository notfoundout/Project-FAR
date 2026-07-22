from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-queue-v1.0.json'
class PostW9InternalScopeChallengeTests(unittest.TestCase):
    def load(self,path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_post_w9_internal_scope_challenge.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_program_forces_terminal_outcome(self):
        data=self.load(PROGRAM); self.assertEqual(len(data['workstreams']),6); self.assertIn('multiple_incomparable_kernels',data['terminal_outcomes']); self.assertIn('generic_only_commonality',data['terminal_outcomes']); self.assertIn('current_theorem_scope_construct_loaded',data['terminal_outcomes'])
    def test_external_work_is_deferred(self):
        data=self.load(PROGRAM); self.assertEqual(data['external_disposition'],'deferred_until_final_internal_adjudication'); self.assertIn('No external review or replication is authorized by this program.',data['frozen_principles'])
    def test_queue_begins_with_scope_neutrality(self):
        queue=self.load(QUEUE); next_pr=queue['next_action']['target_pr']; self.assertIn(next_pr,{270,271,272,273,274,275})
        expected={270:'SC-W1-SCOPE-NEUTRALITY',271:'SC-W2-BOUNDARY-REASONING',272:'SC-W3-CONTRACT-LADDER',273:'SC-W4-REPRESENTATION-ESCAPE',274:'SC-W5-HELD-OUT-CONTEXTS',275:'SC-W6-FINAL-INTERNAL-ADJUDICATION'}
        self.assertEqual(queue['next_action']['workstream'],expected[next_pr])
        if next_pr==270:
            self.assertEqual(queue['ordered_followups'],[271,272,273,274,275])
        if next_pr==272:
            self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[270,271]); self.assertEqual(queue['ordered_followups'],[273,274,275]); self.assertEqual(queue['next_action']['workstream'],'SC-W3-CONTRACT-LADDER')
        if next_pr>=273:
            self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[270,271,272]); self.assertEqual(queue['ordered_followups'],[274,275]); self.assertEqual(queue['next_action']['workstream'],'SC-W4-REPRESENTATION-ESCAPE')
if __name__=='__main__':unittest.main()
