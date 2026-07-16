#!/usr/bin/env python3
"""Validate the frozen, non-executed CRE-002 preregistration package."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
REQUIRED = [
    "README.md",
    "preregistration.md",
    "scenario/scenario-v1.0.md",
    "scenario/scenario-v1.0.json",
    "ambiguity-policies.json",
    "decision-rules.json",
    "execution-lock.json",
    "package-manifest.json",
]
NONCLAIMS = [
    "universal sufficiency",
    "primitive-only sufficiency",
    "necessity",
    "minimality",
    "independence",
    "superiority",
    "FAR proof",
    "universal structure of reasoning",
]


def load(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (BASE / rel).is_file():
            errors.append(f"missing {rel}")
    if errors:
        print("CRE-002 PREREGISTRATION CHECK FAILED")
        print("\n".join(errors))
        return 1

    scenario = load("scenario/scenario-v1.0.json")
    policies = load("ambiguity-policies.json")
    decisions = load("decision-rules.json")
    lock = load("execution-lock.json")
    manifest = load("package-manifest.json")

    if lock.get("execution_permitted") is not False:
        errors.append("execution lock must remain false in preregistration PR")
    if manifest.get("execution_permitted") is not False:
        errors.append("manifest must mark execution as prohibited")
    if manifest.get("official_results_present") is not False:
        errors.append("manifest must state no official results exist")
    if len(scenario.get("transitions", [])) < 9:
        errors.append("scenario transition set is incomplete")
    if len(policies.get("policies", [])) < 8:
        errors.append("ambiguity policy set is incomplete")
    if set(decisions.get("candidate_outcomes", [])) != {"complete", "partial", "unsupported", "error"}:
        errors.append("candidate outcome set differs from preregistration")
    manifest_paths = {entry.get("path") for entry in manifest.get("files", [])}
    for rel in REQUIRED[:-1]:
        if rel not in manifest_paths:
            errors.append(f"manifest omits {rel}")
    combined = "\n".join((BASE / rel).read_text(encoding="utf-8") for rel in ["README.md", "preregistration.md"])
    for claim in NONCLAIMS:
        if claim not in combined:
            errors.append(f"missing nonclaim: {claim}")
    forbidden_dirs = [BASE / "results", BASE / "generated", BASE / "submissions"]
    for path in forbidden_dirs:
        if path.exists() and any(path.rglob("*")):
            errors.append(f"official execution material exists before unlock: {path.relative_to(ROOT)}")

    if errors:
        print("CRE-002 PREREGISTRATION CHECK FAILED")
        print("\n".join(errors))
        return 1
    print("CRE-002 PREREGISTRATION CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
