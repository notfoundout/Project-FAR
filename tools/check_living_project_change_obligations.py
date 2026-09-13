#!/usr/bin/env python3
"""Fail closed when governed living research requires a Project FAR correction."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from tools import promote_living_research as promoter

REVIEWS = Path("research/living/review-dispositions-v1.0.json")
PROMOTION_AUTHS = Path("research/living/promotion-authorizations-v1.0.json")
SNAPSHOT_AUTHS = Path("research/living/snapshot-authorizations-v1.0.json")
PROMOTION_POLICY = Path("research/living/promotion-policy-v1.0.json")
CHANGE_POLICY = Path("research/living/project-change-policy-v1.0.json")
CHANGE_DISPOSITION = "PROJECT_CHANGE_REQUIRED"
SOURCE_PR = 490
SOURCE_BRANCH = "automation/living-research-inbox"
DEFAULT_SOURCE_REF = f"refs/remotes/origin/{SOURCE_BRANCH}"
PROPOSAL_PREFIX = "research/living/inbox/promotion-proposals/"
PAYLOAD_PREFIX = "research/living/inbox/promotion-payloads/"
CANDIDATE_PREFIX = "research/living/inbox/candidates/"
PROPOSAL_RE = re.compile(r"FAR-LIVING-PROP-[A-Z0-9][A-Z0-9._-]{0,63}")
CANDIDATE_RE = re.compile(r"FAR-LIT-[0-9A-F]{16}")
REQUIRED_REVIEW_FIELDS = {
    "candidate_id",
    "source_key",
    "disposition",
    "reviewed_on",
    "review_basis",
    "proposal_id",
    "suppress_from_core_claim_review_queue",
}
SNAPSHOT_AUTH_FIELDS = {
    "candidate_id",
    "candidate_sha256",
    "source_key",
    "disposition",
    "review_basis",
    "review_basis_sha256",
    "review_record_sha256",
    "authorization_status",
}
PROMOTION_AUTH_FIELDS = {
    "proposal_id",
    "candidate_id",
    "proposal_sha256",
    "candidate_sha256",
    "operations_sha256",
    "lifecycle_stage",
    "authorization_status",
    "provenance_sha256",
}


class ObligationError(RuntimeError):
    pass


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ObligationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ObligationError(f"{path}: expected JSON object")
    return value


def unique(rows: Any, key: str, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ObligationError(f"{label}: expected array")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(key), str):
            raise ObligationError(f"{label}: malformed row")
        ident = row[key]
        if ident in result:
            raise ObligationError(f"{label}: duplicate {key} {ident}")
        result[ident] = row
    return result


def local_obligations(root: Path) -> list[dict[str, str]]:
    reviews = load(root / REVIEWS)
    promotion_auths = load(root / PROMOTION_AUTHS)
    snapshot_auths = load(root / SNAPSHOT_AUTHS)
    promotion_policy = load(root / PROMOTION_POLICY)
    change_policy = load(root / CHANGE_POLICY)

    if change_policy.get("program_id") != "FAR-LIVING-PROJECT-CHANGE-001":
        raise ObligationError("project-change policy identity drift")
    if change_policy.get("authority") != "Research":
        raise ObligationError("project-change policy authority drift")
    if change_policy.get("disposition") != CHANGE_DISPOSITION:
        raise ObligationError("project-change disposition drift")
    if change_policy.get("source_pr") != SOURCE_PR or change_policy.get("source_branch") != SOURCE_BRANCH:
        raise ObligationError("project-change source identity drift")
    required_fields = change_policy.get("required_review_fields")
    if not isinstance(required_fields, list) or set(required_fields) != REQUIRED_REVIEW_FIELDS:
        raise ObligationError("project-change required-review fields drift")

    allowed_dispositions = reviews.get("allowed_dispositions")
    if not isinstance(allowed_dispositions, list) or CHANGE_DISPOSITION not in allowed_dispositions:
        raise ObligationError(f"review registry must allow {CHANGE_DISPOSITION}")
    snapshots = promotion_policy.get("snapshot_review_dispositions")
    if not isinstance(snapshots, list) or CHANGE_DISPOSITION not in snapshots:
        raise ObligationError(f"promotion policy must snapshot {CHANGE_DISPOSITION}")

    review_rows = reviews.get("reviewed_candidates")
    if not isinstance(review_rows, list):
        raise ObligationError("reviewed_candidates must be an array")
    p_auths = unique(promotion_auths.get("authorizations"), "proposal_id", "promotion authorizations")
    s_auths = unique(snapshot_auths.get("authorizations"), "candidate_id", "snapshot authorizations")

    obligations: list[dict[str, str]] = []
    for review in review_rows:
        if not isinstance(review, dict) or review.get("disposition") != CHANGE_DISPOSITION:
            continue
        missing = REQUIRED_REVIEW_FIELDS - set(review)
        if missing:
            raise ObligationError("project-change review missing fields: " + ", ".join(sorted(missing)))
        candidate_id = review.get("candidate_id")
        proposal_id = review.get("proposal_id")
        if not isinstance(candidate_id, str) or CANDIDATE_RE.fullmatch(candidate_id) is None:
            raise ObligationError("project-change review has invalid candidate_id")
        if not isinstance(proposal_id, str) or PROPOSAL_RE.fullmatch(proposal_id) is None:
            raise ObligationError(f"{candidate_id}: {CHANGE_DISPOSITION} requires exact proposal_id")
        for field in ("source_key", "reviewed_on", "review_basis"):
            if not isinstance(review.get(field), str) or not review[field].strip():
                raise ObligationError(f"{candidate_id}: project-change review has invalid {field}")
        if review.get("suppress_from_core_claim_review_queue") is not True:
            raise ObligationError(f"{candidate_id}: accepted project change must leave the metadata-only review queue")

        promotion = p_auths.get(proposal_id)
        if promotion is None:
            raise ObligationError(f"{candidate_id}: missing promotion authorization for {proposal_id}")
        if set(promotion) != PROMOTION_AUTH_FIELDS:
            raise ObligationError(f"{candidate_id}: promotion authorization fields are malformed")
        if promotion.get("candidate_id") != candidate_id:
            raise ObligationError(f"{candidate_id}: promotion authorization candidate mismatch")
        if promotion.get("lifecycle_stage") != "PROMOTION_PROPOSED":
            raise ObligationError(f"{candidate_id}: promotion authorization stage mismatch")
        if promotion.get("authorization_status") != "ACCEPTED_FOR_MECHANICAL_PROMOTION":
            raise ObligationError(f"{candidate_id}: promotion authorization status mismatch")
        for field in ("proposal_sha256", "candidate_sha256", "operations_sha256"):
            value = promotion.get(field)
            if not isinstance(value, str) or promoter.HEX64_RE.fullmatch(value) is None:
                raise ObligationError(f"{candidate_id}: promotion authorization {field} is malformed")
        provenance_hashes = promotion.get("provenance_sha256")
        if (
            not isinstance(provenance_hashes, dict)
            or set(provenance_hashes) != set(promoter.PROV_KEYS)
            or any(
                not isinstance(provenance_hashes[key], str)
                or promoter.HEX64_RE.fullmatch(provenance_hashes[key]) is None
                for key in promoter.PROV_KEYS
            )
        ):
            raise ObligationError(f"{candidate_id}: promotion authorization provenance hashes are malformed")

        snapshot = s_auths.get(candidate_id)
        if snapshot is None:
            raise ObligationError(f"{candidate_id}: missing snapshot authorization")
        if set(snapshot) != SNAPSHOT_AUTH_FIELDS:
            raise ObligationError(f"{candidate_id}: snapshot authorization fields are malformed")
        for field in ("candidate_sha256", "review_basis_sha256", "review_record_sha256"):
            value = snapshot.get(field)
            if not isinstance(value, str) or promoter.HEX64_RE.fullmatch(value) is None:
                raise ObligationError(f"{candidate_id}: snapshot authorization {field} is malformed")
        for field in ("source_key", "review_basis", "disposition"):
            if snapshot.get(field) != review.get(field):
                raise ObligationError(f"{candidate_id}: snapshot authorization {field} mismatch")
        if snapshot.get("authorization_status") != "ACCEPTED_FOR_MECHANICAL_SNAPSHOT":
            raise ObligationError(f"{candidate_id}: snapshot authorization status mismatch")
        if snapshot["review_record_sha256"] != promoter.canonical_json_sha(review):
            raise ObligationError(f"{candidate_id}: snapshot authorization review-record hash mismatch")
        try:
            basis_path = promoter.safe(review["review_basis"])
            basis = promoter.mainbytes(root, basis_path)
        except promoter.PromotionError as exc:
            raise ObligationError(f"{candidate_id}: invalid review-basis path: {exc}") from exc
        if basis is None or promoter.h(basis) != snapshot["review_basis_sha256"]:
            raise ObligationError(f"{candidate_id}: snapshot authorization review-basis hash mismatch")

        obligations.append(
            {
                "candidate_id": candidate_id,
                "proposal_id": proposal_id,
                "snapshot_candidate_sha256": snapshot["candidate_sha256"],
                "promotion_candidate_sha256": promotion["candidate_sha256"],
                "proposal_sha256": promotion["proposal_sha256"],
                "operations_sha256": promotion["operations_sha256"],
                **{
                    f"provenance_{key}_sha256": provenance_hashes[key]
                    for key in promoter.PROV_KEYS
                },
            }
        )
    return obligations


def git_show(root: Path, ref: str, path: str) -> bytes | None:
    result = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=root, capture_output=True, check=False)
    return result.stdout if result.returncode == 0 else None


def fetch_default_source(root: Path) -> str:
    result = subprocess.run(
        [
            "git",
            "fetch",
            "--no-tags",
            "origin",
            f"+refs/heads/{SOURCE_BRANCH}:{DEFAULT_SOURCE_REF}",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ObligationError(f"failed to fetch permanent living-research source: {detail}")
    return DEFAULT_SOURCE_REF


def source_obligations(root: Path, source_ref: str, obligations: list[dict[str, str]]) -> None:
    for obligation in obligations:
        candidate_id = obligation["candidate_id"]
        proposal_id = obligation["proposal_id"]
        candidate_raw = git_show(root, source_ref, f"{CANDIDATE_PREFIX}{candidate_id}.json")
        if candidate_raw is None:
            raise ObligationError(f"{candidate_id}: candidate missing from {source_ref}")
        candidate_sha = promoter.h(candidate_raw)
        if candidate_sha != obligation["snapshot_candidate_sha256"]:
            raise ObligationError(f"{candidate_id}: snapshot authorization candidate hash mismatch")
        if candidate_sha != obligation["promotion_candidate_sha256"]:
            raise ObligationError(f"{candidate_id}: promotion authorization candidate hash mismatch")

        proposal_path = f"{PROPOSAL_PREFIX}{proposal_id}.json"
        raw = git_show(root, source_ref, proposal_path)
        if raw is None:
            raise ObligationError(f"{candidate_id}: correction proposal {proposal_id} missing from {source_ref}")
        if promoter.h(raw) != obligation["proposal_sha256"]:
            raise ObligationError(f"{proposal_id}: protected proposal hash mismatch")
        try:
            proposal = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise ObligationError(f"{proposal_id}: invalid proposal JSON: {exc}") from exc
        if not isinstance(proposal, dict):
            raise ObligationError(f"{proposal_id}: proposal must be an object")
        if proposal.get("proposal_id") != proposal_id or proposal.get("candidate_id") != candidate_id:
            raise ObligationError(f"{proposal_id}: identity binding mismatch")
        if proposal.get("candidate_sha256") != candidate_sha:
            raise ObligationError(f"{proposal_id}: proposal candidate hash mismatch")
        if proposal.get("lifecycle_stage") != "PROMOTION_PROPOSED":
            raise ObligationError(f"{proposal_id}: proposal stage mismatch")
        operations = proposal.get("operations")
        if not isinstance(operations, list) or not operations:
            raise ObligationError(f"{proposal_id}: project change requires nonempty operations")
        if promoter.canonical_json_sha(operations) != obligation["operations_sha256"]:
            raise ObligationError(f"{proposal_id}: protected operation-set hash mismatch")

        provenance = proposal.get("provenance")
        if not isinstance(provenance, dict) or set(provenance) != set(promoter.PROV_KEYS):
            raise ObligationError(f"{proposal_id}: incomplete provenance")
        for key in promoter.PROV_KEYS:
            item = provenance[key]
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                raise ObligationError(f"{proposal_id}: malformed {key} provenance")
            expected = obligation[f"provenance_{key}_sha256"]
            if item.get("sha256") != expected:
                raise ObligationError(f"{proposal_id}: protected {key} provenance hash mismatch")
            try:
                path = promoter.safe(item.get("path"))
                current = promoter.mainbytes(root, path)
            except promoter.PromotionError as exc:
                raise ObligationError(f"{proposal_id}: invalid {key} provenance path: {exc}") from exc
            if current is None or promoter.h(current) != expected:
                raise ObligationError(f"{proposal_id}: current {key} provenance hash mismatch")

        seen: set[str] = set()
        for operation in operations:
            if not isinstance(operation, dict) or operation.get("op") != "write_file":
                raise ObligationError(f"{proposal_id}: only write_file operations are permitted")
            target = operation.get("path")
            source_path = operation.get("source_path")
            if not isinstance(target, str) or not target or target in seen:
                raise ObligationError(f"{proposal_id}: malformed or duplicate target")
            seen.add(target)
            prefix = f"{PAYLOAD_PREFIX}{proposal_id}/"
            if not isinstance(source_path, str) or not source_path.startswith(prefix):
                raise ObligationError(f"{proposal_id}: payload path is outside proposal directory")
            payload = git_show(root, source_ref, source_path)
            if payload is None:
                raise ObligationError(f"{proposal_id}: missing payload {source_path}")
            result_sha = operation.get("result_sha256")
            if not isinstance(result_sha, str) or result_sha != promoter.h(payload):
                raise ObligationError(f"{proposal_id}: payload hash mismatch for {target}")


def check(root: Path, source_ref: str | None = None) -> list[str]:
    try:
        obligations = local_obligations(root)
        if source_ref:
            source_obligations(root, source_ref, obligations)
        return []
    except (ObligationError, promoter.PromotionError) as exc:
        return [str(exc)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-ref")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    try:
        source_ref = args.source_ref or fetch_default_source(root)
    except ObligationError as exc:
        print(f"living project-change obligation failed: {exc}", file=sys.stderr)
        return 2
    errors = check(root, source_ref)
    if errors:
        for error in errors:
            print(f"living project-change obligation failed: {error}", file=sys.stderr)
        return 2
    print("living project-change obligations: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
