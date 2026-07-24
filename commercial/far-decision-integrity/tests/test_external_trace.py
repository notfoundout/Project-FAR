from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.external_trace import ProvenanceKind, compile_trace
from far_decision_integrity.external_trace_cli import main
from far_decision_integrity.swe_agent import load_swe_agent_trace


class TestExternalTraceAdapter(unittest.TestCase):
    def test_swe_agent_records_preserve_observed_provenance(self):
        payload = {
            "trajectory": [
                {"role": "assistant", "content": "Inspect the failing test.", "action": "pytest tests/test_x.py"},
                {"observation": "1 failed, 4 passed"},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "case.traj.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            trace = load_swe_agent_trace(source, trace_id="candidate-001")
            self.assertEqual(trace.trace_id, "candidate-001")
            self.assertFalse(trace.complete)
            self.assertEqual(len(trace.events), 3)
            self.assertTrue(all(event.provenance is ProvenanceKind.OBSERVED for event in trace.events))
            self.assertEqual(trace.events[0].source.record, "0")

    def test_compilation_preserves_unknown_completeness(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "trace.json"
            source.write_text(json.dumps([{"content": "Done"}]), encoding="utf-8")
            package = compile_trace(load_swe_agent_trace(source, trace_id="candidate-001"))
            self.assertEqual(package.decision_type, "external-agent-trace")
            self.assertEqual(package.trace_completeness, 0.0)
            self.assertIn("external-trace-completeness-not-established", package.unknowns)
            self.assertFalse(package.metadata["semantic_completeness_verified"])
            package.validate_graph()

    def test_cli_is_deterministic(self):
        payload = [{"role": "assistant", "action": {"command": "pytest"}}, {"observation": "passed"}]
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "trace.json"
            first = root / "first.json"
            second = root / "second.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(main([str(source), "--trace-id", "case", "--output", str(first)]), 0)
            self.assertEqual(main([str(source), "--trace-id", "case", "--output", str(second)]), 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_rejects_missing_record_list(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "bad.json"
            source.write_text(json.dumps({"result": "pass"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "list of records"):
                load_swe_agent_trace(source)


if __name__ == "__main__":
    unittest.main()
