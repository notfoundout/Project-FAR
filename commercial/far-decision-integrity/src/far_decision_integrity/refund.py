from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import SCHEMA_VERSION, DecisionPackage

REFUND_POLICY_VERSION = "refund-policy/2026-07"
AUTO_APPROVAL_LIMIT = 500.0
AUTO_APPROVAL_WINDOW_DAYS = 30


@dataclass(frozen=True, slots=True)
class RefundRequest:
    request_id: str
    order_id: str
    amount: float
    order_exists: bool | None
    payment_confirmed: bool | None
    days_since_purchase: int | None
    previous_refund: bool | None
    agent_authorized: bool | None
    policy_version: str = REFUND_POLICY_VERSION
    conflicting_delivery_status: bool = False


def build_refund_package(request: RefundRequest) -> DecisionPackage:
    """Compile an explicit refund request into a FAR decision package.

    ``None`` means unavailable, not false. ``False`` means a requirement was
    observed and failed. The compiler never invents missing facts.
    """
    nodes: list[dict[str, Any]] = []
    dependencies: list[dict[str, str]] = []
    requirements: list[str] = []
    unknowns: list[str] = []

    def add_requirement(node_id: str, statement: str, value: bool | None) -> None:
        attributes: dict[str, Any] = {}
        if value is False:
            attributes["valid"] = False
        elif value is None:
            unknowns.append(node_id)
        nodes.append({
            "node_id": node_id,
            "kind": "evidence",
            "statement": statement,
            "attributes": attributes,
        })
        dependencies.append({
            "source_id": node_id,
            "target_id": "approve-refund",
            "relation": "supports",
        })
        requirements.append(node_id)

    add_requirement("order-exists", "The referenced order exists.", request.order_exists)
    add_requirement("payment-confirmed", "Payment for the order is confirmed.", request.payment_confirmed)
    add_requirement(
        "within-refund-window",
        f"The request is within {AUTO_APPROVAL_WINDOW_DAYS} days of purchase.",
        None if request.days_since_purchase is None else request.days_since_purchase <= AUTO_APPROVAL_WINDOW_DAYS,
    )
    add_requirement(
        "no-previous-refund",
        "No previous refund has been issued for this order.",
        None if request.previous_refund is None else not request.previous_refund,
    )
    add_requirement("agent-authorized", "The requesting agent has refund authority.", request.agent_authorized)
    add_requirement(
        "within-auto-approval-limit",
        f"The requested amount does not exceed ${AUTO_APPROVAL_LIMIT:.2f}.",
        request.amount <= AUTO_APPROVAL_LIMIT,
    )

    policy_valid = request.policy_version == REFUND_POLICY_VERSION
    nodes.append({
        "node_id": "applicable-policy",
        "kind": "rule",
        "statement": f"Apply {REFUND_POLICY_VERSION} to automated refund decisions.",
        "attributes": {"valid": policy_valid},
    })
    dependencies.append({
        "source_id": "applicable-policy",
        "target_id": "approve-refund",
        "relation": "authorizes",
    })
    requirements.append("applicable-policy")
    nodes.append({
        "node_id": "approve-refund",
        "kind": "conclusion",
        "statement": f"Approve refund of ${request.amount:.2f} for order {request.order_id}.",
    })

    metadata: dict[str, Any] = {
        "domain": "refund-authorization",
        "compiler": "far-refund/0.1",
    }
    if request.conflicting_delivery_status:
        metadata["material_alternatives"] = ["approve-refund", "manual-review"]

    observations = (
        request.order_exists,
        request.payment_confirmed,
        request.days_since_purchase,
        request.previous_refund,
        request.agent_authorized,
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "decision_id": request.request_id,
        "decision_type": "issue_refund",
        "policy_version": request.policy_version,
        "decision_root": "approve-refund",
        "proposed_action": {
            "kind": "financial_action",
            "target": request.order_id,
            "amount": request.amount,
            "currency": "USD",
        },
        "nodes": nodes,
        "dependencies": dependencies,
        "authorization_requirements": requirements,
        "unknowns": unknowns,
        "trace_completeness": sum(value is not None for value in observations) / len(observations),
        "metadata": metadata,
    }
    return DecisionPackage.from_dict(payload)
