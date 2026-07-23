"""Executable model for UPP-W11 historical-trace necessity.

The model is deliberately three-valued.  A theorem is proved only when every
registered premise and every witness obligation is positively established.
Any false obligation refutes the candidate; unresolved evidence remains
Unknown and is never promoted to success.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Iterable


class Evidence(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


class EventKind(str, Enum):
    ASSERT = "assert"
    DENY = "deny"
    DERIVE = "derive"
    REVISE = "revise"
    RETRACT = "retract"
    REPLACE = "replace"
    ACCEPT = "accept"
    REJECT = "reject"
    QUERY = "query"
    ANSWER = "answer"
    FAILURE = "failure"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class TraceEvent:
    event_id: str
    kind: EventKind
    time_index: int
    subject_id: str
    predecessor_ids: FrozenSet[str] = frozenset()
    dependency_ids: FrozenSet[str] = frozenset()
    reason_ids: FrozenSet[str] = frozenset()
    supersedes_ids: FrozenSet[str] = frozenset()

    def structurally_valid(self) -> bool:
        return bool(self.event_id and self.subject_id) and self.time_index >= 0


@dataclass(frozen=True, slots=True)
class HistoricalTraceWitness:
    events: tuple[TraceEvent, ...]
    effective_recovery: Evidence
    event_identity_stable: Evidence
    temporal_order_total_for_registered_events: Evidence
    predecessor_links_complete: Evidence
    dependency_lineage_complete: Evidence
    revision_lineage_complete: Evidence
    reasons_recoverable: Evidence
    rollback_or_replay_fidelity: Evidence
    equivalence_invariant: Evidence
    machinery_fully_accounted: Evidence
    registered_queries_total: Evidence
    failure_unknown_separated: Evidence

    def event_ids_unique(self) -> bool:
        ids = [event.event_id for event in self.events]
        return len(ids) == len(set(ids))

    def references_resolve(self) -> bool:
        ids = {event.event_id for event in self.events}
        for event in self.events:
            refs = (
                event.predecessor_ids
                | event.dependency_ids
                | event.reason_ids
                | event.supersedes_ids
            )
            if not refs.issubset(ids):
                return False
        return True

    def temporal_edges_forward(self) -> bool:
        by_id = {event.event_id: event for event in self.events}
        for event in self.events:
            for predecessor in event.predecessor_ids | event.supersedes_ids:
                if by_id[predecessor].time_index >= event.time_index:
                    return False
        return True

    def has_nontrivial_history(self) -> bool:
        if len(self.events) < 2:
            return False
        return any(
            event.predecessor_ids
            or event.dependency_ids
            or event.supersedes_ids
            or event.kind in {EventKind.REVISE, EventKind.RETRACT, EventKind.REPLACE}
            for event in self.events
        )

    def obligations(self) -> tuple[Evidence, ...]:
        structural = Evidence.TRUE if (
            self.events
            and all(event.structurally_valid() for event in self.events)
            and self.event_ids_unique()
            and self.references_resolve()
            and self.temporal_edges_forward()
            and self.has_nontrivial_history()
        ) else Evidence.FALSE
        return (
            structural,
            self.effective_recovery,
            self.event_identity_stable,
            self.temporal_order_total_for_registered_events,
            self.predecessor_links_complete,
            self.dependency_lineage_complete,
            self.revision_lineage_complete,
            self.reasons_recoverable,
            self.rollback_or_replay_fidelity,
            self.equivalence_invariant,
            self.machinery_fully_accounted,
            self.registered_queries_total,
            self.failure_unknown_separated,
        )


@dataclass(frozen=True, slots=True)
class HistoricalTraceTheoremCase:
    target_class_member: Evidence
    admissible_representation: Evidence
    machinery_closed: Evidence
    fully_faithful: Evidence
    commitment_equivalence_preserved: Evidence
    history_sensitive_behavior: Evidence
    registered_history_queries_total: Evidence
    witness: HistoricalTraceWitness

    def antecedent(self) -> tuple[Evidence, ...]:
        return (
            self.target_class_member,
            self.admissible_representation,
            self.machinery_closed,
            self.fully_faithful,
            self.commitment_equivalence_preserved,
            self.history_sensitive_behavior,
            self.registered_history_queries_total,
        )

    def evaluate(self) -> Verdict:
        evidence = self.antecedent() + self.witness.obligations()
        if Evidence.FALSE in evidence:
            return Verdict.REFUTED
        if Evidence.UNKNOWN in evidence:
            return Verdict.UNKNOWN
        return Verdict.PROVED


def aggregate(values: Iterable[Evidence]) -> Verdict:
    values = tuple(values)
    if Evidence.FALSE in values:
        return Verdict.REFUTED
    if Evidence.UNKNOWN in values:
        return Verdict.UNKNOWN
    return Verdict.PROVED


FROZEN_ANTECEDENT_IDS = (
    "target_class_membership",
    "representation_admissibility",
    "machinery_closure",
    "full_faithfulness",
    "commitment_equivalence_preservation",
    "history_sensitive_behavior",
    "registered_history_query_totality",
)

FROZEN_WITNESS_OBLIGATION_IDS = (
    "nontrivial_structurally_valid_trace",
    "effective_recovery",
    "stable_event_identity",
    "registered_temporal_order_totality",
    "complete_predecessor_links",
    "complete_dependency_lineage",
    "complete_revision_lineage",
    "recoverable_reasons",
    "rollback_or_replay_fidelity",
    "equivalence_invariance",
    "complete_machinery_accounting",
    "registered_query_totality",
    "failure_unknown_separation",
)

ANTI_TRIVIALIZATION_CASES = (
    "final_snapshot_only",
    "timestamped_log_without_identity",
    "unordered_event_bag",
    "history_reconstructed_post_hoc",
    "revision_without_supersession_lineage",
    "hidden_external_audit_log",
    "rollback_that_changes_commitments",
    "unknown_history_answer_collapsed_to_absence",
)
