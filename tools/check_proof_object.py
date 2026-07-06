#!/usr/bin/env python3
"""Structural proof-object checker for Project FAR YAML proof objects."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Set

import yaml

ALLOWED_RULES = {
    "definition_unfolding",
    "axiom_application",
    "prior_theorem",
    "lemma_application",
    "modus_ponens",
    "conjunction_intro",
    "universal_instantiation",
    "registry_substitution",
    "semantic_preservation",
}

REQUIRED_FIELDS = {"id", "theorem", "status", "premises", "steps", "conclusion"}


def check_proof_object(path: Path) -> List[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["proof object must be a mapping"]

    missing = REQUIRED_FIELDS - set(data)
    if missing:
        errors.append(f"missing required fields: {sorted(missing)}")

    premise_ids: Set[str] = set()
    for premise in data.get("premises", []):
        pid = str(premise.get("id", ""))
        if not pid:
            errors.append("premise missing id")
        if pid in premise_ids:
            errors.append(f"duplicate premise id: {pid}")
        premise_ids.add(pid)

    available: Set[str] = set(premise_ids)
    step_ids: Set[str] = set()
    for step in data.get("steps", []):
        sid = str(step.get("id", ""))
        if not sid:
            errors.append("step missing id")
            continue
        if sid in step_ids:
            errors.append(f"duplicate step id: {sid}")
        step_ids.add(sid)

        rule = str(step.get("rule", ""))
        if rule not in ALLOWED_RULES:
            errors.append(f"step {sid} uses unknown rule: {rule}")

        for inp in step.get("inputs", []):
            inp = str(inp)
            if inp not in available:
                errors.append(f"step {sid} references unavailable input: {inp}")

        if not step.get("statement"):
            errors.append(f"step {sid} missing statement")
        if not step.get("justification"):
            errors.append(f"step {sid} missing justification")

        available.add(sid)

    conclusion = str(data.get("conclusion", ""))
    if conclusion and conclusion not in {str(step.get("statement", "")) for step in data.get("steps", [])}:
        errors.append("conclusion does not match any proof step statement")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Project FAR proof object")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = check_proof_object(args.path)
    if errors:
        print("PROOF OBJECT CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PROOF OBJECT CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
