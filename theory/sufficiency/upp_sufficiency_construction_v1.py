#!/usr/bin/env python3
"""Executable RCCD sufficiency-construction model for POST-TUE-UPP-001."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable, Mapping, Tuple

class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"

COMPONENTS: Tuple[str, ...] = (
    "recoverable_commitment",
    "constrained_evolution",
    "dependency_structure",
    "semantic_interpretation",
    "historical_trace",
)

PRESERVATION_DIMENSIONS: Tuple[str, ...] = (
    "structural", "semantic", "operational", "dependency",
    "information", "historical", "registered_query_totality",
    "failure_unknown_separation",
)

ANTI_TRIVIALIZATION_CASES: Tuple[str, ...] = (
    "component_presence_without_interfaces",
    "untyped_tuple_bag",
    "final_output_only",
    "hidden_cross_component_decoder",
    "non_effective_reconstruction",
    "partial_registered_query_interface",
    "identity_collapse",
    "history_erasure",
    "dependency_erasure",
    "semantic_erasure",
    "constraint_erasure",
    "failure_unknown_collapse",
)

@dataclass(frozen=True, slots=True)
class RCCDPackage:
    components: FrozenSet[str]
    typed_interfaces: FrozenSet[str]
    effective_assembly: bool
    closed_machinery: bool
    total_registered_queries: bool
    stable_identity: bool
    equivalence_invariant: bool
    round_trip_reconstruction: bool
    failure_unknown_separated: bool
    preservation: Mapping[str, bool | None]

@dataclass(frozen=True, slots=True)
class Assessment:
    verdict: Verdict
    defects: Tuple[str, ...]
    unresolved: Tuple[str, ...]


def assess(package: RCCDPackage) -> Assessment:
    defects: list[str] = []
    unresolved: list[str] = []
    missing_components = sorted(set(COMPONENTS) - set(package.components))
    if missing_components:
        defects.append("missing_components:" + ",".join(missing_components))
    required_interfaces = {
        "commitment_query", "transition_admissibility", "dependency_query",
        "interpretation_query", "history_query", "assembly", "reconstruction",
    }
    missing_interfaces = sorted(required_interfaces - set(package.typed_interfaces))
    if missing_interfaces:
        defects.append("missing_interfaces:" + ",".join(missing_interfaces))
    for name, value in (
        ("effective_assembly", package.effective_assembly),
        ("closed_machinery", package.closed_machinery),
        ("total_registered_queries", package.total_registered_queries),
        ("stable_identity", package.stable_identity),
        ("equivalence_invariant", package.equivalence_invariant),
        ("round_trip_reconstruction", package.round_trip_reconstruction),
        ("failure_unknown_separated", package.failure_unknown_separated),
    ):
        if not value:
            defects.append(name)
    for dimension in PRESERVATION_DIMENSIONS:
        value = package.preservation.get(dimension)
        if value is False:
            defects.append("preservation:" + dimension)
        elif value is None:
            unresolved.append("preservation:" + dimension)
    if defects:
        return Assessment(Verdict.REFUTED, tuple(defects), tuple(unresolved))
    if unresolved:
        return Assessment(Verdict.UNKNOWN, (), tuple(unresolved))
    return Assessment(Verdict.PROVED, (), ())


def canonical_package() -> RCCDPackage:
    return RCCDPackage(
        components=frozenset(COMPONENTS),
        typed_interfaces=frozenset({
            "commitment_query", "transition_admissibility", "dependency_query",
            "interpretation_query", "history_query", "assembly", "reconstruction",
        }),
        effective_assembly=True,
        closed_machinery=True,
        total_registered_queries=True,
        stable_identity=True,
        equivalence_invariant=True,
        round_trip_reconstruction=True,
        failure_unknown_separated=True,
        preservation={dimension: True for dimension in PRESERVATION_DIMENSIONS},
    )


def theorem_holds(package: RCCDPackage) -> bool:
    return assess(package).verdict is Verdict.PROVED

if __name__ == "__main__":
    result = assess(canonical_package())
    print(result.verdict.value)
    raise SystemExit(0 if result.verdict is Verdict.PROVED else 1)
