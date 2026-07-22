from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w9-terminal-adjudication-v1.0.json'
class IKDW9TerminalAdjudicationTests(unittest.TestCase):
    def load(self)->dict:return json.loads(RESULT.read_text(encoding='utf-8'))
    def test_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/'tools/check_ikd_w9_terminal_adjudication.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr); self.assertIn('PASS',cp.stdout)
    def test_selects_registered_positive_outcome(self):
        data=self.load(); self.assertEqual(data['terminal_outcome'],'one_nontrivial_common_kernel'); self.assertEqual(data['kernel']['id'],'RCCD-001')
    def test_scope_is_explicit(self):
        scope=self.load()['scope']; self.assertEqual(scope['universality_class']['id'],'C-EFFECTIVE-REASONING-001'); self.assertEqual(scope['preservation_contract']['id'],'P-RCCD-FAITHFUL-001'); self.assertEqual(scope['representation_family']['id'],'E-EFFECTIVE-REP-001')
    def test_all_five_commitments_are_required(self):
        self.assertEqual(len(self.load()['kernel']['necessary_commitments']),5)
    def test_answer_is_bounded_not_unrestricted(self):
        data=self.load(); self.assertIn('Relative to',data['internal_answer']); self.assertIn('unrestricted',data['internal_answer']); self.assertIn('unrestricted universality over every possible form of reasoning',data['excluded_claims'])
    def test_stopping_rule_is_falsification_driven(self):
        stop=self.load()['post_internal_stopping_rule']; self.assertIn('stop adding broad supportive mappings',stop['internal_exploration']); self.assertEqual(len(stop['reopen_conditions']),4)
    def test_external_validation_remains_pending(self):
        data=self.load(); self.assertEqual(data['program_status'],'internal_discovery_program_complete_external_validation_pending'); self.assertGreaterEqual(len(data['external_requirements']),5)
if __name__=='__main__':unittest.main()
