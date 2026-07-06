#!/usr/bin/env python3
"""Parse machine-readable FAR YAML files into FARObject structures."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml

from far_core import FARObject, InterpretationAssignment, Relation, Representation, Rule, Transition


def load_far_yaml(path: Path) -> FARObject:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("FAR file must contain a YAML mapping")

    investigation = str(data.get("investigation", ""))
    far = FARObject(investigation=investigation)

    for item in data.get("representations", []):
        rep = Representation(
            id=str(item["id"]),
            kind=str(item.get("kind", "claim")),
            content=str(item.get("content", "")),
        )
        if rep.id in far.representations:
            raise ValueError(f"duplicate representation id: {rep.id}")
        far.representations[rep.id] = rep

    for item in data.get("relations", []):
        rel = Relation(
            id=str(item["id"]),
            type=str(item["type"]),
            source=str(item["source"]),
            target=str(item["target"]),
        )
        if rel.id in far.relations:
            raise ValueError(f"duplicate relation id: {rel.id}")
        far.relations[rel.id] = rel

    for item in data.get("interpretations", []):
        assignment = InterpretationAssignment(
            representation=str(item["representation"]),
            meaning=str(item.get("meaning", "")),
        )
        far.interpretations[assignment.representation] = assignment

    for item in data.get("rules", []):
        rule = Rule(
            id=str(item["id"]),
            name=str(item.get("name", item["id"])),
            inputs=[str(x) for x in item.get("inputs", [])],
            output=str(item["output"]),
            condition=str(item.get("condition", "")),
        )
        if rule.id in far.rules:
            raise ValueError(f"duplicate rule id: {rule.id}")
        far.rules[rule.id] = rule

    for item in data.get("transitions", []):
        transition = Transition(
            id=str(item["id"]),
            source=str(item["source"]),
            rule=str(item["rule"]),
            target=str(item["target"]),
            status=str(item.get("status", "unresolved")),
            order=int(item["order"]),
        )
        if transition.id in far.transitions:
            raise ValueError(f"duplicate transition id: {transition.id}")
        far.transitions[transition.id] = transition

    return far


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse and validate a FAR YAML file")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    far = load_far_yaml(args.path)
    errors = far.validate_well_formed()
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
