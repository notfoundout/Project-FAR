"""Defense-in-depth semantic verifier for PR #435 review-closure contracts."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_integrity as integrity
import verify_amendment_v1_1_rooted as amendment_v1_1
import verify_review_closure_v1_2 as closure_v1_2

DesignError = integrity.DesignError
HERE = Path(__file__).resolve().parent
SEED = HERE / "bootstrap-seed-commitment-contract-v1.0.json"
TASK = HERE / "task-manifest-contract-v1.0.json"
GATE = HERE / "execution-gate-v1.0.json"


def verify_task_identity_contract(path: Path = TASK) -> None:
    data = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(data, dict):
        raise DesignError("task manifest contract must be object")
    if (
        data.get("schema_version"),
        data.get("program_id"),
        data.get("manifest_status"),
        data.get("execution_authorized"),
    ) != ("1.3", "FAR-SWE-V3-001", "uninstantiated", False):
        raise DesignError("base task manifest identity/boundary drifted")
    freeze = data.get("freeze_timing", "")
    if (
        "before any sacrificial pilot or confirmatory execution" not in freeze
        or "freezing after any agent run is prohibited" not in freeze
    ):
        raise DesignError("base task manifest freeze timing drifted")
    record = data.get("record_schema", {})
    if record.get("required_keys_exactly") != [
        "blind_task_id",
        "repository_blind_id",
        "task_bundle_root_sha256",
    ]:
        raise DesignError("base task record shape drifted")
    blind = record.get("blind_task_id", {})
    repo_blind = record.get("repository_blind_id", {})
    task_root = record.get("task_bundle_root_sha256", {})
    if blind.get("unique") is not True or blind.get("unicode_permitted") is not False:
        raise DesignError("blind task identity drifted")
    if (
        repo_blind.get("unicode_permitted") is not False
        or "one-to-one" not in repo_blind.get("canonical_mapping", "")
    ):
        raise DesignError("repository blind identity drifted")
    if task_root.get("unique") is not True or task_root.get("pattern") != "^[0-9a-f]{64}$":
        raise DesignError("task root uniqueness drifted")
    root = data.get("task_bundle_root_contract", {})
    values = root.get("descriptor_values", {})
    if (
        root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2"
        or root.get("hash") != "SHA-256"
    ):
        raise DesignError("base task root algorithm drifted")
    if "exact JSON string github.com" not in values.get("repository_provider", ""):
        raise DesignError("GitHub-only provider contract drifted")
    provider_id = values.get("repository_provider_id", "")
    if "positive JSON integer" not in provider_id or "GitHub REST repository id" not in provider_id:
        raise DesignError("repository provider ID type drifted")
    if "lowercase 40-character Git commit SHA" not in values.get("repository_commit_sha", ""):
        raise DesignError("repository commit identity drifted")
    identity = data.get("repository_identity_contract", {})
    if identity.get("supported_provider") != "github.com only":
        raise DesignError("repository provider scope drifted")
    if (
        identity.get("equal_authoritative_identities_same_blind_id") is not True
        or identity.get("distinct_authoritative_identities_distinct_blind_ids") is not True
    ):
        raise DesignError("repository identity-to-blind-ID mapping drifted")
    for key in ("minimum_repository_count_basis", "per_repository_cap_basis"):
        if "(repository_provider, repository_provider_id)" not in identity.get(key, ""):
            raise DesignError("repository count/cap identity basis drifted")
    order = data.get("order_contract", {})
    if (
        order.get("authoritative_sequence") != "top-level JSON array order"
        or order.get("runtime_sorting_permitted") is not False
    ):
        raise DesignError("task manifest order drifted")


def verify_seed_contract(path: Path = SEED) -> None:
    data = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(data, dict):
        raise DesignError("bootstrap seed commitment must be object")
    if (
        data.get("schema_version"),
        data.get("program_id"),
        data.get("artifact_status"),
        data.get("commitment_status"),
    ) != ("1.0", "FAR-SWE-V3-001", "Research", "frozen_pre_execution"):
        raise DesignError("bootstrap seed commitment identity drifted")
    authority = data.get("authority")
    if not isinstance(authority, dict) or authority.get("outcome_exposure_status") != "none":
        raise DesignError("bootstrap seed outcome boundary drifted")
    for key in (
        "model_calls_authorized",
        "pilot_execution_authorized",
        "benchmark_execution_authorized",
        "confirmatory_execution_authorized",
    ):
        if authority.get(key) is not False:
            raise DesignError("bootstrap seed authorization boundary drifted")
    rng = data.get("rng_contract", {})
    seed = rng.get("seed_hex")
    if (
        rng.get("procedure_id") != "sha256_rejection_stream_v1"
        or rng.get("seed_encoding")
        != "64 lowercase hexadecimal characters decoded as exactly 32 bytes"
    ):
        raise DesignError("bootstrap RNG contract drifted")
    if (
        type(seed) is not str
        or re.fullmatch(r"[0-9a-f]{64}", seed) is None
        or len(bytes.fromhex(seed)) != 32
    ):
        raise DesignError("bootstrap seed encoding drifted")

    expected_inputs = closure_v1_2.SEED_INPUTS
    derivation = data.get("derivation")
    if not isinstance(derivation, dict) or derivation.get("inputs") != expected_inputs:
        raise DesignError("bootstrap seed prospective input identities drifted")
    capsule_blob = expected_inputs[0]["git_blob_sha1"]
    gate_blob = expected_inputs[1]["git_blob_sha1"]
    payload = (
        "FAR-SWE-V3-001/bootstrap-seed/v1\n"
        f"treatment_capsule_git_blob_sha1={capsule_blob}\n"
        f"execution_gate_git_blob_sha1={gate_blob}\n"
    )
    if (
        derivation.get("method") != "SHA-256 over the exact UTF-8 bytes of canonical_payload"
        or derivation.get("canonical_payload") != payload
    ):
        raise DesignError("bootstrap seed derivation contract drifted")
    if (
        hashlib.sha256(payload.encode("utf-8")).hexdigest() != seed
        or derivation.get("sha256") != seed
    ):
        raise DesignError("bootstrap seed recomputation failed")
    if (
        derivation.get("outcome_or_grade_inputs_permitted") is not False
        or derivation.get("task_identity_inputs_permitted") is not False
    ):
        raise DesignError("post-outcome or task-identity seed inputs were enabled")
    timing = data.get("timing")
    if not isinstance(timing, dict) or set(timing) != {
        "must_be_committed_and_integrity_rooted_before_any_sacrificial_pilot_execution",
        "must_be_committed_and_integrity_rooted_before_any_confirmatory_execution",
        "must_precede_any_pilot_or_confirmatory_outcome_reveal",
        "immutable_after_commitment",
    } or any(value is not True for value in timing.values()):
        raise DesignError("bootstrap seed timing contract drifted")


def verify_gate_closed(path: Path = GATE) -> None:
    data = integrity._load_json(path)
    for key in (
        "execution_authorized",
        "model_calls_authorized",
        "benchmark_execution_authorized",
        "pilot_execution_authorized",
        "confirmatory_execution_authorized",
    ):
        if data.get(key) is not False:
            raise DesignError(f"execution gate opened: {key}")


def verify(here: Path | None = None) -> None:
    """Validate review-closure semantics against one explicit active artifact root."""
    active = here or integrity.HERE
    try:
        amendment_v1_1.validate(
            amend=active / "failure-arithmetic-amendment-v1.1.json",
            readme=active / "AMENDMENT-v1.1.md",
            gate=active / "execution-gate-v1.0.json",
            historical_root=active / "historical-base-83c951",
        )
    except amendment_v1_1.AmendmentError as exc:
        raise DesignError(f"failure/arithmetic amendment validation failed: {exc}") from exc
    verify_task_identity_contract(active / "task-manifest-contract-v1.0.json")
    verify_seed_contract(active / "bootstrap-seed-commitment-contract-v1.0.json")
    closure_v1_2.validate(active / "review-closure-amendment-v1.2.json")
    verify_gate_closed(active / "execution-gate-v1.0.json")


if __name__ == "__main__":
    try:
        verify()
    except (DesignError, amendment_v1_1.AmendmentError) as exc:
        raise SystemExit(f"FAIL: {exc}")
    print(
        "PASS: PR #435 review-closure semantics are prospective, shallow-checkout reproducible, "
        "v1.1 failure/arithmetic semantics are enforced, stratum-auditable, harm-threshold frozen, "
        "and execution remains blocked."
    )
