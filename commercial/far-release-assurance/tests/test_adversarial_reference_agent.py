from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_release_assurance.adversarial import run_all_scenarios
from far_release_assurance.model import ClosureStatus, Decision
from far_release_assurance.reference_agent import baseline_configuration, run_reference_agent


class TestReferenceAgent(unittest.TestCase):
    def test_baseline_is_closed_and_deterministic(self):
        first = run_reference_agent(baseline_configuration())
        second = run_reference_agent(baseline_configuration())
        self.assertEqual(first, second)
        self.assertEqual(first.output, "REFUND_APPROVED")
        self.assertTrue(first.package.events)
        self.assertEqual(first.package.replay_completeness, 1.0)

    def test_all_required_scenarios_preserve_output(self):
        results = run_all_scenarios()
        self.assertEqual(len(results), 7)
        self.assertTrue(all(result.conventional_output_test_passed for result in results))
        self.assertTrue(all(result.baseline.output == "REFUND_APPROVED" for result in results))
        self.assertTrue(all(result.candidate.output == "REFUND_APPROVED" for result in results))

    def test_far_prevents_every_adversarial_candidate_from_passing(self):
        results = run_all_scenarios()
        self.assertTrue(all(result.comparison.decision is not Decision.PASS for result in results))

    def test_expected_decisions(self):
        decisions = {result.scenario_id: result.comparison.decision for result in run_all_scenarios()}
        self.assertEqual(decisions["unauthorized-dependency"], Decision.BLOCKED)
        self.assertEqual(decisions["stale-policy"], Decision.BLOCKED)
        self.assertEqual(decisions["invalidated-support"], Decision.BLOCKED)
        self.assertEqual(decisions["hidden-memory"], Decision.BLOCKED)
        self.assertEqual(decisions["identity-drift"], Decision.BLOCKED)
        self.assertEqual(decisions["benchmark-leakage"], Decision.BLOCKED)
        self.assertEqual(decisions["same-output-different-integrity"], Decision.UNKNOWN)

    def test_each_scenario_has_actionable_evidence(self):
        for result in run_all_scenarios():
            with self.subTest(result.scenario_id):
                self.assertTrue(result.comparison.findings)
                self.assertTrue(all(finding.rationale for finding in result.comparison.findings))
                self.assertTrue(all(finding.affected_ids for finding in result.comparison.findings))
                self.assertNotEqual(result.comparison.candidate_closure.status, ClosureStatus.CLOSED if result.scenario_id in {"unauthorized-dependency", "hidden-memory", "same-output-different-integrity"} else ClosureStatus.OPEN)

    def test_scenario_order_and_results_are_stable(self):
        first = run_all_scenarios()
        second = run_all_scenarios()
        self.assertEqual(first, second)
        self.assertEqual(
            tuple(result.scenario_id for result in first),
            (
                "unauthorized-dependency",
                "stale-policy",
                "invalidated-support",
                "hidden-memory",
                "identity-drift",
                "benchmark-leakage",
                "same-output-different-integrity",
            ),
        )


if __name__ == "__main__":
    unittest.main()
