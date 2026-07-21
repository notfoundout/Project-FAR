#!/usr/bin/env python3
"""Validate the frozen W3.5 GREL-FARA factorization package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from w3_5_factorization import FactorizationError, run_factorization

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "theory/evaluation/w3-5-factorization-result-v1.0.json"
WITNESSES = ROOT / "theory/evaluation/w3-5-factorization-witnesses-v1.0.json"
BASELINE = ROOT / "theory/evaluation/generic-relational-baseline-v1.0.json"
W35 = ROOT / "theory/evaluation/w3-5-specificity-and-discovery-gate.json"
GATES = ROOT / "theory/evaluation/research-gates.json"
TARGET = ROOT / "theory/evaluation/thm-target-001.json"
EXPECTED_DIMENSIONS = {
    "expressiveness": "equivalent",
    "translation": "bidirectional",
    "constraint_strength": "fara_stricter",
    "reasoning_specificity": "not_established",
    "cost_relation": "tradeoff",
    "overall_interpretation": "fara_constrained_equivalent",
}


class ValidationError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> dict[str, Any]:
    paths = {name: root / path.relative_to(ROOT) for name, path in {
        "result": RESULT, "witnesses": WITNESSES, "baseline": BASELINE,
        "w35": W35, "gates": GATES, "target": TARGET,
    }.items()}
    for path in paths.values():
        if not path.is_file():
            raise ValidationError(f"missing factorization dependency: {path.relative_to(root)}")
    result, witnesses, baseline = load(paths["result"]), load(paths["witnesses"]), load(paths["baseline"])
    w35, gates, target = load(paths["w35"]), load(paths["gates"]), load(paths["target"])

    if result.get("artifact_id") != "W35-FACTOR-RESULT-001" or result.get("status") != "complete":
        raise ValidationError("factorization result artifact is not complete")
    if result.get("dimensions") != EXPECTED_DIMENSIONS or result.get("scope", {}).get("instance_count") != 18:
        raise ValidationError("factorization dimensions or scope changed")
    contract = result.get("factorization_contract", {})
    if contract.get("primitive_reduction_established") is not False:
        raise ValidationError("operational factorization was promoted to a primitive reduction")
    required_reintroduced = {"fixed FARA-oriented compile_projection source adapter", "accepted SCORE-W3 construct_witness implementation"}
    if not required_reintroduced <= set(contract.get("reintroduced_machinery", [])):
        raise ValidationError("reintroduced FARA adapter/constructor machinery is not fully declared")
    if result.get("gate_effect", {}).get("w5_authorized") is not False:
        raise ValidationError("factorization result prematurely authorizes W5")

    registry = result.get("witness_registry", {})
    if registry.get("path") != WITNESSES.relative_to(ROOT).as_posix() or registry.get("artifact_id") != "W35-GREL-FARA-FACTOR-WITNESSES-001":
        raise ValidationError("factorization witness identity changed")
    if registry.get("content_sha256") != sha256_file(paths["witnesses"]):
        raise ValidationError("factorization witness digest mismatch")
    records = witnesses.get("records")
    if witnesses.get("status") != "frozen_expected_runtime_witnesses" or not isinstance(records, list):
        raise ValidationError("factorization witness registry is malformed")
    ids = [item.get("instance_id") for item in records]
    if len(ids) != 18 or len(set(ids)) != 18 or witnesses.get("class_counts") != {"positive": 8, "contrast": 8, "disputed": 2}:
        raise ValidationError("factorization witness registry scope changed")
    required_checks = {"candidate_neutral_compiler", "grel_exact_authoritative_source_recovery", "fixed_adapter_stability", "direct_equals_via_grel_fara", "fara_target_only_recovery", "fara_exact_generic_translation", "no_case_database", "no_hidden_interpreter"}
    for item in records:
        if item.get("status") != "pass_required" or set(item.get("required_checks", [])) != required_checks:
            raise ValidationError(f"{item.get('instance_id')}: runtime obligations changed")

    if baseline.get("baseline_id") != "GREL-001" or baseline.get("current_result") != EXPECTED_DIMENSIONS:
        raise ValidationError("GREL-001 result does not match factorization")
    baseline_result = baseline.get("factorization_result", {})
    if baseline_result.get("artifact_id") != "W35-FACTOR-RESULT-001" or baseline_result.get("content_sha256") != sha256_file(paths["result"]):
        raise ValidationError("GREL-001 factorization result link is invalid")

    artifacts = {item["id"]: item for item in w35.get("required_result_artifacts", [])}
    factor = artifacts.get("W35-FACTOR-RESULT")
    if not factor or factor.get("status") != "complete" or factor.get("path") != RESULT.relative_to(ROOT).as_posix() or factor.get("artifact_id") != "W35-FACTOR-RESULT-001" or factor.get("content_sha256") != sha256_file(paths["result"]):
        raise ValidationError("W35-FACTOR-RESULT linkage is invalid")
    current = w35.get("current_results", {})
    if current.get("factorization") != EXPECTED_DIMENSIONS or w35.get("status") not in {"in_progress_factorization_complete", "in_progress_specificity_complete"} or w35.get("w5_authorized") is not False:
        raise ValidationError("W3.5 factorization state is inconsistent")
    for artifact_id in ("W35-CANDIDATE-RESULT", "W35-COST-RESULT", "W35-CLAIM-RESULT", "W35-FAILURE-RESULT"):
        if artifacts.get(artifact_id, {}).get("status") != "missing":
            raise ValidationError(f"{artifact_id} was promoted before its own execution")

    gate_map = {item["name"]: item for item in gates.get("gates", [])}
    baseline_gate = gate_map.get("baseline-factorization-resolved")
    expected_evidence = {"docs/research/w3-5-grel-fara-factorization-v1.0.md", "docs/audits/w3-5-factorization-audit.md", RESULT.relative_to(ROOT).as_posix(), WITNESSES.relative_to(ROOT).as_posix()}
    if not baseline_gate or baseline_gate.get("status") != "satisfied" or not expected_evidence <= set(baseline_gate.get("evidence", [])):
        raise ValidationError("baseline factorization gate lacks immutable evidence")
    if w35.get("status") == "in_progress_factorization_complete":
        for name in ("fara-specificity-resolved", "reasoning-contrast-execution"):
            if gate_map.get(name, {}).get("status") != "not_satisfied":
                raise ValidationError(f"{name} was promoted without a later-stage result")
    else:
        for name in ("fara-specificity-resolved", "reasoning-contrast-execution"):
            if gate_map.get(name, {}).get("status") != "satisfied" or not gate_map.get(name, {}).get("evidence"):
                raise ValidationError(f"{name} lacks later-stage evidence")
    authorization = target.get("w5_authorization", {})
    if authorization.get("authorized") is not False or authorization.get("blocked_by") != ["W3.5-SDG-001"]:
        raise ValidationError("THM-TARGET-001 no longer blocks W5")
    return {"result": result, "witnesses": witnesses, "baseline": baseline, "w35": w35, "gates": gates, "target": target}


def validate_runtime(root: Path, witnesses: dict[str, Any]) -> dict[str, Any]:
    report = run_factorization(root)
    if report.get("dimensions") != EXPECTED_DIMENSIONS:
        raise ValidationError("runtime factorization dimensions changed")
    runtime = {item["instance_id"]: item for item in report.get("records", [])}
    expected = {item["instance_id"]: item for item in witnesses.get("records", [])}
    if set(runtime) != set(expected):
        raise ValidationError("runtime factorization instance set differs from frozen registry")
    for instance_id, item in runtime.items():
        if item.get("status") != "pass" or any(value != "pass" for value in item.get("checks", {}).values()):
            raise ValidationError(f"{instance_id}: runtime factorization failed")
        grel, fara = item.get("cost", {}).get("grel", {}), item.get("cost", {}).get("fara", {})
        if grel.get("schema_components") != 10 or fara.get("architecture_fields") != 14 or fara.get("witness_fields") != 5:
            raise ValidationError(f"{instance_id}: architecture surface changed")
        if grel.get("semantic_axis_access_operations", 0) <= fara.get("semantic_axis_access_operations", 0):
            raise ValidationError(f"{instance_id}: declared FARA semantic-access advantage disappeared")
    return report


def validate(root: Path = ROOT) -> dict[str, Any]:
    static = validate_static(root)
    runtime = validate_runtime(root, static["witnesses"])
    return {"status": "pass", "artifact_id": static["result"]["artifact_id"], "runtime_experiment_id": runtime["experiment_id"], "instance_count": runtime["scope"]["instances"], "dimensions": runtime["dimensions"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate W3.5 GREL-FARA factorization")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = validate(args.root.resolve())
    except (ValidationError, FactorizationError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAR-VAL-FACTOR-001: {exc}")
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"W3.5 factorization validation: PASS ({report['instance_count']} instances; {report['dimensions']['overall_interpretation']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
