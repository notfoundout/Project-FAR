"""Noncanonical live-research ledger: targets, issues, and immutable history.

Nothing in this module confers canonical Acceptance or Promotion.
``READY_UNDER_INTERNAL_PROTOCOL`` is an internal research disposition under a
frozen protocol; it is not Acceptance, and it is never derived from the two
lanes agreeing with each other.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .safety import sha256_hex

LEDGER_SCHEMA = "far-adversarial-ledger/1"

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
# of them is epistemic: no execution failure may produce any of them.
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

# --- evidence confidence classes ----------------------------------------

EXACT_TRANSCRIPT_EVIDENCE = "EXACT_TRANSCRIPT_EVIDENCE"
RECONSTRUCTED_RESEARCH_STATE = "RECONSTRUCTED_RESEARCH_STATE"
MISSING_TRANSCRIPT_EVIDENCE = "MISSING_TRANSCRIPT_EVIDENCE"

CONFIDENCE_CLASSES = frozenset(
    {EXACT_TRANSCRIPT_EVIDENCE, RECONSTRUCTED_RESEARCH_STATE, MISSING_TRANSCRIPT_EVIDENCE}
)

# --- issue actions and states -------------------------------------------

SUSTAIN = "SUSTAIN"
REJECT = "REJECT"
CONCEDE = "CONCEDE"
PARTIAL_CONCEDE = "PARTIAL_CONCEDE"
WITHDRAW = "WITHDRAW"
REVISE = "REVISE"
COUNTEREXAMPLE = "COUNTEREXAMPLE"
REQUEST_SOURCE = "REQUEST_SOURCE"
FORMAL_CHECK_REQUIRED_ACTION = "FORMAL_CHECK_REQUIRED"
GOVERNANCE_BLOCK = "GOVERNANCE_BLOCK"

ISSUE_ACTIONS = frozenset(
    {
        SUSTAIN,
        REJECT,
        CONCEDE,
        PARTIAL_CONCEDE,
        WITHDRAW,
        REVISE,
        COUNTEREXAMPLE,
        REQUEST_SOURCE,
        FORMAL_CHECK_REQUIRED_ACTION,
        GOVERNANCE_BLOCK,
    }
)

ISSUE_OPEN = "OPEN"
ISSUE_SUSTAINED = "SUSTAINED"
ISSUE_PARTIALLY_CONCEDED = "PARTIALLY_CONCEDED"
ISSUE_REVISED = "REVISED"
ISSUE_CONCEDED = "CONCEDED"
ISSUE_WITHDRAWN = "WITHDRAWN"
ISSUE_REJECTED = "REJECTED"
ISSUE_SOURCE_REQUIRED = "SOURCE_REQUIRED"
ISSUE_FORMAL_REQUIRED = "FORMAL_CHECK_REQUIRED"
ISSUE_GOVERNANCE_BLOCKED = "GOVERNANCE_BLOCKED"

# An objection in one of these states has been defeated or given up by the
# party that raised it. It stays in history forever and can never silently
# return to OPEN; only an explicit, separately recorded new objection can
# re-raise the substance, and that new objection gets its own identity.
DEFEATED_ISSUE_STATES = frozenset({ISSUE_CONCEDED, ISSUE_WITHDRAWN, ISSUE_REJECTED})

# States in which an objection still counts against readiness.
LIVE_ISSUE_STATES = frozenset(
    {ISSUE_OPEN, ISSUE_SUSTAINED, ISSUE_PARTIALLY_CONCEDED, ISSUE_REVISED}
)

BLOCKING_ISSUE_STATES = frozenset(
    {ISSUE_SOURCE_REQUIRED, ISSUE_FORMAL_REQUIRED, ISSUE_GOVERNANCE_BLOCKED}
)

_ACTION_TO_STATE = {
    SUSTAIN: ISSUE_SUSTAINED,
    REJECT: ISSUE_REJECTED,
    CONCEDE: ISSUE_CONCEDED,
    PARTIAL_CONCEDE: ISSUE_PARTIALLY_CONCEDED,
    WITHDRAW: ISSUE_WITHDRAWN,
    REVISE: ISSUE_REVISED,
    COUNTEREXAMPLE: ISSUE_SUSTAINED,
    REQUEST_SOURCE: ISSUE_SOURCE_REQUIRED,
    FORMAL_CHECK_REQUIRED_ACTION: ISSUE_FORMAL_REQUIRED,
    GOVERNANCE_BLOCK: ISSUE_GOVERNANCE_BLOCKED,
}

_WS = re.compile(r"\s+")
_EDGE_PUNCT = re.compile(r"^[^\w]+|[^\w]+$")


def normalize_claim(text: str) -> str:
    """Deterministic normalisation used for issue identity.

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


class IssueReopenError(RuntimeError):
    """Raised when a defeated objection is pushed back toward OPEN."""


@dataclass
class Target:
    id: str
    original_formulation: str
    current_formulation: str
    frozen_scope: str
    status: str = OPEN
    confidence_class: str = RECONSTRUCTED_RESEARCH_STATE
    provenance: str = ""
    repository_relationship: str = ""
    depends_on: list[str] = field(default_factory=list)
    authorized: bool = False
    supporting_arguments: list[str] = field(default_factory=list)
    sustained_objections: list[str] = field(default_factory=list)
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


class Ledger:
    """The live noncanonical research state.

    Persisted as JSON so that unresolved issues survive process restarts and
    context compaction. Reloading is lossless for issue identity and history.
    """

    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else None
        self.targets: dict[str, Target] = {}
        self.issues: dict[str, Issue] = {}
        self.meta: dict[str, Any] = {"schema": LEDGER_SCHEMA}

    # -- targets ----------------------------------------------------------

    def add_target(self, target: Target) -> Target:
        if target.status not in TARGET_STATUSES:
            raise ValueError(f"unknown target status: {target.status}")
        if target.confidence_class not in CONFIDENCE_CLASSES:
            raise ValueError(f"unknown confidence class: {target.confidence_class}")
        if not target.provenance:
            raise ValueError(f"target {target.id} has no provenance")
        self.targets[target.id] = target
        return target

    def set_target_status(self, target_id: str, status: str, note: str = "") -> None:
        if status not in TARGET_STATUSES:
            raise ValueError(f"unknown target status: {status}")
        target = self.targets[target_id]
        target.status = status
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

        Re-registering a defeated objection does not reopen it. The identity is
        content-addressed, so an attempt to smuggle a settled attack back into
        the queue by resending the same text is a no-op against history.
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
            IssueEvent(
                at=time.time(),
                actor=raised_by,
                action="RAISE",
                rationale=claim,
                from_state="",
                to_state=ISSUE_OPEN,
                provenance=provenance,
            )
        )
        self.issues[iid] = issue
        return issue

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
        if action not in ISSUE_ACTIONS:
            raise ValueError(f"unknown issue action: {action}")
        issue = self.issues[issue_id_]
        target_state = _ACTION_TO_STATE[action]
        if issue.is_defeated() and target_state in LIVE_ISSUE_STATES:
            raise IssueReopenError(
                f"{issue.id} is {issue.state}; a defeated objection cannot return to "
                f"{target_state}. Raise a new, distinctly formulated objection instead."
            )
        previous = issue.state
        issue.state = target_state
        if revised_claim and action == REVISE:
            successor = self.register_issue(
                target_id=issue.target_id,
                claim=revised_claim,
                raised_by=actor,
                provenance=provenance or issue.provenance,
                confidence_class=issue.confidence_class,
            )
            issue.superseded_by = successor.id
        issue.history.append(
            IssueEvent(
                at=time.time(),
                actor=actor,
                action=action,
                rationale=rationale,
                from_state=previous,
                to_state=target_state,
                provenance=provenance,
                invocation_id=invocation_id,
                agreement=dict(agreement or {}),
            )
        )
        return issue

    def issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues.values() if i.target_id == target_id]

    def live_issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues_for(target_id) if i.is_live()]

    def blocking_issues_for(self, target_id: str) -> list[Issue]:
        return [i for i in self.issues_for(target_id) if i.is_blocking()]

    # -- dispositions -----------------------------------------------------

    def evaluate_target(self, target_id: str) -> str:
        """Derive a target disposition from surviving objections alone.

        Model agreement is deliberately not an input. READY requires that no
        registered material objection survives under the frozen protocol, and
        that at least one objection was actually adjudicated — a target nobody
        ever attacked is untested, not ready.
        """
        target = self.targets[target_id]
        issues = self.issues_for(target_id)
        blocking = [i for i in issues if i.is_blocking()]
        if blocking:
            states = {i.state for i in blocking}
            if ISSUE_GOVERNANCE_BLOCKED in states:
                return GOVERNANCE_DECISION_REQUIRED
            if ISSUE_SOURCE_REQUIRED in states:
                return SOURCE_REQUIRED
            return FORMAL_CHECK_REQUIRED
        live = [i for i in issues if i.is_live()]
        if live:
            return NEAR_READY if len(live) == 1 else OPEN
        if not issues:
            return OPEN
        if target.missing_evidence:
            return SOURCE_REQUIRED
        return READY_UNDER_INTERNAL_PROTOCOL

    def next_target(self) -> Target | None:
        """Shortest dependency-valid next step.

        A target is eligible when it is non-terminal, explicitly authorized,
        and every declared dependency has already reached a terminal
        disposition. Selection order is deterministic by target id.
        """
        for target in sorted(self.targets.values(), key=lambda t: t.id):
            if target.is_terminal() or not target.authorized:
                continue
            if all(
                dep in self.targets and self.targets[dep].is_terminal()
                for dep in target.depends_on
            ):
                return target
        return None

    def select_target(self, target_id: str) -> Target:
        """Explicit selection, refused for unauthorized or blocked targets."""
        target = self.targets[target_id]
        if not target.authorized:
            raise PermissionError(
                f"{target_id} is not authorized for execution under current governance"
            )
        unmet = [
            dep
            for dep in target.depends_on
            if dep not in self.targets or not self.targets[dep].is_terminal()
        ]
        if unmet:
            raise PermissionError(f"{target_id} has unmet dependencies: {', '.join(unmet)}")
        return target

    # -- persistence ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "meta": self.meta,
            "targets": {k: asdict(v) for k, v in sorted(self.targets.items())},
            "issues": {k: asdict(v) for k, v in sorted(self.issues.items())},
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
        for tid, raw in data.get("targets", {}).items():
            ledger.targets[tid] = Target(**raw)
        for iid, raw in data.get("issues", {}).items():
            history = [IssueEvent(**event) for event in raw.pop("history", [])]
            issue = Issue(**raw)
            issue.history = history
            ledger.issues[iid] = issue
        return ledger

    def digest(self) -> str:
        return sha256_hex(json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False))
