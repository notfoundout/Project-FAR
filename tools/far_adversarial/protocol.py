"""Prompt construction and structured-output parsing for the two lanes.

Prompt builders are pure functions of the frozen target and the eligible frozen
evidence. A first-pass prompt has no parameter through which another lane's
output could reach it, which is what makes blindness checkable rather than
merely intended.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .ledger import ISSUE_ACTIONS
from .safety import UNTRUSTED_PREAMBLE, fence

PROTOCOL_VERSION = "far-adversarial-protocol/1"

CLAUDE_ROLE = """You are the RECONSTRUCTION lane.

Your job: state the strongest defensible formulation of the frozen target that
the eligible frozen evidence actually supports; reconstruct its semantics and
dependencies; interpret sources strictly by what they say; propose the minimal
repair when something fails; and concede explicitly and immediately when an
objection defeats your position.

You are not the judge. Your agreement with anyone proves nothing. Overclaiming
is a worse failure than reporting Unknown."""

GPT_ROLE = """You are the ADVERSARIAL lane.

Your job: attack the frozen target. Search for countermodels, equivocation,
hidden assumptions, invalid inference, scope drift, source overread, and
stronger alternative formulations. Try to falsify.

You are not the judge. Your agreement with anyone proves nothing. An objection
you cannot ground in the frozen evidence is worse than no objection."""

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
several forms. If you have no material objection, return an empty list."""

_CROSS_AUDIT_CONTRACT = """Reply with a single JSON object and nothing else:

{
  "responses": [
    {"issue_id": "<exact registered id>",
     "action": "<%s>",
     "rationale": "<prose>",
     "revised_claim": "<required only for REVISE, else null>"}
  ]
}

Respond to every listed issue exactly once. Use CONCEDE when the objection
defeats your position, WITHDRAW when the objection is yours and you no longer
maintain it, REQUEST_SOURCE when the issue cannot be settled without an
artifact you do not have, and FORMAL_CHECK_REQUIRED when it needs a proof
rather than an argument.""" % "|".join(sorted(ISSUE_ACTIONS))


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


def cross_audit_prompt(*, role: str, target: Any, issues: list[Any], evidence: dict[str, str],
                       source_freeze: str) -> str:
    """Build an issue-by-issue cross-audit prompt.

    Only the registered issues under audit are sent, not the accumulated
    transcript. Settled issues are not resent, so a growing history cannot
    quietly reintroduce a defeated attack.
    """
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
            _CROSS_AUDIT_CONTRACT,
        ]
    )


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def extract_json(raw: str) -> dict[str, Any] | None:
    """Recover a single JSON object from a provider response.

    Tolerates a code fence or surrounding prose. Returns ``None`` when nothing
    parses; the caller must treat that as ``INVALID_PROVIDER_OUTPUT`` and never
    as a research finding.
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


def parse_cross_audit(raw: str, known_issue_ids: set[str]) -> list[dict[str, Any]] | None:
    """Parse typed cross-audit actions.

    A response naming an issue that was never registered is rejected outright:
    a lane does not get to invent an issue identity mid-audit.
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
        if issue not in known_issue_ids or action not in ISSUE_ACTIONS:
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
