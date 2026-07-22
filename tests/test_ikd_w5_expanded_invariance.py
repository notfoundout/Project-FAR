from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w5-expanded-invariance-v1.0.json'
class IKDW5ExpandedInvarianceTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w5_expanded_invariance.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_all_registered_transformations_pass(self):
        r=self.load(); tx=r['executed_transformations']
        self.assertEqual(len(tx),12); self.assertEqual(len({x['id'] for x in tx}),12); self.assertTrue(all(x['result']=='pass' for x in tx))
    def test_invariance_is_not_vacuous(self):
        c=self.load()['invariance_contract']
        self.assertTrue(c['bidirectional_commitment_recovery_required']); self.assertTrue(c['operational_consequences_preserved']); self.assertTrue(c['all_encoders_decoders_adapters_canonicalizers_and_proof_objects_charged']); self.assertTrue(c['unrestricted_interpreters_prohibited'])
    def test_negative_controls_remain_rejected(self):
        rejected=set(self.load()['rejected_non_equivalences'])
        for item in ('dependency_erasure','retroactive_revision_rewrite','semantic_version_merging','hidden_state_collapse_without_commitment_equivalence','scheduler_hiding','future_history_access'): self.assertIn(item,rejected)
    def test_claim_boundary_and_next_workstream(self):
        r=self.load(); self.assertEqual(r['terminal_result'],'bounded_expanded_representation_invariance_supported'); self.assertEqual(r['claim_effect']['all_possible_representation_changes'],'not_supported'); self.assertEqual(r['next_decisive_workstream'],'IKD-W6-GLOBAL-RECONSTRUCTION'); self.assertIn('RCCD is invariant under every conceivable encoding',r['nonclaims'])
if __name__=='__main__': unittest.main()
