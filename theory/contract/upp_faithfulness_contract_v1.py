from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class Verdict(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"


class AssumptionKind(str, Enum):
    DEFINITIONAL = "definitional"
    LOGICAL = "logical"
    COMPUTATIONAL = "computational"
    NORMATIVE = "normative"
    EMPIRICAL = "empirical"
    METHODOLOGICAL = "methodological"


class ClauseId(str, Enum):
    STRUCTURAL = "structural_fidelity"
    SEMANTIC = "semantic_fidelity"
    OPERATIONAL = "operational_fidelity"
    DEPENDENCY = "dependency_fidelity"
    INFORMATION = "information_fidelity"
    HISTORICAL = "historical_fidelity"
    QUERY = "query_totality_on_registered_questions"
    ERROR = "error_and_unknown_separation"


@dataclass(frozen=True, slots=True)
class ClauseAssessment:
    clause: ClauseId
    verdict: Verdict
    evidence_ids: FrozenSet[str] = frozenset()
    reason: str = ""

    def validate(self) -> None:
        if self.verdict is Verdict.PASS and not self.evidence_ids:
            raise ValueError("Pass requires evidence")
        if self.verdict is Verdict.UNKNOWN and not self.reason:
            raise ValueError("Unknown requires a reason")


@dataclass(frozen=True, slots=True)
class FaithfulnessAssessment:
    clauses: tuple[ClauseAssessment, ...]

    def validate(self) -> None:
        ids = [c.clause for c in self.clauses]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate clause")
        if set(ids) != set(ClauseId):
            raise ValueError("all frozen clauses must be assessed")
        for clause in self.clauses:
            clause.validate()

    @property
    def verdict(self) -> Verdict:
        self.validate()
        values = {c.verdict for c in self.clauses}
        if Verdict.FAIL in values:
            return Verdict.FAIL
        if Verdict.UNKNOWN in values:
            return Verdict.UNKNOWN
        return Verdict.PASS


FORBIDDEN_CONCLUSION_TERMS = frozenset({
    "rccd", "recoverable commitments", "constrained evolution",
    "dependency-sensitive revision", "historical identity",
    "uniform effective recovery", "universal kernel",
})


def text_is_conclusion_neutral(text: str) -> bool:
    lowered = text.casefold()
    return not any(term in lowered for term in FORBIDDEN_CONCLUSION_TERMS)
