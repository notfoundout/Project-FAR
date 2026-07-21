from __future__ import annotations
import copy, hashlib, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'
if str(TOOLS) not in sys.path: sys.path.insert(0,str(TOOLS))
from check_w3_5_corpus_freeze import PATHS, load, validate, validate_data
class W35CorpusFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope=load(ROOT/PATHS['scope']); cls.catalog=load(ROOT/PATHS['catalog']); cls.bundles={}
        for item in cls.catalog['records']: cls.bundles.setdefault(item['bundle_path'],load(ROOT/item['bundle_path']))
        cls.source_records=[cls.bundles[item['bundle_path']]['records'][item['record_index']] for item in cls.catalog['records']]
        cls.bundle_digests={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in cls.bundles}; cls.registries={k:load(ROOT/PATHS[k]) for k in ('positive','contrast','disputed')}; cls.result=load(ROOT/PATHS['result']); cls.w35=load(ROOT/PATHS['w35']); cls.gates=load(ROOT/PATHS['gates']); cls.digests={k:hashlib.sha256((ROOT/PATHS[k]).read_bytes()).hexdigest() for k in ('catalog','positive','contrast','disputed','result')}
    def errors(self,**changes):
        payload={'scope':copy.deepcopy(self.scope),'catalog':copy.deepcopy(self.catalog),'source_records':copy.deepcopy(self.source_records),'registries':copy.deepcopy(self.registries),'result':copy.deepcopy(self.result),'w35':copy.deepcopy(self.w35),'gates':copy.deepcopy(self.gates),'actual_digests':copy.deepcopy(self.digests),'actual_bundle_digests':copy.deepcopy(self.bundle_digests)}; payload.update(changes); return validate_data(**payload)
    def test_frozen_package_passes(self): self.assertEqual(validate(ROOT),[])
    def test_empty_positive_registry_is_rejected(self):
        regs=copy.deepcopy(self.registries); regs['positive']['instances']=[]; self.assertTrue(any('positive registry requires' in x for x in self.errors(registries=regs)))
    def test_candidate_dependent_rationale_is_rejected(self):
        records=copy.deepcopy(self.source_records); records[0]['admission_rationale']='Admitted because FARA supports the expected W3.5 result.'; self.assertTrue(any('candidate-dependent' in x for x in self.errors(source_records=records)))
    def test_digest_mismatch_is_rejected(self):
        d=copy.deepcopy(self.digests); d['catalog']='0'*64; self.assertTrue(any('source catalog digest mismatch' in x for x in self.errors(actual_digests=d)))
    def test_missing_observation_is_rejected(self):
        records=copy.deepcopy(self.source_records); del records[0]['candidate_neutral_observations']['history_and_path_dependence']; self.assertTrue(any('missing observations' in x for x in self.errors(source_records=records)))
    def test_duplicate_instance_is_rejected(self):
        records=copy.deepcopy(self.source_records); records[1]['instance_id']=records[0]['instance_id']; self.assertTrue(any('duplicate instance id' in x for x in self.errors(source_records=records)))
    def test_source_record_digest_mismatch_is_rejected(self):
        d=copy.deepcopy(self.bundle_digests); d[self.catalog['records'][0]['bundle_path']]='0'*64; self.assertTrue(any('source bundle digest mismatch' in x for x in self.errors(actual_bundle_digests=d)))
    def test_status_only_gate_is_rejected(self):
        gates=copy.deepcopy(self.gates); next(g for g in gates['gates'] if g['name']=='reasoning-contrast-corpus-frozen')['evidence']=[]; self.assertTrue(any('gate evidence is incomplete' in x for x in self.errors(gates=gates)))
    def test_candidate_execution_and_w5_promotion_are_rejected(self):
        w=copy.deepcopy(self.w35); w['current_results']['candidate_invariants']='complete'; w['w5_authorized']=True; errors=self.errors(w35=w); self.assertTrue(any('W5 must remain unauthorized' in x for x in errors)); self.assertTrue(any('candidate stage is inconsistent' in x for x in errors))
if __name__=='__main__': unittest.main()
