#!/usr/bin/env python3
"""Fail-closed validation and deterministic reporting for FARA-REP-W4-001."""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "theory/evaluation/fara-w4-representation-boundary-v1.0.json"
REPORT = ROOT / "theory/evaluation/generated-fara-w4-representation-summary.md"
DIMENSIONS = ("structural", "semantic", "operational", "dependency", "information", "historical")
STATUSES = {"Pass", "Partial", "Fail", "Unknown"}
CLAIMS = {
    "representability", "lossless_representability", "recoverability", "behavioral_equivalence",
    "semantic_equivalence", "historical_dependency_preservation", "operational_simulation",
    "bidirectional_translation",
}
TOPICS = {
    "changing rule sets", "changing semantic interpretations", "incompatible or evolving ontologies",
    "nonmonotonic revision", "paraconsistency", "probabilistic information",
    "causal and counterfactual structure", "continuous state", "embodied or tacit information",
    "external observation or oracle access", "identity-changing merge or quotient operations",
    "deletion and constraint relaxation", "provenance-sensitive histories",
}
OWNER_FIELDS = ("id", "proof_object_id", "claim_id", "theorem_id")


def load() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def encode_source(source: dict) -> str:
    required = {"X", "R", "Sem", "Step", "Obs", "Hist", "Ext"}
    assert set(source) == required
    archive = {
        "format": "finite_tagged_archive_v1",
        "X": [{"id": item["id"], "type": item["type"]} for item in source["X"]],
        "R": [{"id": item["id"], "premise": item["premise"], "conclusion": item["conclusion"]} for item in source["R"]],
        "Sem": [{"symbol": item["symbol"], "meaning": item["meaning"], "version": item["version"]} for item in source["Sem"]],
        "Step": [{"from": item["from"], "input": item["input"], "to": item["to"]} for item in source["Step"]],
        "Obs": list(source["Obs"]),
        "Hist": [{"seq": item["seq"], "event": item["event"]} for item in source["Hist"]],
        "Ext": {
            "ratio": [source["Ext"]["ratio"].numerator, source["Ext"]["ratio"].denominator],
            "flags": list(source["Ext"]["flags"]),
        },
    }
    return json.dumps(archive, sort_keys=True, separators=(",", ":"))


def decode_source(archive_text: str) -> dict:
    archive = json.loads(archive_text)
    assert archive["format"] == "finite_tagged_archive_v1"
    numerator, denominator = archive["Ext"]["ratio"]
    return {
        "X": archive["X"],
        "R": archive["R"],
        "Sem": archive["Sem"],
        "Step": archive["Step"],
        "Obs": archive["Obs"],
        "Hist": archive["Hist"],
        "Ext": {"ratio": Fraction(numerator, denominator), "flags": archive["Ext"]["flags"]},
    }


def fixture(bits: tuple[int, ...]) -> dict:
    x, rule, sem, step, hist, ext = bits
    state0 = "s1" if x else "s0"
    state1 = "s0" if step else "s1"
    return {
        "X": [{"id": state0, "type": "state"}, {"id": state1, "type": "state"}],
        "R": [{"id": "r1", "premise": "p", "conclusion": "q" if rule else "p"}],
        "Sem": [{"symbol": "p", "meaning": "true" if sem else "unknown", "version": sem}],
        "Step": [{"from": state0, "input": "tick", "to": state1}],
        "Obs": ["state", "q" if rule else "p"],
        "Hist": [{"seq": 0, "event": "init"}, {"seq": 1, "event": "transition" if hist else "observe"}],
        "Ext": {"ratio": Fraction(2 if ext else 1, 3), "flags": [bool(ext)]},
    }


def exhaustive_injection_check() -> None:
    sources = [fixture(bits) for bits in itertools.product(range(2), repeat=6)]
    encoded = [encode_source(source) for source in sources]
    assert len(encoded) == len(set(encoded)) == 64
    for source, archive in zip(sources, encoded):
        assert decode_source(archive) == source


def _json_owner_values(value: object, found: set[tuple[str, str]]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in OWNER_FIELDS and isinstance(item, str):
                found.add((key, item))
            _json_owner_values(item, found)
    elif isinstance(value, list):
        for item in value:
            _json_owner_values(item, found)


def duplicate_owner_paths(data: dict) -> list[str]:
    expected = {(field, data[field]) for field in OWNER_FIELDS}
    owners = []
    for path in (ROOT / "theory/evaluation").glob("*.json"):
        if path == ARTIFACT:
            continue
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            continue
        found: set[tuple[str, str]] = set()
        _json_owner_values(parsed, found)
        if expected & found:
            owners.append(str(path.relative_to(ROOT)))
    return owners


def validate(data: dict) -> None:
    assert data["id"] == "FARA-REP-W4-001"
    assert data["proof_object_id"] == "FARA-W4-PROOF-001"
    assert data["claim_id"] == "CLM-REP-W4-001"
    assert data["theorem_id"] == "THM-REP-001"
    assert data["authority_recovery"]["w3_consumed"] is False
    assert set(data["authority_recovery"]["dependencies"]) == {"FARA-W1-PRIMITIVE-INDEPENDENCE-001", "FARA-OPS-W2-001"}
    assert tuple(data["contract"]["preservation_vector"]) == DIMENSIONS
    assert data["contract"]["failure_outputs"] and data["contract"]["excluded"]
    assert set(data["claim_separation"]) == CLAIMS
    results = data["results"]
    assert len(results) == 14 and len({case["id"] for case in results}) == len(results)
    assert TOPICS <= {case["topic"] for case in results}
    assert sum(case["kind"] == "positive" for case in results) >= 4
    assert sum(case["kind"] in {"failure", "unresolved"} for case in results) >= 8
    for case in results:
        assert set(case["preservation"]) == set(DIMENSIONS), f"incomplete vector: {case['id']}"
        assert set(case["preservation"].values()) <= STATUSES
        assert set(case["claims"]) == CLAIMS
        assert case["recovery"] in {"exact", "partial", "impossible", "unknown"}
        assert isinstance(case["hidden_auxiliary"], bool) and isinstance(case["narrowed_observation"], bool)
        assert case["witness"] and case["information_change"]
        all_pass = all(value == "Pass" for value in case["preservation"].values())
        justified_lossless = all_pass and case["recovery"] == "exact" and not case["hidden_auxiliary"] and not case["narrowed_observation"]
        assert case["claims"]["lossless_representability"] is justified_lossless, f"omitted loss: {case['id']}"
        assert case["claims"]["recoverability"] is (case["recovery"] == "exact"), f"recovery claim mismatch: {case['id']}"
        if case["hidden_auxiliary"]:
            assert case.get("hidden_detail") and not case["claims"]["lossless_representability"]
        if case["narrowed_observation"] and case["claims"]["behavioral_equivalence"]:
            assert not case["claims"]["semantic_equivalence"], f"weak interface promoted: {case['id']}"
    assert data["strongest_results"]["unresolved"]
    prohibited = {"all reasoning systems are representable", "finite examples prove universal faithfulness", "simulation proves recovery", "unknown is pass"}
    assert prohibited <= set(data["nonclaims"])
    assert data["assurance"]["proof_assistant_verification"] == "not performed"
    exhaustive_injection_check()


def report(data: dict) -> str:
    lines = [
        "# Generated FARA W4 representation boundary summary", "",
        "Generated deterministically by `python tools/check_fara_w4_representation.py --write`.", "",
        "## Frozen contract", "", data["contract"]["source_system"], "", data["contract"]["target_representation"], "",
        "## Registered cases", "",
        "| ID | Topic | Kind | Preservation S/Sem/O/D/I/H | Recovery | Hidden | Narrowed |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for case in data["results"]:
        vector = "/".join(case["preservation"][d] for d in DIMENSIONS)
        lines.append(f"| {case['id']} | {case['topic']} | {case['kind']} | {vector} | {case['recovery']} | {str(case['hidden_auxiliary']).lower()} | {str(case['narrowed_observation']).lower()} |")
    lines += ["", "## Strongest bounded result", "", data["strongest_results"]["bounded_sufficient_condition"], "", "## Explicit nonclaims", ""]
    lines += [f"- {item}" for item in data["nonclaims"]]
    lines += ["", "## Unresolved obligations", ""] + [f"- {item}" for item in data["strongest_results"]["unresolved"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = load()
    validate(data)
    expected = report(data)
    if args.write:
        REPORT.write_text(expected, encoding="utf-8")
    else:
        assert REPORT.read_text(encoding="utf-8") == expected, "generated report stale"
    owners = duplicate_owner_paths(data)
    assert not owners, f"duplicate identifier owners: {owners}"
    print("FARA W4 representation boundary: PASS (14 cases; exhaustive 64-source encoder/decoder check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
