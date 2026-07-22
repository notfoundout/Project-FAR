from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_usd_w1_partial_observability.py"
spec = importlib.util.spec_from_file_location("check_usd_w1_partial_observability", CHECKER_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


class PartialObservabilityValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scope = json.loads(checker.SCOPE.read_text(encoding="utf-8"))
        cls.result = json.loads(checker.RESULT.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(checker.FIXTURES.read_text(encoding="utf-8"))
        cls.proof = checker.PROOF.read_text(encoding="utf-8")
        cls.audit = checker.AUDIT.read_text(encoding="utf-8")

    def validate(self, scope=None, result=None, fixtures=None, proof=None, audit=None) -> None:
        checker.validate(
            copy.deepcopy(self.scope if scope is None else scope),
            copy.deepcopy(self.result if result is None else result),
            copy.deepcopy(self.fixtures if fixtures is None else fixtures),
            self.proof if proof is None else proof,
            self.audit if audit is None else audit,
        )

    def test_registered_artifacts_pass(self) -> None:
        self.validate()

    def test_rejects_true_state_access(self) -> None:
        scope = copy.deepcopy(self.scope)
        scope["observation_boundary"]["prohibited"].remove("policy_access_to_true_latent_state")
        with self.assertRaises(AssertionError):
            self.validate(scope=scope)

    def test_rejects_universal_promotion(self) -> None:
        result = copy.deepcopy(self.result)
        result["claim_effect"]["universal_structure"] = "proved"
        with self.assertRaises(AssertionError):
            self.validate(result=result)

    def test_rejects_scope_promotion(self) -> None:
        result = copy.deepcopy(self.result)
        result["terminal_outcome"] = "extension_proved"
        with self.assertRaises(AssertionError):
            self.validate(result=result)

    def test_rejects_new_target_primitive(self) -> None:
        result = copy.deepcopy(self.result)
        result["new_target_primitive"] = True
        with self.assertRaises(AssertionError):
            self.validate(result=result)

    def test_rejects_missing_negative_control(self) -> None:
        fixtures = copy.deepcopy(self.fixtures)
        fixtures["fixtures"] = [x for x in fixtures["fixtures"] if x["id"] != "PO-NEG-LEAK-001"]
        with self.assertRaises(AssertionError):
            self.validate(fixtures=fixtures)

    def test_rejects_mechanization_overclaim(self) -> None:
        result = copy.deepcopy(self.result)
        result["machine_check_status"] = "machine_checked"
        with self.assertRaises(AssertionError):
            self.validate(result=result)

    def test_rejects_removed_proof_boundary(self) -> None:
        proof = self.proof.replace("does not establish representation of all partially observable reasoning", "")
        with self.assertRaises(AssertionError):
            self.validate(proof=proof)


if __name__ == "__main__":
    unittest.main()
