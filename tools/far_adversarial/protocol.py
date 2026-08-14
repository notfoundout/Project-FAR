"""Prompt construction, strict output schemas, and parsing for the two lanes.

Prompt builders are pure functions of the frozen target and the eligible frozen
evidence. A first-pass prompt has no parameter through which another lane's
output could reach it, which is what makes blindness checkable rather than
merely intended.

The action contract shown to a lane is the contract that lane may actually
legally use. A challenged lane is never offered a way to terminate somebody
else's objection, because it has no such standing.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .ledger import CHALLENGED_ACTIONS, OWNER_ACTIONS
from .safety import UNTRUSTED_PREAMBLE, fence

PROTOCOL_VERSION = "far-adversarial-protocol/2"

CLAUDE_ROLE = """You are the RECONSTRUCTION lane.

Your job: state the strongest defensible formulation of the frozen target that
the eligible frozen evidence actually supports; reconstruct its semantics and
dependencies; interpret sources strictly by what they say; propose the minimal
repair when something fails; and concede explicitly and immediately when an
objection defeats your position.

You are not the judge. Your agreement with anyone proves nothing. Overclaiming
is a worse failure than reporting Unknown.

Reason only from the fenced frozen evidence in this prompt. You have no tools
and no repository access; if something you need is absent, record it as a
source request rather than recalling it."""

GPT_ROLE = """You are the ADVERSARIAL lane.

Your job: attack the frozen target. Search for countermodels, equivocation,
hidden assumptions, invalid inference, scope drift, source overread, and
stronger alternative formulations. Try to falsify.

You are not the judge. Your agreement with anyone proves nothing. An objection
you cannot ground in the frozen evidence is worse than no objection.

Reason only from the fenced frozen evidence in this prompt. You have no tools
and no repository access; if something you need is absent, record it as a
source request rather than recalling it."""

# --- strict output schemas ------------------------------------------------

FIRST_PASS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "assessment": {"type": "string"},
        "objections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "kind": {
                        "type": "string",
                        "enum": ["countermodel", "equivocation", "hidden-assumption",
                                 "invalid-inference", "scope-drift", "source-overread",
                                 "alternative", "other"],
                    },
                    "rationale": {"type": "string"},
                },
                "required": ["claim", "kind", "rationale"],
                "additionalProperties": False,
            },
        },
        "source_requests": {"type": "array", "items": {"type": "string"}},
        "formal_obligations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["assessment", "objections", "source_requests", "formal_obligations"],
    "additionalProperties": False,
}


def cross_audit_schema(actions: list[str]) -> dict[str, Any]:
    """Schema restricted to the actions this actor may legally take."""
    return {
        "type": "object",
        "properties": {
            "responses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "issue_id": {"type": "string"},
                        "action": {"type": "string", "enum": sorted(actions)},
                        "rationale": {"type": "string"},
                        "revised_claim": {"type": ["string", "null"]},
                    },
                    "required": ["issue_id", "action", "rationale", "revised_claim"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["responses"],
        "additionalProperties": False,
    }


_FIRST_PASS_CONTRACT = """Reply with a single JSON object and nothing else:

{
  "assessment": "<your analysis, prose>",
  "objections": [
    {"claim": "<one material objection, one sentence, self-contained>",
     "kind": "<countermodel|equivocation|hidden-assumption|invalid-inference|scope-drift|source-overread|alternative|other>",
     "rationale": "<why this bites, citing the frozen evidence>"}
  ],
  "source_requests": ["<exact artifact you need and do not have>"],
  "formal_obligations": ["<proof obligation that must be discharged formally>"]
}

Each objection must be independently statable. Do not restate one objection in
several forms. If you have no material objection, return an empty list.

A source request or formal obligation you record here will block this target
from reaching READY until it is discharged with provenance. Record one only if
you mean it."""

_CHALLENGED_CONTRACT = """You are the CHALLENGED party for every issue listed below.
Another lane raised them against your position. You do not own them and you
cannot terminate them.

Permitted actions: %s

  REBUT              - you answer the objection. It stays live; its owner
                       reviews your rebuttal and decides.
  CONCEDE            - the objection is right. It then stands against the target.
  PARTIAL_CONCEDE    - part of it is right.
  REQUEST_SOURCE     - it cannot be settled without an artifact you lack.
  FORMAL_CHECK_REQUIRED - it needs a proof, not an argument.
  GOVERNANCE_BLOCK   - it needs a governance decision.

There is no action by which you declare the objection wrong and finished.
Asserting that an objection fails is a REBUT.

Reply with a single JSON object and nothing else:

{"responses": [{"issue_id": "<exact registered id>", "action": "<one of the above>",
                "rationale": "<prose>", "revised_claim": null}]}

Respond to every listed issue exactly once."""

_OWNER_CONTRACT = """You OWN every issue listed below: you raised them, and the other
lane has now responded. Review each rebuttal and decide.

Permitted actions: %s

  SUSTAIN            - the rebuttal does not answer your objection. The
                       disagreement remains live.
  WITHDRAW           - the rebuttal defeats your objection. This is the only
                       way an objection becomes defeated, and only you can do it.
  REVISE             - your objection was overbroad; supply a narrower successor
                       claim in revised_claim.
  COUNTEREXAMPLE     - you have a concrete counterexample to the rebuttal.
  REQUEST_SOURCE     - it cannot be settled without an artifact you lack.
  FORMAL_CHECK_REQUIRED - it needs a proof, not an argument.
  GOVERNANCE_BLOCK   - it needs a governance decision.

Withdraw when you are actually defeated. Sustaining a defeated objection wastes
rounds; withdrawing a live one loses a real finding.

Reply with a single JSON object and nothing else:

{"responses": [{"issue_id": "<exact registered id>", "action": "<one of the above>",
                "rationale": "<prose>",
                "revised_claim": "<required only for REVISE, else null>"}]}

Respond to every listed issue exactly once."""

CHALLENGED_CONTRACT = _CHALLENGED_CONTRACT % ", ".join(sorted(CHALLENGED_ACTIONS))
OWNER_CONTRACT = _OWNER_CONTRACT % ", ".join(sorted(OWNER_ACTIONS))

ROLE_CHALLENGED = "challenged"
ROLE_OWNER = "owner"


def _evidence_block(evidence: dict[str, str]) -> str:
    parts = [UNTRUSTED_PREAMBLE, ""]
    for name in sorted(evidence):
        parts.append(fence(name, evidence[name]))
        parts.append("")
    return "\n".join(parts)


def first_pass_prompt(*, role: str, target: Any, evidence: dict[str, str],
                      source_freeze: str) -> str:
    """Build a blind first-pass prompt.

    Pure in (role, target, evidence, source_freeze). There is deliberately no
    parameter for another lane's findings.
    """
    return "\n".join(
        [
            role,
            "",
            f"Protocol: {PROTOCOL_VERSION}",
            f"Frozen source: {source_freeze}",
            "",
            "## Frozen target",
            "",
            f"Target id: {target.id}",
            f"Frozen scope: {target.frozen_scope}",
            "",
            target.current_formulation,
            "",
            "## Eligible frozen evidence",
            "",
            _evidence_block(evidence),
            "## Output contract",
            "",
            _FIRST_PASS_CONTRACT,
        ]
    )


def cross_audit_prompt(*, role: str, audit_role: str, target: Any, issues: list[Any],
                       evidence: dict[str, str], source_freeze: str) -> str:
    """Build an issue-by-issue cross-audit prompt for one side of the exchange.

    Only the issues under audit are sent, not the accumulated transcript.
    Settled issues are not resent, so a growing history cannot quietly
    reintroduce a defeated attack.
    """
    if audit_role not in {ROLE_CHALLENGED, ROLE_OWNER}:
        raise ValueError(f"unknown audit role: {audit_role}")
    contract = CHALLENGED_CONTRACT if audit_role == ROLE_CHALLENGED else OWNER_CONTRACT
    listing = [
        f"- {issue.id} [raised by {issue.raised_by}, state {issue.state}]: {issue.claim}"
        for issue in issues
    ]
    return "\n".join(
        [
            role,
            "",
            f"Protocol: {PROTOCOL_VERSION}",
            f"Frozen source: {source_freeze}",
            "",
            "## Frozen target",
            "",
            f"Target id: {target.id}",
            f"Frozen scope: {target.frozen_scope}",
            "",
            target.current_formulation,
            "",
            "## Registered issues under audit",
            "",
            *listing,
            "",
            "## Eligible frozen evidence",
            "",
            _evidence_block(evidence),
            "## Output contract",
            "",
            contract,
        ]
    )


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def extract_json(raw: str) -> dict[str, Any] | None:
    """Recover a single JSON object from a provider response.

    Tolerates a code fence or surrounding prose, which the Claude CLI produces.
    Returns ``None`` when nothing parses; the caller must treat that as
    ``INVALID_PROVIDER_OUTPUT`` and never as a research finding.
    """
    if not raw or not raw.strip():
        return None
    candidates: list[str] = []
    match = _FENCE.search(raw)
    if match:
        candidates.append(match.group(1))
    candidates.append(raw)
    start = raw.find("{")
    if start != -1:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(raw)):
            char = raw[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(raw[start:index + 1])
                    break
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except (ValueError, TypeError):
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def parse_first_pass(raw: str) -> dict[str, Any] | None:
    parsed = extract_json(raw)
    if parsed is None:
        return None
    objections = parsed.get("objections", [])
    if not isinstance(objections, list):
        return None
    clean: list[dict[str, str]] = []
    for item in objections:
        if not isinstance(item, dict):
            return None
        claim = item.get("claim")
        if not isinstance(claim, str) or not claim.strip():
            return None
        clean.append(
            {
                "claim": claim.strip(),
                "kind": str(item.get("kind", "other")),
                "rationale": str(item.get("rationale", "")),
            }
        )
    return {
        "assessment": str(parsed.get("assessment", "")),
        "objections": clean,
        "source_requests": [str(x) for x in parsed.get("source_requests", []) or []],
        "formal_obligations": [str(x) for x in parsed.get("formal_obligations", []) or []],
    }


def parse_cross_audit(raw: str, known_issue_ids: set[str],
                      permitted_actions: set[str]) -> list[dict[str, Any]] | None:
    """Parse typed cross-audit actions, rejecting anything out of standing.

    A response naming an unregistered issue is rejected: a lane does not get to
    invent an issue identity mid-audit. A response using an action the actor
    has no standing for is rejected here as well as at the ledger, so an
    illegal move can never be partially applied.
    """
    parsed = extract_json(raw)
    if parsed is None:
        return None
    responses = parsed.get("responses")
    if not isinstance(responses, list):
        return None
    out: list[dict[str, Any]] = []
    for item in responses:
        if not isinstance(item, dict):
            return None
        issue = item.get("issue_id")
        action = item.get("action")
        if issue not in known_issue_ids or action not in permitted_actions:
            return None
        revised = item.get("revised_claim")
        out.append(
            {
                "issue_id": issue,
                "action": action,
                "rationale": str(item.get("rationale", "")),
                "revised_claim": revised if isinstance(revised, str) and revised.strip() else None,
            }
        )
    return out
