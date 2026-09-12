import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from far_build_backend import build_wheel


class WheelRelocationTests(unittest.TestCase):
    def test_noneditable_wheel_is_relocatable_for_far_intake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wheel_dir = root / "wheel"
            target = root / "installed"
            wheel_dir.mkdir()
            target.mkdir()

            wheel_path = wheel_dir / build_wheel(str(wheel_dir))
            with zipfile.ZipFile(wheel_path) as archive:
                names = set(archive.namelist())
                archive.extractall(target)

            self.assertIn("mechanization/far_mechanization/intake_v1.py", names)
            self.assertIn("jsonschema/__init__.py", names)
            self.assertIn("schemas/far-intake-v1.schema.json", names)
            self.assertFalse(any(name.endswith(".pth") for name in names))

            code = "\n".join(
                [
                    "from mechanization.far_mechanization.intake_v1 import (",
                    "    SCHEMA_PATH, new_manifest, validate_manifest,",
                    ")",
                    "assert SCHEMA_PATH.is_file(), SCHEMA_PATH",
                    "manifest = new_manifest('raw', 'INTAKE-RELOCATED-001')",
                    "errors = validate_manifest(manifest)",
                    "assert errors == [], errors",
                ]
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(target)
            result = subprocess.run(
                [sys.executable, "-S", "-c", code],
                cwd=root,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
