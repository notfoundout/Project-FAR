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
    def test_inventory_discovers_only_official_frozen_vocabularies(self):
        inv=COMP.discover(); ids=[v['vocabulary_identifier'] for v in inv['vocabularies']]
        self.assertEqual(ids,['CRE-001-VOCAB-A-1.0','CRE-001-VOCAB-B-1.0','CRE-001-VOCAB-C-1.0'])
        self.assertTrue(all(v['eligible_for_cre001_comparison'] for v in inv['vocabularies']))
        self.assertIn('pilot mappings', inv['excluded_classes'])
    def test_source_checksums_match(self):
        for v in COMP.discover()['vocabularies']:
            self.assertEqual(v['source_sha256'], hashlib.sha256((ROOT/v['source_path']).read_bytes()).hexdigest())
    def test_compiler_output_is_deterministic_and_regenerates_committed(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            _,arts1=COMP.generate(Path(a)); _,arts2=COMP.generate(Path(b))
            self.assertEqual(arts1,arts2)
            committed=[json.loads((DET/'generated'/x['vocabulary_identifier']/'compiler-artifact.json').read_text()) for x in COMP.discover()['vocabularies']]
            self.assertEqual(arts1,committed)
    def test_complete_compilation_and_verification(self):
        ref=COMP.model_from_scenario()
        for v in COMP.discover()['vocabularies']:
            art=COMP.compile_entry(v, Path(tempfile.mkdtemp()))
            self.assertEqual(art['compilation_status'],'complete')
            self.assertEqual(VER.verify(ref, art['generated_execution_model'])['result'],'pass')
    def test_partial_compilation_missing_primitive_capability(self):
        v=copy.deepcopy(COMP.discover()['vocabularies'][0]); v['source_path']='theory/evaluation/comparative-representation/experiments/CRE-001/vocabularies/vocabulary-A.md'
        old=COMP.parse_vocab; COMP.parse_vocab=lambda p:{'identifier':'X','primitive_categories':['Object'],'official_definitions':{},'text':''}
        try: self.assertEqual(COMP.compile_entry(v, Path(tempfile.mkdtemp()))['compilation_status'],'partial')
        finally: COMP.parse_vocab=old
    def test_undeclared_or_reference_copying_detection_inputs(self):
        source=(ROOT/'tools/cre001_compile_vocabularies.py').read_text()
        self.assertNotIn("load(REF)", source)
        art=json.loads((DET/'generated/CRE-001-VOCAB-A-1.0/compiler-artifact.json').read_text())
        self.assertIn('compiler', art['provenance']['source'])
        self.assertTrue(art['declared_derived_constructs'])
        self.assertNotIn('preservation_result', art)
    def test_altering_translation_rule_changes_output(self):
        art=json.loads((DET/'generated/CRE-001-VOCAB-A-1.0/compiler-artifact.json').read_text())
        changed=copy.deepcopy(art); changed['translation_rules'][0]='changed rule'
        self.assertNotEqual(art,changed)
    def test_verifier_regressions(self):
        ref=COMP.model_from_scenario(); cand=copy.deepcopy(ref)
        for mut, code in [
            (lambda m: m['transitions'].pop(), 'missing_transition'),
            (lambda m: m['transitions'].append({'name':'T_extra','guard':[],'updates':[]}), 'extra_transition'),
            (lambda m: m['transitions'][0]['guard'].pop(), 'guard_mismatch'),
            (lambda m: m['transitions'][0]['updates'].clear(), 'update_mismatch'),
            (lambda m: m['outputs'].pop('ordered_history'), 'output_mismatch'),
            (lambda m: m['ambiguity_policy'].update({'unterminated_output':'other'}), 'ambiguity_policy_mismatch')]:
            c=copy.deepcopy(cand); mut(c); self.assertIn(code,{d['code'] for d in VER.verify(ref,c)['diagnostics']})
    def test_shortest_counterexample_stability_and_no_scientific_conclusion(self):
        ref=COMP.model_from_scenario(); c=copy.deepcopy(ref); c['terminal_blocks_all_transitions']=False
        r=VER.verify(ref,c); self.assertEqual(r['checks']['operational'],'fail')
        summary=json.loads((DET/'cre001-deterministic-comparison.json').read_text())
        text=json.dumps(summary).lower(); self.assertNotIn(' is necessary', text); self.assertNotIn(' is minimal', text); self.assertIn('does not draw universal sufficiency', text)
    def test_manual_generated_edit_detected(self):
        with tempfile.TemporaryDirectory() as td:
            _,arts=COMP.generate(Path(td)); committed=json.loads((DET/'generated/CRE-001-VOCAB-A-1.0/compiler-artifact.json').read_text())
            edited=copy.deepcopy(committed); edited['assumptions'].append('manual edit')
            self.assertNotEqual(arts[0], edited)
if __name__=='__main__': unittest.main()
