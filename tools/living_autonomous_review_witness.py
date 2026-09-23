from __future__ import annotations

from typing import Any

from tools.living_autonomous_review_core import CandidateReviewError, PRIOR_ART_STRENGTH


def _assessment_map(
    record: dict[str, Any],
    claim_ids: set[str],
    label: str,
) -> dict[str, dict[str, Any]]:
    rows = record.get("claim_assessments")
    if not isinstance(rows, list) or len(rows) != len(claim_ids):
        raise CandidateReviewError(f"{label}: exact {label} per-claim witness coverage is incomplete")
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise CandidateReviewError(f"{label}: malformed per-claim witness")
        claim_id = row.get("claim_id")
        if not isinstance(claim_id, str) or claim_id not in claim_ids or claim_id in out:
            raise CandidateReviewError(f"{label}: invalid or duplicate per-claim witness id")
        reason = row.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise CandidateReviewError(f"{label}: per-claim witness lacks a reason for {claim_id}")
        out[claim_id] = row
    if set(out) != claim_ids:
        raise CandidateReviewError(f"{label}: exact per-claim witness set does not match frozen claims")
    return out


def _strength_at_least(value: Any, minimum: str) -> bool:
    return (
        isinstance(value, str)
        and value in PRIOR_ART_STRENGTH
        and minimum in PRIOR_ART_STRENGTH
        and PRIOR_ART_STRENGTH[value] >= PRIOR_ART_STRENGTH[minimum]
    )


def validate_exact_claim_witnesses(
    decision: dict[str, Any],
    policy: dict[str, Any],
    claim_ids: set[str],
    screening: dict[str, Any],
    attack: dict[str, Any],
    replication: dict[str, Any],
) -> None:
    """Reject cross-claim composition of aggregate autonomous-review findings.

    Aggregate booleans are useful summaries, but they are not evidence that one
    exact FAR claim satisfies every predicate required by a strong disposition.
    This gate reconstructs the decision from the structured per-claim records and
    requires a single claim to carry the complete contradiction or prior-art
    witness end-to-end.
    """

    screen = _assessment_map(screening, claim_ids, "screening")
    attacked = _assessment_map(attack, claim_ids, "attack")
    replicated = _assessment_map(replication, claim_ids, "replication")

    contradiction_disagreements = sorted(
        claim_id
        for claim_id in claim_ids
        if (attacked[claim_id].get("contradiction_found") is True)
        != (replicated[claim_id].get("contradiction_found") is True)
    )
    if contradiction_disagreements:
        raise CandidateReviewError(
            "attack/replication contradiction disagreement for frozen claims: "
            + ", ".join(contradiction_disagreements)
        )

    invalid_reproductions = sorted(
        claim_id
        for claim_id in claim_ids
        if replicated[claim_id].get("attack_reproduced") is True
        and not (
            attacked[claim_id].get("contradiction_found") is True
            and replicated[claim_id].get("contradiction_found") is True
        )
    )
    if invalid_reproductions:
        raise CandidateReviewError(
            "replication marks a per-claim attack reproduced without a jointly claimed contradiction: "
            + ", ".join(invalid_reproductions)
        )

    unreproduced_joint_contradictions = sorted(
        claim_id
        for claim_id in claim_ids
        if attacked[claim_id].get("contradiction_found") is True
        and replicated[claim_id].get("contradiction_found") is True
        and replicated[claim_id].get("attack_reproduced") is not True
    )
    if unreproduced_joint_contradictions:
        raise CandidateReviewError(
            "replication did not reproduce jointly claimed per-claim contradictions: "
            + ", ".join(unreproduced_joint_contradictions)
        )

    contradiction_witnesses = {
        claim_id
        for claim_id in claim_ids
        if screen[claim_id].get("relevant") is True
        and screen[claim_id].get("premise_match") is True
        and screen[claim_id].get("scope_match") is True
        and attacked[claim_id].get("contradiction_found") is True
        and replicated[claim_id].get("contradiction_found") is True
        and replicated[claim_id].get("attack_reproduced") is True
    }

    aggregate_reproduced_contradiction = (
        attack.get("contradiction_found") is True
        and replication.get("contradiction_found") is True
        and replication.get("attack_reproduced") is True
    )
    if aggregate_reproduced_contradiction and not contradiction_witnesses:
        raise CandidateReviewError(
            "reproduced contradiction has no single exact claim carrying premise, scope, attack, and replication"
        )

    disposition = decision.get("disposition")
    if disposition == "PROJECT_CHANGE_REQUIRED" and not contradiction_witnesses:
        raise CandidateReviewError("PROJECT_CHANGE_REQUIRED lacks a complete exact per-claim contradiction witness")
    if contradiction_witnesses and disposition != "PROJECT_CHANGE_REQUIRED":
        raise CandidateReviewError("adjudication downgraded a complete exact per-claim contradiction witness")

    prior_gate = policy.get("prior_art_gate")
    if not isinstance(prior_gate, dict) or not isinstance(prior_gate.get("minimum_strength"), str):
        raise CandidateReviewError("prior-art witness gate is malformed")
    minimum = prior_gate["minimum_strength"]
    prior_witnesses = {
        claim_id
        for claim_id in claim_ids
        if screen[claim_id].get("relevant") is True
        and attacked[claim_id].get("prior_art_found") is True
        and replicated[claim_id].get("prior_art_found") is True
        and _strength_at_least(attacked[claim_id].get("prior_art_strength"), minimum)
        and _strength_at_least(replicated[claim_id].get("prior_art_strength"), minimum)
    }

    aggregate_direct_prior = (
        attack.get("prior_art_found") is True
        and replication.get("prior_art_found") is True
        and _strength_at_least(attack.get("prior_art_strength"), minimum)
        and _strength_at_least(replication.get("prior_art_strength"), minimum)
    )
    if aggregate_direct_prior and not prior_witnesses:
        raise CandidateReviewError(
            "agreed direct prior art has no single exact claim carrying both attack and replication findings"
        )

    if disposition == "N1_PRIOR_ART_LEAD" and not prior_witnesses:
        raise CandidateReviewError("N1_PRIOR_ART_LEAD lacks a complete exact per-claim prior-art witness")
    if prior_witnesses and disposition not in {"N1_PRIOR_ART_LEAD", "PROJECT_CHANGE_REQUIRED"}:
        raise CandidateReviewError("adjudication downgraded a complete exact per-claim prior-art witness")
