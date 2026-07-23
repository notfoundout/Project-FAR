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


@dataclass(frozen=True, slots=True)
class EvolutionTransition:
    transition_id: str
    before_commitments: tuple[str, ...]
    after_commitments: tuple[str, ...]
    history_prefix: tuple[str, ...]
    admissible: Truth
    governing_constraints: tuple[str, ...]
    reason_recoverable: Truth
    equivalence_stable: Truth
    machinery_charged: Truth

    @property
    def changes_commitments(self) -> bool:
        return self.before_commitments != self.after_commitments


@dataclass(frozen=True, slots=True)
class EvolutionAssessment:
    target_class_member: Truth
    representation_admissible: Truth
    machinery_closed: Truth
    fully_faithful: Truth
    equivalence_preserved: Truth
    transitions: tuple[EvolutionTransition, ...]
    registered_query_total: Truth
    failure_unknown_separated: Truth


def _all_yes(values: Iterable[Truth]) -> bool:
    return all(value is Truth.YES for value in values)


def _any_no(values: Iterable[Truth]) -> bool:
    return any(value is Truth.NO for value in values)


def assess_constrained_evolution(assessment: EvolutionAssessment) -> Verdict:
    premises = (
        assessment.target_class_member,
        assessment.representation_admissible,
        assessment.machinery_closed,
        assessment.fully_faithful,
        assessment.equivalence_preserved,
        assessment.registered_query_total,
        assessment.failure_unknown_separated,
    )
    if _any_no(premises):
        return Verdict.REFUTED
    if not _all_yes(premises):
        return Verdict.UNKNOWN

    changing = tuple(t for t in assessment.transitions if t.changes_commitments)
    if not changing:
        return Verdict.UNKNOWN

    support_facts = tuple(
        fact
        for t in changing
        for fact in (
            t.reason_recoverable,
            t.equivalence_stable,
            t.machinery_charged,
        )
    )
    if _any_no(support_facts):
        return Verdict.REFUTED
    if not _all_yes(support_facts):
        return Verdict.UNKNOWN
    if any(t.admissible is Truth.UNKNOWN for t in changing):
        return Verdict.UNKNOWN

    for transition in changing:
        if not transition.transition_id:
            return Verdict.REFUTED
        if not transition.history_prefix:
            return Verdict.REFUTED
        if not transition.governing_constraints:
            return Verdict.REFUTED

    admissible_values = {t.admissible for t in changing}
    if admissible_values != {Truth.YES, Truth.NO}:
        return Verdict.REFUTED

    return Verdict.PROVED


def construct_admissibility_relation(
    transitions: Sequence[EvolutionTransition],
) -> Mapping[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]], Truth]:
    relation: dict[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]], Truth] = {}
    for transition in transitions:
        if not transition.changes_commitments:
            continue
        key = (
            transition.history_prefix,
            transition.before_commitments,
            transition.after_commitments,
        )
        previous = relation.get(key)
        if previous is not None and previous is not transition.admissible:
            raise ValueError("inconsistent admissibility verdict for identical historical transition")
        relation[key] = transition.admissible
    return relation


def theorem_witness_exists(assessment: EvolutionAssessment) -> bool:
    if assess_constrained_evolution(assessment) is not Verdict.PROVED:
        return False
    relation = construct_admissibility_relation(assessment.transitions)
    return bool(relation) and set(relation.values()) == {Truth.YES, Truth.NO}
