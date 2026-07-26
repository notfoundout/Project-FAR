import copy, importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('forensics',ROOT/'tools/check_swe_agent_v2_forensics.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ForensicValidationTests(unittest.TestCase):
 def test_repository_forensics_validate(self): self.assertEqual([],mod.validate())
 def test_negative_rejects_unclassified_claim(self):
  causes={'claims':[{'claim_id':'x','run':'v1.0.0-r1','evidence_class':'opinion','remediable':False}]}; req={'requirements':[]}
  self.assertTrue(any('evidence class' in e for e in mod.validate_records(causes,req)))
 def test_negative_rejects_inference_without_falsification(self):
  causes={'claims':[{'claim_id':'x','run':'v1.0.0-r1','evidence_class':'inferred','confidence':'high','confidence_reasoning':'x','confirmation_condition':'x','supporting_evidence':['x'],'contradictory_evidence':['x'],'alternative_explanations':['x'],'remediable':False}]}
  self.assertTrue(any('falsification' in e for e in mod.validate_records(causes,{'requirements':[]})))
 def test_negative_rejects_remediable_cause_without_control(self):
  causes={'claims':[{'claim_id':'x','run':'v1.0.0-r1','evidence_class':'observed','remediable':True,'validation_test':'x'}]}
  self.assertTrue(any('lacks control' in e for e in mod.validate_records(causes,{'requirements':[]})))
 def test_negative_rejects_control_without_validation_test(self):
  req={'requirements':[{'requirement_id':'R','failure_addressed':'x','supporting_evidence':['x'],'required_behavior':'x','acceptance_criterion':'x','negative_test':'x','likely_cost':'x','residual_risk':'x'}]}
  cause={'claim_id':'x','run':'v1.0.0-r1','evidence_class':'observed','remediable':True,'proposed_control':'R'}
  self.assertTrue(any('validation test' in e for e in mod.validate_records({'claims':[cause]},req)))
class OptionalDemoCollectionContractTests(unittest.TestCase):
 def test_demo_tests_declare_optional_dependency_before_fastapi_import(self):
  for relative in ('commercial/far-demo/tests/test_demo.py','commercial/far-demo/tests/test_validation.py'):
   source=(ROOT/relative).read_text()
   self.assertIn('raise unittest.SkipTest(',source)
   self.assertLess(source.index('raise unittest.SkipTest('),source.index('from fastapi.testclient import TestClient'))
   self.assertNotIn('import pytest',source)


class InventoryReconciliationNegativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.inventory=mod.load(mod.FORENSICS/'evidence-inventory.json')
  cls.lock=mod.load(mod.CASE/'primary-freeze/source-artifact-lock.json')
 def validate(self,inventory=None,lock=None): return mod.validate_inventory(inventory or copy.deepcopy(self.inventory),lock or copy.deepcopy(self.lock))
 def mutate_entry(self,predicate,**changes):
  data=copy.deepcopy(self.inventory); entry=next(x for x in data['artifacts'] if predicate(x)); entry.update(changes); return data
 def test_deleted_committed_entry_fails(self):
  data=copy.deepcopy(self.inventory); data['artifacts']=[x for x in data['artifacts'] if not x['path'].endswith('/manifest.json')]
  self.assertTrue(any('absent from inventory' in e for e in self.validate(data)))
 def test_duplicate_entry_fails(self):
  data=copy.deepcopy(self.inventory); data['artifacts'].append(copy.deepcopy(data['artifacts'][0]))
  self.assertTrue(any('duplicate inventory paths' in e for e in self.validate(data)))
 def test_external_artifact_falsely_marked_present_fails(self):
  data=self.mutate_entry(lambda x:x['actual_format']=='unavailable in Git',completeness='present')
  self.assertTrue(any('falsely represented as committed' in e for e in self.validate(data)))
 def test_fabricated_entry_fails(self):
  data=copy.deepcopy(self.inventory); fake=copy.deepcopy(data['artifacts'][0]); fake['path']='fabricated/evidence.json'; data['artifacts'].append(fake)
  self.assertTrue(any('orphaned or fabricated' in e for e in self.validate(data)))
 def test_changed_hash_fails(self):
  data=self.mutate_entry(lambda x:x['completeness']=='present',sha256='0'*64)
  self.assertTrue(any('hash mismatch' in e for e in self.validate(data)))
 def test_wrong_path_fails(self):
  data=self.mutate_entry(lambda x:x['completeness']=='present',path='renamed/evidence.json')
  errors=self.validate(data); self.assertTrue(any('absent from inventory' in e or 'orphaned' in e for e in errors))
 def test_present_artifact_mislabeled_external_fails(self):
  data=self.mutate_entry(lambda x:x['completeness']=='present',artifact_type='external_source_evidence')
  self.assertTrue(any('mislabeled external-only' in e for e in self.validate(data)))
 def test_external_artifact_missing_from_source_lock_fails(self):
  lock=copy.deepcopy(self.lock); target=lock['files'].pop(); self.assertFalse((mod.CASE/target['path']).exists())
  self.assertTrue(any('orphaned or fabricated' in e for e in self.validate(lock=lock)))
 def test_external_lock_hash_conflict_fails(self):
  data=self.mutate_entry(lambda x:x['actual_format']=='unavailable in Git',sha256='f'*64)
  self.assertTrue(any('external lock hash conflict' in e for e in self.validate(data)))
 def test_external_artifact_identity_conflict_fails(self):
  data=self.mutate_entry(lambda x:x['actual_format']=='unavailable in Git',provenance='wrong artifact')
  self.assertTrue(any('external artifact identity conflict' in e for e in self.validate(data)))

class TimelineReconciliationNegativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.run_id='v1.0.0-r1'; cls.timeline=mod.load(mod.FORENSICS/'timelines'/f'{cls.run_id}.json')
  cls.package=mod.load(mod.CASE/'primary-freeze/packages/System-A-r1.json')
  cls.outcome=mod.load(mod.CASE/'post-freeze-reveal/outcome-reveal.json')['outcomes'][cls.run_id]
 def errors(self,key,value):
  data=copy.deepcopy(self.timeline)
  if key in ('run_id','agent_version','outcome'): data[key]=value
  else: data['authoritative_facts'][key]=value
  return mod.validate_timeline_facts(data,self.run_id,self.package,self.outcome)
 def assert_mismatch(self,key,value): self.assertTrue(self.errors(key,value),key)
 def test_resolved_outcome_fails(self): self.assert_mismatch('outcome','resolved')
 def test_resolved_boolean_fails(self): self.assert_mismatch('resolved',True)
 def test_call_budget_fails(self): self.assert_mismatch('call_budget_limit',999)
 def test_termination_reason_fails(self): self.assert_mismatch('termination_reason','submitted')
 def test_patch_application_fails(self): self.assert_mismatch('patch_successfully_applied',False)
 def test_grader_result_fails(self): self.assert_mismatch('grader_result',{'required_test_result':'passed'})
 def test_version_fails(self): self.assert_mismatch('agent_version','v1.0.1')
 def test_run_identity_fails(self): self.assert_mismatch('run_id','v1.0.0-r9')
 def test_unknown_replaced_by_unsupported_claim_fails(self): self.assert_mismatch('provider_status','provider caused failure')

class TaxonomyEvidenceNegativeTests(unittest.TestCase):
 def test_patch_design_cannot_be_observed_without_distinguishing_evidence(self):
  taxonomy=mod.load(mod.FORENSICS/'failure-taxonomy.json'); item=next(x for x in taxonomy['categories'] if x['code']=='F')
  self.assertEqual('unknown',item['occurrence']); self.assertIn('cannot be separated',item['direct_evidence'][0])

if __name__=='__main__': unittest.main()
