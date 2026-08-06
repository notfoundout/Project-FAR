from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/target-category-discovery/verify_compositional_invariant.py"
SPEC_PATH = ROOT / "research/target-category-discovery/compositional-invariant-spec-v1.0.json"
RESULT_PATH = ROOT / "research/target-category-discovery/compositional-invariant-result-v1.0.json"
REPORT_PATH = ROOT / "research/target-category-discovery/compositional-invariant-terminal-result-v1.0.md"

spec = importlib.util.spec_from_file_location("verify_compositional_invariant", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class CompositionalInvariantTests(unittest.TestCase):
    def _mutated_report(self, raw: bytes) -> Path:
        self.temp_dir = tempfile.TemporaryDirectory()
        path = Path(self.temp_dir.name) / "report.md"
        path.write_bytes(raw)
        self.addCleanup(self.temp_dir.cleanup)
        return path

    def test_frozen_result_passes(self) -> None:
        result = module.verify(SPEC_PATH, RESULT_PATH, REPORT_PATH)
        self.assertEqual(result["classification"], "scoped_theoretical_question_closed")
        self.assertEqual(result["rccd_status"], "not_derived")
        self.assertEqual(result["empirical_program_status"], "not_executed")
        self.assertEqual(result["evidence"]["distinguished_paths"], ["c", "b∘a"])
        self.assertEqual(result["evidence"]["new_nonidentity_paths"], ["b∘a"])

    def test_free_category_supplies_a_genuinely_new_composite(self) -> None:
        result = module.build_result(module.load_json(SPEC_PATH))
        evidence = result["evidence"]
        self.assertFalse(evidence["graph_only_has_composite"])
        self.assertTrue(evidence["free_category_has_composite"])
        self.assertEqual(evidence["fixture_generator_count"], 3)
        self.assertEqual(evidence["free_category_nonidentity_arrow_count"], 4)
        self.assertEqual(evidence["nontrivial_composite"], "b∘a")

    def test_absolute_broadest_overclaim_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["broadness_policy"]["absolute_maximum_claimed"] = True
        with self.assertRaisesRegex(module.VerificationError, "broadness policy drifted"):
            module.build_result(data)

    def test_arbitrary_recodings_are_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["broadness_policy"]["recodings"] = "all underlying set functions"
        with self.assertRaisesRegex(module.VerificationError, "broadness policy drifted"):
            module.build_result(data)

    def test_noncanonical_base_commit_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["base_commit"] = "a" * 40
        with self.assertRaisesRegex(module.VerificationError, "frozen repository base"):
            module.build_result(data)

    def test_nonhex_base_commit_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["base_commit"] = "z" * 40
        with self.assertRaisesRegex(module.VerificationError, "hexadecimal SHA"):
            module.build_result(data)

    def test_input_operation_schema_drift_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["input_operation_schema"]["invariance"] = "preserve the four RCCD operations"
        with self.assertRaisesRegex(module.VerificationError, "input operation schema drifted"):
            module.build_result(data)

    def test_theorem_semantic_drift_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["theorem_claims"][1]["statement"] = "RCCD is universally derived."
        data["theorem_claims"][1]["status"] = "accepted"
        with self.assertRaisesRegex(module.VerificationError, "semantics drifted"):
            module.build_result(data)

    def test_missing_associativity_axiom_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["axioms"] = [axiom for axiom in data["axioms"] if axiom["id"] != "TC4"]
        with self.assertRaisesRegex(module.VerificationError, "exact four-axiom contract"):
            module.build_result(data)

    def test_rccd_derivation_claim_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["terminal_disposition"]["rccd_status"] = "derived"
        with self.assertRaisesRegex(module.VerificationError, "terminal disposition"):
            module.build_result(data)

    def test_empirical_completion_claim_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["terminal_disposition"]["empirical_program_status"] = "complete"
        with self.assertRaisesRegex(module.VerificationError, "terminal disposition"):
            module.build_result(data)

    def test_committed_result_drift_is_rejected(self) -> None:
        result = module.load_json(RESULT_PATH)
        result["evidence"]["free_category_arrow_count"] = 6
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "fresh rebuild"):
                module.verify(SPEC_PATH, path, REPORT_PATH)

    def test_report_without_absolute_nonclaim_is_rejected(self) -> None:
        text = REPORT_PATH.read_text(encoding="utf-8").replace(
            "Small categories are the absolute broadest possible class of every conceivable reasoning system.",
            "",
        )
        with self.assertRaisesRegex(module.VerificationError, "report content drifted"):
            module.verify(SPEC_PATH, RESULT_PATH, self._mutated_report(text.encode()))

    def test_report_proof_status_reversal_is_rejected(self) -> None:
        text = REPORT_PATH.read_text(encoding="utf-8").replace(
            "it is not a proof assistant and does not convert CI success into mathematical proof",
            "it is a proof assistant and converts CI success into mathematical proof",
        )
        with self.assertRaisesRegex(module.VerificationError, "report content drifted"):
            module.verify(SPEC_PATH, RESULT_PATH, self._mutated_report(text.encode()))

    def test_report_rccd_contradiction_is_rejected(self) -> None:
        raw = REPORT_PATH.read_bytes() + b"\nRCCD is universally derived.\n"
        with self.assertRaisesRegex(module.VerificationError, "report content drifted"):
            module.verify(SPEC_PATH, RESULT_PATH, self._mutated_report(raw))

    def test_report_empirical_completion_contradiction_is_rejected(self) -> None:
        raw = REPORT_PATH.read_bytes() + b"\nThe clean-room empirical program is complete.\n"
        with self.assertRaisesRegex(module.VerificationError, "report content drifted"):
            module.verify(SPEC_PATH, RESULT_PATH, self._mutated_report(raw))

    def test_report_bom_is_rejected(self) -> None:
        path = self._mutated_report(b"\xef\xbb\xbf" + REPORT_PATH.read_bytes())
        with self.assertRaisesRegex(module.VerificationError, "UTF-8 BOM"):
            module.verify(SPEC_PATH, RESULT_PATH, path)

    def test_report_invalid_utf8_is_rejected(self) -> None:
        path = self._mutated_report(REPORT_PATH.read_bytes() + b"\xff")
        with self.assertRaisesRegex(module.VerificationError, "invalid UTF-8"):
            module.verify(SPEC_PATH, RESULT_PATH, path)

    def test_duplicate_json_key_is_rejected(self) -> None:
        raw = SPEC_PATH.read_text(encoding="utf-8")
        mutated = raw.replace(
            '  "version": "1.0",',
            '  "version": "1.0",\n  "version": "1.1",',
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text(mutated, encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "duplicate JSON key"):
                module.load_json(path)

    def test_utf8_bom_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom.json"
            path.write_bytes(b"\xef\xbb\xbf" + SPEC_PATH.read_bytes())
            with self.assertRaisesRegex(module.VerificationError, "UTF-8 BOM"):
                module.load_json(path)


if __name__ == "__main__":
    unittest.main()
