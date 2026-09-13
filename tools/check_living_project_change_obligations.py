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
        if promotion.get("candidate_id") != candidate_id:
            raise ObligationError(f"{candidate_id}: promotion authorization candidate mismatch")
        if promotion.get("lifecycle_stage") != "PROMOTION_PROPOSED":
            raise ObligationError(f"{candidate_id}: promotion authorization stage mismatch")
        if promotion.get("authorization_status") != "ACCEPTED_FOR_MECHANICAL_PROMOTION":
            raise ObligationError(f"{candidate_id}: promotion authorization status mismatch")

        snapshot = s_auths.get(candidate_id)
        if snapshot is None:
            raise ObligationError(f"{candidate_id}: missing snapshot authorization")
        for field in ("source_key", "review_basis", "disposition"):
            if snapshot.get(field) != review.get(field):
                raise ObligationError(f"{candidate_id}: snapshot authorization {field} mismatch")
        if snapshot.get("authorization_status") != "ACCEPTED_FOR_MECHANICAL_SNAPSHOT":
            raise ObligationError(f"{candidate_id}: snapshot authorization status mismatch")
        obligations.append({"candidate_id": candidate_id, "proposal_id": proposal_id})
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
        if git_show(root, source_ref, f"{CANDIDATE_PREFIX}{candidate_id}.json") is None:
            raise ObligationError(f"{candidate_id}: candidate missing from {source_ref}")
        proposal_path = f"{PROPOSAL_PREFIX}{proposal_id}.json"
        raw = git_show(root, source_ref, proposal_path)
        if raw is None:
            raise ObligationError(f"{candidate_id}: correction proposal {proposal_id} missing from {source_ref}")
        try:
            proposal = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise ObligationError(f"{proposal_id}: invalid proposal JSON: {exc}") from exc
        if not isinstance(proposal, dict):
            raise ObligationError(f"{proposal_id}: proposal must be an object")
        if proposal.get("proposal_id") != proposal_id or proposal.get("candidate_id") != candidate_id:
            raise ObligationError(f"{proposal_id}: identity binding mismatch")
        if proposal.get("lifecycle_stage") != "PROMOTION_PROPOSED":
            raise ObligationError(f"{proposal_id}: proposal stage mismatch")
        operations = proposal.get("operations")
        if not isinstance(operations, list) or not operations:
            raise ObligationError(f"{proposal_id}: project change requires nonempty operations")
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
            if git_show(root, source_ref, source_path) is None:
                raise ObligationError(f"{proposal_id}: missing payload {source_path}")


def check(root: Path, source_ref: str | None = None) -> list[str]:
    try:
        obligations = local_obligations(root)
        if source_ref:
            source_obligations(root, source_ref, obligations)
        return []
    except ObligationError as exc:
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
