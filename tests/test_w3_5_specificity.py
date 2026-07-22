from __future__ import annotations
import copy, hashlib
from pathlib import Path
import sys, unittest
ROOT=Path(__file__).resolve().parents[1]; TOOLS=ROOT/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))
from check_w3_5_specificity import CANDIDATES,DISC,FACTOR,GATES,LICENSING,SPEC,TARGET,W35,EXPECTED_COUNTS,load,policy_errors,validate
from w3_5_factor_source import load_records
from w3_5_specificity import CRITERIA,SpecificityError,classify,run_discrimination,validate_licensing
class W35SpecificityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.licensing=load(LICENSING); cls.discrimination=load(DISC); cls.specificity=load(SPEC); cls.w35=load(W35); cls.gates=load(GATES); cls.target=load(TARGET); cls.candidates=load(CANDIDATES); cls.factorization=load(FACTOR); cls.digests={'licensing':hashlib.sha256(LICENSING.read_bytes()).hexdigest(),'discrimination':hashlib.sha256(DISC.read_bytes()).hexdigest(),'specificity':hashlib.sha256(SPEC.read_bytes()).hexdigest()}
    def errors(self,**changes):
        payload={'licensing':copy.deepcopy(self.licensing),'discrimination':copy.deepcopy(self.discrimination),'specificity':copy.deepcopy(self.specificity),'w35':copy.deepcopy(self.w35),'gates':copy.deepcopy(self.gates),'target':copy.deepcopy(self.target),'candidates':copy.deepcopy(self.candidates),'factorization':copy.deepcopy(self.factorization),'digests':copy.deepcopy(self.digests)}; payload.update(changes); return policy_errors(**payload)
    def test_complete_package_passes(self):
        report=validate(ROOT); self.assertEqual(report['status'],'pass'); self.assertEqual(report['instance_count'],18); self.assertEqual(report['class_counts'],EXPECTED_COUNTS); self.assertEqual(report['fara_specificity'],'not_unique_at_registered_scope')
    def test_runtime_scoring_preserves_disputed_cases(self):
        report=run_discrimination(ROOT); self.assertEqual(report['class_counts']['disputed']['borderline'],2); self.assertEqual(report['primary_metrics']['statistical_inference'],'not_authorized')
    def test_decision_rule_is_conjunctive(self):
        all_pass={criterion:{'status':'pass'} for criterion in CRITERIA}; self.assertEqual(classify(all_pass),'reasoning_like'); two=copy.deepcopy(all_pass); two['R2']['status']='fail'; two['R5']['status']='fail'; self.assertEqual(classify(two),'nonreasoning_like'); partial=copy.deepcopy(all_pass); partial['R2']['status']='partial'; self.assertEqual(classify(partial),'borderline'); unknown=copy.deepcopy(all_pass); unknown['R7']['status']='unknown'; self.assertEqual(classify(unknown),'unknown')
    def test_admission_metadata_is_banned_from_licensing(self):
        licensing=copy.deepcopy(self.licensing); licensing['records'][0]['admission_decision']='positive'
        with self.assertRaisesRegex(SpecificityError,'banned'): validate_licensing(licensing,load_records(ROOT))
    def test_missing_criterion_is_rejected(self):
        licensing=copy.deepcopy(self.licensing); licensing['records'][0]['profile']=licensing['records'][0]['profile'][:-1]
        with self.assertRaisesRegex(SpecificityError,'criterion profile'): validate_licensing(licensing,load_records(ROOT))
    def test_semantic_coding_cannot_be_promoted_to_blind_or_independent(self):
        licensing=copy.deepcopy(self.licensing); licensing['authorship_and_blinding']['semantic_coder_blind_to_admission_labels']=True; self.assertTrue(any('misreported as blind' in error for error in self.errors(licensing=licensing))); licensing=copy.deepcopy(self.licensing); licensing['authorship_and_blinding']['independent_external_evaluator']=True; self.assertTrue(any('misreported as independent' in error for error in self.errors(licensing=licensing)))
    def test_unique_fara_capacity_promotion_is_rejected(self):
        specificity=copy.deepcopy(self.specificity); specificity['result']['unique_discriminative_capacity_of_fara']='established'; self.assertTrue(any('uniqueness' in error for error in self.errors(specificity=specificity)))
    def test_general_specificity_and_necessity_promotion_are_rejected(self):
        specificity=copy.deepcopy(self.specificity); specificity['result']['fara_primitive_necessity']='established'; specificity['result']['fara_reasoning_specificity_general']='established'; joined='\n'.join(self.errors(specificity=specificity)); self.assertIn('primitive necessity',joined); self.assertIn('general FARA specificity',joined)
    def test_disputed_cases_cannot_enter_primary_metric(self):
        discrimination=copy.deepcopy(self.discrimination); discrimination['execution_contract']['disputed_excluded_from_primary_metric']=False; self.assertTrue(any('disputed' in error for error in self.errors(discrimination=discrimination)))
    # Historical name retained; now verifies completed registered-scope evidence cannot regress to unresolved.
    def test_candidate_registry_remains_unexecuted(self):
        candidates=copy.deepcopy(self.candidates); candidates['candidates'][0]['structural_commitment_necessity']='unresolved'; self.assertTrue(any('candidate structural axis is not terminal' in error for error in self.errors(candidates=candidates)))
    def test_candidate_aggregate_promotion_is_rejected(self):
        candidates=copy.deepcopy(self.candidates); candidates['aggregate_result']='no_registered_candidate_indispensable_within_frozen_class'; self.assertTrue(any('candidate aggregate changed' in error for error in self.errors(candidates=candidates)))
    def test_status_only_w5_promotion_is_rejected(self):
        w35=copy.deepcopy(self.w35); target=copy.deepcopy(self.target); w35['w5_authorized']=False; target['w5_authorization']['authorized']=False; target['w5_authorization']['blocked_by']=['W3.5-SDG-001']; joined='\n'.join(self.errors(w35=w35,target=target)); self.assertIn('authorization stage is inconsistent',joined); self.assertIn('blocker stage is inconsistent',joined)
    def test_missing_gate_evidence_is_rejected(self):
        gates=copy.deepcopy(self.gates); next(item for item in gates['gates'] if item['name']=='fara-specificity-resolved')['evidence']=[]; self.assertTrue(any('lacks complete evidence' in error for error in self.errors(gates=gates)))
if __name__=='__main__': unittest.main()
