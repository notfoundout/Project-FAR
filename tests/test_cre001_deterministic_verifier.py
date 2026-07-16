from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "cre001_verifier.py"
SPEC = importlib.util.spec_from_file_location("cre001_verifier", TOOL_PATH)
assert SPEC and SPEC.loader
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)

MODEL_ROOT = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/deterministic-verifier"
REFERENCE = MODEL_ROOT / "reference-model.json"
VALID = MODEL_ROOT / "fixtures" / "valid-candidate.json"


class Cre001DeterministicVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
        self.valid = json.loads(VALID.read_text(encoding="utf-8"))

    def test_valid_candidate_passes(self) -> None:
        report = VERIFIER.verify(self.reference, self.valid)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["diagnostics"], [])

    def test_missing_variable_fails_structural_check(self) -> None:
        candidate = copy.deepcopy(self.valid)
        del candidate["variables"]["p_rule_modified"]
        report = VERIFIER.verify(self.reference, candidate)
        self.assertEqual(report["result"], "fail")
        self.assertIn("missing_variable", {item["code"] for item in report["diagnostics"]})

    def test_wrong_guard_returns_shortest_counterexample(self) -> None:
        candidate = copy.deepcopy(self.valid)
        transition = next(item for item in candidate["transitions"] if item["name"] == "T_reject")
        transition["guard"] = [item for item in transition["guard"] if item["variable"] != "R_reject_active"]
        report = VERIFIER.verify(self.reference, candidate)
        counterexample = next(item for item in report["diagnostics"] if item["code"] == "enabled_set_mismatch")
        self.assertEqual(counterexample["trace"], ["T_check", "T_disable_reject"])
        self.assertIn("T_reject", counterexample["details"]["candidate_enabled"])
        self.assertNotIn("T_reject", counterexample["details"]["reference_enabled"])

    def test_wrong_update_is_detected(self) -> None:
        candidate = copy.deepcopy(self.valid)
        transition = next(item for item in candidate["transitions"] if item["name"] == "T_accept")
        transition["updates"][0] = {"variable": "p_rejected", "operation": "set", "value": True}
        report = VERIFIER.verify(self.reference, candidate)
        codes = {item["code"] for item in report["diagnostics"]}
        self.assertIn("update_mismatch", codes)
        self.assertIn("post_state_mismatch", codes)

    def test_history_corruption_is_detected(self) -> None:
        candidate = copy.deepcopy(self.valid)
        transition = next(item for item in candidate["transitions"] if item["name"] == "T_accept")
        transition["updates"][-1] = {"variable": "history", "operation": "append", "value": "WRONG"}
        report = VERIFIER.verify(self.reference, candidate)
        self.assertIn("update_mismatch", {item["code"] for item in report["diagnostics"]})
        self.assertEqual(report["checks"]["historical"], "fail")

    def test_post_halt_policy_mismatch_is_detected(self) -> None:
        candidate = copy.deepcopy(self.valid)
        candidate["terminal_blocks_all_transitions"] = False
        report = VERIFIER.verify(self.reference, candidate)
        self.assertIn("terminal_policy_mismatch", {item["code"] for item in report["diagnostics"]})

    def test_lost_output_is_detected(self) -> None:
        candidate = copy.deepcopy(self.valid)
        del candidate["outputs"]["rule_modification_occurred"]
        report = VERIFIER.verify(self.reference, candidate)
        self.assertEqual(report["checks"]["information"], "fail")
        self.assertIn("output_mismatch", {item["code"] for item in report["diagnostics"]})

    def test_ambiguity_policy_must_match(self) -> None:
        candidate = copy.deepcopy(self.valid)
        candidate["ambiguity_policy"]["disable_reject_repeatability"] = "allow_idempotent_repeat"
        report = VERIFIER.verify(self.reference, candidate)
        self.assertEqual(report["checks"]["ambiguity_policy"], "fail")


if __name__ == "__main__":
    unittest.main()
