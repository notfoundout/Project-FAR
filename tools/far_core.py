#!/usr/bin/env python3
"""Core FIR-style data structures for Project FAR machine-readable objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

ALLOWED_STATEMENT_KINDS = {
    "claim", "universal", "existential", "definition", "conditional",
    "conjunction", "semantic", "registry", "equivalence",
}


@dataclass(frozen=True)
class Statement:
    kind: str
    claim: str
    subject: str = ""
    predicate: str = ""
    scope: str = ""

    @classmethod
    def from_value(cls, value: Any, location: str) -> "Statement":
        if isinstance(value, str):
            if not value.strip():
                raise ValueError(f"{location} statement must be nonempty")
            return cls(kind="claim", claim=value)
        if not isinstance(value, dict):
            raise ValueError(f"{location} statement must be prose or a mapping")
        kind = str(value.get("kind", "")).strip()
        claim = str(value.get("claim", "")).strip()
        if not kind:
            raise ValueError(f"{location} statement missing kind")
        if kind not in ALLOWED_STATEMENT_KINDS:
            raise ValueError(f"{location} statement has invalid kind: {kind}")
        if not claim:
            raise ValueError(f"{location} statement missing claim")
        for optional in ("subject", "predicate", "scope"):
            if optional in value and not isinstance(value[optional], str):
                raise ValueError(f"{location} statement {optional} must be a string when present")
        return cls(
            kind=kind,
            claim=claim,
            subject=str(value.get("subject", "")),
            predicate=str(value.get("predicate", "")),
            scope=str(value.get("scope", "")),
        )

    def to_dict(self) -> Dict[str, str]:
        data = {"kind": self.kind, "claim": self.claim}
        if self.subject:
            data["subject"] = self.subject
        if self.predicate:
            data["predicate"] = self.predicate
        if self.scope:
            data["scope"] = self.scope
        return data


@dataclass(frozen=True)
class Representation:
    id: str
    kind: str
    content: str
    statement: Optional[Statement] = None

    def fir(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"id": self.id, "kind": self.kind, "content": self.content}
        if self.statement:
            data["statement"] = self.statement.to_dict()
        return data


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

    def fir(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "rule": self.rule,
            "target": self.target,
            "status": self.status,
            "order": self.order,
        }


@dataclass(frozen=True)
class ReasoningSystemMapping:
    system: str
    investigation: str
    representation: str
    representational_structure: str
    interpretation: str
    reasoning_calculus: str
    cleanly_maps: List[str] = field(default_factory=list)
    requires_assumptions: List[str] = field(default_factory=list)
    not_yet_represented: List[str] = field(default_factory=list)
    verdict: str = "draft"

    @classmethod
    def from_mapping(cls, value: Dict[str, Any]) -> "ReasoningSystemMapping":
        primitives = value.get("far_primitives", {})
        if not isinstance(primitives, dict):
            raise ValueError("reasoning_system.far_primitives must be a mapping")
        return cls(
            system=str(value.get("system", "")),
            investigation=str(primitives.get("Investigation", "")),
            representation=str(primitives.get("Representation", "")),
            representational_structure=str(primitives.get("Representational Structure", "")),
            interpretation=str(primitives.get("Interpretation", "")),
            reasoning_calculus=str(primitives.get("Reasoning Calculus", "")),
            cleanly_maps=[str(x) for x in value.get("cleanly_maps", [])],
            requires_assumptions=[str(x) for x in value.get("requires_assumptions", [])],
            not_yet_represented=[str(x) for x in value.get("not_yet_represented", [])],
            verdict=str(value.get("verdict", "draft")),
        )

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.system:
            errors.append("reasoning system mapping missing system")
        for primitive, value in [
            ("Investigation", self.investigation),
            ("Representation", self.representation),
            ("Representational Structure", self.representational_structure),
            ("Interpretation", self.interpretation),
            ("Reasoning Calculus", self.reasoning_calculus),
        ]:
            if not value:
                errors.append(f"reasoning system mapping missing FAR primitive: {primitive}")
        if self.verdict not in {"fits FAR", "extends FAR", "falsifies FAR", "draft"}:
            errors.append(f"reasoning system mapping has invalid verdict: {self.verdict}")
        return errors


@dataclass
class FARObject:
    investigation: str
    representations: Dict[str, Representation] = field(default_factory=dict)
    relations: Dict[str, Relation] = field(default_factory=dict)
    interpretations: Dict[str, InterpretationAssignment] = field(default_factory=dict)
    rules: Dict[str, Rule] = field(default_factory=dict)
    transitions: Dict[str, Transition] = field(default_factory=dict)
    reasoning_system: Optional[ReasoningSystemMapping] = None

    def representation_ids(self) -> Set[str]:
        return set(self.representations)

    def rule_ids(self) -> Set[str]:
        return set(self.rules)

    def validate_well_formed(self) -> List[str]:
        errors: List[str] = []

        if not self.investigation.strip():
            errors.append("investigation must be nonempty")

        for rep in self.representations.values():
            if not rep.id.strip():
                errors.append("representation id must be nonempty")
            if not rep.kind.strip():
                errors.append(f"representation {rep.id} kind must be nonempty")
            if not rep.content.strip() and rep.statement is None:
                errors.append(f"representation {rep.id} requires content or a statement object")

        for rel in self.relations.values():
            if rel.source not in self.representations:
                errors.append(f"relation {rel.id} has unknown source representation {rel.source}")
            if rel.target not in self.representations:
                errors.append(f"relation {rel.id} has unknown target representation {rel.target}")

        for assignment in self.interpretations.values():
            if assignment.representation not in self.representations:
                errors.append(f"interpretation references unknown representation {assignment.representation}")

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
            if transition.status not in {"admissible", "inadmissible", "unresolved", "draft"}:
                errors.append(f"transition {transition.id} has invalid status {transition.status}")
            if transition.order in seen_orders:
                errors.append(f"duplicate transition order {transition.order}")
            seen_orders.add(transition.order)

        if self.reasoning_system:
            errors.extend(self.reasoning_system.validate())

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
        return [transition.fir() for transition in sorted(self.transitions.values(), key=lambda item: item.order)]

    def proof_trace(self) -> Dict[str, Any]:
        return {
            "investigation": self.investigation,
            "representations": [rep.fir() for rep in self.representations.values()],
            "dependency_edges": [
                {"source": source, "target": target, "type": edge_type}
                for source, target, edge_type in self.dependency_edges()
            ],
            "cycles": self.detect_cycles(),
            "derivation_tree": self.derivation_tree(),
        }
