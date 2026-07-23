from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Mapping, Sequence, Tuple


class Verdict(str, Enum):
    EQUIVALENT = "equivalent"
    NON_EQUIVALENT = "non_equivalent"
    UNKNOWN = "unknown"


class Dimension(str, Enum):
    STRUCTURE = "structure"
    SEMANTICS = "semantics"
    OPERATION = "operation"
    DEPENDENCY = "dependency"
    INFORMATION = "information"
    HISTORY = "history"
    QUERY = "query"
    ERROR = "error"
    IDENTITY = "identity"
    MACHINERY = "machinery"


ALL_DIMENSIONS: FrozenSet[Dimension] = frozenset(Dimension)


@dataclass(frozen=True, slots=True)
class ClosedPackage:
    package_id: str
    facts: FrozenSet[str]
    transitions: FrozenSet[Tuple[str, str, str]]
    dependencies: FrozenSet[Tuple[str, str, str]]
    histories: FrozenSet[Tuple[str, ...]]
    query_answers: Mapping[str, str]
    error_answers: Mapping[str, str]
    identity_classes: FrozenSet[FrozenSet[str]]
    machinery: FrozenSet[str]

    def validate(self) -> Tuple[str, ...]:
        errors: list[str] = []
        if not self.package_id:
            errors.append("package_id_empty")
        if any(not fact for fact in self.facts):
            errors.append("empty_fact")
        if any(len(t) != 3 or not all(t) for t in self.transitions):
            errors.append("invalid_transition")
        if any(len(d) != 3 or not all(d) for d in self.dependencies):
            errors.append("invalid_dependency")
        if any(not h or not all(h) for h in self.histories):
            errors.append("invalid_history")
        if any(not q or not a for q, a in self.query_answers.items()):
            errors.append("invalid_query_answer")
        if any(not q or not a for q, a in self.error_answers.items()):
            errors.append("invalid_error_answer")
        if any(not c or not all(c) for c in self.identity_classes):
            errors.append("invalid_identity_class")
        if any(not m for m in self.machinery):
            errors.append("invalid_machinery")
        return tuple(sorted(set(errors)))


@dataclass(frozen=True, slots=True)
class Correspondence:
    source_package: str
    target_package: str
    fact_map: Mapping[str, str]
    state_map: Mapping[str, str]
    relation_map: Mapping[str, str]
    query_map: Mapping[str, str]
    machinery_map: Mapping[str, str]
    total_claimed: bool
    effective_claimed: bool

    def validate(self) -> Tuple[str, ...]:
        errors: list[str] = []
        if not self.source_package or not self.target_package:
            errors.append("package_reference_empty")
        for name, mapping in (
            ("fact_map", self.fact_map),
            ("state_map", self.state_map),
            ("relation_map", self.relation_map),
            ("query_map", self.query_map),
            ("machinery_map", self.machinery_map),
        ):
            if any(not k or not v for k, v in mapping.items()):
                errors.append(f"{name}_invalid")
            if len(set(mapping.values())) != len(mapping.values()):
                errors.append(f"{name}_noninjective")
        return tuple(sorted(set(errors)))


@dataclass(frozen=True, slots=True)
class Evidence:
    checked_dimensions: FrozenSet[Dimension]
    unresolved_dimensions: FrozenSet[Dimension] = frozenset()

    def validate(self) -> Tuple[str, ...]:
        errors: list[str] = []
        if self.checked_dimensions & self.unresolved_dimensions:
            errors.append("dimension_both_checked_and_unresolved")
        if not self.checked_dimensions | self.unresolved_dimensions:
            errors.append("no_dimensions_addressed")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class EquivalenceAssessment:
    verdict: Verdict
    failures: Tuple[str, ...]
    unresolved: Tuple[str, ...]
    checked_dimensions: FrozenSet[Dimension]


def _map_tuple(values: Sequence[str], mapping: Mapping[str, str]) -> Tuple[str, ...] | None:
    out: list[str] = []
    for value in values:
        if value not in mapping:
            return None
        out.append(mapping[value])
    return tuple(out)


def _mapped_set(values: FrozenSet[str], mapping: Mapping[str, str]) -> FrozenSet[str] | None:
    if not values.issubset(mapping):
        return None
    return frozenset(mapping[v] for v in values)


def _preservation_failures(
    source: ClosedPackage,
    target: ClosedPackage,
    corr: Correspondence,
) -> Tuple[str, ...]:
    failures: list[str] = []

    mapped_facts = _mapped_set(source.facts, corr.fact_map)
    if mapped_facts is None or mapped_facts != target.facts:
        failures.append("fact_bijection_failure")

    mapped_transitions = set()
    for pre, relation, post in source.transitions:
        mapped = _map_tuple((pre, relation, post), {**corr.state_map, **corr.relation_map})
        if mapped is None:
            failures.append("transition_map_partial")
            break
        mapped_transitions.add(mapped)
    if frozenset(mapped_transitions) != target.transitions:
        failures.append("transition_preservation_failure")

    mapped_dependencies = set()
    for dependent, relation, support in source.dependencies:
        merged = {**corr.fact_map, **corr.relation_map}
        mapped = _map_tuple((dependent, relation, support), merged)
        if mapped is None:
            failures.append("dependency_map_partial")
            break
        mapped_dependencies.add(mapped)
    if frozenset(mapped_dependencies) != target.dependencies:
        failures.append("dependency_preservation_failure")

    mapped_histories = set()
    for history in source.histories:
        mapped = _map_tuple(history, corr.state_map)
        if mapped is None:
            failures.append("history_map_partial")
            break
        mapped_histories.add(mapped)
    if frozenset(mapped_histories) != target.histories:
        failures.append("history_preservation_failure")

    mapped_queries: dict[str, str] = {}
    for query, answer in source.query_answers.items():
        if query not in corr.query_map or answer not in corr.fact_map:
            failures.append("query_map_partial")
            break
        mapped_queries[corr.query_map[query]] = corr.fact_map[answer]
    if mapped_queries != dict(target.query_answers):
        failures.append("query_preservation_failure")

    mapped_errors: dict[str, str] = {}
    for query, answer in source.error_answers.items():
        if query not in corr.query_map:
            failures.append("error_query_map_partial")
            break
        mapped_errors[corr.query_map[query]] = answer
    if mapped_errors != dict(target.error_answers):
        failures.append("error_unknown_preservation_failure")

    mapped_identity = set()
    for identity_class in source.identity_classes:
        mapped = _mapped_set(identity_class, corr.state_map)
        if mapped is None:
            failures.append("identity_map_partial")
            break
        mapped_identity.add(mapped)
    if frozenset(mapped_identity) != target.identity_classes:
        failures.append("identity_preservation_failure")

    mapped_machinery = _mapped_set(source.machinery, corr.machinery_map)
    if mapped_machinery is None or mapped_machinery != target.machinery:
        failures.append("machinery_preservation_failure")

    return tuple(sorted(set(failures)))


def assess_equivalence(
    left: ClosedPackage,
    right: ClosedPackage,
    left_to_right: Correspondence,
    right_to_left: Correspondence,
    evidence: Evidence,
) -> EquivalenceAssessment:
    failures: list[str] = []
    unresolved: list[str] = []

    failures.extend(left.validate())
    failures.extend(right.validate())
    failures.extend(left_to_right.validate())
    failures.extend(right_to_left.validate())
    failures.extend(evidence.validate())

    if left_to_right.source_package != left.package_id or left_to_right.target_package != right.package_id:
        failures.append("left_to_right_endpoint_mismatch")
    if right_to_left.source_package != right.package_id or right_to_left.target_package != left.package_id:
        failures.append("right_to_left_endpoint_mismatch")

    if not left_to_right.total_claimed or not right_to_left.total_claimed:
        unresolved.append("totality_not_established")
    if not left_to_right.effective_claimed or not right_to_left.effective_claimed:
        unresolved.append("effectivity_not_established")

    failures.extend(_preservation_failures(left, right, left_to_right))
    failures.extend(_preservation_failures(right, left, right_to_left))

    for name, forward, backward, domain in (
        ("fact", left_to_right.fact_map, right_to_left.fact_map, left.facts),
        ("state", left_to_right.state_map, right_to_left.state_map, frozenset(s for h in left.histories for s in h)),
        ("relation", left_to_right.relation_map, right_to_left.relation_map, frozenset(r for _, r, _ in left.transitions | left.dependencies)),
        ("query", left_to_right.query_map, right_to_left.query_map, frozenset(left.query_answers) | frozenset(left.error_answers)),
        ("machinery", left_to_right.machinery_map, right_to_left.machinery_map, left.machinery),
    ):
        for item in domain:
            if item not in forward or forward[item] not in backward or backward[forward[item]] != item:
                failures.append(f"{name}_round_trip_failure")
                break

    missing = ALL_DIMENSIONS - evidence.checked_dimensions - evidence.unresolved_dimensions
    if missing:
        unresolved.append("unaddressed_dimensions:" + ",".join(sorted(d.value for d in missing)))
    if evidence.unresolved_dimensions:
        unresolved.append("unresolved_dimensions:" + ",".join(sorted(d.value for d in evidence.unresolved_dimensions)))

    failures = sorted(set(failures))
    unresolved = sorted(set(unresolved))
    if failures:
        verdict = Verdict.NON_EQUIVALENT
    elif unresolved:
        verdict = Verdict.UNKNOWN
    else:
        verdict = Verdict.EQUIVALENT
    return EquivalenceAssessment(verdict, tuple(failures), tuple(unresolved), evidence.checked_dimensions)


def commitment_equivalent(*args: object, **kwargs: object) -> bool:
    return assess_equivalence(*args, **kwargs).verdict is Verdict.EQUIVALENT
