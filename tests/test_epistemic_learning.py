from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import unittest
import jsonschema

from mechanization.far_mechanization.epistemic import (
    EpistemicDocument, EpistemicValidationError, calibration, migrate, recurring_failure_modes, score_binary,
)

ROOT = Path(__file__).parents[1]
FIXTURE = ROOT / "examples/epistemic/complete-learning-loop.json"


class EpistemicLearningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assert_invalid(self, mutate, message: str) -> None:
        value = deepcopy(self.data)
        mutate(value)
        with self.assertRaises(EpistemicValidationError) as caught:
            EpistemicDocument.from_dict(value)
        self.assertIn(message, str(caught.exception))

    def test_complete_loop_round_trip_and_audit_commitment(self) -> None:
        schema = json.loads((ROOT / "schemas/far-epistemic-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual([], list(jsonschema.Draft202012Validator(schema).iter_errors(self.data)))
        document = EpistemicDocument.from_dict(self.data)
        restored = EpistemicDocument.loads(document.dumps())
        self.assertEqual(document, restored)
        self.assertEqual(document.digest, restored.digest)
        self.assertEqual([r["kind"] for r in restored.to_dict()["records"]],
                         ["belief", "causal_model", "dialectic", "prediction", "decision", "error"])
        event = restored.audit_event()
        self.assertTrue(event["valid"])
        self.assertEqual(restored.digest, event["content_hash"])

    def test_scoring_math_and_boundaries(self) -> None:
        self.assertEqual(Decimal("0.04"), score_binary("0.8", 1)["brier"])
        self.assertAlmostEqual(-__import__("math").log(0.8), float(score_binary("0.8", 1)["log"]), places=14)
        for probability in (0, 1, -0.1, 1.1, True):
            with self.assertRaises(EpistemicValidationError):
                score_binary(probability, 1)

    def test_longitudinal_calibration(self) -> None:
        result = calibration([
            {"probability": 0.2, "outcome": 0}, {"probability": 0.4, "outcome": 1},
            {"probability": 0.8, "outcome": 1}, {"probability": 0.9, "outcome": 1},
        ], bins=2)
        self.assertEqual("0.3", result["bins"][0]["mean_probability"])
        self.assertEqual("0.5", result["bins"][0]["observed_frequency"])
        self.assertEqual("0.1125", result["mean_brier"])
        with self.assertRaises(EpistemicValidationError): calibration([], bins=0)

    def test_competing_hypothesis_and_update_invariants(self) -> None:
        self.assert_invalid(lambda d: d["records"][0]["hypotheses"][0].update(confidence=0.4), "confidences must sum exactly to 1")
        self.assert_invalid(lambda d: d["records"][0]["hypotheses"][0].update(prior_probability=0.4), "priors must sum exactly to 1")
        self.assert_invalid(lambda d: d["records"][0]["evidence_updates"][0]["posterior"].pop("h.dry"), "must contain exactly all hypothesis ids")
        self.assert_invalid(lambda d: d["records"][0]["hypotheses"][0].update(falsifiers=[]), "non-empty array required")
        self.assert_invalid(lambda d: d["records"][0]["revision_history"].reverse(), "revision history must be chronological")

    def test_prediction_resolution_and_snapshot_invariants(self) -> None:
        self.assert_invalid(lambda d: d["records"][3].update(outcome=None), "unresolved prediction cannot have scores")
        self.assert_invalid(lambda d: d["records"][3]["scores"].update(brier=0.2), "does not match computed score")
        self.assert_invalid(lambda d: d["records"][3].update(evidence_snapshot_hash="sha256:other"), "must equal provenance content_hash")

    def test_decision_math_and_semantic_separation(self) -> None:
        self.assert_invalid(lambda d: d["records"][4]["actions"][0].update(expected_utility=99), "expected 0.2")
        self.assert_invalid(lambda d: d["records"][4].update(opportunity_cost=3), "expected 0.0")
        self.assert_invalid(lambda d: d["records"][4].update(value_of_information=3), "expected 2.4")
        self.assert_invalid(lambda d: d["records"][4].update(regret=-1), "expected 0")
        self.assert_invalid(lambda d: d["records"][4].update(approximation_cost=1), "field is not valid for decision records")
        self.assert_invalid(lambda d: d["records"][0].update(utility=4), "field is not valid for belief records")

    def test_causal_graph_and_cross_record_references(self) -> None:
        self.assert_invalid(lambda d: d["records"][1]["edges"].append({"cause": "rain", "effect": "front", "mechanism": "bad cycle"}), "causal graph must be acyclic")
        self.assert_invalid(lambda d: d["records"][5].update(prediction_ref="missing"), "unknown record id")
        self.assert_invalid(lambda d: d["records"][5]["linked_record_ids"].append("missing"), "unknown record id missing")

    def test_recurring_failure_mode_detection(self) -> None:
        error = self.data["records"][5]
        second = deepcopy(error); second["id"] = "error.weather.2"
        modes = recurring_failure_modes([error, second])
        self.assertEqual(2, modes[0]["count"])
        self.assertEqual(["error.weather.1", "error.weather.2"], modes[0]["record_ids"])
        self.assertEqual([], recurring_failure_modes([error]))

    def test_migration_is_loss_explicit_and_validated(self) -> None:
        legacy = deepcopy(self.data)
        legacy["format_version"] = "far-epistemic/0.9"
        prediction = legacy["records"][3]
        prediction["resolution_date"] = prediction.pop("resolution_window_start")
        prediction.pop("resolution_window_end")
        migrated = migrate(legacy)
        self.assertEqual("far-epistemic/1.0", migrated["format_version"])
        self.assertEqual(migrated["records"][3]["resolution_window_start"], migrated["records"][3]["resolution_window_end"])
        broken = deepcopy(legacy); broken["records"][0].pop("provenance")
        with self.assertRaises(EpistemicValidationError): migrate(broken)

    def test_cli_validation_calibration_and_migration(self) -> None:
        base = [sys.executable, "-m", "mechanization.far_mechanization.cli", "epistemic"]
        checked = subprocess.run(base + ["validate", str(FIXTURE)], cwd=ROOT, check=True, text=True, capture_output=True)
        self.assertTrue(json.loads(checked.stdout)["valid"])
        calibrated = subprocess.run(base + ["calibration", str(FIXTURE), "--bins", "2"], cwd=ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(1, json.loads(calibrated.stdout)["resolved_count"])


if __name__ == "__main__":
    unittest.main()
