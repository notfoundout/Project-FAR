from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from typing import Any, Callable
from uuid import uuid4

from .trace_ingest import SEMANTIC_CONVENTION_VERSION, ingest_trace


class InstrumentationError(ValueError):
    """Raised when an application attempts to emit an invalid FAR trace."""


@dataclass(frozen=True, slots=True)
class RecordedNode:
    node_id: str
    kind: str
    statement: str
    attributes: dict[str, Any] = field(default_factory=dict)
    dependency_target: str | None = None
    dependency_relation: str | None = None
    authorization_required: bool = False
    unknown: bool = False


class DecisionSession(AbstractContextManager["DecisionSession"]):
    """Build a disclosed FAR decision trace without inferring missing reasoning."""

    def __init__(
        self,
        decision_id: str,
        decision_type: str,
        policy_version: str,
        decision_root: str,
        proposed_action: dict[str, Any],
        *,
        trace_id: str | None = None,
        span_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.decision_id = _text(decision_id, "decision_id")
        self.decision_type = _text(decision_type, "decision_type")
        self.policy_version = _text(policy_version, "policy_version")
        self.decision_root = _text(decision_root, "decision_root")
        if not isinstance(proposed_action, dict) or not proposed_action:
            raise InstrumentationError("proposed_action must be a non-empty object")
        if any(not isinstance(key, str) or not key for key in proposed_action):
            raise InstrumentationError("proposed_action keys must be non-empty strings")
        self.proposed_action = dict(proposed_action)
        self.trace_id = trace_id or uuid4().hex
        self._span_id_factory = span_id_factory or (lambda: uuid4().hex[:16])
        self._nodes: dict[str, RecordedNode] = {}
        self._declared_unknowns: set[str] = set()
        self._closed = False
        self._trace: dict[str, Any] | None = None

    def __enter__(self) -> "DecisionSession":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is None and not self._closed:
            self.finish()
        return False

    def record_node(
        self,
        node_id: str,
        kind: str,
        statement: str,
        *,
        attributes: dict[str, Any] | None = None,
        supports: str | None = None,
        relation: str = "supports",
        authorization_required: bool = False,
        unknown: bool = False,
    ) -> "DecisionSession":
        self._ensure_open()
        node_id = _text(node_id, "node_id")
        if node_id in self._nodes:
            raise InstrumentationError(f"duplicate node_id {node_id!r}")
        kind = _text(kind, "kind")
        statement = _text(statement, "statement")
        if attributes is not None and not isinstance(attributes, dict):
            raise InstrumentationError("attributes must be an object")
        target = _text(supports, "supports") if supports is not None else None
        dependency_relation = _text(relation, "relation") if target is not None else None
        self._nodes[node_id] = RecordedNode(
            node_id=node_id,
            kind=kind,
            statement=statement,
            attributes=dict(attributes or {}),
            dependency_target=target,
            dependency_relation=dependency_relation,
            authorization_required=bool(authorization_required),
            unknown=bool(unknown),
        )
        return self

    def record_evidence(self, node_id: str, statement: str, **kwargs: Any) -> "DecisionSession":
        return self.record_node(node_id, "evidence", statement, **kwargs)

    def record_rule(self, node_id: str, statement: str, **kwargs: Any) -> "DecisionSession":
        return self.record_node(node_id, "rule", statement, **kwargs)

    def record_conclusion(self, node_id: str, statement: str, **kwargs: Any) -> "DecisionSession":
        return self.record_node(node_id, "conclusion", statement, **kwargs)

    def declare_unknown(self, name: str) -> "DecisionSession":
        self._ensure_open()
        self._declared_unknowns.add(_text(name, "unknown"))
        return self

    def finish(self, *, claim_complete: bool = False) -> dict[str, Any]:
        self._ensure_open()
        self._validate_graph()
        unresolved = sorted(self._declared_unknowns | {n.node_id for n in self._nodes.values() if n.unknown})
        if claim_complete and unresolved:
            raise InstrumentationError(
                "cannot claim a complete trace while unresolved unknowns are disclosed: "
                f"{unresolved}"
            )
        trace = self._build_trace(claimed_completeness=1.0 if claim_complete else None)
        # Round-trip validation is part of finalization: emitted traces must be ingestible.
        ingest_trace(trace)
        self._trace = trace
        self._closed = True
        return trace

    @property
    def trace(self) -> dict[str, Any]:
        if self._trace is None:
            raise InstrumentationError("decision session has not been finalized")
        return self._trace

    def _validate_graph(self) -> None:
        if self.decision_root not in self._nodes:
            raise InstrumentationError(
                f"decision_root {self.decision_root!r} must identify a recorded node"
            )
        missing_targets = sorted(
            node.dependency_target
            for node in self._nodes.values()
            if node.dependency_target is not None and node.dependency_target not in self._nodes
        )
        if missing_targets:
            raise InstrumentationError(f"dependency targets are not recorded: {missing_targets}")

    def _build_trace(self, *, claimed_completeness: float | None) -> dict[str, Any]:
        root_span_id = self._span_id_factory()
        root_attributes: dict[str, Any] = {
            "far.semantic_convention": SEMANTIC_CONVENTION_VERSION,
            "far.decision.root_span": True,
            "far.decision.id": self.decision_id,
            "far.decision.type": self.decision_type,
            "far.policy.version": self.policy_version,
            "far.decision.root": self.decision_root,
        }
        root_attributes.update({f"far.action.{key}": value for key, value in self.proposed_action.items()})
        if self._declared_unknowns:
            root_attributes["far.unknowns"] = sorted(self._declared_unknowns)
        if claimed_completeness is not None:
            root_attributes["far.trace.completeness"] = claimed_completeness

        spans = [
            {
                "trace_id": self.trace_id,
                "span_id": root_span_id,
                "name": "far.decision",
                "attributes": root_attributes,
            }
        ]
        for node in sorted(self._nodes.values(), key=lambda item: item.node_id):
            attrs: dict[str, Any] = {
                "far.semantic_convention": SEMANTIC_CONVENTION_VERSION,
                "far.node.id": node.node_id,
                "far.node.kind": node.kind,
                "far.node.statement": node.statement,
            }
            attrs.update({f"far.node.attribute.{key}": value for key, value in node.attributes.items()})
            if node.dependency_target is not None:
                attrs["far.dependency.target"] = node.dependency_target
                attrs["far.dependency.relation"] = node.dependency_relation
            if node.authorization_required:
                attrs["far.authorization.required"] = True
            if node.unknown:
                attrs["far.node.unknown"] = True
            spans.append(
                {
                    "trace_id": self.trace_id,
                    "span_id": self._span_id_factory(),
                    "parent_span_id": root_span_id,
                    "name": f"far.node.{node.kind}",
                    "attributes": attrs,
                }
            )
        return {"spans": spans}

    def _ensure_open(self) -> None:
        if self._closed:
            raise InstrumentationError("decision session is already finalized")


def decision_session(
    decision_id: str,
    decision_type: str,
    policy_version: str,
    decision_root: str,
    proposed_action: dict[str, Any],
    **kwargs: Any,
) -> DecisionSession:
    return DecisionSession(
        decision_id,
        decision_type,
        policy_version,
        decision_root,
        proposed_action,
        **kwargs,
    )


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InstrumentationError(f"{field_name} must be a non-empty string")
    return value
