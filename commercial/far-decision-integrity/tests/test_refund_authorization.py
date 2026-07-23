from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.authorize import RuntimeDisposition, authorize
from far_decision_integrity.model import IntegrityStatus
from far_decision_integrity.refund import REFUND_POLICY_VERSION, RefundRequest, build_refund_package


def request(**overrides):
    values = {
        "request_id": "refund-1042",
        "order_id": "order-8831",
        "amount": 480.0,
        "order_exists": True,
        "payment_confirmed": True,
        "days_since_purchase": 12,
        "previous_refund": False,
        "agent_authorized": True,
    }
    values.update(overrides)
    return RefundRequest(**values)


class TestRefundAuthorization(unittest.TestCase):
    def test_justified_request_is_allowed(self):
        result = authorize(build_refund_package(request()))
        self.assertEqual(result.disposition, RuntimeDisposition.ALLOW)
        self.assertEqual(result.adjudication.status, IntegrityStatus.JUSTIFIED)

    def test_missing_payment_is_escalated_as_unverifiable(self):
        result = authorize(build_refund_package(request(payment_confirmed=None)))
        self.assertEqual(result.disposition, RuntimeDisposition.ESCALATE)
        self.assertEqual(result.adjudication.status, IntegrityStatus.UNVERIFIABLE)

    def test_failed_payment_is_blocked_as_unsupported(self):
        result = authorize(build_refund_package(request(payment_confirmed=False)))
        self.assertEqual(result.disposition, RuntimeDisposition.BLOCK)
        self.assertEqual(result.adjudication.status, IntegrityStatus.UNSUPPORTED)

    def test_expired_policy_is_blocked(self):
        result = authorize(build_refund_package(request(policy_version="refund-policy/2025-01")))
        self.assertEqual(result.disposition, RuntimeDisposition.BLOCK)
        self.assertIn("required-node-invalid", {f.rule_id for f in result.adjudication.findings})

    def test_conflicting_material_outcomes_are_escalated(self):
        result = authorize(build_refund_package(request(conflicting_delivery_status=True)))
        self.assertEqual(result.disposition, RuntimeDisposition.ESCALATE)
        self.assertEqual(result.adjudication.status, IntegrityStatus.UNDERDETERMINED)

    def test_amount_above_limit_is_blocked(self):
        result = authorize(build_refund_package(request(amount=750.0)))
        self.assertEqual(result.disposition, RuntimeDisposition.BLOCK)

    def test_previous_refund_is_blocked(self):
        result = authorize(build_refund_package(request(previous_refund=True)))
        self.assertEqual(result.disposition, RuntimeDisposition.BLOCK)

    def test_policy_version_is_frozen(self):
        package = build_refund_package(request())
        self.assertEqual(package.policy_version, REFUND_POLICY_VERSION)
        self.assertEqual(package.metadata["compiler"], "far-refund/0.1")


if __name__ == "__main__":
    unittest.main()
