#!/usr/bin/env python3
"""Validate PBTS-001 RUN-001 records, interpretation, and claim boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "theory/evaluation/pb001-execution-run-001-records.json"
SUMMARY = ROOT / "theory/evaluation/pb001-execution-run-001-summary.json"
REPORT = ROOT / "docs/research/pb001-execution-run-001-report.md"

AXES = {f"P{i}" for i in range(1, 9)}
DOMAINS = {f"D{i}" for i in range(1, 17)}
PAIR_IDS = {f"PA-{i:02d}" for i in range(1, 9)}
COUNTERMODELS = {
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
ADDITION_HYPOTHESES = {
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


def fail(message: str) -> None:
    raise SystemExit(f"PBTS-001 RUN-001 check failed: {message}")


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    records = load_json(RECORDS)
    summary = load_json(SUMMARY)
    if not REPORT.is_file():
        fail("missing execution report")

    if records.get("run_id") != "PBTS-001-RUN-001":
        fail("unexpected run identity")
    if records.get("suite_id") != "PBTS-001" or records.get("basis_id") != "PB-001":
        fail("suite or basis identity drift")
    if records.get("independence_level") != "none_external":
        fail("RUN-001 must not claim external independence")

    frozen = records.get("frozen_inputs", [])
    if len(frozen) < 3:
        fail("frozen input manifest is incomplete")
    for item in frozen:
        path = ROOT / item["path"]
        if not path.is_file():
            fail(f"missing frozen input {item['path']}")
        if git_blob_sha(path) != item["blob_sha"]:
            fail(f"frozen input drift: {item['path']}")

    evaluators = records.get("evaluation_passes", [])
    if {item.get("id") for item in evaluators} != {"EV-A", "EV-B", "EV-C"}:
        fail("expected exactly EV-A, EV-B, and EV-C")

    pairs = records.get("paired_axis_responses", [])
    if {item.get("pair_id") for item in pairs} != PAIR_IDS:
        fail("paired-axis coverage is incomplete")
    if {item.get("target_axis") for item in pairs} != AXES:
        fail("paired-axis targets are incomplete")
    for item in pairs:
        responses = item.get("responses", [])
        if {r.get("evaluator") for r in responses} != {"EV-A", "EV-B", "EV-C"}:
            fail(f"{item['pair_id']} lacks three method responses")
        if not all(r.get("score") in {"pass", "partial", "fail", "unknown"} for r in responses):
            fail(f"{item['pair_id']} has invalid score")

    ablations = records.get("ablation_responses", [])
    if {item.get("axis") for item in ablations} != AXES:
        fail("ablation coverage is incomplete")
    allowed_ablation = {
        "loss_detected",
        "recoverable_with_counted_commitment",
        "hidden_reintroduction",
        "no_observed_loss",
        "unknown",
    }
    for item in ablations:
        responses = item.get("responses", [])
        if {r.get("evaluator") for r in responses} != {"EV-A", "EV-B", "EV-C"}:
            fail(f"{item['axis']} ablation lacks three responses")
        if not all(r.get("outcome") in allowed_ablation for r in responses):
            fail(f"{item['axis']} has invalid ablation outcome")

    coverage = records.get("domain_coverage", [])
    if len(coverage) != 32:
        fail("domain coverage must contain exactly 32 records")
    for domain in DOMAINS:
        cases = [item for item in coverage if item.get("domain") == domain]
        if len(cases) != 2:
            fail(f"{domain} must have exactly two coverage cases")
        roles = {item.get("role") for item in cases}
        if roles != {"ordinary_or_representative", "pressure_or_boundary_adjacent"}:
            fail(f"{domain} role coverage is incomplete")

    countermodels = records.get("countermodel_results", [])
    if {item.get("id") for item in countermodels} != COUNTERMODELS:
        fail("mandatory countermodel coverage is incomplete")

    hidden = records.get("hidden_recovery_rejections", [])
    if len(hidden) != 8 or {item.get("target_axis") for item in hidden} != AXES:
        fail("hidden-recovery audit must include one rejected attempt per axis")
    if any(item.get("disposition") != "rejected" for item in hidden):
        fail("all registered hidden recoveries must remain rejected")

    additions = records.get("addition_search_results", [])
    if {item.get("hypothesis") for item in additions} != ADDITION_HYPOTHESES:
        fail("adversarial addition-search coverage is incomplete")
    if any(item.get("classification") == "candidate_new_axis" for item in additions):
        fail("summary must be revised before claiming no missing general axis")

    rejected = records.get("rejected_records", [])
    if len(rejected) < 4 or not all(item.get("preserved") is True for item in rejected):
        fail("rejected records were not preserved")

    if summary.get("status") != "executed_internal_interpreted":
        fail("summary status is incorrect")
    if summary.get("result_classification") != "scoped_internal_support_with_independence_block":
        fail("result classification exceeds or understates RUN-001")

    paired_summary = summary.get("paired_axis_summary", {})
    if set(paired_summary) != AXES:
        fail("paired-axis summary is incomplete")
    for axis, item in paired_summary.items():
        if item.get("valid_pair") is not True:
            fail(f"{axis} is not registered as internally discriminating")
        if sum(item.get("distribution", {}).values()) != 3:
            fail(f"{axis} distribution does not contain three responses")

    suite_gate = summary.get("suite_advance_gate", {})
    expected_suite_gates = {
        "all_axes_have_valid_pair",
        "all_ablations_resolved_or_explicitly_unknown",
        "D1_D16_coverage_complete",
        "countermodel_coverage_complete",
        "hidden_recovery_audits_complete",
        "no_missing_general_axis",
        "no_required_IRD_or_domain_revision",
        "results_registered",
    }
    if set(suite_gate) != expected_suite_gates or not all(suite_gate.values()):
        fail("substantive suite gate must be complete and internally supported")

    independence_gate = summary.get("execution_requirement_gate", {})
    if independence_gate.get("three_independently_constructed_evaluations") is not False:
        fail("independent construction must remain unsatisfied")
    theorem_gate = summary.get("representation_theorem_gate", {})
    if theorem_gate.get("open") is not False:
        fail("representation-theorem gate must remain closed")

    report_text = REPORT.read_text(encoding="utf-8")
    required_phrases = [
        "scoped internal methodological support",
        "representation-theorem gate remains closed",
        "not independent evaluators",
        "P8 issue",
        "does not establish",
    ]
    for phrase in required_phrases:
        if phrase not in report_text:
            fail(f"report missing required phrase: {phrase}")

    print("PBTS-001 RUN-001 execution check: PASS")


if __name__ == "__main__":
    main()
