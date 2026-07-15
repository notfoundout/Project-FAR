from __future__ import annotations
import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class GeneratedAndStatusGovernanceTests(unittest.TestCase):
    def test_generated_theorem_index_check_is_read_only(self):
        before=subprocess.run(['git','status','--short'],cwd=ROOT,text=True,capture_output=True).stdout
        cp=subprocess.run([sys.executable,'tools/generate_theorem_index.py','--check'],cwd=ROOT,text=True,capture_output=True)
        after=subprocess.run(['git','status','--short'],cwd=ROOT,text=True,capture_output=True).stdout
        self.assertEqual(before,after); self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
    def test_no_case_insensitive_project_status_collision(self):
        paths=[p.relative_to(ROOT).as_posix() for p in (ROOT/'docs').glob('*status*.md')]
        lowered={}
        for p in paths: lowered.setdefault(p.lower(),[]).append(p)
        self.assertFalse([v for v in lowered.values() if len(v)>1])
    def test_canonical_status_document_exists(self):
        self.assertTrue((ROOT/'docs/project-status.md').exists())
