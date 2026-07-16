from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
class TestCre002Ext001Preregistration(unittest.TestCase):
    def test_preregistration_checker(self):
        cp=subprocess.run([sys.executable,'tools/check_cre002_ext001_preregistration.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
if __name__=='__main__': unittest.main()
