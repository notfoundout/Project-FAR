from __future__ import annotations

import unittest

from far_decision_integrity.adjudicate import adjudicate
from far_decision_integrity.instrumentation import DecisionSession, InstrumentationError
from far_decision_integrity.model import IntegrityStatus
from far_decision_integrity.trace_ingest import ingest_trace


class Ids:
    def __init__(self) -> None:
        self.value = 0

    def __call__(self) -> str:
        self.value += 1
        return f"span-{self.value}"


def session() -> DecisionSession:
    return DecisionSession(
        "refund-1",
        "issue_refund",
        "refund-policy/2026-07",
        "approve",
        {"kind": "financial_action", "amount": 100},
        trace_id="trace-1",
        span_id_factory=Ids(),
    )


class TestInstrumentation(unittest.TestCase):
    def test_round_trip_preserves_commitments(self):
        sdk = session()
        sdk.record_evidence(
            "payment",
            "Payment confirmed.",
            attributes={"valid": True},
            supports="approve",
            authorization_required=True,
        )
        sdk.record_rule(
            "policy",
            "Refund policy authorizes the action.",
            supports="approve",
            relation="authorizes",
            authorization_required=True,
        )
        sdk.record_conclusion("approve", "Approve refund.")
        package = ingest_trace(sdk.finish(claim_complete=True))
        self.assertEqual(package.decision_id, "refund-1")
        self.assertEqual(package.authorization_requirements, ("payment", "policy"))
        self.assertEqual(adjudicate(package).status, IntegrityStatus.JUSTIFIED)

    def test_context_manager_finalizes(self):
        with session() as sdk:
            sdk.record_conclusion("approve", "Approve refund.")
        self.assertEqual(sdk.trace["spans"][0]["attributes"]["far.decision.id"], "refund-1")

    def test_unknowns_are_preserved(self):
        sdk = session()
        sdk.record_conclusion("approve", "Approve refund.")
        sdk.declare_unknown("delivery-status")
        package = ingest_trace(sdk.finish())
        self.assertEqual(package.unknowns, ("delivery-status",))
        self.assertEqual(adjudicate(package).status, IntegrityStatus.UNVERIFIABLE)

    def test_complete_claim_rejects_unknowns(self):
        sdk = session()
        sdk.record_conclusion("approve", "Approve refund.")
        sdk.declare_unknown("delivery-status")
        with self.assertRaisesRegex(InstrumentationError, "cannot claim a complete trace"):
            sdk.finish(claim_complete=True)

    def test_missing_root_is_rejected(self):
        sdk = session()
        sdk.record_evidence("payment", "Payment confirmed.")
        with self.assertRaisesRegex(InstrumentationError, "decision_root"):
            sdk.finish()

    def test_dangling_dependency_is_rejected(self):
        sdk = session()
        sdk.record_conclusion("approve", "Approve refund.", supports="missing")
        with self.assertRaisesRegex(InstrumentationError, "dependency targets"):
            sdk.finish()

    def test_duplicate_node_is_rejected(self):
        sdk = session()
        sdk.record_conclusion("approve", "Approve refund.")
        with self.assertRaisesRegex(InstrumentationError, "duplicate node_id"):
            sdk.record_conclusion("approve", "Duplicate.")

    def test_finalized_session_is_immutable(self):
        sdk = session()
        sdk.record_conclusion("approve", "Approve refund.")
        sdk.finish()
        with self.assertRaisesRegex(InstrumentationError, "already finalized"):
            sdk.declare_unknown("later")


if __name__ == "__main__":
    unittest.main()
