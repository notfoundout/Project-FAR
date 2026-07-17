import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-004"
SPEC = importlib.util.spec_from_file_location("cre004_execution", BASE / "execution.py")
assert SPEC and SPEC.loader
EXECUTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXECUTION)


class CRE004ExecutionTests(unittest.TestCase):
    def response(self, **overrides):
        value = {
            "protocol_version": "CRE-004-v1.0",
            "evaluator_id": "EVAL-001",
            "evaluator_type": "human",
            "case_label": "CASE-001",
            "candidate_label": "CAND-001",
            "source_difference": "yes",
            "translated_difference": "yes",
            "difference_carriers": ["stores_objects"],
            "confidence": "certain",
            "submitted_at": "2026-07-17T12:00:00Z",
        }
        value.update(overrides)
        return value

    def test_manifest_hashes_all_normative_files(self):
        manifest = EXECUTION.protocol_manifest()
        self.assertEqual("CRE-004-v1.0", manifest["protocol_version"])
        self.assertEqual(set(EXECUTION.NORMATIVE_FILES), set(manifest["files"]))
        self.assertTrue(all(len(value) == 64 for value in manifest["files"].values()))

    def test_unknown_hidden_reintroduction_is_not_false(self):
        scored = EXECUTION.score_response(
            self.response(difference_carriers=["other"], other_function="cannot_determine")
        )
        self.assertEqual("unknown", scored["classification"])
        self.assertEqual("unknown", scored["hidden_reintroduction"])

    def test_append_and_replay_are_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            response_path = root / "response.json"
            ledger_path = root / "responses.jsonl"
            response_path.write_text(json.dumps(self.response()), encoding="utf-8")
            record = EXECUTION.append_response(response_path, ledger_path)
            report_a = EXECUTION.aggregate(EXECUTION.read_ledger(ledger_path))
            report_b = EXECUTION.aggregate(EXECUTION.read_ledger(ledger_path))
            self.assertEqual(report_a, report_b)
            self.assertEqual(record["score"]["classification"], "pass")
            self.assertEqual(report_a["active_record_count"], 1)

    def test_duplicate_response_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            response_path = root / "response.json"
            ledger_path = root / "responses.jsonl"
            response_path.write_text(json.dumps(self.response()), encoding="utf-8")
            EXECUTION.append_response(response_path, ledger_path)
            with self.assertRaisesRegex(ValueError, "already recorded"):
                EXECUTION.append_response(response_path, ledger_path)

    def test_supersession_preserves_original_but_excludes_it_from_active_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first_path = root / "first.json"
            second_path = root / "second.json"
            ledger_path = root / "responses.jsonl"
            first_path.write_text(json.dumps(self.response()), encoding="utf-8")
            first = EXECUTION.append_response(first_path, ledger_path)
            corrected = self.response(
                submitted_at="2026-07-17T12:05:00Z",
                translated_difference="no",
                difference_carriers=[],
                supersedes_record_id=first["record_id"],
            )
            second_path.write_text(json.dumps(corrected), encoding="utf-8")
            EXECUTION.append_response(second_path, ledger_path)
            report = EXECUTION.aggregate(EXECUTION.read_ledger(ledger_path))
            self.assertEqual(report["record_count"], 2)
            self.assertEqual(report["active_record_count"], 1)
            self.assertEqual(report["superseded_record_count"], 1)
            self.assertEqual(report["overall"], {"fail": 1})

    def test_tampering_is_detected(self):
        response = self.response()
        manifest = EXECUTION.protocol_manifest()
        record = {
            "record_id": EXECUTION.record_id_for(response, manifest),
            "recorded_at": "2026-07-17T12:00:01Z",
            "protocol_manifest": manifest,
            "response": response,
            "score": EXECUTION.score_response(response),
        }
        record["score"]["classification"] = "fail"
        with self.assertRaisesRegex(ValueError, "does not replay"):
            EXECUTION.verify_records([record])


if __name__ == "__main__":
    unittest.main()
