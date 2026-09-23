#!/usr/bin/env python3
"""Prepare one bounded autonomous living-research review package.

The runner is intentionally split across two authority surfaces:

- ``inbox/`` contains only retry/backoff records that may be written to the
  permanent noncanonical living-research branch before human review.
- ``review/`` contains the scientific review, exact candidate snapshot,
  governed authorizations, and any proposed correction payloads. Those bytes
  acquire protected authority only if a human merges the generated review PR.

After that merge, the existing living-research branch rebuild carries the
human-approved proposal/payload bytes forward from protected ``main`` and the
existing promotion / implementation runners may open separate correction PRs.
No automated path in this module merges any PR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

from tools import living_implementation_contract as implementation
from tools import promote_living_research as promoter

POLICY = Path("research/living/autonomous-review-policy-v1.0.json")
REVIEWS = Path("research/living/review-dispositions-v1.0.json")
SNAPSHOT_AUTHS = Path("research/living/snapshot-authorizations-v1.0.json")
PROMOTION_AUTHS = Path("research/living/promotion-authorizations-v1.0.json")
IMPLEMENTATION_AUTHS = Path("research/living/implementation-authorizations-v1.0.json")
CLAIMS = Path("theory/terminal/project-far-core-theory-v1.1.json")
STATE = Path("research/living/repository-state-v1.0.json")
CANDIDATES = Path("research/living/inbox/candidates")
ATTEMPTS = Path("research/living/inbox/autonomous-review-attempts")
PROMOTION_PROPOSALS = Path("research/living/inbox/promotion-proposals")
PROMOTION_PAYLOADS = Path("research/living/inbox/promotion-payloads")
IMPLEMENTATION_PROPOSALS = Path("research/living/inbox/implementation-proposals")
IMPLEMENTATION_PAYLOADS = Path("research/living/inbox/implementation-payloads")
REVIEW_ROOT = Path("research/living/autonomous-review")
AUDIT_ROOT = Path("docs/audits/living-autonomous-review")

CID_RE = re.compile(r"FAR-LIT-[0-9A-F]{16}")
ALLOWED = {
    "IRRELEVANT_FALSE_POSITIVE",
    "ADJACENT_NO_CONTRADICTION",
    "N1_PRIOR_ART_LEAD",
    "PROJECT_CHANGE_REQUIRED",
}
PRIOR_ART_STRENGTH = {"NONE": 0, "ADJACENT": 1, "DIRECT": 2, "STRONG": 3}


class ReviewError(RuntimeError):
    """Repository/policy invariant failure. This should stop the workflow."""


class CandidateReviewError(RuntimeError):
    """Candidate- or model-specific failure. This is backoff/retryable."""


class ModelRequestError(CandidateReviewError):
    pass


class Model(Protocol):
    def generate(
        self,
        *,
        role: str,
        prompt: str,
        schema: dict[str, Any],
        urls: list[str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]: ...


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ReviewError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"{path}: expected JSON object")
    return value


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_policy(policy: dict[str, Any]) -> None:
    expected = {
        "schema_version": "1.1",
        "program_id": "FAR-LIVING-AUTONOMOUS-REVIEW-001",
        "authority": "Research",
        "source_pr": 490,
        "source_branch": "automation/living-research-inbox",
        "provider": "google_gemini",
        "default_model": "gemini-3.8-flash",
    }
    for key, wanted in expected.items():
        if policy.get(key) != wanted:
            raise ReviewError(f"autonomous-review policy drift: {key}")
    values = policy.get("allowed_dispositions")
    if not isinstance(values, list) or len(values) != len(ALLOWED) or set(values) != ALLOWED:
        raise ReviewError("autonomous-review disposition contract drift")
    if policy.get("required_roles") != ["screening", "attack", "replication", "adjudication"]:
        raise ReviewError("autonomous-review role contract drift")
    for key in (
        "max_candidates_per_run",
        "max_source_urls",
        "max_scientific_targets",
        "max_implementation_targets",
        "max_total_replacement_bytes",
    ):
        if not isinstance(policy.get(key), int) or policy[key] <= 0:
            raise ReviewError(f"invalid autonomous-review bound: {key}")
    change = policy.get("project_change_gate")
    if not isinstance(change, dict):
        raise ReviewError("project_change_gate missing")
    required_change_keys = {
        "require_verified_primary_source",
        "require_exact_claim_binding",
        "require_premise_match",
        "require_scope_match",
        "require_reproducible_attack",
        "require_attack_contradiction",
        "require_replication",
        "require_replication_contradiction",
        "require_matching_claim_id",
        "require_nonempty_scientific_operations",
    }
    if set(change) != required_change_keys or any(change[k] is not True for k in required_change_keys):
        raise ReviewError("project_change_gate drift")
    prior = policy.get("prior_art_gate")
    if not isinstance(prior, dict):
        raise ReviewError("prior_art_gate missing")
    if set(prior) != {
        "require_attack_prior_art",
        "require_replication_prior_art",
        "minimum_strength",
        "require_matching_claim_id",
    }:
        raise ReviewError("prior_art_gate drift")
    if prior["require_attack_prior_art"] is not True or prior["require_replication_prior_art"] is not True:
        raise ReviewError("prior_art_gate must require both internal roles")
    if prior["require_matching_claim_id"] is not True or prior["minimum_strength"] not in PRIOR_ART_STRENGTH:
        raise ReviewError("invalid prior_art_gate")


def reviewed_ids(root: Path) -> set[str]:
    rows = load_json(root / REVIEWS).get("reviewed_candidates")
    if not isinstance(rows, list):
        raise ReviewError("review registry missing reviewed_candidates")
    ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("candidate_id"), str):
            raise ReviewError("malformed review row")
        cid = row["candidate_id"]
        if cid in ids:
            raise ReviewError(f"duplicate reviewed candidate: {cid}")
        ids.add(cid)
    return ids


def retry_blocked(source_root: Path, cid: str, now: datetime) -> bool:
    path = source_root / ATTEMPTS / f"{cid}.json"
    if not path.is_file():
        return False
    try:
        retry = datetime.fromisoformat(str(load_json(path)["next_retry_utc"]).replace("Z", "+00:00"))
    except Exception:
        return False
    return retry.astimezone(timezone.utc) > now


def select_candidate(root: Path, source_root: Path, now: datetime) -> str | None:
    queue = load_json(source_root / STATE).get("core_claim_review_queue")
    if not isinstance(queue, list):
        raise ReviewError("source repository state missing core_claim_review_queue")
    reviewed = reviewed_ids(root)
    ranked: list[tuple[int, int, str]] = []
    for item in queue:
        if not isinstance(item, dict):
            continue
        cid = item.get("candidate_id")
        if not isinstance(cid, str) or CID_RE.fullmatch(cid) is None or cid in reviewed:
            continue
        if retry_blocked(source_root, cid, now):
            continue
        attention = item.get("attention_terms") if isinstance(item.get("attention_terms"), list) else []
        claims = item.get("claim_ids") if isinstance(item.get("claim_ids"), list) else []
        ranked.append((-len(attention), -len(claims), cid))
    return min(ranked)[2] if ranked else None


def candidate_urls(candidate: dict[str, Any], limit: int) -> list[str]:
    out: list[str] = []
    for source in candidate.get("sources", []):
        if not isinstance(source, dict):
            continue
        for key in ("url", "doi"):
            value = source.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            value = value.strip()
            if key == "doi" and not value.startswith("http"):
                value = "https://doi.org/" + value.removeprefix("doi:")
            if value.startswith(("https://", "http://")) and value not in out:
                out.append(value)
                if len(out) >= limit:
                    return out
    return out


def claim_subset(root: Path, ids: list[str]) -> list[dict[str, Any]]:
    claims = load_json(root / CLAIMS).get("claims")
    if not isinstance(claims, list):
        raise ReviewError("canonical claim ledger missing claims")
    wanted = set(ids)
    return [x for x in claims if isinstance(x, dict) and x.get("id") in wanted]


def object_schema(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {"type": "object", "properties": properties, "required": required}


STR = {"type": "string"}
BOOL = {"type": "boolean"}
STRS = {"type": "array", "items": STR}
STRENGTH = {"type": "string", "enum": list(PRIOR_ART_STRENGTH)}
SCREEN_SCHEMA = object_schema(
    {
        "primary_source_verified": BOOL,
        "relevant": BOOL,
        "source_urls_used": STRS,
        "affected_claim_ids": STRS,
        "premise_match": BOOL,
        "scope_match": BOOL,
        "summary": STR,
        "evidence_locations": STRS,
        "limits": STRS,
    },
    [
        "primary_source_verified", "relevant", "source_urls_used", "affected_claim_ids",
        "premise_match", "scope_match", "summary", "evidence_locations", "limits",
    ],
)
ATTACK_SCHEMA = object_schema(
    {
        "contradiction_found": BOOL,
        "prior_art_found": BOOL,
        "prior_art_strength": STRENGTH,
        "source_urls_used": STRS,
        "affected_claim_ids": STRS,
        "exact_reason": STR,
        "reproducible_attack": STR,
        "source_locations": STRS,
        "limits": STRS,
    },
    [
        "contradiction_found", "prior_art_found", "prior_art_strength", "source_urls_used",
        "affected_claim_ids", "exact_reason", "reproducible_attack", "source_locations", "limits",
    ],
)
REPLICATION_SCHEMA = object_schema(
    {
        "contradiction_found": BOOL,
        "prior_art_found": BOOL,
        "prior_art_strength": STRENGTH,
        "source_urls_used": STRS,
        "affected_claim_ids": STRS,
        "independent_reason": STR,
        "attack_reproduced": BOOL,
        "source_locations": STRS,
        "limits": STRS,
    },
    [
        "contradiction_found", "prior_art_found", "prior_art_strength", "source_urls_used",
        "affected_claim_ids", "independent_reason", "attack_reproduced", "source_locations", "limits",
    ],
)
ADJUDICATION_SCHEMA = object_schema(
    {
        "disposition": {"type": "string", "enum": sorted(ALLOWED)},
        "project_change_required": BOOL,
        "scientific_targets": STRS,
        "implementation_required": BOOL,
        "implementation_targets": STRS,
        "rationale": STR,
        "limits": STRS,
    },
    [
        "disposition", "project_change_required", "scientific_targets",
        "implementation_required", "implementation_targets", "rationale", "limits",
    ],
)
REPLACEMENTS_SCHEMA = object_schema(
    {
        "files": {
            "type": "array",
            "items": object_schema({"path": STR, "content": STR}, ["path", "content"]),
        }
    },
    ["files"],
)
