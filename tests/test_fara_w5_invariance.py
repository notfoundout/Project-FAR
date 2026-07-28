import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location('w5',ROOT/'tools/check_fara_w5_invariance.py'); W5=importlib.util.module_from_spec(S);S.loader.exec_module(W5)
class W5Tests(unittest.TestCase):
 def setUp(self):self.d=W5.load()
 def reject(self,mutator):
  bad=copy.deepcopy(self.d);mutator(bad)
  with self.assertRaises(AssertionError):W5.validate(bad)
 def test_canonical_and_report(self):
  W5.validate(self.d);self.assertEqual(W5.REPORT.read_text(),W5.report(self.d))
 def test_scope_expansion(self):self.reject(lambda d:d['contract'].__setitem__('source_system_class','all possible systems'))
 def test_representation_family_omission(self):self.reject(lambda d:d['representation_families'].pop('logic'))
 def test_missing_dimension(self):self.reject(lambda d:d['cases'][0]['preservation'].pop('historical'))
 def test_invalid_vocabulary(self):self.reject(lambda d:d['cases'][0]['preservation'].__setitem__('semantic','Good'))
 def test_hidden_auxiliary(self):self.reject(lambda d:d['cases'][2].__setitem__('hidden_assumptions',[]))
 def test_omitted_loss(self):self.reject(lambda d:d['cases'][2].__setitem__('losses_ambiguities_failures',[]))
 def test_recovery_claim_contradiction(self):self.reject(lambda d:d['cases'][0].__setitem__('recovery','partial'))
 def test_equivalence_drift(self):self.reject(lambda d:d['contract'].__setitem__('equivalence_criteria','same outputs'))
 def test_circular_definition(self):self.reject(lambda d:d['contract'].__setitem__('equivalence_criteria','equivalent exactly when tested conclusions agree'))
 def test_superficial_reencoding(self):self.reject(lambda d:d['representation_families']['graphs'].__setitem__('not_superficial_reason',''))
 def test_embedded_universal_language(self):self.reject(lambda d:d.__setitem__('strongest_result','universally invariant for every reasoning system'))
 def test_promoted_semantic_invariance(self):self.reject(lambda d:d['claim_levels'].__setitem__('universal_invariance','established'))
 def test_unresolved_changed_to_all_pass(self):
  def m(d):d['cases'][9]['preservation']={x:'Pass' for x in W5.DIMENSIONS};d['cases'][9]['conclusion_agreement']=True
  self.reject(m)
 def test_decoder_smuggled_semantics(self):self.reject(lambda d:d['contract']['forbidden_hidden_machinery'].remove('decoder-held rule or conclusion'))
 def test_replaced_obligation_contents(self):self.reject(lambda d:d.__setitem__('remaining_obligations',['none']))
 def test_exact_recovery_recoverability_contradiction(self):
  def m(d):d['cases'][0]['recovery']='exact';d['cases'][0]['conclusion_agreement']=False
  self.reject(m)
 def test_stale_report(self):
  changed=copy.deepcopy(self.d);changed['strongest_result']='changed'
  self.assertNotEqual(W5.REPORT.read_text(),W5.report(changed))
 def test_duplicate_owner_compact_json(self):
  oldr,olda=W5.ROOT,W5.ARTIFACT
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);ev=root/'theory/evaluation';ev.mkdir(parents=True);canonical=ev/'canonical.json';canonical.write_text('{}');(ev/'compact.json').write_text(json.dumps({'proof_object_id':self.d['proof_object_id']},separators=(',',':')))
   try:
    W5.ROOT,W5.ARTIFACT=root,canonical;self.assertEqual(W5.duplicate_owner_paths(self.d),['theory/evaluation/compact.json'])
   finally:W5.ROOT,W5.ARTIFACT=oldr,olda
if __name__=='__main__':unittest.main()
