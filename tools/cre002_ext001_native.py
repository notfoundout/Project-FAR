#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
from typing import Any

from cre002_ext001_model import canonical

VOCABS = {
    "CRE-001-VOCAB-A-1.0": ("Object", "Relation", "Transformation"),
    "CRE-001-VOCAB-B-1.0": ("State", "Transition", "Label"),
    "CRE-001-VOCAB-C-1.0": ("Representation", "Representational Structure", "Interpretation", "Investigation", "Calculus"),
}
DERIVED = {"D_nondeterminism", "D_concurrency", "D_priority", "D_provenance", "D_rule_modification"}


def build_records(scenario: dict[str, Any], vocab: str) -> list[dict[str, Any]]:
    primitives = VOCABS[vocab]
    records: list[dict[str, Any]] = []

    def add(role: str, primitive: str, data: dict[str, Any]) -> None:
        if primitive not in primitives:
            raise ValueError(f"{vocab}: invalid primitive {primitive}")
        records.append({
            "record_id": f"{vocab}:{len(records):04d}",
            "primitive": primitive,
            "semantic_role": role,
            "data": data,
        })

    if vocab.endswith("A-1.0"):
        value_primitive, relation_primitive, transition_primitive = "Object", "Relation", "Transformation"
    elif vocab.endswith("B-1.0"):
        value_primitive, relation_primitive, transition_primitive = "State", "Label", "Transition"
    else:
        value_primitive, relation_primitive, transition_primitive = "Representation", "Representational Structure", "Calculus"
        add("investigation_scope", "Investigation", {"scenario_id": scenario["scenario_id"], "bounded": True})
        add("semantic_interpretation", "Interpretation", {"authority": scenario["semantic_authority"]})

    initial = scenario["initial_state"]
    for name, value in sorted(initial["booleans"].items()):
        add("initial_boolean", value_primitive, {"name": name, "value": value})
    for rule in initial["active_rules"]:
        add("initial_rule", value_primitive, {"rule": rule, "status": "active"})
    add("initial_priorities", relation_primitive, {"priorities": copy.deepcopy(initial["priorities"])})
    add("initial_histories", relation_primitive, {"evidence": [], "actions": []})
    add("initial_modification_count", relation_primitive, {"value": initial["modification_count"]})
    for transition in scenario["transitions"]:
        add("transition_schema", transition_primitive, copy.deepcopy(transition))
    add("interleaving", relation_primitive, copy.deepcopy(scenario["interleaving"]))
    for invariant in scenario["invariants"]:
        add("invariant", relation_primitive, {"text": invariant})
    add("outputs", relation_primitive, {"fields": copy.deepcopy(scenario["outputs"])})
    add("bounds", relation_primitive, copy.deepcopy(scenario["bounds"]))
    return records


def lower_records(records: list[dict[str, Any]], vocab: str, scenario_id: str, authority: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    allowed = set(VOCABS[vocab])
    if any(r["primitive"] not in allowed for r in records):
        raise ValueError("native primitive mismatch")
    booleans = {r["data"]["name"]: r["data"]["value"] for r in records if r["semantic_role"] == "initial_boolean"}
    active_rules = [r["data"]["rule"] for r in records if r["semantic_role"] == "initial_rule"]
    priorities = next(r["data"]["priorities"] for r in records if r["semantic_role"] == "initial_priorities")
    modification_count = next(r["data"]["value"] for r in records if r["semantic_role"] == "initial_modification_count")
    transitions = [copy.deepcopy(r["data"]) for r in records if r["semantic_role"] == "transition_schema"]
    interleaving = next(copy.deepcopy(r["data"]) for r in records if r["semantic_role"] == "interleaving")
    invariants = [r["data"]["text"] for r in records if r["semantic_role"] == "invariant"]
    outputs = next(copy.deepcopy(r["data"]["fields"]) for r in records if r["semantic_role"] == "outputs")
    bounds = next(copy.deepcopy(r["data"]) for r in records if r["semantic_role"] == "bounds")
    model = {
        "scenario_id": scenario_id,
        "semantic_authority": authority,
        "bounds": bounds,
        "initial_state": {
            "booleans": booleans,
            "evidence_log": [],
            "action_history": [],
            "active_rules": active_rules,
            "priorities": priorities,
            "modification_count": modification_count,
        },
        "transitions": transitions,
        "interleaving": interleaving,
        "invariants": invariants,
        "outputs": outputs,
    }
    trace = [{
        "record_id": r["record_id"],
        "primitive": r["primitive"],
        "semantic_role": r["semantic_role"],
        "data_digest": hashlib.sha256(canonical(r["data"]).encode()).hexdigest(),
    } for r in records]
    return model, trace


def licensing_audit(baseline: dict[str, Any], vocab: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    license_record = baseline["vocabulary_licensing"][vocab]
    constructs = {x["identifier"]: x for x in baseline["derived_constructs"]}
    licensed = set(license_record["licensed_derived_constructs"])
    missing = sorted(DERIVED - licensed)
    malformed = sorted(name for name in DERIVED if not constructs[name].get("required_fields") or not constructs[name].get("operational_constraints"))
    primitive_mismatch = sorted({r["primitive"] for r in records} - set(license_record["primitive_basis"]))
    status = "pass" if not (missing or malformed or primitive_mismatch) else "fail"
    return {
        "status": status,
        "licensed_constructs": sorted(licensed),
        "missing_constructs": missing,
        "malformed_constructs": malformed,
        "primitive_mismatch": primitive_mismatch,
        "construction_rule": license_record["construction_rule"],
        "limitation": license_record["limitation"],
    }
