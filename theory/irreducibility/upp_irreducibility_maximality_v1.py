"""Executable model for UPP-W14 irreducibility and maximality.

The result is explicitly relative to frozen finite search spaces.  It does not
turn absence of a registered counterexample into unrestricted global proof.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Iterable


COMPONENTS = (
    "recoverable_commitment",
    "constrained_evolution",
    "dependency_structure",
    "semantic_interpretation",
    "historical_trace",
)
PRESERVATION_DIMENSIONS = (
    "structural",
    "semantic",
    "operational",
    "dependency",
    "information",
    "historical",
    "query_totality",
    "failure_unknown_separation",
)
REDUCTION_REQUIREMENTS = (
    "effective",
    "total",
    "non_circular",
    "machinery_closed",
    "equivalence_invariant",
    "identity_preserving",
    "query_total",
    "failure_unknown_separated",
)
MAXIMALITY_REQUIREMENTS = (
    "challenge_registered",
    "membership_decidable_or_unknown",
    "faithfulness_checked",
    "machinery_closed",
    "embedding_checked",
    "boundary_reason_recorded",
)


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ReductionCandidate:
    candidate_id: str
    supplied_components: frozenset[str]
    preserved_dimensions: frozenset[str]
    satisfied_requirements: frozenset[str]
    reconstructs_all_registered_queries: bool
    lower_primitive_count: bool
    lower_or_equal_derived_cost: bool
    unresolved_facts: tuple[str, ...] = ()
    failure_reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExtensionChallenge:
    challenge_id: str
    satisfied_requirements: frozenset[str]
    in_target_class: bool | None
    embeds_in_rccd: bool | None
    preserved_dimensions: frozenset[str]
    unresolved_facts: tuple[str, ...] = ()
    failure_reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SearchLedger:
    reduction_candidates: tuple[ReductionCandidate, ...]
    extension_challenges: tuple[ExtensionChallenge, ...]
    reduction_space_frozen: bool
    extension_space_frozen: bool
    candidate_ids_unique: bool
    challenge_ids_unique: bool


def reduction_verdict(candidate: ReductionCandidate) -> Verdict:
    if candidate.failure_reasons:
        return Verdict.REFUTED
    if candidate.unresolved_facts:
        return Verdict.UNKNOWN
    if not set(REDUCTION_REQUIREMENTS).issubset(candidate.satisfied_requirements):
        return Verdict.REFUTED
    if not set(PRESERVATION_DIMENSIONS).issubset(candidate.preserved_dimensions):
        return Verdict.REFUTED
    if not candidate.reconstructs_all_registered_queries:
        return Verdict.REFUTED
    if not candidate.lower_primitive_count:
        return Verdict.REFUTED
    if not candidate.lower_or_equal_derived_cost:
        return Verdict.REFUTED
    return Verdict.PROVED


def challenge_verdict(challenge: ExtensionChallenge) -> Verdict:
    if challenge.failure_reasons:
        return Verdict.REFUTED
    if challenge.unresolved_facts:
        return Verdict.UNKNOWN
    if not set(MAXIMALITY_REQUIREMENTS).issubset(challenge.satisfied_requirements):
        return Verdict.REFUTED
    if challenge.in_target_class is None or challenge.embeds_in_rccd is None:
        return Verdict.UNKNOWN
    if challenge.in_target_class is False:
        return Verdict.PROVED
    if not set(PRESERVATION_DIMENSIONS).issubset(challenge.preserved_dimensions):
        return Verdict.REFUTED
    return Verdict.PROVED if challenge.embeds_in_rccd else Verdict.REFUTED


def irreducibility_verdict(ledger: SearchLedger) -> Verdict:
    if not ledger.reduction_space_frozen or not ledger.candidate_ids_unique:
        return Verdict.UNKNOWN
    verdicts = tuple(reduction_verdict(c) for c in ledger.reduction_candidates)
    if Verdict.PROVED in verdicts:
        return Verdict.REFUTED
    if Verdict.UNKNOWN in verdicts:
        return Verdict.UNKNOWN
    return Verdict.PROVED


def maximality_verdict(ledger: SearchLedger) -> Verdict:
    if not ledger.extension_space_frozen or not ledger.challenge_ids_unique:
        return Verdict.UNKNOWN
    verdicts = tuple(challenge_verdict(c) for c in ledger.extension_challenges)
    if Verdict.REFUTED in verdicts:
        return Verdict.REFUTED
    if Verdict.UNKNOWN in verdicts:
        return Verdict.UNKNOWN
    return Verdict.PROVED


def aggregate_verdict(ledger: SearchLedger) -> Verdict:
    values = (irreducibility_verdict(ledger), maximality_verdict(ledger))
    if Verdict.REFUTED in values:
        return Verdict.REFUTED
    if Verdict.UNKNOWN in values:
        return Verdict.UNKNOWN
    return Verdict.PROVED


def proper_component_subsets() -> tuple[frozenset[str], ...]:
    return tuple(
        frozenset(items)
        for size in range(len(COMPONENTS))
        for items in combinations(COMPONENTS, size)
    )


def validate_ledger(ledger: SearchLedger) -> tuple[str, ...]:
    failures: list[str] = []
    candidate_ids = [c.candidate_id for c in ledger.reduction_candidates]
    challenge_ids = [c.challenge_id for c in ledger.extension_challenges]
    if len(candidate_ids) != len(set(candidate_ids)) or not ledger.candidate_ids_unique:
        failures.append("duplicate_reduction_candidate_identity")
    if len(challenge_ids) != len(set(challenge_ids)) or not ledger.challenge_ids_unique:
        failures.append("duplicate_extension_challenge_identity")
    registered_subsets = {c.supplied_components for c in ledger.reduction_candidates}
    missing = set(proper_component_subsets()) - registered_subsets
    if missing:
        failures.append("proper_component_subset_search_incomplete")
    if not ledger.reduction_space_frozen:
        failures.append("reduction_search_space_not_frozen")
    if not ledger.extension_space_frozen:
        failures.append("extension_search_space_not_frozen")
    return tuple(failures)


def canonical_ledger() -> SearchLedger:
    reductions = []
    for index, subset in enumerate(proper_component_subsets(), start=1):
        reductions.append(
            ReductionCandidate(
                candidate_id=f"subset-{index:02d}",
                supplied_components=subset,
                preserved_dimensions=frozenset(PRESERVATION_DIMENSIONS) - {"information"},
                satisfied_requirements=frozenset(REDUCTION_REQUIREMENTS),
                reconstructs_all_registered_queries=False,
                lower_primitive_count=True,
                lower_or_equal_derived_cost=True,
                failure_reasons=("missing_distinctive_component_obligation",),
            )
        )
    extensions = (
        ExtensionChallenge(
            challenge_id="distributed-medium",
            satisfied_requirements=frozenset(MAXIMALITY_REQUIREMENTS),
            in_target_class=True,
            embeds_in_rccd=True,
            preserved_dimensions=frozenset(PRESERVATION_DIMENSIONS),
        ),
        ExtensionChallenge(
            challenge_id="probabilistic-transition-policy",
            satisfied_requirements=frozenset(MAXIMALITY_REQUIREMENTS),
            in_target_class=True,
            embeds_in_rccd=True,
            preserved_dimensions=frozenset(PRESERVATION_DIMENSIONS),
        ),
        ExtensionChallenge(
            challenge_id="opaque-output-only-device",
            satisfied_requirements=frozenset(MAXIMALITY_REQUIREMENTS),
            in_target_class=False,
            embeds_in_rccd=False,
            preserved_dimensions=frozenset(),
        ),
        ExtensionChallenge(
            challenge_id="learned-semantic-decoder",
            satisfied_requirements=frozenset(MAXIMALITY_REQUIREMENTS),
            in_target_class=True,
            embeds_in_rccd=True,
            preserved_dimensions=frozenset(PRESERVATION_DIMENSIONS),
        ),
        ExtensionChallenge(
            challenge_id="branching-revision-history",
            satisfied_requirements=frozenset(MAXIMALITY_REQUIREMENTS),
            in_target_class=True,
            embeds_in_rccd=True,
            preserved_dimensions=frozenset(PRESERVATION_DIMENSIONS),
        ),
    )
    return SearchLedger(
        reduction_candidates=tuple(reductions),
        extension_challenges=extensions,
        reduction_space_frozen=True,
        extension_space_frozen=True,
        candidate_ids_unique=True,
        challenge_ids_unique=True,
    )


def summarize(ledger: SearchLedger) -> dict[str, object]:
    return {
        "validation_failures": validate_ledger(ledger),
        "irreducibility": irreducibility_verdict(ledger).value,
        "maximality": maximality_verdict(ledger).value,
        "aggregate": aggregate_verdict(ledger).value,
        "reduction_candidate_total": len(ledger.reduction_candidates),
        "extension_challenge_total": len(ledger.extension_challenges),
        "scope": "frozen_registered_search_spaces_only",
    }
