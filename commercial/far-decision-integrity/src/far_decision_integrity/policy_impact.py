from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable

from .refund import RefundRequest


class PolicyDisposition(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    ESCALATE = "escalate"


class ImpactDecision(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RefundPolicy:
    version: str
    auto_approval_limit: float = 500.0
    approval_window_days: int = 30
    require_order_exists: bool = True
    require_payment_confirmed: bool = True
    require_no_previous_refund: bool = True
    require_agent_authority: bool = True

    def __post_init__(self) -> None:
        if not self.version.strip():
            raise ValueError("policy version must be non-empty")
        if self.auto_approval_limit < 0:
            raise ValueError("auto_approval_limit must be non-negative")
        if self.approval_window_days < 0:
            raise ValueError("approval_window_days must be non-negative")


@dataclass(frozen=True, slots=True)
class CaseImpact:
    request_id: str
    baseline: PolicyDisposition
    candidate: PolicyDisposition
    changed: bool
    direction: str


@dataclass(frozen=True, slots=True)
class PolicyImpactReport:
    baseline_version: str
    candidate_version: str
    decision: ImpactDecision
    changed_rules: tuple[str, ...]
    cases: tuple[CaseImpact, ...]

    def to_dict(self) -> dict:
        return {
            "baseline_version": self.baseline_version,
            "candidate_version": self.candidate_version,
            "decision": self.decision.value,
            "changed_rules": list(self.changed_rules),
            "cases": [
                {
                    "request_id": case.request_id,
                    "baseline": case.baseline.value,
                    "candidate": case.candidate.value,
                    "changed": case.changed,
                    "direction": case.direction,
                }
                for case in self.cases
            ],
        }


def evaluate_refund(request: RefundRequest, policy: RefundPolicy) -> PolicyDisposition:
    observed = {
        "order_exists": request.order_exists,
        "payment_confirmed": request.payment_confirmed,
        "previous_refund": request.previous_refund,
        "agent_authorized": request.agent_authorized,
        "days_since_purchase": request.days_since_purchase,
    }
    required = {
        "order_exists": policy.require_order_exists,
        "payment_confirmed": policy.require_payment_confirmed,
        "previous_refund": policy.require_no_previous_refund,
        "agent_authorized": policy.require_agent_authority,
        "days_since_purchase": True,
    }
    if any(required[key] and observed[key] is None for key in observed):
        return PolicyDisposition.ESCALATE
    if request.conflicting_delivery_status:
        return PolicyDisposition.ESCALATE
    if policy.require_order_exists and request.order_exists is not True:
        return PolicyDisposition.BLOCK
    if policy.require_payment_confirmed and request.payment_confirmed is not True:
        return PolicyDisposition.BLOCK
    if policy.require_no_previous_refund and request.previous_refund is not False:
        return PolicyDisposition.BLOCK
    if policy.require_agent_authority and request.agent_authorized is not True:
        return PolicyDisposition.BLOCK
    if request.days_since_purchase is None or request.days_since_purchase > policy.approval_window_days:
        return PolicyDisposition.BLOCK
    if request.amount > policy.auto_approval_limit:
        return PolicyDisposition.BLOCK
    return PolicyDisposition.ALLOW


def compare_policies(
    baseline: RefundPolicy,
    candidate: RefundPolicy,
    cases: Iterable[RefundRequest],
) -> PolicyImpactReport:
    changed_rules = tuple(
        key
        for key, value in asdict(baseline).items()
        if key != "version" and value != asdict(candidate)[key]
    )
    impacts: list[CaseImpact] = []
    for request in sorted(cases, key=lambda item: item.request_id):
        before = evaluate_refund(request, baseline)
        after = evaluate_refund(request, candidate)
        if before == after:
            direction = "unchanged"
        elif before == PolicyDisposition.BLOCK and after == PolicyDisposition.ALLOW:
            direction = "authorization-expanded"
        elif before == PolicyDisposition.ALLOW and after == PolicyDisposition.BLOCK:
            direction = "authorization-restricted"
        else:
            direction = "review-path-changed"
        impacts.append(CaseImpact(request.request_id, before, after, before != after, direction))

    directions = {impact.direction for impact in impacts if impact.changed}
    if "authorization-expanded" in directions:
        decision = ImpactDecision.BLOCKED
    elif directions:
        decision = ImpactDecision.REVIEW
    else:
        decision = ImpactDecision.PASS
    return PolicyImpactReport(
        baseline.version,
        candidate.version,
        decision,
        changed_rules,
        tuple(impacts),
    )
