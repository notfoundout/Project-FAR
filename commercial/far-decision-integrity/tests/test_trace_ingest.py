from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.trace_cli import main
from far_decision_integrity.trace_ingest import TraceIngestionError, ingest_trace


def flat_trace() -> dict:
    return {
        "spans": [
            {
                "trace_id": "trace-1",
                "span_id": "root",
                "attributes": {
                    "far.decision.root_span": True,
                    "far.decision.id": "refund-1",
                    "far.decision.type": "issue_refund",
                    "far.policy.version": "refund-policy/2026-07",
                    "far.decision.root": "approve-refund",
                    "far.action.kind": "financial_action",
                    "far.action.target": "order-1",
                    "far.action.amount": 100,
                    "far.trace.completeness": 1.0,
                },
            },
            {
                "trace_id": "trace-1",
                "span_id": "payment",
                "attributes": {
                    "far.node.id": "payment-confirmed",
                    "far.node.kind": "evidence",
                    "far.node.statement": "Payment is confirmed.",
                    "far.dependency.target": "approve-refund",
                    "far.dependency.relation": "supports",
                    "far.authorization.required": True,
                },
            },
            {
                "trace_id": "trace-1",
                "span_id": "decision",
                "attributes": {
                    "far.node.id": "approve-refund",
                    "far.node.kind": "conclusion",
                    "far.node.statement": "Approve the refund.",
                },
            },
        ]
    }


class TestTraceIngestion(unittest.TestCase):
    def test_flat_openinference_trace_normalizes(self):
        package = ingest_trace(flat_trace())
        self.assertEqual(package.decision_id, "refund-1")
        self.assertEqual(package.metadata["source_format"], "openinference-flat-json")
        self.assertEqual(package.authorization_requirements, ("payment-confirmed",))

    def test_otlp_attribute_arrays_normalize(self):
        trace = flat_trace()
        spans = trace["spans"]
        otlp_spans = []
        for span in spans:
            attrs = []
            for key, value in span["attributes"].items():
                if isinstance(value, bool):
                    wrapped = {"boolValue": value}
                elif isinstance(value, (int, float)):
                    wrapped = {"doubleValue": value}
                else:
                    wrapped = {"stringValue": value}
                attrs.append({"key": key, "value": wrapped})
            otlp_spans.append({"traceId": span["trace_id"], "spanId": span["span_id"], "attributes": attrs})
        package = ingest_trace({"resourceSpans": [{"scopeSpans": [{"spans": otlp_spans}]}]})
        self.assertEqual(package.metadata["source_format"], "otlp-json")

    def test_missing_root_commitment_is_rejected(self):
        trace = flat_trace()
        del trace["spans"][0]["attributes"]["far.policy.version"]
        with self.assertRaisesRegex(TraceIngestionError, "far.policy.version"):
            ingest_trace(trace)

    def test_no_root_marker_is_rejected(self):
        trace = flat_trace()
        trace["spans"][0]["attributes"]["far.decision.root_span"] = False
        with self.assertRaisesRegex(TraceIngestionError, "exactly one"):
            ingest_trace(trace)

    def test_unknowns_are_preserved(self):
        trace = flat_trace()
        trace["spans"][0]["attributes"]["far.unknowns"] = ["delivery-status"]
        package = ingest_trace(trace)
        self.assertEqual(package.unknowns, ("delivery-status",))

    def test_cli_writes_deterministic_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "trace.json"
            output = root / "package.json"
            source.write_text(json.dumps(flat_trace()), encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(output)]), 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "far-decision-package/0.1")
            self.assertEqual(payload["metadata"]["ingestion_schema"], "far-trace-ingestion/0.1")

    def test_cli_invalid_trace_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "trace.json"
            output = pathlib.Path(directory) / "package.json"
            source.write_text("{}", encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(output)]), 40)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
