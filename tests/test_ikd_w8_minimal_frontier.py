from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w8-minimal-frontier-v1.0.json'
class IKDW8MinimalFrontierTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w8_minimal_frontier.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_bidirectional_reconstruction_covers_successful_set(self):
        rows=self.load()['bidirectional_reconstructions']; self.assertEqual({x['architecture'] for x in rows},{'FARA-001','LTS-PROV-001','COALG-DYN-001'})
        for row in rows:
            self.assertTrue(row['from_rccd']); self.assertTrue(row['to_rccd']); self.assertTrue(row['hidden_machinery_charged']); self.assertEqual(row['classification'],'rccd_equivalent_realization')
    def test_one_commitment_equivalence_class(self):
        classes=self.load()['commitment_equivalence_classes']; self.assertEqual(len(classes),1); self.assertEqual(classes[0]['id'],'CEC-RCCD-001'); self.assertEqual(set(classes[0]['members']),{'RCCD-001','FARA-001','LTS-PROV-001','COALG-DYN-001'}); self.assertEqual(len(classes[0]['shared_necessary_commitments']),5)
    def test_kernel_and_realization_frontiers_are_separate(self):
        frontier=self.load()['pareto_frontier']; self.assertEqual(frontier['kernel_level'],['CEC-RCCD-001']); self.assertEqual(set(frontier['realization_level']),{'FARA-001','LTS-PROV-001','COALG-DYN-001'})
    def test_rccd_is_only_conditionally_irreducible(self):
        data=self.load(); self.assertEqual(data['rccd_reducibility']['result'],'not_reducible_under_registered_contract'); self.assertIn('relative to C, P, and E',data['rccd_reducibility']['scope_limit'])
    def test_no_additional_or_incomparable_kernel_survives(self):
        data=self.load(); self.assertEqual(data['additional_essential_commitment_search']['result'],'none_required_across_all_successful_architectures'); self.assertEqual(data['incomparable_kernel_search']['result'],'no_surviving_incomparable_kernel_in_registered_successful_set')
    def test_terminal_result_remains_pending_w9(self):
        data=self.load(); self.assertEqual(data['terminal_result'],'one_nontrivial_common_kernel_on_defined_class_pending_terminal_adjudication'); self.assertEqual(data['next_decisive_workstream'],'IKD-W9-TERMINAL-ADJUDICATION'); self.assertIn('independent external validation',data['nonclaims'])
if __name__=='__main__':unittest.main()
