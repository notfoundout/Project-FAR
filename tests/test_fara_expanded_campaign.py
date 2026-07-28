import copy,json,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import check_fara_expanded_campaign as checker
class ExpandedCampaignTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.spec=json.loads(checker.SPEC.read_text());cls.proof=json.loads(checker.PROOF.read_text())
 def test_fresh_executable_evidence(self):self.assertEqual([],checker.validate(self.spec,self.proof,checker.REPORT.read_text()))
 def test_explicit_expanded_costs(self):
  self.assertEqual(4,self.proof['bounds']['maximum_carrier_size'])
  self.assertEqual([31,66067],[x['interpretations_examined'] for x in self.proof['cost_accounting']['enumeration_axes']])
  self.assertEqual(70,self.proof['cost_accounting']['paired_reduct_models'])
  self.assertEqual(57,self.proof['cost_accounting']['foundation_executions']);self.assertEqual(336,self.proof['cost_accounting']['ablation_executions'])
 def test_external_semantics_remain_unknown(self):self.assertEqual({'oracle':'Unknown','continuous':'Unknown','hybrid':'Unknown','embodied':'Unknown'},self.proof['unknown_cases'])
 def test_all_required_evidence_categories_exist(self):
  f=self.proof['foundation'];self.assertEqual(21,len(f['ablations']));self.assertEqual(12,len(f['round_trip_ledger']));self.assertEqual(57,len(f['results']))
  for key in ('preservation_matrix','structural_accounting','pareto_vectors','pareto_matrix','dominance_graph'):self.assertTrue(f[key])
 def reject_proof(self,mutation):
  p=copy.deepcopy(self.proof);mutation(p);self.assertTrue(checker.validate(self.spec,p,checker.REPORT.read_text()))
 def test_stale_fabricated_incomplete_and_overclaimed_proofs_fail_closed(self):
  mutations=[lambda p:p.__setitem__('spec_digest','0'*64),lambda p:p['countermodels'].pop(),lambda p:p['foundation']['ablations'].pop(),lambda p:p['trace_manifest'].pop(next(iter(p['trace_manifest']))),lambda p:p['unknown_cases'].__setitem__('oracle','Pass'),lambda p:p['conclusions'].__setitem__('pareto','global superiority')]
  for mutation in mutations:self.reject_proof(mutation)
 def test_mutated_trace_directory_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d)
   for k,v in self.proof['trace_manifest'].items():(d/f'{k}.json').write_text(json.dumps(v))
   first=next(d.glob('*.json'));data=json.loads(first.read_text());data['status']='Pass' if data['status']!='Pass' else 'Fail';first.write_text(json.dumps(data))
   self.assertIn('stale or incomplete trace manifest',checker.validate(self.spec,self.proof,checker.REPORT.read_text(),d))
 def test_historical_hash_mutation_fails_closed(self):self.reject_proof(lambda p:p['historical_artifacts'].__setitem__(next(iter(p['historical_artifacts'])),'0'*64))
 def test_report_mutation_fails_closed(self):self.assertIn('stale report',checker.validate(self.spec,self.proof,checker.REPORT.read_text()+'fabricated'))
if __name__=='__main__':unittest.main()
