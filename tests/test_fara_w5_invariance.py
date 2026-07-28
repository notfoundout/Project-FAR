import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w5",ROOT/"tools/check_fara_w5_invariance.py")
W5=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(W5)

class FaraW5InvarianceTests(unittest.TestCase):
    def setUp(self):
        self.data=W5.load()

    def test_canonical_execution(self):
        W5.validate(self.data)
        for case in self.data["cases"]:
            self.assertEqual(case["preservation"],W5.adjudicate(case)["preservation"])

    def test_only_admissible_pairs_support_invariance(self):
        positives=[c for c in self.data["cases"] if c["admissible_pair"]]
        self.assertEqual(["W5-FIX-001","W5-FIX-002"],[c["id"] for c in positives])
        self.assertTrue(all(c["conclusion_agreement"] is True for c in positives))
        self.assertFalse(any(c["classification"]=="inadmissible_boundary" and c["conclusion_agreement"] is False for c in self.data["cases"]))

    def test_rejects_counterexample_promotion(self):
        bad=copy.deepcopy(self.data)
        bad["terminal_result"]="explicit representation-sensitive counterexample"
        bad["status"]=bad["terminal_result"]
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_lossy_pair_as_admissible(self):
        bad=copy.deepcopy(self.data)
        bad["cases"][2]["admissible_pair"]=True
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_declared_labels_not_matching_execution(self):
        bad=copy.deepcopy(self.data)
        bad["cases"][2]["preservation"]["information"]="Pass"
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_recovery_contradiction(self):
        bad=copy.deepcopy(self.data)
        bad["cases"][0]["recovery"]="partial"
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_conclusion_contradiction(self):
        bad=copy.deepcopy(self.data)
        bad["cases"][0]["conclusion_agreement"]=False
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_unavailable_fixture_promoted(self):
        bad=copy.deepcopy(self.data)
        bad["cases"][9]["representation_execution"]["lsts"]["available"]=True
        bad["cases"][9]["representation_execution"]["tables"]["available"]=True
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_missing_family(self):
        bad=copy.deepcopy(self.data); del bad["representation_families"]["logic"]
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_missing_dimension(self):
        bad=copy.deepcopy(self.data); del bad["cases"][0]["source"]["historical"]
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_invalid_status(self):
        bad=copy.deepcopy(self.data); bad["cases"][0]["preservation"]["semantic"]="Maybe"
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_circular_equivalence(self):
        bad=copy.deepcopy(self.data); bad["contract"]["equivalence_criteria"]="equal conclusions"
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_hidden_decoder(self):
        bad=copy.deepcopy(self.data); bad["contract"]["forbidden_hidden_machinery"].remove("decoder-held rule or conclusion")
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_changed_obligations(self):
        bad=copy.deepcopy(self.data); bad["remaining_obligations"][0]="different same-length obligation"
        with self.assertRaises(AssertionError): W5.validate(bad,canonical=False)

    def test_rejects_duplicate_owner_in_compact_json(self):
        original_root,original_artifact=W5.ROOT,W5.ARTIFACT
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); evaluation=root/"theory/evaluation"; evaluation.mkdir(parents=True)
            canonical=evaluation/"canonical.json"; canonical.write_text("{}",encoding="utf-8")
            duplicate=evaluation/"compact.json"; duplicate.write_text(json.dumps({"id":self.data["id"]},separators=(",",":")),encoding="utf-8")
            try:
                W5.ROOT=root; W5.ARTIFACT=canonical
                self.assertIn("theory/evaluation/compact.json",W5.duplicate_owner_paths(self.data))
            finally:
                W5.ROOT,W5.ARTIFACT=original_root,original_artifact

    def test_generated_report_fresh(self):
        self.assertEqual(W5.REPORT.read_text(encoding="utf-8"),W5.report(self.data))

if __name__=="__main__":
    unittest.main()
