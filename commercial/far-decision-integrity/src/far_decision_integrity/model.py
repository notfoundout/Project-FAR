from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

SCHEMA_VERSION = "far-decision-package/0.1"


class IntegrityStatus(str, Enum):
    JUSTIFIED = "justified"
    UNSUPPORTED = "unsupported"
    UNDERDETERMINED = "underdetermined"
    UNVERIFIABLE = "unverifiable"


class PackageValidationError(ValueError):
    """Raised when a decision package violates the versioned contract."""


@dataclass(frozen=True, slots=True)
class DecisionNode:
    node_id: str
    kind: str
    statement: str
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecisionNode":
        return cls(
            node_id=_required_text(data, "node_id"),
            kind=_required_text(data, "kind"),
            statement=_required_text(data, "statement"),
            attributes=_mapping(data.get("attributes", {}), "attributes"),
        )


@dataclass(frozen=True, slots=True)
class Dependency:
    source_id: str
    target_id: str
    relation: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Dependency":
        return cls(
            source_id=_required_text(data, "source_id"),
            target_id=_required_text(data, "target_id"),
            relation=_required_text(data, "relation"),
        )


@dataclass(frozen=True, slots=True)
class DecisionPackage:
    schema_version: str
    decision_id: str
    decision_type: str
    policy_version: str
    decision_root: str
    proposed_action: dict[str, Any]
    nodes: tuple[DecisionNode, ...]
    dependencies: tuple[Dependency, ...]
    authorization_requirements: tuple[str, ...]
    unknowns: tuple[str, ...]
    trace_completeness: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecisionPackage":
        if not isinstance(data, dict):
            raise PackageValidationError("decision package must be a JSON object")

        schema_version = _required_text(data, "schema_version")
        if schema_version != SCHEMA_VERSION:
            raise PackageValidationError(
                f"unsupported schema_version {schema_version!r}; expected {SCHEMA_VERSION!r}"
            )

        raw_nodes = _list(data.get("nodes"), "nodes")
        raw_dependencies = _list(data.get("dependencies"), "dependencies")
        package = cls(
            schema_version=schema_version,
            decision_id=_required_text(data, "decision_id"),
            decision_type=_required_text(data, "decision_type"),
            policy_version=_required_text(data, "policy_version"),
            decision_root=_required_text(data, "decision_root"),
            proposed_action=_mapping(data.get("proposed_action"), "proposed_action"),
            nodes=tuple(DecisionNode.from_dict(_mapping(item, "nodes[]")) for item in raw_nodes),
            dependencies=tuple(
                Dependency.from_dict(_mapping(item, "dependencies[]"))
                for item in raw_dependencies
            ),
            authorization_requirements=tuple(
                _text_list(data.get("authorization_requirements", []), "authorization_requirements")
            ),
            unknowns=tuple(_text_list(data.get("unknowns", []), "unknowns")),
            trace_completeness=_bounded_number(
                data.get("trace_completeness"), "trace_completeness", 0.0, 1.0
            ),
            metadata=_mapping(data.get("metadata", {}), "metadata"),
        )
        package.validate_graph()
        return package

    def validate_graph(self) -> None:
        node_ids = [node.node_id for node in self.nodes]
        duplicates = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
        if duplicates:
            raise PackageValidationError(f"duplicate node_id values: {duplicates}")

        known = set(node_ids)
        if self.decision_root not in known:
            raise PackageValidationError(
                f"decision_root {self.decision_root!r} does not identify a declared node"
            )

        for dependency in self.dependencies:
            if dependency.source_id not in known:
                raise PackageValidationError(
                    f"dependency source {dependency.source_id!r} is not declared"
                )
            if dependency.target_id not in known:
                raise PackageValidationError(
                    f"dependency target {dependency.target_id!r} is not declared"
                )
            if dependency.source_id == dependency.target_id:
                raise PackageValidationError("self-dependencies are not permitted")

        missing_requirements = sorted(
            requirement
            for requirement in self.authorization_requirements
            if requirement not in known
        )
        if missing_requirements:
            raise PackageValidationError(
                "authorization_requirements reference undeclared nodes: "
                f"{missing_requirements}"
            )


def _required_text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PackageValidationError(f"{key} must be a non-empty string")
    return value


def _mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PackageValidationError(f"{field_name} must be an object")
    return dict(value)


def _list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise PackageValidationError(f"{field_name} must be an array")
    return value


def _text_list(value: Any, field_name: str) -> list[str]:
    items = _list(value, field_name)
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise PackageValidationError(f"{field_name} must contain only non-empty strings")
    return list(items)


def _bounded_number(value: Any, field_name: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PackageValidationError(f"{field_name} must be numeric")
    number = float(value)
    if not minimum <= number <= maximum:
        raise PackageValidationError(
            f"{field_name} must be between {minimum} and {maximum} inclusive"
        )
    return number
