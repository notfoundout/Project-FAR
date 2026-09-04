from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_validation_protection.py"
SPEC = importlib.util.spec_from_file_location("check_validation_protection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
PROTECTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROTECTION)


def compliant_readback() -> dict:
    actual = {
        "required_status_checks": {"strict": True, "contexts": ["merge-authority"]},
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
        },
    }
    for field, enabled in {
        "enforce_admins": True, "required_conversation_resolution": True,
        "required_linear_history": False, "allow_force_pushes": False,
        "allow_deletions": False, "block_creations": False,
        "required_signatures": False, "lock_branch": False, "allow_fork_syncing": False,
    }.items():
        actual[field] = {"enabled": enabled}
    return actual


class CheckValidationProtectionTests(unittest.TestCase):
    def test_exact_policy_passes_readback(self) -> None:
        self.assertEqual(PROTECTION.protection_errors(compliant_readback()), [])

    def test_missing_merge_authority_fails(self) -> None:
        actual = compliant_readback()
        actual["required_status_checks"]["contexts"] = []
        self.assertTrue(PROTECTION.protection_errors(actual))

    def test_non_strict_checks_and_admin_bypass_fail(self) -> None:
        actual = compliant_readback()
        actual["required_status_checks"]["strict"] = False
        actual["enforce_admins"]["enabled"] = False
        errors = PROTECTION.protection_errors(actual)
        self.assertTrue(any("strict" in error for error in errors))
        self.assertTrue(any("administrator" in error for error in errors))

    def test_force_push_or_deletion_fails(self) -> None:
        for field in ("allow_force_pushes", "allow_deletions"):
            with self.subTest(field=field):
                actual = copy.deepcopy(compliant_readback())
                actual[field]["enabled"] = True
                self.assertTrue(PROTECTION.protection_errors(actual))


if __name__ == "__main__":
    unittest.main()
