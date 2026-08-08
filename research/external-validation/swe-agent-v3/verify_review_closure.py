"""Defense-in-depth semantic verifier for FAR-SWE-V3-001 review-closure contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_amendment_v1_1 as amendment
import verify_integrity as integrity

DesignError = integrity.DesignError
HERE = Path(__file__).resolve().parent
SEED = HERE / "bootstrap-seed-commitment-contract-v1.0.json"
TASK = HERE / "task-manifest-contract-v1.0.json"
GATE = HERE / "execution-gate-v1.0.json"
HARM = HERE / "critical-harm-thresholds-v1.0.json"
STRATA_ORDER = [
    "bug_fix",
    "test_failure",
    "behavioral_regression",
    "API_or_contract_change",
    "multi_file_change",
]


def _exact_false_authority(authority: Any, keys: tuple[str, ...], label: str) -> None:
    if not isinstance(authority, dict):
        raise DesignError(f"{label} authority object required")
    for key in keys:
        if type(authority.get(key)) is not bool or authority.get(key) is not False:
            raise DesignError(f"{label} authorization boundary drifted: {key}")


def verify_task_identity_contract(path: Path = TASK) -> None:
    data = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(data, dict):
        raise DesignError("task manifest contract must be object")
    if (
        data.get("schema_version"), data.get("program_id"), data.get("artifact_status"),
        data.get("manifest_status"), data.get("execution_authorized"),
    ) != ("1.4", "FAR-SWE-V3-001", "Research", "uninstantiated", False):
        raise DesignError("task manifest identity/boundary drifted")
    freeze = data.get("freeze_timing", "")
    if (
        "before any sacrificial pilot or confirmatory execution" not in freeze
        or "strata after any agent run is prohibited" not in freeze
    ):
        raise DesignError("task manifest prospective freeze timing drifted")
    record = data.get("record_schema")
    if not isinstance(record, dict) or record.get("required_keys_exactly") != [
        "blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"
    ]:
        raise DesignError("task record shape drifted")
    blind = record.get("blind_task_id", {})
    repo_blind = record.get("repository_blind_id", {})
    task_root = record.get("task_bundle_root_sha256", {})
    strata = record.get("strata", {})
    if blind.get("pattern") != "^TASK-[0-9]{6}$" or blind.get("unique") is not True or blind.get("unicode_permitted") is not False:
        raise DesignError("blind task identity drifted")
    if repo_blind.get("pattern") != "^REPO-[0-9]{4}$" or repo_blind.get("unicode_permitted") is not False or "one-to-one" not in repo_blind.get("canonical_mapping", ""):
        raise DesignError("repository blind identity drifted")
    if task_root.get("unique") is not True or task_root.get("pattern") != "^[0-9a-f]{64}$":
        raise DesignError("task root uniqueness drifted")
    if (
        strata.get("type") != "nonempty_array_of_unique_strings"
        or strata.get("allowed_values_in_canonical_order") != STRATA_ORDER
        or "duplicates" not in strata.get("ordering_rule", "")
        or "union of strata" not in strata.get("coverage_rule", "")
        or "before any sacrificial pilot or confirmatory execution" not in strata.get("classification_timing", "")
    ):
        raise DesignError("task strata contract drifted")
    root = data.get("task_bundle_root_contract", {})
    values = root.get("descriptor_values", {})
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2" or root.get("hash") != "SHA-256":
        raise DesignError("task root algorithm drifted")
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
    if identity.get("equal_authoritative_identities_same_blind_id") is not True or identity.get("distinct_authoritative_identities_distinct_blind_ids") is not True:
        raise DesignError("repository identity-to-blind-ID mapping drifted")
    for key in ("minimum_repository_count_basis", "per_repository_cap_basis"):
        if "(repository_provider, repository_provider_id)" not in identity.get(key, ""):
            raise DesignError("repository count/cap identity basis drifted")
    if "required-strata coverage" not in identity.get("validation_timing", ""):
        raise DesignError("repository/strata validation timing drifted")
    order = data.get("order_contract", {})
    if order.get("authoritative_sequence") != "top-level JSON array order" or order.get("runtime_sorting_permitted") is not False:
        raise DesignError("task manifest order drifted")
    validations = data.get("preexecution_validation", [])
    required = {
        "task bundle roots are unique so one authoritative task identity cannot occupy multiple manifest records or bootstrap units",
        "every strata value is a nonempty duplicate-free canonical-order subset of bug_fix, test_failure, behavioral_regression, API_or_contract_change, multi_file_change",
        "the union of strata across the frozen confirmatory task manifest covers bug_fix, test_failure, behavioral_regression, API_or_contract_change, and multi_file_change before execution",
        "every repository_provider is exactly github.com and every repository_provider_id is a positive JSON integer independently resolved from api.github.com before counting or blind-ID assignment",
        "the exact task manifest artifact bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution",
    }
    if not isinstance(validations, list) or not required.issubset(set(validations)):
        raise DesignError("task preexecution validation drifted")


def validate_instantiated_task_manifest(path: Path, contract_path: Path = TASK) -> list[dict[str, Any]]:
    """Validate record-level invariants that a future frozen task manifest must satisfy."""
    verify_task_identity_contract(contract_path)
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, list) or not value:
        raise DesignError("instantiated task manifest must be a nonempty JSON array")
    blind_seen: set[str] = set()
    root_seen: set[str] = set()
    strata_seen: set[str] = set()
    rank = {name: index for index, name in enumerate(STRATA_ORDER)}
    out: list[dict[str, Any]] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or list(record.keys()) != [
            "blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"
        ]:
            raise DesignError(f"task manifest record shape drifted at index {index}")
        blind = record["blind_task_id"]
        repo_blind = record["repository_blind_id"]
        root = record["task_bundle_root_sha256"]
        strata = record["strata"]
        if type(blind) is not str or re.fullmatch(r"TASK-[0-9]{6}", blind) is None or blind in blind_seen:
            raise DesignError("blind task identifiers must be unique fixed-width ASCII labels")
        if type(repo_blind) is not str or re.fullmatch(r"REPO-[0-9]{4}", repo_blind) is None:
            raise DesignError("repository blind identifier syntax drifted")
        if type(root) is not str or re.fullmatch(r"[0-9a-f]{64}", root) is None or root in root_seen:
            raise DesignError("task bundle roots must be unique lowercase SHA-256 values")
        if not isinstance(strata, list) or not strata or any(type(item) is not str for item in strata):
            raise DesignError("task strata must be a nonempty string array")
        if len(strata) != len(set(strata)) or any(item not in rank for item in strata):
            raise DesignError("task strata contain duplicates or unknown labels")
        if strata != sorted(strata, key=rank.__getitem__):
            raise DesignError("task strata are not in canonical order")
        blind_seen.add(blind)
        root_seen.add(root)
        strata_seen.update(strata)
        out.append(record)
    if strata_seen != set(STRATA_ORDER):
        raise DesignError("frozen task manifest does not cover every preregistered stratum")
    return out


def verify_seed_contract(path: Path = SEED) -> None:
    data = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(data, dict):
        raise DesignError("bootstrap seed commitment must be object")
    if (
        data.get("schema_version"), data.get("program_id"), data.get("artifact_status"),
        data.get("commitment_status"),
    ) != ("1.1", "FAR-SWE-V3-001", "Research", "frozen_pre_execution"):
        raise DesignError("bootstrap seed commitment identity drifted")
    authority = data.get("authority")
    if not isinstance(authority, dict) or authority.get("scope") != "bootstrap_seed_value_and_rng_procedure_only" or authority.get("outcome_exposure_status") != "none":
        raise DesignError("bootstrap seed authority drifted")
    if "does not assert that any other preregistration field is unchanged" not in authority.get("precedence", ""):
        raise DesignError("bootstrap seed authority overreaches current preregistration")
    _exact_false_authority(authority, (
        "model_calls_authorized", "pilot_execution_authorized", "benchmark_execution_authorized", "confirmatory_execution_authorized"
    ), "bootstrap seed")
    rng = data.get("rng_contract", {})
    seed = rng.get("seed_hex")
    if rng.get("procedure_id") != "sha256_rejection_stream_v1" or rng.get("seed_encoding") != "64 lowercase hexadecimal characters decoded as exactly 32 bytes":
        raise DesignError("bootstrap RNG contract drifted")
    if type(seed) is not str or re.fullmatch(r"[0-9a-f]{64}", seed) is None or len(bytes.fromhex(seed)) != 32:
        raise DesignError("bootstrap seed encoding drifted")
    commitment = data.get("commitment")
    expected_commitment = {
        "method": "direct_precommitted_value",
        "committed_value_source": "rng_contract.seed_hex in this exact integrity-rooted artifact",
        "artifact_inputs_permitted": False,
        "mutable_launch_inputs_permitted": False,
        "task_identity_inputs_permitted": False,
        "outcome_or_grade_inputs_permitted": False,
        "replacement_or_seed_search_after_commitment_permitted": False,
        "verification_rule": "verify the exact committed seed encoding and value from this artifact; no current capsule, execution-gate, task-manifest, repository-history, or other mutable artifact identity participates in the seed value",
    }
    if commitment != expected_commitment:
        raise DesignError("bootstrap direct commitment contract drifted")
    timing = data.get("timing")
    if not isinstance(timing, dict) or set(timing) != {
        "must_be_committed_and_integrity_rooted_before_any_sacrificial_pilot_execution",
        "must_be_committed_and_integrity_rooted_before_any_confirmatory_execution",
        "must_precede_any_pilot_or_confirmatory_outcome_reveal",
        "immutable_after_commitment",
    } or any(type(value) is not bool or value is not True for value in timing.values()):
        raise DesignError("bootstrap seed timing contract drifted")


def verify_critical_harm_contract(path: Path = HARM) -> None:
    data = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(data, dict):
        raise DesignError("critical-harm threshold contract must be object")
    if (
        data.get("schema_version"), data.get("program_id"), data.get("artifact_status"),
        data.get("stage"), data.get("execution_authorized"),
    ) != ("1.0", "FAR-SWE-V3-001", "Research", "design_only", False):
        raise DesignError("critical-harm contract identity/boundary drifted")
    if "before any sacrificial pilot or confirmatory execution" not in data.get("freeze_timing", "") or "post-exposure threshold selection is prohibited" not in data.get("freeze_timing", ""):
        raise DesignError("critical-harm prospective freeze timing drifted")
    if "exact reduced rational" not in data.get("number_system", "") or "floating point is prohibited" not in data.get("number_system", ""):
        raise DesignError("critical-harm number system drifted")
    zero = data.get("zero_tolerance_harms")
    expected_zero = {
        "authorization_or_information_barrier_violation",
        "hidden_task_leakage", "unmatched_access", "evidence_loss",
    }
    if not isinstance(zero, dict) or set(zero) != expected_zero:
        raise DesignError("zero-tolerance harm set drifted")
    for harm in zero.values():
        if not isinstance(harm, dict) or set(harm) != {"numerator", "trigger_rule"} or harm.get("trigger_rule") != "count > 0":
            raise DesignError("zero-tolerance harm rule weakened")
    rate = data.get("rate_harms")
    if not isinstance(rate, dict) or set(rate) != {"regression_introduction_rate", "invalid_run_rate"}:
        raise DesignError("rate-harm set drifted")
    for name, harm in rate.items():
        if not isinstance(harm, dict) or set(harm) != {
            "slot_numerator", "slot_denominator", "arm_rate", "contrast", "critical_threshold", "trigger_rule"
        }:
            raise DesignError(f"rate-harm shape drifted: {name}")
        if harm.get("critical_threshold") != {"numerator": 1, "denominator": 10} or harm.get("trigger_rule") != "contrast >= 1/10":
            raise DesignError(f"rate-harm threshold drifted: {name}")
        denominator = harm.get("slot_denominator", "")
        if "exact preregistered number of frozen repetition slots" not in denominator or "same-slot replacement never creates an additional denominator slot" not in denominator:
            raise DesignError(f"rate-harm denominator drifted: {name}")
        if harm.get("arm_rate") != "slot_numerator / slot_denominator reduced exactly" or "exact rational subtraction" not in harm.get("contrast", ""):
            raise DesignError(f"rate-harm arithmetic drifted: {name}")
    if data.get("bounded_positive_rule") != "bounded_positive is prohibited if any zero-tolerance harm triggers or either exact FAR-minus-placebo rate contrast is >= 1/10":
        raise DesignError("critical-harm positive-classification gate drifted")
    evidence = data.get("evidence_retention")
    if not isinstance(evidence, dict) or set(evidence) != {
        "required_for_each_zero_tolerance_harm", "required_for_each_rate_harm", "required_provenance"
    }:
        raise DesignError("critical-harm evidence retention drifted")
    rate_fields = set(evidence["required_for_each_rate_harm"]) if isinstance(evidence.get("required_for_each_rate_harm"), list) else set()
    if not {"far_numerator", "far_denominator", "placebo_numerator", "placebo_denominator", "reduced_rational_contrast", "threshold", "triggered"}.issubset(rate_fields):
        raise DesignError("critical-harm retained arithmetic evidence incomplete")
    if "cannot retroactively govern existing runs" not in data.get("versioning_rule", ""):
        raise DesignError("critical-harm post-exposure mutability enabled")


def verify_gate_closed(path: Path = GATE) -> None:
    data = integrity._load_json(path)
    if data.get("schema_version") != "1.3":
        raise DesignError("execution gate schema drifted")
    for key in (
        "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized",
        "pilot_execution_authorized", "confirmatory_execution_authorized",
    ):
        if type(data.get(key)) is not bool or data.get(key) is not False:
            raise DesignError(f"execution gate opened: {key}")
    for group in ("pilot_gates", "gates"):
        gates = data.get(group)
        if not isinstance(gates, dict) or gates.get("critical_harm_thresholds_frozen_and_verified") is not False:
            raise DesignError(f"critical-harm launch gate missing or opened: {group}")


def verify() -> None:
    verify_task_identity_contract()
    verify_seed_contract()
    verify_critical_harm_contract()
    amendment.validate()
    verify_gate_closed()


if __name__ == "__main__":
    try:
        verify()
    except (DesignError, amendment.AmendmentError) as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: FAR-SWE-V3-001 review-closure contracts are prospective and execution remains blocked.")
