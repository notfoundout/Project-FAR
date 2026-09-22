#!/usr/bin/env python3
"""Independently verify an autonomous living-review package before any branch write.

The verifier deliberately does not call a model. It rechecks the deterministic facts
that can make a proposed disposition safe to expose for human merge: exact candidate
binding, role/provenance structure, source-retrieval evidence, disposition-specific
agreement, protected authorization hashes, allowed targets, preimages, payload hashes,
and non-no-op repository changes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tools import living_implementation_contract as implementation
from tools import promote_living_research as promoter
from tools import run_living_autonomous_review as review


class PackageError(RuntimeError):
    pass


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PackageError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise PackageError(f"{path}: expected JSON object")
    return value


def one(rows: Any, key: str, value: str, label: str) -> dict[str, Any]:
    if not isinstance(rows, list):
        raise PackageError(f"{label}: expected array")
    found = [row for row in rows if isinstance(row, dict) and row.get(key) == value]
    if len(found) != 1:
        raise PackageError(f"{label}: expected exactly one {key}={value}, found {len(found)}")
    return found[0]


def exact_tree(root: Path) -> set[str]:
    if not root.exists():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def context_success(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    rows = value.get("urlMetadata")
    if not isinstance(rows, list):
        rows = value.get("url_metadata")
    if not isinstance(rows, list):
        return False
    return any(
        isinstance(row, dict)
        and "SUCCESS" in str(row.get("urlRetrievalStatus", row.get("url_retrieval_status", ""))).upper()
        for row in rows
    )


def claim_set(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        raise PackageError(f"{label}: malformed claim ids")
    return set(value)


def check_operation(
    repo_root: Path,
    inbox_root: Path,
    operation: dict[str, Any],
    *,
    implementation_surface: bool,
) -> str:
    if not isinstance(operation, dict) or operation.get("op") != "write_file":
        raise PackageError("proposal contains non-write_file operation")
    target = promoter.safe(operation.get("path"))
    source_path = promoter.safe(operation.get("source_path"))
    payload = inbox_root / source_path
    if not payload.is_file() or payload.is_symlink():
        raise PackageError(f"missing or unsafe payload: {source_path}")
    raw = payload.read_bytes()
    if operation.get("result_sha256") != promoter.h(raw):
        raise PackageError(f"payload hash mismatch: {target}")
    if implementation_surface:
        policy = implementation.load_json(repo_root / implementation.IMPLEMENTATION_POLICY)
        implementation.validate_policy(policy)
        implementation.validate_target(target, policy)
        before = implementation.read_regular(repo_root, target)
    else:
        policy = promoter.load(repo_root / promoter.POLICY)
        promoter.validate_policy(policy)
        promoter.validate_target(target, policy)
        forbidden = policy.get("canonical_forbidden_prefixes", [])
        if any(target.startswith(prefix) for prefix in forbidden):
            raise PackageError(f"scientific target uses forbidden prefix: {target}")
        before = promoter.mainbytes(repo_root, target)
    expected = "ABSENT" if before is None else promoter.h(before)
    if operation.get("expected_main_sha256") != expected:
        raise PackageError(f"stale main preimage: {target}")
    if before == raw:
        raise PackageError(f"no-op replacement is not an admissible project change: {target}")
    return target


def find_artifact_root(review_root: Path, cid: str) -> Path:
    base = review_root / review.REVIEW_ROOT
    if not base.is_dir():
        raise PackageError("review package has no autonomous-review artifact directory")
    candidates = [path for path in base.iterdir() if path.is_dir() and path.name.startswith(cid + "-")]
    if len(candidates) != 1:
        raise PackageError(f"expected exactly one autonomous-review artifact directory for {cid}")
    artifact = candidates[0]
    expected = {f"{name}.json" for name in promoter.PROV_KEYS}
    observed = {path.name for path in artifact.iterdir() if path.is_file()}
    if observed != expected:
        raise PackageError(f"review provenance file set mismatch: {sorted(observed)}")
    return artifact


def validate_review_ready(repo_root: Path, package_root: Path, manifest: dict[str, Any]) -> None:
    cid = manifest.get("candidate_id")
    disposition = manifest.get("disposition")
    candidate_sha = manifest.get("candidate_sha256")
    if not isinstance(cid, str) or review.CID_RE.fullmatch(cid) is None:
        raise PackageError("manifest candidate_id malformed")
    if disposition not in review.ALLOWED:
        raise PackageError("manifest disposition malformed")
    if not isinstance(candidate_sha, str) or promoter.HEX64_RE.fullmatch(candidate_sha) is None:
        raise PackageError("manifest candidate_sha256 malformed")

    review_root = package_root / "review"
    inbox_root = package_root / "inbox"
    candidate_path = review_root / review.CANDIDATES / f"{cid}.json"
    if not candidate_path.is_file() or promoter.h(candidate_path.read_bytes()) != candidate_sha:
        raise PackageError("review candidate does not match manifest hash")
    candidate = load(candidate_path)
    if candidate.get("candidate_id") != cid or candidate.get("authority") != "Research":
        raise PackageError("review candidate identity/authority drift")

    artifact = find_artifact_root(review_root, cid)
    question = load(artifact / "question.json")
    execution = load(artifact / "execution.json")
    observation = load(artifact / "observation.json")
    discovery = load(artifact / "discovery.json")
    replication = load(artifact / "replication.json")
    acceptance = load(artifact / "acceptance.json")
    screening = observation.get("screening")
    attack = observation.get("attack")
    if not isinstance(screening, dict) or not isinstance(attack, dict):
        raise PackageError("observation record lacks screening/attack roles")
    if execution.get("roles") != ["screening", "attack", "replication", "adjudication"]:
        raise PackageError("execution record role separation drift")
    if acceptance.get("disposition") != disposition:
        raise PackageError("acceptance disposition differs from manifest")
    if question.get("candidate_id") != cid or discovery.get("candidate_id") != cid:
        raise PackageError("provenance candidate binding drift")

    canonical_claims = question.get("canonical_claims")
    if not isinstance(canonical_claims, list):
        raise PackageError("question canonical_claims malformed")
    allowed_claims = {
        row.get("id") for row in canonical_claims
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if not allowed_claims:
        raise PackageError("review has no exact canonical claim binding")
    screening_claims = claim_set(screening.get("affected_claim_ids"), "screening")
    attack_claims = claim_set(attack.get("affected_claim_ids"), "attack")
    replication_claims = claim_set(replication.get("affected_claim_ids"), "replication")
    for label, values in (
        ("screening", screening_claims), ("attack", attack_claims), ("replication", replication_claims)
    ):
        unknown = values - allowed_claims
        if unknown:
            raise PackageError(f"{label}: claims outside frozen canonical binding: {sorted(unknown)}")

    source_meta = discovery.get("url_context_metadata")
    if not isinstance(source_meta, dict):
        raise PackageError("discovery URL-context metadata missing")
    screening_source_ok = context_success(source_meta.get("screening"))
    attack_source_ok = context_success(source_meta.get("attack"))
    replication_source_ok = context_success(source_meta.get("replication"))
    if screening.get("primary_source_verified") is not True or not screening_source_ok:
        raise PackageError("review_ready package lacks independently recorded primary-source retrieval")

    policy = load(repo_root / review.POLICY)
    review.validate_policy(policy)
    gate = policy["project_change_gate"]
    prior_gate = policy["prior_art_gate"]
    project = acceptance.get("project_change_required")
    if not isinstance(project, bool) or (disposition == "PROJECT_CHANGE_REQUIRED") != project:
        raise PackageError("project-change disposition/boolean mismatch")

    if disposition == "IRRELEVANT_FALSE_POSITIVE" and screening.get("relevant") is not False:
        raise PackageError("IRRELEVANT_FALSE_POSITIVE requires screening.relevant=false")

    if disposition == "N1_PRIOR_ART_LEAD":
        if prior_gate.get("require_relevant") and screening.get("relevant") is not True:
            raise PackageError("N1 prior-art lead lacks direct relevance")
        if prior_gate.get("require_premise_match") and screening.get("premise_match") is not True:
            raise PackageError("N1 prior-art lead lacks premise match")
        if prior_gate.get("require_scope_match") and screening.get("scope_match") is not True:
            raise PackageError("N1 prior-art lead lacks scope match")
        if prior_gate.get("require_attack_prior_art") and attack.get("prior_art_found") is not True:
            raise PackageError("N1 prior-art lead not established by attack role")
        if prior_gate.get("require_replication_prior_art") and replication.get("prior_art_found") is not True:
            raise PackageError("N1 prior-art lead not reproduced by replication role")
        if not attack_source_ok or not replication_source_ok:
            raise PackageError("N1 prior-art lead requires primary-source retrieval in attack and replication")
        if prior_gate.get("require_matching_claim_id") and not (attack_claims & replication_claims):
            raise PackageError("N1 prior-art roles disagree on affected claim")

    if disposition == "PROJECT_CHANGE_REQUIRED":
        if gate.get("require_relevant") and screening.get("relevant") is not True:
            raise PackageError("project change lacks direct relevance")
        if gate.get("require_exact_claim_binding") and not (screening_claims & attack_claims & replication_claims):
            raise PackageError("project change lacks exact cross-role claim binding")
        if gate.get("require_premise_match") and screening.get("premise_match") is not True:
            raise PackageError("project change lacks premise match")
        if gate.get("require_scope_match") and screening.get("scope_match") is not True:
            raise PackageError("project change lacks scope match")
        if gate.get("require_attack_contradiction") and attack.get("contradiction_found") is not True:
            raise PackageError("project change attack role did not find a contradiction")
        if gate.get("require_reproducible_attack") and not str(attack.get("reproducible_attack", "")).strip():
            raise PackageError("project change lacks reproducible attack")
        if gate.get("require_replication") and replication.get("attack_reproduced") is not True:
            raise PackageError("project change attack was not reproduced")
        if gate.get("require_replication_contradiction") and replication.get("contradiction_found") is not True:
            raise PackageError("replication role did not independently find contradiction")
        if not attack_source_ok or not replication_source_ok:
            raise PackageError("project change requires primary-source retrieval in attack and replication")
        if gate.get("require_matching_claim_id") and not (attack_claims & replication_claims):
            raise PackageError("project-change roles disagree on affected claim")

    review_registry = load(review_root / review.REVIEWS)
    review_row = one(review_registry.get("reviewed_candidates"), "candidate_id", cid, "review registry")
    if review_row.get("disposition") != disposition or review_row.get("source_key") != candidate.get("source_key"):
        raise PackageError("review row differs from frozen candidate/disposition")
    audit_path = review_row.get("review_basis")
    if not isinstance(audit_path, str):
        raise PackageError("review row lacks review_basis")
    audit_file = review_root / promoter.safe(audit_path)
    if not audit_file.is_file():
        raise PackageError("review basis is absent from package")

    snapshots = load(review_root / review.SNAPSHOT_AUTHS)
    snapshot = one(snapshots.get("authorizations"), "candidate_id", cid, "snapshot authorizations")
    if snapshot.get("candidate_sha256") != candidate_sha:
        raise PackageError("snapshot authorization candidate hash mismatch")
    if snapshot.get("source_key") != candidate.get("source_key") or snapshot.get("disposition") != disposition:
        raise PackageError("snapshot authorization identity/disposition mismatch")
    if snapshot.get("review_basis") != audit_path or snapshot.get("review_basis_sha256") != promoter.h(audit_file.read_bytes()):
        raise PackageError("snapshot authorization review-basis mismatch")
    if snapshot.get("review_record_sha256") != promoter.canonical_json_sha(review_row):
        raise PackageError("snapshot authorization review-row hash mismatch")
    if snapshot.get("authorization_status") != "ACCEPTED_FOR_MECHANICAL_SNAPSHOT":
        raise PackageError("snapshot authorization status mismatch")

    proposal_paths = list((inbox_root / review.PROMOTION_PROPOSALS).glob("*.json")) if (inbox_root / review.PROMOTION_PROPOSALS).is_dir() else []
    impl_paths = list((inbox_root / review.IMPLEMENTATION_PROPOSALS).glob("*.json")) if (inbox_root / review.IMPLEMENTATION_PROPOSALS).is_dir() else []
    if disposition != "PROJECT_CHANGE_REQUIRED":
        if proposal_paths or impl_paths or (review_root / review.PROMOTION_AUTHS).exists() or (review_root / review.IMPLEMENTATION_AUTHS).exists():
            raise PackageError("non-project-change review contains canonical change authority")
        return

    proposal_id = review_row.get("proposal_id")
    if not isinstance(proposal_id, str) or promoter.PROPOSAL_RE.fullmatch(proposal_id) is None:
        raise PackageError("project-change review lacks valid proposal_id")
    proposal_path = inbox_root / review.PROMOTION_PROPOSALS / f"{proposal_id}.json"
    proposal = load(proposal_path)
    proposal_raw = proposal_path.read_bytes()
    if proposal.get("candidate_id") != cid or proposal.get("candidate_sha256") != candidate_sha:
        raise PackageError("scientific proposal candidate binding mismatch")
    if proposal.get("lifecycle_stage") != "PROMOTION_PROPOSED":
        raise PackageError("scientific proposal stage mismatch")
    provenance = proposal.get("provenance")
    if not isinstance(provenance, dict) or set(provenance) != set(promoter.PROV_KEYS):
        raise PackageError("scientific proposal provenance incomplete")
    for key in promoter.PROV_KEYS:
        item = provenance[key]
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise PackageError(f"scientific proposal {key} provenance malformed")
        raw = (review_root / promoter.safe(item["path"])).read_bytes()
        if promoter.h(raw) != item["sha256"]:
            raise PackageError(f"scientific proposal {key} provenance hash mismatch")
    operations = proposal.get("operations")
    if not isinstance(operations, list) or (gate.get("require_nonempty_scientific_operations") and not operations):
        raise PackageError("project change has no scientific operations")
    scientific_targets = [check_operation(repo_root, inbox_root, op, implementation_surface=False) for op in operations]
    expected_targets = acceptance.get("scientific_targets")
    if not isinstance(expected_targets, list) or set(scientific_targets) != set(expected_targets):
        raise PackageError("scientific operation targets differ from adjudication")
    auth_registry = load(review_root / review.PROMOTION_AUTHS)
    auth = one(auth_registry.get("authorizations"), "proposal_id", proposal_id, "promotion authorizations")
    if auth.get("candidate_id") != cid or auth.get("candidate_sha256") != candidate_sha:
        raise PackageError("promotion authorization candidate binding mismatch")
    if auth.get("proposal_sha256") != promoter.h(proposal_raw):
        raise PackageError("promotion authorization proposal hash mismatch")
    if auth.get("operations_sha256") != promoter.canonical_json_sha(operations):
        raise PackageError("promotion authorization operation hash mismatch")
    if auth.get("provenance_sha256") != {key: provenance[key]["sha256"] for key in promoter.PROV_KEYS}:
        raise PackageError("promotion authorization provenance hash mismatch")
    if auth.get("authorization_status") != promoter.AUTH_STATUS:
        raise PackageError("promotion authorization status mismatch")

    impl_required = acceptance.get("implementation_required")
    impl_targets = acceptance.get("implementation_targets")
    if not isinstance(impl_required, bool) or not isinstance(impl_targets, list):
        raise PackageError("implementation adjudication fields malformed")
    if impl_required != bool(impl_targets):
        raise PackageError("implementation requirement/target mismatch")
    if review_row.get("implementation_required") != impl_required:
        raise PackageError("review row implementation requirement mismatch")
    if not impl_required:
        if review_row.get("implementation_proposal_id") is not None or impl_paths or (review_root / review.IMPLEMENTATION_AUTHS).exists():
            raise PackageError("implementation authority exists when implementation is not required")
        return

    impl_id = review_row.get("implementation_proposal_id")
    if not isinstance(impl_id, str) or implementation.PROPOSAL_RE.fullmatch(impl_id) is None:
        raise PackageError("project-change review lacks valid implementation_proposal_id")
    impl_path = inbox_root / review.IMPLEMENTATION_PROPOSALS / f"{impl_id}.json"
    impl = load(impl_path)
    impl_raw = impl_path.read_bytes()
    if impl.get("candidate_id") != cid or impl.get("candidate_sha256") != candidate_sha:
        raise PackageError("implementation proposal candidate binding mismatch")
    if impl.get("lifecycle_stage") != "IMPLEMENTATION_PROPOSED":
        raise PackageError("implementation proposal stage mismatch")
    impl_ops = impl.get("operations")
    if not isinstance(impl_ops, list) or not impl_ops:
        raise PackageError("required implementation proposal has no operations")
    actual_impl_targets = [check_operation(repo_root, inbox_root, op, implementation_surface=True) for op in impl_ops]
    if set(actual_impl_targets) != set(impl_targets):
        raise PackageError("implementation operation targets differ from adjudication")
    impl_auths = load(review_root / review.IMPLEMENTATION_AUTHS)
    impl_auth = one(impl_auths.get("authorizations"), "proposal_id", impl_id, "implementation authorizations")
    if impl_auth.get("candidate_id") != cid or impl_auth.get("candidate_sha256") != candidate_sha:
        raise PackageError("implementation authorization candidate binding mismatch")
    if impl_auth.get("proposal_sha256") != promoter.h(impl_raw):
        raise PackageError("implementation authorization proposal hash mismatch")
    if impl_auth.get("operations_sha256") != implementation.canonical_json_sha(impl_ops):
        raise PackageError("implementation authorization operation hash mismatch")
    if impl_auth.get("review_record_sha256") != implementation.canonical_json_sha(review_row):
        raise PackageError("implementation authorization review-row hash mismatch")
    if impl_auth.get("authorization_status") != "ACCEPTED_FOR_PROTECTED_IMPLEMENTATION_PR":
        raise PackageError("implementation authorization status mismatch")


def validate(repo_root: Path, package_root: Path) -> list[str]:
    try:
        repo_root = repo_root.resolve()
        package_root = package_root.resolve()
        top = {path.name for path in package_root.iterdir()} if package_root.is_dir() else set()
        if not top <= {"manifest.json", "review", "inbox"}:
            raise PackageError(f"unexpected package top-level paths: {sorted(top - {'manifest.json', 'review', 'inbox'})}")
        manifest = load(package_root / "manifest.json")
        status = manifest.get("status")
        if status == "no_candidate":
            if exact_tree(package_root / "review") or exact_tree(package_root / "inbox"):
                raise PackageError("no_candidate package must contain no review/inbox files")
            return []
        if status == "source_blocked":
            if exact_tree(package_root / "review"):
                raise PackageError("source_blocked package may not contain review authority")
            files = exact_tree(package_root / "inbox")
            cid = manifest.get("candidate_id")
            expected = {(review.ATTEMPTS / f"{cid}.json").as_posix()}
            if files != expected:
                raise PackageError("source_blocked package must contain exactly one retry record")
            attempt = load(package_root / "inbox" / next(iter(expected)))
            if attempt.get("status") != "SOURCE_BLOCKED" or attempt.get("candidate_id") != cid:
                raise PackageError("source-blocked retry record identity/status mismatch")
            return []
        if status != "review_ready":
            raise PackageError(f"unknown package status: {status!r}")
        validate_review_ready(repo_root, package_root, manifest)
        return []
    except (PackageError, promoter.PromotionError, implementation.ImplementationContractError, KeyError, OSError, ValueError) as exc:
        return [str(exc)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args()
    errors = validate(Path.cwd(), Path(args.package_root))
    if errors:
        for error in errors:
            print(f"living autonomous review package invalid: {error}", file=sys.stderr)
        return 2
    print("living autonomous review package valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
