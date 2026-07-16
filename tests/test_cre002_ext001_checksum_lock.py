from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"


class Cre002Ext001ChecksumLockTests(unittest.TestCase):
    def test_checksum_lock_verifier_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/check_cre002_ext001_checksums.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_lock_keeps_execution_disabled(self) -> None:
        lock = json.loads((PACKAGE / "checksum-lock.json").read_text(encoding="utf-8"))
        self.assertFalse(lock["execution_permitted"])
        self.assertFalse(lock["compiler_implementation_permitted"])
        self.assertFalse(lock["official_results_present"])


if __name__ == "__main__":
    unittest.main()
