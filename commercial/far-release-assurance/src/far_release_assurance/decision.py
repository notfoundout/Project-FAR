"""Deterministic Pass/Review/Blocked/Unknown adjudication."""

from __future__ import annotations

from .model import (
    ClosureStatus,
    Decision,
    Finding,
    FindingDisposition,
    Severity,
)


def adjudicate(findings: tuple[Finding, ...], candidate_closure: ClosureStatus) -> tuple[Decision, str]:
    active = tuple(f for f in findings if f.disposition is not FindingDisposition.DISMISSED)

    confirmed_blockers = tuple(
        f
        for f in active
        if f.disposition is FindingDisposition.CONFIRMED
        and f.blocking
        and f.severity in {Severity.HIGH, Severity.CRITICAL}
    )
    if confirmed_blockers:
        ids = ", ".join(sorted(f.finding_id for f in confirmed_blockers))
        return Decision.BLOCKED, f"Confirmed blocking findings: {ids}."

    mandatory_review = tuple(
        f
        for f in active
        if (
            f.disposition is FindingDisposition.CONFIRMED
            and f.severity is Severity.MEDIUM
        )
        or (
            f.disposition is FindingDisposition.INFERRED
            and f.severity in {Severity.HIGH, Severity.CRITICAL}
        )
    )
    if mandatory_review:
        ids = ", ".join(sorted(f.finding_id for f in mandatory_review))
        return Decision.REVIEW_REQUIRED, f"Findings require human adjudication: {ids}."

    if candidate_closure is ClosureStatus.OPEN:
        return Decision.BLOCKED, "Candidate machinery closure is open."

    unresolved = tuple(
        f for f in active if f.disposition is FindingDisposition.UNKNOWN
    )
    if candidate_closure is ClosureStatus.UNKNOWN or unresolved:
        return Decision.UNKNOWN, "Material evidence remains unresolved; Pass is not justified."

    return Decision.PASS, "No configured blocking, review, or material unresolved condition was established."
