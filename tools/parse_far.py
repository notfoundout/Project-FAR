#!/usr/bin/env python3
"""Parse and strictly validate machine-readable FAR YAML files."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable, Set

import yaml

from far_core import FARObject, InterpretationAssignment, ReasoningSystemMapping, Relation, Representation, Rule, Statement, Transition

TOP_LEVEL_KEYS = {"investigation", "reasoning_system", "representations", "relations", "interpretations", "rules", "transitions"}
RECORD_KEYS = {
    "representation": {"id", "kind", "content", "statement"},
    "relation": {"id", "type", "source", "target"},
    "interpretation": {"representation", "meaning"},
    "rule": {"id", "name", "inputs", "output", "condition"},
    "transition": {"id", "source", "rule", "target", "status", "order"},
}
REASONING_SYSTEM_KEYS = {"system", "far_primitives", "verdict"}
PRIMITIVE_KEYS = {"Investigation", "Representation", "Representational Structure", "Interpretation", "Reasoning Calculus", "investigation", "representation", "structure", "interpretation", "calculus"}


def as_list(data: Dict[str, Any], key: str, *, required: bool = False) -> Iterable[Any]:
    if required and key not in data:
        raise ValueError(f"missing required top-level key: {key}")
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    if required and not value:
        raise ValueError(f"{key} must be nonempty")
    return value


def reject_unknown(mapping: Dict[str, Any], allowed: Set[str], location: str) -> None:
    unknown = set(mapping) - allowed
    if unknown:
        raise ValueError(f"{location} has unknown keys: {sorted(unknown)}")


def require_nonempty(value: Any, location: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{location} must be nonempty")
    return text


def validate_reasoning_system(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        raise ValueError("reasoning_system must be a mapping")
    reject_unknown(value, REASONING_SYSTEM_KEYS, "reasoning_system")
    primitives = value.get("far_primitives")
    if not isinstance(primitives, dict):
        raise ValueError("reasoning_system.far_primitives must be a mapping")
    reject_unknown(primitives, PRIMITIVE_KEYS, "reasoning_system.far_primitives")


def validate_record(item: Any, kind: str) -> Dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError(f"each {kind} must be a mapping")
    reject_unknown(item, RECORD_KEYS[kind], kind)
    return item


def load_far_yaml(path: Path) -> FARObject:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"malformed YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("FAR file must contain a YAML mapping")
    reject_unknown(data, TOP_LEVEL_KEYS, "FAR object")
    investigation = require_nonempty(data.get("investigation", ""), "investigation")
    validate_reasoning_system(data.get("reasoning_system"))
    far = FARObject(investigation=investigation, reasoning_system=ReasoningSystemMapping.from_value(data.get("reasoning_system")))

    for raw in as_list(data, "representations", required=True):
        item = validate_record(raw, "representation")
        rep_id = require_nonempty(item.get("id", ""), "representation id")
        statement = Statement.from_value(item["statement"], f"representation {rep_id}") if "statement" in item else None
        rep = Representation(id=rep_id, kind=require_nonempty(item.get("kind", ""), f"representation {rep_id} kind"), content=str(item.get("content", "")), statement=statement)
        if rep.id in far.representations:
            raise ValueError(f"duplicate representation id: {rep.id}")
        far.representations[rep.id] = rep

    for raw in as_list(data, "relations"):
        item = validate_record(raw, "relation")
        rel = Relation(id=require_nonempty(item.get("id", ""), "relation id"), type=require_nonempty(item.get("type", ""), "relation type"), source=require_nonempty(item.get("source", ""), "relation source"), target=require_nonempty(item.get("target", ""), "relation target"))
        if rel.id in far.relations:
            raise ValueError(f"duplicate relation id: {rel.id}")
        far.relations[rel.id] = rel

    for raw in as_list(data, "interpretations"):
        item = validate_record(raw, "interpretation")
        assignment = InterpretationAssignment(representation=require_nonempty(item.get("representation", ""), "interpretation representation"), meaning=require_nonempty(item.get("meaning", ""), "interpretation meaning"))
        if assignment.representation in far.interpretations:
            raise ValueError(f"duplicate interpretation for representation: {assignment.representation}")
        far.interpretations[assignment.representation] = assignment

    for raw in as_list(data, "rules"):
        item = validate_record(raw, "rule")
        rule_id = require_nonempty(item.get("id", ""), "rule id")
        inputs = item.get("inputs", [])
        if not isinstance(inputs, list):
            raise ValueError(f"rule {rule_id} inputs must be a list")
        rule = Rule(id=rule_id, name=require_nonempty(item.get("name", rule_id), f"rule {rule_id} name"), inputs=[require_nonempty(x, f"rule {rule_id} input") for x in inputs], output=require_nonempty(item.get("output", ""), f"rule {rule_id} output"), condition=str(item.get("condition", "")))
        if rule.id in far.rules:
            raise ValueError(f"duplicate rule id: {rule.id}")
        far.rules[rule.id] = rule

    for raw in as_list(data, "transitions"):
        item = validate_record(raw, "transition")
        transition_id = require_nonempty(item.get("id", ""), "transition id")
        order = item.get("order")
        if isinstance(order, bool) or not isinstance(order, int):
            raise ValueError(f"transition {transition_id} order must be an integer")
        transition = Transition(id=transition_id, source=require_nonempty(item.get("source", ""), f"transition {transition_id} source"), rule=require_nonempty(item.get("rule", ""), f"transition {transition_id} rule"), target=require_nonempty(item.get("target", ""), f"transition {transition_id} target"), status=str(item.get("status", "unresolved")), order=order)
        if transition.id in far.transitions:
            raise ValueError(f"duplicate transition id: {transition.id}")
        far.transitions[transition.id] = transition
    return far


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse and validate a FAR YAML file")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        far = load_far_yaml(args.path)
        errors = far.validate_well_formed()
    except Exception as exc:
        print("FAR PARSE FAILED")
        print(f"- {exc}")
        return 1
    if errors:
        print("FAR PARSE FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("FAR PARSE PASSED")
    print(f"representations: {len(far.representations)}")
    print(f"relations: {len(far.relations)}")
    print(f"rules: {len(far.rules)}")
    print(f"transitions: {len(far.transitions)}")
    if far.reasoning_system:
        print(f"reasoning_system: {far.reasoning_system.system}")
        print(f"verdict: {far.reasoning_system.verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
