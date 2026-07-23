from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class Verdict(str, Enum):
    ADMISSIBLE = "admissible"
    INADMISSIBLE = "inadmissible"
    UNKNOWN = "unknown"


class EncodingFamily(str, Enum):
    SYMBOLIC = "symbolic"
    GRAPH = "graph"
    RELATIONAL = "relational"
    FUNCTIONAL = "functional"
    DISTRIBUTED = "distributed"
    PROBABILISTIC = "probabilistic"
    LEARNED = "learned"
    HYBRID = "hybrid"


class SupportKind(str, Enum):
    DECODER = "decoder"
    INTERPRETER = "interpreter"
    SCHEDULER = "scheduler"
    QUERY_INTERFACE = "query_interface"
    CODEBOOK = "codebook"
    EXTERNAL_STORE = "external_store"
    ORACLE = "oracle"
    PROOF_OBJECT = "proof_object"


@dataclass(frozen=True, slots=True)
class RepresentationCandidate:
    identifier: str
    family: EncodingFamily
    finite_description: bool | None
    effective_construction: bool | None
    effective_use: bool | None
    support_inventory_complete: bool | None
    declared_support: FrozenSet[SupportKind] = frozenset()
    total_registered_query_interface: bool | None = None
    stable_identity_conditions: bool | None = None

    def validate(self) -> None:
        if not self.identifier.strip():
            raise ValueError("identifier is required")
        if SupportKind.ORACLE in self.declared_support and self.effective_use is True:
            raise ValueError("an oracle cannot be treated as effective without a separately effective realization")


def classify(candidate: RepresentationCandidate) -> Verdict:
    candidate.validate()
    required = (
        candidate.finite_description,
        candidate.effective_construction,
        candidate.effective_use,
        candidate.support_inventory_complete,
        candidate.total_registered_query_interface,
        candidate.stable_identity_conditions,
    )
    if any(value is False for value in required):
        return Verdict.INADMISSIBLE
    if any(value is None for value in required):
        return Verdict.UNKNOWN
    return Verdict.ADMISSIBLE


def is_medium_invariant(a: RepresentationCandidate, b: RepresentationCandidate) -> bool:
    """Medium differs, admissibility commitments do not."""
    return (
        a.identifier != b.identifier
        and a.family != b.family
        and classify(a) == classify(b)
        and a.finite_description == b.finite_description
        and a.effective_construction == b.effective_construction
        and a.effective_use == b.effective_use
        and a.support_inventory_complete == b.support_inventory_complete
        and a.total_registered_query_interface == b.total_registered_query_interface
        and a.stable_identity_conditions == b.stable_identity_conditions
    )


FORBIDDEN_KERNEL_TERMS = frozenset({
    "rccd", "recoverable commitments", "constrained evolution",
    "dependency-sensitive revision", "historical identity",
    "uniform effective recovery",
})


def text_is_kernel_neutral(text: str) -> bool:
    lowered = text.casefold()
    return all(term not in lowered for term in FORBIDDEN_KERNEL_TERMS)
