"""Defense-in-depth semantic verifier for FAR-SWE-V3-001 review-closure contracts."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
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
DESCRIPTOR_KEYS = [
    "algorithm_id",
    "repository_provider",
    "repository_provider_id",
    "canonical_repository_url",
    "repository_commit_sha",
    "task_payload_sha256",
    "task_payload_bytes",
]
EXPECTED_DESCRIPTOR_VALUES = {
    "algorithm_id": "far-swe-v3-task-bundle-root-v2",
    "repository_provider": "exact JSON string github.com; no other provider or self-hosted instance is permitted in FAR-SWE-V3-001",
    "repository_provider_id": "positive JSON integer equal to the decimal GitHub REST repository id returned by api.github.com for the repository; strings, owner/name text, zero, negatives, and alternate numeric encodings are prohibited",
    "canonical_repository_url": "exact HTTPS URL https://github.com/{full_name} where full_name is returned by api.github.com for repository_provider_id at freeze time; query, fragment, userinfo, explicit port, terminal .git suffix, and trailing slash are prohibited; URL spelling is audit metadata and never the repository-count identity",
    "repository_commit_sha": "lowercase 40-character Git commit SHA identifying the exact repository snapshot",
    "task_payload_sha256": "lowercase SHA-256 of the exact task/issue payload bytes supplied to the agent, before prompt wrapping",
    "task_payload_bytes": "nonnegative integer byte count of that exact task/issue payload",
}
EXPECTED_LEDGER_CONTRACT = {
    "status": "uninstantiated",
    "execution_authorized": False,
    "media_type": "application/json",
    "top_level_type": "array",
    "record_required_keys_exactly": [
        "blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "repository_provider",
        "repository_provider_id", "canonical_repository_url", "repository_commit_sha",
        "task_payload_sha256", "task_payload_bytes", "strata",
        "github_fork_source_repository_id", "contains_project_far_treatment_material",
    ],
    "array_binding_rule": "there is exactly one ledger record for every task-manifest record and no extras; ledger array position, blind_task_id, repository_blind_id, task_bundle_root_sha256, and strata must exactly match the corresponding frozen task-manifest record",
    "descriptor_binding_rule": "the seven descriptor fields algorithm_id=far-swe-v3-task-bundle-root-v2 plus repository_provider, repository_provider_id, canonical_repository_url, repository_commit_sha, task_payload_sha256, and task_payload_bytes reconstructed from each ledger record must recompute that record's task_bundle_root_sha256 exactly",
    "repository_binding_rule": "repository_provider must be exactly github.com and repository_provider_id must be a positive JSON integer independently resolved from api.github.com before freeze; equal provider/id pairs must use the same repository_blind_id and canonical_repository_url, distinct provider/id pairs must use distinct repository_blind_id values, and one canonical_repository_url may not map to multiple provider/id pairs",
    "population_rule": "minimum repository count and per-repository task cap are computed from distinct (repository_provider, repository_provider_id) pairs in this sealed ledger, never URL spellings or blind labels alone",
    "prohibited_repository_binding_rule": "every ledger record must satisfy prohibited_repository_contract: repository_provider_id must not equal the Project FAR repository ID, github_fork_source_repository_id must not equal the Project FAR repository ID, and contains_project_far_treatment_material must be boolean false",
    "access_control": "ledger contents containing repository and task identity material are sealed from the agent and capsule authors; only the independent preexecution identity auditor and explicitly authorized evidence custodians may access them before scoring freeze",
    "freeze_timing": "the exact ledger bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution and before any task identity is released to an executing agent",
    "launch_binding": "the separate prospective pilot or confirmatory launch record must name both the frozen task-manifest Git blob identity and frozen sealed-identity-ledger Git blob identity plus the retained repository-prohibition audit report root",
    "retention_rule": "the exact sealed ledger bytes, Git blob identity, independent validation report, and repository-prohibition audit report are retained in the experiment evidence store for post-run audit",
}
EXPECTED_PROHIBITED_REPOSITORY_CONTRACT = {
    "project_far_repository_provider": "github.com",
    "project_far_repository_provider_id": 1283452680,
    "reject_exact_project_far_repository": True,
    "reject_github_fork_source_project_far": True,
    "require_project_far_treatment_material_absent": True,
    "github_fork_source_rule": "github_fork_source_repository_id is null for a non-fork or a positive JSON integer equal to api.github.com source.id for a GitHub fork; a value equal to project_far_repository_provider_id is prohibited",
    "treatment_material_audit_rule": "before freeze, the independent task-identity auditor inspects the exact candidate repository commit for Project FAR treatment material using the frozen FAR capsule and current Project FAR source artifacts as the reference set; contains_project_far_treatment_material must be boolean false and the audit report is retained and launch-bound",
    "canonical_url_uniqueness_rule": "one authoritative (repository_provider, repository_provider_id) pair must map to exactly one canonical_repository_url and one canonical_repository_url must map to exactly one authoritative pair within the frozen sealed identity ledger",
    "failure_rule": "any exact Project FAR repository, Project FAR GitHub fork-source match, treatment-material-positive audit, canonical-URL/provider-ID inconsistency, or unavailable required prohibition evidence rejects the task population before execution",
}
EXPECTED_REPOSITORY_IDENTITY = {
    "supported_provider": "github.com only",
    "authoritative_identity": "the ordered pair (repository_provider, repository_provider_id), where repository_provider is exactly the JSON string github.com and repository_provider_id is a positive JSON integer equal to the api.github.com REST repository id resolved before freeze; URL strings and repository_blind_id labels are never repository identities",
    "github_identity_rule": "repository_provider must equal github.com exactly and repository_provider_id must be a positive JSON integer equal to the decimal GitHub REST repository id; strings, owner/repository text, host aliases, self-hosted GitHub instances, path-case variants, default-port variants, .git suffixes, redirects, and renames cannot create distinct repository identities",
    "canonical_url_rule": "canonical_repository_url must equal https://github.com/{full_name} using the full_name returned by api.github.com for the authoritative repository id at freeze time and is retained only for auditability; each authoritative provider/id pair has exactly one canonical URL in the ledger and each canonical URL maps to exactly one authoritative pair",
    "equal_authoritative_identities_same_blind_id": True,
    "distinct_authoritative_identities_distinct_blind_ids": True,
    "minimum_repository_count_basis": "count distinct (repository_provider, repository_provider_id) pairs in the sealed identity ledger, never URL strings or repository_blind_id labels alone",
    "per_repository_cap_basis": "apply the preregistered per-repository task cap by the same (repository_provider, repository_provider_id) pair in the sealed identity ledger before execution",
    "validation_timing": "validate every github.com repository identity from api.github.com, canonical URL one-to-one mapping, the ledger-to-manifest one-to-one binding, unique task-bundle roots, Project FAR repository/fork/treatment-material prohibitions, minimum repository count, per-repository cap, and required-strata coverage before any sacrificial pilot or confirmatory execution",
}
EXPECTED_ORDER = {
    "authoritative_sequence": "top-level JSON array order",
    "runtime_sorting_permitted": False,
    "locale_collation_permitted": False,
    "normalization_step": "none because identifiers are ASCII-only",
    "complete_case_filter": "remove records whose FAR or placebo primary cell is missing while preserving relative array order",
    "bootstrap_vector_mapping": "D_i index i is the corresponding retained array position after the stable complete-case filter",
}
EXPECTED_PREEXECUTION = [
    "record keys match the exact schema",
    "blind task identifiers are unique",
    "task bundle roots are unique so one authoritative task identity cannot occupy multiple manifest records or bootstrap units",
    "every strata value is a nonempty duplicate-free canonical-order subset of bug_fix, test_failure, behavioral_regression, API_or_contract_change, multi_file_change",
    "the union of strata across the frozen confirmatory task manifest covers bug_fix, test_failure, behavioral_regression, API_or_contract_change, and multi_file_change before execution",
    "all identifiers match their ASCII fixed-width patterns",
    "all task bundle roots are lowercase 64-character SHA-256 hex",
    "the sealed identity ledger contains exactly one record for every frozen task-manifest record, in the same array order, with exact matching blind identifiers, task root, and strata",
    "every task bundle root is independently recomputed from the corresponding sealed identity-ledger descriptor",
    "every repository_provider is exactly github.com and every repository_provider_id is a positive JSON integer independently resolved from api.github.com before counting or blind-ID assignment",
    "every canonical repository URL is derived from the authoritative GitHub repository id and returned full_name before counting or blind-ID assignment",
    "equal authoritative repository identities use the same repository blind ID and canonical URL, distinct authoritative identities use distinct blind IDs, and one canonical URL never maps to multiple authoritative identities",
    "no ledger repository_provider_id equals the Project FAR repository provider ID, no github_fork_source_repository_id equals it, and every contains_project_far_treatment_material value is boolean false under the retained independent prohibition audit",
    "minimum repository count and per-repository cap are computed from authoritative provider-stable repository identities in the sealed identity ledger rather than URL spellings or blind-ID label count",
    "the exact task manifest artifact bytes, sealed identity-ledger bytes, both Git blob identities, and repository-prohibition audit report root are committed before any sacrificial pilot or confirmatory execution",
]
LAUNCH_BINDINGS = [
    "frozen_design_commit", "design_manifest_git_blob_sha1", "task_manifest_git_blob_sha1",
    "sealed_identity_ledger_git_blob_sha1", "task_population_prohibition_audit_report_root",
    "bootstrap_seed_commitment_git_blob_sha1",
    "critical_harm_threshold_contract_git_blob_sha1", "far_capsule_root_sha256",
    "placebo_capsule_root_sha256", "model_provider_endpoint_version", "prompts_agent_configuration_root",
    "environment_image_digest_dependency_lock", "run_budgets_stopping_rules_root",
    "counterbalancing_assignment_seed_commitment", "grader_scoring_contract_root",
    "evidence_store_configuration_root", "branch_or_tag_protection_reference", "manual_authorization_record_identity",
]
PILOT_GATES = {
    "theory_version_frozen", "far_capsule_built_and_hash_frozen", "placebo_built_and_matching_verified",
    "confirmatory_task_population_frozen", "task_identity_information_barriers_verified",
    "model_endpoint_and_version_frozen", "prompts_and_agent_configuration_frozen",
    "environment_images_and_dependencies_frozen", "budgets_and_stopping_rules_frozen",
    "counterbalancing_and_randomization_seed_frozen", "grader_and_scoring_contract_frozen",
    "critical_harm_thresholds_frozen_and_verified", "evidence_store_and_restoration_test_passed",
    "independent_preexecution_review_clean", "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_pilot_launch_authorization_recorded",
}
GATES = (PILOT_GATES - {"manual_pilot_launch_authorization_recorded"}) | {
    "sacrificial_pilot_completed_and_excluded", "manual_launch_authorization_recorded"
}
EXPECTED_PILOT_GATE_RULE = "sacrificial pilot execution is authorized only when every pilot gate is true, the exact design manifest verifies, and a separate prospective pilot launch record committed before execution names every launch_record_required_bindings value for the frozen pilot configuration; sacrificial_pilot_completed_and_excluded is not a pilot prerequisite"
EXPECTED_GATE_RULE = "confirmatory execution is authorized only when every gate is true, the exact design manifest verifies, and a separate prospective confirmatory launch record committed before execution names every launch_record_required_bindings value for the frozen confirmatory configuration"


def _strict_object(path: Path, label: str) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError(f"{label} must be object")
    return value


def verify_task_identity_contract(path: Path = TASK) -> None:
    data = _strict_object(path, "task manifest contract")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("manifest_status")) != (
        "1.6", "FAR-SWE-V3-001", "Research", "uninstantiated"
    ) or type(data.get("execution_authorized")) is not bool or data.get("execution_authorized") is not False:
        raise DesignError("task manifest identity/boundary drifted")
    if data.get("freeze_timing") != "exact task manifest bytes and Git blob identity must be committed and independently reviewed before any sacrificial pilot or confirmatory execution; freezing or changing task identity, order, repository identity, strata, repository-prohibition evidence, or the sealed identity ledger after any agent run is prohibited even if outcomes or grades remain concealed":
        raise DesignError("task manifest prospective freeze timing drifted")
    integrity._require_type_exact(data.get("document_shape"), {
        "media_type": "application/json", "top_level_type": "array",
        "canonical_serialization": "UTF-8, LF line endings, no BOM, duplicate keys prohibited, NaN and infinities prohibited",
    }, "task manifest document shape")
    record = data.get("record_schema")
    if not isinstance(record, dict) or set(record) != {"required_keys_exactly", "blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"}:
        raise DesignError("task record schema shape drifted")
    integrity._require_type_exact(record.get("required_keys_exactly"), ["blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"], "task record keys")
    integrity._require_type_exact(record.get("blind_task_id"), {"pattern": "^TASK-[0-9]{6}$", "encoding": "ASCII subset of UTF-8", "unicode_permitted": False, "unique": True}, "blind task ID")
    integrity._require_type_exact(record.get("repository_blind_id"), {
        "pattern": "^REPO-[0-9]{4}$", "encoding": "ASCII subset of UTF-8", "unicode_permitted": False,
        "canonical_mapping": "repository_blind_id is a one-to-one label for authoritative_repository_identity: equal authoritative repository identities must use the same blind ID, and distinct authoritative repository identities must use distinct blind IDs",
    }, "repository blind ID")
    integrity._require_type_exact(record.get("task_bundle_root_sha256"), {
        "pattern": "^[0-9a-f]{64}$",
        "construction": "SHA-256 over the exact UTF-8 bytes of the canonical task-bundle descriptor defined by task_bundle_root_contract",
        "unique": True,
    }, "task bundle root field")
    integrity._require_type_exact(record.get("strata"), {
        "type": "nonempty_array_of_unique_strings", "allowed_values_in_canonical_order": STRATA_ORDER,
        "ordering_rule": "each record lists only applicable labels and preserves their relative order from allowed_values_in_canonical_order; duplicates, unknown labels, empty arrays, and alternative ordering are prohibited",
        "classification_timing": "classification is frozen in the exact task manifest before any sacrificial pilot or confirmatory execution",
        "coverage_rule": "the union of strata across the frozen confirmatory task manifest must contain every allowed_values_in_canonical_order label before execution",
    }, "task strata contract")
    root = data.get("task_bundle_root_contract")
    if not isinstance(root, dict) or set(root) != {
        "algorithm_id", "hash", "descriptor_media_type", "descriptor_canonicalization",
        "descriptor_required_keys_exactly", "descriptor_values", "required_root_members",
        "archive_or_filesystem_metadata_in_root", "path_order_or_archive_format_in_root", "recomputation_rule",
    }:
        raise DesignError("task bundle root contract shape drifted")
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2" or root.get("hash") != "SHA-256" or root.get("descriptor_media_type") != "application/json" or root.get("descriptor_canonicalization") != "RFC 8785 JSON Canonicalization Scheme (JCS); UTF-8 bytes; no BOM; no insignificant whitespace":
        raise DesignError("task bundle root algorithm/canonicalization drifted")
    integrity._require_type_exact(root.get("descriptor_required_keys_exactly"), DESCRIPTOR_KEYS, "task bundle descriptor keys")
    integrity._require_type_exact(root.get("descriptor_values"), EXPECTED_DESCRIPTOR_VALUES, "task bundle descriptor semantics")
    integrity._require_type_exact(root.get("required_root_members"), [
        "authoritative repository provider", "provider-stable repository identity", "canonical repository URL",
        "exact repository commit", "exact task/issue payload digest", "exact task/issue payload byte count",
    ], "task bundle required root members")
    if type(root.get("archive_or_filesystem_metadata_in_root")) is not bool or root.get("archive_or_filesystem_metadata_in_root") is not False or type(root.get("path_order_or_archive_format_in_root")) is not bool or root.get("path_order_or_archive_format_in_root") is not False:
        raise DesignError("task bundle root includes prohibited archive/path metadata")
    if root.get("recomputation_rule") != "independent auditors reconstruct the seven-key descriptor from the sealed identity-ledger record, JCS-canonicalize it, and SHA-256 the resulting bytes":
        raise DesignError("task bundle root recomputation rule drifted")
    integrity._require_type_exact(data.get("prohibited_repository_contract"), EXPECTED_PROHIBITED_REPOSITORY_CONTRACT, "prohibited repository contract")
    integrity._require_type_exact(data.get("sealed_identity_ledger_contract"), EXPECTED_LEDGER_CONTRACT, "sealed task identity ledger contract")
    integrity._require_type_exact(data.get("repository_identity_contract"), EXPECTED_REPOSITORY_IDENTITY, "repository identity contract")
    integrity._require_type_exact(data.get("order_contract"), EXPECTED_ORDER, "task order contract")
    integrity._require_type_exact(data.get("preexecution_validation"), EXPECTED_PREEXECUTION, "task preexecution validation")


def _load_array(path: Path, label: str) -> list[Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, list):
        raise DesignError(f"{label} must be array")
    return value


def validate_instantiated_task_manifest(path: Path, contract_path: Path = TASK) -> list[dict[str, Any]]:
    verify_task_identity_contract(contract_path)
    value = _load_array(path, "instantiated task manifest")
    if not value:
        raise DesignError("instantiated task manifest must be nonempty")
    blind_seen: set[str] = set()
    root_seen: set[str] = set()
    strata_seen: set[str] = set()
    rank = {name: index for index, name in enumerate(STRATA_ORDER)}
    out: list[dict[str, Any]] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != {"blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"}:
            raise DesignError(f"task manifest record shape drifted at index {index}")
        blind, repo_blind, root, strata = record["blind_task_id"], record["repository_blind_id"], record["task_bundle_root_sha256"], record["strata"]
        if type(blind) is not str or re.fullmatch(r"TASK-[0-9]{6}", blind) is None or blind in blind_seen:
            raise DesignError("blind task identifiers must be unique fixed-width ASCII labels")
        if type(repo_blind) is not str or re.fullmatch(r"REPO-[0-9]{4}", repo_blind) is None:
            raise DesignError("repository blind identifier syntax drifted")
        if type(root) is not str or re.fullmatch(r"[0-9a-f]{64}", root) is None or root in root_seen:
            raise DesignError("task bundle roots must be unique lowercase SHA-256 values")
        if not isinstance(strata, list) or not strata or any(type(item) is not str for item in strata):
            raise DesignError("task strata must be a nonempty string array")
        if len(strata) != len(set(strata)) or any(item not in rank for item in strata) or strata != sorted(strata, key=rank.__getitem__):
            raise DesignError("task strata contain duplicates, unknown labels, or noncanonical order")
        blind_seen.add(blind); root_seen.add(root); strata_seen.update(strata); out.append(record)
    if strata_seen != set(STRATA_ORDER):
        raise DesignError("frozen task manifest does not cover every preregistered stratum")
    return out


def _canonical_descriptor_bytes(record: dict[str, Any]) -> bytes:
    descriptor = {
        "algorithm_id": "far-swe-v3-task-bundle-root-v2",
        "repository_provider": record["repository_provider"],
        "repository_provider_id": record["repository_provider_id"],
        "canonical_repository_url": record["canonical_repository_url"],
        "repository_commit_sha": record["repository_commit_sha"],
        "task_payload_sha256": record["task_payload_sha256"],
        "task_payload_bytes": record["task_payload_bytes"],
    }
    return json.dumps(descriptor, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def validate_instantiated_identity_ledger(manifest_path: Path, ledger_path: Path, contract_path: Path = TASK) -> list[dict[str, Any]]:
    manifest = validate_instantiated_task_manifest(manifest_path, contract_path)
    ledger = _load_array(ledger_path, "sealed identity ledger")
    if len(ledger) != len(manifest):
        raise DesignError("sealed identity ledger must contain exactly one record per manifest record")
    required = set(EXPECTED_LEDGER_CONTRACT["record_required_keys_exactly"])
    provider_to_blind: dict[tuple[str, int], str] = {}
    blind_to_provider: dict[str, tuple[str, int]] = {}
    provider_to_url: dict[tuple[str, int], str] = {}
    url_to_provider: dict[str, tuple[str, int]] = {}
    repo_counts: Counter[tuple[str, int]] = Counter()
    for index, (blind_record, identity) in enumerate(zip(manifest, ledger)):
        if not isinstance(identity, dict) or set(identity) != required:
            raise DesignError(f"sealed identity ledger record shape drifted at index {index}")
        for key in ("blind_task_id", "repository_blind_id", "task_bundle_root_sha256", "strata"):
            if not integrity._type_exact_equal(identity[key], blind_record[key]):
                raise DesignError(f"sealed ledger/manifest binding drifted: {key} at index {index}")
        if identity["repository_provider"] != "github.com" or type(identity["repository_provider_id"]) is not int or identity["repository_provider_id"] <= 0:
            raise DesignError("sealed ledger requires github.com plus positive integer REST repository id")
        if identity["repository_provider_id"] == EXPECTED_PROHIBITED_REPOSITORY_CONTRACT["project_far_repository_provider_id"]:
            raise DesignError("Project FAR repository is prohibited from the task population")
        fork_source = identity["github_fork_source_repository_id"]
        if fork_source is not None and (type(fork_source) is not int or fork_source <= 0):
            raise DesignError("GitHub fork source repository id must be null or a positive integer")
        if fork_source == EXPECTED_PROHIBITED_REPOSITORY_CONTRACT["project_far_repository_provider_id"]:
            raise DesignError("Project FAR forks are prohibited from the task population")
        treatment_material = identity["contains_project_far_treatment_material"]
        if type(treatment_material) is not bool or treatment_material is not False:
            raise DesignError("Project FAR treatment material must be independently audited absent")
        url = identity["canonical_repository_url"]
        if type(url) is not str or re.fullmatch(r"https://github\.com/[^/?#]+/[^/?#]+", url) is None or url.endswith(".git") or url.endswith("/"):
            raise DesignError("sealed ledger canonical repository URL drifted")
        if type(identity["repository_commit_sha"]) is not str or re.fullmatch(r"[0-9a-f]{40}", identity["repository_commit_sha"]) is None:
            raise DesignError("sealed ledger repository commit identity drifted")
        if type(identity["task_payload_sha256"]) is not str or re.fullmatch(r"[0-9a-f]{64}", identity["task_payload_sha256"]) is None:
            raise DesignError("sealed ledger task payload digest drifted")
        if type(identity["task_payload_bytes"]) is not int or identity["task_payload_bytes"] < 0:
            raise DesignError("sealed ledger task payload byte count drifted")
        recomputed = hashlib.sha256(_canonical_descriptor_bytes(identity)).hexdigest()
        if recomputed != identity["task_bundle_root_sha256"]:
            raise DesignError("sealed ledger descriptor does not recompute task bundle root")
        provider_id = (identity["repository_provider"], identity["repository_provider_id"])
        blind_id = identity["repository_blind_id"]
        if provider_id in provider_to_blind and provider_to_blind[provider_id] != blind_id:
            raise DesignError("equal authoritative repositories use different blind IDs")
        if blind_id in blind_to_provider and blind_to_provider[blind_id] != provider_id:
            raise DesignError("one repository blind ID maps to multiple authoritative repositories")
        if provider_id in provider_to_url and provider_to_url[provider_id] != url:
            raise DesignError("one authoritative repository maps to multiple canonical URLs")
        if url in url_to_provider and url_to_provider[url] != provider_id:
            raise DesignError("one canonical URL maps to multiple authoritative repositories")
        provider_to_blind[provider_id] = blind_id
        blind_to_provider[blind_id] = provider_id
        provider_to_url[provider_id] = url
        url_to_provider[url] = provider_id
        repo_counts[provider_id] += 1
    if len(ledger) < 24:
        raise DesignError("confirmatory ledger contains fewer than 24 tasks")
    if len(repo_counts) < 5:
        raise DesignError("confirmatory ledger contains fewer than five authoritative repositories")
    if max(repo_counts.values(), default=0) * 5 > len(ledger):
        raise DesignError("one authoritative repository exceeds the 20% task cap")
    return ledger


def verify_seed_contract(path: Path = SEED) -> None:
    data = _strict_object(path, "bootstrap seed commitment")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("commitment_status")) != (
        "1.1", "FAR-SWE-V3-001", "Research", "frozen_pre_execution"
    ):
        raise DesignError("bootstrap seed commitment identity drifted")
    expected_authority = {
        "scope": "bootstrap_seed_value_and_rng_procedure_only",
        "precedence": "This prospective contract governs only the bootstrap seed value, encoding, RNG procedure identity, and commitment timing. It does not assert that any other preregistration field is unchanged and it does not supersede later prospective amendments on unrelated subjects.",
        "outcome_exposure_status": "none", "model_calls_authorized": False, "pilot_execution_authorized": False,
        "benchmark_execution_authorized": False, "confirmatory_execution_authorized": False,
    }
    integrity._require_type_exact(data.get("authority"), expected_authority, "bootstrap seed authority")
    rng = data.get("rng_contract")
    if not isinstance(rng, dict) or set(rng) != {"procedure_id", "seed_encoding", "seed_hex"} or rng.get("procedure_id") != "sha256_rejection_stream_v1" or rng.get("seed_encoding") != "64 lowercase hexadecimal characters decoded as exactly 32 bytes":
        raise DesignError("bootstrap RNG contract drifted")
    seed = rng.get("seed_hex")
    if type(seed) is not str or re.fullmatch(r"[0-9a-f]{64}", seed) is None or len(bytes.fromhex(seed)) != 32:
        raise DesignError("bootstrap seed encoding drifted")
    if seed != "76764013d297cadd3865295298e160a9fbb1a39833aac5860b0dfb13f54fdf87":
        raise DesignError("frozen bootstrap seed value drifted")
    integrity._require_type_exact(data.get("commitment"), {
        "method": "direct_precommitted_value",
        "committed_value_source": "rng_contract.seed_hex in this exact integrity-rooted artifact",
        "artifact_inputs_permitted": False, "mutable_launch_inputs_permitted": False,
        "task_identity_inputs_permitted": False, "outcome_or_grade_inputs_permitted": False,
        "replacement_or_seed_search_after_commitment_permitted": False,
        "verification_rule": "verify the exact committed seed encoding and value from this artifact; no current capsule, execution-gate, task-manifest, repository-history, or other mutable artifact identity participates in the seed value",
    }, "bootstrap direct commitment")
    integrity._require_type_exact(data.get("timing"), {
        "must_be_committed_and_integrity_rooted_before_any_sacrificial_pilot_execution": True,
        "must_be_committed_and_integrity_rooted_before_any_confirmatory_execution": True,
        "must_precede_any_pilot_or_confirmatory_outcome_reveal": True, "immutable_after_commitment": True,
    }, "bootstrap seed timing")
    if data.get("nonclaims") != [
        "This commitment does not authorize model calls, pilot execution, benchmark execution, confirmatory execution, grading, or outcome reveal.",
        "This commitment does not freeze the task population, assignment-randomization seed, treatment capsule, placebo, model endpoint, environment, budgets, thresholds, or launch authorization.",
        "This commitment does not establish that FAR improves software engineering.",
    ]:
        raise DesignError("bootstrap seed nonclaims drifted")


def verify_critical_harm_contract(path: Path = HARM) -> None:
    data = _strict_object(path, "critical-harm threshold contract")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("stage")) != (
        "1.1", "FAR-SWE-V3-001", "Research", "design_only"
    ) or type(data.get("execution_authorized")) is not bool or data.get("execution_authorized") is not False:
        raise DesignError("critical-harm contract identity/boundary drifted")
    if data.get("freeze_timing") != "the exact contract bytes and Git blob identity must be committed, integrity-rooted, and independently verified before any sacrificial pilot or confirmatory execution; post-exposure threshold selection is prohibited":
        raise DesignError("critical-harm prospective freeze timing drifted")
    if data.get("number_system") != "exact reduced rational arithmetic over arbitrary-precision integers; floating point is prohibited for threshold decisions":
        raise DesignError("critical-harm number system drifted")
    zero = data.get("zero_tolerance_harms")
    expected_zero_ids = {"authorization_or_information_barrier_violation", "hidden_task_leakage", "unmatched_access", "evidence_loss"}
    if not isinstance(zero, dict) or set(zero) != expected_zero_ids:
        raise DesignError("zero-tolerance harm set drifted")
    expected_zero_numerators = {
        "authorization_or_information_barrier_violation": "number of exact frozen repetition slots invalidated by any verified authorization violation or information-barrier breach; a global breach counts every frozen slot whose evidence or causal isolation is compromised",
        "hidden_task_leakage": "number of exact frozen repetition slots invalidated by verified exposure of hidden task identity, hidden tests, gold patches, sealed task content, or equivalent prohibited task information to a prohibited actor or arm; a global leak counts every affected frozen slot",
        "unmatched_access": "number of exact frozen repetition slots invalidated by any verified unmatched tool permission, context-window allowance, model-call allowance, token budget, wall-clock budget, cost budget, repository access, or other execution resource across mandatory arms",
        "evidence_loss": "number of exact frozen repetition slots whose required retained evidence is missing, corrupt, unverifiable, or insufficient to independently reconstruct the run and its classification under the frozen contracts",
    }
    zero_denominator = "exact total number of preregistered frozen repetition slots across all mandatory arms before execution; same-slot replacements never add denominator slots"
    for name, harm in zero.items():
        integrity._require_type_exact(harm, {
            "slot_numerator": expected_zero_numerators[name], "slot_denominator": zero_denominator,
            "incidence_rate": "slot_numerator / slot_denominator reduced exactly",
            "critical_threshold": {"allowed_occurrences": 0}, "trigger_rule": "slot_numerator > 0",
        }, f"zero-tolerance harm {name}")
    rate = data.get("rate_harms")
    if not isinstance(rate, dict) or set(rate) != {"regression_introduction_rate", "invalid_run_rate"}:
        raise DesignError("rate-harm set drifted")
    rate_denominator = "exact preregistered number of frozen repetition slots in that arm before any execution; resolved, unresolved, invalid, and replacement-eligible terminal states remain in the denominator; a same-slot replacement never creates an additional denominator slot"
    expected_numerators = {
        "regression_introduction_rate": "number of exact frozen repetition slots for which every frozen regression test used by the harm rule passes in the pristine frozen repository/environment control immediately before the slot and at least one of those same tests fails against the submitted workspace after the run; no causal-attribution override, operator waiver, or post-hoc exclusion is permitted; each slot contributes at most one",
        "invalid_run_rate": "number of exact frozen repetition slots whose retained terminal outcome is invalid after the single permitted same-slot infrastructure replacement process is exhausted or inapplicable; each frozen slot contributes at most one",
    }
    for name, harm in rate.items():
        integrity._require_type_exact(harm, {
            "slot_numerator": expected_numerators[name], "slot_denominator": rate_denominator,
            "arm_rate": "slot_numerator / slot_denominator reduced exactly",
            "contrast": "FAR arm rate minus placebo arm rate using exact rational subtraction",
            "critical_threshold": {"numerator": 1, "denominator": 10}, "trigger_rule": "contrast >= 1/10",
        }, f"rate harm {name}")
    if data.get("bounded_positive_rule") != "bounded_positive is prohibited if any zero-tolerance harm triggers or either exact FAR-minus-placebo rate contrast is >= 1/10":
        raise DesignError("critical-harm positive-classification gate drifted")
    integrity._require_type_exact(data.get("evidence_retention"), {
        "required_for_each_zero_tolerance_harm": ["harm_id", "slot_numerator", "slot_denominator", "reduced_rational_incidence_rate", "threshold", "trigger_rule", "triggered"],
        "required_for_each_rate_harm": ["harm_id", "far_numerator", "far_denominator", "far_reduced_rational_rate", "placebo_numerator", "placebo_denominator", "placebo_reduced_rational_rate", "reduced_rational_contrast", "threshold", "triggered"],
        "required_provenance": ["frozen_design_commit", "frozen_task_manifest_git_blob_sha1", "frozen_task_identity_ledger_git_blob_sha1", "grader_version", "evidence_bundle_content_root"],
    }, "critical-harm evidence retention")
    if data.get("versioning_rule") != "Any threshold, numerator predicate, denominator rule, comparison rule, evidence requirement, or harm-set change after any pilot or confirmatory exposure creates a new experiment version and cannot retroactively govern existing runs.":
        raise DesignError("critical-harm post-exposure mutability enabled")
    if data.get("nonclaims") != [
        "These thresholds do not authorize execution.",
        "The 1/10 rate-difference threshold is a preregistered decision rule for FAR-SWE-V3-001 and is not asserted to be a universal safety threshold.",
        "Passing these gates does not establish FAR safety, superiority, or commercial readiness.",
    ]:
        raise DesignError("critical-harm nonclaims drifted")


def verify_gate_closed(path: Path = GATE) -> None:
    data = integrity._load_json(path)
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status")) != ("1.5", "FAR-SWE-V3-001", "Research"):
        raise DesignError("execution gate schema/identity drifted")
    for key in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized"):
        if type(data.get(key)) is not bool or data.get(key) is not False:
            raise DesignError(f"execution gate opened or changed type: {key}")
    integrity._require_type_exact(data.get("launch_record_required_bindings"), LAUNCH_BINDINGS, "launch record required bindings")
    if data.get("pilot_gate_rule") != EXPECTED_PILOT_GATE_RULE or data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("launch gate rule drifted")
    for group, keys in (("pilot_gates", PILOT_GATES), ("gates", GATES)):
        value = data.get(group)
        if not isinstance(value, dict) or set(value) != keys or any(type(v) is not bool or v is not False for v in value.values()):
            raise DesignError(f"{group} must contain exact false gate set")
    integrity._require_type_exact(data.get("current_blockers"), [
        "theory version is not frozen for this experiment", "FAR treatment capsule does not exist", "placebo does not exist",
        "tasks, sealed identity ledger, repository-prohibition audit, model, prompts, environments, budgets, randomization, grader, and critical-harm threshold verification are not frozen or complete",
        "evidence storage and sacrificial pilot are not complete",
        "independent review and separate fully bound pilot/confirmatory launch authorization are absent",
    ], "current execution blockers")
    integrity._require_type_exact(data.get("forbidden_current_actions"), [
        "model access probe", "agent model call", "benchmark task selection with capsule-author access",
        "pilot execution", "confirmatory execution", "outcome reveal", "claim of FAR improvement",
    ], "forbidden current actions")


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
