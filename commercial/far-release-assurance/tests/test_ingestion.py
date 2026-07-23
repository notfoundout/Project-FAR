from __future__ import annotations

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_release_assurance.cli import main
from far_release_assurance.io import (
    ReleasePackageError,
    canonical_json,
    load_package,
    package_digest,
    package_from_dict,
    package_to_dict,
    write_package,
)
from far_release_assurance.reference_agent import baseline_configuration, run_reference_agent


class TestReleasePackageIngestion(unittest.TestCase):
    def setUp(self):
        self.package = run_reference_agent(baseline_configuration()).package
        self.payload = package_to_dict(self.package)

    def test_round_trip_is_lossless_and_canonical(self):
        reconstructed = package_from_dict(self.payload)
        self.assertEqual(package_to_dict(reconstructed), self.payload)
        self.assertEqual(canonical_json(reconstructed), canonical_json(self.package))

    def test_digest_is_stable_across_input_order(self):
        reordered = dict(self.payload)
        reordered["machinery"] = list(reversed(reordered["machinery"]))
        self.assertEqual(package_digest(package_from_dict(reordered)), package_digest(self.package))

    def test_write_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "release.json"
            write_package(self.package, path)
            loaded = load_package(path)
            self.assertEqual(package_to_dict(loaded), package_to_dict(self.package))
            self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_rejects_wrong_schema_version(self):
        payload = dict(self.payload)
        payload["schema_version"] = "wrong"
        with self.assertRaisesRegex(ReleasePackageError, "schema_version"):
            package_from_dict(payload)

    def test_rejects_cross_release_event(self):
        payload = json.loads(json.dumps(self.payload))
        payload["events"][0]["release_id"] = "other-release"
        with self.assertRaisesRegex(ReleasePackageError, "release_id"):
            package_from_dict(payload)

    def test_rejects_duplicate_event_identity(self):
        payload = json.loads(json.dumps(self.payload))
        payload["events"].append(dict(payload["events"][0], sequence=999))
        with self.assertRaisesRegex(ReleasePackageError, "event_id"):
            package_from_dict(payload)

    def test_rejects_missing_machinery_reference(self):
        payload = json.loads(json.dumps(self.payload))
        payload["events"][0]["machinery_refs"] = ["not-present"]
        with self.assertRaisesRegex(ReleasePackageError, "missing machinery"):
            package_from_dict(payload)

    def test_rejects_invalid_replay_completeness(self):
        payload = dict(self.payload)
        payload["replay_completeness"] = 1.1
        with self.assertRaisesRegex(ReleasePackageError, "between 0 and 1"):
            package_from_dict(payload)

    def test_cli_validate_normalize_digest_and_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "input.json"
            normalized = pathlib.Path(directory) / "normalized.json"
            inventory = pathlib.Path(directory) / "inventory.json"
            write_package(self.package, source)

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main(["validate", str(source)]), 0)
            self.assertIn("VALID baseline", stdout.getvalue())

            self.assertEqual(main(["normalize", str(source), "--output", str(normalized)]), 0)
            self.assertEqual(normalized.read_text(encoding="utf-8"), canonical_json(self.package))

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main(["digest", str(source)]), 0)
            self.assertEqual(stdout.getvalue().strip(), package_digest(self.package))

            self.assertEqual(main(["inventory", str(source), "--output", str(inventory)]), 0)
            inventory_payload = json.loads(inventory.read_text(encoding="utf-8"))
            self.assertEqual(inventory_payload["closure"]["status"], "closed")
            self.assertEqual(inventory_payload["package_digest"], package_digest(self.package))

    def test_cli_invalid_input_has_stable_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "invalid.json"
            source.write_text("{}", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(main(["validate", str(source)]), 10)
            self.assertIn("INVALID", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
