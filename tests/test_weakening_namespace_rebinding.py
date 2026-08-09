from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import weakening


ROOT = Path(__file__).resolve().parents[1]
PROTECTED = tuple(weakening.REQUIRED_SEMANTIC_CALLS)


class NamespaceRebindingWeakeningTests(unittest.TestCase):
    def _baseline_repo(self, root: Path) -> str:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "assurance@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Validator Assurance"], cwd=root, check=True)
        for protected in PROTECTED:
            target = root / protected
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((ROOT / protected).read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

    def _mutate_before_cli_guard(self, root: Path, payload: str) -> None:
        marker = '\nif __name__ == "__main__":\n'
        for protected in PROTECTED:
            target = root / protected
            source = target.read_text(encoding="utf-8")
            self.assertEqual(source.count(marker), 1, protected)
            target.write_text(source.replace(marker, "\n" + payload + marker, 1), encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "mutate namespace bindings"], cwd=root, check=True)

    def _assert_rejected(self, root: Path, base: str) -> None:
        report = weakening.detect_weakening(root, base=base)
        self.assertFalse(report.successful)
        failures = {finding.path: finding.failures for finding in report.findings}
        for protected in PROTECTED:
            self.assertIn(protected, failures)
            self.assertTrue(
                any("protected validator binding changed" in failure for failure in failures[protected]),
                failures[protected],
            )

    def test_globals_dunder_setitem_rebinding_is_rejected(self) -> None:
        payload = (
            "def _far_no_op(*args, **kwargs):\n"
            "    return None\n\n"
            "globals().__setitem__(\"validate_empirical_authority\", _far_no_op)\n"
            "globals().__setitem__(\"validate_gate\", _far_no_op)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base = self._baseline_repo(repo)
            self._mutate_before_cli_guard(repo, payload)
            self._assert_rejected(repo, base)

    def test_globals_update_rebinding_is_rejected(self) -> None:
        payload = (
            "def _far_no_op(*args, **kwargs):\n"
            "    return None\n\n"
            "globals().update({\n"
            "    \"validate_empirical_authority\": _far_no_op,\n"
            "    \"validate_gate\": _far_no_op,\n"
            "})\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base = self._baseline_repo(repo)
            self._mutate_before_cli_guard(repo, payload)
            self._assert_rejected(repo, base)

    def test_dynamic_namespace_update_fails_closed(self) -> None:
        payload = (
            "def _far_no_op(*args, **kwargs):\n"
            "    return None\n\n"
            "_far_rebindings = {\"validate_empirical_authority\": _far_no_op}\n"
            "globals().update(_far_rebindings)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base = self._baseline_repo(repo)
            self._mutate_before_cli_guard(repo, payload)
            self._assert_rejected(repo, base)


if __name__ == "__main__":
    unittest.main()
