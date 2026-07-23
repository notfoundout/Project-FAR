from __future__ import annotations

import unittest

from far_decision_integrity.policy_impact import (
    ImpactDecision,
    PolicyDisposition,
    RefundPolicy,
    compare_policies,
    evaluate_refund,
)
from far_decision_integrity.refund import RefundRequest


def request(request_id: str, amount: float = 100.0, **overrides) -> RefundRequest:
    values = {
        "request_id": request_id,
        "order_id": f"order-{request_id}",
        "amount": amount,
        "order_exists": True,
        "payment_confirmed": True,
        "days_since_purchase": 10,
        "previous_refund": False,
        "agent_authorized": True,
    }
    values.update(overrides)
    return RefundRequest(**values)


class TestPolicyImpact(unittest.TestCase):
    def test_identical_policy_passes(self):
        baseline = RefundPolicy("refund/1")
        candidate = RefundPolicy("refund/2")
        report = compare_policies(baseline, candidate, [request("a")])
        self.assertEqual(report.decision, ImpactDecision.PASS)
        self.assertEqual(report.changed_rules, ())
        self.assertFalse(report.cases[0].changed)

    def test_expanded_authorization_blocks_gate(self):
        baseline = RefundPolicy("refund/1", auto_approval_limit=500.0)
        candidate = RefundPolicy("refund/2", auto_approval_limit=1000.0)
        report = compare_policies(baseline, candidate, [request("high", amount=750.0)])
        self.assertEqual(report.decision, ImpactDecision.BLOCKED)
        self.assertEqual(report.changed_rules, ("auto_approval_limit",))
        self.assertEqual(report.cases[0].direction, "authorization-expanded")

    def test_restricted_authorization_requires_review(self):
        baseline = RefundPolicy("refund/1", approval_window_days=30)
        candidate = RefundPolicy("refund/2", approval_window_days=7)
        report = compare_policies(baseline, candidate, [request("late", days_since_purchase=10)])
        self.assertEqual(report.decision, ImpactDecision.REVIEW)
        self.assertEqual(report.cases[0].direction, "authorization-restricted")

    def test_missing_fact_escalates_under_both_versions(self):
        policy = RefundPolicy("refund/1")
        case = request("unknown", payment_confirmed=None)
        self.assertEqual(evaluate_refund(case, policy), PolicyDisposition.ESCALATE)

    def test_case_order_is_deterministic(self):
        policy = RefundPolicy("refund/1")
        report = compare_policies(policy, RefundPolicy("refund/2"), [request("z"), request("a")])
        self.assertEqual([case.request_id for case in report.cases], ["a", "z"])

    def test_invalid_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            RefundPolicy("refund/2", auto_approval_limit=-1)


if __name__ == "__main__":
    unittest.main()
