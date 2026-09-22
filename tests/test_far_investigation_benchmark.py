import json, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "far_investigation_benchmark.py"
MANIFEST = ROOT / "research/comparisons/far-investigation-benchmark-v0.1/manifest.prepared.json"

class BenchmarkManifestTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *args], cwd=ROOT, text=True, capture_output=True)

    def temporary_manifest(self, data):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(data, f)
        f.close()
        self.addCleanup(lambda: pathlib.Path(f.name).unlink(missing_ok=True))
        return f.name

    def test_prepared_manifest_validates(self):
        r = self.run_tool("validate", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_prepared_manifest_cannot_analyze(self):
        r = self.run_tool("analyze", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOCKED", r.stderr)

    def test_extra_top_level_field_fails_closed(self):
        data = json.loads(MANIFEST.read_text())
        data["unexpected"] = True
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("schema <root>", r.stderr)

    def test_nested_schema_violation_fails_closed(self):
        data = json.loads(MANIFEST.read_text())
        data["evaluators"] = [{}]
        data["stages"] = "invalid"
        data["times"] = {}
        data["replay"] = {}
        data["limitations"] = []
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("schema", r.stderr)

    def test_fake_frozen_manifest_fails_completeness_gate(self):
        data = json.loads(MANIFEST.read_text())
        data["status"] = "frozen"
        for a in data["artifacts"]:
            a["sha256"] = "1" * 64
            a["verify_current_path"] = False
        data["protocol"]["sha256"] = "1" * 64
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("frozen-or-later", r.stderr)

if __name__ == "__main__":
    unittest.main()