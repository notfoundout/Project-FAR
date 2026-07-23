"""Commercial FAR Release Assurance domain model.

This module is application code. It does not modify or certify Project FAR research
claims and does not claim access to hidden cognition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class EvidenceStatus(StrEnum):
    CONFIRMED = "confirmed"
    INFERRED = "inferred"
    DISCLOSED_UNVERIFIED = "disclosed_unverified"
    MISSING = "missing"
    CONTRADICTORY = "contradictory"
    INEFFECTIVE = "ineffective"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class ClosureStatus(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    UNKNOWN = "unknown"


class Decision(StrEnum):
    PASS = "pass"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingDisposition(StrEnum):
    CONFIRMED = "confirmed"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    DISMISSED = "dismissed"


@dataclass(frozen=True, slots=True)
class MachineryItem:
    machinery_id: str
    kind: str
    name: str
    version: str | None = None
    digest: str | None = None
    required_dependencies: tuple[str, ...] = ()
    evidence_status: EvidenceStatus = EvidenceStatus.UNKNOWN
    declared: bool = True
    effective: bool | None = None
    valid: bool | None = None
    mutable: bool = False
    external: bool = False
    attributes: Mapping[str, object] = field(default_factory=dict)

    def unresolved(self) -> bool:
        return self.evidence_status in {
            EvidenceStatus.DISCLOSED_UNVERIFIED,
            EvidenceStatus.UNKNOWN,
        } or self.effective is None or self.valid is None

    def opening_defect(self) -> bool:
        return (
            not self.declared
            or self.evidence_status
            in {
                EvidenceStatus.MISSING,
                EvidenceStatus.CONTRADICTORY,
                EvidenceStatus.INEFFECTIVE,
                EvidenceStatus.INVALID,
            }
            or self.effective is False
            or self.valid is False
        )


@dataclass(frozen=True, slots=True)
class ReasoningEvent:
    event_id: str
    run_id: str
    release_id: str
    sequence: int
    event_type: str
    subject_id: str
    object_ids: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    dependency_refs: tuple[str, ...] = ()
    machinery_refs: tuple[str, ...] = ()
    identity_context: Mapping[str, str] = field(default_factory=dict)
    status: EvidenceStatus = EvidenceStatus.UNKNOWN
    source_ref: str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ReleasePackage:
    release_id: str
    source_commit: str
    machinery: tuple[MachineryItem, ...]
    events: tuple[ReasoningEvent, ...]
    decision_roots: tuple[str, ...]
    release_roots: tuple[str, ...]
    replay_completeness: float | None = None
    output_metrics: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ClosureResult:
    status: ClosureStatus
    reached: tuple[str, ...]
    unresolved: tuple[str, ...]
    defects: tuple[str, ...]
    duplicates: tuple[str, ...]
    undeclared_roots: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    rule_id: str
    severity: Severity
    disposition: FindingDisposition
    rationale: str
    baseline_refs: tuple[str, ...] = ()
    candidate_refs: tuple[str, ...] = ()
    affected_ids: tuple[str, ...] = ()
    remediation: str | None = None
    blocking: bool = False


@dataclass(frozen=True, slots=True)
class ReleaseComparison:
    baseline_release_id: str
    candidate_release_id: str
    baseline_closure: ClosureResult
    candidate_closure: ClosureResult
    findings: tuple[Finding, ...]
    decision: Decision
    rationale: str
