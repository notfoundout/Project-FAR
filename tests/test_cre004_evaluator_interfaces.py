from __future__ import annotations

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-004"


class CRE004EvaluatorInterfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.preregistration = json.loads((BASE / "preregistration.json").read_text(encoding="utf-8"))
        self.schema = json.loads((BASE / "response.schema.json").read_text(encoding="utf-8"))
        self.human_form = (BASE / "human_response_form.html").read_text(encoding="utf-8")
        self.ai_template = json.loads((BASE / "ai_response_template.json").read_text(encoding="utf-8"))

    def test_human_form_exposes_every_frozen_question_and_choice(self) -> None:
        for question in self.preregistration["questions"]:
            self.assertIn(question["id"], self.human_form)
            for choice in question["choices"]:
                self.assertIn(choice, self.human_form)

    def test_human_form_does_not_expose_prohibited_terms(self) -> None:
        for term in self.preregistration["prohibited_interface_terms"]:
            self.assertNotIn(term, self.human_form)

    def test_human_form_exports_protocol_fields_without_manual_scoring(self) -> None:
        for field in self.schema["required"]:
            self.assertIn(field, self.human_form)
        for prohibited in ("manual_score", "classification", "hidden_reintroduction"):
            self.assertNotIn(prohibited, self.human_form)

    def test_ai_template_uses_same_required_schema(self) -> None:
        self.assertEqual(set(self.schema["required"]), set(self.ai_template) - {"other_function"})
        self.assertEqual("CRE-004-v1.0", self.ai_template["protocol_version"])
        self.assertEqual("ai_agent", self.ai_template["evaluator_type"])

    def test_human_and_ai_interfaces_share_frozen_choice_tokens(self) -> None:
        for question in self.preregistration["questions"]:
            for choice in question["choices"]:
                self.assertIn(choice, self.human_form)
                self.assertIn(choice, json.dumps(self.ai_template, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
