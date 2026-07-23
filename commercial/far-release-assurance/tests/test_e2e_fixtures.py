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
from far_release_assurance.compare import compare_releases
from far_release_assurance.io import load_package
from far_release_assurance.model import Decision

FIXTURES = ROOT / "fixtures" / "e2e"


class TestEndToEndFixtures(unittest.TestCase):
    def setUp(self):
        self.baseline = load_package(FIXTURES / "baseline.json")
        self.passing = load_package(FIXTURES / "candidate-pass.json")
        self.blocked = load_package(FIXTURES / "candidate-blocked.json")

    def test_committed_fixtures_cover_pass_and_blocked_decisions(self):
        self.assertEqual(
            compare_releases(self.baseline, self.passing).comparison.decision,
            Decision.PASS,
        )
        blocked = compare_releases(self.baseline, self.blocked)
        self.assertEqual(blocked.comparison.decision, Decision.BLOCKED)
        self.assertIn(
            "machinery-disclosure-regression",
            {finding.rule_id for finding in blocked.comparison.findings},
        )

    def test_installed_gate_contract_writes_evidence_before_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            pass_output = root / "pass"
            blocked_output = root / "blocked"
            with contextlib.redirect_stdout(io.StringIO()):
                pass_code = main(
                    [
                        "gate",
                        "--baseline",
                        str(FIXTURES / "baseline.json"),
                        "--candidate",
                        str(FIXTURES / "candidate-pass.json"),
                        "--output-directory",
                        str(pass_output),
                    ]
                )
                blocked_code = main(
                    [
                        "gate",
                        "--baseline",
                        str(FIXTURES / "baseline.json"),
                        "--candidate",
                        str(FIXTURES / "candidate-blocked.json"),
                        "--output-directory",
                        str(blocked_output),
                    ]
                )
            self.assertEqual(pass_code, 0)
            self.assertEqual(blocked_code, 30)
            for output, decision in ((pass_output, "pass"), (blocked_output, "blocked")):
                self.assertEqual(
                    {path.name for path in output.iterdir()},
                    {"report.json", "report.md", "manifest.json"},
                )
                report = json.loads((output / "report.json").read_text(encoding="utf-8"))
                manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(report["decision"], decision)
                self.assertEqual(manifest["decision"], decision)


if __name__ == "__main__":
    unittest.main()
