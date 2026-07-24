from __future__ import annotations

import json
import subprocess
import unittest
from unittest.mock import patch

import run_comparison


DIGEST = "sha256:" + "a" * 64


class DigestResolutionTests(unittest.TestCase):
    def test_tagged_reference_adds_latest(self) -> None:
        self.assertEqual(run_comparison.tagged_reference("swebench/example"), "swebench/example:latest")
        self.assertEqual(run_comparison.tagged_reference("swebench/example:v1"), "swebench/example:v1")
        self.assertEqual(run_comparison.tagged_reference(f"swebench/example@{DIGEST}"), f"swebench/example@{DIGEST}")

    def test_parse_digest_requires_exactly_one_unique_digest(self) -> None:
        self.assertEqual(run_comparison.parse_digest(f"Digest: {DIGEST}\n{DIGEST}"), DIGEST)
        with self.assertRaises(ValueError):
            run_comparison.parse_digest("no digest")
        with self.assertRaises(ValueError):
            run_comparison.parse_digest(f"{DIGEST}\nsha256:{'b' * 64}")

    @patch("run_comparison.shutil.which", return_value="/usr/bin/docker")
    @patch("run_comparison.run")
    def test_buildx_registry_lookup_is_primary(self, mocked_run, _mocked_which) -> None:
        mocked_run.return_value = f"Name: example\nDigest: {DIGEST}\n"
        self.assertEqual(run_comparison.resolve_image_digest("swebench/example"), DIGEST)
        mocked_run.assert_called_once_with(
            ["docker", "buildx", "imagetools", "inspect", "swebench/example:latest"]
        )

    @patch("run_comparison.shutil.which", return_value="/usr/bin/docker")
    @patch("run_comparison.run")
    def test_manifest_lookup_is_independent_fallback(self, mocked_run, _mocked_which) -> None:
        mocked_run.side_effect = [
            subprocess.CalledProcessError(1, ["docker", "buildx"]),
            json.dumps({"Descriptor": {"digest": DIGEST}}),
        ]
        self.assertEqual(run_comparison.resolve_image_digest("swebench/example:v1"), DIGEST)
        self.assertEqual(mocked_run.call_count, 2)

    @patch("run_comparison.shutil.which", return_value="/usr/bin/docker")
    @patch("run_comparison.run")
    def test_both_registry_methods_failing_is_fatal(self, mocked_run, _mocked_which) -> None:
        mocked_run.side_effect = subprocess.CalledProcessError(1, ["docker"])
        with self.assertRaises(SystemExit):
            run_comparison.resolve_image_digest("swebench/example")


if __name__ == "__main__":
    unittest.main()
