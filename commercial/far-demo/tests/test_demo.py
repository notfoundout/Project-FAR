from __future__ import annotations

import json
import unittest

from fastapi.testclient import TestClient

from far_demo.app import SAMPLE_BASELINE, SAMPLE_CANDIDATE, app


class TestFarDemo(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_identifies_far_engine(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["engine"], "far-decision-integrity")

    def test_example_runs_canonical_adjudication_deterministically(self) -> None:
        first = self.client.get("/api/example").json()
        second = self.client.get("/api/example").json()
        self.assertEqual(first, second)
        self.assertEqual(first["status_transition"], ["justified", "unsupported"])
        self.assertEqual(first["status"], "unsupported")
        self.assertTrue(
            any(item["type"] == "authorization_dependency_removed" for item in first["changes"])
        )
        self.assertTrue(
            any(
                item["rule_id"] == "authorization-dependency-missing"
                for item in first["artifact"]["candidate"]["findings"]
            )
        )
        self.assertEqual(len(first["artifact"]["sha256"]), 64)

    def test_report_download_is_deterministic_json(self) -> None:
        response = self.client.get("/api/example/report")
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response.headers["content-disposition"])
        payload = response.json()
        self.assertEqual(payload["engine"], "far-decision-integrity/1.0.0")
        self.assertEqual(payload["candidate"]["status"], "unsupported")

    def test_upload_flow_accepts_far_decision_packages(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.json", json.dumps(SAMPLE_BASELINE), "application/json"),
                "candidate": ("candidate.json", json.dumps(SAMPLE_CANDIDATE), "application/json"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "unsupported")

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
