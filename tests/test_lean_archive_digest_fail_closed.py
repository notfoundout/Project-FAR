"""Executable attack test for the digest-bound Lean toolchain acquisition steps."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class LeanArchiveDigestFailClosedTests(unittest.TestCase):
    def test_corrupt_download_never_reaches_extraction(self) -> None:
        installs: list[tuple[Path, str]] = []
        for workflow_path in sorted(WORKFLOWS.glob("*.yml")):
            workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8")) or {}
            for job in (workflow.get("jobs") or {}).values():
                for step in job.get("steps", []):
                    if step.get("name") == "Install pinned Lean toolchain":
                        installs.append((workflow_path, step["run"]))
        self.assertGreaterEqual(len(installs), 2)

        for workflow_path, script in installs:
            with self.subTest(workflow=workflow_path.name), tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                fakebin = temp / "bin"
                fakebin.mkdir()
                marker = temp / "tar-ran"
                curl = fakebin / "curl"
                curl.write_text(
                    "#!/bin/sh\n"
                    "out=''\n"
                    "while [ $# -gt 0 ]; do\n"
                    "  if [ \"$1\" = '-o' ]; then out=$2; shift 2; else shift; fi\n"
                    "done\n"
                    "[ -n \"$out\" ] || exit 64\n"
                    "printf 'attacker-controlled-corrupt-archive' > \"$out\"\n",
                    encoding="utf-8",
                )
                curl.chmod(0o755)
                tar = fakebin / "tar"
                tar.write_text(
                    "#!/bin/sh\n"
                    "printf ran > \"$FAR_FAKE_TAR_MARKER\"\n"
                    "exit 0\n",
                    encoding="utf-8",
                )
                tar.chmod(0o755)
                env = dict(
                    os.environ,
                    PATH=f"{fakebin}:/usr/bin:/bin",
                    RUNNER_TEMP=str(temp),
                    GITHUB_ENV=str(temp / "github-env"),
                    FAR_FAKE_TAR_MARKER=str(marker),
                )
                result = subprocess.run(
                    ["bash", "-c", script], cwd=ROOT, env=env,
                    capture_output=True, text=True, check=False,
                )
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(marker.exists(), "corrupt Lean archive reached extraction")


if __name__ == "__main__":
    unittest.main()
