#!/usr/bin/env python3
"""Provider-neutral blind/cross-audit harness with immutable invocation history."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timezone
from pathlib import Path

try:  # support both `python tools/...` and package-style test imports
    from tools.research_campaign import build_prompt_evidence, canonical_json
except ModuleNotFoundError:  # pragma: no cover - exercised by direct script execution
    from research_campaign import build_prompt_evidence, canonical_json

Reasoner = Callable[[str, str], str]


_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[^\s,;]{8,}"),
)


def redact_outbound(text: str) -> str:
    """Redact credential-shaped material before it reaches any provider prompt."""
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


@dataclasses.dataclass(frozen=True, slots=True)
class ReasonerLane:
    """A provider-neutral callable plus an auditable isolation assertion.

    The harness can verify the declaration and sequencing, but cannot inspect a remote
    provider's undisclosed infrastructure. Campaign capsules must record that limitation.
    """

    provider_id: str
    model_identity: str
    sandbox_id: str
    reasoner: Reasoner
    isolation_verified: bool
    repository_tools_enabled: bool = False
    shared_state_with: tuple[str, ...] = ()
    prior_exposure: str = "unknown"


@dataclasses.dataclass(frozen=True, slots=True)
class Invocation:
    invocation_id: str
    provider_id: str
    phase: str
    request_sha256: str
    evidence_sha256: str
    status: str
    raw_output: str | None
    error: str | None
    replay_of: str | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class IssueRevision:
    issue_id: str
    invocation_id: str
    provider_id: str
    text: str
    revision: int
    supersedes_revision: int | None = None


@dataclasses.dataclass(frozen=True, slots=True)
class FrozenPass:
    phase: str
    invocations: tuple[Invocation, ...]
    issues: tuple[IssueRevision, ...]
    freeze_sha256: str


def _validate_lanes(reasoners: Mapping[str, ReasonerLane]) -> None:
    if not reasoners:
        raise ValueError("at least one reasoner lane is required")
    sandbox_ids: list[str] = []
    for provider_id, lane in reasoners.items():
        if not isinstance(lane, ReasonerLane):
            raise TypeError(f"{provider_id}: reasoner must be a ReasonerLane")
        if lane.provider_id != provider_id:
            raise ValueError(f"{provider_id}: lane/provider identity mismatch")
        if not lane.model_identity or not lane.sandbox_id:
            raise ValueError(f"{provider_id}: model identity and sandbox id are required")
        if not lane.isolation_verified:
            raise ValueError(f"{provider_id}: lane isolation was not verified")
        if lane.repository_tools_enabled:
            raise ValueError(f"{provider_id}: repository tools are prohibited in a blind lane")
        if lane.shared_state_with:
            raise ValueError(f"{provider_id}: cross-lane shared state is prohibited: {lane.shared_state_with}")
        sandbox_ids.append(lane.sandbox_id)
    if len(sandbox_ids) != len(set(sandbox_ids)):
        raise ValueError("reasoner lanes must use distinct sandbox identities")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _redact_json_strings(value):
    """Redact string values without ever rewriting serialized JSON structure."""
    if isinstance(value, str):
        return redact_outbound(value)
    if isinstance(value, list):
        return [_redact_json_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: _redact_json_strings(item) for key, item in value.items()}
    return value


def _invocation_id(campaign_id: str, phase: str, provider_id: str, ordinal: int, request: str) -> str:
    digest = _sha(f"{campaign_id}\0{phase}\0{provider_id}\0{ordinal}\0{request}")[:16]
    return f"INV-{phase.upper()}-{ordinal:03d}-{digest}"


def _extract_issues(invocation: Invocation) -> tuple[IssueRevision, ...]:
    if invocation.status != "completed" or not invocation.raw_output:
        return ()
    lines = [line.removeprefix("ISSUE:").strip() for line in invocation.raw_output.splitlines() if line.strip().startswith("ISSUE:")]
    return tuple(
        IssueRevision(
            issue_id=f"ISSUE-{_sha(invocation.provider_id + chr(0) + text)[:16]}",
            invocation_id=invocation.invocation_id,
            provider_id=invocation.provider_id,
            text=text,
            revision=1,
        )
        for text in lines
    )


def _call_reasoner(reasoner: Reasoner, provider_id: str, phase: str, invocation_id: str, prompt: str, evidence_hash: str, replay_of: str | None = None) -> Invocation:
    try:
        output = reasoner(prompt, invocation_id)
        if not isinstance(output, str):
            raise TypeError("reasoner output must be text")
        return Invocation(invocation_id, provider_id, phase, _sha(prompt), evidence_hash, "completed", output, None, replay_of)
    except Exception as exc:  # failures are durable evidence, not dropped lanes
        return Invocation(invocation_id, provider_id, phase, _sha(prompt), evidence_hash, "failed", None, f"{type(exc).__name__}: {exc}", replay_of)


def run_blind_first_pass(
    *,
    campaign_id: str,
    problem: str,
    root: Path,
    capsule: dict,
    stage_id: str,
    evidence_paths: Iterable[str],
    reasoners: Mapping[str, ReasonerLane],
) -> FrozenPass:
    """Apply the firewall before constructing a prompt or calling any provider."""
    # Isolation is checked before credentials, provider availability, or repository bytes.
    _validate_lanes(reasoners)
    evidence = build_prompt_evidence(root, capsule, stage_id, evidence_paths)
    outbound_evidence = {path: redact_outbound(value) for path, value in evidence.items()}
    evidence_blob = canonical_json(outbound_evidence)
    evidence_hash = _sha(evidence_blob)
    prompt = canonical_json({"phase":"blind-first-pass","problem":redact_outbound(problem),"evidence":outbound_evidence,"rules":["extract falsifiable issues","do not infer proof from agreement"]})
    invocations: list[Invocation] = []
    issues: list[IssueRevision] = []
    for ordinal, (provider_id, lane) in enumerate(sorted(reasoners.items()), 1):
        invocation_id = _invocation_id(campaign_id, "blind", provider_id, ordinal, prompt)
        invocation = _call_reasoner(lane.reasoner, provider_id, "blind", invocation_id, prompt, evidence_hash)
        invocations.append(invocation)
        issues.extend(_extract_issues(invocation))
    frozen_payload = {"phase":"blind","invocations":[dataclasses.asdict(item) for item in invocations],"issues":[dataclasses.asdict(item) for item in issues]}
    return FrozenPass("blind", tuple(invocations), tuple(issues), _sha(canonical_json(frozen_payload)))


def append_issue_revision(history: Iterable[IssueRevision], issue_id: str, invocation_id: str, provider_id: str, text: str) -> tuple[IssueRevision, ...]:
    prior = tuple(history)
    revisions = [item.revision for item in prior if item.issue_id == issue_id]
    if not revisions:
        raise ValueError(f"unknown issue id: {issue_id}")
    next_revision = max(revisions) + 1
    return prior + (IssueRevision(issue_id, invocation_id, provider_id, text, next_revision, next_revision - 1),)


def run_controlled_cross_challenge(*, campaign_id: str, frozen: FrozenPass, challengers: Mapping[str, ReasonerLane]) -> FrozenPass:
    if not frozen.freeze_sha256:
        raise ValueError("cross-challenge requires a frozen first pass")
    _validate_lanes(challengers)
    outbound_issues = _redact_json_strings([dataclasses.asdict(item) for item in frozen.issues])
    outbound_issue_blob = canonical_json(outbound_issues)
    prompt = canonical_json({"phase":"controlled-cross-challenge","frozen_pass_sha256":frozen.freeze_sha256,"issues":outbound_issues,"rules":["challenge issues, not providers","no vote is proof"]})
    evidence_hash = _sha(outbound_issue_blob)
    invocations: list[Invocation] = []
    issues: list[IssueRevision] = list(frozen.issues)
    for ordinal, (provider_id, lane) in enumerate(sorted(challengers.items()), 1):
        invocation_id = _invocation_id(campaign_id, "cross", provider_id, ordinal, prompt)
        invocation = _call_reasoner(lane.reasoner, provider_id, "cross", invocation_id, prompt, evidence_hash)
        invocations.append(invocation)
        issues.extend(_extract_issues(invocation))
    payload = {"phase":"cross","parent":frozen.freeze_sha256,"invocations":[dataclasses.asdict(item) for item in invocations],"issues":[dataclasses.asdict(item) for item in issues]}
    return FrozenPass("cross", tuple(invocations), tuple(issues), _sha(canonical_json(payload)))


def replay_selected(*, campaign_id: str, records: Iterable[Invocation], selected_invocation_ids: Iterable[str], reasoners: Mapping[str, ReasonerLane], prompts_by_invocation: Mapping[str, str]) -> tuple[Invocation, ...]:
    """Controlled re-execution; exact recorded-byte replay is `replay_recorded`."""
    _validate_lanes(reasoners)
    by_id = {record.invocation_id: record for record in records}
    selected = tuple(selected_invocation_ids)
    if len(selected) != len(set(selected)):
        raise ValueError("selected invocation ids must be unique")
    replayed: list[Invocation] = []
    for ordinal, invocation_id in enumerate(selected, 1):
        if invocation_id not in by_id:
            raise ValueError(f"unknown selected invocation: {invocation_id}")
        original = by_id[invocation_id]
        if original.provider_id not in reasoners:
            raise ValueError(f"provider unavailable for exact replay: {original.provider_id}")
        prompt = prompts_by_invocation[invocation_id]
        if _sha(prompt) != original.request_sha256:
            raise ValueError(f"exact replay prompt hash mismatch: {invocation_id}")
        new_id = _invocation_id(campaign_id, "replay", original.provider_id, ordinal, invocation_id + prompt)
        replayed.append(_call_reasoner(reasoners[original.provider_id].reasoner, original.provider_id, "replay", new_id, prompt, original.evidence_sha256, invocation_id))
    return tuple(replayed)


def replay_recorded(*, records: Iterable[Invocation], selected_invocation_ids: Iterable[str], prompts_by_invocation: Mapping[str, str]) -> tuple[Invocation, ...]:
    """Deterministically replay exact recorded output/failure bytes by invocation identity."""
    by_id = {record.invocation_id: record for record in records}
    selected = tuple(selected_invocation_ids)
    if len(selected) != len(set(selected)):
        raise ValueError("selected invocation ids must be unique")
    replayed: list[Invocation] = []
    for invocation_id in selected:
        if invocation_id not in by_id:
            raise ValueError(f"unknown selected invocation: {invocation_id}")
        original = by_id[invocation_id]
        prompt = prompts_by_invocation[invocation_id]
        if _sha(prompt) != original.request_sha256:
            raise ValueError(f"exact replay prompt hash mismatch: {invocation_id}")
        replayed.append(dataclasses.replace(original, phase="recorded-replay", replay_of=invocation_id))
    return tuple(replayed)


def adjudication_record(*, campaign_id: str, frozen: FrozenPass, dispositions: Mapping[str, str], adjudicator: str) -> dict:
    known = {issue.issue_id for issue in frozen.issues}
    provided = set(dispositions)
    unknown = provided - known
    if unknown:
        raise ValueError(f"adjudication references unknown issues: {sorted(unknown)}")
    missing = known - provided
    if missing:
        raise ValueError(f"adjudication omits frozen issues: {sorted(missing)}")
    return {
        "campaign_id": campaign_id,
        "frozen_pass_sha256": frozen.freeze_sha256,
        "adjudicator": adjudicator,
        "adjudicated_at": datetime.now(timezone.utc).isoformat(),
        "dispositions": [{"issue_id": key, "disposition": dispositions[key]} for key in sorted(dispositions)],
        "reasoner_vote_used_as_proof": False,
    }
