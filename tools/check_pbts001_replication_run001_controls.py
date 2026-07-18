#!/usr/bin/env python3
"""Validate frozen coordinator controls for PBTS-001-REP-001-RUN-001."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "PBTS-001-REP-001-RUN-001"
RUN_REGISTRY = ROOT / "theory/evaluation/pbts001-independent-replication-run-001-registry.json"
PACKAGE_REGISTRY = ROOT / "theory/evaluation/pbts001-independent-replication-registry.json"
CONTROLS = ROOT / "docs/research/pbts001-replication-run-001-coordinator-controls.md"

CHANNELS = {
    "registrations": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/registrations.json",
    "exposure_declarations": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/exposure-declarations.json",
    "calibrations": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/calibrations.json",
    "independence_audits": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/independence-audits.json",
    "assignments": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/assignments.json",
    "submissions": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/submissions.json",
    "rejections_withdrawals": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/rejections-withdrawals.json",
    "adjudications": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/adjudications.json",
    "results": ROOT / "theory/evaluation/pbts001-independent-replication/run-001/results.json",
}

EXPECTED_SLOTS = ["REP-A", "REP-B", "REP-C"]
EXPECTED_SECTIONS = [
    "PAIR",
    "ABLATION",
    "DOMAIN",
    "COUNTERMODEL",
    "HIDDEN_RECOVERY",
    "ADDITION_SEARCH",
    "P8",
    "DISCLOSURES",
]


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def require_false(mapping: dict, keys: list[str], context: str) -> None:
    for key in keys:
        if mapping.get(key) is not False:
            raise AssertionError(f"{context}.{key} must remain false before real execution")


def main() -> int:
    package = load_json(PACKAGE_REGISTRY)
    run = load_json(RUN_REGISTRY)

    assert package.get("package_id") == "PBTS-001-REP-001"
    assert package.get("status") == "frozen_prospective_not_executed"
    assert package.get("participant_registrations") == []
    assert package.get("submissions") == []
    assert package.get("results") == []
    assert package.get("advance_gate", {}).get("representation_theorem_gate_open") is False

    assert run.get("run_id") == RUN_ID
    assert run.get("package_id") == "PBTS-001-REP-001"
    assert run.get("package_version") == "1.0"
    assert run.get("status") == "coordinator_controls_frozen_no_participants"
    assert run.get("target_replication_layer") == "R3_independent_technical_replication"
    assert run.get("public_repository_blinding_guaranteed") is False
    assert run.get("minimum_primary_registrants") == 3
    assert run.get("minimum_distinct_organizational_affiliations") == 2

    slots = run.get("primary_slots")
    assert isinstance(slots, list) and [slot.get("slot_id") for slot in slots] == EXPECTED_SLOTS
    for slot in slots:
        assert slot.get("registration_id") is None
        assert slot.get("qualification_status") == "unregistered"
        assert slot.get("calibration_status") == "not_administered"
        assert slot.get("exposure_declaration_status") == "missing"
        assert slot.get("independence_audit_status") == "not_started"
        assert slot.get("maximum_justified_layer") == "unresolved"
        assert slot.get("assignment_status") == "not_generated"
        assert slot.get("submission_status") == "not_started"

    calibration = run.get("calibration_rule", {})
    assert calibration.get("items") == 6
    assert calibration.get("minimum_correct") == 5
    assert calibration.get("critical_item") == "CAL-04_observation_vs_inference"
    assert calibration.get("maximum_retests") == 1
    assert calibration.get("self_scoring_prohibited") is True

    assignment = run.get("assignment_plan", {})
    assert assignment.get("all_slots_receive_full_suite") is True
    assert assignment.get("canonical_sections") == EXPECTED_SECTIONS
    assert assignment.get("algorithm") == "deterministic_fisher_yates_sha256_counter_mode"
    assert assignment.get("seed_template") == "PBTS-001-REP-001-RUN-001|{slot_id}|order-v1"
    assert assignment.get("generated_assignments") == []

    policy = run.get("channel_policy", {})
    for key in [
        "append_only",
        "deletion_prohibited",
        "silent_replacement_prohibited",
        "supersession_requires_new_record",
        "stable_record_ids_required",
        "content_digests_required",
    ]:
        assert policy.get(key) is True, f"channel_policy.{key} must be true"

    for field in [
        "registrations",
        "calibration_records",
        "exposure_declarations",
        "independence_audits",
        "assignments",
        "submissions",
        "rejections",
        "adjudications",
        "results",
    ]:
        assert run.get(field) == [], f"run registry field {field} must remain empty"

    execution_gate = run.get("execution_gate", {})
    assert execution_gate.get("append_only_channels_operational") is True
    require_false(
        execution_gate,
        [
            "three_real_registrants_recorded",
            "all_calibrations_passed",
            "all_exposure_declarations_recorded",
            "all_independence_audits_complete",
            "all_assignments_generated",
            "participant_bundles_verified",
            "execution_authorized",
        ],
        "execution_gate",
    )

    require_false(
        run.get("result_gate", {}),
        [
            "three_primary_submissions_frozen_or_permanently_unavailable",
            "adjudication_complete",
            "full_distributions_registered",
            "unfavorable_and_unresolved_results_published",
            "P8_role_resolved_or_alternatives_registered",
            "maximum_replication_layer_recorded",
            "representation_theorem_gate_open",
        ],
        "result_gate",
    )

    registered_paths = run.get("channels", {})
    assert set(registered_paths) == set(CHANNELS)
    for channel_name, path in CHANNELS.items():
        expected = str(path.relative_to(ROOT))
        assert registered_paths.get(channel_name) == expected
        payload = load_json(path)
        assert payload.get("schema_version") == "1.0"
        assert payload.get("run_id") == RUN_ID
        assert payload.get("channel") == channel_name
        assert payload.get("append_only") is True
        assert payload.get("records") == [], f"{channel_name} must contain no records at freeze"

    assignments = load_json(CHANNELS["assignments"])
    assert assignments.get("algorithm") == "deterministic_fisher_yates_sha256_counter_mode"
    assert assignments.get("seed_template") == "PBTS-001-REP-001-RUN-001|{slot_id}|order-v1"

    submissions = load_json(CHANNELS["submissions"])
    assert submissions.get("mutual_embargo") is True

    results = load_json(CHANNELS["results"])
    assert results.get("aggregation_locked") is True

    text = CONTROLS.read_text(encoding="utf-8")
    required_phrases = [
        "No replicator is registered",
        "No placeholder, simulated identity, assistant persona",
        "public",
        "append-only",
        "representation-theorem gate remains closed",
        "recruit and register qualified real replicators",
        "cannot manufacture genuine human, organizational, or conceptual independence",
    ]
    for phrase in required_phrases:
        assert phrase in text, f"controls document missing required phrase: {phrase}"

    prohibited_claims = [
        "independent replication is established",
        "PB-001 is sufficient",
        "FARA is universal",
        "representation theorem is proved",
    ]
    lowered = text.lower()
    for claim in prohibited_claims:
        assert claim.lower() not in lowered, f"unsupported claim present: {claim}"

    print("PBTS-001-REP-001-RUN-001 coordinator controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
