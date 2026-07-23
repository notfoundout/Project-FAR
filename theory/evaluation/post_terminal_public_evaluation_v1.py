from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Tuple


class Verdict(str, Enum):
    CONFIRMED = "confirmed"
    DEFEATED = "defeated"
    UNKNOWN = "unknown"
    INADMISSIBLE = "inadmissible"


class Impact(str, Enum):
    NONE = "no_claim_change"
    UPGRADE_EVIDENCE = "upgrade_evidence_dimension_only"
    REVISE = "revise_or_narrow_claim"
    RETRACT = "retract_affected_claim"
    RECORD_UNKNOWN = "record_unknown"


REQUIRED_DISCLOSURES: FrozenSet[str] = frozenset({
    "exact_theorem",
    "frozen_premises",
    "finite_maximality_boundary",
    "non_kernel_checked_terminal_composition",
    "unknown_discipline",
    "nonclaims",
    "evidence_type",
})

PROHIBITED_PROMOTIONS: FrozenSet[str] = frozenset({
    "unrestricted_metaphysical_universality",
    "open_world_maximality",
    "unique_final_ontology",
    "consciousness_criterion",
    "proof_by_finite_testing",
    "ci_as_mathematical_proof",
    "internal_as_independent_replication",
})


@dataclass(frozen=True)
class Submission:
    disclosure_fields: FrozenSet[str]
    evidence_type: str
    independent: bool
    challenge_resolved: bool
    challenge_defeats_claim: bool = False
    challenge_confirms_claim: bool = False
    prohibited_promotions: FrozenSet[str] = frozenset()
    immutable_artifact: bool = True
    conflict_disclosed: bool = True


@dataclass(frozen=True)
class Assessment:
    verdict: Verdict
    impact: Impact
    reasons: Tuple[str, ...]


def assess(submission: Submission) -> Assessment:
    missing = REQUIRED_DISCLOSURES - submission.disclosure_fields
    if missing:
        return Assessment(Verdict.INADMISSIBLE, Impact.NONE, (f"missing_disclosures:{sorted(missing)}",))
    if submission.prohibited_promotions & PROHIBITED_PROMOTIONS:
        return Assessment(Verdict.INADMISSIBLE, Impact.NONE, ("claim_exceeds_authorized_scope",))
    if not submission.immutable_artifact or not submission.conflict_disclosed:
        return Assessment(Verdict.INADMISSIBLE, Impact.NONE, ("provenance_or_conflict_requirement_failed",))
    if submission.challenge_defeats_claim and submission.challenge_confirms_claim:
        return Assessment(Verdict.UNKNOWN, Impact.RECORD_UNKNOWN, ("internally_conflicting_submission",))
    if not submission.challenge_resolved:
        return Assessment(Verdict.UNKNOWN, Impact.RECORD_UNKNOWN, ("challenge_unresolved",))
    if submission.challenge_defeats_claim:
        return Assessment(Verdict.DEFEATED, Impact.REVISE, ("confirmed_defect_requires_claim_impact",))
    if submission.challenge_confirms_claim:
        if submission.independent:
            return Assessment(Verdict.CONFIRMED, Impact.UPGRADE_EVIDENCE, ("independent_support_upgrades_only_reviewed_dimension",))
        return Assessment(Verdict.CONFIRMED, Impact.NONE, ("internal_support_does_not_upgrade_independence",))
    return Assessment(Verdict.UNKNOWN, Impact.RECORD_UNKNOWN, ("resolved_submission_has_no_determinate_claim_impact",))


def canonical_submission() -> Submission:
    return Submission(
        disclosure_fields=REQUIRED_DISCLOSURES,
        evidence_type="independent_proof_review",
        independent=True,
        challenge_resolved=True,
        challenge_confirms_claim=True,
    )
