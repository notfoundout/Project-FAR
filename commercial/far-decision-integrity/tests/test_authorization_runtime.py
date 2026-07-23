from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.authorization import authorize_refund, load_refund_request
from far_decision_integrity.cli import main
from far_decision_integrity.refund import RefundRequest


class TestAuthorizationRuntime(unittest.TestCase):
    def request(self, **overrides):
        values = dict(
            request_id="refund-runtime-1",
            order_id="order-1",
            amount=100.0,
            order_exists=True,
            payment_confirmed=True,
            days_since_purchase=10,
            previous_refund=False,
            agent_authorized=True,
        )
        values.update(overrides)
        return RefundRequest(**values)

    def test_writes_complete_allow_evidence_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            result = authorize_refund(self.request(), directory)
            self.assertEqual(result.disposition, "allow")
            files = {path.name for path in pathlib.Path(directory).iterdir()}
            self.assertEqual(files, {"decision-package.json", "authorization.json", "manifest.json"})
            manifest = json.loads((pathlib.Path(directory) / "manifest.json").read_text())
            self.assertEqual(manifest["disposition"], "allow")
            self.assertEqual(set(manifest["files"]), {"decision-package.json", "authorization.json"})

    def test_block_and_escalate_still_write_evidence(self):
        cases = ((self.request(payment_confirmed=False), "block"), (self.request(payment_confirmed=None), "escalate"))
        for request, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                result = authorize_refund(request, directory)
                self.assertEqual(result.disposition, expected)
                self.assertTrue((pathlib.Path(directory) / "manifest.json").exists())

    def test_installed_cli_exit_contract(self):
        payload = {
            "request_id": "refund-cli-1", "order_id": "order-1", "amount": 100,
            "order_exists": True, "payment_confirmed": False,
            "days_since_purchase": 10, "previous_refund": False,
            "agent_authorized": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "request.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            code = main(["authorize-refund", str(source), "--output-directory", str(root / "evidence")])
            self.assertEqual(code, 30)
            self.assertTrue((root / "evidence" / "authorization.json").exists())

    def test_request_loader_preserves_missing_boolean_as_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "request.json"
            path.write_text(json.dumps({"request_id": "r", "order_id": "o", "amount": 1}), encoding="utf-8")
            request = load_refund_request(path)
            self.assertIsNone(request.payment_confirmed)


if __name__ == "__main__":
    unittest.main()
