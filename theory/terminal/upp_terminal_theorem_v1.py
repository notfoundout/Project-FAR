from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Tuple


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


class Outcome(str, Enum):
    FULL = "full_registered_universal_theorem_proved"
    WEAKENED = "strictly_weakened_universal_theorem_proved"
    REVISION = "rccd_requires_extension_or_revision"
    DEFEATED = "rccd_universality_defeated"
    BLOCKED = "proof_blocked_by_indispensable_unproved_assumption"


REQUIRED_WORKSTREAMS: Tuple[int, ...] = tuple(range(281, 296))
REQUIRED_PROPERTIES: FrozenSet[str] = frozenset({
    "typed_formal_domain",
    "rccd_independent_class_definition",
    "independent_faithfulness_contract",
    "admissible_representation_universe",
    "machinery_closure",
    "representation_and_commitment_equivalence",
    "recoverable_commitment_necessity",
    "constrained_evolution_necessity",
    "dependency_sensitive_revision_necessity",
    "historical_identity_necessity",
    "uniform_effective_recovery_necessity",
    "rccd_sufficiency_by_reconstruction",
    "component_independence_and_irreducibility",
    "nontriviality",
    "relative_maximality",
    "mechanized_terminal_theorem",
})


@dataclass(frozen=True)
class TerminalEvidence:
    completed_workstreams: FrozenSet[int]
    established_properties: FrozenSet[str]
    refuted_properties: FrozenSet[str] = frozenset()
    unresolved_properties: FrozenSet[str] = frozenset()
    theorem_scope_frozen: bool = True
    definitions_non_circular: bool = True
    hidden_machinery_charged: bool = True
    unknown_preserved: bool = True
    central_semantic_theorem_kernel_checked: bool = False
    executable_composition_verified: bool = True
    open_world_maximality_claimed: bool = False
    unrestricted_metaphysical_claimed: bool = False


@dataclass(frozen=True)
class Adjudication:
    verdict: Verdict
    outcome: Outcome
    reasons: Tuple[str, ...]
    public_evaluation_authorized: bool


def adjudicate(e: TerminalEvidence) -> Adjudication:
    reasons = []
    missing = set(REQUIRED_WORKSTREAMS) - set(e.completed_workstreams)
    if missing:
        return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, (f"missing_workstreams:{sorted(missing)}",), False)
    if e.refuted_properties:
        return Adjudication(Verdict.REFUTED, Outcome.DEFEATED, tuple(sorted(e.refuted_properties)), False)
    if not all((e.theorem_scope_frozen, e.definitions_non_circular, e.hidden_machinery_charged, e.unknown_preserved)):
        return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, ("proof_standard_not_satisfied",), False)
    unresolved = set(e.unresolved_properties)
    absent = set(REQUIRED_PROPERTIES) - set(e.established_properties) - unresolved
    if absent:
        unresolved.update(absent)
    if unresolved:
        return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, tuple(sorted(unresolved)), False)
    if not e.executable_composition_verified:
        return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, ("terminal_composition_not_verified",), False)
    if e.open_world_maximality_claimed or e.unrestricted_metaphysical_claimed:
        return Adjudication(Verdict.REFUTED, Outcome.DEFEATED, ("claim_exceeds_registered_scope",), False)
    if e.central_semantic_theorem_kernel_checked:
        return Adjudication(Verdict.PROVED, Outcome.FULL, ("all_registered_properties_and_kernel_checked_terminal_theorem",), True)
    reasons.extend((
        "all_registered_relative_operational_lemmas_composed",
        "terminal_semantic_theorem_not_kernel_checked",
        "maximality_limited_to_frozen_extension_rules",
    ))
    return Adjudication(Verdict.PROVED, Outcome.WEAKENED, tuple(reasons), True)


def canonical_evidence() -> TerminalEvidence:
    established = set(REQUIRED_PROPERTIES)
    return TerminalEvidence(
        completed_workstreams=frozenset(REQUIRED_WORKSTREAMS),
        established_properties=frozenset(established),
        central_semantic_theorem_kernel_checked=False,
        executable_composition_verified=True,
    )
