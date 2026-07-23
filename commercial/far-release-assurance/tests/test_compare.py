from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_release_assurance.cli import main
from far_release_assurance.compare import compare_releases, comparison_to_dict
from far_release_assurance.io import write_package
from far_release_assurance.model import Decision
from far_release_assurance.reference_agent import (
    AgentConfiguration,
    baseline_configuration,
    run_reference_agent,
)


class TestReleaseComparison(unittest.TestCase):
    def setUp(self):
        self.baseline = run_reference_agent(baseline_configuration()).package

    def compare(self, config: AgentConfiguration):
        return compare_releases(self.baseline, run_reference_agent(config).package)

    def test_identical_release_passes(self):
        summary = compare_releases(self.baseline, self.baseline)
        self.assertEqual(summary.comparison.decision, Decision.PASS)
        self.assertEqual(summary.machinery.added, ())
        self.assertEqual(summary.machinery.changed, ())
        self.assertEqual(summary.output_metric_deltas, {"accuracy": 0.0})

    def test_undeclared_dependency_is_blocked(self):
        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-unauthorized",
                source_commit="candidate-1",
                customer_source="shadow-customer-db",
                customer_source_declared=False,
            )
        )
        self.assertEqual(summary.comparison.decision, Decision.BLOCKED)
        self.assertIn("customer-data", summary.machinery.changed)
        self.assertIn(
            "machinery-disclosure-regression",
            {finding.rule_id for finding in summary.comparison.findings},
        )

    def test_mutable_unversioned_policy_is_blocked(self):
        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-policy",
                source_commit="candidate-2",
                policy_source="https://policy.example/current",
                policy_version=None,
                policy_mutable=True,
            )
        )
        self.assertEqual(summary.comparison.decision, Decision.BLOCKED)
        self.assertIn(
            "policy-version-regression",
            {finding.rule_id for finding in summary.comparison.findings},
        )

    def test_invalidated_support_is_blocked(self):
        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-invalidated",
                source_commit="candidate-3",
                invalidate_eligibility_support=True,
                withdraw_dependent_conclusion=False,
            )
        )
        self.assertEqual(summary.comparison.decision, Decision.BLOCKED)
        self.assertIn(
            "invalidated-support-not-propagated",
            {finding.rule_id for finding in summary.comparison.findings},
        )

    def test_identity_drift_is_blocked(self):
        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-identity",
                source_commit="candidate-4",
                customer_id_after_handoff="customer-999",
                revalidate_identity=False,
            )
        )
        self.assertEqual(summary.comparison.decision, Decision.BLOCKED)
        self.assertEqual(summary.event_type_deltas["identity_changed"], 1)

    def test_unresolved_external_state_is_unknown(self):
        from far_release_assurance.model import EvidenceStatus

        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-external",
                source_commit="candidate-5",
                external_state_source="remote-state",
                external_state_status=EvidenceStatus.UNKNOWN,
            )
        )
        self.assertEqual(summary.comparison.decision, Decision.UNKNOWN)
        self.assertIn("external-state", summary.machinery.added)
        self.assertIn("external-state", summary.machinery.newly_unresolved)

    def test_replay_regression_requires_review(self):
        from dataclasses import replace

        candidate = replace(
            self.baseline,
            release_id="candidate-replay",
            source_commit="candidate-6",
            replay_completeness=0.75,
        )
        summary = compare_releases(self.baseline, candidate)
        self.assertEqual(summary.comparison.decision, Decision.REVIEW_REQUIRED)
        self.assertAlmostEqual(summary.replay_delta, -0.25)

    def test_output_metric_improvement_is_reported_not_used_to_cancel_block(self):
        summary = self.compare(
            AgentConfiguration(
                release_id="candidate-metric",
                source_commit="candidate-7",
                customer_source="shadow-customer-db",
                customer_source_declared=False,
            )
        )
        self.assertEqual(summary.output_metric_deltas["accuracy"], 0.0)
        self.assertEqual(summary.comparison.decision, Decision.BLOCKED)

    def test_serialization_is_deterministic(self):
        summary = compare_releases(self.baseline, self.baseline)
        first = json.dumps(comparison_to_dict(summary), sort_keys=True)
        second = json.dumps(comparison_to_dict(summary), sort_keys=True)
        self.assertEqual(first, second)

    def test_cli_compare_emits_versioned_result(self):
        candidate = run_reference_agent(
            AgentConfiguration(
                release_id="candidate-cli",
                source_commit="candidate-8",
                policy_source="https://policy.example/current",
                policy_version=None,
                policy_mutable=True,
            )
        ).package
        with tempfile.TemporaryDirectory() as directory:
            baseline_path = pathlib.Path(directory) / "baseline.json"
            candidate_path = pathlib.Path(directory) / "candidate.json"
            output_path = pathlib.Path(directory) / "comparison.json"
            write_package(self.baseline, baseline_path)
            write_package(candidate, candidate_path)
            code = main(
                [
                    "compare",
                    "--baseline",
                    str(baseline_path),
                    "--candidate",
                    str(candidate_path),
                    "--output",
                    str(output_path),
                ]
            )
            self.assertEqual(code, 0)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "far-release-comparison/0.1")
            self.assertEqual(payload["decision"], "blocked")


if __name__ == "__main__":
    unittest.main()
