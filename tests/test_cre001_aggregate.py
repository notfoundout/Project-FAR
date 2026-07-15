from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'tests/fixtures/cre001'
class CRE001AggregateTests(unittest.TestCase):
    def test_aggregation_preserves_three_mappings_and_unknown(self):
        cp=subprocess.run([sys.executable,'tools/cre_001_aggregate.py',str(FIX/'A.json'),str(FIX/'B.json'),str(FIX/'C.json')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stderr); data=json.loads(cp.stdout); self.assertEqual(data['vocabularies'],['A','B','C']); self.assertTrue(all(v=='Unknown' for v in data['existential_sufficiency'].values()))
    def test_missing_artifact_refused(self):
        cp=subprocess.run([sys.executable,'tools/cre_001_aggregate.py',str(FIX/'A.json')],cwd=ROOT,text=True,capture_output=True)
        self.assertNotEqual(cp.returncode,0); self.assertIn('exactly three',cp.stderr)
