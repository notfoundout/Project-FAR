from __future__ import annotations

import importlib.util
import json
import subprocess
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
        self.assertEqual(result["version"], "1.0")
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
                module.validate_empirical_authority(module.DEFAULT_EMPIRICAL_CHARTER, module.DEFAULT_EMPIRICAL_MANIFEST, audit)

    def test_verify_end_to_end_rejects_empirical_authority_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "chat-audit-2026-08-05.md"
            audit.write_bytes(module.DEFAULT_CHAT_AUDIT.read_bytes() + b"\n")
            with self.assertRaisesRegex(module.VerificationError, "registered chat audit identity drifted"):
                module.verify(
                    SPEC_PATH,
                    RESULT_PATH,
                    REPORT_PATH,
                    README_PATH,
                    CHARTER_PATH,
                    GATES_PATH,
                    module.DEFAULT_EMPIRICAL_CHARTER,
                    module.DEFAULT_EMPIRICAL_MANIFEST,
                    audit,
                )

    def test_registered_artifact_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "chat-audit-2026-08-05.md"
            link.symlink_to(module.DEFAULT_CHAT_AUDIT)
            with self.assertRaisesRegex(module.VerificationError, "regular non-symlink file"):
                module.verify(
                    SPEC_PATH,
                    RESULT_PATH,
                    REPORT_PATH,
                    README_PATH,
                    CHARTER_PATH,
                    GATES_PATH,
                    module.DEFAULT_EMPIRICAL_CHARTER,
                    module.DEFAULT_EMPIRICAL_MANIFEST,
                    link,
                )

    def test_missing_empirical_chat_audit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "chat-audit-2026-08-05.md"
            with self.assertRaises(module.VerificationError):
                module.validate_empirical_authority(module.DEFAULT_EMPIRICAL_CHARTER, module.DEFAULT_EMPIRICAL_MANIFEST, missing)

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

    def test_rg07_must_gate_evidence_and_theorem_release_exactly(self) -> None:
        gates = module.load_json(GATES_PATH)
        rg07 = next(g for g in gates["gates"] if g["id"] == "RG-07")
        self.assertEqual(rg07["required_before"], ["evidence_release", "theorem_release"])
        for mutated_required in (["theorem_release"], ["evidence_release"], ["theorem_release", "evidence_release"], ["evidence_release", "theorem_release", "other"]):
            with self.subTest(required_before=mutated_required), tempfile.TemporaryDirectory() as tmp:
                changed = json.loads(json.dumps(gates))
                next(g for g in changed["gates"] if g["id"] == "RG-07")["required_before"] = mutated_required
                path = Path(tmp) / "gates.json"
                path.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaisesRegex(module.VerificationError, "evidence_release and theorem_release"):
                    module.verify(SPEC_PATH, RESULT_PATH, REPORT_PATH, README_PATH, CHARTER_PATH, path)

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

    def test_semantic_field_mutations_are_rejected(self) -> None:
        """Every field that materially determines scope or result must be frozen.

        Key presence is not sufficient: each mutation below keeps the schema shape
        and every identifier intact while reversing the substantive claim.
        """
        mutations = {
            "rccd_in_operation_schema": lambda d: d["input_operation_schema"].__setitem__(
                "invariance",
                "for every functor H:C->D, H(alpha_C(x))=alpha_D(H composed with x), "
                "where alpha decomposes as Construct, Differentiate, Restrict, Resolve",
            ),
            "theorem_text_rewritten_as_rccd_derivation": lambda d: d["theorem_claims"][3].__setitem__(
                "statement", "RCCD is derived from typed composition alone."
            ),
            "status_promoted_with_unchanged_ids": lambda d: d["theorem_claims"][3].__setitem__(
                "status", "established_derivation"
            ),
            "nonclaim_semantically_reversed": lambda d: d.__setitem__(
                "nonclaims",
                ["RCCD is derived." if x == "RCCD is not derived." else x for x in d["nonclaims"]],
            ),
            "scope_widened_to_absolute_broadest": lambda d: d["broadness_policy"].__setitem__(
                "selected_scope", "the broadest possible class of systems"
            ),
            "recoding_class_narrowed": lambda d: d["broadness_policy"].__setitem__(
                "recodings", "all identity functors"
            ),
            "axiom_weakened": lambda d: d["axioms"][3].__setitem__(
                "statement", "Associativity is optional."
            ),
            "identity_promoted_to_nontrivial_witness": lambda d: d["fixture"].__setitem__(
                "identity_is_nontrivial_for_distinguished_shape", True
            ),
            "question_text_changed": lambda d: d.__setitem__(
                "question", "Which finitary operations derive RCCD?"
            ),
            "system_class_changed": lambda d: d["broadness_policy"].__setitem__(
                "scope_criterion", "A system is included exactly when it supplies RCCD components."
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name):
                data = module.load_json(SPEC_PATH)
                mutate(data)
                with self.assertRaisesRegex(module.VerificationError, "specification|base_commit"):
                    module.build_result(data)

    def test_canonical_digest_independently_freezes_semantic_content(self) -> None:
        """The digest must reject drift even if the literal expected spec is relaxed."""
        data = module.load_json(SPEC_PATH)
        data["theorem_claims"][3]["statement"] = "RCCD is derived from typed composition alone."
        self.assertNotEqual(
            module.hashlib.sha256(module.canonical_json(data)).hexdigest(),
            module.EXPECTED_SPEC_SHA256,
        )

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

    def test_legacy_cli_passes_directly_without_wrapper_patching(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(DIR / "verify_compositional_invariant_legacy.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_weakening_detector_includes_research_verifiers(self) -> None:
        path = ROOT / "far_validation/weakening.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn('"research"', source)
        self.assertIn('path.startswith("research/")', source)
        self.assertIn('Path(path).name.startswith("verify_")', source)
        weakening_spec = importlib.util.spec_from_file_location("far_weakening_test", path)
        assert weakening_spec and weakening_spec.loader
        weakening = importlib.util.module_from_spec(weakening_spec)
        sys.modules[weakening_spec.name] = weakening
        weakening_spec.loader.exec_module(weakening)
        for protected in (
            "research/target-category-discovery/verify_compositional_invariant.py",
            "research/target-category-discovery/verify_compositional_invariant_legacy.py",
        ):
            self.assertEqual(weakening.REQUIRED_LIVE_CALL_PREFIXES[protected], ("validate_empirical_authority", "validate_gate"))
            protected_source = (ROOT / protected).read_text(encoding="utf-8")
            self.assertIn("validate_empirical_authority", weakening._called_functions(protected_source, protected))
            weakened = protected_source.replace("validate_empirical_authority", "removed_empirical_authority_call")
            self.assertNotIn("validate_empirical_authority", weakening._called_functions(weakened, protected))

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "assurance@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Validator Assurance"], cwd=repo, check=True)
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / protected).read_text(encoding="utf-8"), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                target.write_text(target.read_text(encoding="utf-8").replace("validate_empirical_authority", "removed_empirical_authority_call"), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "remove authority calls"], cwd=repo, check=True)
            report = weakening.detect_weakening(repo, base=base)
            self.assertFalse(report.successful)
            failures = {finding.path: finding.failures for finding in report.findings}
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                self.assertIn(protected, failures)
                self.assertTrue(any("required live verify call prefix changed" in item for item in failures[protected]))

            subprocess.run(["git", "reset", "--hard", base], cwd=repo, check=True, stdout=subprocess.DEVNULL)
            direct = "    validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)\n"
            dead = "    if False:\n        validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)\n"
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                source = target.read_text(encoding="utf-8")
                self.assertEqual(source.count(direct), 1)
                target.write_text(source.replace(direct, dead, 1), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "hide authority calls behind dead branches"], cwd=repo, check=True)
            dead_report = weakening.detect_weakening(repo, base=base)
            self.assertFalse(dead_report.successful)
            dead_failures = {finding.path: finding.failures for finding in dead_report.findings}
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                self.assertIn(protected, dead_failures)
                self.assertTrue(any("required live verify call prefix changed" in item for item in dead_failures[protected]))
                self.assertTrue(any("required live verify call prefix changed" in item for item in failures[protected]))

            subprocess.run(["git", "reset", "--hard", base], cwd=repo, check=True, stdout=subprocess.DEVNULL)
            direct = "    validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)\n"
            early_return = "    if True:\n        return None\n" + direct
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                source = target.read_text(encoding="utf-8")
                self.assertEqual(source.count(direct), 1)
                target.write_text(source.replace(direct, early_return, 1), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "insert conditionally terminating branch before authority calls"], cwd=repo, check=True)
            early_report = weakening.detect_weakening(repo, base=base)
            self.assertFalse(early_report.successful)
            early_failures = {finding.path: finding.failures for finding in early_report.findings}
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                self.assertIn(protected, early_failures)
                self.assertTrue(any("required live verify call prefix changed" in item for item in early_failures[protected]))

            subprocess.run(["git", "reset", "--hard", base], cwd=repo, check=True, stdout=subprocess.DEVNULL)
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                source = target.read_text(encoding="utf-8")
                source += "\nvalidate_empirical_authority = lambda *args, **kwargs: None\n"
                source += "validate_gate = lambda *args, **kwargs: None\n"
                target.write_text(source, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "rebind protected authority validators"], cwd=repo, check=True)
            rebound_report = weakening.detect_weakening(repo, base=base)
            self.assertFalse(rebound_report.successful)
            rebound_failures = {finding.path: finding.failures for finding in rebound_report.findings}
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                self.assertIn(protected, rebound_failures)
                self.assertTrue(any("protected validator binding changed" in item for item in rebound_failures[protected]))


if __name__ == "__main__":
    unittest.main()
