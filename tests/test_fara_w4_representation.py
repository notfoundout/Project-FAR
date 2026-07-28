import copy
import importlib.util
import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("w4", ROOT / "tools/check_fara_w4_representation.py")
W4 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(W4)


class FaraW4RepresentationTests(unittest.TestCase):
    def setUp(self):
        self.data = W4.load()

    def test_canonical_artifact_and_bounded_exhaustion(self):
        W4.validate(self.data)
        W4.exhaustive_injection_check()

    def test_declared_encoder_decoder_round_trip_full_source(self):
        source = {
            "X": [{"id": "s0", "type": "state"}, {"id": "s1", "type": "state"}],
            "R": [{"id": "r1", "premise": "p", "conclusion": "q"}],
            "Sem": [{"symbol": "p", "meaning": "true", "version": 1}],
            "Step": [{"from": "s0", "input": "tick", "to": "s1"}],
            "Obs": ["state", "q"],
            "Hist": [{"seq": 0, "event": "init"}, {"seq": 1, "event": "transition"}],
            "Ext": {"ratio": Fraction(2, 3), "flags": [True]},
        }
        archive = W4.encode_source(source)
        self.assertEqual(source, W4.decode_source(archive))
        self.assertIn('"format":"finite_tagged_archive_v1"', archive)

    def test_generated_report_is_fresh(self):
        self.assertEqual(W4.REPORT.read_text(encoding="utf-8"), W4.report(self.data))

    def test_rejects_incomplete_preservation_vector(self):
        bad = copy.deepcopy(self.data)
        del bad["results"][0]["preservation"]["historical"]
        with self.assertRaises(AssertionError):
            W4.validate(bad)

    def test_rejects_omitted_loss_and_recovery_drift(self):
        bad = copy.deepcopy(self.data)
        bad["results"][2]["claims"]["lossless_representability"] = True
        with self.assertRaises(AssertionError):
            W4.validate(bad)
        bad = copy.deepcopy(self.data)
        bad["results"][2]["claims"]["recoverability"] = True
        with self.assertRaises(AssertionError):
            W4.validate(bad)
        bad = copy.deepcopy(self.data)
        bad["results"][0]["claims"]["recoverability"] = False
        with self.assertRaises(AssertionError):
            W4.validate(bad)

    def test_rejects_hidden_machinery_and_weak_interface_promotion(self):
        bad = copy.deepcopy(self.data)
        bad["results"][8].pop("hidden_detail")
        with self.assertRaises(AssertionError):
            W4.validate(bad)
        bad = copy.deepcopy(self.data)
        bad["results"][6]["claims"]["semantic_equivalence"] = True
        with self.assertRaises(AssertionError):
            W4.validate(bad)

    def test_rejects_compact_json_duplicate_identifier_owner(self):
        original_root, original_artifact = W4.ROOT, W4.ARTIFACT
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            evaluation = temp_root / "theory/evaluation"
            evaluation.mkdir(parents=True)
            canonical = evaluation / "canonical.json"
            canonical.write_text("{}", encoding="utf-8")
            duplicate = evaluation / "compact.json"
            duplicate.write_text(json.dumps({"id": self.data["id"]}, separators=(",", ":")), encoding="utf-8")
            try:
                W4.ROOT = temp_root
                W4.ARTIFACT = canonical
                self.assertIn("theory/evaluation/compact.json", W4.duplicate_owner_paths(self.data))
            finally:
                W4.ROOT, W4.ARTIFACT = original_root, original_artifact

    def test_rejects_global_promotion(self):
        bad = copy.deepcopy(self.data)
        bad["nonclaims"].remove("finite examples prove universal faithfulness")
        with self.assertRaises(AssertionError):
            W4.validate(bad)


if __name__ == "__main__":
    unittest.main()
