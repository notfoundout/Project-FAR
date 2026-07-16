from __future__ import annotations
import copy, hashlib, importlib.util, json, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m
COMP=loadmod('cre001_compile_vocabularies', ROOT/'tools/cre001_compile_vocabularies.py')
VER=loadmod('cre001_verifier', ROOT/'tools/cre001_verifier.py')
DET=ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001/deterministic-verifier'
class Cre001ComparisonTests(unittest.TestCase):
    def entries(self): return COMP.discover()['vocabularies']
    def native(self, i=0): return json.loads((DET/'generated'/self.entries()[i]['vocabulary_identifier']/'native-representation.json').read_text())
    def all_natives(self): return [self.native(i) for i in range(3)]
    def test_inventory_discovers_only_official_frozen_vocabularies(self):
        inv=COMP.discover(); self.assertEqual([v['vocabulary_identifier'] for v in inv['vocabularies']],['CRE-001-VOCAB-A-1.0','CRE-001-VOCAB-B-1.0','CRE-001-VOCAB-C-1.0']); self.assertIn('pilot mappings',inv['excluded_classes']); self.assertIn('control fixtures',inv['excluded_classes'])
    def test_source_checksums_match(self):
        for v in self.entries(): self.assertEqual(v['source_sha256'], hashlib.sha256((ROOT/v['source_path']).read_bytes()).hexdigest())
    def test_deterministic_regeneration_matches_committed(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            _,arts1=COMP.generate(Path(a)); _,arts2=COMP.generate(Path(b)); self.assertEqual(arts1,arts2)
            committed=[json.loads((DET/'generated'/x['vocabulary_identifier']/'compiler-artifact.json').read_text()) for x in self.entries()]
            self.assertEqual(arts1,committed)
    def test_candidate_compilers_do_not_call_reference_or_prebuilt_transition_helpers(self):
        src=(ROOT/'tools/cre001_compile_vocabularies.py').read_text(); self.assertNotIn('transition_specs',src); self.assertNotIn('assemble_execution_model',src); self.assertNotIn("DET/'reference-model.json'",src)
        for art_path in (DET/'generated').glob('*/compiler-artifact.json'): self.assertIn('atomic native records',json.loads(art_path.read_text())['provenance']['source'])
    def test_native_artifacts_contain_no_ready_made_common_model_fragments(self):
        forbidden={'transition','guard','guard_any','updates','outputs','invariants','ambiguity_policy','variables'}
        for native in self.all_natives():
            def walk(x):
                if isinstance(x,dict):
                    self.assertTrue(forbidden.isdisjoint(x.keys())); [walk(v) for v in x.values()]
                elif isinstance(x,list): [walk(v) for v in x]
            walk(native)
    def test_complete_atomic_lowering_and_verification(self):
        ref=COMP.reference_model()
        for v in self.entries():
            art=COMP.compile_entry(v,Path(tempfile.mkdtemp())); self.assertEqual(art['compilation_status'],'complete'); self.assertTrue(art['definition_capability_validation_passed']); self.assertTrue(art['atomic_lowering_complete']); self.assertFalse(art['shared_semantic_defaults_used']); self.assertTrue(art['mutation_sensitivity_passed']); self.assertEqual(VER.verify(ref,art['generated_execution_model'])['result'],'pass')
    def test_missing_atomic_guard_update_terminal_output_ambiguity_failures(self):
        removals=[('guard_all_condition','missing atomic precondition'),('atomic_update','missing atomic update'),('terminal_blocking','terminal blocking'),('output','output'),('ambiguity_policy','ambiguity')]
        for role,_ in removals:
            n=self.native(); c=next(x for x in n['constructs'] if x['role']==role); n['constructs'].remove(c)
            with self.assertRaises(Exception): COMP.lower(n)
    def test_guard_and_update_mutations_change_output_and_fail_verifier(self):
        ref=COMP.reference_model()
        for role,field in [('guard_all_condition','equals'),('atomic_update','value')]:
            n=self.native(); c=next(x for x in n['constructs'] if x['role']==role and isinstance(x.get(field),bool)); c[field]=not c[field]
            model,_=COMP.lower(n); self.assertNotEqual(VER.verify(ref,model)['result'],'pass')
    def test_swap_a_native_into_b_lowerer_and_definition_contract_fail(self):
        n=self.native(0); rules=COMP.rule_set('B')
        with self.assertRaises(Exception): COMP.lower(n,rules)
        e=copy.deepcopy(self.entries()[0]); old=COMP.parse_vocab; long='x '*100
        COMP.parse_vocab=lambda p:{'identifier':e['vocabulary_identifier'],'primitive_categories':['Object','Relation','Transformation'],'official_definitions':{'Object':long,'Relation':long,'Transformation':long},'definition_digest':'bad','text':long}
        try: self.assertEqual(COMP.compile_entry(e,Path(tempfile.mkdtemp()))['compilation_status'],'partial')
        finally: COMP.parse_vocab=old
    def test_lowering_rule_removal_and_semantic_mutation_detected(self):
        n=self.native(); rules=COMP.rule_set('A'); del rules['condition']
        with self.assertRaises(KeyError): COMP.lower(n,rules)
        rules=COMP.rule_set('A'); old=rules['effect']; rules['effect']=COMP.LoweringRule(old.rule_id,old.accepted_kinds,old.primitive,old.required_fields,old.output_type,lambda c:{'variable':c['variable'],'operation':c['operation'],'value':'MUTATED'})
        with self.assertRaises(Exception): COMP.lower(n,rules)
    def test_every_atomic_common_model_field_has_trace_and_not_generic_container(self):
        for e in self.entries():
            model=json.loads((DET/'generated'/e['vocabulary_identifier']/'generated-execution-model.json').read_text()); trace=json.loads((DET/'generated'/e['vocabulary_identifier']/'lowering-trace.json').read_text()); paths={x['output_path'] for x in trace['entries']}
            required={f'/variables/{k}' for k in model['variables']}|{f"/transitions/{t['name']}/name" for t in model['transitions']}|{f"/transitions/{t['name']}/guard/{i}" for t in model['transitions'] for i,_ in enumerate(t.get('guard',[]))}|{f"/transitions/{t['name']}/guard_any/{i}" for t in model['transitions'] for i,_ in enumerate(t.get('guard_any',[]))}|{f"/transitions/{t['name']}/updates/{i}" for t in model['transitions'] for i,_ in enumerate(t.get('updates',[]))}|{'/terminal_condition','/terminal_blocks_all_transitions'}|{f'/invariants/{i}' for i,_ in enumerate(model['invariants'])}|{f'/outputs/{k}' for k in model['outputs']}|{f'/ambiguity_policy/{k}' for k in model['ambiguity_policy']}
            self.assertTrue(required<=paths)
            for t in trace['entries']:
                self.assertNotRegex(t['output_path'],r'^/transitions/[^/]+$')
                for k in ['source_scenario_path','native_construct_id','native_construct_kind','supplied_vocabulary_primitive','primitive_definition_sha256','executable_lowering_rule_id','source_native_field','resulting_common_model_value']: self.assertIn(k,t)
    def test_three_native_representations_distinct_and_no_shared_defaults_reported(self):
        kinds=[{c['kind'] for c in n['constructs']} for n in self.all_natives()]; self.assertEqual(len({tuple(sorted(k)) for k in kinds}),3)
        summary=json.loads((DET/'cre001-deterministic-comparison.json').read_text())
        for r in summary['results']: self.assertFalse(r['shared_semantic_defaults_used']); self.assertTrue(r['mutation_sensitivity_passed']); self.assertIn('cre001_conditional_equivalence_demonstrated',r)
    def test_committed_mutation_reports_pass(self):
        for e in self.entries():
            rep=json.loads((DET/'generated'/e['vocabulary_identifier']/'mutation-test-report.json').read_text()); self.assertTrue(rep['passed']); self.assertGreaterEqual(len(rep['cases']),11); self.assertTrue(all(c['detected'] for c in rep['cases']))
if __name__=='__main__': unittest.main()
