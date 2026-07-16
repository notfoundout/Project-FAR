from __future__ import annotations
import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CRE001SemanticRegressionTests(unittest.TestCase):
    def test_frozen_semantic_specification_is_consistent(self):
        cp=subprocess.run([sys.executable,'tools/check_cre001_semantics.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('CRE-001 SEMANTIC CHECK PASSED', cp.stdout)
if __name__=='__main__': unittest.main()
