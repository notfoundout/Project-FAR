import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "far_investigation_benchmark.py"
MANIFEST = ROOT / "research/comparisons/far-investigation-benchmark-v0.1/manifest.prepared.json"


class BenchmarkManifestTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def temporary_manifest(self, data):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(data, f)
        f.close()
        self.addCleanup(lambda: pathlib.Path(f.name).unlink(missing_ok=True))
        return f.name

    def prepared(self):
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_prepared_manifest_validates(self):
        r = self.run_tool("validate", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_prepared_manifest_cannot_analyze(self):
        r = self.run_tool("analyze", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOCKED", r.stderr)

    def test_extra_top_level_field_fails_closed(self):
        data = self.prepared()
        data["unexpected"] = True
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("additional property", r.stderr)

    def test_nested_schema_violation_fails_closed(self):
        data = self.prepared()
        data["evaluators"] = [{}]
        data["stages"] = "invalid"
        data["times"] = {}
        data["replay"] = {}
        data["limitations"] = []
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("schema", r.stderr)

    def test_schema_pattern_violation_fails_closed(self):
        data = self.prepared()
        data["target"]["commit"] = "not-a-commit"
        data["artifacts"][0]["sha256"] = "xyz"
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("pattern", r.stderr)

    def test_duplicate_unique_schema_values_fail_closed(self):
        data = self.prepared()
        data["limitations"] = ["duplicate", "duplicate"]
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unique", r.stderr)

    def test_unsafe_artifact_path_fails_closed(self):
        data = self.prepared()
        data["artifacts"][0]["path"] = "../outside.md"
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unsafe repository path", r.stderr)

    def test_nonzero_prepared_artifact_hash_is_verified(self):
        data = self.prepared()
        data["artifacts"][0]["sha256"] = "1" * 64
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("hash mismatch", r.stderr)

    def test_source_manifest_hash_is_verified_even_prepared(self):
        data = self.prepared()
        data["source_manifest"] = [
            {
                "path": "tools/far_investigation_benchmark.py",
                "sha256": "1" * 64,
                "role": "validator",
                "verify_current_path": True,
            }
        ]
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("source_manifest", r.stderr)
        self.assertIn("hash mismatch", r.stderr)

    def test_fake_frozen_manifest_fails_completeness_gate(self):
        data = self.prepared()
        data["status"] = "frozen"
        for artifact in data["artifacts"]:
            artifact["sha256"] = "1" * 64
            artifact["verify_current_path"] = False
        data["protocol"]["sha256"] = "1" * 64
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("freeze_time", r.stderr)
        self.assertIn("source_manifest", r.stderr)
        self.assertIn("required artifact", r.stderr)

    def test_frozen_manifest_rejects_prepared_config_sentinels(self):
        data = self.prepared()
        data["status"] = "frozen"
        data["times"]["freeze_time"] = "2026-09-22T19:00:00-04:00"
        data["evaluators"] = [
            {
                "id": f"RATER-{i}",
                "identity": f"rater-{i}",
                "provider": "human",
                "model": "none",
                "prior_exposure": "none",
                "conflicts": "none",
                "lane": "primary" if i < 3 else "other",
            }
            for i in range(1, 4)
        ]
        # The frozen completeness gate must fail before any execution because the
        # prepared bundle still has placeholders and lacks generated/source artifacts.
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertTrue(
            "unset sentinel" in r.stderr or "required artifact" in r.stderr,
            r.stderr,
        )

    def test_unblinding_time_cannot_precede_freeze(self):
        data = self.prepared()
        data["status"] = "unblinded"
        data["times"] = {
            "freeze_time": "2026-09-22T20:00:00-04:00",
            "unblinding_time": "2026-09-22T19:00:00-04:00",
        }
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unblinding_time cannot precede freeze_time", r.stderr)


if __name__ == "__main__":
    unittest.main()
