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
   self.assertIn('pytest.importorskip(',source)
   self.assertLess(source.index('pytest.importorskip('),source.index('from fastapi.testclient import TestClient'))

if __name__=='__main__': unittest.main()
