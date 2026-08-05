from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/target-category-discovery/verify_program_freeze.py"
MANIFEST_PATH = ROOT / "research/target-category-discovery/freeze-manifest-v1.0.json"
AUDIT_MANIFEST_PATH = ROOT / "research/target-category-discovery/audit-manifest-v1.1.json"
spec = importlib.util.spec_from_file_location("verify_program_freeze", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ProgramFreezeTests(unittest.TestCase):

    def test_audit_manifest_registers_current_freeze(self) -> None:
        audit = json.loads(AUDIT_MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(audit["schema_version"], "1.1")
        self.assertEqual(audit["artifact_status"], "Research")
        self.assertFalse(audit["execution_gate"]["authorized"])
        self.assertEqual(
            audit["freeze_manifest"]["path"],
            "research/target-category-discovery/freeze-manifest-v1.0.json",
        )
        self.assertEqual(
            audit["freeze_manifest"]["governed_file_count"],
            len(module.REQUIRED_GOVERNED_PATHS),
        )

    def test_current_freeze_passes(self) -> None:
        result = module.verify(MANIFEST_PATH)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["files_checked"], len(module.REQUIRED_GOVERNED_PATHS))

    def _manifest_copy(self) -> dict:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def _write_manifest(self, data: dict, directory: str) -> Path:
        path = Path(directory) / "manifest.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_duplicate_path_is_rejected(self) -> None:
        data = self._manifest_copy()
        data["files"].append(dict(data["files"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_manifest(data, tmp)
            with self.assertRaisesRegex(module.FreezeError, "sorted|duplicate"):
                module.verify(path)

    def test_unsorted_paths_are_rejected(self) -> None:
        data = self._manifest_copy()
        data["files"][0], data["files"][1] = data["files"][1], data["files"][0]
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_manifest(data, tmp)
            with self.assertRaisesRegex(module.FreezeError, "sorted"):
                module.verify(path)

    def test_missing_required_path_is_rejected(self) -> None:
        data = self._manifest_copy()
        data["files"].pop()
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_manifest(data, tmp)
            with self.assertRaisesRegex(module.FreezeError, "path set mismatch"):
                module.verify(path)

    def test_invalid_digest_is_rejected(self) -> None:
        data = self._manifest_copy()
        data["files"][0]["sha256"] = "bad"
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_manifest(data, tmp)
            with self.assertRaisesRegex(module.FreezeError, "invalid SHA"):
                module.verify(path)

    def test_governed_file_mutation_is_rejected(self) -> None:
        data = self._manifest_copy()
        target = data["files"][0]["path"]
        fake_root = Path(tempfile.mkdtemp())
        try:
            # Mirror every governed file so the test reaches the mutated target.
            for entry in data["files"]:
                source = ROOT / entry["path"]
                destination = fake_root / entry["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
            (fake_root / target).write_bytes((fake_root / target).read_bytes() + b"x")
            with mock.patch.object(module, "REPO_ROOT", fake_root):
                with self.assertRaisesRegex(module.FreezeError, "digest mismatch"):
                    module.verify(MANIFEST_PATH)
        finally:
            import shutil
            shutil.rmtree(fake_root)


if __name__ == "__main__":
    unittest.main()
