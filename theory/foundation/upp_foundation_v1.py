from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Mapping, Optional, Tuple


Identifier = str
TimeIndex = int


class AssumptionKind(str, Enum):
    DEFINITIONAL = "definitional"
    LOGICAL = "logical"
    COMPUTATIONAL = "computational"
    NORMATIVE = "normative"
    EMPIRICAL = "empirical"
    METHODOLOGICAL = "methodological"


class TransitionStatus(str, Enum):
    ADMISSIBLE = "admissible"
    INADMISSIBLE = "inadmissible"
    UNDETERMINED = "undetermined"


class RecoveryStatus(str, Enum):
    RECOVERED = "recovered"
    NOT_RECOVERED = "not_recovered"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Commitment:
    id: Identifier
    content_key: Identifier
    bearer: Identifier
    introduced_at: TimeIndex

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id or not self.content_key or not self.bearer:
            errors.append("commitment identifiers must be non-empty")
        if self.introduced_at < 0:
            errors.append("introduced_at must be non-negative")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class Dependency:
    source: Identifier
    target: Identifier
    kind: Identifier
    active_from: TimeIndex
    active_until: Optional[TimeIndex] = None

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.source or not self.target or not self.kind:
            errors.append("dependency identifiers must be non-empty")
        if self.active_from < 0:
            errors.append("active_from must be non-negative")
        if self.active_until is not None and self.active_until < self.active_from:
            errors.append("active_until precedes active_from")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ReasoningFact:
    id: Identifier
    fact_type: Identifier
    payload_key: Identifier
    time_index: Optional[TimeIndex]
    revision_relevant: bool

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id or not self.fact_type or not self.payload_key:
            errors.append("reasoning-fact identifiers must be non-empty")
        if self.time_index is not None and self.time_index < 0:
            errors.append("time_index must be non-negative")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class State:
    id: Identifier
    time_index: TimeIndex
    commitments: FrozenSet[Identifier]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id:
            errors.append("state id must be non-empty")
        if self.time_index < 0:
            errors.append("state time_index must be non-negative")
        if any(not x for x in self.commitments):
            errors.append("commitment references must be non-empty")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class Transition:
    id: Identifier
    source_state: Identifier
    target_state: Identifier
    status: TransitionStatus
    grounds: FrozenSet[Identifier]

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id or not self.source_state or not self.target_state:
            errors.append("transition identifiers must be non-empty")
        if self.source_state == self.target_state and self.status is TransitionStatus.INADMISSIBLE:
            errors.append("an explicitly inadmissible self-transition must be represented as a rejected proposal, not an executed transition")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class HistoryEvent:
    id: Identifier
    time_index: TimeIndex
    event_type: Identifier
    before_state: Optional[Identifier]
    after_state: Optional[Identifier]
    causes: FrozenSet[Identifier]

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id or not self.event_type:
            errors.append("history-event identifiers must be non-empty")
        if self.time_index < 0:
            errors.append("history-event time_index must be non-negative")
        if self.before_state is None and self.after_state is None:
            errors.append("history event must identify a before or after state")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class Observation:
    id: Identifier
    query_key: Identifier
    result_key: Identifier
    observed_at: TimeIndex

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id or not self.query_key or not self.result_key:
            errors.append("observation identifiers must be non-empty")
        if self.observed_at < 0:
            errors.append("observed_at must be non-negative")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class RecoveryWitness:
    fact_id: Identifier
    representation_id: Identifier
    procedure_id: Identifier
    status: RecoveryStatus
    output_key: Optional[Identifier]
    finite_steps: Optional[int]

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.fact_id or not self.representation_id or not self.procedure_id:
            errors.append("recovery-witness identifiers must be non-empty")
        if self.finite_steps is not None and self.finite_steps < 0:
            errors.append("finite_steps must be non-negative")
        if self.status is RecoveryStatus.RECOVERED and self.output_key is None:
            errors.append("recovered witness requires output_key")
        return tuple(errors)


@dataclass(frozen=True, slots=True)
class ReasoningSystem:
    id: Identifier
    states: Tuple[State, ...]
    transitions: Tuple[Transition, ...]
    commitments: Tuple[Commitment, ...]
    dependencies: Tuple[Dependency, ...]
    history: Tuple[HistoryEvent, ...]
    reasoning_facts: Tuple[ReasoningFact, ...]
    observations: Tuple[Observation, ...]

    def validate(self) -> Tuple[str, ...]:
        errors = []
        if not self.id:
            errors.append("system id must be non-empty")
        collections = {
            "state": self.states,
            "transition": self.transitions,
            "commitment": self.commitments,
            "history": self.history,
            "reasoning_fact": self.reasoning_facts,
            "observation": self.observations,
        }
        ids = {}
        for kind, values in collections.items():
            for value in values:
                value_id = getattr(value, "id")
                if value_id in ids:
                    errors.append(f"duplicate id {value_id!r} across {ids[value_id]} and {kind}")
                ids[value_id] = kind
                errors.extend(value.validate())
        for dependency in self.dependencies:
            errors.extend(dependency.validate())
        state_ids = {s.id for s in self.states}
        commitment_ids = {c.id for c in self.commitments}
        fact_ids = {f.id for f in self.reasoning_facts}
        for state in self.states:
            missing = state.commitments - commitment_ids
            if missing:
                errors.append(f"state {state.id} references missing commitments {sorted(missing)}")
        for transition in self.transitions:
            if transition.source_state not in state_ids or transition.target_state not in state_ids:
                errors.append(f"transition {transition.id} references missing state")
        for event in self.history:
            if event.before_state is not None and event.before_state not in state_ids:
                errors.append(f"history event {event.id} references missing before_state")
            if event.after_state is not None and event.after_state not in state_ids:
                errors.append(f"history event {event.id} references missing after_state")
        for dependency in self.dependencies:
            if dependency.source not in commitment_ids | fact_ids or dependency.target not in commitment_ids | fact_ids:
                errors.append("dependency endpoints must reference commitments or reasoning facts")
        ordered_times = [event.time_index for event in self.history]
        if ordered_times != sorted(ordered_times):
            errors.append("history must be stored in nondecreasing time order")
        return tuple(errors)


FOUNDATION_PRIMITIVES = frozenset({
    "identifier",
    "time_index",
    "commitment",
    "state",
    "transition",
    "dependency",
    "history_event",
    "reasoning_fact",
    "observation",
    "recovery_witness",
    "reasoning_system",
})

RCCD_TERMS_PROHIBITED_IN_CLASS_DEFINITION = frozenset({
    "R1", "R2", "R3", "R4", "R5", "RCCD",
    "recoverable commitments", "constrained evolution",
    "dependency-sensitive revision", "historical identity",
    "uniform effective recovery",
})
