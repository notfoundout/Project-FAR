#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from cre002_ext001_model import explore
from cre002_ext001_native import DERIVED, VOCABS, build_records, licensing_audit, lower_records

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
EXEC = PKG / "execution"
GENERATED = EXEC / "generated"
BASELINE = ROOT / "theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json"
NONCLAIMS = [
    "universal sufficiency", "primitive-only sufficiency", "necessity", "minimality",
    "independence", "superiority", "FAR proof", "universal structure of reasoning",
    "retrospective validation of CRE-002",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mutation_suite(model: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    def remove_choice(m: dict[str, Any]) -> None:
        m["transitions"][0]["nondeterministic_alternatives"].pop()

    def allow_simultaneous(m: dict[str, Any]) -> None:
        m["interleaving"]["simultaneous_execution"] = True

    def weaken_priority(m: dict[str, Any]) -> None:
        m["initial_state"]["priorities"]["R_override"] = 0

    def erase_provenance(m: dict[str, Any]) -> None:
        m["transitions"][2]["guard_expression"] = "sensor_a_positive=true AND (sensor_b_positive=true OR manual_override=true)"

    def erase_modification(m: dict[str, Any]) -> None:
        m["transitions"][6]["updates"] = ["modification_count:=1"]

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("D_nondeterminism", remove_choice),
        ("D_concurrency", allow_simultaneous),
        ("D_priority", weaken_priority),
        ("D_provenance", erase_provenance),
        ("D_rule_modification", erase_modification),
    ]
    results = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(model)
        mutate(candidate)
        try:
            detected = explore(candidate) != reference
        except Exception:
            detected = True
        results.append({"mutation": name, "detected": detected})
    return {"status": "pass" if all(x["detected"] for x in results) else "fail", "cases": results}


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    scenario_path = PKG / "scenario/scenario-v1.0.json"
    scenario, baseline = load(scenario_path), load(BASELINE)
    reference = explore(scenario)
    source_checksums = {
        "scenario": sha256(scenario_path),
        "semantic_baseline": sha256(BASELINE),
        "ambiguity_policies": sha256(PKG / "ambiguity-policies.json"),
        "decision_rules": sha256(PKG / "decision-rules.json"),
        "output_schema": sha256(PKG / "output-schema.json"),
    }
    candidates: list[dict[str, Any]] = []
    bundles: dict[str, dict[str, Any]] = {}
    for vocab in VOCABS:
        records = build_records(scenario, vocab)
        licensing = licensing_audit(baseline, vocab, records)
        model, trace = lower_records(records, vocab, scenario["scenario_id"], scenario["semantic_authority"])
        replay_model, replay_trace = lower_records(copy.deepcopy(records), vocab, scenario["scenario_id"], scenario["semantic_authority"])
        replay_pass = model == replay_model and trace == replay_trace
        behavior = explore(model)
        verifier_pass = behavior == reference
        mutation = mutation_suite(model, reference)
        complete = all([
            licensing["status"] == "pass", replay_pass, verifier_pass,
            behavior["required_outputs_preserved"], mutation["status"] == "pass",
        ])
        outcome = "complete" if complete else "partial"
        candidate = {
            "vocabulary_id": vocab,
            "source_checksums": source_checksums,
            "semantic_baseline_checksum": source_checksums["semantic_baseline"],
            "construction_status": outcome,
            "semantic_licensing_by_role": licensing,
            "derived_constructs_used": sorted(DERIVED),
            "embedded_metalanguage_classification": "bounded registered schemas only",
            "native_representation_path": f"generated/{vocab}/native-representation.json",
            "lowering_trace_path": f"generated/{vocab}/lowering-trace.json",
            "trace_replay_status": "pass" if replay_pass else "fail",
            "behavioral_verification_status": "pass" if verifier_pass else "fail",
            "shortest_counterexample": None if verifier_pass else "state-graph digest mismatch",
            "required_outputs_preserved": behavior["required_outputs_preserved"],
            "unsupported_commitments": licensing["missing_constructs"],
            "ambiguity_policy_dependence": [f"AP-{i:03d}" for i in range(1, 10)],
            "deterministic_regeneration_status": "pass" if replay_pass else "fail",
            "mutation_status": mutation["status"],
            "limitations": ["bounded scenario only", "derived machinery required", "no ranking or universal claim"],
            "outcome": outcome,
            "behavior_summary": behavior,
            "mutation_report": mutation,
        }
        candidates.append(candidate)
        bundles[vocab] = {
            "native": {"vocabulary_id": vocab, "records": records},
            "trace": {"vocabulary_id": vocab, "entries": trace},
            "model": model,
        }
    counts = Counter(c["outcome"] for c in candidates)
    comparison = {
        "experiment_id": "CRE-002-EXT-001",
        "scenario_id": scenario["scenario_id"],
        "semantic_authority": scenario["semantic_authority"],
        "reference_behavior": reference,
        "candidates": candidates,
        "candidate_outcome_counts": {name: counts.get(name, 0) for name in ["complete", "partial", "unsupported", "error"]},
        "reproducible_complete_candidates": sorted(c["vocabulary_id"] for c in candidates if c["outcome"] == "complete"),
        "nonclaims": NONCLAIMS,
    }
    return comparison, reference, bundles


def markdown(comparison: dict[str, Any]) -> str:
    lines = [
        "# CRE-002-EXT-001 Execution Report", "", "## Scope", "",
        "Prospective bounded execution under Vocabulary Semantics Baseline 1.1. The checksum-locked scientific inputs were not modified.",
        "", "## Candidate results", "",
        "| Vocabulary | Outcome | Licensing | Replay | Verifier | Mutation |",
        "|---|---|---|---|---|---|",
    ]
    for row in comparison["candidates"]:
        lines.append(f"| {row['vocabulary_id']} | {row['outcome']} | {row['semantic_licensing_by_role']['status']} | {row['trace_replay_status']} | {row['behavioral_verification_status']} | {row['mutation_status']} |")
    lines += [
        "", "## Supported conclusion", "",
        "A candidate marked complete preserved the full bounded CRE-002-EXT-001 state graph under Baseline 1.1 and all frozen ambiguity policies.",
        "", "## Nonclaims", "",
    ]
    lines.extend(f"- {item}" for item in comparison["nonclaims"])
    return "\n".join(lines) + "\n"


def expected_outputs() -> dict[Path, str]:
    comparison, reference, bundles = build()
    expected = {
        EXEC / "reference-behavior.json": json.dumps(reference, indent=2, sort_keys=True) + "\n",
        EXEC / "cre002-ext001-comparison.json": json.dumps(comparison, indent=2, sort_keys=True) + "\n",
        EXEC / "execution-report.md": markdown(comparison),
    }
    for vocab, bundle in bundles.items():
        directory = GENERATED / vocab
        expected[directory / "native-representation.json"] = json.dumps(bundle["native"], indent=2, sort_keys=True) + "\n"
        expected[directory / "lowering-trace.json"] = json.dumps(bundle["trace"], indent=2, sort_keys=True) + "\n"
        expected[directory / "generated-execution-model.json"] = json.dumps(bundle["model"], indent=2, sort_keys=True) + "\n"
    return expected


def write() -> None:
    for path, content in expected_outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def check() -> int:
    mismatches = [str(path.relative_to(ROOT)) for path, content in expected_outputs().items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
    if mismatches:
        print("CRE-002-EXT-001 EXECUTION CHECK FAILED")
        print("\n".join(mismatches))
        return 1
    print("CRE-002-EXT-001 EXECUTION CHECK PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write()
    return check() if args.check or not args.write else 0


if __name__ == "__main__":
    raise SystemExit(main())
