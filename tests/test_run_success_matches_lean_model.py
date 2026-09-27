"""A validation run succeeds only when every selected result passed, as the Lean model proves."""
from __future__ import annotations

import typing
import unittest

from far_validation.model import CheckResult, CheckStatus, RunSummary


def _summary(*statuses: str) -> RunSummary:
    return RunSummary(
        run_id="r", profile="p", selected_checks=[f"c{i}" for i in range(len(statuses))],
        results=[CheckResult(check_id=f"c{i}", title="t", status=status) for i, status in enumerate(statuses)],
        repository_root=".", commit_sha="0" * 40, base_sha="0" * 40, manifest_hash="h",
        started_at="", finished_at="", duration_ms=0,
    )


class RunSuccessMatchesLeanModelTests(unittest.TestCase):
    def test_only_passed_is_a_successful_result(self) -> None:
        for status in typing.get_args(CheckStatus):
            with self.subTest(status=status):
                self.assertEqual(CheckResult(check_id="c", title="t", status=status).successful, status == "passed")

    def test_any_result_that_did_not_pass_fails_the_run(self) -> None:
        self.assertTrue(_summary("passed", "passed").successful)
        for status in typing.get_args(CheckStatus):
            if status != "passed":
                with self.subTest(status=status):
                    self.assertFalse(_summary("passed", status).successful)
                    self.assertFalse(_summary(status).successful)

    def test_an_empty_run_is_not_successful(self) -> None:
        self.assertFalse(_summary().successful)


if __name__ == "__main__":
    unittest.main()
