from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class AssessmentStatus(str, Enum):
    IN_SCOPE = "in_scope"
    OUT_OF_SCOPE = "out_of_scope"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ClassEvidence:
    has_alternative_options: bool
    options_can_be_appraised: bool
    appraisal_can_change_permitted_response: bool
    relevant_facts_are_finitely_specifiable: bool
    assessment_is_repeatable_in_principle: bool
    evidence_is_accessible: bool


@dataclass(frozen=True, slots=True)
class ClassDecision:
    status: AssessmentStatus
    satisfied_criteria: FrozenSet[str]
    failed_criteria: FrozenSet[str]
    unknown_criteria: FrozenSet[str]


CRITERIA = frozenset({
    "alternative_options",
    "normative_appraisability",
    "appraisal_sensitive_response",
    "finite_specifiability",
    "repeatable_assessment",
})

FORBIDDEN_RCCD_TERMS = frozenset({
    "commitment", "constrained evolution", "dependency", "revision",
    "historical identity", "uniform recovery", "rccd", "r1", "r2", "r3", "r4", "r5",
})


def classify(evidence: ClassEvidence) -> ClassDecision:
    if not evidence.evidence_is_accessible:
        return ClassDecision(AssessmentStatus.UNKNOWN, frozenset(), frozenset(), CRITERIA)

    values = {
        "alternative_options": evidence.has_alternative_options,
        "normative_appraisability": evidence.options_can_be_appraised,
        "appraisal_sensitive_response": evidence.appraisal_can_change_permitted_response,
        "finite_specifiability": evidence.relevant_facts_are_finitely_specifiable,
        "repeatable_assessment": evidence.assessment_is_repeatable_in_principle,
    }
    passed = frozenset(k for k, v in values.items() if v)
    failed = frozenset(k for k, v in values.items() if not v)
    status = AssessmentStatus.IN_SCOPE if not failed else AssessmentStatus.OUT_OF_SCOPE
    return ClassDecision(status, passed, failed, frozenset())


def criterion_text_is_rccd_independent(text: str) -> bool:
    normalized = text.casefold()
    return not any(term in normalized for term in FORBIDDEN_RCCD_TERMS)
