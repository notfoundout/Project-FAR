"""Proof-derived validation for authoritative FARA foundation-comparison prose."""
from __future__ import annotations

import re
from collections.abc import Callable

SNAPSHOT_START = "<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->"
SNAPSHOT_END = "<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->"
STALE_CLAIMS = (
    "dominance graph has no edges",
    "no pareto edge",
    "finds no edge",
    "has no edge",
    "retain all three candidates as incomparable",
    "retains all three candidates as incomparable",
    "no candidate is no worse",
)


def without_snapshot(text: str) -> str:
    start = text.find(SNAPSHOT_START)
    end = text.find(SNAPSHOT_END)
    if start < 0 or end < 0 or end < start:
        return text
    return text[:start] + text[end + len(SNAPSHOT_END) :]


def normalize(text: str) -> str:
    text = text.lower().replace("`", "").replace("*", "")
    text = re.sub(r"[-_/]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def line_has_forward_edge(line: str, source: str, target: str) -> bool:
    normalized = normalize(line)
    source_name = normalize(source)
    target_name = normalize(target)
    source_index = normalized.find(source_name)
    target_index = normalized.find(target_name)
    if source_index < 0 or target_index < 0 or source_index >= target_index:
        return False
    between = normalized[source_index + len(source_name) : target_index]
    return "dominates" in between or "pareto dominates" in between or "→" in line or "->" in line


def line_has_reverse_edge(line: str, source: str, target: str) -> bool:
    normalized = normalize(line)
    source_name = normalize(source)
    target_name = normalize(target)
    target_index = normalized.find(target_name)
    source_index = normalized.find(source_name)
    if target_index < 0 or source_index < 0 or target_index >= source_index:
        return False
    between = normalized[target_index + len(target_name) : source_index]
    return "dominates" in between or "pareto dominates" in between or "→" in line or "->" in line


def validate_claims(text: str, proof: dict) -> bool:
    body = without_snapshot(text)
    lowered = normalize(body)
    if any(stale in lowered for stale in STALE_CLAIMS):
        return False

    edges = proof.get("dominance_graph", {}).get("edges", [])
    if len(edges) != 1 or len(edges[0]) != 2:
        return False
    source, target = edges[0]
    lines = [line for line in body.splitlines() if line.strip()]
    if not any(line_has_forward_edge(line, source, target) for line in lines):
        return False
    if any(line_has_reverse_edge(line, source, target) for line in lines):
        return False

    incomparable_pairs = {
        frozenset((row.get("a"), row.get("b")))
        for row in proof.get("incomparability_witnesses", [])
        if row.get("a") and row.get("b")
    }
    if frozenset(("typed-hypergraph", "many-sorted-relational")) not in incomparable_pairs:
        return False
    if not any(
        "typed hypergraph" in normalize(line)
        and "many sorted relational" in normalize(line)
        and "incomparable" in normalize(line)
        for line in lines
    ):
        return False

    return proof.get("terminal_result") == "multiple foundations remain Pareto-incomparable"


def validate_text(text: str, proof: dict, snapshot_builder: Callable[[dict], str]) -> bool:
    snapshot = snapshot_builder(proof)
    snapshot_valid = (
        text.count(snapshot) == 1
        and text.count(SNAPSHOT_START) == 1
        and text.count(SNAPSHOT_END) == 1
    )
    return snapshot_valid and validate_claims(text, proof)
