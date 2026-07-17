import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-004"
SPEC_PATH = BASE / "preregistration.json"
SCHEMA_PATH = BASE / "response.schema.json"
REPORT_PATH = BASE / "README.md"
SCORING_PATH = BASE / "scoring.py"

module_spec = importlib.util.spec_from_file_location("cre004_scoring", SCORING_PATH)
SCORING = importlib.util.module_from_spec(module_spec)
assert module_spec and module_spec.loader
module_spec.loader.exec_module(SCORING)


class CRE004ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.report = REPORT_PATH.read_text(encoding="utf-8")

    def response(self, **overrides):
        base = {
            "source_difference": "yes",
            "translated_difference": "yes",
            "difference_carriers": ["assigns_meaning"],
            "confidence": "certain",
        }
        base.update(overrides)
        return base

    def test_protocol_is_frozen_before_execution(self) -> None:
        self.assertEqual("CRE-004", self.spec["experiment_id"])
        self.assertEqual("frozen-before-evaluator-execution", self.spec["status"])
        self.assertEqual("CRE-003", self.spec["source_benchmark"])
        self.assertIn("does not replace or revise CRE-003", self.report)

    def test_interface_uses_plain_language_and_hides_far_terms(self) -> None:
        prompts = " ".join(question["prompt"] for question in self.spec["questions"])
        for prohibited in self.spec["prohibited_interface_terms"]:
            self.assertNotIn(prohibited, prompts)
        self.assertEqual(
            {
                "stores_objects",
                "organizes_objects",
                "assigns_meaning",
                "defines_objective",
                "determines_permitted_steps",
            },
            set(self.spec["functional_commitment_map"]),
        )

    def test_humans_and_ai_agents_share_one_response_schema(self) -> None:
        evaluator_types = self.schema["properties"]["evaluator_type"]["enum"]
        self.assertEqual(["human", "ai_agent"], evaluator_types)
        self.assertFalse(self.schema["additionalProperties"])

    def test_pass_is_derived_from_preserved_difference(self) -> None:
        result = SCORING.score_response(self.response())
        self.assertEqual("pass", result["classification"])
        self.assertFalse(result["hidden_reintroduction"])

    def test_collapsed_difference_fails(self) -> None:
        result = SCORING.score_response(
            self.response(translated_difference="no", difference_carriers=[])
        )
        self.assertEqual("fail", result["classification"])

    def test_cannot_determine_is_unknown(self) -> None:
        result = SCORING.score_response(
            self.response(translated_difference="cannot_determine", difference_carriers=[])
        )
        self.assertEqual("unknown", result["classification"])

    def test_source_denial_flags_invalid_case_response(self) -> None:
        result = SCORING.score_response(self.response(source_difference="no"))
        self.assertEqual("invalid_case_response", result["classification"])

    def test_other_function_detects_hidden_reintroduction(self) -> None:
        result = SCORING.score_response(
            self.response(difference_carriers=["other"], other_function="defines_objective")
        )
        self.assertEqual("pass", result["classification"])
        self.assertTrue(result["hidden_reintroduction"])

    def test_confidence_never_changes_classification(self) -> None:
        classifications = {
            SCORING.score_response(self.response(confidence=value))["classification"]
            for value in ["certain", "likely", "unsure"]
        }
        self.assertEqual({"pass"}, classifications)

    def test_inconsistent_responses_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SCORING.score_response(
                self.response(translated_difference="no", difference_carriers=["assigns_meaning"])
            )
        with self.assertRaises(ValueError):
            SCORING.score_response(
                self.response(difference_carriers=["cannot_determine", "assigns_meaning"])
            )
        with self.assertRaises(ValueError):
            SCORING.score_response(self.response(difference_carriers=["other"]))

    def test_complexity_is_not_assigned_by_evaluator(self) -> None:
        policy = self.spec["complexity_policy"]
        self.assertFalse(policy["evaluator_counts_complexity"])
        self.assertEqual(["A_used", "A_required", "D", "O", "L"], policy["metrics"])

    def test_blinding_and_claim_boundaries_are_frozen(self) -> None:
        forbidden = set(self.spec["blinding"]["forbidden_packet_content"])
        self.assertIn("candidate names", forbidden)
        self.assertIn("answer keys", forbidden)
        self.assertFalse(self.spec["blinding"]["candidate_repair_after_exposure"])
        boundaries = self.spec["claim_boundary"]["does_not_support"]
        self.assertIn("global minimality", boundaries)
        self.assertIn("universal reasoning coverage", boundaries)
        self.assertIn("external replication without genuinely independent evaluators and adjudication", boundaries)


if __name__ == "__main__":
    unittest.main()
