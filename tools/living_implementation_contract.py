#!/usr/bin/env python3
"""Pure contract for separately authorized living-research implementation proposals."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

CHANGE_DISPOSITION = "PROJECT_CHANGE_REQUIRED"
CANDIDATE_PREFIX = "research/living/inbox/candidates"
PROPOSAL_PREFIX = "research/living/inbox/implementation-proposals"
PAYLOAD_PREFIX = "research/living/inbox/implementation-payloads"
REVIEWS = "research/living/review-dispositions-v1.0.json"
CHANGE_POLICY = "research/living/project-change-policy-v1.0.json"
IMPLEMENTATION_POLICY = "research/living/implementation-policy-v1.0.json"
IMPLEMENTATION_AUTHS = "research/living/implementation-authorizations-v1.0.json"
CANDIDATE_RE = re.compile(r"FAR-LIT-[0-9A-F]{16}")
PROPOSAL_RE = re.compile(r"FAR-LIVING-IMPL-[A-Z0-9][A-Z0-9._-]{0,63}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
AUTH_FIELDS = {
    "proposal_id", "candidate_id", "proposal_sha256", "candidate_sha256",
    "operations_sha256", "review_record_sha256", "authorization_status",
}


class ImplementationContractError(RuntimeError):
    pass


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json_sha(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    return sha256(raw.encode("utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ImplementationContractError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ImplementationContractError(f"expected object: {path}")
    return value


def safe_path(raw: str) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw):
        raise ImplementationContractError("unsafe repository path")
    path = PurePosixPath(raw)
    if path.is_absolute() or "." in path.parts or ".." in path.parts or any(not p or p.strip() != p for p in path.parts):
        raise ImplementationContractError(f"unsafe repository path: {raw}")
    return path.as_posix()


def under(path: str, root: str) -> bool:
    parts = PurePosixPath(path).parts
    root_parts = PurePosixPath(root).parts
    return parts[: len(root_parts)] == root_parts


def validate_policy(policy: dict[str, Any]) -> None:
    expected = {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-IMPLEMENTATION-001",
        "authority": "Research",
        "source_pr": 490,
        "source_branch": "automation/living-research-inbox",
        "proposal_stage": "IMPLEMENTATION_PROPOSED",
        "authorization_status": "ACCEPTED_FOR_PROTECTED_IMPLEMENTATION_PR",
    }
    for key, wanted in expected.items():
        if policy.get(key) != wanted:
            raise ImplementationContractError(f"implementation policy drift: {key}")
    for key in ("write_roots", "write_exact_paths"):
        values = policy.get(key)
        if not isinstance(values, list) or not values or len(values) != len(set(values)):
            raise ImplementationContractError(f"implementation policy {key} malformed")
        if any(not isinstance(item, str) or not item for item in values):
            raise ImplementationContractError(f"implementation policy {key} malformed")


def validate_target(path: str, policy: dict[str, Any]) -> str:
    path = safe_path(path)
    if path in set(policy["write_exact_paths"]):
        return path
    if not any(under(path, root) for root in policy["write_roots"]):
        raise ImplementationContractError(f"target outside implementation surface: {path}")
    return path


def read_regular(root: Path, raw: str) -> bytes | None:
    path = safe_path(raw)
    current = root
    for part in PurePosixPath(path).parts:
        current = current / part
        if current.is_symlink():
            raise ImplementationContractError(f"symlink path rejected: {path}")
    if not current.exists():
        return None
    if not current.is_file():
        raise ImplementationContractError(f"non-file path rejected: {path}")
    return current.read_bytes()


def expected_preimage(root: Path, target: str) -> str:
    raw = read_regular(root, target)
    return "ABSENT" if raw is None else sha256(raw)


def _unique(rows: Any, key: str, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ImplementationContractError(f"{label}: expected array")
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(key), str):
            raise ImplementationContractError(f"{label}: malformed row")
        ident = row[key]
        if ident in out:
            raise ImplementationContractError(f"{label}: duplicate {ident}")
        out[ident] = row
    return out


def build_plan(canonical_root: Path, source_root: Path, *, source_sha: str, base_sha: str) -> dict[str, Any]:
    reviews = load_json(canonical_root / REVIEWS)
    change_policy = load_json(canonical_root / CHANGE_POLICY)
    policy = load_json(canonical_root / IMPLEMENTATION_POLICY)
    auth_registry = load_json(canonical_root / IMPLEMENTATION_AUTHS)
    validate_policy(policy)
    if change_policy.get("program_id") != "FAR-LIVING-PROJECT-CHANGE-001":
        raise ImplementationContractError("project-change policy identity drift")
    fields = change_policy.get("implementation_review_fields")
    if not isinstance(fields, list) or set(fields) != {"implementation_required", "implementation_proposal_id"}:
        raise ImplementationContractError("implementation review-field contract drift")
    if (
        auth_registry.get("schema_version") != "1.0"
        or auth_registry.get("program_id") != "FAR-LIVING-IMPLEMENTATION-AUTHORIZATIONS-001"
        or auth_registry.get("authority") != "Research"
    ):
        raise ImplementationContractError("implementation authorization registry drift")
    auths = _unique(auth_registry.get("authorizations"), "proposal_id", "implementation authorizations")
    rows = reviews.get("reviewed_candidates")
    if not isinstance(rows, list):
        raise ImplementationContractError("reviewed_candidates must be an array")

    proposals: list[dict[str, Any]] = []
    all_targets: set[str] = set()
    for review in rows:
        if not isinstance(review, dict) or review.get("disposition") != CHANGE_DISPOSITION:
            continue
        cid = review.get("candidate_id")
        if not isinstance(cid, str) or CANDIDATE_RE.fullmatch(cid) is None:
            raise ImplementationContractError("project-change review has invalid candidate_id")
        if "implementation_required" not in review or "implementation_proposal_id" not in review:
            raise ImplementationContractError(f"{cid}: project-change review must declare implementation fields")
        required = review["implementation_required"]
        pid = review["implementation_proposal_id"]
        if not isinstance(required, bool):
            raise ImplementationContractError(f"{cid}: implementation_required must be boolean")
        if not required:
            if pid is not None:
                raise ImplementationContractError(f"{cid}: implementation_proposal_id must be null when implementation is not required")
            continue
        if not isinstance(pid, str) or PROPOSAL_RE.fullmatch(pid) is None:
            raise ImplementationContractError(f"{cid}: invalid implementation_proposal_id")
        auth = auths.get(pid)
        if auth is None:
            raise ImplementationContractError(f"{cid}: missing protected implementation authorization for {pid}")
        if set(auth) != AUTH_FIELDS:
            raise ImplementationContractError(f"{pid}: authorization fields malformed")
        if auth.get("candidate_id") != cid or auth.get("authorization_status") != policy["authorization_status"]:
            raise ImplementationContractError(f"{pid}: authorization identity/status mismatch")
        for key in ("proposal_sha256", "candidate_sha256", "operations_sha256", "review_record_sha256"):
            value = auth.get(key)
            if not isinstance(value, str) or HEX64_RE.fullmatch(value) is None:
                raise ImplementationContractError(f"{pid}: malformed {key}")
        if auth["review_record_sha256"] != canonical_json_sha(review):
            raise ImplementationContractError(f"{pid}: authorization does not bind exact review row")

        candidate_path = f"{CANDIDATE_PREFIX}/{cid}.json"
        candidate = read_regular(source_root, candidate_path)
        if candidate is None:
            raise ImplementationContractError(f"{cid}: candidate missing from source")
        candidate_sha = sha256(candidate)
        if candidate_sha != auth["candidate_sha256"]:
            raise ImplementationContractError(f"{pid}: candidate hash mismatch")
        proposal_path = f"{PROPOSAL_PREFIX}/{pid}.json"
        raw = read_regular(source_root, proposal_path)
        if raw is None:
            raise ImplementationContractError(f"{pid}: implementation proposal missing from source")
        if sha256(raw) != auth["proposal_sha256"]:
            raise ImplementationContractError(f"{pid}: proposal hash mismatch")
        try:
            proposal = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise ImplementationContractError(f"{pid}: invalid proposal JSON: {exc}") from exc
        if not isinstance(proposal, dict):
            raise ImplementationContractError(f"{pid}: proposal must be an object")
        if proposal.get("proposal_id") != pid or proposal.get("candidate_id") != cid:
            raise ImplementationContractError(f"{pid}: proposal identity mismatch")
        if proposal.get("candidate_sha256") != candidate_sha:
            raise ImplementationContractError(f"{pid}: proposal candidate hash mismatch")
        if proposal.get("lifecycle_stage") != policy["proposal_stage"]:
            raise ImplementationContractError(f"{pid}: proposal stage mismatch")
        operations = proposal.get("operations")
        if not isinstance(operations, list) or not operations:
            raise ImplementationContractError(f"{pid}: implementation proposal requires nonempty operations")
        if canonical_json_sha(operations) != auth["operations_sha256"]:
            raise ImplementationContractError(f"{pid}: operation-set hash mismatch")

        normalized: list[dict[str, str]] = []
        seen: set[str] = set()
        for operation in operations:
            if not isinstance(operation, dict) or operation.get("op") != "write_file":
                raise ImplementationContractError(f"{pid}: only write_file operations are allowed")
            target = validate_target(operation.get("path"), policy)
            if target in seen or target in all_targets:
                raise ImplementationContractError(f"{pid}: duplicate or colliding target {target}")
            seen.add(target)
            all_targets.add(target)
            source_path = safe_path(operation.get("source_path"))
            prefix = f"{PAYLOAD_PREFIX}/{pid}/"
            if not source_path.startswith(prefix):
                raise ImplementationContractError(f"{pid}: payload outside proposal directory")
            payload = read_regular(source_root, source_path)
            if payload is None:
                raise ImplementationContractError(f"{pid}: payload missing: {source_path}")
            result_sha = operation.get("result_sha256")
            if not isinstance(result_sha, str) or result_sha != sha256(payload):
                raise ImplementationContractError(f"{pid}: payload hash mismatch for {target}")
            preimage = expected_preimage(canonical_root, target)
            if operation.get("expected_main_sha256") != preimage:
                raise ImplementationContractError(f"{pid}: stale main preimage for {target}")
            if read_regular(canonical_root, target) == payload:
                continue
            normalized.append({
                "op": "write_file",
                "path": target,
                "source_path": source_path,
                "expected_main_sha256": preimage,
                "result_sha256": result_sha,
            })
        if normalized:
            proposals.append({
                "proposal_id": pid,
                "candidate_id": cid,
                "proposal_sha256": auth["proposal_sha256"],
                "candidate_sha256": candidate_sha,
                "operations_sha256": auth["operations_sha256"],
                "operations": normalized,
            })
    manifest_prefix = safe_path(policy["manifest_prefix"])
    manifest_path = f"{manifest_prefix}{source_sha}-{base_sha}.json"
    return {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-IMPLEMENTATION-001",
        "source_pr": 490,
        "source_branch": policy["source_branch"],
        "source_head_sha": source_sha,
        "base_main_sha": base_sha,
        "manifest_path": manifest_path,
        "proposals": proposals,
        "actionable": bool(proposals),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-root", default=".")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        plan = build_plan(
            Path(args.canonical_root).resolve(),
            Path(args.source_root).resolve(),
            source_sha=args.source_sha,
            base_sha=args.base_sha,
        )
    except ImplementationContractError as exc:
        print(f"living implementation contract failed: {exc}", file=sys.stderr)
        return 2
    encoded = json.dumps(plan, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
