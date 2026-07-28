import copy, json, unittest
from tools.check_fara_core_formalization import SPEC, PROOF, REPORT, build_spec, build_proof, closure, execute_family, render, validate

class CoreFormalizationTests(unittest.TestCase):
    def setUp(self):
        self.s=build_spec(); self.p=build_proof(self.s)
    def reject(self, fn, proof=False):
        s=copy.deepcopy(self.s); p=copy.deepcopy(self.p); fn(p if proof else s)
        self.assertTrue(validate(s,p))
    def test_canonical_freshness(self):
        s=json.loads(SPEC.read_text());p=json.loads(PROOF.read_text())
        self.assertEqual([],validate(s,p,REPORT.read_text()))
        self.assertEqual(self.s,s); self.assertEqual(self.p,p)
        self.assertEqual(render(self.s,self.p),REPORT.read_text())
    def test_dependency_closure(self): self.assertIn('Object',closure(self.s['post_dependency_graph'])['SemanticContent'])
    def test_relation_codomain_declared(self): self.assertIn('Relation',self.s['language']['sorts'])
    def test_foundations_formally_typed(self):
        self.assertEqual(3,len(self.p['foundation_checks']))
        self.assertTrue(all(x['typed'] and x['coherent'] for x in self.p['foundation_checks']))
        self.assertEqual(3,len({json.dumps(x['non_equivalence_witness'],sort_keys=True) for x in self.s['foundations']}))
    def test_countermodels_are_paired_reducts(self):
        self.assertEqual(5,len(self.p['countermodels']))
        for c in self.p['countermodels']:
            self.assertTrue(c['verified']); self.assertEqual(c['reduct_a'],c['reduct_b'])
            self.assertNotEqual(c['model_a'][c['target']],c['model_b'][c['target']])
    def test_model_families_execute(self):
        for m in self.p['models']:
            src,result=execute_family(m['family'])
            if src is None: self.assertEqual('Unknown',m['execution'])
            else:
                self.assertEqual('Pass',m['execution']); self.assertEqual(src,m['source_model']); self.assertEqual(result,m['execution_result'])
    def test_undeclared_symbol(self): self.reject(lambda s:s['post_dependency_graph'].__setitem__('Ghost',[]))
    def test_deleted_dependency(self): self.reject(lambda s:s['post_dependency_graph'].__setitem__('Representation',[]))
    def test_cycle(self): self.reject(lambda s:s['post_dependency_graph']['Object'].append('SemanticContent'))
    def test_missing_recursion_base(self): self.reject(lambda s:s['base_cases'].pop())
    def test_object_representation_collapse(self): self.reject(lambda s:s['language']['sorts'].remove('Token'))
    def test_representation_interpretation_collapse(self): self.reject(lambda s:s['definitions'][4].__setitem__('codomain','Token'))
    def test_investigation_calculus_cycle(self): self.reject(lambda s:s['post_dependency_graph']['ReasoningCalculus'].append('Investigation'))
    def test_arbitrary_payload(self): self.reject(lambda s:s['definitions'][2].__setitem__('definition','arbitrary payload'))
    def test_decoder_smuggling(self): self.reject(lambda s:s['definitions'][3].__setitem__('definition','token containing decoder'))
    def test_missing_identity(self): self.reject(lambda s:s['definitions'][0].__setitem__('identity',''))
    def test_undeclared_codomain(self): self.reject(lambda s:s['definitions'][1].__setitem__('codomain','GhostSort'))
    def test_changed_non_derivability(self): self.reject(lambda p:p['w1_re_evaluation'].__setitem__('Object','derivable under the frozen theory'),True)
    def test_invalid_countermodel(self): self.reject(lambda p:p['countermodels'][0].__setitem__('reduct_b',{'changed':True}),True)
    def test_model_execution_drift(self): self.reject(lambda p:p['models'][0]['execution_result'].__setitem__('state',999),True)
    def test_global_promotion(self): self.reject(lambda p:p['w1_re_evaluation'].__setitem__('Object','globally independent'),True)
    def test_false_conservativity(self): self.reject(lambda p:p['conservativity'][0].__setitem__('result','conservative'),True)
    def test_removed_countermodel(self): self.reject(lambda p:p['countermodels'].pop(),True)
    def test_same_length_obligation_mutation(self): self.reject(lambda p:p['remaining_obligations'].__setitem__(0,'x'*len(p['remaining_obligations'][0])),True)
    def test_compact_duplicate_identifier(self): self.reject(lambda p:p.__setitem__('duplicate',{'id':p['id']}),True)
    def test_stale_report(self): self.assertTrue(validate(self.s,self.p,render(self.s,self.p)+'stale'))

if __name__=='__main__':unittest.main()
