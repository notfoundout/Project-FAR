import json, pathlib, subprocess, sys, tempfile, unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"far_investigation_benchmark.py"
MANIFEST=ROOT/"research/comparisons/far-investigation-benchmark-v0.1/manifest.prepared.json"

class BenchmarkManifestTests(unittest.TestCase):
    def run_tool(self,*args):
        return subprocess.run([sys.executable,str(TOOL),*args],cwd=ROOT,text=True,capture_output=True)

    def test_prepared_manifest_validates(self):
        r=self.run_tool("validate","--manifest",str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode,0,r.stderr)

    def test_prepared_manifest_cannot_analyze(self):
        r=self.run_tool("analyze","--manifest",str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode,2)
        self.assertIn("BLOCKED",r.stderr)

    def test_extra_top_level_field_fails_closed(self):
        data=json.loads(MANIFEST.read_text())
        data["unexpected"]=True
        with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False) as f:
            json.dump(data,f); p=f.name
        try:
            r=self.run_tool("validate","--manifest",p)
            self.assertEqual(r.returncode,1)
        finally:
            pathlib.Path(p).unlink(missing_ok=True)

if __name__=="__main__": unittest.main()
