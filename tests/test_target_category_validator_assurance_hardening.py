from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
