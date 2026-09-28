"""CLI boundary regressions for the security-sensitive repin protection audit."""
from __future__ import annotations

import unittest
from unittest import mock

from far_validation import repin_gate_app as gate_app
from far_validation import repin_protection_audit as audit


class RepinProtectionAuditCliTests(unittest.TestCase):
    def test_bootstrap_mode_requires_its_exact_option_name(self) -> None:
        original = gate_app.check_protection
        try:
            with mock.patch.object(gate_app, "run_actions", return_value=0):
                self.assertEqual(audit.main(["--bootstrap"]), 0)
                with self.assertRaises(SystemExit) as raised:
                    audit.main(["--boot"])
                self.assertEqual(raised.exception.code, 2)
        finally:
            gate_app.check_protection = original


if __name__ == "__main__":
    unittest.main()
