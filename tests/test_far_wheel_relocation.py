import os
import json
import subprocess
import sys
import tempfile
import unittest
import venv
import zipfile
from pathlib import Path

from far_build_backend import build_wheel
from tests.test_far_intake_v1 import STAMP, manifest


class WheelRelocationTests(unittest.TestCase):
    def test_installed_console_script_completes_intake_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wheel_path = root / build_wheel(str(root))
            environment = root / "venv"
            venv.EnvBuilder(with_pip=True).create(environment)
            scripts = environment / ("Scripts" if os.name == "nt" else "bin")
            python = scripts / ("python.exe" if os.name == "nt" else "python")
            env = os.environ.copy()
            env.pop("PYTHONPATH", None)
            env.pop("PYTHONHOME", None)
            installed = subprocess.run(
                [str(python), "-I", "-m", "pip", "install", "--no-deps", "--no-index",
                 "--disable-pip-version-check", str(wheel_path)],
                cwd=root, env=env, text=True, capture_output=True, timeout=60,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            cli = scripts / ("far-intake.exe" if os.name == "nt" else "far-intake")

            def run(*args, expected=0):
                result = subprocess.run(
                    [str(cli), *args], cwd=root, env=env, text=True,
                    capture_output=True, timeout=10,
                )
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                return json.loads(result.stdout) if result.stdout else None

            draft = root / "draft.json"
            run("init", "Ω café 😀", "--write", str(draft))
            self.assertEqual(json.loads(draft.read_text())["raw_input"]["text"], "Ω café 😀")
            self.assertTrue(run("validate", str(draft))["valid"])
            self.assertFalse(run("validate", str(draft), "--ready", expected=1)["valid"])
            ready = root / "ready.json"
            ready.write_text(json.dumps(manifest()), encoding="utf-8")
            self.assertTrue(run("validate", str(ready), "--ready")["valid"])
            frozen = root / "frozen.json"
            run("freeze", str(ready), "--frozen-at", STAMP, "--write", str(frozen))
            self.assertTrue(run("validate", str(frozen))["valid"])
            self.assertEqual(run("aggregate", str(frozen), expected=1)["outcome"], "INCOMPLETE")
            record = json.loads(frozen.read_text())
            record["evaluations"] = [
                {"contract_id": row["id"], "contract_sha256": row["sha256"],
                 "freeze_sha256": record["freeze"]["freeze_sha256"], "outcome": "PROVED",
                 "evaluated_at": "2026-09-12T12:01:00Z", "evidence_refs": ["urn:example:proof"]}
                for row in record["discovery"]["contract_candidates"]
            ]
            frozen.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(run("aggregate", str(frozen))["outcome"], "INVARIANTLY_PROVED")
            record["raw_input"]["text"] = "tampered"
            frozen.write_text(json.dumps(record), encoding="utf-8")
            self.assertEqual(run("aggregate", str(frozen), expected=1)["outcome"], "INVALID")
            ready.write_text('{"id": "a", "id": "b"}', encoding="utf-8")
            self.assertFalse(run("validate", str(ready), expected=1)["valid"])

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
