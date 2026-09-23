from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from tools import living_implementation_contract as implementation
from tools import promote_living_research as promoter
from tools.living_autonomous_review_core import *
from tools.living_autonomous_review_model import *

def strength_at_least(value: Any, minimum: str) -> bool:
    return isinstance(value, str) and value in PRIOR_ART_STRENGTH and PRIOR_ART_STRENGTH[value] >= PRIOR_ART_STRENGTH[minimum]


def validate_decision(
    decision: dict[str, Any],
    policy: dict[str, Any],
    root: Path,
    claim_ids: set[str],
    screening: dict[str, Any],
    attack: dict[str, Any],
    replication: dict[str, Any],
    attack_meta: dict[str, Any],
    replication_meta: dict[str, Any],
) -> None:
    disposition = decision.get("disposition")
    if disposition not in ALLOWED:
        raise CandidateReviewError("adjudication returned invalid disposition")
    project = decision.get("project_change_required")
    impl_required = decision.get("implementation_required")
    if not isinstance(project, bool) or not isinstance(impl_required, bool):
        raise CandidateReviewError("adjudication boolean contract malformed")
    if (disposition == "PROJECT_CHANGE_REQUIRED") != project:
        raise CandidateReviewError("project-change disposition/boolean mismatch")
    scientific = decision.get("scientific_targets")
    impl_targets = decision.get("implementation_targets")
    if not isinstance(scientific, list) or any(not isinstance(x, str) for x in scientific):
        raise CandidateReviewError("scientific_targets malformed")
    if not isinstance(impl_targets, list) or any(not isinstance(x, str) for x in impl_targets):
        raise CandidateReviewError("implementation_targets malformed")
    if len(scientific) > policy["max_scientific_targets"] or len(impl_targets) > policy["max_implementation_targets"]:
        raise CandidateReviewError("adjudication target bound exceeded")
    if not project and scientific:
        raise CandidateReviewError("non-project-change disposition may not carry scientific targets")

    if project:
        gate = policy["project_change_gate"]
        if not scientific:
            raise CandidateReviewError("PROJECT_CHANGE_REQUIRED requires scientific targets")
        if gate["require_verified_primary_source"] and not screening.get("primary_source_verified"):
            raise CandidateReviewError("project change lacks primary-source verification")
        if gate["require_premise_match"] and not screening.get("premise_match"):
            raise CandidateReviewError("project change lacks premise match")
        if gate["require_scope_match"] and not screening.get("scope_match"):
            raise CandidateReviewError("project change lacks scope match")
        if gate["require_attack_contradiction"] and attack.get("contradiction_found") is not True:
            raise CandidateReviewError("project change lacks explicit attack contradiction")
        if gate["require_reproducible_attack"] and not attack.get("reproducible_attack"):
            raise CandidateReviewError("project change lacks reproducible attack")
        if gate["require_replication"] and replication.get("attack_reproduced") is not True:
            raise CandidateReviewError("project change lacks replication")
        if gate["require_replication_contradiction"] and replication.get("contradiction_found") is not True:
            raise CandidateReviewError("project change lacks explicit replication contradiction")
        validate_source_binding(attack, attack_meta, "attack")
        validate_source_binding(replication, replication_meta, "replication")
        shared = set(attack.get("affected_claim_ids", [])) & set(replication.get("affected_claim_ids", []))
        if gate["require_matching_claim_id"] and not shared:
            raise CandidateReviewError("attack and replication disagree on affected claim")
        if not shared <= claim_ids:
            raise CandidateReviewError("project change references claim outside selected canonical set")

    if disposition == "N1_PRIOR_ART_LEAD":
        gate = policy["prior_art_gate"]
        if gate["require_attack_prior_art"] and attack.get("prior_art_found") is not True:
            raise CandidateReviewError("prior-art lead lacks attack-role prior art")
        if gate["require_replication_prior_art"] and replication.get("prior_art_found") is not True:
            raise CandidateReviewError("prior-art lead lacks replication-role prior art")
        minimum = gate["minimum_strength"]
        if not strength_at_least(attack.get("prior_art_strength"), minimum):
            raise CandidateReviewError("attack prior art is below configured strength")
        if not strength_at_least(replication.get("prior_art_strength"), minimum):
            raise CandidateReviewError("replication prior art is below configured strength")
        validate_source_binding(attack, attack_meta, "attack")
        validate_source_binding(replication, replication_meta, "replication")
        shared = set(attack.get("affected_claim_ids", [])) & set(replication.get("affected_claim_ids", []))
        if gate["require_matching_claim_id"] and not shared:
            raise CandidateReviewError("prior-art roles disagree on affected claim")
        if not shared <= claim_ids:
            raise CandidateReviewError("prior-art lead references claim outside selected canonical set")

    if impl_required != bool(impl_targets):
        raise CandidateReviewError("implementation_required/targets mismatch")

    promotion_policy = load_json(root / promoter.POLICY)
    promoter.validate_policy(promotion_policy)
    forbidden = promotion_policy.get("canonical_forbidden_prefixes", [])
    for target in scientific:
        try:
            promoter.validate_target(target, promotion_policy)
        except promoter.PromotionError as exc:
            raise CandidateReviewError(f"invalid scientific target {target}: {exc}") from exc
        if any(target.startswith(prefix) for prefix in forbidden):
            raise CandidateReviewError(f"scientific target forbidden by promotion policy: {target}")

    implementation_policy = load_json(root / implementation.IMPLEMENTATION_POLICY)
    implementation.validate_policy(implementation_policy)
    for target in impl_targets:
        try:
            implementation.validate_target(target, implementation_policy)
        except implementation.ImplementationContractError as exc:
            raise CandidateReviewError(f"invalid implementation target {target}: {exc}") from exc


def current_text(root: Path, target: str) -> str:
    path = root / promoter.safe(target)
    if not path.exists():
        return ""
    if not path.is_file() or path.is_symlink():
        raise ReviewError(f"non-regular target: {target}")
    return path.read_text(encoding="utf-8")


def generate_replacements(
    model: Model,
    *,
    kind: str,
    targets: list[str],
    root: Path,
    context: Any,
    max_bytes: int,
) -> dict[str, bytes]:
    if not targets:
        return {}
    current = {path: current_text(root, path) for path in targets}
    result, _ = model.generate(
        role=f"{kind}_change_generator",
        prompt=(
            f"Generate the minimal exact {kind} replacements required by the adjudication. Return every "
            "requested target exactly once and no other target. Preserve unrelated content. JSON targets "
            "must be complete valid JSON.\n\n"
            + json.dumps({"targets": targets, "current_files": current, "adjudication": context}, ensure_ascii=False)
        ),
        schema=REPLACEMENTS_SCHEMA,
    )
    rows = result.get("files")
    if not isinstance(rows, list):
        raise CandidateReviewError(f"{kind} generator returned malformed files")
    out: dict[str, bytes] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "content"}:
            raise CandidateReviewError(f"{kind} generator returned malformed row")
        path, content = row["path"], row["content"]
        if path not in targets or path in out or not isinstance(content, str):
            raise CandidateReviewError(f"{kind} generator target mismatch: {path!r}")
        if Path(path).suffix.lower() == ".json":
            try:
                json.loads(content)
            except Exception as exc:
                raise CandidateReviewError(f"generated JSON invalid for {path}: {exc}") from exc
        out[path] = content.encode("utf-8")
    if set(out) != set(targets):
        raise CandidateReviewError(f"{kind} generator omitted targets")
    if sum(len(raw) for raw in out.values()) > max_bytes:
        raise CandidateReviewError(f"{kind} replacement byte bound exceeded")
    if all(out[path] == current[path].encode("utf-8") for path in targets):
        raise CandidateReviewError(f"{kind} correction is an all-no-op replacement set")
    return out


def review_artifacts(
    cid: str,
    candidate: dict[str, Any],
    claims: list[dict[str, Any]],
    screening: dict[str, Any],
    screen_meta: dict[str, Any],
    attack: dict[str, Any],
    attack_meta: dict[str, Any],
    replication: dict[str, Any],
    replication_meta: dict[str, Any],
    decision: dict[str, Any],
    now: datetime,
):
    fingerprint = digest(canonical_bytes({
        "candidate": candidate,
        "screening": screening,
        "attack": attack,
        "replication": replication,
        "adjudication": decision,
    }))[:16]
    review_id = f"{cid}-{fingerprint}"
    root = REVIEW_ROOT / review_id
    values = {
        "question": {"candidate_id": cid, "candidate": candidate, "canonical_claims": claims},
        "execution": {
            "program_id": "FAR-LIVING-AUTONOMOUS-REVIEW-001",
            "executed_utc": iso(now),
            "roles": ["screening", "attack", "replication", "adjudication"],
            "model_metadata": {"screening": screen_meta, "attack": attack_meta, "replication": replication_meta},
        },
        "observation": {"screening": screening, "attack": attack},
        "discovery": {
            "candidate_id": cid,
            "source_key": candidate.get("source_key"),
            "sources": candidate.get("sources", []),
            "url_context_metadata": {
                "screening": screen_meta.get("url_context_metadata", {}),
                "attack": attack_meta.get("url_context_metadata", {}),
                "replication": replication_meta.get("url_context_metadata", {}),
            },
        },
        "replication": replication,
        "acceptance": decision,
    }
    files: dict[str, bytes] = {}
    provenance: dict[str, dict[str, str]] = {}
    for key, value in values.items():
        rel = (root / f"{key}.json").as_posix()
        raw = pretty_bytes(value)
        files[rel] = raw
        provenance[key] = {"path": rel, "sha256": digest(raw)}
    audit_rel = (AUDIT_ROOT / f"{review_id}.md").as_posix()
    files[audit_rel] = (
        f"# Autonomous living review — {cid}\n\n"
        f"- review id: `{review_id}`\n"
        f"- executed UTC: `{iso(now)}`\n"
        f"- proposed disposition: `{decision['disposition']}`\n"
        "- authority: **Research proposal only until this PR is merged**\n\n"
        "## Screening\n\n" + screening["summary"] + "\n\n"
        "## Attack\n\n" + attack["exact_reason"] + "\n\n"
        "## Internal replication\n\n" + replication["independent_reason"] + "\n\n"
        "## Adjudication\n\n" + decision["rationale"] + "\n\n"
        "## Limits\n\n" + "\n".join(f"- {x}" for x in decision.get("limits", [])) + "\n"
    ).encode("utf-8")
    return files, provenance, audit_rel


def append_unique(registry: dict[str, Any], field: str, row: dict[str, Any], key: str) -> None:
    rows = registry.get(field)
    if not isinstance(rows, list):
        raise ReviewError(f"registry missing {field}")
    ident = row[key]
    if any(isinstance(x, dict) and x.get(key) == ident for x in rows):
        raise ReviewError(f"duplicate protected row: {ident}")
    registry[field] = [*rows, row]


def retry_block(cid: str, reason: str, now: datetime, *, status: str, hours: int) -> dict[str, Any]:
    rel = (ATTEMPTS / f"{cid}.json").as_posix()
    return {
        "status": status.lower(),
        "candidate_id": cid,
        "review_files": {},
        "inbox_files": {rel: pretty_bytes({
            "schema_version": "1.1",
            "program_id": "FAR-LIVING-AUTONOMOUS-REVIEW-001",
            "candidate_id": cid,
            "status": status,
            "reason": reason,
            "attempted_utc": iso(now),
            "next_retry_utc": iso(now + timedelta(hours=hours)),
        })},
    }


def source_block(cid: str, reason: str, now: datetime) -> dict[str, Any]:
    return retry_block(cid, reason, now, status="SOURCE_BLOCKED", hours=24)


def candidate_block(cid: str, reason: str, now: datetime) -> dict[str, Any]:
    return retry_block(cid, reason, now, status="REVIEW_RETRY_BLOCKED", hours=6)
