from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/target-category-discovery"
MODULE_PATH = DIR / "verify_compositional_invariant.py"
SPEC_PATH = DIR / "compositional-invariant-spec-v1.0.json"
RESULT_PATH = DIR / "compositional-invariant-result-v1.0.json"
REPORT_PATH = DIR / "compositional-invariant-terminal-result-v1.0.md"
README_PATH = DIR / "README.md"
CHARTER_PATH = DIR / "scope-and-universality-charter-v1.2.md"
GATES_PATH = ROOT / "theory/evaluation/research-gates.json"

spec = importlib.util.spec_from_file_location("verify_compositional_invariant", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class CompositionalInvariantTests(unittest.TestCase):
    def test_frozen_result_passes(self) -> None:
        result = module.verify(SPEC_PATH, RESULT_PATH, REPORT_PATH, README_PATH, CHARTER_PATH, GATES_PATH)
        self.assertEqual(result["classification"], "exploratory_unregistered_derivation")
        self.assertEqual(result["release_status"], "not_eligible_unregistered_deductive_program")
        self.assertEqual(result["theorem_status"], "not_established_exploratory_argument_with_bounded_executable_corroboration")
        self.assertFalse(result["accepted_theory_change"])

    def test_nontrivial_witness_is_composition_not_identity(self) -> None:
        result = module.build_result(module.load_json(SPEC_PATH))
        evidence = result["evidence"]
        self.assertEqual(evidence["nontrivial_invariant_witness"], "b∘a")
        self.assertFalse(evidence["identity_is_nontrivial_witness"])
        self.assertFalse(evidence["identity_is_admissible_for_distinguished_A_to_C_shape"])
        self.assertNotIn("id_A", evidence["distinguished_paths"])

    def test_spec_identity_overclaim_is_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["theorem_claims"][2]["statement"] = "Identity is a nontrivial A-to-C invariant."
        with self.assertRaisesRegex(module.VerificationError, "specification"):
            module.build_result(data)

    def test_unregistered_derivation_cannot_be_promoted_to_theorem(self) -> None:
        for field, value in (
            ("classification", "scoped_theorem_established_internal_release_blocked"),
            ("release_status", "blocked_by_rg_07_nonclaim_audit"),
        ):
            data = module.load_json(SPEC_PATH)
            data["disposition"][field] = value
            with self.subTest(field=field), self.assertRaises(module.VerificationError):
                module.build_result(data)
        data = module.load_json(SPEC_PATH)
        data["theorem_claims"][1]["status"] = "proved_in_internal_research_report"
        with self.assertRaises(module.VerificationError):
            module.build_result(data)

    def test_each_public_surface_is_locked_independently(self) -> None:
        surfaces = {"README": README_PATH, "Charter": CHARTER_PATH, "Report": REPORT_PATH}
        for name, source in surfaces.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                mutated = Path(tmp) / source.name
                mutated.write_text(source.read_text(encoding="utf-8").replace(module.PUBLIC_NONCLAIMS[0], "", 1), encoding="utf-8")
                with self.assertRaisesRegex(module.VerificationError, f"{name} public claim surface drifted"):
                    module.validate_public_surface(name, mutated)

    def test_every_surface_contains_every_comparison_boundary_once(self) -> None:
        for path in (README_PATH, CHARTER_PATH, REPORT_PATH):
            text = path.read_text(encoding="utf-8")
            for line in module.PUBLIC_NONCLAIMS:
                self.assertEqual(text.count(line), 1, f"{path} missing or duplicates {line}")

    def test_public_surface_theorem_overclaim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README.md"
            path.write_text(README_PATH.read_text(encoding="utf-8") + "\nTheorem established.\n", encoding="utf-8")
            with self.assertRaises(module.VerificationError):
                module.validate_public_surface("README", path)

    def test_empirical_chat_audit_bytes_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "chat-audit-2026-08-05.md"
            audit.write_bytes(module.DEFAULT_CHAT_AUDIT.read_bytes() + b"\n")
            with self.assertRaisesRegex(module.VerificationError, "registered chat audit identity drifted"):
                module.validate_empirical_authority(
                    module.DEFAULT_EMPIRICAL_CHARTER,
                    module.DEFAULT_EMPIRICAL_MANIFEST,
                    audit,
                )

    def test_missing_empirical_chat_audit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "chat-audit-2026-08-05.md"
            with self.assertRaisesRegex(module.VerificationError, "required artifact missing or unreadable"):
                module.validate_empirical_authority(
                    module.DEFAULT_EMPIRICAL_CHARTER,
                    module.DEFAULT_EMPIRICAL_MANIFEST,
                    missing,
                )

    def test_rg07_must_remain_unsatisfied_for_this_version(self) -> None:
        gates = module.load_json(GATES_PATH)
        rg07 = next(g for g in gates["gates"] if g["id"] == "RG-07")
        rg07["status"] = "satisfied"
        rg07["evidence"] = ["fake.md"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gates.json"
            path.write_text(json.dumps(gates), encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "RG-07 state changed"):
                module.validate_gate(path)

    def test_release_cannot_be_claimed_by_mutating_result(self) -> None:
        data = module.load_json(RESULT_PATH)
        data["release_status"] = "released"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "fresh rebuild"):
                module.verify(SPEC_PATH, path, REPORT_PATH, README_PATH, CHARTER_PATH, GATES_PATH)

    def test_broadness_and_optimality_overclaims_are_rejected(self) -> None:
        data = module.load_json(SPEC_PATH)
        data["broadness_policy"]["absolute_maximum_claimed"] = True
        with self.assertRaisesRegex(module.VerificationError, "specification"):
            module.build_result(data)
        data = module.load_json(SPEC_PATH)
        data["nonclaims"] = [x for x in data["nonclaims"] if "globally optimal" not in x]
        with self.assertRaisesRegex(module.VerificationError, "specification"):
            module.build_result(data)

    def test_duplicate_json_key_and_nonfinite_number_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            duplicate = Path(tmp) / "duplicate.json"
            duplicate.write_text('{"x":1,"x":2}', encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "duplicate JSON key"):
                module.load_json(duplicate)
            nonfinite = Path(tmp) / "nonfinite.json"
            nonfinite.write_text('{"x":NaN}', encoding="utf-8")
            with self.assertRaisesRegex(module.VerificationError, "non-finite"):
                module.load_json(nonfinite)

if __name__ == "__main__":
    unittest.main()
