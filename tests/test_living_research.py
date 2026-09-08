from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "run_living_research.py"
spec = importlib.util.spec_from_file_location("run_living_research", MODULE_PATH)
assert spec and spec.loader
living = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = living
spec.loader.exec_module(living)

RQ = {"questions": [{"id": "FAR-RQ-003", "exact_question": "Can the quotient be computed?", "current_disposition": "OPEN"}]}
THREATS = {"threats": [{"id": "THREAT-004"}]}
CONFIG = {
    "schema_version": "1.0",
    "program_id": "FAR-LIVING-RESEARCH-001",
    "authority_boundary": living.AUTHORITY_BOUNDARY,
    "source": {
        "provider": "Crossref REST API",
        "endpoint": "https://api.crossref.org/works",
        "rows_per_query": 8,
        "initial_lookback_days": 14,
        "overlap_days": 2,
        "timeout_seconds": 1,
        "max_retries": 0,
        "user_agent": "test"
    },
    "threat_guards": ["THREAT-004"],
    "attention_terms": ["counterexample"],
    "targets": [{
        "target_id": "FAR-RQ-003",
        "allowed_dispositions": ["OPEN"],
        "candidate_relation": "COMPUTABILITY_OR_OBSTRUCTION_CANDIDATE",
        "queries": ["observational quotient"],
        "signal_terms": ["observational", "quotient"],
        "min_signal_hits": 1,
        "max_candidates_per_query": 3
    }]
}


class LivingResearchTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for relative, value in ((living.CONFIG_PATH, CONFIG), (living.RQ_PATH, RQ), (living.THREAT_PATH, THREATS)):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value), encoding="utf-8")
        return root

    def test_source_identity_is_stable_and_case_insensitive_for_doi(self):
        a = {"DOI": "10.1000/ABC", "title": ["One"]}
        b = {"DOI": "10.1000/abc", "title": ["Changed metadata"]}
        self.assertEqual(living._source_key(a), "doi:10.1000/abc")
        self.assertEqual(living._candidate_id(living._source_key(a)), living._candidate_id(living._source_key(b)))

    def test_binding_validation_fails_on_unknown_governed_target(self):
        bad = json.loads(json.dumps(CONFIG))
        bad["targets"][0]["target_id"] = "FAR-RQ-999"
        with self.assertRaises(living.LivingResearchError):
            living.validate_bindings(bad, RQ, THREATS)

    def test_binding_validation_fails_when_question_is_no_longer_watched(self):
        changed = json.loads(json.dumps(RQ))
        changed["questions"][0]["current_disposition"] = "RESOLVED"
        with self.assertRaises(living.LivingResearchError):
            living.validate_bindings(CONFIG, changed, THREATS)

    def test_success_writes_candidate_run_state_and_advances_cursor(self):
        root = self.make_root()
        def transport(url, headers, timeout):
            self.assertIn("from-index-date%3A2026-08-25", url)
            return {"message": {"items": [
                {"DOI": "10.1234/example", "title": ["An observational quotient counterexample"], "author": [{"given": "Ada", "family": "Lovelace"}], "publisher": "Example", "type": "journal-article", "indexed": {"date-time": "2026-09-08T00:00:00Z"}},
                {"DOI": "10.1234/noise", "title": ["Unrelated chemistry result"]}
            ]}}
        now = datetime(2026, 9, 8, 2, 0, tzinfo=timezone.utc)
        report = living.run_once(root, now=now, transport=transport, sleep_fn=lambda _: None)
        self.assertEqual(report["summary"]["status"], "SUCCESS")
        self.assertEqual(report["summary"]["accepted_new"], 1)
        self.assertEqual(report["summary"]["rejected_results"], 1)
        state = living._read_json(root / living.STATE_PATH)
        self.assertEqual(state["source_cursor_utc"], "2026-09-08T02:00:00Z")
        files = list((root / living.CANDIDATE_DIR).glob("*.json"))
        self.assertEqual(len(files), 1)
        candidate = living._read_json(files[0])
        self.assertEqual(candidate["authority"], "Research")
        self.assertFalse(candidate["epistemic_boundary"]["may_change_claim_status"])
        self.assertEqual(candidate["triage"]["attention"], "HIGH")
        self.assertEqual(report["queries"][0]["results"][1]["reason"], "NO_SIGNAL_TERM")

    def test_repeat_discovery_deduplicates_candidate_and_binding(self):
        root = self.make_root()
        def transport(url, headers, timeout):
            return {"message": {"items": [{"DOI": "10.1234/example", "title": ["Observational quotient"]}]}}
        living.run_once(root, now=datetime(2026, 9, 8, 2, 0, tzinfo=timezone.utc), transport=transport, sleep_fn=lambda _: None)
        report = living.run_once(root, now=datetime(2026, 9, 8, 8, 0, tzinfo=timezone.utc), transport=transport, sleep_fn=lambda _: None)
        self.assertEqual(report["summary"]["accepted_new"], 0)
        self.assertEqual(report["summary"]["accepted_seen"], 1)
        candidate = living._read_json(next((root / living.CANDIDATE_DIR).glob("*.json")))
        self.assertEqual(len(candidate["discovery"]["query_bindings"]), 1)
        self.assertEqual(candidate["discovery"]["last_seen_utc"], "2026-09-08T08:00:00Z")

    def test_source_failure_is_preserved_and_cursor_does_not_advance(self):
        root = self.make_root()
        state = {"schema_version": "1.0", "program_id": "FAR-LIVING-RESEARCH-001", "source_cursor_utc": "2026-09-08T00:00:00Z", "last_run_id": "old", "last_run_status": "SUCCESS", "total_unique_candidates": 0, "updated_utc": "2026-09-08T00:00:00Z"}
        path = root / living.STATE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state), encoding="utf-8")
        def transport(url, headers, timeout):
            raise TimeoutError("synthetic timeout")
        report = living.run_once(root, now=datetime(2026, 9, 8, 8, 0, tzinfo=timezone.utc), transport=transport, sleep_fn=lambda _: None)
        self.assertEqual(report["summary"]["status"], "PARTIAL_SOURCE_FAILURE")
        self.assertEqual(report["summary"]["queries_failed"], 1)
        after = living._read_json(root / living.STATE_PATH)
        self.assertEqual(after["source_cursor_utc"], "2026-09-08T00:00:00Z")
        self.assertEqual(report["failures"][0]["error_type"], "TimeoutError")


if __name__ == "__main__":
    unittest.main()
