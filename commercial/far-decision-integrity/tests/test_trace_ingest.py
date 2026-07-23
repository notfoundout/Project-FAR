from __future__ import annotations

import copy
import json
import math
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.trace_cli import main
from far_decision_integrity.trace_ingest import TraceIngestionError, ingest_trace, package_payload


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
                    "far.trace.completeness": 0.8,
                },
            },
            {
                "trace_id": "trace-1",
                "span_id": "payment",
                "parent_span_id": "root",
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
                "parent_span_id": "root",
                "attributes": {
                    "far.node.id": "approve-refund",
                    "far.node.kind": "conclusion",
                    "far.node.statement": "Approve the refund.",
                },
            },
        ]
    }


def as_otlp(trace: dict) -> dict:
    otlp_spans = []
    for span in trace["spans"]:
        attrs = []
        for key, value in span["attributes"].items():
            if isinstance(value, bool):
                wrapped = {"boolValue": value}
            elif isinstance(value, (int, float)):
                wrapped = {"doubleValue": value}
            elif isinstance(value, list):
                wrapped = {
                    "arrayValue": {
                        "values": [{"stringValue": item} for item in value]
                    }
                }
            else:
                wrapped = {"stringValue": value}
            attrs.append({"key": key, "value": wrapped})
        otlp_span = {
            "traceId": span["trace_id"],
            "spanId": span["span_id"],
            "attributes": attrs,
        }
        if "parent_span_id" in span:
            otlp_span["parentSpanId"] = span["parent_span_id"]
        otlp_spans.append(otlp_span)
    return {"resourceSpans": [{"scopeSpans": [{"spans": otlp_spans}]}]}


class TestTraceIngestion(unittest.TestCase):
    def test_flat_far_semantic_convention_trace_normalizes(self):
        package = ingest_trace(flat_trace())
        self.assertEqual(package.decision_id, "refund-1")
        self.assertEqual(package.metadata["source_format"], "flat-json+far-semconv")
        self.assertEqual(package.authorization_requirements, ("payment-confirmed",))
        self.assertEqual(package.trace_completeness, 1.0)
        self.assertEqual(package.metadata["producer_claimed_completeness"], 0.8)
        self.assertFalse(package.metadata["semantic_completeness_verified"])
        payment = next(node for node in package.nodes if node.node_id == "payment-confirmed")
        self.assertEqual(payment.attributes["_far_source"]["span_id"], "payment")

    def test_otlp_attribute_arrays_normalize(self):
        package = ingest_trace(as_otlp(flat_trace()))
        self.assertEqual(package.metadata["source_format"], "otlp-json+far-semconv")
        topology = {item["span_id"]: item for item in package.metadata["execution_topology"]}
        self.assertEqual(topology["payment"]["parent_span_id"], "root")

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

    def test_foreign_far_span_is_rejected(self):
        trace = flat_trace()
        trace["spans"][1]["trace_id"] = "trace-2"
        with self.assertRaisesRegex(TraceIngestionError, "foreign span ids"):
            ingest_trace(trace)

    def test_unrelated_foreign_non_far_span_is_ignored_but_counted(self):
        trace = flat_trace()
        trace["spans"].append(
            {"trace_id": "trace-other", "span_id": "noise", "attributes": {"http.status_code": 200}}
        )
        package = ingest_trace(trace)
        self.assertEqual(package.metadata["source_span_count"], 3)
        self.assertEqual(package.metadata["input_span_count"], 4)

    def test_missing_trace_id_is_rejected(self):
        trace = flat_trace()
        del trace["spans"][1]["trace_id"]
        with self.assertRaisesRegex(TraceIngestionError, "trace id"):
            ingest_trace(trace)

    def test_missing_span_id_is_rejected(self):
        trace = flat_trace()
        del trace["spans"][1]["span_id"]
        with self.assertRaisesRegex(TraceIngestionError, "span id"):
            ingest_trace(trace)

    def test_duplicate_span_identity_is_rejected(self):
        trace = flat_trace()
        trace["spans"].append(copy.deepcopy(trace["spans"][1]))
        with self.assertRaisesRegex(TraceIngestionError, "duplicate trace/span identities"):
            ingest_trace(trace)

    def test_duplicate_node_id_is_rejected_by_package_contract(self):
        trace = flat_trace()
        trace["spans"][2]["attributes"]["far.node.id"] = "payment-confirmed"
        trace["spans"][0]["attributes"]["far.decision.root"] = "payment-confirmed"
        with self.assertRaisesRegex(TraceIngestionError, "duplicate node_id"):
            ingest_trace(trace)

    def test_dependency_target_must_exist(self):
        trace = flat_trace()
        trace["spans"][1]["attributes"]["far.dependency.target"] = "missing"
        with self.assertRaisesRegex(TraceIngestionError, "dependency target"):
            ingest_trace(trace)

    def test_completeness_out_of_range_is_rejected(self):
        for value in (-0.1, 1.1, math.inf, math.nan):
            with self.subTest(value=value):
                trace = flat_trace()
                trace["spans"][0]["attributes"]["far.trace.completeness"] = value
                with self.assertRaisesRegex(TraceIngestionError, "finite and between"):
                    ingest_trace(trace)

    def test_duplicate_otlp_attribute_is_rejected(self):
        payload = as_otlp(flat_trace())
        attrs = payload["resourceSpans"][0]["scopeSpans"][0]["spans"][0]["attributes"]
        attrs.append(copy.deepcopy(attrs[0]))
        with self.assertRaisesRegex(TraceIngestionError, "duplicate attribute"):
            ingest_trace(payload)

    def test_output_graph_is_deterministic_under_span_reordering(self):
        first = package_payload(ingest_trace(flat_trace()))
        trace = flat_trace()
        trace["spans"].reverse()
        second = package_payload(ingest_trace(trace))
        self.assertEqual(first["nodes"], second["nodes"])
        self.assertEqual(first["dependencies"], second["dependencies"])
        self.assertEqual(
            first["metadata"]["execution_topology"],
            second["metadata"]["execution_topology"],
        )

    def test_source_payload_digest_changes_when_source_changes(self):
        first = ingest_trace(flat_trace()).metadata["source_payload_sha256"]
        trace = flat_trace()
        trace["spans"][1]["attributes"]["far.node.statement"] = "Payment cleared."
        second = ingest_trace(trace).metadata["source_payload_sha256"]
        self.assertNotEqual(first, second)

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
            self.assertEqual(payload["metadata"]["semantic_convention"], "far-agent-semconv/0.1")

    def test_cli_invalid_trace_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "trace.json"
            output = pathlib.Path(directory) / "package.json"
            source.write_text("{}", encoding="utf-8")
            self.assertEqual(main([str(source), "--output", str(output)]), 40)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
