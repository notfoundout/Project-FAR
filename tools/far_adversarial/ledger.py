"""Noncanonical live-research ledger: targets, issues, obligations, candidates.

Nothing in this module confers canonical Acceptance or Promotion.
``READY_UNDER_INTERNAL_PROTOCOL`` is an internal research disposition under a
frozen protocol; it is not Acceptance, and it is never derived from the two
lanes agreeing with each other.

Two separations are load-bearing and are enforced structurally rather than by
convention:

- **Execution versus epistemics.** Nothing in this module can be reached from a
  round, token, time, or provider ceiling. Resource stops live in the
  orchestrator's report type and never touch a disposition.
- **Rebuttal versus adjudication.** A challenged lane can rebut an objection.
  It cannot defeat one. Only the objection's owner may withdraw it, and only
  non-model evidence may settle it.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .safety import sha256_hex

LEDGER_SCHEMA = "far-adversarial-ledger/2"

# Bumped whenever the meaning of an event application changes. Replay refuses
# to reconstruct a run recorded under a different reducer.
REDUCER_VERSION = "far-adversarial-reducer/2"

# --- target dispositions -------------------------------------------------

OPEN = "OPEN"
NEAR_READY = "NEAR_READY"
READY_UNDER_INTERNAL_PROTOCOL = "READY_UNDER_INTERNAL_PROTOCOL"
REFUTED = "REFUTED"
BLOCKED = "BLOCKED"
UNDERDETERMINED = "UNDERDETERMINED"
SOURCE_REQUIRED = "SOURCE_REQUIRED"
FORMAL_CHECK_REQUIRED = "FORMAL_CHECK_REQUIRED"
GOVERNANCE_DECISION_REQUIRED = "GOVERNANCE_DECISION_REQUIRED"

TARGET_STATUSES = frozenset(
    {
        OPEN,
        NEAR_READY,
        READY_UNDER_INTERNAL_PROTOCOL,
        REFUTED,
        BLOCKED,
        UNDERDETERMINED,
        SOURCE_REQUIRED,
        FORMAL_CHECK_REQUIRED,
        GOVERNANCE_DECISION_REQUIRED,
    }
)

# A target stops receiving rounds only in one of these dispositions. Every one
# is epistemic: no execution failure may produce any of them.
TERMINAL_TARGET_STATUSES = frozenset(
    {
        READY_UNDER_INTERNAL_PROTOCOL,
        REFUTED,
        BLOCKED,
        UNDERDETERMINED,
        SOURCE_REQUIRED,
        FORMAL_CHECK_REQUIRED,
        GOVERNANCE_DECISION_REQUIRED,
    }
)

# Dispositions that record an established positive result. Only these satisfy a
# dependency that requires an established artifact.
ESTABLISHED_TARGET_STATUSES = frozenset({READY_UNDER_INTERNAL_PROTOCOL})

# --- evidence confidence classes ----------------------------------------

EXACT_TRANSCRIPT_EVIDENCE = "EXACT_TRANSCRIPT_EVIDENCE"
RECONSTRUCTED_RESEARCH_STATE = "RECONSTRUCTED_RESEARCH_STATE"
MISSING_TRANSCRIPT_EVIDENCE = "MISSING_TRANSCRIPT_EVIDENCE"

CONFIDENCE_CLASSES = frozenset(
    {EXACT_TRANSCRIPT_EVIDENCE, RECONSTRUCTED_RESEARCH_STATE, MISSING_TRANSCRIPT_EVIDENCE}
)

# --- issue lifecycle -----------------------------------------------------

ISSUE_OPEN = "OPEN"                       # raised, awaiting rebuttal
ISSUE_REBUTTED = "REBUTTED"               # challenged party answered, owner must review
ISSUE_SUSTAINED = "SUSTAINED"             # owner sustained after rebuttal: live disagreement
ISSUE_PARTIALLY_CONCEDED = "PARTIALLY_CONCEDED"
ISSUE_REVISED = "REVISED"                 # superseded by an owner-issued successor
ISSUE_CONCEDED = "CONCEDED"               # challenged party conceded: objection stands
ISSUE_WITHDRAWN = "WITHDRAWN"             # owner withdrew: objection defeated
ISSUE_SETTLED_DEFEATED = "SETTLED_DEFEATED"   # non-model evidence defeated it
ISSUE_SETTLED_UPHELD = "SETTLED_UPHELD"       # non-model evidence upheld it
ISSUE_SOURCE_REQUIRED = "SOURCE_REQUIRED"
ISSUE_FORMAL_REQUIRED = "FORMAL_CHECK_REQUIRED"
ISSUE_GOVERNANCE_BLOCKED = "GOVERNANCE_BLOCKED"

# Objections that are settled against the party who raised them. They stay in
# history forever and can never silently return to a live state.
DEFEATED_ISSUE_STATES = frozenset({ISSUE_WITHDRAWN, ISSUE_SETTLED_DEFEATED})

# Objections that stand against the target. These are not "resolved": they
# refute the target as formulated.
UPHELD_ISSUE_STATES = frozenset({ISSUE_CONCEDED, ISSUE_SETTLED_UPHELD})

# Objections still in play.
LIVE_ISSUE_STATES = frozenset(
    {ISSUE_OPEN, ISSUE_REBUTTED, ISSUE_SUSTAINED, ISSUE_PARTIALLY_CONCEDED, ISSUE_REVISED}
)

BLOCKING_ISSUE_STATES = frozenset(
    {ISSUE_SOURCE_REQUIRED, ISSUE_FORMAL_REQUIRED, ISSUE_GOVERNANCE_BLOCKED}
)

# --- typed actions and their legality ------------------------------------

REBUT = "REBUT"
CONCEDE = "CONCEDE"
PARTIAL_CONCEDE = "PARTIAL_CONCEDE"
SUSTAIN = "SUSTAIN"
WITHDRAW = "WITHDRAW"
REVISE = "REVISE"
COUNTEREXAMPLE = "COUNTEREXAMPLE"
REQUEST_SOURCE = "REQUEST_SOURCE"
FORMAL_CHECK_REQUIRED_ACTION = "FORMAL_CHECK_REQUIRED"
GOVERNANCE_BLOCK = "GOVERNANCE_BLOCK"
SETTLE_BY_EVIDENCE = "SETTLE_BY_EVIDENCE"

ISSUE_ACTIONS = frozenset(
    {
        REBUT,
        CONCEDE,
        PARTIAL_CONCEDE,
        SUSTAIN,
        WITHDRAW,
        REVISE,
        COUNTEREXAMPLE,
        REQUEST_SOURCE,
        FORMAL_CHECK_REQUIRED_ACTION,
        GOVERNANCE_BLOCK,
    }
)

# Actions a lane may take on an objection it raised.
OWNER_ACTIONS = frozenset(
    {SUSTAIN, WITHDRAW, REVISE, COUNTEREXAMPLE, REQUEST_SOURCE,
     FORMAL_CHECK_REQUIRED_ACTION, GOVERNANCE_BLOCK}
)

# Actions a lane may take on an objection raised against it. REBUT is the
# strongest available: a challenged lane cannot terminate the objection.
CHALLENGED_ACTIONS = frozenset(
    {REBUT, CONCEDE, PARTIAL_CONCEDE, REQUEST_SOURCE,
     FORMAL_CHECK_REQUIRED_ACTION, GOVERNANCE_BLOCK}
)

# Actors that are not analytical lanes. Only these may settle an issue, and
# only with an evidence reference.
ADJUDICATING_ACTORS = frozenset({"deterministic", "formal", "source"})

_ACTION_TO_STATE = {
    REBUT: ISSUE_REBUTTED,
    CONCEDE: ISSUE_CONCEDED,
    PARTIAL_CONCEDE: ISSUE_PARTIALLY_CONCEDED,
    SUSTAIN: ISSUE_SUSTAINED,
    WITHDRAW: ISSUE_WITHDRAWN,
    REVISE: ISSUE_REVISED,
    COUNTEREXAMPLE: ISSUE_SUSTAINED,
    REQUEST_SOURCE: ISSUE_SOURCE_REQUIRED,
    FORMAL_CHECK_REQUIRED_ACTION: ISSUE_FORMAL_REQUIRED,
    GOVERNANCE_BLOCK: ISSUE_GOVERNANCE_BLOCKED,
}

# --- obligations ---------------------------------------------------------

OBLIGATION_SOURCE = "SOURCE"
OBLIGATION_FORMAL = "FORMAL"
OBLIGATION_KINDS = frozenset({OBLIGATION_SOURCE, OBLIGATION_FORMAL})

OBLIGATION_UNRESOLVED = "UNRESOLVED"
OBLIGATION_DISCHARGED = "DISCHARGED"
OBLIGATION_WAIVED = "WAIVED_BY_GOVERNANCE"
OBLIGATION_STATES = frozenset(
    {OBLIGATION_UNRESOLVED, OBLIGATION_DISCHARGED, OBLIGATION_WAIVED}
)

_WS = re.compile(r"\s+")
_EDGE_PUNCT = re.compile(r"^[^\w]+|[^\w]+$")


def normalize_claim(text: str) -> str:
    """Deterministic normalisation used for issue and obligation identity.

    Whitespace and edge punctuation only. Semantic duplicates are never merged
    by embedding or model similarity: two objections with different wording get
    different identities and must be reconciled by an explicit recorded action.
    """
    lowered = _WS.sub(" ", text.strip().lower())
    return _EDGE_PUNCT.sub("", lowered)


def issue_id(target_id: str, claim: str) -> str:
    """Stable content-addressed issue identity."""
    digest = sha256_hex(f"{target_id}\x1f{normalize_claim(claim)}")
    return f"ISS-{digest[:12].upper()}"


def obligation_id(target_id: str, kind: str, statement: str) -> str:
    digest = sha256_hex(f"{target_id}\x1f{kind}\x1f{normalize_claim(statement)}")
    return f"OBL-{digest[:12].upper()}"


def candidate_id(target_id: str, formulation: str) -> str:
    digest = sha256_hex(f"{target_id}\x1f{normalize_claim(formulation)}")
    return f"CAND-{digest[:12].upper()}"


class IssueReopenError(RuntimeError):
    """Raised when a settled objection is pushed back toward a live state."""


class IllegalActionError(RuntimeError):
    """Raised when an actor takes an action it has no standing to take."""


@dataclass
class IssueEvent:
    at: float
    actor: str
    action: str
    rationale: str
    from_state: str
    to_state: str
    provenance: str = ""
    invocation_id: str | None = None
    agreement: dict[str, Any] = field(default_factory=dict)
    evidence_ref: str = ""


@dataclass
class Issue:
    id: str
    target_id: str
    claim: str
    raised_by: str
    state: str = ISSUE_OPEN
    confidence_class: str = RECONSTRUCTED_RESEARCH_STATE
    provenance: str = ""
    history: list[IssueEvent] = field(default_factory=list)
    superseded_by: str | None = None

    def is_live(self) -> bool:
        return self.state in LIVE_ISSUE_STATES

    def is_blocking(self) -> bool:
        return self.state in BLOCKING_ISSUE_STATES

    def is_defeated(self) -> bool:
        return self.state in DEFEATED_ISSUE_STATES

    def is_upheld(self) -> bool:
        return self.state in UPHELD_ISSUE_STATES

    def is_settled(self) -> bool:
        return self.is_defeated() or self.is_upheld()


@dataclass
class Obligation:
    """An unresolved source requirement or proof obligation.

    A first-class ledger object with its own state and resolution provenance,
    not a string in a list. An unresolved obligation blocks readiness.
    """

    id: str
    target_id: str
    kind: str
    statement: str
    raised_by: str
    provenance: str
    state: str = OBLIGATION_UNRESOLVED
    required_by_protocol: bool = True
    resolution_provenance: str = ""
    history: list[IssueEvent] = field(default_factory=list)

    def is_unresolved(self) -> bool:
        return self.state == OBLIGATION_UNRESOLVED

    def blocks_readiness(self) -> bool:
        return self.is_unresolved() and self.required_by_protocol


@dataclass
class Candidate:
    """A proposed repair of a frozen target.

    A candidate never mutates the target it repairs. A material candidate is
    materialised as a successor target with its own identity, and that
    successor requires fresh blind first passes.
    """

    id: str
    predecessor_target_id: str
    version: str
    proposed_formulation: str
    changed_propositions: list[str]
    justification: str
    issues_addressed: list[str] = field(default_factory=list)
    issues_introduced: list[str] = field(default_factory=list)
    regression_status: str = "NOT_RUN"
    formal_status: str = "NOT_RUN"
    successor_target_id: str | None = None
    state: str = "PROPOSED"
    provenance: str = ""


# How a target's current status was arrived at. A status copied out of a
# transcript is a record of what someone else concluded; a status this executor
# derived is a result of the ledger's own rules. They are not interchangeable.
STATUS_DERIVED = "DERIVED_FROM_LEDGER"
STATUS_RECORDED = "RECORDED_TRANSCRIPT_DISPOSITION"
STATUS_BASES = frozenset({STATUS_DERIVED, STATUS_RECORDED})


@dataclass
class Dependency:
    """A typed edge: which predecessor dispositions actually unlock this target.

    A bare "predecessor is terminal" edge is invalid — ``REFUTED``,
    ``SOURCE_REQUIRED``, and ``GOVERNANCE_DECISION_REQUIRED`` are terminal but
    establish nothing, and an execution stop leaves a status that establishes
    nothing either.

    ``accept_recorded`` defaults to false: a disposition transcribed from a
    research conversation does not unlock downstream execution unless an edge
    says in so many words that it may.
    """

    target_id: str
    requires: list[str] = field(default_factory=lambda: sorted(ESTABLISHED_TARGET_STATUSES))
    accept_recorded: bool = False

    def satisfied_by(self, status: str, status_basis: str = STATUS_DERIVED) -> bool:
        if status not in set(self.requires):
            return False
        if status_basis == STATUS_RECORDED and not self.accept_recorded:
            return False
        return True


@dataclass
class Target:
    id: str
    original_formulation: str
    current_formulation: str
    frozen_scope: str
    status: str = OPEN
    status_basis: str = STATUS_DERIVED
    confidence_class: str = RECONSTRUCTED_RESEARCH_STATE
    provenance: str = ""
    repository_relationship: str = ""
    depends_on: list[Dependency] = field(default_factory=list)
    authorized: bool = False
    requires_fresh_blind_pass: bool = True
    # Declared frozen-evidence paths. This is an input contract, never a place
    # to accumulate a lane's free-text source requests.
    frozen_evidence_paths: list[str] = field(default_factory=list)
    supporting_arguments: list[str] = field(default_factory=list)
    sustained_objections: list[str] = field(default_factory=list)
    upheld_objections: list[str] = field(default_factory=list)
    defeated_objections: list[str] = field(default_factory=list)
    withdrawn_objections: list[str] = field(default_factory=list)
    counterexamples: list[str] = field(default_factory=list)
    concessions: list[str] = field(default_factory=list)
    source_dependencies: list[str] = field(default_factory=list)
    formal_obligations: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def is_terminal(self) -> bool:
        return self.status in TERMINAL_TARGET_STATUSES

    def is_established(self) -> bool:
        return self.status in ESTABLISHED_TARGET_STATUSES


class Ledger:
    """The live noncanonical research state.

    Persisted as JSON so that unresolved issues survive process restarts and
    context compaction. Reloading is lossless for identity and history.
    """

    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else None
        self.targets: dict[str, Target] = {}
        self.issues: dict[str, Issue] = {}
        self.obligations: dict[str, Obligation] = {}
        self.candidates: dict[str, Candidate] = {}
        self.meta: dict[str, Any] = {"schema": LEDGER_SCHEMA, "reducer": REDUCER_VERSION}

    # -- targets ----------------------------------------------------------

    def add_target(self, target: Target) -> Target:
        if target.status not in TARGET_STATUSES:
            raise ValueError(f"unknown target status: {target.status}")
        if target.confidence_class not in CONFIDENCE_CLASSES:
            raise ValueError(f"unknown confidence class: {target.confidence_class}")
        if target.status_basis not in STATUS_BASES:
            raise ValueError(f"unknown status basis: {target.status_basis}")
        if not target.provenance:
            raise ValueError(f"target {target.id} has no provenance")
        for dependency in target.depends_on:
            unknown = set(dependency.requires) - TARGET_STATUSES
            if unknown:
                raise ValueError(f"{target.id}: unknown required disposition {unknown}")
        self.targets[target.id] = target
        return target

    def set_target_status(self, target_id: str, status: str, note: str = "",
                          basis: str = STATUS_DERIVED) -> None:
        if status not in TARGET_STATUSES:
            raise ValueError(f"unknown target status: {status}")
        if basis not in STATUS_BASES:
            raise ValueError(f"unknown status basis: {basis}")
        target = self.targets[target_id]
        target.status = status
        target.status_basis = basis
        if note:
            target.notes.append(note)

    # -- issues -----------------------------------------------------------

    def register_issue(
        self,
        *,
        target_id: str,
        claim: str,
        raised_by: str,
        provenance: str,
        confidence_class: str = RECONSTRUCTED_RESEARCH_STATE,
    ) -> Issue:
        """Register an objection, or return the existing one with that identity.

        Re-registering a settled objection does not reopen it. The identity is
        content-addressed, so resending the same text cannot smuggle a settled
        attack back into the queue.
        """
        if confidence_class not in CONFIDENCE_CLASSES:
            raise ValueError(f"unknown confidence class: {confidence_class}")
        iid = issue_id(target_id, claim)
        existing = self.issues.get(iid)
        if existing is not None:
            return existing
        issue = Issue(
            id=iid,
            target_id=target_id,
            claim=claim,
            raised_by=raised_by,
            provenance=provenance,
            confidence_class=confidence_class,
        )
        issue.history.append(
            IssueEvent(at=time.time(), actor=raised_by, action="RAISE", rationale=claim,
                       from_state="", to_state=ISSUE_OPEN, provenance=provenance)
        )
        self.issues[iid] = issue
        return issue

    def check_action_legality(self, issue: Issue, actor: str, action: str) -> None:
        """Refuse actions the actor has no standing to take.

        The asymmetry is the point. An objection belongs to the lane that
        raised it: only that lane may withdraw or sustain it. The challenged
        lane may concede or rebut, and rebutting leaves the objection live.
        """
        if action not in ISSUE_ACTIONS:
            raise ValueError(f"unknown issue action: {action}")
        if actor in ADJUDICATING_ACTORS:
            raise IllegalActionError(
                f"{actor} is an adjudicating actor and must use settle_issue()"
            )
        is_owner = actor == issue.raised_by
        permitted = OWNER_ACTIONS if is_owner else CHALLENGED_ACTIONS
        if action not in permitted:
            role = "owner" if is_owner else "challenged party"
            raise IllegalActionError(
                f"{actor} is the {role} of {issue.id} and may not {action}. "
                f"Permitted: {', '.join(sorted(permitted))}."
            )

    def apply_action(
        self,
        issue_id_: str,
        *,
        actor: str,
        action: str,
        rationale: str,
        provenance: str = "",
        invocation_id: str | None = None,
        agreement: dict[str, Any] | None = None,
        revised_claim: str | None = None,
    ) -> Issue:
        """Record a typed action against an objection.

        A concession records a model-position change; it is not itself proof of
        anything. ``agreement`` is stored as metadata and has no effect on any
        disposition computed anywhere in this module.
        """
        issue = self.issues[issue_id_]
        self.check_action_legality(issue, actor, action)
        target_state = _ACTION_TO_STATE[action]
        if issue.is_settled() and target_state not in (DEFEATED_ISSUE_STATES | UPHELD_ISSUE_STATES):
            raise IssueReopenError(
                f"{issue.id} is {issue.state}; a settled objection cannot return to "
                f"{target_state}. Raise a new, distinctly formulated objection instead."
            )
        if issue.is_settled():
            raise IssueReopenError(f"{issue.id} is already settled as {issue.state}")
        previous = issue.state
        issue.state = target_state
        if revised_claim and action == REVISE:
            successor = self.register_issue(
                target_id=issue.target_id, claim=revised_claim, raised_by=actor,
                provenance=provenance or issue.provenance,
                confidence_class=issue.confidence_class,
            )
            issue.superseded_by = successor.id
        issue.history.append(
            IssueEvent(at=time.time(), actor=actor, action=action, rationale=rationale,
                       from_state=previous, to_state=target_state, provenance=provenance,
                       invocation_id=invocation_id, agreement=dict(agreement or {}))
        )
        return issue

    def settle_issue(
        self,
        issue_id_: str,
        *,
        actor: str,
        outcome: str,
        rationale: str,
        evidence_ref: str,
        provenance: str = "",
    ) -> Issue:
        """Settle an objection on non-model evidence.

        Only a deterministic check, a formal proof, or a source citation can do
        this, and only with a reference to the evidence. No lane may call it.
        """
        if actor not in ADJUDICATING_ACTORS:
            raise IllegalActionError(
                f"{actor} may not settle an issue; only {sorted(ADJUDICATING_ACTORS)} may, "
                "and no analytical lane is an adjudicator"
            )
        if outcome not in {"DEFEATED", "UPHELD"}:
            raise ValueError(f"unknown settlement outcome: {outcome}")
        if not evidence_ref:
            raise ValueError("settlement requires an evidence reference")
        issue = self.issues[issue_id_]
        if issue.is_settled():
            raise IssueReopenError(f"{issue.id} is already settled as {issue.state}")
        previous = issue.state
        issue.state = ISSUE_SETTLED_DEFEATED if outcome == "DEFEATED" else ISSUE_SETTLED_UPHELD
        issue.history.append(
            IssueEvent(at=time.time(), actor=actor, action=SETTLE_BY_EVIDENCE,
                       rationale=rationale, from_state=previous, to_state=issue.state,
                       provenance=provenance, evidence_ref=evidence_ref)
        )
        return issue

    def issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues.values() if i.target_id == target_id]

    def live_issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues_for(target_id) if i.is_live()]

    def blocking_issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues_for(target_id) if i.is_blocking()]

    # -- obligations ------------------------------------------------------

    def register_obligation(
        self,
        *,
        target_id: str,
        kind: str,
        statement: str,
        raised_by: str,
        provenance: str,
        required_by_protocol: bool = True,
    ) -> Obligation:
        if kind not in OBLIGATION_KINDS:
            raise ValueError(f"unknown obligation kind: {kind}")
        oid = obligation_id(target_id, kind, statement)
        existing = self.obligations.get(oid)
        if existing is not None:
            return existing
        obligation = Obligation(
            id=oid, target_id=target_id, kind=kind, statement=statement,
            raised_by=raised_by, provenance=provenance,
            required_by_protocol=required_by_protocol,
        )
        obligation.history.append(
            IssueEvent(at=time.time(), actor=raised_by, action="RAISE", rationale=statement,
                       from_state="", to_state=OBLIGATION_UNRESOLVED, provenance=provenance)
        )
        self.obligations[oid] = obligation
        return obligation

    def resolve_obligation(self, obligation_id_: str, *, actor: str, state: str,
                           resolution_provenance: str, rationale: str = "") -> Obligation:
        """Discharge or waive an obligation, with mandatory provenance.

        A lane cannot discharge its own obligation by asserting it is fine:
        discharge requires an adjudicating actor and a provenance reference.
        """
        if state not in {OBLIGATION_DISCHARGED, OBLIGATION_WAIVED}:
            raise ValueError(f"cannot set obligation to {state}")
        if actor not in ADJUDICATING_ACTORS and state == OBLIGATION_DISCHARGED:
            raise IllegalActionError(
                f"{actor} may not discharge an obligation; discharge requires "
                f"one of {sorted(ADJUDICATING_ACTORS)}"
            )
        if not resolution_provenance:
            raise ValueError("obligation resolution requires provenance")
        obligation = self.obligations[obligation_id_]
        previous = obligation.state
        obligation.state = state
        obligation.resolution_provenance = resolution_provenance
        obligation.history.append(
            IssueEvent(at=time.time(), actor=actor, action=state, rationale=rationale,
                       from_state=previous, to_state=state,
                       provenance=resolution_provenance)
        )
        return obligation

    def obligations_for(self, target_id: str) -> list[Obligation]:
        return [o for o in self.obligations.values() if o.target_id == target_id]

    def blocking_obligations_for(self, target_id: str) -> list[Obligation]:
        return [o for o in self.obligations_for(target_id) if o.blocks_readiness()]

    # -- candidates -------------------------------------------------------

    def propose_candidate(
        self,
        *,
        predecessor_target_id: str,
        proposed_formulation: str,
        changed_propositions: list[str],
        justification: str,
        provenance: str,
        issues_addressed: list[str] | None = None,
        version: str | None = None,
    ) -> Candidate:
        predecessor = self.targets[predecessor_target_id]
        cid = candidate_id(predecessor_target_id, proposed_formulation)
        if cid in self.candidates:
            return self.candidates[cid]
        existing_versions = sum(
            1 for c in self.candidates.values()
            if c.predecessor_target_id == predecessor_target_id
        )
        candidate = Candidate(
            id=cid,
            predecessor_target_id=predecessor_target_id,
            version=version or f"v{existing_versions + 2}",
            proposed_formulation=proposed_formulation,
            changed_propositions=list(changed_propositions),
            justification=justification,
            issues_addressed=list(issues_addressed or []),
            provenance=provenance,
        )
        self.candidates[cid] = candidate
        # The frozen predecessor is never edited in place.
        assert self.targets[predecessor_target_id] is predecessor
        return candidate

    def materialize_successor(self, candidate_id_: str, *,
                              successor_id: str | None = None) -> Target:
        """Turn a candidate into a successor target with its own identity.

        The predecessor keeps its formulation and its issue history unchanged.
        The successor requires fresh blind first passes: it is a new frozen
        target, not a continuation of the old one's audit.
        """
        candidate = self.candidates[candidate_id_]
        predecessor = self.targets[candidate.predecessor_target_id]
        before = predecessor.current_formulation
        new_id = successor_id or f"{predecessor.id}-{candidate.version}"
        successor = Target(
            id=new_id,
            original_formulation=candidate.proposed_formulation,
            current_formulation=candidate.proposed_formulation,
            frozen_scope=predecessor.frozen_scope,
            status=OPEN,
            confidence_class=predecessor.confidence_class,
            provenance=f"candidate:{candidate.id} of {predecessor.id}; {candidate.provenance}",
            repository_relationship=predecessor.repository_relationship,
            depends_on=list(predecessor.depends_on),
            authorized=predecessor.authorized,
            requires_fresh_blind_pass=True,
            frozen_evidence_paths=list(predecessor.frozen_evidence_paths),
        )
        self.add_target(successor)
        candidate.successor_target_id = new_id
        candidate.state = "PROMOTED_TO_SUCCESSOR"
        if predecessor.current_formulation != before:
            raise RuntimeError("predecessor formulation mutated during materialisation")
        return successor

    # -- dispositions -----------------------------------------------------

    def evaluate_target(self, target_id: str) -> str:
        """Derive a target disposition from surviving objections and obligations.

        Model agreement is deliberately not an input. READY requires that no
        registered material objection survives, that no required obligation is
        unresolved, and that at least one objection was actually adjudicated —
        a target nobody ever attacked is untested, not ready.
        """
        target = self.targets[target_id]
        issues = self.issues_for(target_id)
        if any(i.is_upheld() for i in issues):
            return REFUTED
        blocking = [i for i in issues if i.is_blocking()]
        obligations = self.blocking_obligations_for(target_id)
        states = {i.state for i in blocking}
        if ISSUE_GOVERNANCE_BLOCKED in states:
            return GOVERNANCE_DECISION_REQUIRED
        if ISSUE_SOURCE_REQUIRED in states or any(
            o.kind == OBLIGATION_SOURCE for o in obligations
        ):
            return SOURCE_REQUIRED
        if ISSUE_FORMAL_REQUIRED in states or any(
            o.kind == OBLIGATION_FORMAL for o in obligations
        ):
            return FORMAL_CHECK_REQUIRED
        live = [i for i in issues if i.is_live()]
        if live:
            return NEAR_READY if len(live) == 1 else OPEN
        if not issues:
            return OPEN
        if target.missing_evidence:
            return SOURCE_REQUIRED
        return READY_UNDER_INTERNAL_PROTOCOL

    def dependency_report(self, target_id: str) -> list[tuple[Dependency, str, bool]]:
        """(dependency, predecessor status, satisfied) for each declared edge."""
        out: list[tuple[Dependency, str, bool]] = []
        for dependency in self.targets[target_id].depends_on:
            predecessor = self.targets.get(dependency.target_id)
            status = predecessor.status if predecessor else "MISSING"
            satisfied = bool(predecessor) and dependency.satisfied_by(
                status, predecessor.status_basis
            )
            out.append((dependency, status, satisfied))
        return out

    def dependencies_satisfied(self, target_id: str) -> bool:
        return all(ok for _, _, ok in self.dependency_report(target_id))

    def next_target(self) -> Target | None:
        """Shortest dependency-valid next step.

        Eligible means: non-terminal, explicitly authorized, and every declared
        dependency satisfied by a predecessor disposition that edge actually
        accepts. Selection order is deterministic by target id.
        """
        for target in sorted(self.targets.values(), key=lambda t: t.id):
            if target.is_terminal() or not target.authorized:
                continue
            if self.dependencies_satisfied(target.id):
                return target
        return None

    def select_target(self, target_id: str) -> Target:
        """Explicit selection, refused for unauthorized or unsatisfied targets."""
        target = self.targets[target_id]
        if not target.authorized:
            raise PermissionError(
                f"{target_id} is not authorized for execution under current governance"
            )
        unmet = [
            f"{dep.target_id} is {status}"
            f"{'' if dep.accept_recorded else ' (recorded dispositions do not unlock)'}"
            f", requires one of {sorted(dep.requires)}"
            for dep, status, ok in self.dependency_report(target_id)
            if not ok
        ]
        if unmet:
            raise PermissionError(f"{target_id} has unmet dependencies: {'; '.join(unmet)}")
        return target

    # -- persistence ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "meta": self.meta,
            "targets": {k: asdict(v) for k, v in sorted(self.targets.items())},
            "issues": {k: asdict(v) for k, v in sorted(self.issues.items())},
            "obligations": {k: asdict(v) for k, v in sorted(self.obligations.items())},
            "candidates": {k: asdict(v) for k, v in sorted(self.candidates.items())},
        }

    def save(self, path: Path | None = None) -> Path:
        destination = Path(path or self.path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return destination

    @classmethod
    def load(cls, path: Path) -> "Ledger":
        ledger = cls(path)
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        ledger.meta = data.get("meta", {"schema": LEDGER_SCHEMA})
        schema = ledger.meta.get("schema")
        if schema != LEDGER_SCHEMA:
            raise ValueError(
                f"ledger schema {schema!r} is not {LEDGER_SCHEMA!r}; migrate explicitly"
            )
        for tid, raw in data.get("targets", {}).items():
            deps = [Dependency(**d) for d in raw.pop("depends_on", [])]
            target = Target(**raw)
            target.depends_on = deps
            ledger.targets[tid] = target
        for iid, raw in data.get("issues", {}).items():
            history = [IssueEvent(**event) for event in raw.pop("history", [])]
            issue = Issue(**raw)
            issue.history = history
            ledger.issues[iid] = issue
        for oid, raw in data.get("obligations", {}).items():
            history = [IssueEvent(**event) for event in raw.pop("history", [])]
            obligation = Obligation(**raw)
            obligation.history = history
            ledger.obligations[oid] = obligation
        for cid, raw in data.get("candidates", {}).items():
            ledger.candidates[cid] = Candidate(**raw)
        return ledger

    # -- digests ----------------------------------------------------------

    _VOLATILE_FIELDS = ("at",)

    def _canonical_state(self) -> dict[str, Any]:
        """State with wall-clock fields stripped.

        Replay must reproduce a digest computed on a different day, so
        timestamps cannot participate in it. Everything semantic does.
        """
        def strip(obj):
            if isinstance(obj, dict):
                return {k: strip(v) for k, v in obj.items()
                        if k not in self._VOLATILE_FIELDS}
            if isinstance(obj, list):
                return [strip(v) for v in obj]
            return obj

        return strip(self.to_dict())

    def digest(self) -> str:
        """Content digest of the semantic state, stable across runs."""
        return sha256_hex(json.dumps(self._canonical_state(), sort_keys=True,
                                     ensure_ascii=False))
