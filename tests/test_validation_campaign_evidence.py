"""The validator assurance campaign counts only evidence-bearing mutants and binds the model to the engine."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from far_validation import formal_model, mutations  # noqa: E402
from far_validation.engine import ValidationEngine  # noqa: E402
from far_validation.mutations import MutationResult  # noqa: E402


class EngineConformanceTest(unittest.TestCase):
    def test_every_small_case_runs_on_the_real_engine(self):
        self.assertEqual(2 + 2 * 4 + 8 * 8, formal_model.engine_conformance(3))

    def test_engine_divergence_from_the_model_is_detected(self):
        original = ValidationEngine.run

        def never_blocks(self, *args, **kwargs):
            summary = original(self, *args, **kwargs)
            for result in summary.results:
                if result.status == "blocked_by_root_failure":
                    result.status = "passed"
            return summary

        with mock.patch.object(ValidationEngine, "run", never_blocks):
            with self.assertRaisesRegex(AssertionError, "engine diverges from model"):
                formal_model.engine_conformance(2)


class CampaignCompositionTest(unittest.TestCase):
    def campaign(self, rule_rejected=True, static_rejected=True):
        rule = ([MutationResult("RULE-x-L1", "rule-deletion", rule_rejected)], 1)
        static = ([MutationResult("ORACLE-x-empty", "independent-oracle", static_rejected)], 1)
        with mock.patch.object(mutations, "_rule_deletion_mutations", return_value=rule), \
                mock.patch.object(mutations, "_checker_mutations", return_value=static), \
                mock.patch.object(mutations, "exhaustive_model_check", return_value={"runs": 1, "attestation_mutations": 5, "engine_conformance_runs": 1}):
            return mutations.run_campaign(ROOT)

    def test_static_oracle_texts_are_not_counted_as_mutations(self):
        report = self.campaign()
        self.assertTrue(report.successful)
        self.assertNotIn("independent-oracle", {item.detector for item in report.results})
        self.assertEqual(["ORACLE-x-empty"], [item.mutation_id for item in report.static_oracle_checks])
        self.assertIn("rule-deletion", {item.detector for item in report.results})

    def test_surviving_rule_deletion_fails_the_campaign(self):
        self.assertFalse(self.campaign(rule_rejected=False).successful)

    def test_static_oracle_failure_still_fails_the_campaign(self):
        self.assertFalse(self.campaign(static_rejected=False).successful)


if __name__ == "__main__":
    unittest.main()
