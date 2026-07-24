from __future__ import annotations

import csv
import io
import json
import unittest

import yaml
from fastapi.testclient import TestClient

from far_demo.app import SAMPLE_BASELINE, SAMPLE_CANDIDATE, app
from far_demo.formats import SUPPORTED_EXTENSIONS, parse_package_file


class TestFarDemo(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_identifies_far_engine(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["engine"], "far-decision-integrity")

    def test_example_is_deterministic_and_blocks_control_regression(self) -> None:
        first = self.client.get("/api/example").json()
        second = self.client.get("/api/example").json()
        self.assertEqual(first, second)
        self.assertEqual(first["status_transition"], ["justified", "unsupported"])
        self.assertEqual(first["status"], "unsupported")
        self.assertEqual(first["release_decision"], "BLOCKED")
        self.assertEqual(len(first["structural_changes"]), 2)
        self.assertGreaterEqual(len(first["rule_findings"]), 1)
        removed = {item["node_id"] for item in first["structural_changes"]}
        self.assertEqual(removed, {"sanctions-clearance", "treasury-approval"})
        self.assertEqual(first["changes"], first["structural_changes"] + first["rule_findings"])
        self.assertEqual(len(first["artifact"]["sha256"]), 64)

    def test_report_download_contains_release_decision(self) -> None:
        response = self.client.get("/api/example/report")
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response.headers["content-disposition"])
        payload = response.json()
        self.assertEqual(payload["engine"], "far-decision-integrity/1.0.0")
        self.assertEqual(payload["candidate"]["status"], "unsupported")
        self.assertEqual(payload["release_decision"], "BLOCKED")

    def test_page_presents_frontier_treasury_experience(self) -> None:
        page = self.client.get("/").text
        self.assertIn("Your eval says", page)
        self.assertIn("$2.4M", page)
        self.assertIn("NovaGrid Systems GmbH", page)
        self.assertIn("Run release-integrity audit", page)
        self.assertNotIn("$420 refund", page)
        self.assertNotIn("#d9ff6a", page.lower())

    def test_json_upload_flow_remains_evidence_bound(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.json", json.dumps(SAMPLE_BASELINE), "application/json"),
                "candidate": ("candidate.json", json.dumps(SAMPLE_CANDIDATE), "application/json"),
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "unsupported")
        self.assertEqual(payload["release_decision"], "BLOCKED")
        self.assertEqual(len(payload["structural_changes"]), 2)
        self.assertIn("2 dependencies", payload["plain_summary"])
        self.assertNotIn("NovaGrid", payload["headline"])

    def test_yaml_and_markdown_can_be_mixed(self) -> None:
        baseline_yaml = yaml.safe_dump(SAMPLE_BASELINE, sort_keys=False)
        candidate_markdown = "# Candidate\n\n```json\n" + json.dumps(SAMPLE_CANDIDATE) + "\n```\n"
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.yaml", baseline_yaml, "application/yaml"),
                "candidate": ("candidate.md", candidate_markdown, "text/markdown"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["release_decision"], "BLOCKED")

    def test_tabular_csv_adapter_handles_richer_package(self) -> None:
        stream = io.StringIO()
        fields = [
            "record_type", "key", "value", "node_id", "kind", "statement",
            "attributes", "source_id", "target_id", "relation",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for key in (
            "schema_version", "decision_id", "decision_type", "policy_version",
            "decision_root", "trace_completeness",
        ):
            writer.writerow({"record_type": "meta", "key": key, "value": json.dumps(SAMPLE_BASELINE[key])})
        for key, value in SAMPLE_BASELINE["proposed_action"].items():
            writer.writerow({"record_type": "meta", "key": f"proposed_action.{key}", "value": json.dumps(value)})
        for node in SAMPLE_BASELINE["nodes"]:
            writer.writerow({"record_type": "node", **node, "attributes": json.dumps(node["attributes"])})
        for dependency in SAMPLE_BASELINE["dependencies"]:
            writer.writerow({"record_type": "dependency", **dependency})
        for node_id in SAMPLE_BASELINE["authorization_requirements"]:
            writer.writerow({"record_type": "authorization_requirement", "node_id": node_id})
        parsed = parse_package_file("baseline.csv", stream.getvalue().encode())
        self.assertEqual(parsed["decision_id"], "treasury-wire-baseline-741")
        self.assertEqual(len(parsed["nodes"]), 8)
        self.assertEqual(len(parsed["dependencies"]), 7)
        self.assertEqual(len(parsed["authorization_requirements"]), 2)

    def test_common_extensions_are_declared(self) -> None:
        expected = {
            ".json", ".jsonl", ".yaml", ".yml", ".toml", ".xml", ".csv",
            ".txt", ".md", ".docx", ".pdf", ".xlsx",
        }
        self.assertEqual(SUPPORTED_EXTENSIONS, expected)

    def test_rejects_unknown_extension(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.exe", b"not a package", "application/octet-stream"),
                "candidate": ("candidate.json", json.dumps(SAMPLE_CANDIDATE), "application/json"),
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported file type", response.json()["detail"])

    def test_rejects_non_far_json(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.json", "{}", "application/json"),
                "candidate": ("candidate.json", "{}", "application/json"),
            },
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
