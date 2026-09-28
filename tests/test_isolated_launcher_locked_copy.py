"""Adversarial regressions for the pre-candidate-code validator launcher."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "validation_bootstrap" / "assurance-lock.json"
LAUNCHER = ROOT / "validation_bootstrap" / "run_isolated.py"


class LockedCopyIsolationTests(unittest.TestCase):
    def fixture(self, directory: str) -> Path:
        root = Path(directory)
        (root / "validation_bootstrap").mkdir(parents=True)
        shutil.copy2(LAUNCHER, root / "validation_bootstrap" / "run_isolated.py")
        shutil.copy2(LOCK, root / "validation_bootstrap" / "assurance-lock.json")
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        for relative in sorted(lock["files"]):
            if not (relative.startswith("far_validation/") and relative.endswith(".py")):
                continue
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return root

    def run_launcher(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-I", str(root / "validation_bootstrap" / "run_isolated.py"), *args],
            cwd=root,
            env={"PATH": str(Path(sys.executable).parent) + ":/usr/bin:/bin"},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_unlocked_package_initializer_and_root_modules_never_execute(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            marker = root / "candidate-code-ran"
            (root / "far_validation" / "__init__.py").write_text(
                f"from pathlib import Path\nPath({str(marker)!r}).write_text('package')\n",
                encoding="utf-8",
            )
            (root / "nt.py").write_text(
                f"from pathlib import Path\nPath({str(marker)!r}).write_text('root')\n",
                encoding="utf-8",
            )
            result = self.run_launcher(root, "formal", "--max-checks", "1", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists(), result.stdout + result.stderr)

    def test_locked_module_tampering_fails_before_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            target = root / "far_validation" / "oracle.py"
            target.write_text(target.read_text(encoding="utf-8") + "\nraise SystemExit(0)\n", encoding="utf-8")
            result = self.run_launcher(root, "oracle", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertIn("locked module hash mismatch: far_validation/oracle.py", result.stderr)

    def test_launcher_exposes_only_the_frozen_trusted_command_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            result = self.run_launcher(root, "validate")
            self.assertEqual(result.returncode, 2)
            self.assertIn("command must be one of", result.stderr)


if __name__ == "__main__":
    unittest.main()
