"""Candidate reconstruction and exact six-dimensional comparison."""
from __future__ import annotations

import copy
import importlib
import json

DIMENSIONS = ("structural", "semantic", "operational", "dependency", "information", "historical")
MODULES = {
    "many-sorted-relational": "theory.foundation.fara_foundation_comparison.many_sorted",
    "typed-hypergraph": "theory.foundation.fara_foundation_comparison.typed_hypergraph",
    "algebraic-state-transition": "theory.foundation.fara_foundation_comparison.algebraic_state",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def reconstruct(source, trace, execution):
    foundation = trace["target_model"]["candidate"] if trace.get("target_model") else None
    if foundation is None:
        return {
            "reconstruction_steps": [],
            "recovered_elements": [],
            "recovered_commitments": {dimension: None for dimension in DIMENSIONS},
            "recovered_result": {"status": "Unknown", "reason": source.get("unknown_reason")},
        }
    module = importlib.import_module(MODULES[foundation])
    recovered = module.recover(trace["target_model"], execution)
    reverse = {target: key for key, target in trace["correspondence_map"].items()}
    return {
        "reconstruction_steps": [
            {"target": target, "source": reverse[target]}
            for target in trace["generated_target_elements"]
            if target in reverse
        ],
        "recovered_elements": [reverse[target] for target in trace["generated_target_elements"] if target in reverse],
        "recovered_commitments": recovered["commitments"],
        "recovered_result": recovered["result"],
    }


def compare(source, reconstruction, reference_result):
    preservation = {}
    differences = {}
    for dimension in DIMENSIONS:
        expected = source["commitments"][dimension]
        observed = reconstruction["recovered_commitments"][dimension]
        if expected is None:
            preservation[dimension] = "Unknown"
        elif canonical(expected) == canonical(observed):
            preservation[dimension] = "Pass"
        else:
            preservation[dimension] = "Fail"
            differences[dimension] = {"expected": copy.deepcopy(expected), "observed": copy.deepcopy(observed)}
    result_equivalent = canonical(reference_result) == canonical(reconstruction["recovered_result"])
    return {
        "preservation": preservation,
        "differences": differences,
        "result_equivalent": result_equivalent,
        "commitment_equivalent": all(value == "Pass" for value in preservation.values()) and result_equivalent,
        "missing": sorted(differences),
    }
