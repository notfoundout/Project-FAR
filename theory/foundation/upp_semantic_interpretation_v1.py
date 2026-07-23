from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class Truth(str, Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


class SemanticRole(str, Enum):
    ASSERTION = "assertion"
    DENIAL = "denial"
    QUESTION = "question"
    RULE = "rule"
    CONDITION = "condition"
    REASON = "reason"
    DEFEATER = "defeater"
    REVISION_DIRECTIVE = "revision_directive"


@dataclass(frozen=True, slots=True)
class Interpretation:
    item_id: str
    context_id: str
    content_id: str
    role: SemanticRole
    truth_conditions_id: str
    recoverable: Truth
    context_sensitive: Truth
    compositional_or_explicit: Truth
    operationally_relevant: Truth
    equivalence_stable: Truth
    machinery_charged: Truth


@dataclass(frozen=True, slots=True)
class SemanticAssessment:
    target_class_member: Truth
    representation_admissible: Truth
    machinery_closed: Truth
    fully_faithful: Truth
    equivalence_preserved: Truth
    registered_query_total: Truth
    failure_unknown_separated: Truth
    interpretations: tuple[Interpretation, ...]


def _all_yes(values: Iterable[Truth]) -> bool:
    return all(value is Truth.YES for value in values)


def _any_no(values: Iterable[Truth]) -> bool:
    return any(value is Truth.NO for value in values)


def construct_interpretation_function(
    interpretations: tuple[Interpretation, ...],
) -> Mapping[tuple[str, str], tuple[str, SemanticRole, str]]:
    function: dict[tuple[str, str], tuple[str, SemanticRole, str]] = {}
    for interpretation in interpretations:
        key = (interpretation.context_id, interpretation.item_id)
        value = (
            interpretation.content_id,
            interpretation.role,
            interpretation.truth_conditions_id,
        )
        previous = function.get(key)
        if previous is not None and previous != value:
            raise ValueError("inconsistent interpretation for identical context and item")
        function[key] = value
    return function


def assess_semantic_interpretation(assessment: SemanticAssessment) -> Verdict:
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
    if not assessment.interpretations:
        return Verdict.UNKNOWN

    facts = tuple(
        fact
        for i in assessment.interpretations
        for fact in (
            i.recoverable,
            i.context_sensitive,
            i.compositional_or_explicit,
            i.operationally_relevant,
            i.equivalence_stable,
            i.machinery_charged,
        )
    )
    if _any_no(facts):
        return Verdict.REFUTED
    if not _all_yes(facts):
        return Verdict.UNKNOWN

    for i in assessment.interpretations:
        if not all((i.item_id, i.context_id, i.content_id, i.truth_conditions_id)):
            return Verdict.REFUTED

    try:
        function = construct_interpretation_function(assessment.interpretations)
    except ValueError:
        return Verdict.REFUTED
    return Verdict.PROVED if function else Verdict.UNKNOWN


def theorem_witness_exists(assessment: SemanticAssessment) -> bool:
    return assess_semantic_interpretation(assessment) is Verdict.PROVED
