from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from tools import check_repository_truth as truth

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTruthTests(unittest.TestCase):
    def test_checker_passes_current_repository(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/check_repository_truth.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["successful"])
        self.assertEqual(payload["package_version"], "0.6.0")
        self.assertEqual(payload["latest_release"], "v1.0.0")
        self.assertEqual(payload["governing_core"], "PROJECT-FAR-CORE-THEORY-1.1")
        self.assertEqual(payload["historical_core"], "PROJECT-FAR-CORE-THEORY-1.0")
        self.assertEqual(
            payload["historical_core_sha256"],
            "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5",
        )
        self.assertEqual(payload["specification_export_version"], "1.2.0")
        self.assertEqual(payload["current_program"], "POST-CLOSURE-001")
        self.assertEqual(
            payload["completed_domain_contracts_workstream"],
            "PCA-W4-DOMAIN-CONTRACTS",
        )
        self.assertEqual(
            payload["completed_approximation_cost_workstream"],
            "PCA-W5-APPROXIMATION-AND-COST",
        )
        self.assertEqual(
            payload["completed_audit_utility_workstream"],
            "PCA-W6-EMPIRICAL-AUDIT-UTILITY",
        )
        self.assertIsNone(payload["active_workstream"])
        self.assertEqual(
            payload["domain_contracts_status"],
            "six_finite_explicit_native_contracts_six_lossy_collisions_six_scoped_repairs_internal_mapping_only",
        )
        self.assertEqual(
            payload["audit_utility_status"],
            "bounded_internal_registered_collision_detection_6_of_6_clean_acceptance_6_of_6_oracle_agreement_12_of_12_human_and_external_utility_not_established",
        )
        self.assertEqual(
            payload["current_phase"],
            "post-closure registered program complete; downstream external utility open",
        )

    def test_terminal_w6_boundary_cannot_reopen_a_registered_w7(self) -> None:
        authority = json.loads((ROOT / "governance/repository-truth-authority-v1.json").read_text())
        status = authority["project_status"]
        self.assertIsNone(status["active_workstream"])
        self.assertEqual(
            status["completed_audit_utility_workstream"],
            "PCA-W6-EMPIRICAL-AUDIT-UTILITY",
        )
        boundaries = " ".join(authority["claim_boundaries"])
        self.assertIn("no registered W7", boundaries)
        self.assertIn("OP-28", boundaries)

    def test_version_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path.endswith("__init__.py"):
                return text.replace('__version__ = "0.6.0"', '__version__ = "9.9.9"')
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("package version drift", str(caught.exception))

    def test_historical_dashboard_cannot_be_current(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text + "\nCurrent project phase: W3.5\n"
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("historical W3.5 dashboard", str(caught.exception))

    def test_release_badge_tag_pin_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text.replace(
                    "](https://github.com/notfoundout/Project-FAR/releases/latest)\n",
                    "](https://github.com/notfoundout/Project-FAR/releases/tag/v1.0.0)\n",
                    1,
                )
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("latest-release route", str(caught.exception))

    def test_release_badge_version_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text.replace("Release v1.0.0", "Release v0.4.0", 1)
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("release badge drift", str(caught.exception))

    def test_release_record_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "docs/releases/project-far-v1.0.0.md":
                return text.replace("v1.0.0", "v0.4.0")
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("release record", str(caught.exception))

    def test_export_manifest_cannot_repromote_v1_0(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "exports/far-spec-v1/manifest.json":
                payload = json.loads(text)
                for row in payload["artifacts"]:
                    if row["path"] == "theorems/Project-FAR-Theory-Closure-v1.0.md":
                        row["status"] = "canonical"
                return json.dumps(payload)
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("preserve v1.0 as historical", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
