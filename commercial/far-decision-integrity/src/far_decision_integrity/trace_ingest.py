from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .model import DecisionPackage, PackageValidationError, SCHEMA_VERSION

TRACE_SCHEMA_VERSION = "far-trace-ingestion/0.1"


class TraceIngestionError(ValueError):
    """Raised when disclosed trace data cannot be normalized safely."""


def load_trace(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TraceIngestionError(f"unable to load trace: {exc}") from exc
    if not isinstance(payload, dict):
        raise TraceIngestionError("trace payload must be a JSON object")
    return payload


def ingest_trace(payload: dict[str, Any]) -> DecisionPackage:
    """Normalize disclosed OpenTelemetry/OpenInference spans into a FAR package.

    The adapter only uses explicit attributes. Missing commitments are preserved as
    unknowns and reduce trace completeness; they are never inferred from span names.
    """
    spans = list(_iter_spans(payload))
    if not spans:
        raise TraceIngestionError("trace contains no spans")

    root = _select_root(spans)
    root_attrs = _attributes(root)
    decision_id = _required_attribute(root_attrs, "far.decision.id")
    decision_type = _required_attribute(root_attrs, "far.decision.type")
    policy_version = _required_attribute(root_attrs, "far.policy.version")
    decision_root = _required_attribute(root_attrs, "far.decision.root")

    action: dict[str, Any] = {}
    for key, value in root_attrs.items():
        if key.startswith("far.action."):
            action[key.removeprefix("far.action.")] = value
    if not action:
        raise TraceIngestionError("root span must disclose at least one far.action.* attribute")

    nodes: list[dict[str, Any]] = []
    dependencies: list[dict[str, str]] = []
    requirements: list[str] = []
    unknowns: list[str] = []
    observed_fields = 0
    expected_fields = 0

    for span in spans:
        attrs = _attributes(span)
        node_id = attrs.get("far.node.id")
        if node_id is None:
            continue
        expected_fields += 3
        kind = attrs.get("far.node.kind")
        statement = attrs.get("far.node.statement")
        observed_fields += sum(value is not None for value in (node_id, kind, statement))
        if not all(isinstance(value, str) and value.strip() for value in (node_id, kind, statement)):
            raise TraceIngestionError(
                f"span {_span_id(span)!r} has incomplete far.node.id/kind/statement attributes"
            )

        node_attributes: dict[str, Any] = {
            key.removeprefix("far.node.attribute."): value
            for key, value in attrs.items()
            if key.startswith("far.node.attribute.")
        }
        nodes.append({
            "node_id": node_id,
            "kind": kind,
            "statement": statement,
            "attributes": node_attributes,
        })

        target = attrs.get("far.dependency.target")
        relation = attrs.get("far.dependency.relation")
        if target is not None or relation is not None:
            expected_fields += 2
            observed_fields += sum(value is not None for value in (target, relation))
            if not all(isinstance(value, str) and value.strip() for value in (target, relation)):
                raise TraceIngestionError(
                    f"span {_span_id(span)!r} has incomplete dependency attributes"
                )
            dependencies.append({"source_id": node_id, "target_id": target, "relation": relation})

        if attrs.get("far.authorization.required") is True:
            requirements.append(node_id)
        if attrs.get("far.node.unknown") is True:
            unknowns.append(node_id)

    if not nodes:
        raise TraceIngestionError("trace contains no spans with far.node.id attributes")

    declared_unknowns = root_attrs.get("far.unknowns", [])
    if isinstance(declared_unknowns, str):
        declared_unknowns = [item.strip() for item in declared_unknowns.split(",") if item.strip()]
    if not isinstance(declared_unknowns, list) or any(not isinstance(item, str) for item in declared_unknowns):
        raise TraceIngestionError("far.unknowns must be an array of strings or comma-separated string")
    unknowns.extend(declared_unknowns)

    explicit_completeness = root_attrs.get("far.trace.completeness")
    if explicit_completeness is None:
        trace_completeness = observed_fields / expected_fields if expected_fields else 0.0
    elif isinstance(explicit_completeness, bool) or not isinstance(explicit_completeness, (int, float)):
        raise TraceIngestionError("far.trace.completeness must be numeric")
    else:
        trace_completeness = float(explicit_completeness)

    package_payload = {
        "schema_version": SCHEMA_VERSION,
        "decision_id": decision_id,
        "decision_type": decision_type,
        "policy_version": policy_version,
        "decision_root": decision_root,
        "proposed_action": action,
        "nodes": sorted(nodes, key=lambda item: item["node_id"]),
        "dependencies": sorted(
            dependencies,
            key=lambda item: (item["target_id"], item["source_id"], item["relation"]),
        ),
        "authorization_requirements": sorted(set(requirements)),
        "unknowns": sorted(set(unknowns)),
        "trace_completeness": trace_completeness,
        "metadata": {
            "ingestion_schema": TRACE_SCHEMA_VERSION,
            "source_format": _source_format(payload),
            "source_trace_id": _trace_id(root),
            "source_root_span_id": _span_id(root),
            "span_count": len(spans),
        },
    }
    try:
        return DecisionPackage.from_dict(package_payload)
    except PackageValidationError as exc:
        raise TraceIngestionError(f"normalized trace violates FAR package contract: {exc}") from exc


def package_payload(package: DecisionPackage) -> dict[str, Any]:
    return {
        "schema_version": package.schema_version,
        "decision_id": package.decision_id,
        "decision_type": package.decision_type,
        "policy_version": package.policy_version,
        "decision_root": package.decision_root,
        "proposed_action": package.proposed_action,
        "nodes": [
            {
                "node_id": node.node_id,
                "kind": node.kind,
                "statement": node.statement,
                "attributes": node.attributes,
            }
            for node in package.nodes
        ],
        "dependencies": [
            {
                "source_id": dependency.source_id,
                "target_id": dependency.target_id,
                "relation": dependency.relation,
            }
            for dependency in package.dependencies
        ],
        "authorization_requirements": list(package.authorization_requirements),
        "unknowns": list(package.unknowns),
        "trace_completeness": package.trace_completeness,
        "metadata": package.metadata,
    }


def _iter_spans(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
    flat = payload.get("spans")
    if isinstance(flat, list):
        for span in flat:
            if not isinstance(span, dict):
                raise TraceIngestionError("spans must contain only objects")
            yield span
        return

    resource_spans = payload.get("resourceSpans")
    if not isinstance(resource_spans, list):
        raise TraceIngestionError("expected spans or OTLP resourceSpans")
    for resource in resource_spans:
        if not isinstance(resource, dict):
            raise TraceIngestionError("resourceSpans must contain objects")
        scope_spans = resource.get("scopeSpans", resource.get("instrumentationLibrarySpans", []))
        if not isinstance(scope_spans, list):
            raise TraceIngestionError("scopeSpans must be an array")
        for scope in scope_spans:
            if not isinstance(scope, dict) or not isinstance(scope.get("spans"), list):
                raise TraceIngestionError("each scopeSpans entry must contain a spans array")
            for span in scope["spans"]:
                if not isinstance(span, dict):
                    raise TraceIngestionError("OTLP spans must contain only objects")
                yield span


def _attributes(span: dict[str, Any]) -> dict[str, Any]:
    raw = span.get("attributes", {})
    if isinstance(raw, dict):
        return dict(raw)
    if not isinstance(raw, list):
        raise TraceIngestionError(f"span {_span_id(span)!r} attributes must be an object or OTLP array")
    result: dict[str, Any] = {}
    for item in raw:
        if not isinstance(item, dict) or not isinstance(item.get("key"), str):
            raise TraceIngestionError("OTLP attributes must contain key/value objects")
        result[item["key"]] = _otlp_value(item.get("value"))
    return result


def _otlp_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    for key in ("stringValue", "boolValue", "intValue", "doubleValue"):
        if key in value:
            return value[key]
    if "arrayValue" in value:
        values = value["arrayValue"].get("values", [])
        return [_otlp_value(item) for item in values]
    return value


def _select_root(spans: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = [span for span in spans if _attributes(span).get("far.decision.root_span") is True]
    if len(candidates) != 1:
        raise TraceIngestionError(
            "trace must contain exactly one span with far.decision.root_span=true"
        )
    return candidates[0]


def _required_attribute(attributes: dict[str, Any], key: str) -> str:
    value = attributes.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TraceIngestionError(f"root span must disclose non-empty {key}")
    return value


def _span_id(span: dict[str, Any]) -> str:
    value = span.get("spanId", span.get("span_id", "unknown"))
    return str(value)


def _trace_id(span: dict[str, Any]) -> str:
    value = span.get("traceId", span.get("trace_id", "unknown"))
    return str(value)


def _source_format(payload: dict[str, Any]) -> str:
    return "otlp-json" if "resourceSpans" in payload else "openinference-flat-json"
