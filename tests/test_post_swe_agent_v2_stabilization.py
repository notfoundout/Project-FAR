from __future__ import annotations

import unittest
from unittest import mock

from tools import check_post_swe_agent_v2_stabilization as check


class PostSweAgentV2StabilizationTests(unittest.TestCase):
    def test_repository_passes(self) -> None:
        self.assertEqual(check.main(), 0)

    def test_changed_outcome_fails(self) -> None:
        original = check.data
        def mutated(path):
            value = original(path)
            if str(path).endswith("outcome-reveal.json"):
                value["outcomes"]["v1.0.1-r1"]["resolved"] = True
            return value
        with mock.patch.object(check, "data", side_effect=mutated), self.assertRaisesRegex(SystemExit, "unexpected or malformed"):
            check.check_evidence()

    def test_missing_bounded_language_fails(self) -> None:
        original = check.read
        def mutated(path):
            value = original(path)
            return value.replace("REVIEW_REQUIRED", "PASS") if str(path) == "README.md" else value
        with mock.patch.object(check, "read", side_effect=mutated), self.assertRaisesRegex(SystemExit, "bounded status"):
            check.check_claims_and_workflows()

    def test_internal_failure_masking_fails(self) -> None:
        original = check.read
        def mutated(path):
            value = original(path)
            return value.replace("exit 75", "exit 0") if str(path).endswith("far-swe-agent-execution-v2.yml") else value
        with mock.patch.object(check, "read", side_effect=mutated), self.assertRaisesRegex(SystemExit, "not propagated"):
            check.check_claims_and_workflows()

    def test_empty_prediction_contract_removal_fails(self) -> None:
        original = check.read
        def mutated(path):
            value = original(path)
            return value.replace("not model_patch.strip()", "False") if str(path).endswith("evidence_pipeline_v2.py") else value
        with mock.patch.object(check, "read", side_effect=mutated), self.assertRaisesRegex(SystemExit, "fail-closed contract"):
            check.check_claims_and_workflows()


if __name__ == "__main__":
    unittest.main()
