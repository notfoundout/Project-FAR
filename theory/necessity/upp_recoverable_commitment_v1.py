from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Mapping, Tuple


class Verdict(str, Enum):
    PROVED = "proved"
    REFUTED = "refuted"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class CommitmentWitness:
    commitment_ids: FrozenSet[str]
    query_to_commitment: Mapping[str, str]
    effective: bool
    total_on_registered_queries: bool
    stable_under_equivalence: bool
    distinguishes_failure_unknown: bool


@dataclass(frozen=True, slots=True)
class RecoverabilityPremises:
    in_target_class: bool | None
    representation_admissible: bool | None
    machinery_closed: bool | None
    full_faithfulness: bool | None
    commitment_equivalence_respected: bool | None
    witness: CommitmentWitness | None


@dataclass(frozen=True, slots=True)
class NecessityAssessment:
    verdict: Verdict
    established_obligations: Tuple[str, ...]
    failed_obligations: Tuple[str, ...]
    unresolved_obligations: Tuple[str, ...]


OBLIGATIONS = (
    "target_class_membership",
    "representation_admissibility",
    "machinery_closure",
    "full_faithfulness",
    "commitment_equivalence",
    "effective_commitment_domain",
    "registered_query_totality",
    "stable_commitment_identity",
    "failure_unknown_separation",
)


def assess_recoverable_commitment(p: RecoverabilityPremises) -> NecessityAssessment:
    raw = {
        "target_class_membership": p.in_target_class,
        "representation_admissibility": p.representation_admissible,
        "machinery_closure": p.machinery_closed,
        "full_faithfulness": p.full_faithfulness,
        "commitment_equivalence": p.commitment_equivalence_respected,
        "effective_commitment_domain": None if p.witness is None else p.witness.effective and bool(p.witness.commitment_ids),
        "registered_query_totality": None if p.witness is None else p.witness.total_on_registered_queries and all(
            q and c in p.witness.commitment_ids for q, c in p.witness.query_to_commitment.items()
        ),
        "stable_commitment_identity": None if p.witness is None else p.witness.stable_under_equivalence,
        "failure_unknown_separation": None if p.witness is None else p.witness.distinguishes_failure_unknown,
    }
    established = tuple(k for k in OBLIGATIONS if raw[k] is True)
    failed = tuple(k for k in OBLIGATIONS if raw[k] is False)
    unresolved = tuple(k for k in OBLIGATIONS if raw[k] is None)
    if failed:
        verdict = Verdict.REFUTED
    elif unresolved:
        verdict = Verdict.UNKNOWN
    else:
        verdict = Verdict.PROVED
    return NecessityAssessment(verdict, established, failed, unresolved)


def theorem_instance(p: RecoverabilityPremises) -> bool:
    """Executable theorem instance: full premises entail a recoverable commitment witness."""
    return assess_recoverable_commitment(p).verdict is Verdict.PROVED
