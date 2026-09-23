from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools import living_implementation_contract as implementation
from tools import promote_living_research as promoter
from tools.living_autonomous_review_core import *
from tools.living_autonomous_review_model import *
from tools.living_autonomous_review_plan import *


def require_full_claim_coverage(record: dict[str, Any], claim_ids: set[str], label: str) -> None:
    covered = set(validate_claim_ids(record.get("evaluated_claim_ids"), claim_ids, f"{label} evaluated_claim_ids"))
    if covered != claim_ids:
        missing = sorted(claim_ids - covered)
        extra = sorted(covered - claim_ids)
        detail = []
        if missing:
            detail.append("missing=" + ",".join(missing))
        if extra:
            detail.append("extra=" + ",".join(extra))
        raise CandidateReviewError(f"{label}: incomplete frozen claim coverage ({'; '.join(detail)})")


def build_plan(root: Path, source_root: Path, model: Model, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    policy = load_json(root / POLICY)
    validate_policy(policy)
    cid = select_candidate(root, source_root, now)
    if cid is None:
        return {"status": "no_candidate", "review_files": {}, "inbox_files": {}}

    candidate_path = source_root / CANDIDATES / f"{cid}.json"
    if not candidate_path.is_file():
        return candidate_block(cid, "selected candidate file is missing", now)
    candidate_raw = candidate_path.read_bytes()
    try:
        candidate = promoter.loadb(candidate_raw, candidate_path.as_posix())
    except promoter.PromotionError as exc:
        return candidate_block(cid, f"candidate JSON is invalid: {exc}", now)
    if candidate.get("candidate_id") != cid:
        return candidate_block(cid, "candidate identity drift", now)
    if candidate.get("record_type") != "CANDIDATE_LITERATURE":
        return candidate_block(cid, "candidate record_type drift", now)
    source_key = candidate.get("source_key")
    if not isinstance(source_key, str) or not source_key.strip():
        return candidate_block(cid, "candidate source_key missing", now)
    if candidate.get("authority") != "Research" or candidate.get("lifecycle", {}).get("stage") != "DISCOVERED":
        return candidate_block(cid, "candidate authority/lifecycle drift", now)
    if not isinstance(candidate.get("sources"), list) or not candidate["sources"]:
        return candidate_block(cid, "candidate source records missing", now)

    urls = candidate_urls(candidate, policy["max_source_urls"])
    queue = load_json(source_root / STATE).get("core_claim_review_queue", [])
    matches = [x for x in queue if isinstance(x, dict) and x.get("candidate_id") == cid]
    if len(matches) != 1:
        return candidate_block(cid, "candidate queue identity is missing or duplicated", now)
    item = matches[0]
    ids_raw = item.get("claim_ids")
    if not isinstance(ids_raw, list) or not ids_raw or any(not isinstance(x, str) for x in ids_raw):
        return candidate_block(cid, "candidate queue claim binding malformed", now)
    if len(ids_raw) != len(set(ids_raw)):
        return candidate_block(cid, "candidate queue claim binding duplicated", now)
    ids = list(ids_raw)
    potential = candidate.get("potential_claim_ids")
    if not isinstance(potential, list) or any(not isinstance(x, str) for x in potential):
        return candidate_block(cid, "candidate potential_claim_ids malformed", now)
    if len(potential) != len(set(potential)):
        return candidate_block(cid, "candidate potential_claim_ids duplicated", now)
    if set(ids) != set(potential):
        return candidate_block(cid, "candidate queue/candidate claim binding drift", now)
    claims = claim_subset(root, ids)
    claim_ids = {x["id"] for x in claims if isinstance(x.get("id"), str)}
    if set(ids) != claim_ids:
        return candidate_block(cid, "candidate references unknown or missing canonical claim ids", now)
    if not urls or not claims:
        return source_block(cid, "candidate lacks a source URL or exact claim binding", now)

    try:
        screening, screen_meta = model.generate(
            role="screening",
            prompt=prompt_for("screening", candidate, claims, urls),
            schema=SCREEN_SCHEMA,
            urls=urls,
        )
        require_full_claim_coverage(screening, claim_ids, "screening")
        validate_claim_ids(screening.get("affected_claim_ids"), claim_ids, "screening affected_claim_ids")
        if not screening.get("primary_source_verified"):
            return source_block(cid, "screening did not verify a primary source", now)
        try:
            validate_source_binding(screening, screen_meta, "screening")
        except CandidateReviewError as exc:
            return source_block(cid, str(exc), now)

        attack, attack_meta = model.generate(
            role="attack",
            prompt=prompt_for("attack", candidate, claims, urls, {"screening": screening}),
            schema=ATTACK_SCHEMA,
            urls=urls,
        )
        require_full_claim_coverage(attack, claim_ids, "attack")
        validate_claim_ids(attack.get("affected_claim_ids"), claim_ids, "attack affected_claim_ids")
        try:
            validate_source_binding(attack, attack_meta, "attack")
        except CandidateReviewError as exc:
            return source_block(cid, str(exc), now)

        replication, replication_meta = model.generate(
            role="replication",
            prompt=prompt_for("replication", candidate, claims, urls),
            schema=REPLICATION_SCHEMA,
            urls=urls,
        )
        require_full_claim_coverage(replication, claim_ids, "replication")
        validate_claim_ids(replication.get("affected_claim_ids"), claim_ids, "replication affected_claim_ids")
        try:
            validate_source_binding(replication, replication_meta, "replication")
        except CandidateReviewError as exc:
            return source_block(cid, str(exc), now)

        common_sources = record_sources(screening) & record_sources(attack) & record_sources(replication)
        if not common_sources:
            return source_block(cid, "review roles lack one common retrieved primary source", now)

        decision, decision_meta = model.generate(
            role="adjudication",
            prompt=prompt_for(
                "adjudication",
                candidate,
                claims,
                urls,
                {"screening": screening, "attack": attack, "replication": replication},
            ),
            schema=ADJUDICATION_SCHEMA,
        )
        validate_decision(
            decision,
            policy,
            root,
            claim_ids,
            screening,
            attack,
            replication,
            screen_meta,
            attack_meta,
            replication_meta,
        )

        review_files, provenance, audit_rel = review_artifacts(
            cid, candidate, claims, screening, screen_meta, attack, attack_meta,
            replication, replication_meta, decision, decision_meta, now,
        )
        candidate_hash = digest(candidate_raw)
        freeze_tag = candidate_hash[:12].upper()
        proposal_id = f"FAR-LIVING-PROP-AUTO-{cid.removeprefix('FAR-LIT-')}-{freeze_tag}"
        impl_id = f"FAR-LIVING-IMPL-AUTO-{cid.removeprefix('FAR-LIT-')}-{freeze_tag}"
        disposition = decision["disposition"]
        review_row: dict[str, Any] = {
            "candidate_id": cid,
            "source_key": source_key,
            "disposition": disposition,
            "reviewed_on": now.date().isoformat(),
            "review_basis": audit_rel,
            "suppress_from_core_claim_review_queue": True,
        }
        inbox_files: dict[str, bytes] = {}
        promotion_ops: list[dict[str, Any]] = []
        implementation_ops: list[dict[str, Any]] = []
        scientific_replacements: dict[str, bytes] = {}
        implementation_replacements: dict[str, bytes] = {}

        if disposition == "PROJECT_CHANGE_REQUIRED":
            scientific_replacements = generate_replacements(
                model,
                kind="scientific",
                targets=decision["scientific_targets"],
                root=root,
                context={"screening": screening, "attack": attack, "replication": replication, "adjudication": decision},
                max_bytes=policy["max_total_replacement_bytes"],
            )
            enforce_total_replacement_bytes(policy["max_total_replacement_bytes"], scientific_replacements)
            for target, raw in scientific_replacements.items():
                source_path = (PROMOTION_PAYLOADS / proposal_id / target).as_posix()
                before = promoter.mainbytes(root, target)
                promotion_ops.append({
                    "op": "write_file",
                    "path": target,
                    "source_path": source_path,
                    "expected_main_sha256": "ABSENT" if before is None else digest(before),
                    "result_sha256": digest(raw),
                })
                review_files[source_path] = raw
            if not promotion_ops:
                raise CandidateReviewError("PROJECT_CHANGE_REQUIRED produced no scientific operations")
            proposal = {
                "schema_version": "1.0",
                "proposal_id": proposal_id,
                "candidate_id": cid,
                "candidate_sha256": candidate_hash,
                "lifecycle_stage": "PROMOTION_PROPOSED",
                "provenance": provenance,
                "operations": promotion_ops,
            }
            proposal_raw = pretty_bytes(proposal)
            review_files[(PROMOTION_PROPOSALS / f"{proposal_id}.json").as_posix()] = proposal_raw
            review_row.update({
                "proposal_id": proposal_id,
                "implementation_required": decision["implementation_required"],
                "implementation_proposal_id": impl_id if decision["implementation_required"] else None,
            })
            if decision["implementation_required"]:
                implementation_replacements = generate_replacements(
                    model,
                    kind="implementation",
                    targets=decision["implementation_targets"],
                    root=root,
                    context={"screening": screening, "attack": attack, "replication": replication, "adjudication": decision},
                    max_bytes=policy["max_total_replacement_bytes"],
                )
                enforce_total_replacement_bytes(
                    policy["max_total_replacement_bytes"], scientific_replacements, implementation_replacements
                )
                for target, raw in implementation_replacements.items():
                    source_path = (IMPLEMENTATION_PAYLOADS / impl_id / target).as_posix()
                    before = implementation.read_regular(root, target)
                    implementation_ops.append({
                        "op": "write_file",
                        "path": target,
                        "source_path": source_path,
                        "expected_main_sha256": "ABSENT" if before is None else digest(before),
                        "result_sha256": digest(raw),
                    })
                    review_files[source_path] = raw
                if not implementation_ops:
                    raise CandidateReviewError("implementation_required produced no implementation operations")
                impl_proposal = {
                    "proposal_id": impl_id,
                    "candidate_id": cid,
                    "candidate_sha256": candidate_hash,
                    "lifecycle_stage": "IMPLEMENTATION_PROPOSED",
                    "operations": implementation_ops,
                }
                impl_raw = pretty_bytes(impl_proposal)
                review_files[(IMPLEMENTATION_PROPOSALS / f"{impl_id}.json").as_posix()] = impl_raw

        reviews = load_json(root / REVIEWS)
        append_unique(reviews, "reviewed_candidates", review_row, "candidate_id")
        review_files[REVIEWS.as_posix()] = pretty_bytes(reviews)

        promotion_policy = load_json(root / promoter.POLICY)
        promoter.validate_policy(promotion_policy)
        snapshot_dispositions = set(promotion_policy.get("snapshot_review_dispositions", []))
        excluded_dispositions = set(promotion_policy.get("excluded_review_dispositions", []))
        if disposition in snapshot_dispositions:
            snapshots = load_json(root / SNAPSHOT_AUTHS)
            append_unique(snapshots, "authorizations", {
                "candidate_id": cid,
                "candidate_sha256": candidate_hash,
                "source_key": source_key,
                "disposition": disposition,
                "review_basis": audit_rel,
                "review_basis_sha256": digest(review_files[audit_rel]),
                "review_record_sha256": promoter.canonical_json_sha(review_row),
                "authorization_status": "ACCEPTED_FOR_MECHANICAL_SNAPSHOT",
            }, "candidate_id")
            review_files[SNAPSHOT_AUTHS.as_posix()] = pretty_bytes(snapshots)
        elif disposition not in excluded_dispositions:
            raise ReviewError(f"disposition is in neither promotion snapshot nor exclusion policy: {disposition}")

        if disposition == "PROJECT_CHANGE_REQUIRED":
            proposal_raw = review_files[(PROMOTION_PROPOSALS / f"{proposal_id}.json").as_posix()]
            auths = load_json(root / PROMOTION_AUTHS)
            append_unique(auths, "authorizations", {
                "proposal_id": proposal_id,
                "candidate_id": cid,
                "proposal_sha256": digest(proposal_raw),
                "candidate_sha256": candidate_hash,
                "operations_sha256": promoter.canonical_json_sha(promotion_ops),
                "lifecycle_stage": "PROMOTION_PROPOSED",
                "authorization_status": "ACCEPTED_FOR_MECHANICAL_PROMOTION",
                "provenance_sha256": {key: value["sha256"] for key, value in provenance.items()},
            }, "proposal_id")
            review_files[PROMOTION_AUTHS.as_posix()] = pretty_bytes(auths)
            if decision["implementation_required"]:
                impl_raw = review_files[(IMPLEMENTATION_PROPOSALS / f"{impl_id}.json").as_posix()]
                auths = load_json(root / IMPLEMENTATION_AUTHS)
                append_unique(auths, "authorizations", {
                    "proposal_id": impl_id,
                    "candidate_id": cid,
                    "proposal_sha256": digest(impl_raw),
                    "candidate_sha256": candidate_hash,
                    "operations_sha256": implementation.canonical_json_sha(implementation_ops),
                    "review_record_sha256": implementation.canonical_json_sha(review_row),
                    "authorization_status": "ACCEPTED_FOR_PROTECTED_IMPLEMENTATION_PR",
                }, "proposal_id")
                review_files[IMPLEMENTATION_AUTHS.as_posix()] = pretty_bytes(auths)

        review_files[(CANDIDATES / f"{cid}.json").as_posix()] = candidate_raw
        return {
            "status": "review_ready",
            "candidate_id": cid,
            "candidate_sha256": candidate_hash,
            "disposition": disposition,
            "review_files": review_files,
            "inbox_files": inbox_files,
        }
    except CandidateReviewError as exc:
        return candidate_block(cid, str(exc), now)
