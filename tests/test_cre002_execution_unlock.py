from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"


class Cre002ExecutionUnlockTests(unittest.TestCase):
    def test_checksum_and_control_verifier_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/check_cre002_lock.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_immutable_package_excludes_mutable_execution_control(self) -> None:
        manifest = json.loads((PACKAGE / "package-manifest.json").read_text())
        locked_paths = {item["path"] for item in manifest["files"]}
        self.assertNotIn("execution-lock.json", locked_paths)
        self.assertEqual(len(locked_paths), 6)
        controls = manifest["mutable_administrative_controls"]
        self.assertEqual(controls[0]["path"], "execution-lock.json")
        self.assertTrue(controls[0]["review_required_for_change"])

    def test_execution_is_authorized_with_complete_evidence(self) -> None:
        control = json.loads((PACKAGE / "execution-lock.json").read_text())
        manifest = json.loads((PACKAGE / "package-manifest.json").read_text())
        audit = json.loads((PACKAGE / "execution-unlock-audit.json").read_text())
        self.assertTrue(control["execution_permitted"])
        self.assertTrue(manifest["execution_permitted"])
        self.assertTrue(audit["execution_permitted_after_merge"])
        self.assertEqual(control["authorization_evidence"]["repository_health_before_unlock"], "passed")
        self.assertFalse(control["authorization_evidence"]["pre_unlock_result_artifacts_present"])

    def test_unlock_creates_no_scientific_result(self) -> None:
        audit = json.loads((PACKAGE / "execution-unlock-audit.json").read_text())
        self.assertFalse(audit["scientific_results_created_by_unlock"])
        for present in audit["pre_unlock_checks"].values():
            self.assertFalse(present)

    def test_nonclaims_remain_preserved(self) -> None:
        required = {
            "universal sufficiency",
            "primitive-only sufficiency",
            "necessity",
            "minimality",
            "independence",
            "superiority",
            "FAR proof",
            "universal structure of reasoning",
        }
        manifest = json.loads((PACKAGE / "package-manifest.json").read_text())
        audit = json.loads((PACKAGE / "execution-unlock-audit.json").read_text())
        self.assertTrue(required.issubset(manifest["nonclaims"]))
        self.assertTrue(required.issubset(audit["nonclaims_preserved"]))


if __name__ == "__main__":
    unittest.main()
