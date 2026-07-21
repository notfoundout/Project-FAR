from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from far_validation.engine import ValidationEngine
from far_validation.manifest import ManifestError, load_manifest


class UnifiedManifestTests(unittest.TestCase):
    def test_canonical_manifest_is_valid(self) -> None:
        manifest = load_manifest(ROOT / "validation" / "manifest.json")
        self.assertEqual(manifest.schema_version, "1.0")
        self.assertGreaterEqual(len(manifest.checks), 32)
        self.assertIn("governance.w5-authorization", manifest.protected_checks)
        self.assertIn("repository.health-fast", manifest.profiles["pr-fast"])
        self.assertIn("repository.health-full", manifest.profiles["pr-full"])
        for protected in manifest.protected_checks:
            for profile in ("pr-fast", "pr-full", "full", "release"):
                self.assertIn(protected, manifest.profiles[profile])

    def test_dependency_cycle_is_rejected(self) -> None:
        payload = {
            "schema_version": "1.0",
            "profiles": {"pr-fast": ["a", "b"]},
            "protected_checks": [],
            "global_invalidation_paths": [],
            "checks": [
                {"id": "a", "title": "a", "builtin": "manifest", "depends_on": ["b"]},
                {"id": "b", "title": "b", "builtin": "manifest", "depends_on": ["a"]},
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ManifestError, "dependency cycle"):
                load_manifest(path)


class UnifiedEngineTests(unittest.TestCase):
    def _write_manifest(self, root: Path, checks: list[dict], profiles: dict[str, list[str]]) -> None:
        validation = root / "validation"
        validation.mkdir(parents=True)
        payload = {
            "schema_version": "1.0",
            "profiles": profiles,
            "protected_checks": [],
            "global_invalidation_paths": ["validation/**"],
            "checks": checks,
        }
        (validation / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")

    def test_sandboxed_generator_detects_drift_without_mutating_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tracked.txt").write_text("original\n", encoding="utf-8")
            checks = [
                {
                    "id": "generator",
                    "title": "generator",
                    "command": [
                        sys.executable,
                        "-c",
                        "from pathlib import Path; Path('tracked.txt').write_text('changed\\n')",
                    ],
                    "profiles": ["pr-fast"],
                    "inputs": ["tracked.txt"],
                    "sandbox_copy": True,
                    "expect_no_changes": True,
                    "cacheable": False,
                    "failure_code": "FAR-VAL-GEN-002",
                }
            ]
            self._write_manifest(root, checks, {"pr-fast": ["generator"]})
            summary = ValidationEngine(root, jobs=1, use_cache=False).run(profile="pr-fast")
            self.assertFalse(summary.successful)
            self.assertEqual(summary.results[0].failure_code, "FAR-VAL-GEN-002")
            self.assertEqual((root / "tracked.txt").read_text(encoding="utf-8"), "original\n")
            self.assertEqual(summary.results[0].changed_files, ["tracked.txt"])

    def test_dependency_failure_blocks_downstream_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checks = [
                {
                    "id": "root",
                    "title": "root",
                    "command": [sys.executable, "-c", "raise SystemExit(2)"],
                    "profiles": ["pr-fast"],
                    "cacheable": False,
                },
                {
                    "id": "dependent",
                    "title": "dependent",
                    "command": [sys.executable, "-c", "print('should not run')"],
                    "profiles": ["pr-fast"],
                    "depends_on": ["root"],
                    "cacheable": False,
                },
            ]
            self._write_manifest(root, checks, {"pr-fast": ["root", "dependent"]})
            summary = ValidationEngine(root, jobs=2, use_cache=False).run(profile="pr-fast")
            by_id = {item.check_id: item for item in summary.results}
            self.assertEqual(by_id["root"].status, "validation_failure")
            self.assertEqual(by_id["dependent"].status, "blocked_by_root_failure")
            self.assertEqual(by_id["dependent"].dependency_failures, ["root"])

    def test_changed_selection_falls_back_when_path_is_uncovered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            checks = [
                {
                    "id": "known",
                    "title": "known",
                    "command": [sys.executable, "-c", "print('ok')"],
                    "profiles": ["pr-fast"],
                    "inputs": ["known/**"],
                    "cacheable": False,
                }
            ]
            self._write_manifest(root, checks, {"pr-fast": ["known"]})
            (root / "initial.txt").write_text("a", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "initial"], cwd=root, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            (root / "uncovered.txt").write_text("b", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "change"], cwd=root, check=True)
            summary = ValidationEngine(root, jobs=1, use_cache=False).run(
                profile="pr-fast", changed_base=base
            )
            self.assertTrue(summary.selection_fallback_to_full)
            self.assertTrue(any("uncovered.txt" in note for note in summary.selection_notes))

    def test_cache_reuses_only_identical_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "input.txt"
            input_path.write_text("one\n", encoding="utf-8")
            checks = [
                {
                    "id": "cached",
                    "title": "cached",
                    "command": [sys.executable, "-c", "print('ok')"],
                    "profiles": ["pr-fast"],
                    "inputs": ["input.txt"],
                }
            ]
            self._write_manifest(root, checks, {"pr-fast": ["cached"]})
            engine = ValidationEngine(root, jobs=1, use_cache=True)
            first = engine.run(profile="pr-fast")
            second = engine.run(profile="pr-fast")
            self.assertFalse(first.results[0].cache_hit)
            self.assertTrue(second.results[0].cache_hit)
            input_path.write_text("two\n", encoding="utf-8")
            third = engine.run(profile="pr-fast")
            self.assertFalse(third.results[0].cache_hit)
            self.assertNotEqual(first.results[0].cache_key, third.results[0].cache_key)


class RegisteredResearchCheckerRegressionTests(unittest.TestCase):
    def test_frozen_architecture_neutral_checkers_pass(self) -> None:
        scripts = (
            "tools/check_independent_reasoning_definition.py",
            "tools/check_preservation_basis.py",
            "tools/check_pbts001_replication_package.py",
        )
        for script in scripts:
            with self.subTest(script=script):
                completed = subprocess.run(
                    [sys.executable, script],
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(
                    completed.returncode,
                    0,
                    msg=(
                        f"{script} failed\nstdout:\n{completed.stdout}\n"
                        f"stderr:\n{completed.stderr}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
