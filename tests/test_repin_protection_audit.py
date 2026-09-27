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


if __name__ == "__main__":
    unittest.main()
