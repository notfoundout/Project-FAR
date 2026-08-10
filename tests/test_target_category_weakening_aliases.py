from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import weakening

ROOT = Path(__file__).resolve().parents[1]
LEGACY_REL = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
LEGACY = ROOT / LEGACY_REL


class TargetCategoryWeakeningAliasTests(unittest.TestCase):
    def _mutated_report(self, suffix: str):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            target = repo / LEGACY_REL
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(LEGACY.read_text(encoding="utf-8"), encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "assurance@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Validator Assurance"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
            target.write_text(target.read_text(encoding="utf-8") + suffix, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "adversarial mutation"], cwd=repo, check=True)
            return weakening.detect_weakening(repo, base=base)

    def test_module_alias_to_exec_is_rejected_even_when_called_from_class_body(self) -> None:
        report = self._mutated_report(
            "\n_far_dynamic = exec\n"
            "class _FarAliasAttack:\n"
            "    _far_dynamic('globals()[\\\"validate_empirical_authority\\\"] = lambda *a, **k: None')\n"
        )
        self.assertFalse(report.successful)
        failures = [item for finding in report.findings for item in finding.failures]
        self.assertTrue(any("dynamic execution rejected" in item for item in failures), failures)

    def test_vars_namespace_rebinding_of_protected_helper_is_rejected(self) -> None:
        report = self._mutated_report(
            "\nvars()[\"_git_blob_sha1\"] = lambda payload: None\n"
        )
        self.assertFalse(report.successful)
        failures = [item for finding in report.findings for item in finding.failures]
        self.assertTrue(
            any("protected validator binding changed for _git_blob_sha1" in item for item in failures),
            failures,
        )


if __name__ == "__main__":
    unittest.main()
