import subprocess
import sys
import unittest
from pathlib import Path


class Cre002Ext001Rep001ChecksumTests(unittest.TestCase):
    def test_checksum_lock(self) -> None:
        root = Path(__file__).resolve().parents[1]
        subprocess.run(
            [sys.executable, "tools/check_cre002_ext001_rep001_checksums.py"],
            cwd=root,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
