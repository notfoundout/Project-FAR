#!/usr/bin/env python3
"""Core data structures for Project FAR machine-readable objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class Representation:
    id: str
    kind: str
    content: str


@dataclass(frozen=True)
class Relation:
    id: str
    type: str
    source: str
    target: str


@dataclass(frozen=True)
class InterpretationAssignment:
    representation: str
    meaning: str


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    inputs: List[str]
    output: str
    condition: str = ""


@dataclass(frozen=True)
class Transition:
    id: str
    source: str
    rule: str
    target: str
    status: str
    order: int


@dataclass
class FARObject:
    investigation: str
    representations: Dict[str, Representation] = field(default_factory=dict)
    relations: Dict[str, Relation] = field(default_factory=dict)
    interpretations: Dict[str, InterpretationAssignment] = field(default_factory=dict)
    rules: Dict[str, Rule] = field(default_factory=dict)
    transitions: Dict[str, Transition] = field(default_factory=dict)

    def representation_ids(self) -> Set[str]:
        return set(self.representations)

    def rule_ids(self) -> Set[str]:
        return set(self.rules)

    def validate_well_formed(self) -> List[str]:
        errors: List[str] = []

        if not self.investigation.strip():
            errors.append("investigation must be nonempty")

        for rel in self.relations.values():
            if rel.source not in self.representations:
                errors.append(f"relation {rel.id} has unknown source representation {rel.source}")
            if rel.target not in self.representations:
                errors.append(f"relation {rel.id} has unknown target representation {rel.target}")

        for assignment in self.interpretations.values():
            if assignment.representation not in self.representations:
                errors.append(
                    f"interpretation references unknown representation {assignment.representation}"
                )

        for rule in self.rules.values():
            for rep_id in rule.inputs:
                if rep_id not in self.representations:
                    errors.append(f"rule {rule.id} has unknown input representation {rep_id}")
            if rule.output not in self.representations:
                errors.append(f"rule {rule.id} has unknown output representation {rule.output}")

        seen_orders: Set[int] = set()
        for transition in self.transitions.values():
            if transition.rule not in self.rules:
                errors.append(f"transition {transition.id} references unknown rule {transition.rule}")
            if transition.status not in {"admissible", "inadmissible", "unresolved"}:
                errors.append(f"transition {transition.id} has invalid status {transition.status}")
            if transition.order in seen_orders:
                errors.append(f"duplicate transition order {transition.order}")
            seen_orders.add(transition.order)

        return errors

    def dependency_edges(self) -> List[Tuple[str, str, str]]:
        edges: List[Tuple[str, str, str]] = []
        for rel in self.relations.values():
            if rel.type in {"depends_on", "supports", "contradicts", "rebuts", "undercuts"}:
                edges.append((rel.source, rel.target, rel.type))
        return edges

    def detect_cycles(self) -> List[List[str]]:
        graph: Dict[str, List[str]] = {rep_id: [] for rep_id in self.representations}
        for source, target, _ in self.dependency_edges():
            graph.setdefault(source, []).append(target)

        cycles: List[List[str]] = []
        visiting: Set[str] = set()
        visited: Set[str] = set()
        path: List[str] = []

        def visit(node: str) -> None:
            if node in visiting:
                index = path.index(node) if node in path else 0
                cycles.append(path[index:] + [node])
                return
            if node in visited:
                return
            visiting.add(node)
            path.append(node)
            for nxt in graph.get(node, []):
                visit(nxt)
            path.pop()
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)

        return cycles

    def derivation_tree(self) -> List[Dict[str, object]]:
        ordered = sorted(self.transitions.values(), key=lambda item: item.order)
        return [
            {
                "transition": transition.id,
                "order": transition.order,
                "rule": transition.rule,
                "status": transition.status,
                "source": transition.source,
                "target": transition.target,
            }
            for transition in ordered
        ]
