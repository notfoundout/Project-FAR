#!/usr/bin/env python3
"""Execute the preregistered CRE-002 semantic-licensing gate.

CRE-002 requires semantic licensing before native compilation or behavioral
verification. The frozen baseline explicitly declares only five derived
constructs. It does not declare machinery for five new CRE-002 pressure
classes. Under CRE-002-DECISION-RULES-1.0, each candidate therefore receives
an official `unsupported` outcome at the prerequisite gate.

This is not a claim that the informal vocabularies are inherently incapable of
representing the scenario. It is a claim about what the frozen prospective
semantic authority explicitly licenses.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
SEMANTICS = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/semantics/semantic-specification.json"
RESULT = BASE / "execution/cre002-comparison.json"
REPORT = ROOT / "docs/reports/cre002-prospective-comparison.md"
VOCABS = ["CRE-001-VOCAB-A-1.0", "CRE-001-VOCAB-B-1.0", "CRE-001-VOCAB-C-1.0"]
REQUIRED_CAPABILITIES = {
    "nested conditions": ["D_guarded_update", "D_disjunction"],
    "bounded nondeterminism": ["D_nondeterminism"],
    "interleaved concurrency": ["D_concurrency"],
    "defeasible priority": ["D_priority"],
    "provenance sensitivity": ["D_provenance"],
    "higher-order rule modification": ["D_rule_modification"],
    "bounded history": ["D_ordered_history"],
    "terminal deadlock": ["D_terminality"],
}
NONCLAIMS = [
    "universal sufficiency", "primitive-only sufficiency", "necessity",
    "minimality", "independence", "superiority", "FAR proof",
    "universal structure of reasoning",
    "the informal vocabularies are inherently incapable of representing CRE-002",
    "behavioral failure of any candidate vocabulary",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def declared_constructs(semantics: dict[str, Any]) -> set[str]:
    return {
        item["identifier"]
        for item in semantics.get("derived_constructs", [])
        if item.get("classification") == "derived"
    }


def licensing_audit(available: set[str]) -> dict[str, Any]:
    dimensions = []
    for dimension, required in REQUIRED_CAPABILITIES.items():
        missing = sorted(set(required) - available)
        dimensions.append({
            "dimension": dimension,
            "licensed": not missing,
            "missing_constructs": missing,
            "required_constructs": required,
        })
    return {
        "all_required_commitments_licensed": all(item["licensed"] for item in dimensions),
        "dimensions": dimensions,
        "missing_constructs": sorted({m for item in dimensions for m in item["missing_constructs"]}),
    }


def mutation_audit(available: set[str]) -> dict[str, Any]:
    all_required = {item for group in REQUIRED_CAPABILITIES.values() for item in group}
    completed = licensing_audit(available | all_required)
    removed = licensing_audit(available - {"D_guarded_update"})
    baseline = licensing_audit(available)
    cases = [
        {
            "detected": completed["all_required_commitments_licensed"],
            "mutation": "add every explicitly required construct",
        },
        {
            "detected": "D_guarded_update" in removed["missing_constructs"],
            "mutation": "remove D_guarded_update",
        },
    ]
    return {
        "cases": cases,
        "passed": (
            not baseline["all_required_commitments_licensed"]
            and all(case["detected"] for case in cases)
        ),
    }


def build_result() -> dict[str, Any]:
    scenario = load(BASE / "scenario/scenario-v1.0.json")
    decisions = load(BASE / "decision-rules.json")
    manifest = load(BASE / "package-manifest.json")
    control = load(BASE / "execution-lock.json")
    semantics = load(SEMANTICS)
    if control.get("execution_permitted") is not True or manifest.get("execution_permitted") is not True:
        raise ValueError("CRE-002 execution is not authorized")
    if decisions.get("decision_rule_id") != "CRE-002-DECISION-RULES-1.0":
        raise ValueError("unexpected CRE-002 decision rule version")
    if semantics.get("chronology", {}).get("frozen_for") != "future experiments beginning with CRE-002":
        raise ValueError("Vocabulary Semantics Baseline 1.0 is not prospective for CRE-002")

    available = declared_constructs(semantics)
    audit = licensing_audit(available)
    mutation = mutation_audit(available)
    if audit["all_required_commitments_licensed"]:
        raise ValueError("licensing unexpectedly passed; this pipeline must be reviewed before compilation")
    if not mutation["passed"]:
        raise ValueError("semantic-licensing mutation audit failed")

    candidates = []
    for vocabulary in VOCABS:
        candidates.append({
            "behavioral_verification_attempted": False,
            "decision_basis": "A required commitment cannot be licensed under Vocabulary Semantics Baseline 1.0.",
            "licensing_audit": audit,
            "native_compilation_attempted": False,
            "outcome": "unsupported",
            "scope_note": "This outcome concerns the frozen baseline's declared licensing, not possible expressivity under future semantics.",
            "shortest_counterexample": None,
            "vocabulary_id": vocabulary,
        })

    return {
        "aggregate": {
            "complete_candidates": 0,
            "error_candidates": 0,
            "existential_complete": False,
            "partial_candidates": 0,
            "reproducible_complete": False,
            "unsupported_candidates": 3,
        },
        "artifact_id": "CRE-002-COMPARISON-1.0",
        "available_declared_derived_constructs": sorted(available),
        "candidates": candidates,
        "decision_rule_id": decisions["decision_rule_id"],
        "execution_authorized": True,
        "mutation_audit": mutation,
        "nonclaims": NONCLAIMS,
        "scenario_audit": {
            "frozen_package_checksum_verified_by": "tools/check_cre002_lock.py",
            "required_pressure_dimensions": list(REQUIRED_CAPABILITIES),
            "transition_count": len(scenario.get("transitions", [])),
        },
        "scenario_id": scenario["scenario_id"],
        "semantic_authority": semantics["artifact_id"],
        "status": "official prospective execution result",
        "supported_conclusions": [
            "Vocabulary Semantics Baseline 1.0 does not explicitly license every required CRE-002 commitment.",
            "Each official candidate receives the preregistered outcome unsupported at the semantic-licensing gate.",
            "No native candidate compiler or behavioral verifier result is claimed after the failed prerequisite gate.",
        ],
    }


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def render_report(data: dict[str, Any]) -> str:
    missing = data["candidates"][0]["licensing_audit"]["missing_constructs"]
    rows = "\n".join(
        f"| {candidate['vocabulary_id']} | {candidate['outcome']} | No | No |"
        for candidate in data["candidates"]
    )
    return f"""# CRE-002 Prospective Vocabulary Comparison

## Result

CRE-002 stopped at the preregistered semantic-licensing gate. Vocabulary Semantics Baseline 1.0 does not explicitly license all commitments required by the frozen scenario.

Missing declared constructs: {', '.join(missing)}.

| Vocabulary | Outcome | Native compilation attempted | Behavioral verification attempted |
|---|---:|---:|---:|
{rows}

## Interpretation

The outcome is **unsupported**, exactly as defined by `CRE-002-DECISION-RULES-1.0`: at least one required commitment cannot be licensed under the frozen semantics baseline. It is not a behavioral counterexample and does not show that the informal vocabularies are inherently incapable of representing the scenario.

## Supported conclusions

- The prospective baseline licenses nested guarded structure, bounded ordered history, and terminality through its declared machinery.
- It does not explicitly license bounded nondeterminism, interleaved concurrency, defeasible priority, provenance sensitivity, or higher-order rule modification.
- All three candidates therefore fail the same prerequisite licensing gate before native compilation.

## Nonclaims

No universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, FAR proof, universal structure of reasoning, vocabulary impossibility, or behavioral-failure conclusion is supported.
"""


def verify_checksum() -> None:
    result = subprocess.run(
        [sys.executable, "tools/check_cre002_lock.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)


def generated_files() -> dict[Path, str]:
    result = build_result()
    return {RESULT: render_json(result), REPORT: render_report(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        verify_checksum()
        files = generated_files()
        if args.write:
            for path, content in files.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        if args.check:
            for path, expected in files.items():
                if not path.exists() or path.read_text(encoding="utf-8") != expected:
                    raise ValueError(f"generated CRE-002 artifact drift: {path.relative_to(ROOT)}")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"CRE-002 execution failed: {exc}", file=sys.stderr)
        return 1
    print("CRE-002 prospective execution completed: 3 unsupported, 0 complete, 0 partial, 0 error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
