"""Regression coverage for reproduced merged-review residuals."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from far_validation.assured_engine import ValidationEngine as AssuredEngine
from far_validation.engine import ValidationEngine, _matches
from far_validation.model import CheckDefinition
from mechanization.far_mechanization.compare_adjudication import (
    InterfaceError, canonical_json_bytes, normalize_package,
)
from tests.test_compare_adjudication import package


class InternalAssuranceRegressionTests(unittest.TestCase):
    def test_globstars_cover_zero_or_multiple_directories(self) -> None:
        for path, pattern in (
            ("README.md", "**/*.md"),
            ("tools/run_tests.py", "tools/**/*.py"),
            ("tools/deep/run_tests.py", "tools/**/*.py"),
            ("a/b.py", "**/a/**/b.py"),
        ):
            with self.subTest(path=path, pattern=pattern):
                self.assertTrue(_matches(path, (pattern,)))
        self.assertFalse(_matches("README.txt", ("**/*.md",)))
        self.assertFalse(_matches("other/run_tests.py", ("tools/**/*.py",)))

    def test_changed_selection_includes_direct_files_even_if_other_check_matches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema_version": "1.0",
                "profiles": {"pr-full": ["markdown", "broad"]},
                "protected_checks": [], "global_invalidation_paths": [],
                "checks": [
                    {"id": name, "title": name, "command": [sys.executable, "-c", "pass"],
                     "profiles": ["pr-full"], "inputs": inputs}
                    for name, inputs in (("markdown", ["**/*.md"]), ("broad", ["README.md"]))
                ],
            }))
            for cls in (ValidationEngine, AssuredEngine):
                selected, _, fallback, _ = cls(root, manifest_path=manifest)._select_changed(
                    "pr-full", ["README.md"]
                )
                self.assertEqual(set(selected), {"markdown", "broad"})
                self.assertFalse(fallback)

    def test_base_timeout_output_remains_serializable(self) -> None:
        engine = ValidationEngine(Path(__file__).resolve().parents[1])
        result = engine._run_command(CheckDefinition(
            "timeout.reproduction", "timeout reproduction",
            command=(sys.executable, "-c",
                     "import os,time; os.write(1,b'partial\\xff'); os.write(2,b'error'); time.sleep(10)"),
            timeout_seconds=1,
        ))
        self.assertEqual(result.status, "timed_out")
        self.assertEqual(result.stdout, "partial\ufffd")
        self.assertEqual(result.stderr, "error")
        self.assertIn("timed_out", json.dumps(result.to_dict()))

    def test_nonfinite_metadata_is_rejected_before_hashing(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                raw = package("nonfinite")
                raw["metadata"]["number"] = value
                with self.assertRaisesRegex(InterfaceError, "finite JSON scalar"):
                    normalize_package(raw)
                with self.assertRaises(ValueError):
                    canonical_json_bytes({"nested": [value]})

    def test_finite_scalar_metadata_preserves_canonical_bytes(self) -> None:
        raw = package("finite")
        raw["metadata"] = {"integer": 3, "float": 0.5, "boolean": True, "null": None}
        normalized = normalize_package(raw)
        encoded = canonical_json_bytes(normalized)
        self.assertEqual(json.loads(encoded), normalized)
        self.assertEqual(encoded, (json.dumps(normalized, ensure_ascii=False, indent=2,
                         sort_keys=True, separators=(",", ": ")) + "\n").encode())


if __name__ == "__main__":
    unittest.main()
