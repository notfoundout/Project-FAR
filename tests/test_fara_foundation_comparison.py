import copy,importlib,json,pathlib,subprocess,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'tools'))
import check_fara_foundation_comparison as checker
class FoundationComparisonTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.spec=json.loads(checker.SPEC.read_text()); cls.proof=json.loads(checker.PROOF.read_text())
 def rejected(self,mutator,proof=False):
  s=copy.deepcopy(self.spec); p=copy.deepcopy(self.proof); mutator(p if proof else s)
  self.assertTrue(checker.validate(s,p),"mutation was accepted")
 def test_fresh_build_and_report_are_exact(self):
  self.assertEqual(self.proof,checker.build(self.spec)); self.assertEqual(checker.REPORT.read_text(),checker.render(self.spec,self.proof))
 def test_three_modules_execute_independently(self):
  modules=[importlib.import_module(f['module']) for f in self.spec['foundations']]
  self.assertEqual(3,len({pathlib.Path(m.__file__).read_bytes() for m in modules}))
  self.assertFalse(any('many_sorted' in pathlib.Path(m.__file__).read_text() for m in modules[1:]))
 def test_all_traces_and_json_artifacts(self):
  self.assertEqual(57,len(self.proof['traces'])); self.assertEqual(57,len(list(checker.TRACE_DIR.glob('*.json'))))
  for p in [checker.SPEC,checker.PROOF,*checker.TRACE_DIR.glob('*.json')]: json.loads(p.read_text())
 def test_roundtrips_witnesses_ablations_and_pareto(self):
  self.assertEqual(12,len(self.proof['round_trip_ledger'])); self.assertEqual(3,len(self.proof['non_equivalence_witnesses'])); self.assertEqual(21,len(self.proof['ablations'])); self.assertFalse(any(v for row in self.proof['pareto_matrix'].values() for v in row.values()))
 def test_unknown_is_not_promoted(self): self.assertTrue(all(r['status']=='Unknown' for r in self.proof['results'] if r['benchmark'] in ('BFC-017','BFC-018','BFC-019')))
 def test_foundation_executors(self):
  cases=[('many_sorted',{'states':['s0'],'relations':{'applies':[['r','s0','s1']]}}),('typed_hypergraph',{'nodes':{'r':'rule','s0':'state','s1':'state'},'active_states':['s0'],'edges':[{'id':'e','type':'applies','ends':['r','s0','s1']}]}),('algebraic_state',{'initial_state':'s0','program':['f'],'operations':{'f':{'domain':['s0'],'mapping':{'s0':'s1'}}},'composition':{}})]
  for name,model in cases:
   m=importlib.import_module('theory.foundation.fara_foundation_comparison.'+name); self.assertEqual('Pass',m.execute(model)['status'])
 def test_spec_mutations_fail_closed(self):
  mutations=[
   lambda s:s['foundations'][0]['sorts'].append('Undeclared'),lambda s:s['foundations'][0]['native_symbols'].append('bad'),lambda s:s['foundations'][0].pop('admissible_models'),lambda s:s['foundations'].__setitem__(1,{**s['foundations'][1],'module':s['foundations'][0]['module']}),lambda s:s['benchmarks'].pop(),lambda s:s['preservation_dimensions'].pop(),lambda s:s.__setitem__('weights',[1]),lambda s:s['campaign']['pr421_artifact_hashes'].__setitem__('proof','0'*40),lambda s:s['nonclaims'].pop(),lambda s:s['remaining_obligations'].pop(),lambda s:s['benchmarks'][1].__setitem__('id',s['benchmarks'][0]['id']),lambda s:s['foundations'][0].__setitem__('arbitrary_payload_renamed','opaque semantic blob'),lambda s:s['foundations'][1].__setitem__('decoding_service','hidden_decoder'),lambda s:s['comparison_dimensions'].pop(),lambda s:s['terminal_vocabulary'].pop(),lambda s:s['benchmarks'][0].__setitem__('expected_answer','Pass')]
  for mutation in mutations: self.rejected(mutation)
 def test_proof_mutations_fail_closed(self):
  mutations=[lambda p:p['results'][0].__setitem__('status','Fail'),lambda p:p['traces'][next(iter(p['traces']))]['execution_steps'].pop(),lambda p:p['traces'][next(iter(p['traces']))]['correspondence_map'].clear(),lambda p:p['traces'][next(iter(p['traces']))]['recovered_commitments'].clear(),lambda p:p['results'][0].__setitem__('commitment_equivalent',True),lambda p:p['non_equivalence_witnesses'].pop(),lambda p:p['non_equivalence_witnesses'][0].pop('models'),lambda p:p['structural_accounting']['many-sorted-relational']['aggregate'].__setitem__('native',0),lambda p:p['results'][-1].__setitem__('status','Pass'),lambda p:p['pareto_matrix']['many-sorted-relational'].__setitem__('typed-hypergraph',True),lambda p:p['ablations'].pop(),lambda p:p['counterexamples'].pop()]
  for mutation in mutations:self.rejected(mutation,proof=True)
 def test_human_and_generated_reports_are_distinct(self): self.assertNotEqual((ROOT/'docs/research/fara-foundation-comparison-v1.0.md').read_text(),checker.REPORT.read_text())
if __name__=='__main__': unittest.main()
