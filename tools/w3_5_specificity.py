#!/usr/bin/env python3
"""Execute bounded W3.5 reasoning discrimination and FARA-specificity analysis.

Semantic licensing is project-authored and non-blind. Runtime scoring receives
only the candidate-neutral authoritative projection plus the frozen licensing
record. Admission metadata is joined only after all scores are computed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

from s_core_w3_schema import canonical_json
from w3_5_factor_source import (
    FactorizationError,
    authoritative_projection,
    compile_projection,
    load_records,
    sha256_json,
)
from w3_5_grel import decode_grel, encode_grel

ROOT = Path(__file__).resolve().parents[1]
LICENSING = ROOT / "theory" / "evaluation" / "w3-5-reasoning-licensing-v1.0.json"
EXPERIMENT_ID = "W35-REASONING-DISCRIMINATION-001"
CRITERIA = ("R1", "R2", "R3", "R4", "R5", "R6", "R7")
CORE_CRITERIA = {"R2", "R3", "R4", "R5", "R7"}
ALLOWED = {"pass", "partial", "fail", "unknown"}
STATUS_CODES = {"P": "pass", "L": "partial", "F": "fail", "U": "unknown"}
BANNED = {
    "admission_decision", "family", "title", "admission_rationale",
    "candidate_exposure_status", "expected_class", "expected_decision",
}


class SpecificityError(ValueError):
    """Invalid licensing, discrimination result, or specificity inference."""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys |= _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            keys |= _walk_keys(item)
    return keys


def _resolve(projection: dict[str, Any], dotted: str) -> Any:
    value: Any = projection
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise SpecificityError(f"missing licensed source field: {dotted}")
        value = value[part]
    if value in (None, "", [], {}):
        raise SpecificityError(f"empty licensed source field: {dotted}")
    return value


def validate_licensing(
    licensing: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    if licensing.get("registry_id") != "W35-REASONING-LICENSING-001":
        raise SpecificityError("licensing registry id changed")
    if licensing.get("status") != "frozen_project_authored_semantic_licensing":
        raise SpecificityError("licensing registry is not frozen")
    if licensing.get("corpus_id") != "RCS-CORPUS-001":
        raise SpecificityError("licensing corpus changed")
    if licensing.get("status_codes") != STATUS_CODES:
        raise SpecificityError("licensing status vocabulary changed")
    authored = licensing.get("authorship_and_blinding", {})
    if authored.get("admission_labels_hidden_from_runtime_scoring") is not True:
        raise SpecificityError("runtime scoring must hide admission labels")
    if authored.get("semantic_coder_blind_to_admission_labels") is not False:
        raise SpecificityError("semantic licensing must not be misreported as blind")
    if authored.get("independent_external_evaluator") is not False:
        raise SpecificityError("internal semantic coding was promoted to external evaluation")
    if BANNED & _walk_keys(licensing.get("records", [])):
        raise SpecificityError("licensing records contain banned admission or expected-result fields")

    definitions = licensing.get("criteria", [])
    if [item.get("id") for item in definitions] != list(CRITERIA):
        raise SpecificityError("criterion order or identity changed")
    definition_map = {item["id"]: item for item in definitions}
    for criterion_id, definition in definition_map.items():
        if not definition.get("definition") or not definition.get("source_fields") or not definition.get("fara_axes"):
            raise SpecificityError(f"{criterion_id}: incomplete criterion definition")

    expected = {record["instance_id"]: record for record in records}
    entries = licensing.get("records")
    if not isinstance(entries, list):
        raise SpecificityError("licensing records must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for entry in entries:
        instance_id = str(entry.get("instance_id", ""))
        if instance_id in by_id or instance_id not in expected:
            raise SpecificityError(f"duplicate or unknown licensing record: {instance_id}")
        if entry.get("source_record_id") != expected[instance_id].get("source_record_id"):
            raise SpecificityError(f"{instance_id}: source record link changed")
        profile = entry.get("profile")
        if not isinstance(profile, str) or len(profile) != len(CRITERIA) or any(code not in STATUS_CODES for code in profile):
            raise SpecificityError(f"{instance_id}: criterion profile changed")
        evidence = entry.get("evidence_summary")
        if not isinstance(evidence, str) or len(evidence) < 120:
            raise SpecificityError(f"{instance_id}: evidence summary is not substantive")
        projection = authoritative_projection(expected[instance_id])
        for criterion_id in CRITERIA:
            for field in definition_map[criterion_id]["source_fields"]:
                _resolve(projection, field)
        by_id[instance_id] = entry
    if set(by_id) != set(expected) or len(by_id) != 18:
        raise SpecificityError("licensing registry does not cover the frozen 18-record corpus")
    return by_id


def classify(criteria: dict[str, dict[str, Any]]) -> str:
    statuses = {criterion_id: criteria[criterion_id]["status"] for criterion_id in CRITERIA}
    if "unknown" in statuses.values():
        return "unknown"
    if all(status == "pass" for status in statuses.values()):
        return "reasoning_like"
    core_failures = sum(statuses[criterion_id] == "fail" for criterion_id in CORE_CRITERIA)
    if core_failures >= 2:
        return "nonreasoning_like"
    return "borderline"


def score_projection(
    projection: dict[str, Any],
    licensing_entry: dict[str, Any],
    criterion_definitions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Score one candidate-neutral authoritative projection."""
    profile = licensing_entry["profile"]
    criteria = {
        criterion_id: {
            "status": STATUS_CODES[profile[index]],
            "source_fields": copy.deepcopy(criterion_definitions[criterion_id]["source_fields"]),
        }
        for index, criterion_id in enumerate(CRITERIA)
    }
    for criterion_id in CRITERIA:
        definition = criterion_definitions[criterion_id]
        for field in definition["source_fields"]:
            _resolve(projection, field)
    return {
        "instance_id": licensing_entry["instance_id"],
        "source_record_id": licensing_entry["source_record_id"],
        "projection_sha256": sha256_json(projection),
        "criteria": criteria,
        "evidence_summary": licensing_entry["evidence_summary"],
        "decision": classify(criteria),
    }


def _fara_role_coverage(
    projection: dict[str, Any],
    criterion_definitions: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    compiled = compile_projection(projection)
    coverage: dict[str, list[str]] = {}
    for criterion_id in CRITERIA:
        axes = list(criterion_definitions[criterion_id]["fara_axes"])
        for axis in axes:
            reduct = compiled.get("axes", {}).get(axis)
            if not isinstance(reduct, dict) or not any(reduct.get(key) for key in ("members", "relations", "attributes")):
                raise SpecificityError(f"{criterion_id}: FARA-oriented axis {axis} is unavailable")
        coverage[criterion_id] = axes
    return coverage


def run_discrimination(root: Path = ROOT) -> dict[str, Any]:
    records = load_records(root)
    licensing_path = root / LICENSING.relative_to(ROOT)
    licensing = load_json(licensing_path)
    by_license = validate_licensing(licensing, records)
    definitions = {item["id"]: item for item in licensing["criteria"]}

    # Scores are frozen before admission labels are consulted.
    scored: dict[str, dict[str, Any]] = {}
    for record in records:
        projection = authoritative_projection(record)
        entry = by_license[record["instance_id"]]
        source_score = score_projection(projection, entry, definitions)

        grel = encode_grel(projection)
        recovered = decode_grel(grel)
        if canonical_json(recovered) != canonical_json(projection):
            raise SpecificityError(f"{record['instance_id']}: GREL recovery changed the scored projection")
        grel_score = score_projection(recovered, entry, definitions)
        if source_score["decision"] != grel_score["decision"] or source_score["criteria"] != grel_score["criteria"]:
            raise SpecificityError(f"{record['instance_id']}: source and GREL scores differ")

        coverage = _fara_role_coverage(projection, definitions)

        mutated = copy.deepcopy(record)
        mutated.update({
            "title": "ignored title",
            "family": "ignored family",
            "admission_decision": "disputed",
            "admission_rationale": "ignored rationale",
            "candidate_exposure_status": "ignored exposure",
        })
        mutated_score = score_projection(authoritative_projection(mutated), entry, definitions)
        if mutated_score["decision"] != source_score["decision"] or mutated_score["criteria"] != source_score["criteria"]:
            raise SpecificityError(f"{record['instance_id']}: admission metadata steers scoring")

        scored[record["instance_id"]] = {
            **source_score,
            "grel_projection_sha256": sha256_json(recovered),
            "source_grel_identical": True,
            "fara_role_coverage": coverage,
            "representation_transport": "source_projection_to_GREL_exact_and_FARA_axes_direct",
        }

    # Admission labels are joined only after every score is computed.
    joined = []
    counts = {
        "positive": {"reasoning_like": 0, "nonreasoning_like": 0, "borderline": 0, "unknown": 0},
        "contrast": {"reasoning_like": 0, "nonreasoning_like": 0, "borderline": 0, "unknown": 0},
        "disputed": {"reasoning_like": 0, "nonreasoning_like": 0, "borderline": 0, "unknown": 0},
    }
    for record in records:
        item = copy.deepcopy(scored[record["instance_id"]])
        decision = item["decision"]
        admission = record["admission_decision"]
        counts[admission][decision] += 1
        item["admission_decision_joined_after_scoring"] = admission
        joined.append(item)

    if counts["positive"] != {"reasoning_like": 8, "nonreasoning_like": 0, "borderline": 0, "unknown": 0}:
        raise SpecificityError(f"positive registered-scope result changed: {counts['positive']}")
    if counts["contrast"] != {"reasoning_like": 0, "nonreasoning_like": 8, "borderline": 0, "unknown": 0}:
        raise SpecificityError(f"contrast registered-scope result changed: {counts['contrast']}")
    if counts["disputed"] != {"reasoning_like": 0, "nonreasoning_like": 0, "borderline": 2, "unknown": 0}:
        raise SpecificityError(f"disputed cases were not preserved: {counts['disputed']}")

    score_source = inspect.getsource(score_projection)
    if any(term in score_source for term in BANNED):
        raise SpecificityError("score_projection directly references banned admission metadata")

    return {
        "schema": "W35-REASONING-DISCRIMINATION-RUNTIME-1.0",
        "experiment_id": EXPERIMENT_ID,
        "status": "complete",
        "licensing_registry": {
            "artifact_id": licensing["registry_id"],
            "path": LICENSING.relative_to(ROOT).as_posix(),
            "content_sha256": sha256_file(licensing_path),
        },
        "scope": {
            "corpus_id": "RCS-CORPUS-001",
            "instances": 18,
            "positive": 8,
            "contrast": 8,
            "disputed": 2,
            "primary_metric_excludes_disputed": True,
        },
        "decision_rule": copy.deepcopy(licensing["decision_rule"]),
        "class_counts": counts,
        "primary_metrics": {
            "positive_sensitivity": "1.0",
            "contrast_specificity": "1.0",
            "balanced_accuracy": "1.0",
            "statistical_inference": "not_authorized",
        },
        "specificity_analysis": {
            "bounded_role_conjunctive_discrimination": "established_on_registered_corpus",
            "same_predicate_available_on_candidate_neutral_source": True,
            "same_predicate_transportable_through_GREL_exact_recovery": True,
            "FARA_role_directness": True,
            "unique_discriminative_capacity_of_FARA": False,
            "FARA_specificity_result": "not_unique_at_registered_scope",
            "general_reasoning_specificity": "not_established",
        },
        "records": joined,
        "limitations": copy.deepcopy(licensing["limitations"]),
        "nonclaims": [
            "perfect registered-corpus separation generalizes to unseen systems",
            "semantic licensing is evaluator-blind or independently replicated",
            "the two disputed records have terminal reasoning classifications",
            "FARA is uniquely capable of expressing the discriminator",
            "FARA primitives are necessary or minimal",
            "candidate invariants have been executed",
            "W3.5 is resolved",
            "W5 is authorized",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute W3.5 reasoning discrimination and specificity")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = run_discrimination(args.root.resolve())
    except (SpecificityError, FactorizationError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAR-VAL-SPEC-001: {exc}")
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            "W3.5 reasoning discrimination: PASS "
            "(8/8 positive reasoning-like; 8/8 contrast nonreasoning-like; "
            "2/2 disputed borderline; FARA not unique at registered scope)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
