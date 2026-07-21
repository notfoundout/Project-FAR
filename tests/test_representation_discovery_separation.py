from __future__ import annotations
import copy,json
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
from check_representation_discovery_separation import authorization_errors
def load(path:str)->dict: return json.loads((ROOT/path).read_text(encoding='utf-8'))
class RepresentationDiscoverySeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=load('theory/evaluation/generic-relational-baseline-v1.0.json'); cls.scope=load('theory/evaluation/reasoning-and-contrast-scope-v1.0.json'); cls.corpus_result=load('theory/evaluation/w3-5-corpus-freeze-result-v1.0.json'); cls.factor_result=load('theory/evaluation/w3-5-factorization-result-v1.0.json'); cls.discrimination_result=load('theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json'); cls.specificity_result=load('theory/evaluation/w3-5-fara-specificity-result-v1.0.json'); cls.candidate_result=load('theory/evaluation/w3-5-candidate-test-result-v1.0.json'); cls.target=load('theory/evaluation/universal-structure-discovery-target-v1.0.json'); cls.w35=load('theory/evaluation/w3-5-specificity-and-discovery-gate.json'); cls.candidates=load('theory/evaluation/universal-structure-candidate-registry.json'); cls.gates=load('theory/evaluation/research-gates.json'); cls.claims=load('theory/evaluation/central-claim-registry.json'); cls.rep_target=load('theory/evaluation/thm-target-001.json'); cls.ledger=load('theory/evaluation/s-core-construction-obstruction-ledger.json')
    def test_generic_baseline_is_reasoning_neutral(self): self.assertEqual(self.baseline['baseline_id'],'GREL-001'); self.assertEqual(self.baseline['reasoning_specific_primitives'],[])
    def test_factorization_is_dimensioned(self):
        expected={'expressiveness','translation','constraint_strength','reasoning_specificity','cost_relation','overall_interpretation'}; self.assertEqual(set(self.baseline['result_dimensions']),expected); self.assertEqual(set(self.baseline['current_result']),expected); self.assertTrue(self.baseline['single_scalar_classification_prohibited'])
    def test_generic_baseline_has_no_result_yet(self):
        expected={'expressiveness':'equivalent','translation':'bidirectional','constraint_strength':'fara_stricter','reasoning_specificity':'not_established','cost_relation':'tradeoff','overall_interpretation':'fara_constrained_equivalent'}; self.assertEqual(self.baseline['current_result'],expected); self.assertEqual(self.factor_result['dimensions'],expected); self.assertFalse(self.factor_result['factorization_contract']['primitive_reduction_established'])
    def test_positive_scope_is_independent_of_fara(self): self.assertTrue(self.scope['admission_rules']['positive_independent_of_fara'])
    def test_contrast_scope_is_not_selected_by_failure(self): self.assertTrue(self.scope['admission_rules']['contrast_independent_of_fara_failure'])
    def test_scope_framework_and_concrete_corpus_are_frozen_without_execution(self):
        self.assertTrue(self.scope['framework_frozen']); self.assertEqual(self.scope['concrete_corpus_status'],'frozen'); self.assertEqual(self.scope['concrete_corpus_id'],'RCS-CORPUS-001'); self.assertEqual(len(self.scope['positive_instances']),8); self.assertEqual(len(self.scope['contrast_instances']),8); self.assertEqual(len(self.scope['disputed_instances']),2); self.assertEqual(self.scope['execution_status'],'ready_for_candidate_neutral_execution'); self.assertEqual(self.scope['candidate_scoring_status'],'not_started')
    def test_corpus_freeze_does_not_claim_execution_or_w5_authorization(self):
        self.assertEqual(self.corpus_result['status'],'complete'); self.assertEqual(self.corpus_result['artifact_id'],'RCS-CORPUS-001'); self.assertEqual(self.corpus_result['candidate_scoring_status'],'not_started'); self.assertEqual(self.corpus_result['claim_impact']['reasoning_contrast_execution'],'not_started'); self.assertFalse(self.corpus_result['claim_impact']['W5_authorized'])
    def test_universal_target_is_separate(self): self.assertEqual(self.target['target_id'],'THM-US-TARGET-001'); self.assertEqual(self.target['representation_track_implication'],'none')
    def test_no_universal_theorem_is_preproved(self): self.assertTrue(all(item['status']!='proved' for item in self.target['theorem_families']))
    def test_w35_is_between_w3_and_w5(self): self.assertEqual(self.w35['position'],'after_W3_before_W5'); self.assertFalse(self.w35['w5_authorized'])
    def test_w4_and_corpus_freeze_do_not_resolve_w35(self):
        by_id={item['id']:item for item in self.ledger['obligations']}; self.assertEqual(by_id['OBS-SC-010']['status'],'obstruction_established'); self.assertEqual(self.w35['status'],'in_progress_specificity_complete'); self.assertEqual(self.w35['current_results']['reasoning_contrast_corpus'],'frozen'); self.assertEqual(self.w35['current_results']['reasoning_discrimination'],'bounded_role_conjunctive_discrimination_established'); self.assertEqual(self.w35['current_results']['fara_specificity'],'not_unique_at_registered_scope'); self.assertEqual(self.w35['current_results']['candidate_invariants'],'not_executed'); self.assertFalse(self.w35['w5_authorized'])
    def test_w35_registers_completed_and_missing_artifacts(self):
        self.assertGreaterEqual(len(self.w35['required_result_artifacts']),8); by_id={a['id']:a for a in self.w35['required_result_artifacts']}; completed={'W35-CORPUS-RESULT','W35-FACTOR-RESULT','W35-SCOPE-RESULT','W35-SPEC-RESULT'}
        for aid in completed:
            a=by_id[aid]; self.assertEqual(a['status'],'complete'); self.assertRegex(a['content_sha256'],r'^[0-9a-f]{64}$'); self.assertTrue((ROOT/a['path']).is_file())
        for aid,a in by_id.items():
            self.assertIn('path',a); self.assertIn('artifact_id',a); self.assertIn('content_sha256',a)
            if aid not in completed: self.assertEqual(a['status'],'missing'); self.assertIsNone(a['path']); self.assertIsNone(a['artifact_id']); self.assertIsNone(a['content_sha256'])
    def test_candidates_are_not_prejudged(self):
        self.assertTrue(all(item['structural_commitment_necessity']=='unresolved' for item in self.candidates['candidates'])); self.assertTrue(all(item['trial_evidence_status']=='missing' for item in self.candidates['candidates'])); self.assertEqual(self.candidates['aggregate_result'],'candidate_structural_indispensability_unresolved_reexecution_required'); self.assertEqual(self.candidates['status'],'preliminary_internal_adjudication_reexecution_required'); self.assertEqual(self.candidate_result['status'],'preliminary_internal_adjudication_requires_reexecution'); self.assertEqual(self.candidate_result['claim_effect']['universal_structure'],'unresolved')
    def test_representation_target_is_rep_track(self): self.assertEqual(self.rep_target['program_track'],'REP'); self.assertIn('universal_structure',self.rep_target['does_not_imply'])
    def test_w5_now_requires_only_w35(self): self.assertEqual(self.rep_target['w5_authorization']['blocked_by'],['W3.5-SDG-001']); self.assertEqual(self.rep_target['w5_authorization']['resolved_dependencies'],['OBS-SC-010'])
    def test_rep_theorems_are_blocked_by_specificity_bridge(self):
        by_id={item['id']:item for item in self.rep_target['theorem_family']}
        for tid in ('THM-CORE-COMMON-001','THM-CORE-REP-001','THM-IMP-001'): self.assertIn('specificity_discovery_bridge',by_id[tid]['blocked_by']); self.assertNotIn('formal_negative_controls',by_id[tid]['blocked_by'])
    def test_research_gates_separate_framework_corpus_and_results(self):
        by={item['name']:item for item in self.gates['gates']}
        for name in ('generic-baseline-frozen','reasoning-contrast-scope-framework-frozen','reasoning-contrast-corpus-frozen','baseline-factorization-resolved','fara-specificity-resolved','reasoning-contrast-execution','formal-negative-controls'): self.assertEqual(by[name]['status'],'satisfied'); self.assertTrue(by[name]['evidence'])
        self.assertEqual(by['universal-structure-result']['status'],'not_satisfied'); self.assertNotIn('reasoning-contrast-scope-frozen',by)
    def test_rep_capacity_does_not_imply_universal_structure(self): self.assertIn('CLM-UNIVERSAL-STRUCTURE',{i['id']:i for i in self.claims['claims']}['CLM-REP-CAPACITY']['does_not_imply'])
    def test_universal_structure_status_is_unresolved(self): self.assertEqual({i['id']:i for i in self.claims['claims']}['CLM-UNIVERSAL-STRUCTURE']['current_status'],'unresolved')
    def test_current_unauthorized_state_is_valid(self): self.assertEqual(authorization_errors(self.w35,self.rep_target,self.scope,self.gates,self.ledger,ROOT),[])
    def test_status_only_authorization_is_rejected_by_remaining_w35_evidence(self):
        w35=copy.deepcopy(self.w35); target=copy.deepcopy(self.rep_target); w35['w5_authorized']=True; w35['status']='resolved'; target['w5_authorization']['authorized']=True; target['w5_authorization']['blocked_by']=[]; joined='\n'.join(authorization_errors(w35,target,self.scope,self.gates,self.ledger,ROOT)); self.assertNotIn('OBS-SC-010 must have a terminal',joined); self.assertNotIn('concrete reasoning and contrast corpus must be frozen',joined); self.assertNotIn('factorization dimension',joined); self.assertIn('candidate_invariants must be complete',joined); self.assertIn('machinery_and_cost must be complete',joined); self.assertIn('is not complete',joined); self.assertIn('authorization evidence is empty',joined)
    def test_makefile_runs_separation_and_corpus_checkers_three_times(self):
        text=(ROOT/'Makefile').read_text(encoding='utf-8'); self.assertEqual(text.count('python tools/check_representation_discovery_separation.py'),3); self.assertEqual(text.count('python tools/check_w3_5_corpus_freeze.py'),3); self.assertEqual(text.count('python tools/check_w3_5_factorization.py'),3); self.assertEqual(text.count('python tools/check_w3_5_specificity.py'),3); self.assertEqual(text.count('python tools/check_w3_5_candidate_tests.py'),3)
    def test_makefile_runs_separation_checker_three_times(self): self.assertEqual((ROOT/'Makefile').read_text(encoding='utf-8').count('python tools/check_representation_discovery_separation.py'),3)
    def test_scope_framework_is_frozen_but_corpus_is_not(self): self.assertTrue(self.scope['framework_frozen']); self.assertEqual(self.scope['concrete_corpus_status'],'frozen'); self.assertEqual(self.scope['candidate_scoring_status'],'not_started'); self.assertEqual(self.scope['execution_status'],'ready_for_candidate_neutral_execution')
    def test_status_only_authorization_is_rejected(self):
        w35=copy.deepcopy(self.w35); target=copy.deepcopy(self.rep_target); w35['w5_authorized']=True; w35['status']='resolved'; target['w5_authorization']['authorized']=True; target['w5_authorization']['blocked_by']=[]; errors=authorization_errors(w35,target,self.scope,self.gates,self.ledger,ROOT); self.assertTrue(errors); self.assertTrue(any('candidate_invariants must be complete' in e for e in errors)); self.assertTrue(any('machinery_and_cost must be complete' in e for e in errors)); self.assertTrue(any('is not complete' in e for e in errors))
    def test_w35_registers_immutable_evidence_fields(self):
        by={a['id']:a for a in self.w35['required_result_artifacts']}
        for a in by.values(): self.assertIn('path',a); self.assertIn('artifact_id',a); self.assertIn('content_sha256',a)
        for aid in ('W35-CORPUS-RESULT','W35-FACTOR-RESULT','W35-SCOPE-RESULT','W35-SPEC-RESULT'): self.assertEqual(by[aid]['status'],'complete'); self.assertRegex(by[aid]['content_sha256'],r'^[0-9a-f]{64}$')
        self.assertEqual(by['W35-CANDIDATE-RESULT']['status'],'missing')
    def test_w4_completion_does_not_resolve_w35(self):
        by_id={item['id']:item for item in self.ledger['obligations']}; self.assertEqual(by_id['OBS-SC-010']['status'],'obstruction_established'); self.assertEqual(self.w35['status'],'in_progress_specificity_complete'); self.assertFalse(self.w35['w5_authorized']); self.assertEqual(self.w35['current_results']['fara_specificity'],'not_unique_at_registered_scope'); self.assertEqual(self.w35['current_results']['candidate_invariants'],'not_executed')
if __name__=='__main__': unittest.main()