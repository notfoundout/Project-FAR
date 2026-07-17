import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "evaluation" / "comparative-representation" / "experiments" / "CRE-004"


class CRE004EvaluatorPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = (BASE / "evaluator_packet.md").read_text(encoding="utf-8")
        self.tree = (BASE / "decision_tree.md").read_text(encoding="utf-8")
        self.scoring = (BASE / "automatic_scoring.md").read_text(encoding="utf-8")
        self.hidden = (BASE / "hidden_reintroduction.md").read_text(encoding="utf-8")
        self.calibration = json.loads((BASE / "calibration_cases.json").read_text(encoding="utf-8"))

    def test_evaluator_packet_is_plain_language_and_blind(self) -> None:
        forbidden = (
            "Project FAR",
            "Representational Structure",
            "Reasoning Calculus",
            "AV-001",
            "CRE-003",
        )
        for term in forbidden:
            self.assertNotIn(term, self.packet)
        for answer in ("yes", "no", "cannot_determine", "certain", "likely", "unsure"):
            self.assertIn(f"`{answer}`", self.packet)

    def test_evaluator_never_selects_scientific_classification(self) -> None:
        self.assertIn("must not", self.packet)
        self.assertIn("choose `pass`, `fail`, `unknown`", self.packet)
        self.assertIn("Confidence is metadata only", self.packet)

    def test_decision_tree_covers_all_primary_outcomes(self) -> None:
        for outcome in ("pass", "fail", "unknown", "invalid_case_response"):
            self.assertIn(f"`{outcome}`", self.tree)
        self.assertIn("Confidence never changes", self.tree)

    def test_hidden_reintroduction_is_functional_not_lexical(self) -> None:
        self.assertIn("behavioral and commitment-based, not lexical", self.hidden)
        for function in (
            "stores explicit reasoning objects",
            "organizes those objects",
            "assigns meaning",
            "defines the objective",
            "determines permitted inference",
        ):
            self.assertIn(function, self.hidden)
        self.assertIn("must not be forced", self.hidden)

    def test_calibration_is_unrelated_and_complete(self) -> None:
        self.assertEqual("1.0", self.calibration["version"])
        self.assertEqual(3, len(self.calibration["cases"]))
        self.assertIn("unrelated", self.calibration["purpose"].lower())
        observed = {case["case_id"] for case in self.calibration["cases"]}
        self.assertEqual({"CAL-001", "CAL-002", "CAL-003"}, observed)
        for case in self.calibration["cases"]:
            self.assertIn(case["expected_source_difference"], {"yes", "no", "cannot_determine"})
            self.assertIn(case["expected_translated_distinction"], {"yes", "no", "cannot_determine"})

    def test_scoring_freezes_unknown_and_immutability_rules(self) -> None:
        self.assertIn("Unknown` is not mechanically ordered", self.scoring)
        self.assertIn("must be frozen before benchmark exposure", self.scoring)
        self.assertIn("creates a new protocol version", self.scoring)


if __name__ == "__main__":
    unittest.main()
