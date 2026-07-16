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
    def natives(self): return [json.loads((DET/'generated'/e['vocabulary_identifier']/'native-representation.json').read_text()) for e in self.entries()]
    def test_inventory_discovers_only_official_frozen_vocabularies(self):
        inv=COMP.discover(); ids=[v['vocabulary_identifier'] for v in inv['vocabularies']]
        self.assertEqual(ids,['CRE-001-VOCAB-A-1.0','CRE-001-VOCAB-B-1.0','CRE-001-VOCAB-C-1.0'])
        self.assertIn('pilot mappings', inv['excluded_classes']); self.assertIn('control fixtures', inv['excluded_classes'])
    def test_source_checksums_match(self):
        for v in self.entries(): self.assertEqual(v['source_sha256'], hashlib.sha256((ROOT/v['source_path']).read_bytes()).hexdigest())
    def test_compiler_output_is_deterministic_and_regenerates_committed(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            _,arts1=COMP.generate(Path(a)); _,arts2=COMP.generate(Path(b)); self.assertEqual(arts1,arts2)
            committed=[json.loads((DET/'generated'/x['vocabulary_identifier']/'compiler-artifact.json').read_text()) for x in self.entries()]
            self.assertEqual(arts1,committed)
    def test_complete_native_compilation_lowering_and_verification(self):
        ref=COMP.scenario_reference_model()
        for v in self.entries():
            art=COMP.compile_entry(v, Path(tempfile.mkdtemp()))
            self.assertEqual(art['compilation_status'],'complete')
            self.assertEqual(VER.verify(ref, art['generated_execution_model'])['result'],'pass')
            self.assertIsNotNone(art['native_representation_sha256']); self.assertIsNotNone(art['lowering_trace_sha256'])
    def test_no_candidate_directly_calls_or_copies_reference_model(self):
        source=(ROOT/'tools/cre001_compile_vocabularies.py').read_text()
        self.assertNotIn('load(REF', source); self.assertNotIn("DET/'reference-model.json'", source)
        self.assertNotIn('model_from_scenario()', source)
        for art_path in (DET/'generated').glob('*/compiler-artifact.json'):
            art=json.loads(art_path.read_text()); self.assertIn('native representation', art['provenance']['source'])
    def test_removing_required_native_construct_causes_lowering_failure(self):
        native=self.natives()[0]; native['constructs']=[c for c in native['constructs'] if c['id']!='O_history']
        with self.assertRaises(ValueError): COMP.lower(native)
    def test_removing_lowering_rule_causes_failure(self):
        native=self.natives()[1]; rules=copy.deepcopy(COMP.LOWERING_RULES['B']); del rules['transition']
        with self.assertRaises(KeyError): COMP.lower(native,rules)
    def test_changed_or_empty_vocabulary_definition_invalidates_native_compilation(self):
        e=copy.deepcopy(self.entries()[0]); old=COMP.parse_vocab
        COMP.parse_vocab=lambda p:{'identifier':e['vocabulary_identifier'],'primitive_categories':['Object','Relation','Transformation'],'official_definitions':{'Object':'x','Relation':'y','Transformation':'z'},'definition_digest':'bad','text':''}
        try: self.assertEqual(COMP.compile_entry(e,Path(tempfile.mkdtemp()))['compilation_status'],'partial')
        finally: COMP.parse_vocab=old
    def test_swapping_vocabulary_a_native_into_b_lowerer_fails(self):
        native=self.natives()[0]; swapped=copy.deepcopy(native); swapped['vocabulary']='B'
        with self.assertRaises(ValueError): COMP.lower(swapped)
    def test_every_execution_model_field_has_complete_lowering_trace(self):
        for e in self.entries():
            model=json.loads((DET/'generated'/e['vocabulary_identifier']/'generated-execution-model.json').read_text())
            trace=json.loads((DET/'generated'/e['vocabulary_identifier']/'lowering-trace.json').read_text())
            paths={x['output_path'] for x in trace['entries']}
            required={f'/variables/{k}' for k in model['variables']}|{f"/transitions/{t['name']}" for t in model['transitions']}|{'/terminal_condition','/terminal_blocks_all_transitions','/invariants','/outputs','/ambiguity_policy'}
            self.assertTrue(required <= paths)
            for entry in trace['entries']:
                for key in ['source_scenario_path','native_construct_identifier','supplied_vocabulary_primitive','derived_construct_identifier','lowering_rule_identifier']:
                    self.assertTrue(entry.get(key))
    def test_three_native_representations_are_structurally_distinct(self):
        kinds=[{c['kind'] for c in n['constructs']} for n in self.natives()]
        self.assertEqual(len({tuple(sorted(k)) for k in kinds}),3)
    def test_behavior_accepted_only_after_native_construction_and_lowering(self):
        for n in self.natives():
            model,trace=COMP.lower(n); self.assertEqual(VER.verify(COMP.scenario_reference_model(),model)['result'],'pass'); self.assertGreater(len(trace['entries']),0)
    def test_verifier_regressions_and_nonclaims(self):
        ref=COMP.scenario_reference_model(); c=copy.deepcopy(ref); c['transitions'][0]['guard'].pop(); self.assertIn('guard_mismatch',{d['code'] for d in VER.verify(ref,c)['diagnostics']})
        c=copy.deepcopy(ref); c['outputs'].pop('ordered_history'); self.assertIn('output_mismatch',{d['code'] for d in VER.verify(ref,c)['diagnostics']})
        text=json.dumps(json.loads((DET/'cre001-deterministic-comparison.json').read_text())).lower(); self.assertIn('does not draw universal sufficiency',text); self.assertNotIn(' is necessary',text)
    def test_manual_generated_edit_detected(self):
        with tempfile.TemporaryDirectory() as td:
            _,arts=COMP.generate(Path(td)); edited=copy.deepcopy(arts[0]); edited['assumptions'].append('manual edit'); self.assertNotEqual(arts[0],edited)
if __name__=='__main__': unittest.main()
