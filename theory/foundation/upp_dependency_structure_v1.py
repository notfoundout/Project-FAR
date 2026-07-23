from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping, Sequence


class Truth(str, Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


class DependencyKind(str, Enum):
    SUPPORT = "support"
    DEFEAT = "defeat"
    REVISION = "revision"
    REPLACEMENT = "replacement"
    ADMISSIBILITY = "admissibility"
    PROVENANCE = "provenance"


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    edge_id: str
    source_id: str
    target_id: str
    kind: DependencyKind
    active_at: tuple[str, ...]
    recoverable: Truth
    operationally_relevant: Truth
    equivalence_stable: Truth
    machinery_charged: Truth


@dataclass(frozen=True, slots=True)
class DependencyAssessment:
    target_class_member: Truth
    representation_admissible: Truth
    machinery_closed: Truth
    fully_faithful: Truth
    equivalence_preserved: Truth
    dependency_queries_total: Truth
    failure_unknown_separated: Truth
    nodes: tuple[str, ...]
    edges: tuple[DependencyEdge, ...]


def _all_yes(values: Iterable[Truth]) -> bool:
    return all(value is Truth.YES for value in values)


def _any_no(values: Iterable[Truth]) -> bool:
    return any(value is Truth.NO for value in values)


def validate_dependency_graph(assessment: DependencyAssessment) -> tuple[str, ...]:
    errors: list[str] = []
    node_set = set(assessment.nodes)
    if len(node_set) != len(assessment.nodes):
        errors.append("duplicate node identity")
    edge_ids: set[str] = set()
    for edge in assessment.edges:
        if not edge.edge_id:
            errors.append("empty edge identity")
        if edge.edge_id in edge_ids:
            errors.append(f"duplicate edge identity: {edge.edge_id}")
        edge_ids.add(edge.edge_id)
        if edge.source_id not in node_set:
            errors.append(f"unknown source: {edge.source_id}")
        if edge.target_id not in node_set:
            errors.append(f"unknown target: {edge.target_id}")
        if not edge.active_at:
            errors.append(f"missing temporal scope: {edge.edge_id}")
    return tuple(errors)


def assess_dependency_structure(assessment: DependencyAssessment) -> Verdict:
    premises = (
        assessment.target_class_member,
        assessment.representation_admissible,
        assessment.machinery_closed,
        assessment.fully_faithful,
        assessment.equivalence_preserved,
        assessment.dependency_queries_total,
        assessment.failure_unknown_separated,
    )
    if _any_no(premises):
        return Verdict.REFUTED
    if not _all_yes(premises):
        return Verdict.UNKNOWN
    if validate_dependency_graph(assessment):
        return Verdict.REFUTED
    if not assessment.nodes or not assessment.edges:
        return Verdict.UNKNOWN

    edge_facts = tuple(
        fact
        for edge in assessment.edges
        for fact in (
            edge.recoverable,
            edge.operationally_relevant,
            edge.equivalence_stable,
            edge.machinery_charged,
        )
    )
    if _any_no(edge_facts):
        return Verdict.REFUTED
    if not _all_yes(edge_facts):
        return Verdict.UNKNOWN

    if not any(edge.kind in {DependencyKind.SUPPORT, DependencyKind.DEFEAT} for edge in assessment.edges):
        return Verdict.REFUTED
    return Verdict.PROVED


def construct_dependency_relation(
    edges: Sequence[DependencyEdge],
) -> Mapping[tuple[str, str, str, tuple[str, ...]], str]:
    relation: dict[tuple[str, str, str, tuple[str, ...]], str] = {}
    for edge in edges:
        key = (edge.source_id, edge.target_id, edge.kind.value, edge.active_at)
        previous = relation.get(key)
        if previous is not None and previous != edge.edge_id:
            raise ValueError("duplicate dependency commitment under distinct edge identities")
        relation[key] = edge.edge_id
    return relation


def theorem_witness_exists(assessment: DependencyAssessment) -> bool:
    return (
        assess_dependency_structure(assessment) is Verdict.PROVED
        and bool(construct_dependency_relation(assessment.edges))
    )
