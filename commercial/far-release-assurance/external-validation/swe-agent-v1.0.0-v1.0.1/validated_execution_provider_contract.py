from __future__ import annotations

import re
from typing import Any, Callable

import execution_outcome as base

_PERMANENT_MODEL_PATTERNS = (
    re.compile(r"\bnot available to new users\b", re.IGNORECASE),
    re.compile(r"\bmodel(?:s/)?[\w.\-]+\s+is no longer available\b", re.IGNORECASE),
    re.compile(r"\bmodel\s+(?:is\s+)?not found\b", re.IGNORECASE),
    re.compile(r"\bdoes not exist or you do not have access\b", re.IGNORECASE),
    re.compile(r"\bstatus[\"']?\s*[:=]\s*[\"']?not_found\b", re.IGNORECASE),
    re.compile(
        r"\b404\s+not found\b.*\b(?:models?/|generatecontent)\b",
        re.IGNORECASE | re.DOTALL,
    ),
)

_RETRYABLE_ERROR_PATTERNS = (
    re.compile(
        r"\b(?:http(?:\s+status)?|status code:?)\s*(?:500|502|503|504)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:service|temporarily)\s+unavailable\b", re.IGNORECASE),
    re.compile(r"\bconnection\s+(?:reset|aborted|error)\b", re.IGNORECASE),
    re.compile(r"\bgateway\s+timeout\b", re.IGNORECASE),
    re.compile(r"\bbad\s+gateway\b", re.IGNORECASE),
    re.compile(r"\btimed\s+out\b", re.IGNORECASE),
    re.compile(
        r"\b(?:read|connect|request|api|provider|model)\s+timeout\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:read|connect|request)timeout\b", re.IGNORECASE),
    re.compile(r"\btimeout(?:error|exception)\b", re.IGNORECASE),
)


def _first_match(patterns: tuple[re.Pattern[str], ...], text: str) -> str | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match is not None:
            return match.group(0)
    return None


def _terminal_outcome(
    outcome: base.ExecutionOutcome,
    *,
    category: str,
    reason: str,
    signal: str | None,
) -> base.ExecutionOutcome:
    evidence = dict(outcome.evidence)
    evidence["provider_classification_signal"] = signal
    return base.ExecutionOutcome(
        category,
        "failed_terminal",
        False,
        outcome.internal_status,
        outcome.patch_present,
        outcome.no_change_submission,
        reason,
        evidence,
    )


def wrap_classifier(
    delegate: Callable[..., base.ExecutionOutcome],
) -> Callable[..., base.ExecutionOutcome]:
    """Add error-context-aware provider classification to a classifier."""

    def classify_execution(**kwargs: Any) -> base.ExecutionOutcome:
        outcome = delegate(**kwargs)
        if outcome.state == "complete":
            return outcome

        combined = f"{kwargs.get('stdout', '')}\n{kwargs.get('stderr', '')}"
        permanent_signal = _first_match(_PERMANENT_MODEL_PATTERNS, combined)
        if permanent_signal is not None:
            return _terminal_outcome(
                outcome,
                category="provider_model_unavailable",
                reason=(
                    "the frozen model endpoint is unavailable to this API project; "
                    "rerunning with the same credential cannot succeed"
                ),
                signal=permanent_signal,
            )

        if outcome.category == "retryable_provider_error":
            retryable_signal = _first_match(_RETRYABLE_ERROR_PATTERNS, combined)
            if retryable_signal is None:
                return _terminal_outcome(
                    outcome,
                    category="terminal_agent_error",
                    reason=(
                        "retryable provider classification lacked an error-context "
                        "signal; benign configuration text must not trigger a retry"
                    ),
                    signal=None,
                )

        return outcome

    return classify_execution


def install(core: Any, hardening: Any) -> None:
    """Install provider classification for live and restored executions."""
    classifier = wrap_classifier(core.classify_execution)
    core.classify_execution = classifier
    hardening.classify_execution = classifier
