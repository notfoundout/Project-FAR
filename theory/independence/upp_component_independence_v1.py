"""Executable UPP-W12 component-independence adjudicator.

The result is deliberately relative to the frozen UPP framework.  It tests
whether each registered RCCD component has a preservation obligation that
cannot be discharged by merely relabelling, copying, or combining the other
four components.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import FrozenSet, Iterable, Mapping


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


COMPONENTS = (
    "recoverable_commitment",
    "constrained_evolution",
    "dependency_structure",
    "semantic_interpretation",
    "historical_trace",
)

OBLIGATIONS: Mapping[str, FrozenSet[str]] = {
    "recoverable_commitment": frozenset({"commitment_identity", "commitment_query_totality", "failure_unknown_separation"}),
    "constrained_evolution": frozenset({"permitted_forbidden_separation", "history_sensitive_admissibility", "governing_reason_recovery"}),
    "dependency_structure": frozenset({"typed_directed_edges", "operational_relevance", "support_or_defeat_edge"}),
    "semantic_interpretation": frozenset({"content_identity", "semantic_role", "truth_or_satisfaction_conditions"}),
    "historical_trace": frozenset({"event_identity", "predecessor_and_revision_lineage", "replay_or_rollback_fidelity"}),
}


@dataclass(frozen=True, slots=True)
class ReductionAttempt:
    target: str
    sources: FrozenSet[str]
    recovered_obligations: FrozenSet[str]
    effective: bool
    total: bool
    equivalence_invariant: bool
    machinery_accounted: bool
    circular: bool = False
    unresolved: bool = False

    def adjudicate(self) -> Verdict:
        if self.target not in COMPONENTS or not self.sources or self.target in self.sources:
            return Verdict.REFUTED
        if self.circular:
            return Verdict.REFUTED
        if self.unresolved:
            return Verdict.UNKNOWN
        required = OBLIGATIONS[self.target]
        if not (self.effective and self.total and self.equivalence_invariant and self.machinery_accounted):
            return Verdict.REFUTED
        return Verdict.PROVED if required <= self.recovered_obligations else Verdict.REFUTED


@dataclass(frozen=True, slots=True)
class SeparationWitness:
    target: str
    preserved_sources: FrozenSet[str]
    target_obligation_lost: str
    admissible: bool = True
    faithful_except_target: bool = True
    closed: bool = True
    nonvacuous: bool = True
    unresolved: bool = False

    def adjudicate(self) -> Verdict:
        if self.target not in COMPONENTS:
            return Verdict.REFUTED
        if self.target in self.preserved_sources or self.target_obligation_lost not in OBLIGATIONS[self.target]:
            return Verdict.REFUTED
        if self.unresolved:
            return Verdict.UNKNOWN
        expected_sources = frozenset(set(COMPONENTS) - {self.target})
        conditions = (
            self.preserved_sources == expected_sources,
            self.admissible,
            self.faithful_except_target,
            self.closed,
            self.nonvacuous,
        )
        return Verdict.PROVED if all(conditions) else Verdict.REFUTED


@dataclass(frozen=True, slots=True)
class IndependenceCertificate:
    witnesses: tuple[SeparationWitness, ...]
    pairwise_aliasing_excluded: bool
    joint_reduction_excluded: bool
    interaction_preserved: bool
    renaming_invariant: bool
    unresolved: bool = False

    def adjudicate(self) -> Verdict:
        if self.unresolved:
            return Verdict.UNKNOWN
        by_target = {w.target: w for w in self.witnesses}
        if set(by_target) != set(COMPONENTS):
            return Verdict.REFUTED
        if any(w.adjudicate() is not Verdict.PROVED for w in by_target.values()):
            return Verdict.REFUTED
        global_conditions = (
            self.pairwise_aliasing_excluded,
            self.joint_reduction_excluded,
            self.interaction_preserved,
            self.renaming_invariant,
        )
        return Verdict.PROVED if all(global_conditions) else Verdict.REFUTED


def canonical_witnesses() -> tuple[SeparationWitness, ...]:
    lost = {
        "recoverable_commitment": "commitment_identity",
        "constrained_evolution": "permitted_forbidden_separation",
        "dependency_structure": "typed_directed_edges",
        "semantic_interpretation": "truth_or_satisfaction_conditions",
        "historical_trace": "predecessor_and_revision_lineage",
    }
    return tuple(
        SeparationWitness(
            target=target,
            preserved_sources=frozenset(set(COMPONENTS) - {target}),
            target_obligation_lost=lost[target],
        )
        for target in COMPONENTS
    )


def canonical_certificate() -> IndependenceCertificate:
    return IndependenceCertificate(
        witnesses=canonical_witnesses(),
        pairwise_aliasing_excluded=True,
        joint_reduction_excluded=True,
        interaction_preserved=True,
        renaming_invariant=True,
    )


def renaming_invariant(certificate: IndependenceCertificate, renaming: Mapping[str, str]) -> bool:
    if set(renaming) != set(COMPONENTS) or set(renaming.values()) != set(COMPONENTS):
        return False
    renamed = tuple(
        SeparationWitness(
            target=renaming[w.target],
            preserved_sources=frozenset(renaming[s] for s in w.preserved_sources),
            target_obligation_lost=next(iter(OBLIGATIONS[renaming[w.target]])),
            admissible=w.admissible,
            faithful_except_target=w.faithful_except_target,
            closed=w.closed,
            nonvacuous=w.nonvacuous,
            unresolved=w.unresolved,
        )
        for w in certificate.witnesses
    )
    translated = IndependenceCertificate(
        witnesses=renamed,
        pairwise_aliasing_excluded=certificate.pairwise_aliasing_excluded,
        joint_reduction_excluded=certificate.joint_reduction_excluded,
        interaction_preserved=certificate.interaction_preserved,
        renaming_invariant=certificate.renaming_invariant,
        unresolved=certificate.unresolved,
    )
    return translated.adjudicate() is certificate.adjudicate()


def all_component_permutations_preserve_verdict() -> bool:
    cert = canonical_certificate()
    return all(
        renaming_invariant(cert, dict(zip(COMPONENTS, p)))
        for p in permutations(COMPONENTS)
    )
