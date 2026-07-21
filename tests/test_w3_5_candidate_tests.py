from __future__ import annotations
import json, shutil, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from check_w3_5_candidate_tests import validate
FILES=[
 'theory/evaluation/w3-5-candidate-test-contract-v1.0.json',
 'theory/evaluation/w3-5-candidate-test-result-v1.0.json',
 'theory/evaluation/universal-structure-candidate-registry.json',
 'theory/evaluation/w3-5-specificity-and-discovery-gate.json']
class CandidateTests(unittest.TestCase):
    def test_corrected_boundary_passes(self):
        report=validate(ROOT)
        self.assertEqual(report['candidates'],12)
        self.assertEqual(report['atomic_trials_preserved'],0)
        self.assertEqual(report['aggregate_result'],'candidate_structural_indispensability_unresolved_reexecution_required')
    def mutated_root(self,path,mutator,rehash_contract=False,rehash_result=False):
        td=tempfile.TemporaryDirectory(); root=Path(td.name)
        for rel in FILES:
            dst=root/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dst)
        target=root/path; data=json.loads(target.read_text()); mutator(data); target.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
        return td,root
    def assert_rejected(self,path,mutator):
        td,root=self.mutated_root(path,mutator)
        try:
            with self.assertRaises(ValueError): validate(root)
        finally: td.cleanup()
    def test_rejects_structural_nonnecessity_promotion_without_trials(self):
        self.assert_rejected(FILES[1],lambda d:d['results'][0].update(structural_commitment_necessity='refuted_at_registered_scope'))
    def test_rejects_summary_records_counted_as_trials(self):
        self.assert_rejected(FILES[1],lambda d:d['execution'].update(preserved_atomic_trials=12))
    def test_rejects_missing_evidence_marked_complete(self):
        self.assert_rejected(FILES[1],lambda d:d['execution'].update(ablation_evidence_complete=True))
    def test_rejects_hard_coded_terminal_answers_in_contract(self):
        self.assert_rejected(FILES[0],lambda d:d.update(registered_terminal_classification='derivable'))
    def test_rejects_w5_authorization(self):
        self.assert_rejected(FILES[3],lambda d:d.update(w5_authorized=True))
    def test_rejects_registry_result_disagreement(self):
        self.assert_rejected(FILES[2],lambda d:d['candidates'][1].update(structural_commitment_necessity='refuted_at_registered_scope'))
    def test_rejects_registry_digest_drift(self):
        self.assert_rejected(FILES[2],lambda d:d['result_artifact'].update(content_sha256='0'*64))
if __name__=='__main__': unittest.main()
