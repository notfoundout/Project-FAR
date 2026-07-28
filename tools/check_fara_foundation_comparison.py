#!/usr/bin/env python3
"""FARA foundation-comparison validator with proof-derived prose checks."""
from __future__ import annotations

import re

import check_fara_foundation_comparison_core as _core

# Re-export the established executable campaign implementation. The core file is
# the exact prior validator blob; this wrapper adds claim-bearing prose checks
# without duplicating or weakening the executable evidence logic.
for _name, _value in vars(_core).items():
    if not _name.startswith("__"):
        globals()[_name] = _value

_SNAPSHOT_START = "<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->"
_SNAPSHOT_END = "<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->"
_STALE_CLAIMS = (
    "dominance graph has no edges",
    "no pareto edge",
    "finds no edge",
    "has no edge",
    "retain all three candidates as incomparable",
    "retains all three candidates as incomparable",
    "no candidate is no worse",
)


def _without_snapshot(text: str) -> str:
    start = text.find(_SNAPSHOT_START)
    end = text.find(_SNAPSHOT_END)
    if start < 0 or end < 0 or end < start:
        return text
    return text[:start] + text[end + len(_SNAPSHOT_END) :]


def _normalize(text: str) -> str:
    text = text.lower().replace("`", "").replace("*", "")
    text = re.sub(r"[-_/]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _human_name(name: str) -> str:
    return _normalize(name)


def _line_has_forward_edge(line: str, source: str, target: str) -> bool:
    normalized = _normalize(line)
    source_name = _human_name(source)
    target_name = _human_name(target)
    source_index = normalized.find(source_name)
    target_index = normalized.find(target_name)
    if source_index < 0 or target_index < 0 or source_index >= target_index:
        return False
    between = normalized[source_index + len(source_name) : target_index]
    return "dominates" in between or "pareto dominates" in between or "→" in line or "->" in line


def _line_has_reverse_edge(line: str, source: str, target: str) -> bool:
    normalized = _normalize(line)
    source_name = _human_name(source)
    target_name = _human_name(target)
    target_index = normalized.find(target_name)
    source_index = normalized.find(source_name)
    if target_index < 0 or source_index < 0 or target_index >= source_index:
        return False
    between = normalized[target_index + len(target_name) : source_index]
    return "dominates" in between or "pareto dominates" in between or "→" in line or "->" in line


def validate_authoritative_claims(text: str, proof: dict) -> bool:
    """Validate claim-bearing prose independently of the evidence snapshot."""
    body = _without_snapshot(text)
    lowered = _normalize(body)
    if any(stale in lowered for stale in _STALE_CLAIMS):
        return False

    edges = proof.get("dominance_graph", {}).get("edges", [])
    if len(edges) != 1 or len(edges[0]) != 2:
        return False
    source, target = edges[0]
    lines = [line for line in body.splitlines() if line.strip()]
    if not any(_line_has_forward_edge(line, source, target) for line in lines):
        return False
    if any(_line_has_reverse_edge(line, source, target) for line in lines):
        return False

    incomparable_pairs = {
        frozenset((row.get("a"), row.get("b")))
        for row in proof.get("incomparability_witnesses", [])
        if row.get("a") and row.get("b")
    }
    required_pair = frozenset(("typed-hypergraph", "many-sorted-relational"))
    if required_pair not in incomparable_pairs:
        return False
    if not any(
        "typed hypergraph" in _normalize(line)
        and "many sorted relational" in _normalize(line)
        and "incomparable" in _normalize(line)
        for line in lines
    ):
        return False

    terminal = proof.get("terminal_result")
    if terminal != "multiple foundations remain Pareto-incomparable":
        return False
    return True


def validate_authoritative_text(text: str, proof: dict) -> bool:
    snapshot = _core.authoritative_snapshot(proof)
    snapshot_valid = (
        text.count(snapshot) == 1
        and text.count(_SNAPSHOT_START) == 1
        and text.count(_SNAPSHOT_END) == 1
    )
    return snapshot_valid and validate_authoritative_claims(text, proof)


# Patch the core module's global so its existing validate() and main() execute
# the strengthened prose validation, then expose the strengthened functions.
_core.validate_authoritative_claims = validate_authoritative_claims
_core.validate_authoritative_text = validate_authoritative_text
globals()["validate_authoritative_claims"] = validate_authoritative_claims
globals()["validate_authoritative_text"] = validate_authoritative_text


if __name__ == "__main__":
    _core.main()
