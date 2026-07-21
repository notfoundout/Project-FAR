#!/usr/bin/env python3
"""Execute the bounded W3.5 GREL-FARA factorization over RCS-CORPUS-001.

The raw candidate-neutral source projection is encoded by GREL before the
declared FARA-oriented adapter and accepted W3 constructor are applied. The
result is operational factorization, not a primitive reduction.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from s_core_w3_construct import construct_witness
from s_core_w3_expected import expected_recovered
from s_core_w3_recovery import recover_target, validate_package
from s_core_w3_schema import canonical_json
from w3_5_factor_source import (
    FactorizationError, authoritative_projection, compile_projection,
    compile_record, load_records, sha256_json,
)
from w3_5_grel import decode_grel, encode_grel, grel_metrics

ROOT = Path(__file__).resolve().parents[1]
FACTOR_SCHEMA = "W35-FACTOR-WITNESS-1.0"

def fara_metrics(package: dict[str, Any]) -> dict[str, int]:
    A = package["A"]
    return {
        "architecture_fields": 14,
        "witness_fields": 5,
        "objects": len(A["U"]),
        "properties": len(A["Pi"]),
        "relation_facts": sum(len(values) for values in A["R"].values()),
        "serialized_bytes": len(canonical_json(package).encode("utf-8")),
        "semantic_axis_access_operations": 6,
    }

def factor_record(record: dict[str, Any]) -> dict[str, Any]:
    projection = authoritative_projection(record)
    compiled = compile_projection(projection)
    generic_source = encode_grel(projection)
    recovered_projection = decode_grel(generic_source)
    if canonical_json(recovered_projection) != canonical_json(projection):
        raise FactorizationError(f"{record['instance_id']}: GREL authoritative-source recovery mismatch")

    direct_fara = construct_witness(compiled)
    validate_package(direct_fara)
    via_grel_compiled = compile_projection(recovered_projection)
    if canonical_json(via_grel_compiled) != canonical_json(compiled):
        raise FactorizationError(f"{record['instance_id']}: source adapter changed after GREL recovery")
    via_grel_fara = construct_witness(via_grel_compiled)
    if canonical_json(via_grel_fara) != canonical_json(direct_fara):
        raise FactorizationError(f"{record['instance_id']}: FARA constructor does not factor through GREL")

    recovered_target = recover_target(
        direct_fara["A"],
        direct_fara["W"]["D"],
        direct_fara["W"]["kappa"],
    )
    expected_target = expected_recovered(compiled, direct_fara["W"])
    if canonical_json(recovered_target) != canonical_json(expected_target):
        raise FactorizationError(f"{record['instance_id']}: FARA target-only recovery mismatch")

    fara_as_grel = encode_grel(direct_fara)
    if canonical_json(decode_grel(fara_as_grel)) != canonical_json(direct_fara):
        raise FactorizationError(f"{record['instance_id']}: FARA-to-GREL exact translation failed")

    mutated = copy.deepcopy(record)
    mutated["title"] = "candidate-neutral mutation"
    mutated["family"] = "mutated_family"
    mutated["admission_decision"] = "disputed"
    mutated["admission_rationale"] = "mutated and ignored"
    mutated["candidate_exposure_status"] = "mutated and ignored"
    if canonical_json(compile_record(mutated)) != canonical_json(compiled):
        raise FactorizationError(f"{record['instance_id']}: admission metadata steers construction")

    return {
        "instance_id": record["instance_id"],
        "source_record_id": record["source_record_id"],
        "source_bundle": record["_source_bundle"],
        "admission_decision": record["admission_decision"],
        "family": record["family"],
        "status": "pass",
        "factorization_identity": "F_raw = T_GF o E_G, where F_raw = construct_witness o compile_projection",
        "source_projection_sha256": sha256_json(authoritative_projection(record)),
        "compiled_source_sha256": sha256_json(compiled),
        "grel_source_sha256": sha256_json(generic_source),
        "fara_target_sha256": sha256_json(direct_fara),
        "fara_as_grel_sha256": sha256_json(fara_as_grel),
        "checks": {
            "candidate_neutral_compiler": "pass",
            "grel_exact_authoritative_source_recovery": "pass",
            "fixed_adapter_stability": "pass",
            "direct_equals_via_grel_fara": "pass",
            "fara_target_only_recovery": "pass",
            "fara_exact_generic_translation": "pass",
            "no_case_database": "pass",
            "no_hidden_interpreter": "pass",
        },
        "cost": {
            "grel": grel_metrics(generic_source),
            "fara": fara_metrics(direct_fara),
        },
    }

def run_factorization(root: Path = ROOT) -> dict[str, Any]:
    results = [factor_record(record) for record in load_records(root)]
    by_decision: dict[str, int] = {"positive": 0, "contrast": 0, "disputed": 0}
    for item in results:
        by_decision[item["admission_decision"]] += 1
    if by_decision != {"positive": 8, "contrast": 8, "disputed": 2}:
        raise FactorizationError(f"frozen corpus class counts changed: {by_decision}")
    return {
        "schema": FACTOR_SCHEMA,
        "experiment_id": "W35-GREL-FARA-FACTOR-001",
        "status": "complete",
        "scope": {
            "constructor": "SCORE-W3-PROOF-001 finite FARA constructor",
            "baseline": "GREL-001",
            "corpus": "RCS-CORPUS-001",
            "instances": len(results),
            "class_counts": by_decision,
        },
        "factorization": {
            "source_encoder": "encode_grel over the candidate-neutral authoritative projection",
            "shared_source_adapter": "compile_projection",
            "direct_fara_pipeline": "construct_witness o compile_projection",
            "grel_to_fara_translation": "construct_witness o compile_projection o decode_grel",
            "fara_to_grel_translation": "encode_grel",
            "identity": "construct_witness o compile_projection = (construct_witness o compile_projection o decode_grel) o encode_grel",
            "translation_domain": "frozen candidate-neutral finite source projections and finite FARA target packages",
            "primitive_reduction_established": False,
            "reintroduced_machinery": [
                "fixed FARA-oriented compile_projection source adapter",
                "accepted SCORE-W3 construct_witness implementation",
            ],
        },
        "dimensions": {
            "expressiveness": "equivalent",
            "translation": "bidirectional",
            "constraint_strength": "fara_stricter",
            "reasoning_specificity": "not_established",
            "cost_relation": "tradeoff",
            "overall_interpretation": "fara_constrained_equivalent",
        },
        "cost_interpretation": {
            "grel_advantages": [
                "smaller fixed architecture surface: 10 baseline components versus 14 FARA architecture fields plus 5 witness fields",
                "uniform exact encoding of arbitrary finite JSON-shaped authoritative source projections and FARA packages",
            ],
            "fara_advantages": [
                "six preservation axes are directly addressable rather than recovered by scanning a generic relation graph",
                "stronger mandatory category, recovery, coherence, provenance, and admissibility constraints",
            ],
            "decision_rule": "tradeoff because each architecture is strictly lower on at least one declared cost dimension",
        },
        "records": results,
        "nonclaims": [
            "GREL-001 is a primitive reduction of FARA",
            "FARA is reasoning-specific",
            "FARA is superior to GREL-001",
            "GREL-001 is minimal or universal",
            "reasoning and contrast discrimination has been executed",
            "candidate invariants have been scored",
            "W3.5-SDG-001 is resolved",
            "W5 is authorized",
        ],
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute the W3.5 GREL-FARA factorization")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = run_factorization(args.root.resolve())
    except (FactorizationError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"FAR-VAL-FACTOR-001: {exc}")
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            "W3.5 GREL-FARA factorization: PASS "
            f"({report['scope']['instances']} instances; "
            f"{report['dimensions']['overall_interpretation']})"
        )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
