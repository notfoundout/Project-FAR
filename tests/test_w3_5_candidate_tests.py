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
    def test_frozen_package_passes(self):
        report=validate(ROOT); self.assertEqual(report['candidates'],12)
        self.assertEqual(report['aggregate_result'],'no_registered_candidate_indispensable_within_frozen_class')
    def mutated_root(self,path,mutator):
        td=tempfile.TemporaryDirectory(); root=Path(td.name)
        for rel in FILES:
            dst=root/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/rel,dst)
        target=root/path; data=json.loads(target.read_text()); mutator(data); target.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
        return td,root
    def assert_rejected(self,path,mutator):
        td,root=self.mutated_root(path,mutator)
        try:
            with self.assertRaises(AssertionError): validate(root)
        finally: td.cleanup()
    def test_rejects_indispensability_promotion(self):
        self.assert_rejected(FILES[1],lambda d:d['results'][0].update(classification='indispensable_within_frozen_class'))
    def test_rejects_w5_authorization(self):
        self.assert_rejected(FILES[3],lambda d:d.update(w5_authorized=True))
    def test_rejects_missing_equivalent_reintroduction(self):
        self.assert_rejected(FILES[1],lambda d:d['execution'].update(equivalent_reintroduction_checked=False))
    def test_rejects_registry_result_disagreement(self):
        self.assert_rejected(FILES[2],lambda d:d['candidates'][1].update(current_classification='unresolved'))
if __name__=='__main__': unittest.main()
