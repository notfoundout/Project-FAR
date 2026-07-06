#!/usr/bin/env python3
"""Parse machine-readable FAR YAML files into FARObject structures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable

import yaml

from far_core import (
    FARObject,
    InterpretationAssignment,
    ReasoningSystemMapping,
    Relation,
    Representation,
    Rule,
    Statement,
    Transition,
)


def as_list(data: Dict[str, Any], key: str) -> Iterable[Any]:
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    return value


def load_far_yaml(path: Path) -> FARObject:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"malformed YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("FAR file must contain a YAML mapping")

    far = FARObject(
        investigation=str(data.get("investigation", "")),
        reasoning_system=ReasoningSystemMapping.from_value(data.get("reasoning_system")),
    )

    for item in as_list(data, "representations"):
        if not isinstance(item, dict):
            raise ValueError("each representation must be a mapping")
        rep_id = str(item.get("id", ""))
        if not rep_id:
            raise ValueError("representation id must be nonempty")
        statement = Statement.from_value(item["statement"], f"representation {rep_id}") if "statement" in item else None
        rep = Representation(
            id=rep_id,
            kind=str(item.get("kind", "claim")),
            content=str(item.get("content", "")),
            statement=statement,
        )
        if rep.id in far.representations:
            raise ValueError(f"duplicate representation id: {rep.id}")
        far.representations[rep.id] = rep

    for item in as_list(data, "relations"):
        if not isinstance(item, dict):
            raise ValueError("each relation must be a mapping")
        rel = Relation(
            id=str(item.get("id", "")),
            type=str(item.get("type", "")),
            source=str(item.get("source", "")),
            target=str(item.get("target", "")),
        )
        if not rel.id:
            raise ValueError("relation id must be nonempty")
        if rel.id in far.relations:
            raise ValueError(f"duplicate relation id: {rel.id}")
        far.relations[rel.id] = rel

    for item in as_list(data, "interpretations"):
        if not isinstance(item, dict):
            raise ValueError("each interpretation must be a mapping")
        assignment = InterpretationAssignment(
            representation=str(item.get("representation", "")),
            meaning=str(item.get("meaning", "")),
        )
        far.interpretations[assignment.representation] = assignment

    for item in as_list(data, "rules"):
        if not isinstance(item, dict):
            raise ValueError("each rule must be a mapping")
        inputs = item.get("inputs", [])
        if not isinstance(inputs, list):
            raise ValueError(f"rule {item.get('id', '')} inputs must be a list")
        rule = Rule(
            id=str(item.get("id", "")),
            name=str(item.get("name", item.get("id", ""))),
            inputs=[str(x) for x in inputs],
            output=str(item.get("output", "")),
            condition=str(item.get("condition", "")),
        )
        if not rule.id:
            raise ValueError("rule id must be nonempty")
        if rule.id in far.rules:
            raise ValueError(f"duplicate rule id: {rule.id}")
        far.rules[rule.id] = rule

    for item in as_list(data, "transitions"):
        if not isinstance(item, dict):
            raise ValueError("each transition must be a mapping")
        transition = Transition(
            id=str(item.get("id", "")),
            source=str(item.get("source", "")),
            rule=str(item.get("rule", "")),
            target=str(item.get("target", "")),
            status=str(item.get("status", "unresolved")),
            order=int(item.get("order", 0)),
        )
        if not transition.id:
            raise ValueError("transition id must be nonempty")
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
