#!/usr/bin/env python3
"""Corrective entrypoint for FAR-EVIDENCE-AUTHORITY-MODEL-001.

The base discovery and campaign engine remains in ``validator_core_v1.py``.
This entrypoint enforces the reviewed authority-sensitive rules: lower numeric
priority means higher authority, activation decisions must carry complete
resolvable provenance, and every declared provenance field has a mutation
control. Synthetic activation data is non-operative Research evidence only.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import pathlib
from datetime import date
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
CORE_PATH = HERE / "validator_core_v1.py"
_spec = importlib.util.spec_from_file_location("evidence_authority_validator_core", CORE_PATH)
core = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(core)

SYNTHETIC_MANIFEST_ID = "FAR-EVIDENCE-AUTHORITY-MODEL-001-SYNTHETIC-MANIFEST"
SYNTHETIC_MANIFEST_VERSION = "1.0"
MANIFEST_DECISION_ID = "synthetic://manifest-acceptance-decision-v1.0"
PRIORITY_ORDER = "lower_is_higher"
PROVENANCE_FIELDS = ("decision_date", "supporting_evidence", "scope", "limitations")
PROVENANCE_REQUIREMENT_FLAGS = (
    "decision_date_required",
    "supporting_evidence_required",
    "scope_required",
    "limitations_required",
)

# The campaign evaluates many mutations against the same immutable tree. Cache
# immutable Git blobs and parsed documents so the research execution can run in
# CI without repeating hundreds of subprocess and parser calls per mutation.
_original_read_text = core.FrozenTree.read_text
_original_load_json = core.FrozenTree.load_json
_original_load_yaml = core.FrozenTree.load_yaml


def _cached_read_text(self: Any, path: str) -> str:
    cache = getattr(self, "_evidence_authority_text_cache", None)
    if cache is None:
        cache = {}
        setattr(self, "_evidence_authority_text_cache", cache)
    if path not in cache:
        cache[path] = _original_read_text(self, path)
    return cache[path]


def _cached_load_json(self: Any, path: str) -> Any:
    cache = getattr(self, "_evidence_authority_json_cache", None)
    if cache is None:
        cache = {}
        setattr(self, "_evidence_authority_json_cache", cache)
    if path not in cache:
        cache[path] = _original_load_json(self, path)
    return cache[path]


def _cached_load_yaml(self: Any, path: str) -> Any:
    cache = getattr(self, "_evidence_authority_yaml_cache", None)
    if cache is None:
        cache = {}
        setattr(self, "_evidence_authority_yaml_cache", cache)
    if path not in cache:
        cache[path] = _original_load_yaml(self, path)
    return cache[path]


core.FrozenTree.read_text = _cached_read_text
core.FrozenTree.load_json = _cached_load_json
core.FrozenTree.load_yaml = _cached_load_yaml


def _candidate_manifest_schema() -> dict[str, Any]:
    return core.load_json(core.MANIFEST_PATH)


def _record_digest(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_digest"}
    return core.canonical_digest(payload)


def _manifest_digest(manifest: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in manifest.items()
        if key not in {"decision_records", "manifest_digest"}
    }
    return core.canonical_digest(payload)


def _nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _validate_requirement_declarations(manifest_schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    maps = {
        "acceptance": manifest_schema.get("acceptance_decision_record_requirements"),
        "per_entry": manifest_schema.get("per_entry_decision_record_requirements"),
    }
    for label, requirements in maps.items():
        if not isinstance(requirements, dict):
            errors.append(f"candidate_manifest_requirement_map_missing:{label}")
            continue
        for flag in (
            "record_must_resolve_from_explicit_store",
            "tamper_evident_record_digest_required",
            *PROVENANCE_REQUIREMENT_FLAGS,
        ):
            if requirements.get(flag) is not True:
                errors.append(f"candidate_manifest_requirement_missing:{label}:{flag}")
    return errors


def adjudicate_claims(
    claims: list[dict[str, Any]],
    conflict_policy: dict[str, Any],
) -> dict[str, Any]:
    """Adjudicate concrete claims using the declared lower-rank-is-higher rule."""
    if not claims:
        return {"result": "Unknown", "reason": "no_claims"}
    identities = {core.claim_identity(claim) for claim in claims}
    if len(identities) != 1:
        return {"result": "Incomparable", "reason": "different_claim_identity"}
    priorities = [int(claim["priority"]) for claim in claims]
    selected = min(priorities) if PRIORITY_ORDER == "lower_is_higher" else max(priorities)
    top = [claim for claim in claims if int(claim["priority"]) == selected]
    polarities = {claim["polarity"] for claim in top}
    if len(polarities) > 1:
        if (
            conflict_policy.get("dual_authority_for_proposition_and_negation_prohibited")
            and conflict_policy.get("equal_priority_unresolved_result") == "Unknown"
        ):
            return {
                "result": "Unknown",
                "reason": "equal_priority_contradiction",
                "artifacts": sorted(claim["artifact"] for claim in top),
            }
        return {
            "result": "DualAuthority",
            "reason": "equal_priority_contradiction_not_fail_closed",
        }
    return {
        "result": next(iter(polarities)),
        "reason": "unique_highest_authority_polarity",
        "selected_numeric_priority": selected,
        "numeric_priority_order": PRIORITY_ORDER,
        "artifacts": sorted(claim["artifact"] for claim in top),
    }


def unequal_priority_probe(policy: dict[str, Any]) -> dict[str, Any]:
    common = {
        "proposition_id": "PRIORITY-CONTROL-001",
        "scope": "frozen unequal-priority control scope",
        "premises": ["P-A", "P-B"],
        "version": "1.0",
    }
    return adjudicate_claims(
        [
            {
                **common,
                "artifact": "synthetic://accepted-governance.json",
                "authority_class": "governance_decision",
                "priority": 1,
                "polarity": "Affirmed",
            },
            {
                **common,
                "artifact": "synthetic://research-record.json",
                "authority_class": "research_record",
                "priority": 5,
                "polarity": "Denied",
            },
        ],
        policy,
    )


def _provenance(
    *,
    scope: str,
    limitations: list[str],
    evidence: list[str],
) -> dict[str, Any]:
    return {
        "decision_date": "2026-07-30",
        "supporting_evidence": evidence,
        "scope": scope,
        "limitations": limitations,
    }


def synthetic_activation_manifest(inventory: dict[str, set[str]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for index, artifact in enumerate(sorted(inventory)):
        authority_bearing = index == 0
        entries.append(
            {
                "artifact": artifact,
                "artifact_status": "Accepted" if authority_bearing else "Research",
                "authority_bearing": authority_bearing,
                "status_decision_record": f"synthetic://artifact-status-decision-{index:03d}",
                "scope": "frozen validation control",
                "limitations": ["synthetic non-operative activation probe only"],
            }
        )
    manifest: dict[str, Any] = {
        "manifest_id": SYNTHETIC_MANIFEST_ID,
        "manifest_version": SYNTHETIC_MANIFEST_VERSION,
        "status": "Accepted",
        "active": True,
        "synthetic_nonoperative_probe": True,
        "acceptance_decision_required_for_activation": True,
        "acceptance_decision_record": MANIFEST_DECISION_ID,
        "required_entry_fields": sorted(core.REQUIRED_MANIFEST_ENTRY_FIELDS),
        "entries": entries,
    }
    manifest_digest = _manifest_digest(manifest)
    manifest["manifest_digest"] = manifest_digest
    records: dict[str, dict[str, Any]] = {}
    manifest_record = {
        "record_id": MANIFEST_DECISION_ID,
        "decision_type": "manifest_acceptance",
        "decision_status": "Accepted",
        "authority_class": "governance_decision",
        "governance_authority_status": "Accepted",
        "independent_of_candidate": True,
        "synthetic_nonoperative_probe": True,
        "manifest_id": SYNTHETIC_MANIFEST_ID,
        "manifest_version": SYNTHETIC_MANIFEST_VERSION,
        "manifest_digest": manifest_digest,
        **_provenance(
            scope="synthetic non-operative manifest acceptance probe",
            limitations=[
                "Research validation only",
                "does not Accept Promote activate or authorize Repository Change",
            ],
            evidence=[
                "research/evidence-authority-model/execution-spec-v1.0.json",
                "synthetic://frozen-campaign-primary-evidence",
            ],
        ),
    }
    manifest_record["record_digest"] = _record_digest(manifest_record)
    records[MANIFEST_DECISION_ID] = manifest_record
    for entry in entries:
        record_id = entry["status_decision_record"]
        record = {
            "record_id": record_id,
            "decision_type": "artifact_status_and_authority_designation",
            "decision_status": "Accepted",
            "authority_class": "governance_decision",
            "governance_authority_status": "Accepted",
            "independent_of_candidate": True,
            "synthetic_nonoperative_probe": True,
            "manifest_id": SYNTHETIC_MANIFEST_ID,
            "manifest_version": SYNTHETIC_MANIFEST_VERSION,
            "manifest_digest": manifest_digest,
            "artifact": entry["artifact"],
            "artifact_status": entry["artifact_status"],
            "authority_bearing": entry["authority_bearing"],
            **_provenance(
                scope=f"synthetic status decision for {entry['artifact']}",
                limitations=[
                    "Research validation only",
                    "does not assign current status or proof authority",
                ],
                evidence=[
                    "research/evidence-authority-model/execution-spec-v1.0.json",
                    entry["artifact"],
                ],
            ),
        }
        record["record_digest"] = _record_digest(record)
        records[record_id] = record
    manifest["decision_records"] = records
    return manifest


def _validate_decision_record(
    record_id: Any,
    records: dict[str, Any],
    *,
    expected: dict[str, Any],
    requirements: dict[str, Any],
    prefix: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(record_id, str) or record_id not in records:
        return [f"{prefix}_record_missing:{record_id}"]
    record = records[record_id]
    if not isinstance(record, dict):
        return [f"{prefix}_record_not_object:{record_id}"]
    required = {
        "record_id": record_id,
        "decision_status": "Accepted",
        "authority_class": "governance_decision",
        "governance_authority_status": "Accepted",
        "independent_of_candidate": True,
        "synthetic_nonoperative_probe": True,
        **expected,
    }
    for field, value in required.items():
        if record.get(field) != value:
            errors.append(f"{prefix}_field_mismatch:{record_id}:{field}")

    if requirements.get("decision_date_required"):
        if "decision_date" not in record:
            errors.append(f"{prefix}_required_field_missing:{record_id}:decision_date")
        elif not _valid_iso_date(record.get("decision_date")):
            errors.append(f"{prefix}_required_field_invalid:{record_id}:decision_date")
    if requirements.get("supporting_evidence_required"):
        if "supporting_evidence" not in record:
            errors.append(f"{prefix}_required_field_missing:{record_id}:supporting_evidence")
        elif not _nonempty_string_list(record.get("supporting_evidence")):
            errors.append(f"{prefix}_required_field_invalid:{record_id}:supporting_evidence")
    scope_required = requirements.get("scope_required") or requirements.get(
        "scope_and_limitations_required"
    )
    if scope_required:
        if "scope" not in record:
            errors.append(f"{prefix}_required_field_missing:{record_id}:scope")
        elif not isinstance(record.get("scope"), str) or not record["scope"].strip():
            errors.append(f"{prefix}_required_field_invalid:{record_id}:scope")
    limitations_required = requirements.get("limitations_required") or requirements.get(
        "scope_and_limitations_required"
    )
    if limitations_required:
        if "limitations" not in record:
            errors.append(f"{prefix}_required_field_missing:{record_id}:limitations")
        elif not _nonempty_string_list(record.get("limitations")):
            errors.append(f"{prefix}_required_field_invalid:{record_id}:limitations")

    observed_digest = record.get("record_digest")
    if not isinstance(observed_digest, str) or observed_digest != _record_digest(record):
        errors.append(f"{prefix}_hash_mismatch:{record_id}")
    return errors


def validate_manifest_entries(
    manifest: dict[str, Any],
    inventory: dict[str, set[str]],
    status_policy: dict[str, Any],
    *,
    activation: bool,
) -> list[str]:
    if not activation:
        errors: list[str] = []
        if manifest.get("status") != "Research" or manifest.get("active") is not False:
            errors.append("manifest_not_inactive_research")
        if not manifest.get("acceptance_decision_required_for_activation"):
            errors.append("manifest_acceptance_decision_not_required")
        if manifest.get("acceptance_decision_record") is not None:
            errors.append("manifest_claims_unearned_acceptance")
        return errors

    errors: list[str] = []
    schema = _candidate_manifest_schema()
    acceptance_requirements = schema.get("acceptance_decision_record_requirements", {})
    entry_requirements = schema.get("per_entry_decision_record_requirements", {})
    if manifest.get("status") != "Accepted" or manifest.get("active") is not True:
        errors.append("activation_manifest_not_accepted_active")
    if manifest.get("synthetic_nonoperative_probe") is not True:
        errors.append("activation_probe_not_explicitly_nonoperative")
    manifest_id = manifest.get("manifest_id")
    manifest_version = manifest.get("manifest_version")
    if manifest_id != SYNTHETIC_MANIFEST_ID:
        errors.append("activation_manifest_id_mismatch")
    if manifest_version != SYNTHETIC_MANIFEST_VERSION:
        errors.append("activation_manifest_version_mismatch")
    expected_manifest_digest = _manifest_digest(manifest)
    if manifest.get("manifest_digest") != expected_manifest_digest:
        errors.append("activation_manifest_digest_mismatch")
    records = manifest.get("decision_records")
    if not isinstance(records, dict):
        records = {}
        errors.append("decision_record_store_missing")
    errors.extend(
        _validate_decision_record(
            manifest.get("acceptance_decision_record"),
            records,
            expected={
                "decision_type": "manifest_acceptance",
                "manifest_id": manifest_id,
                "manifest_version": manifest_version,
                "manifest_digest": expected_manifest_digest,
            },
            requirements=acceptance_requirements,
            prefix="manifest_decision",
        )
    )
    required_status = status_policy.get("required_status_for_authority_bearing_artifact")
    if required_status != "Accepted":
        errors.append("proof_status_policy_not_accepted")
    if not status_policy.get("authority_bearing_designation_required"):
        errors.append("authority_bearing_designation_not_required")
    if not status_policy.get("exactly_one_status_per_registered_artifact"):
        errors.append("exactly_one_status_not_required")
    if not status_policy.get("non_authority_bearing_artifacts_excluded_from_active_proof_authority"):
        errors.append("non_authority_bearing_not_excluded")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return errors + ["manifest_entries_not_list"]
    by_artifact: dict[str, list[dict[str, Any]]] = core.defaultdict(list)
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"manifest_entry_not_object:{index}")
            continue
        missing = core.REQUIRED_MANIFEST_ENTRY_FIELDS - set(entry)
        for field in sorted(missing):
            errors.append(f"manifest_missing_field:{index}:{field}")
        artifact = entry.get("artifact")
        if isinstance(artifact, str):
            by_artifact[artifact].append(entry)
        status = entry.get("artifact_status")
        if status not in core.CHARTER_STATUSES:
            errors.append(f"manifest_invalid_status:{index}:{status}")
        designation = entry.get("authority_bearing")
        if not isinstance(designation, bool):
            errors.append(f"manifest_invalid_authority_designation:{index}")
        if designation is True and status != required_status:
            errors.append(f"authority_bearing_not_accepted:{index}:{status}")
        errors.extend(
            _validate_decision_record(
                entry.get("status_decision_record"),
                records,
                expected={
                    "decision_type": "artifact_status_and_authority_designation",
                    "manifest_id": manifest_id,
                    "manifest_version": manifest_version,
                    "manifest_digest": expected_manifest_digest,
                    "artifact": artifact,
                    "artifact_status": status,
                    "authority_bearing": designation,
                },
                requirements=entry_requirements,
                prefix="status_decision",
            )
        )
    expected_artifacts = set(inventory)
    actual_artifacts = set(by_artifact)
    for artifact in sorted(expected_artifacts - actual_artifacts):
        errors.append(f"manifest_missing_artifact:{artifact}")
    for artifact in sorted(actual_artifacts - expected_artifacts):
        errors.append(f"manifest_unregistered_artifact:{artifact}")
    for artifact, artifact_entries in sorted(by_artifact.items()):
        if len(artifact_entries) != 1:
            errors.append(f"manifest_duplicate_artifact:{artifact}:{len(artifact_entries)}")
    return errors


_original_validate_candidate = core.validate_candidate


def validate_candidate(
    *args: Any,
    numeric_priority_order: str = "lower_is_higher",
    **kwargs: Any,
) -> dict[str, Any]:
    global PRIORITY_ORDER
    previous = PRIORITY_ORDER
    PRIORITY_ORDER = numeric_priority_order
    try:
        result = _original_validate_candidate(*args, **kwargs)
        candidate_manifest = kwargs.get("manifest") or core.load_json(core.MANIFEST_PATH)
        result["errors"].extend(_validate_requirement_declarations(candidate_manifest))
        registry = kwargs.get("registry") or core.load_json(core.REGISTRY_PATH)
        probe = unequal_priority_probe(registry.get("conflict_policy", {}))
        if probe.get("result") != "Affirmed":
            result["errors"].append(f"priority_probe_wrong_winner:{probe.get('result')}")
        result["unequal_priority_probe"] = probe
        result["valid"] = not result["errors"]
        return result
    finally:
        PRIORITY_ORDER = previous


def execute_negative_controls(frozen: Any) -> list[dict[str, Any]]:
    controls = core._original_execute_negative_controls(frozen)
    inventory, _, _ = core.discover_proof_paths(frozen)
    activation = synthetic_activation_manifest(inventory)

    def record(control_id: str, result: dict[str, Any], expected_prefix: str) -> None:
        observed = [error for error in result["errors"] if error.startswith(expected_prefix)]
        controls.append(
            {
                "control_id": control_id,
                "expected_failure": expected_prefix,
                "observed_failures": observed,
                "detected": bool(observed) and not result["valid"],
            }
        )

    record(
        "reverse_numeric_priority_order",
        validate_candidate(
            frozen,
            numeric_priority_order="higher_is_higher",
            enforce_research_only_placement=False,
        ),
        "priority_probe_wrong_winner:Denied",
    )
    missing = copy.deepcopy(activation)
    missing["decision_records"].pop(MANIFEST_DECISION_ID)
    record(
        "remove_manifest_acceptance_decision_record",
        validate_candidate(
            frozen,
            activation_manifest=missing,
            enforce_research_only_placement=False,
        ),
        "manifest_decision_record_missing:",
    )
    mismatched = copy.deepcopy(activation)
    mismatched["decision_records"][MANIFEST_DECISION_ID]["manifest_version"] = "WRONG"
    record(
        "mismatch_manifest_acceptance_decision_version",
        validate_candidate(
            frozen,
            activation_manifest=mismatched,
            enforce_research_only_placement=False,
        ),
        "manifest_decision_field_mismatch:",
    )
    unauthoritative = copy.deepcopy(activation)
    unauthoritative["decision_records"][MANIFEST_DECISION_ID][
        "governance_authority_status"
    ] = "Research"
    record(
        "reject_non_authoritative_manifest_governance",
        validate_candidate(
            frozen,
            activation_manifest=unauthoritative,
            enforce_research_only_placement=False,
        ),
        "manifest_decision_field_mismatch:",
    )
    broken = copy.deepcopy(activation)
    broken["decision_records"][MANIFEST_DECISION_ID]["record_digest"] = "0" * 64
    record(
        "break_manifest_acceptance_decision_hash_lock",
        validate_candidate(
            frozen,
            activation_manifest=broken,
            enforce_research_only_placement=False,
        ),
        "manifest_decision_hash_mismatch:",
    )
    first_entry = activation["entries"][0]
    status_id = first_entry["status_decision_record"]
    missing_status = copy.deepcopy(activation)
    missing_status["decision_records"].pop(status_id)
    record(
        "remove_artifact_status_decision_record",
        validate_candidate(
            frozen,
            activation_manifest=missing_status,
            enforce_research_only_placement=False,
        ),
        "status_decision_record_missing:",
    )
    bad_link = copy.deepcopy(activation)
    bad_link["decision_records"][status_id]["artifact"] = "theory/proofs/WRONG.md"
    record(
        "mismatch_artifact_status_decision_linkage",
        validate_candidate(
            frozen,
            activation_manifest=bad_link,
            enforce_research_only_placement=False,
        ),
        "status_decision_field_mismatch:",
    )
    bad_status_hash = copy.deepcopy(activation)
    bad_status_hash["decision_records"][status_id]["record_digest"] = "0" * 64
    record(
        "break_artifact_status_decision_hash_lock",
        validate_candidate(
            frozen,
            activation_manifest=bad_status_hash,
            enforce_research_only_placement=False,
        ),
        "status_decision_hash_mismatch:",
    )

    for field in PROVENANCE_FIELDS:
        omitted = copy.deepcopy(activation)
        record_object = omitted["decision_records"][MANIFEST_DECISION_ID]
        record_object.pop(field)
        record_object["record_digest"] = _record_digest(record_object)
        record(
            f"omit_manifest_decision_{field}",
            validate_candidate(
                frozen,
                activation_manifest=omitted,
                enforce_research_only_placement=False,
            ),
            f"manifest_decision_required_field_missing:{MANIFEST_DECISION_ID}:{field}",
        )

    for field in PROVENANCE_FIELDS:
        omitted = copy.deepcopy(activation)
        record_object = omitted["decision_records"][status_id]
        record_object.pop(field)
        record_object["record_digest"] = _record_digest(record_object)
        record(
            f"omit_artifact_status_decision_{field}",
            validate_candidate(
                frozen,
                activation_manifest=omitted,
                enforce_research_only_placement=False,
            ),
            f"status_decision_required_field_missing:{status_id}:{field}",
        )
    return controls


core.adjudicate_claims = adjudicate_claims
core.synthetic_activation_manifest = synthetic_activation_manifest
core.validate_manifest_entries = validate_manifest_entries
core._original_execute_negative_controls = core.execute_negative_controls
core.validate_candidate = validate_candidate
core.execute_negative_controls = execute_negative_controls


def run_full_validation(*, enforce_research_only_placement: bool = True) -> dict[str, Any]:
    result = core.run_full_validation(
        enforce_research_only_placement=enforce_research_only_placement
    )
    result["schema_version"] = "1.3"
    result["evidence_digest"] = core.canonical_digest(
        {key: value for key, value in result.items() if key != "evidence_digest"}
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--allow-canonical-staging", action="store_true")
    args = parser.parse_args()
    result = run_full_validation(
        enforce_research_only_placement=not args.allow_canonical_staging
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["overall"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
