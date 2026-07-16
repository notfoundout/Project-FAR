from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REP = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001"
ROB = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-ROB-001"
COMPILERS = [
    ROOT / "tools/cre002_compilers/compiler_recursive.py",
    ROOT / "tools/cre002_compilers/compiler_iterative.py",
    ROOT / "tools/cre002_compilers/compiler_pairs.py",
]
VERIFIER = ROOT / "tools/cre002_compilers/verifier.py"


class CRE002EXT001ReplicationDispositionTests(unittest.TestCase):
    def test_human_team_track_is_superseded_and_unexecuted(self):
        manifest = json.loads((REP / "package-manifest.json").read_text(encoding="utf-8"))
        control = json.loads((REP / "execution-lock.json").read_text(encoding="utf-8"))
        registry = json.loads((REP / "team-registry.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "superseded-not-executed")
        self.assertEqual(manifest["execution_history"], "not executed")
        self.assertEqual(manifest["superseded_by"], "CRE-002-EXT-001-ROB-001")
        self.assertFalse(manifest["team_registration_authorized"])
        self.assertFalse(manifest["execution_authorized"])
        self.assertEqual(control["state"], "superseded-not-executed-permanently-locked")
        self.assertFalse(control["team_registration_authorized"])
        self.assertFalse(control["execution_authorized"])
        self.assertFalse(control["compiler_implementation_authorized"])
        self.assertEqual(registry["teams"], [])
        self.assertEqual(registry["execution_history"], "not executed")
        self.assertFalse(registry["registration_authorized"])
        self.assertFalse(registry["execution_unlock_eligible"])

    def test_replacement_claim_is_bounded_robustness_only(self):
        readme = (ROB / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("bounded multi-implementation robustness", readme)
        self.assertIn("not independent external replication", readme)
        self.assertIn("three distinct compiler source files", readme)

    def test_compilers_and_verifier_are_separate_files(self):
        self.assertTrue(all(path.is_file() for path in COMPILERS))
        self.assertTrue(VERIFIER.is_file())
        self.assertEqual(len({path.read_bytes() for path in COMPILERS}), 3)
        for compiler in COMPILERS:
            text = compiler.read_text(encoding="utf-8")
            self.assertNotIn("cre002_ext001_robustness", text)
            self.assertNotIn("cre002_compilers.verifier", text)

    def test_automated_multi_implementation_robustness(self):
        result = subprocess.run(
            [sys.executable, "tools/cre002_ext001_robustness.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["implementations"], 3)
        self.assertTrue(report["byte_identical"])
        self.assertTrue(report["deterministic_rerun"])
        self.assertTrue(report["separate_source_files"])
        self.assertEqual(len(report["compiler_files"]), 3)
        self.assertEqual(report["verifier_file"], "tools/cre002_compilers/verifier.py")
        self.assertEqual(report["claim_class"], "bounded multi-implementation robustness")
        self.assertFalse(report["external_replication"])
        self.assertTrue(all(case["rejected"] for case in report["mutation_and_adversarial_cases"]))


if __name__ == "__main__":
    unittest.main()
