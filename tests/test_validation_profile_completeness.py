"""The CI validation profiles must run every registered check except explicitly superseded ones.

`selection.completeness` only requires each check to belong to *some* profile, so deleting a check
from `pr-full` (the profile CI and the merge-authority job run) previously passed every validator.
This pins the exact exclusion set so removing a check from the gate is an explicit, reviewable
change rather than a silent one.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "validation" / "manifest.json"

# Checks deliberately outside the complete gate, with the reason each is superseded.
SUPERSEDED = {
    "environment.doctor": "environment diagnosis only; it validates no repository artifact",
    "repository.health-fast": "strict subset of repository.health-full, which the complete profiles run",
}
COMPLETE_PROFILES = ("pr-full", "full", "release", "health")


class ValidationProfileCompletenessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.checks = {check["id"] for check in self.manifest["checks"]}

    def test_superseded_checks_are_real(self) -> None:
        self.assertLessEqual(set(SUPERSEDED), self.checks)

    def test_complete_profiles_run_every_non_superseded_check(self) -> None:
        for profile in COMPLETE_PROFILES:
            with self.subTest(profile=profile):
                selected = set(self.manifest["profiles"][profile])
                self.assertEqual(sorted(self.checks - set(SUPERSEDED) - selected), [])
                self.assertLessEqual(selected, self.checks)

    def test_validator_change_profile_runs_everything_but_the_fast_health_subset(self) -> None:
        selected = set(self.manifest["profiles"]["validator-change"])
        self.assertEqual(self.checks - selected, {"repository.health-fast"})

    def test_protected_checks_are_in_every_complete_profile(self) -> None:
        for profile in COMPLETE_PROFILES:
            with self.subTest(profile=profile):
                self.assertLessEqual(set(self.manifest["protected_checks"]), set(self.manifest["profiles"][profile]))


if __name__ == "__main__":
    unittest.main()
