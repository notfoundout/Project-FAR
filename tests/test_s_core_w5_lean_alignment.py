from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SCoreW5LeanAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lean=(ROOT/'mechanization/lean/SCoreW5.lean').read_text(encoding='utf-8')
        cls.registry=json.loads((ROOT/'theory/evaluation/s-core-w5-lean-mechanization.json').read_text(encoding='utf-8'))
        cls.w5=json.loads((ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json').read_text(encoding='utf-8'))
    def test_registered_theorems_exist(self):
        for theorem in self.registry['compiled_theorems'].values():
            self.assertIn(theorem.rsplit('.',1)[-1],self.lean)
    def test_no_admissions_or_axioms(self):
        lowered=self.lean.lower()
        self.assertNotIn('sorry',lowered)
        self.assertNotIn('admit',lowered)
        self.assertNotIn('\naxiom ',lowered)
    def test_scope_and_predicate_match_w5(self):
        self.assertEqual(self.registry['source_scope'],self.w5['source_scope'])
        self.assertEqual(self.registry['faithful_predicate'],self.w5['faithful_predicate'])
        self.assertEqual(self.registry['claim_effect']['S_IRD_representation'],self.w5['claim_effect']['S_IRD_representation'])
    def test_bounded_claim_is_machine_checked_without_universal_promotion(self):
        self.assertEqual(self.registry['claim_effect']['bounded_faithful_representation'],'machine_checked')
        self.assertEqual(self.registry['claim_effect']['universal_structure'],'unresolved')
        self.assertEqual(self.registry['claim_effect']['independent_proof_review'],'not_started')
    def test_all_three_assembly_obligations_are_mapped(self):
        mapped=self.registry['compiled_theorems']
        self.assertTrue(all(key in mapped for key in ('ASM-SC-001','ASM-SC-002','ASM-SC-003')))
if __name__=='__main__': unittest.main()
