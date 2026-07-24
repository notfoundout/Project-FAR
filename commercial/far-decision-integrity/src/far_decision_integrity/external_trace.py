from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .model import DecisionNode, DecisionPackage, Dependency, SCHEMA_VERSION

TRACE_SCHEMA_VERSION = "far-external-trace/0.1"


class ProvenanceKind(str, Enum):
    OBSERVED = "observed"
    MECHANICALLY_DERIVED = "mechanically-derived"
    ANALYST_DECLARED = "analyst-declared"
    INFERRED = "inferred"
    UNVERIFIABLE = "unverifiable"


@dataclass(frozen=True, slots=True)
class SourceLocation:
    artifact: str
    record: str


@dataclass(frozen=True, slots=True)
class ExternalEvent:
    event_id: str
    sequence: int
    actor: str
    event_type: str
    statement: str
    provenance: ProvenanceKind
    source: SourceLocation
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExternalTrace:
    trace_id: str
    source_format: str
    events: tuple[ExternalEvent, ...]
    complete: bool = False

    def validate(self) -> None:
        if not self.trace_id or not self.source_format:
            raise ValueError("trace_id and source_format must be non-empty")
        ids = [event.event_id for event in self.events]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate external event_id")
        sequences = [event.sequence for event in self.events]
        if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
            raise ValueError("external event sequence must be unique and increasing")
        if any(event.sequence < 0 for event in self.events):
            raise ValueError("external event sequence must be non-negative")


def compile_trace(trace: ExternalTrace) -> DecisionPackage:
    trace.validate()
    nodes = [
        DecisionNode(
            node_id=event.event_id,
            kind=event.event_type,
            statement=event.statement,
            attributes={
                **event.attributes,
                "actor": event.actor,
                "provenance": event.provenance.value,
                "source_artifact": event.source.artifact,
                "source_record": event.source.record,
            },
        )
        for event in trace.events
    ]
    root_id = f"{trace.trace_id}:trace-root"
    nodes.append(
        DecisionNode(
            node_id=root_id,
            kind="trace-summary",
            statement="External trace observations compiled for FAR evaluation.",
            attributes={"provenance": ProvenanceKind.MECHANICALLY_DERIVED.value},
        )
    )
    dependencies = tuple(
        Dependency(event.event_id, root_id, "contributes-to") for event in trace.events
    )
    unknowns = () if trace.complete else ("external-trace-completeness-not-established",)
    return DecisionPackage(
        schema_version=SCHEMA_VERSION,
        decision_id=trace.trace_id,
        decision_type="external-agent-trace",
        policy_version="external-trace-observation/0.1",
        decision_root=root_id,
        proposed_action={"kind": "evaluate-external-trace"},
        nodes=tuple(nodes),
        dependencies=dependencies,
        authorization_requirements=(),
        unknowns=unknowns,
        trace_completeness=1.0 if trace.complete else 0.0,
        metadata={
            "external_trace_schema": TRACE_SCHEMA_VERSION,
            "source_format": trace.source_format,
            "event_count": len(trace.events),
            "semantic_completeness_verified": False,
        },
    )
