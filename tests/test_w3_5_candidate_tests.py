from __future__ import annotations
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
from check_w3_5_candidate_tests import CONTRACT,RESULT,W35,load,validate
from w3_5_candidate_execution import AXES,derive,execute

class W35CandidateExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=load(CONTRACT); cls.result=load(RESULT); cls.w35=load(W35); cls.trials=execute()
    def test_complete_execution_passes(self):
        report=validate(ROOT); self.assertEqual(report['status'],'pass'); self.assertEqual(report['atomic_trials'],648)
    def test_exact_cartesian_coverage(self):
        self.assertEqual(len(self.trials),648); self.assertEqual(len({t['trial_id'] for t in self.trials}),648)
        self.assertEqual({t['representation_layer'] for t in self.trials},{'source','GREL','FARA'})
    def test_each_candidate_has_54_trials(self):
        counts={}
        for t in self.trials: counts[t['candidate_id']]=counts.get(t['candidate_id'],0)+1
        self.assertEqual(set(counts.values()),{54})
    def test_all_ablation_records_are_commitment_level(self):
        self.assertTrue(all(t['ablation_operation']['label_only_removal'] is False for t in self.trials))
        self.assertTrue(all(t['ablation_operation']['dependent_values_recomputed'] is True for t in self.trials))
    def test_equivalent_reintroduction_requires_equivalence_and_cost(self):
        for t in self.trials:
            if t['equivalent_commitment_reintroduced']:
                self.assertEqual(t['equivalence_comparison']['verdict'],'commitment_equivalent')
                self.assertGreater(t['machinery_cost']['total_units'],0)
    def test_results_are_derived_from_trials(self):
        derived={x['id']:x for x in derive(self.trials)}
        for r in self.result['results']:
            for axis in AXES: self.assertEqual(r[axis],derived[r['id']][axis])
    def test_genericity_does_not_refute_structural_necessity(self):
        by={x['id']:x for x in self.result['results']}
        self.assertEqual(by['USC-001']['reasoning_specificity'],'refuted_at_registered_scope')
        self.assertEqual(by['USC-001']['structural_commitment_necessity'],'supported_at_registered_scope')
    def test_derivability_does_not_refute_structural_necessity(self):
        by={x['id']:x for x in self.result['results']}
        self.assertEqual(by['USC-002']['primitive_necessity'],'refuted_at_registered_scope')
        self.assertEqual(by['USC-002']['structural_commitment_necessity'],'supported_at_registered_scope')
    def test_w5_remains_blocked(self):
        self.assertFalse(self.w35['w5_authorized']); self.assertEqual(self.w35['status'],'in_progress_candidate_complete')
        self.assertEqual(self.w35['current_results']['machinery_and_cost'],'not_executed')
    def test_contract_does_not_freeze_terminal_answers(self):
        self.assertNotIn('registered_terminal_classification',json.dumps(self.contract))
    def test_mutated_trial_breaks_derivation(self):
        trials=copy.deepcopy(self.trials); target=next(t for t in trials if t['candidate_id']=='USC-001' and t['admission_class']=='positive')
        target['trial_outcome']='ablation_preserves_registered_behavior'; target['equivalent_commitment_reintroduced']=False
        derived={x['id']:x for x in derive(trials)}
        recorded=next(x for x in self.result['results'] if x['id']=='USC-001')
        self.assertNotEqual(derived['USC-001']['structural_commitment_necessity'],recorded['structural_commitment_necessity'])
    def test_makefile_runs_candidate_checker_three_times(self):
        self.assertEqual((ROOT/'Makefile').read_text().count('python tools/check_w3_5_candidate_tests.py'),3)
if __name__=='__main__': unittest.main()
