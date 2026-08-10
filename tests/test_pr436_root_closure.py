from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class PR436RootClosureTests(unittest.TestCase):
    def test_legacy_reader_rejects_symlink(self) -> None:
        legacy = load_module(
            "pr436_legacy",
            ROOT / "research/target-category-discovery/verify_compositional_invariant_legacy.py",
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            target = tmp_path / "artifact.md"
            target.write_text("same bytes", encoding="utf-8")
            link = tmp_path / "artifact-link.md"
            link.symlink_to(target)
            with self.assertRaisesRegex(legacy.VerificationError, "regular non-symlink"):
                legacy._read_utf8(link)

    def test_weakening_rejects_aliased_module_namespace_rebinding(self) -> None:
        weakening = load_module("pr436_weakening", ROOT / "far_validation/weakening.py")
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "config", "user.email", "assurance@example.invalid"],
                cwd=repo,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Validator Assurance"],
                cwd=repo,
                check=True,
            )
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / protected).read_text(encoding="utf-8"), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            base = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=repo, text=True
            ).strip()

            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                target = repo / protected
                source = target.read_text(encoding="utf-8")
                source += "\n_far_namespace = globals()\n"
                source += (
                    '_far_namespace.update({"validate_empirical_authority": '
                    'lambda *args, **kwargs: None, "validate_gate": '
                    'lambda *args, **kwargs: None})\n'
                )
                target.write_text(source, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "alias module namespace and rebind validators"],
                cwd=repo,
                check=True,
            )

            report = weakening.detect_weakening(repo, base=base)
            self.assertFalse(report.successful)
            failures = {finding.path: finding.failures for finding in report.findings}
            for protected in weakening.REQUIRED_SEMANTIC_CALLS:
                self.assertIn(protected, failures)
                self.assertTrue(
                    any("protected validator binding changed" in item for item in failures[protected])
                )


if __name__ == "__main__":
    unittest.main()
