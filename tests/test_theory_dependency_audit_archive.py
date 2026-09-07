import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXECUTOR = ROOT / "research/theory-dependency-audit/execute.py"
SPEC = importlib.util.spec_from_file_location("archive_audit", EXECUTOR)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class TheoryDependencyAuditArchiveTests(unittest.TestCase):
    def test_vendored_source_blobs_match_preregistered_locks(self):
        spec = json.loads(audit.SPEC_PATH.read_text())
        frozen_root = ROOT / "research/theory-dependency-audit/frozen-source-v1.0"
        for relative, expected_sha in spec["source_locks"].items():
            path = frozen_root / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(expected_sha, audit.git_blob_sha(path.read_bytes()), relative)

    def test_gitless_archive_replays_committed_result(self):
        spec = json.loads(audit.SPEC_PATH.read_text())
        committed = json.loads(audit.RESULT_PATH.read_text())
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            audit_dir = root / "research/theory-dependency-audit"
            audit_dir.mkdir(parents=True)
            shutil.copy2(audit.SPEC_PATH, audit_dir / "execution-spec-v1.0.json")
            shutil.copy2(audit.RESULT_PATH, audit_dir / "result-v1.0.json")

            frozen_root = ROOT / "research/theory-dependency-audit/frozen-source-v1.0"
            target_frozen = audit_dir / "frozen-source-v1.0"
            for relative in spec["source_locks"]:
                source = frozen_root / relative
                target = target_frozen / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            self.assertFalse((root / ".git").exists())
            self.assertEqual(committed, audit.execute(root=root))

    def test_tampered_vendored_source_fails_closed(self):
        spec = json.loads(audit.SPEC_PATH.read_text())
        relative = next(iter(spec["source_locks"]))
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            audit_dir = root / "research/theory-dependency-audit"
            audit_dir.mkdir(parents=True)
            shutil.copy2(audit.SPEC_PATH, audit_dir / "execution-spec-v1.0.json")

            frozen_root = ROOT / "research/theory-dependency-audit/frozen-source-v1.0"
            target_frozen = audit_dir / "frozen-source-v1.0"
            for locked_relative in spec["source_locks"]:
                source = frozen_root / locked_relative
                target = target_frozen / locked_relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            target = target_frozen / relative
            target.write_bytes(target.read_bytes() + b"\nTAMPERED\n")
            with self.assertRaisesRegex(ValueError, "vendored frozen source identity mismatch"):
                audit.read_base_blob(root, spec["base_commit"], relative)


if __name__ == "__main__":
    unittest.main()
