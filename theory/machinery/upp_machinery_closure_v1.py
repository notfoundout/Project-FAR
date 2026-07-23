"""UPP-W5 machinery closure.

This module closes an admissible representation package over every support
artifact required for its registered operations. It is deliberately neutral
about RCCD and later representation-equivalence claims.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class Verdict(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    UNKNOWN = "unknown"


class Availability(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SupportNode:
    node_id: str
    kind: str
    availability: Availability
    effective: bool | None
    registered_queries: tuple[str, ...] = ()

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self.node_id.strip():
            errors.append("node_id must be non-empty")
        if not self.kind.strip():
            errors.append(f"{self.node_id}: kind must be non-empty")
        if self.availability is Availability.PRESENT and self.effective is not True:
            errors.append(f"{self.node_id}: present support must be effectively usable")
        if len(set(self.registered_queries)) != len(self.registered_queries):
            errors.append(f"{self.node_id}: registered queries must be unique")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class SupportEdge:
    source: str
    target: str
    required: bool
    disclosed: bool
    evidence: Availability


@dataclass(frozen=True, slots=True)
class ClosureResult:
    verdict: Verdict
    reached: frozenset[str]
    unresolved_edges: tuple[SupportEdge, ...]
    concealed_required_edges: tuple[SupportEdge, ...]
    missing_required_nodes: tuple[str, ...]
    invalidities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepresentationPackage:
    roots: tuple[str, ...]
    nodes: tuple[SupportNode, ...]
    edges: tuple[SupportEdge, ...]

    def _node_map(self) -> Mapping[str, SupportNode]:
        return {node.node_id: node for node in self.nodes}

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        ids = [node.node_id for node in self.nodes]
        if len(ids) != len(set(ids)):
            errors.append("support node identifiers must be globally unique")
        node_map = self._node_map()
        for root in self.roots:
            if root not in node_map:
                errors.append(f"root {root} is not declared")
        for node in self.nodes:
            errors.extend(node.validate())
        for edge in self.edges:
            if edge.source not in node_map:
                errors.append(f"edge source {edge.source} is not declared")
            if edge.target not in node_map:
                errors.append(f"edge target {edge.target} is not declared")
            if edge.required and not edge.disclosed:
                # This is reported separately as a closure failure, not a schema defect.
                continue
        return tuple(errors)

    def close(self) -> ClosureResult:
        invalidities = self.validate()
        if invalidities:
            return ClosureResult(Verdict.OPEN, frozenset(), (), (), (), invalidities)

        node_map = self._node_map()
        outgoing: dict[str, list[SupportEdge]] = {node_id: [] for node_id in node_map}
        for edge in self.edges:
            outgoing[edge.source].append(edge)

        reached = set(self.roots)
        frontier = list(self.roots)
        unresolved: list[SupportEdge] = []
        concealed: list[SupportEdge] = []
        missing: set[str] = set()

        while frontier:
            source = frontier.pop()
            for edge in outgoing[source]:
                if not edge.required:
                    continue
                if not edge.disclosed:
                    concealed.append(edge)
                    continue
                if edge.evidence is Availability.UNKNOWN:
                    unresolved.append(edge)
                    continue
                if edge.evidence is Availability.ABSENT:
                    missing.add(edge.target)
                    continue
                target = node_map[edge.target]
                if target.availability is Availability.UNKNOWN:
                    unresolved.append(edge)
                    continue
                if target.availability is Availability.ABSENT or target.effective is not True:
                    missing.add(edge.target)
                    continue
                if edge.target not in reached:
                    reached.add(edge.target)
                    frontier.append(edge.target)

        if concealed or missing:
            verdict = Verdict.OPEN
        elif unresolved:
            verdict = Verdict.UNKNOWN
        else:
            verdict = Verdict.CLOSED
        return ClosureResult(
            verdict,
            frozenset(reached),
            tuple(unresolved),
            tuple(concealed),
            tuple(sorted(missing)),
            (),
        )


def closure_is_idempotent(package: RepresentationPackage) -> bool:
    """The computed reached set is a least fixed point of required support traversal."""
    first = package.close()
    if first.verdict is not Verdict.CLOSED:
        return False
    restricted = RepresentationPackage(
        roots=package.roots,
        nodes=tuple(node for node in package.nodes if node.node_id in first.reached),
        edges=tuple(
            edge for edge in package.edges
            if edge.source in first.reached and edge.target in first.reached
        ),
    )
    second = restricted.close()
    return second.verdict is Verdict.CLOSED and second.reached == first.reached


def monotone_under_disclosed_support(
    package: RepresentationPackage,
    added_nodes: Iterable[SupportNode],
    added_edges: Iterable[SupportEdge],
) -> bool:
    """Adding disclosed effective support cannot remove already reached support."""
    before = package.close()
    expanded = RepresentationPackage(
        roots=package.roots,
        nodes=package.nodes + tuple(added_nodes),
        edges=package.edges + tuple(added_edges),
    ).close()
    return before.reached.issubset(expanded.reached)
