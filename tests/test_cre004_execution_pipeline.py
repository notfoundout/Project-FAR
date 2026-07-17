from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRE004 = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-004"
SPEC = importlib.util.spec_from_file_location(
    "cre004_execution_pipeline", CRE004 / "execution_pipeline.py"
)
assert SPEC is not None and SPEC.loader is not None
PIPELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PIPELINE)


class CRE004ExecutionPipelineTests(unittest.TestCase):
    def manifest(self):
        return {
            "execution_id": "CRE-004-TEST",
            "protocol_version": "CRE-004-v1.0",
            "randomization_seed": 7,
            "expected_case_labels": ["CASE_001"],
            "expected_candidate_labels": ["CANDIDATE_001"],
            "eligible_evaluators": [
                {
                    "evaluator_id": "EVALUATOR_001",
                    "evaluator_type": "human",
                    "calibration_passed": True,
                    "independence_claim": "internal",
                }
            ],
        }

    def response(self):
        return {
            "protocol_version": "CRE-004-v1.0",
            "evaluator_id": "EVALUATOR_001",
            "evaluator_type": "human",
            "case_label": "CASE_001",
            "candidate_label": "CANDIDATE_001",
            "source_difference": "yes",
            "translated_difference": "yes",
            "difference_carriers": ["stores_objects"],
            "confidence": "certain",
            "submitted_at": "2026-07-17T00:00:00Z",
            "_source_file": "response.json",
        }

    def test_frozen_protocol_lock_matches_repository(self):
        checked = PIPELINE.verify_protocol_lock(CRE004)
        self.assertEqual(
            set(checked),
            {
                "preregistration.json",
                "response.schema.json",
                "scoring.py",
                "evaluator_packet.md",
            },
        )

    def test_valid_response_scores_deterministically(self):
        scored = PIPELINE.validate_and_score(
            self.manifest(), [self.response()], CRE004
        )
        self.assertEqual(scored[0]["classification"], "pass")
        self.assertFalse(scored[0]["hidden_reintroduction"])

    def test_uncalibrated_evaluator_is_rejected(self):
        manifest = self.manifest()
        manifest["eligible_evaluators"][0]["calibration_passed"] = False
        with self.assertRaisesRegex(ValueError, "has not passed calibration"):
            PIPELINE.validate_and_score(manifest, [self.response()], CRE004)

    def test_duplicate_response_tuple_is_rejected(self):
        response_a = self.response()
        response_b = self.response()
        response_b["_source_file"] = "duplicate.json"
        with self.assertRaisesRegex(ValueError, "duplicate evaluator/case/candidate"):
            PIPELINE.validate_and_score(
                self.manifest(), [response_a, response_b], CRE004
            )

    def test_unregistered_response_field_is_rejected(self):
        response = self.response()
        response["manual_score"] = "pass"
        with self.assertRaisesRegex(ValueError, "unregistered response fields"):
            PIPELINE.validate_and_score(self.manifest(), [response], CRE004)

    def test_aggregation_is_order_independent(self):
        first = self.response()
        second = self.response()
        second["evaluator_id"] = "EVALUATOR_002"
        second["translated_difference"] = "no"
        second["difference_carriers"] = []
        second["_source_file"] = "second.json"
        manifest = self.manifest()
        manifest["eligible_evaluators"].append(
            {
                "evaluator_id": "EVALUATOR_002",
                "evaluator_type": "ai_agent",
                "calibration_passed": True,
                "independence_claim": "internal",
            }
        )
        scored_a = PIPELINE.validate_and_score(manifest, [first.copy(), second.copy()], CRE004)
        scored_b = PIPELINE.validate_and_score(manifest, [second.copy(), first.copy()], CRE004)
        self.assertEqual(PIPELINE.aggregate(scored_a), PIPELINE.aggregate(scored_b))

    def test_replay_outputs_are_byte_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            responses = temp_path / "responses"
            output_a = temp_path / "output-a"
            output_b = temp_path / "output-b"
            responses.mkdir()
            manifest_path = temp_path / "manifest.json"
            manifest_path.write_text(json.dumps(self.manifest()), encoding="utf-8")
            response = self.response()
            response.pop("_source_file")
            (responses / "response.json").write_text(
                json.dumps(response), encoding="utf-8"
            )
            PIPELINE.replay(manifest_path, responses, output_a)
            PIPELINE.replay(manifest_path, responses, output_b)
            for filename in ("results.csv", "summary.json"):
                self.assertEqual(
                    (output_a / filename).read_bytes(),
                    (output_b / filename).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
