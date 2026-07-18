#!/usr/bin/env python3
"""Validate the frozen PBTS-001 independent replication package."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "theory/evaluation/pbts001-independent-replication-registry.json"
SCHEMA_PATH = ROOT / "theory/evaluation/pbts001-independent-replication-response-schema.json"
PROTOCOL_PATH = ROOT / "docs/research/pbts001-independent-replication-package-v1.0.md"
CALIBRATION_PATH = ROOT / "docs/research/pbts001-independent-replication-calibration-v1.0.md"
AUDIT_PATH = ROOT / "docs/audits/pbts001-independent-replication-freeze-audit.md"

EXPECTED_SLOTS = ["REP-A", "REP-B", "REP-C"]
EXPECTED_SECTIONS = {
    "paired_axis_discrimination",
    "axis_ablation",
    "domain_coverage",
    "IRD_countermodel_coverage",
    "hidden_recovery_audit",
    "adversarial_addition_search",
    "P8_classification",
    "deviations_and_disclosures",
}
EXPECTED_P8 = {
    "ordinary_preservation_coordinate",
    "cross_cutting_evidential_qualifier",
    "separate_evidence_contract",
    "axis_revision_required",
    "unresolved",
}
EXPECTED_PAIR_IDS = {f"PA-{index:02d}" for index in range(1, 9)}
EXPECTED_AXES = {f"P{index}" for index in range(1, 9)}
EXPECTED_DOMAINS = {f"D{index}" for index in range(1, 17)}
EXPECTED_COUNTERMODELS = {
    "arbitrary_labeled_transition",
    "output_equivalent_lookup",
    "post_hoc_narrative",
    "hidden_operator",
    "pure_optimizer",
    "trivial_universal_encoding",
    "distributed_reasoning",
    "self_revision",
    "continuous_embodied_control",
    "conflicting_normative_reasons",
}
EXPECTED_ADDITION_HYPOTHESES = {
    "resource_and_computational_bounds",
    "agency_authorship_responsibility",
    "uncertainty_calibration",
    "social_authority_and_institutional_role",
    "spatial_environmental_embedding",
    "representational_granularity",
    "type_creation_and_ontology_change",
    "counterfactual_causal_intervention_structure",
    "privacy_public_private_commitments",
    "termination_liveness_open_endedness",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(errors, f"missing required file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(errors, f"expected JSON object in {path.relative_to(ROOT)}")
        return {}
    return value


def git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def enum_values(schema: dict[str, Any], property_name: str) -> set[str]:
    value = schema.get("properties", {}).get(property_name, {})
    enum = value.get("enum", [])
    return {str(item) for item in enum}


def item_enum(schema: dict[str, Any], array_name: str, property_name: str) -> set[str]:
    array = schema.get("properties", {}).get(array_name, {})
    item = array.get("items", {})
    prop = item.get("properties", {}).get(property_name, {})
    return {str(value) for value in prop.get("enum", [])}


def main() -> int:
    errors: list[str] = []
    registry = load_json(REGISTRY_PATH, errors)
    schema = load_json(SCHEMA_PATH, errors)

    for path in (PROTOCOL_PATH, CALIBRATION_PATH, AUDIT_PATH):
        if not path.exists():
            fail(errors, f"missing required file: {path.relative_to(ROOT)}")

    if registry.get("package_id") != "PBTS-001-REP-001":
        fail(errors, "package_id must remain PBTS-001-REP-001")
    if registry.get("package_version") != "1.0":
        fail(errors, "package_version must remain 1.0")
    if registry.get("status") != "frozen_prospective_not_executed":
        fail(errors, "package status must remain frozen_prospective_not_executed")
    if registry.get("basis_id") != "PB-001" or registry.get("suite_id") != "PBTS-001":
        fail(errors, "package must target PB-001 and PBTS-001")
    if registry.get("candidate_dependencies") != []:
        fail(errors, "replication package must have no candidate dependencies")
    if registry.get("primary_evidence_class") != "replication":
        fail(errors, "primary evidence class must be replication")
    if registry.get("target_replication_layer") != "R3_independent_technical_replication":
        fail(errors, "target layer must be R3 independent technical replication")

    protected = registry.get("protected_inputs", [])
    excluded = registry.get("excluded_prior_result_artifacts", [])
    if len(protected) != 8:
        fail(errors, "exactly eight protected inputs must be registered")
    if len(excluded) != 3:
        fail(errors, "exactly three RUN-001 result artifacts must be excluded")

    protected_paths: set[str] = set()
    for item in protected:
        path_value = item.get("path")
        expected_sha = item.get("git_blob_sha")
        if not isinstance(path_value, str) or not isinstance(expected_sha, str):
            fail(errors, "every protected input requires path and git_blob_sha")
            continue
        protected_paths.add(path_value)
        path = ROOT / path_value
        if not path.exists():
            fail(errors, f"protected input missing: {path_value}")
            continue
        actual_sha = git_blob_sha(path)
        if actual_sha != expected_sha:
            fail(errors, f"protected input hash mismatch for {path_value}: {actual_sha} != {expected_sha}")

    excluded_paths: set[str] = set()
    for item in excluded:
        path_value = item.get("path")
        expected_sha = item.get("git_blob_sha")
        if not isinstance(path_value, str) or not isinstance(expected_sha, str):
            fail(errors, "every excluded artifact requires path and git_blob_sha")
            continue
        excluded_paths.add(path_value)
        path = ROOT / path_value
        if not path.exists():
            fail(errors, f"excluded RUN-001 artifact missing: {path_value}")
            continue
        actual_sha = git_blob_sha(path)
        if actual_sha != expected_sha:
            fail(errors, f"excluded RUN-001 artifact hash mismatch for {path_value}")

    if protected_paths & excluded_paths:
        fail(errors, "RUN-001 result artifacts cannot be protected participant-facing inputs")

    slots = registry.get("replicator_slots", [])
    if [slot.get("id") for slot in slots] != EXPECTED_SLOTS:
        fail(errors, "replicator slots must remain REP-A, REP-B, REP-C in order")
    for slot in slots:
        if slot.get("identity") is not None or slot.get("registration_status") != "unregistered":
            fail(errors, "package freeze cannot contain registered participant identities")

    if registry.get("minimum_primary_submissions") != 3:
        fail(errors, "minimum primary submissions must remain three")
    if registry.get("minimum_distinct_organizational_affiliations") != 2:
        fail(errors, "minimum distinct organizational affiliations must remain two")

    calibration = registry.get("calibration", {})
    if calibration.get("items") != 6 or calibration.get("minimum_correct") != 5:
        fail(errors, "calibration must contain six items with a five-item passing threshold")
    if calibration.get("critical_item") != "CAL-04_observation_vs_inference":
        fail(errors, "CAL-04 observation-versus-inference must remain critical")
    if calibration.get("status") != "not_administered":
        fail(errors, "calibration status must remain not_administered at package freeze")

    if set(registry.get("required_execution_sections", [])) != EXPECTED_SECTIONS:
        fail(errors, "required execution sections changed")
    if set(registry.get("allowed_P8_classifications", [])) != EXPECTED_P8:
        fail(errors, "allowed P8 classifications changed")

    for empty_field in (
        "participant_registrations",
        "calibration_records",
        "submissions",
        "rejections",
        "adjudications",
        "results",
    ):
        if registry.get(empty_field) != []:
            fail(errors, f"{empty_field} must remain empty before execution")
    if registry.get("execution_status") != "not_started":
        fail(errors, "execution_status must remain not_started")

    advance_gate = registry.get("advance_gate", {})
    if not advance_gate or any(value is not False for value in advance_gate.values()):
        fail(errors, "every replication and theorem gate must remain false at package freeze")
    if "representation_theorem_gate_open" not in advance_gate:
        fail(errors, "representation theorem gate must be explicitly registered")

    if schema.get("title") != "PBTS-001 Independent Replication Response":
        fail(errors, "response schema title changed")
    required = set(schema.get("required", []))
    required_top_level = {
        "independence_declaration",
        "tool_disclosure",
        "paired_axis_results",
        "ablation_results",
        "domain_coverage",
        "countermodel_results",
        "hidden_recovery_results",
        "addition_search_results",
        "P8_classification",
        "deviations",
        "nonclaim_acknowledgements",
    }
    if not required_top_level <= required:
        fail(errors, "response schema is missing required execution sections")

    if item_enum(schema, "paired_axis_results", "pair_id") != EXPECTED_PAIR_IDS:
        fail(errors, "response schema pair IDs changed")
    if item_enum(schema, "paired_axis_results", "target_axis") != EXPECTED_AXES:
        fail(errors, "response schema paired-axis targets changed")
    if item_enum(schema, "domain_coverage", "domain_class") != EXPECTED_DOMAINS:
        fail(errors, "response schema domain classes changed")
    if item_enum(schema, "countermodel_results", "countermodel") != EXPECTED_COUNTERMODELS:
        fail(errors, "response schema countermodels changed")
    if item_enum(schema, "addition_search_results", "hypothesis") != EXPECTED_ADDITION_HYPOTHESES:
        fail(errors, "response schema addition-search hypotheses changed")

    p8_schema = schema.get("properties", {}).get("P8_classification", {})
    p8_enum = set(
        p8_schema.get("properties", {}).get("classification", {}).get("enum", [])
    )
    if p8_enum != EXPECTED_P8:
        fail(errors, "response schema P8 classification options changed")

    if PROTOCOL_PATH.exists():
        protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
        required_phrases = [
            "Frozen prospective replication package",
            "public, so technical prevention of all prior access is impossible",
            "Multiple paths created by one person, one assistant context, or one organization count as R2 at most",
            "RUN-001 is not used as the answer key",
            "Package freeze alone satisfies none of these gates",
            "does not establish FARA compliance",
            "Register qualified independent replicators",
        ]
        for phrase in required_phrases:
            if phrase not in protocol:
                fail(errors, f"protocol missing required phrase: {phrase}")

    if CALIBRATION_PATH.exists():
        calibration_text = CALIBRATION_PATH.read_text(encoding="utf-8")
        for item in range(1, 7):
            if f"CAL-{item:02d}" not in calibration_text:
                fail(errors, f"calibration missing CAL-{item:02d}")
        if "Any answer other than C fails the calibration" not in calibration_text:
            fail(errors, "calibration must preserve critical CAL-04 rule")

    if AUDIT_PATH.exists():
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "cannot guarantee technical blinding",
            "not a secure examination",
            "No person is registered",
            "not yet an independent replication study",
        ):
            if phrase not in audit:
                fail(errors, f"freeze audit missing limitation: {phrase}")

    nonclaims = registry.get("nonclaims", [])
    if len(nonclaims) < 6:
        fail(errors, "replication registry must retain all conservative nonclaims")
    prohibited_claims = (
        "PB-001 is sufficient",
        "PB-001 is necessary",
        "PB-001 is minimal",
        "FARA is universal",
        "representation theorem is established",
    )
    joined_nonclaims = "\n".join(nonclaims)
    for claim in prohibited_claims:
        if claim in joined_nonclaims:
            fail(errors, f"registry contains prohibited affirmative claim: {claim}")

    expected_next = (
        "registered qualified replicators and frozen PBTS-001-REP-001-RUN-001 assignments, "
        "calibration records, exposure declarations, and append-only submission channels without replication results"
    )
    if registry.get("next_required_artifact") != expected_next:
        fail(errors, "next_required_artifact changed")

    if errors:
        print("PBTS-001 independent replication package check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PBTS-001 independent replication package check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
