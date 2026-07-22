from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'theory/evaluation/post-usd-internal-discovery-continuation-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json'
class PostUSDInternalDiscoveryContinuationTests(unittest.TestCase):
    def load(self,path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_post_usd_internal_discovery_continuation.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_external_packages_are_preserved_but_deferred(self):
        disposition=self.load(PROGRAM)['external_package_disposition']
        for key in ('EVC-W1-EXTERNAL-PROOF-REVIEW','EVC-W2-R3-TECHNICAL-REPLICATION','EVC-W3-R4-ADVERSARIAL-REPLICATION'): self.assertEqual(disposition[key],'frozen_preserved_execution_deferred')
        self.assertIn('not withdrawn',disposition['rule']); self.assertIn('No external package is released',disposition['rule'])
    def test_execution_order_is_complete_and_contiguous(self):
        program=self.load(PROGRAM); streams=program['workstreams']
        self.assertEqual(program['registration_pr'],260); self.assertEqual(program['program_id'],'POST-USD-IKD-001'); self.assertEqual(len(streams),9); self.assertEqual([x['sequence'] for x in streams],list(range(1,10))); self.assertEqual([x['target_pr'] for x in streams],list(range(261,270))); self.assertEqual(streams[0]['id'],'IKD-W1-CANDIDATE-ARCHITECTURES'); self.assertEqual(streams[-1]['id'],'IKD-W9-TERMINAL-ADJUDICATION')
    def test_no_premature_universal_or_external_claim(self):
        nonclaims=set(self.load(PROGRAM)['nonclaims']); self.assertIn('a universal structure has been discovered',nonclaims); self.assertIn('existing external packages have been executed',nonclaims); self.assertIn('failure to find a common kernel proves global nonexistence',nonclaims)
    def test_next_action_is_candidate_architecture_freeze(self):
        queue=self.load(QUEUE); self.assertEqual(queue['registration_pr'],260); self.assertEqual(queue['queue_id'],'POST-USD-IKD-QUEUE-001')
        if queue['status']=='internal_program_complete':
            self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],list(range(261,270))); self.assertEqual(queue['ordered_followups'],[]); self.assertEqual(queue['terminal_outcome'],'one_nontrivial_common_kernel'); self.assertEqual(queue['terminal_result'],'bounded_rccd_universality_theorem_supported_internally'); self.assertEqual(queue['next_action']['phase'],'external_validation_and_empirical_bridge'); self.assertEqual(queue['next_action']['status'],'not_authorized_by_internal_queue')
        else:
            next_pr=queue['next_action']['target_pr']; self.assertIn(next_pr,{261,262,263,264,265,266,267,268,269})
            expected={261:'IKD-W1-CANDIDATE-ARCHITECTURES',262:'IKD-W2-EXPANDED-COMPETITION',263:'IKD-W3-COMMON-FACTOR',264:'IKD-W4-CROSS-FEATURE-COMPOSITION',265:'IKD-W5-EXPANDED-INVARIANCE',266:'IKD-W6-GLOBAL-RECONSTRUCTION',267:'IKD-W7-LOWER-BOUNDS',268:'IKD-W8-MINIMAL-FRONTIER',269:'IKD-W9-TERMINAL-ADJUDICATION'}
            self.assertEqual(queue['next_action']['workstream'],expected[next_pr])
            if next_pr==266:
                self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[261,262,263,264,265]); self.assertEqual([x['target_pr'] for x in queue['ordered_followups']],list(range(267,270)))
            if next_pr==267:
                self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[261,262,263,264,265,266]); self.assertEqual([x['target_pr'] for x in queue['ordered_followups']],[268,269])
            if next_pr==268:
                self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[261,262,263,264,265,266,267]); self.assertEqual([x['target_pr'] for x in queue['ordered_followups']],[269])
            if next_pr==269:
                self.assertEqual([x['target_pr'] for x in queue['completed_workstreams']],[261,262,263,264,265,266,267,268]); self.assertEqual(queue['ordered_followups'],[]); self.assertIn('bounded internal answer',queue['next_action']['title'])
    def test_terminal_outcomes_include_positive_negative_and_unresolved(self):
        outcomes=set(self.load(PROGRAM)['terminal_outcomes']); self.assertIn('one_nontrivial_common_kernel',outcomes); self.assertIn('bounded_no_single_kernel',outcomes); self.assertIn('unresolved',outcomes)
if __name__=='__main__': unittest.main()
