import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CRE002ChecksumLockTests(unittest.TestCase):
    def test_checksum_lock_matches_frozen_package(self):
        completed = subprocess.run(
            [sys.executable, "tools/check_cre002_lock.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if completed.returncode != 0:
            self.fail(completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
