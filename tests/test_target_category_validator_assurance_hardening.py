from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAKENING_PATH = ROOT / "far_validation/weakening.py"

spec = importlib.util.spec_from_file_location("far_weakening_hardening_test", WEAKENING_PATH)
assert spec and spec.loader
weakening = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = weakening
spec.loader.exec_module(weakening)


class ProtectedValidatorAssuranceHardeningTests(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
        tmp = tempfile.TemporaryDirectory()
        repo = Path(tmp.name)
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
        return tmp, repo, base

    def _commit_and_report(self, repo: Path, base: str, message: str):
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=repo, check=True)
        return weakening.detect_weakening(repo, base=base)

    def test_protected_verifiers_are_content_pinned_in_assurance_lock(self) -> None:
        """Whole-file pins are the backstop behind the AST-level controls.

        The structural scanners approximate "this verifier was not weakened" by
        enumerating rebinding forms, which can never be complete: a namespace
        provider can be re-derived through ``getattr(builtins, ...)``,
        ``__builtins__[...]``, or ``importlib``. Pinning the verifier bytes makes
        any such edit fail the bootstrap gate regardless of technique.
        """
        lock = json.loads((ROOT / "validation_bootstrap/assurance-lock.json").read_text(encoding="utf-8"))
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            self.assertIn(protected, lock["files"], protected)
            digest = hashlib.sha256((ROOT / protected).read_bytes()).hexdigest()
            self.assertEqual(lock["files"][protected], digest, protected)

    def test_assurance_lock_rejects_protected_verifier_edits(self) -> None:
        lock = json.loads((ROOT / "validation_bootstrap/assurance-lock.json").read_text(encoding="utf-8"))
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            mutated = (ROOT / protected).read_text(encoding="utf-8") + (
                "\nimport builtins as _far_b\n"
                "getattr(_far_b, 'globals')()['validate_gate'] = lambda *a, **k: None\n"
            )
            digest = hashlib.sha256(mutated.encode("utf-8")).hexdigest()
            self.assertNotEqual(lock["files"][protected], digest, protected)

    def test_implementation_digests_match_committed_sources(self) -> None:
        for path, names in weakening.EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.items():
            source = (ROOT / path).read_text(encoding="utf-8")
            self.assertEqual(weakening._protected_implementation_failures(source, path), [], path)
            self.assertTrue(names)

    def test_implementation_digest_is_reproducible_across_interpreters(self) -> None:
        """The pin must track the implementation, not the interpreter.

        ``ast.dump`` output is a debugging representation that differs between
        CPython minor versions, so digesting it would make this control pass only
        on the interpreter that generated the pins.
        """
        candidates = [Path(f"/usr/bin/python3.{minor}") for minor in (11, 12, 13)]
        interpreters = [str(c) for c in candidates if c.exists()]
        if len(interpreters) < 2:
            self.skipTest("need at least two CPython minor versions to compare")
        program = (
            "import json,sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from far_validation import weakening as w\n"
            "from pathlib import Path\n"
            "out={}\n"
            "for path, names in w.EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.items():\n"
            "    src=Path(sys.argv[1], path).read_text(encoding='utf-8')\n"
            "    out[path]={n: w._protected_implementation_digest(src, path, n) for n in names}\n"
            "print(json.dumps(out, sort_keys=True))\n"
        )
        digests = set()
        for interpreter in interpreters:
            completed = subprocess.run(
                [interpreter, "-c", program, str(ROOT)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            digests.add(completed.stdout.strip())
        self.assertEqual(len(digests), 1, f"digests differ across {interpreters}")

    def test_definition_time_decorator_rebinding_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            target = repo / protected
            text = target.read_text(encoding="utf-8")
            mutation = (
                "\ndef _far_rebind(fn):\n"
                "    globals().__setitem__(\"validate_empirical_authority\", lambda *a, **k: None)\n"
                "    globals().__setitem__(\"validate_gate\", lambda *a, **k: None)\n"
                "    return fn\n\n"
                "@_far_rebind\n"
                "def _far_trigger():\n"
                "    return None\n"
            )
            target.write_text(text + mutation, encoding="utf-8")
        report = self._commit_and_report(repo, base, "decorator rebinding attack")
        self.assertFalse(report.successful)
        checked = 0
        for finding in report.findings:
            if finding.path in weakening.REQUIRED_SEMANTIC_CALLS:
                checked += 1
                self.assertTrue(any(("protected validator binding changed" in item) or ("definition-time decorator rejected" in item) for item in finding.failures))
        self.assertEqual(checked, len(weakening.REQUIRED_SEMANTIC_CALLS))

    def test_protected_validator_early_return_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        legacy_rel = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
        legacy = repo / legacy_rel
        text = legacy.read_text(encoding="utf-8")
        needle = "def validate_empirical_authority(charter_path: Path, manifest_path: Path, audit_path: Path = DEFAULT_CHAT_AUDIT) -> None:\n"
        self.assertEqual(text.count(needle), 1)
        legacy.write_text(text.replace(needle, needle + "    return None\n", 1), encoding="utf-8")
        report = self._commit_and_report(repo, base, "early-return protected validator attack")
        self.assertFalse(report.successful)
        failures = next(f.failures for f in report.findings if f.path == legacy_rel)
        self.assertTrue(any("protected validator implementation changed" in item for item in failures))


    def test_class_body_dynamic_exec_rebinding_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            target = repo / protected
            text = target.read_text(encoding="utf-8")
            text += "\nclass _FarDefinitionTimeAttack:\n    exec(\"globals()['validate_empirical_authority'] = lambda *a, **k: None\")\n    exec(\"globals()['validate_gate'] = lambda *a, **k: None\")\n"
            target.write_text(text, encoding="utf-8")
        report = self._commit_and_report(repo, base, "class-body dynamic execution attack")
        self.assertFalse(report.successful)
        checked = 0
        for finding in report.findings:
            if finding.path in weakening.REQUIRED_SEMANTIC_CALLS:
                checked += 1
                self.assertTrue(any("dynamic execution rejected" in item for item in finding.failures))
        self.assertEqual(checked, len(weakening.REQUIRED_SEMANTIC_CALLS))

    def test_nested_scope_builtins_import_exec_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            target = repo / protected
            text = target.read_text(encoding="utf-8")
            text += (
                "\nclass _FarNestedImportAttack:\n"
                "    from builtins import exec as _far_exec\n"
                "    _far_exec(\"globals()['validate_empirical_authority'] = lambda *a, **k: None\")\n"
                "    _far_exec(\"globals()['validate_gate'] = lambda *a, **k: None\")\n"
            )
            target.write_text(text, encoding="utf-8")
        report = self._commit_and_report(repo, base, "nested-scope builtins import execution attack")
        self.assertFalse(report.successful)
        checked = 0
        for finding in report.findings:
            if finding.path in weakening.REQUIRED_SEMANTIC_CALLS:
                checked += 1
                self.assertTrue(any("dynamic execution rejected" in item for item in finding.failures))
        self.assertEqual(checked, len(weakening.REQUIRED_SEMANTIC_CALLS))

    def test_protected_helper_rebinding_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        rel = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
        target = repo / rel
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n_git_blob_sha1 = lambda raw: '0' * 40\n", encoding="utf-8")
        report = self._commit_and_report(repo, base, "protected helper rebinding attack")
        self.assertFalse(report.successful)
        failures = next(f.failures for f in report.findings if f.path == rel)
        self.assertTrue(any("protected validator binding changed for _git_blob_sha1" in item for item in failures))

    def test_verify_early_return_after_authority_prefix_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        rel = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
        target = repo / rel
        text = target.read_text(encoding="utf-8")
        needle = "    validate_gate(gates_path)\n    actual = build_result(load_json(spec_path))\n"
        self.assertEqual(text.count(needle), 1)
        target.write_text(text.replace(needle, "    validate_gate(gates_path)\n    return {}\n    actual = build_result(load_json(spec_path))\n", 1), encoding="utf-8")
        report = self._commit_and_report(repo, base, "verify post-prefix early-return attack")
        self.assertFalse(report.successful)
        failures = next(f.failures for f in report.findings if f.path == rel)
        self.assertTrue(any("protected validator implementation changed for verify" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
