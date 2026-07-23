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
from far_release_assurance.io import write_package
from far_release_assurance.reference_agent import (
    AgentConfiguration,
    baseline_configuration,
    run_reference_agent,
)
from far_release_assurance.report import build_report_bundle, report_payload


class TestReleaseReports(unittest.TestCase):
    def setUp(self):
        self.baseline = run_reference_agent(baseline_configuration()).package
        self.candidate = run_reference_agent(
            AgentConfiguration(
                release_id="candidate-report",
                source_commit="candidate-report-commit",
                customer_source="shadow-customer-db",
                customer_source_declared=False,
            )
        ).package
        self.summary = compare_releases(self.baseline, self.candidate)

    def test_report_payload_is_versioned_and_decision_complete(self):
        payload = report_payload(self.baseline, self.candidate, self.summary)
        self.assertEqual(payload["schema_version"], "far-release-report/0.1")
        self.assertEqual(payload["decision"], "blocked")
        self.assertEqual(payload["candidate"]["source_commit"], "candidate-report-commit")
        self.assertGreater(payload["summary"]["blocking_finding_count"], 0)
        self.assertIn("does not prove hidden cognition", payload["claim_boundary"])

    def test_bundle_is_deterministic(self):
        first = build_report_bundle(self.baseline, self.candidate, self.summary)
        second = build_report_bundle(self.baseline, self.candidate, self.summary)
        self.assertEqual(first, second)
        self.assertTrue(first.report_json.endswith("\n"))
        self.assertTrue(first.report_markdown.endswith("\n"))
        self.assertTrue(first.manifest_json.endswith("\n"))

    def test_manifest_binds_both_packages_and_both_reports(self):
        bundle = build_report_bundle(self.baseline, self.candidate, self.summary)
        manifest = json.loads(bundle.manifest_json)
        self.assertEqual(manifest["schema_version"], "far-evidence-manifest/0.1")
        self.assertEqual(manifest["decision"], "blocked")
        for key in (
            "baseline_package_digest",
            "candidate_package_digest",
            "report_json_digest",
            "report_markdown_digest",
        ):
            self.assertRegex(manifest[key], r"^[0-9a-f]{64}$")

    def test_markdown_contains_actionable_findings(self):
        bundle = build_report_bundle(self.baseline, self.candidate, self.summary)
        self.assertIn("# FAR Release Assurance Report", bundle.report_markdown)
        self.assertIn("**Decision:** Blocked", bundle.report_markdown)
        self.assertIn("machinery-disclosure-regression", bundle.report_markdown)
        self.assertIn("customer-data", bundle.report_markdown)

    def test_cli_report_writes_complete_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            baseline_path = root / "baseline.json"
            candidate_path = root / "candidate.json"
            output_directory = root / "report"
            write_package(self.baseline, baseline_path)
            write_package(self.candidate, candidate_path)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(
                    [
                        "report",
                        "--baseline",
                        str(baseline_path),
                        "--candidate",
                        str(candidate_path),
                        "--output-directory",
                        str(output_directory),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertIn("REPORT candidate-report blocked", stdout.getvalue())
            self.assertEqual(
                {path.name for path in output_directory.iterdir()},
                {"report.json", "report.md", "manifest.json"},
            )
            payload = json.loads((output_directory / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["decision"], "blocked")

    def test_pass_report_has_no_findings(self):
        summary = compare_releases(self.baseline, self.baseline)
        bundle = build_report_bundle(self.baseline, self.baseline, summary)
        payload = json.loads(bundle.report_json)
        self.assertEqual(payload["decision"], "pass")
        self.assertEqual(payload["summary"]["finding_count"], 0)
        self.assertIn("No findings.", bundle.report_markdown)


if __name__ == "__main__":
    unittest.main()
