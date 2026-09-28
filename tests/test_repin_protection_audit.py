from __future__ import annotations

import unittest

from far_validation import repin_protection_audit as audit


APP_ID = 5073230


def protection(*, gate_check=None, enforce_admins=True, strict=True, force=False, delete=False):
    checks = [{"context": "merge-authority", "app_id": 15368}]
    if gate_check is not None:
        checks.append(gate_check)
    return {
        "required_status_checks": {"strict": strict, "checks": checks},
        "enforce_admins": {"enabled": enforce_admins},
        "allow_force_pushes": {"enabled": force},
        "allow_deletions": {"enabled": delete},
    }


class BootstrapProtectionAuditTests(unittest.TestCase):
    def test_unbound_baseline_is_valid(self):
        self.assertEqual([], audit.phase_aware_check_protection(protection(), APP_ID))

    def test_correct_app_bound_gate_is_valid(self):
        self.assertEqual(
            [],
            audit.phase_aware_check_protection(
                protection(gate_check={"context": "protected-repin-gate", "app_id": APP_ID}),
                APP_ID,
            ),
        )

    def test_same_name_wrong_app_is_rejected(self):
        problems = audit.phase_aware_check_protection(
            protection(gate_check={"context": "protected-repin-gate", "app_id": 15368}),
            APP_ID,
        )
        self.assertTrue(any("bound exactly" in p for p in problems), problems)

    def test_admin_enforcement_remains_required_during_bootstrap(self):
        problems = audit.phase_aware_check_protection(protection(enforce_admins=False), APP_ID)
        self.assertIn("enforce_admins must be enabled", problems)

    def test_strict_force_push_and_deletion_invariants_remain_required(self):
        problems = audit.phase_aware_check_protection(
            protection(strict=False, force=True, delete=True), APP_ID
        )
        self.assertIn(
            "required status checks must be strict (branches up to date before merging)", problems
        )
        self.assertIn("force pushes must be disabled", problems)
        self.assertIn("branch deletion must be disabled", problems)


class BoundProtectionAuditTests(unittest.TestCase):
    """After bootstrap the default audit must notice the App-bound gate check being removed."""

    def selected_check(self, argv):
        from unittest import mock
        from far_validation import repin_gate_app as gate_app
        original = gate_app.check_protection
        seen = {}

        def capture(mode):
            seen["mode"], seen["check"] = mode, gate_app.check_protection
            return 0

        try:
            with mock.patch.object(gate_app, "run_actions", capture):
                self.assertEqual(audit.main(argv), 0)
        finally:
            gate_app.check_protection = original
        self.assertEqual(seen["mode"], "audit")
        return seen["check"]

    def test_default_audit_rejects_a_dropped_gate_check(self):
        check = self.selected_check([])
        problems = check(protection(), APP_ID)
        self.assertTrue(any("protected-repin-gate" in p for p in problems), problems)

    def test_default_audit_accepts_the_bound_gate(self):
        check = self.selected_check([])
        bound = protection(gate_check={"context": "protected-repin-gate", "app_id": APP_ID})
        self.assertEqual([], check(bound, APP_ID))

    def test_default_audit_rejects_the_gate_bound_to_another_app(self):
        check = self.selected_check([])
        wrong = protection(gate_check={"context": "protected-repin-gate", "app_id": 15368})
        self.assertTrue(check(wrong, APP_ID))

    def test_bootstrap_audit_is_explicit(self):
        self.assertIs(self.selected_check(["--bootstrap"]), audit.phase_aware_check_protection)
        self.assertIs(self.selected_check([]), audit.bound_check_protection)


if __name__ == "__main__":
    unittest.main()
