from __future__ import annotations

import json
import unittest

from fastapi.testclient import TestClient

from far_demo.app import SAMPLE_BASELINE, SAMPLE_CANDIDATE, app


class TestFarDemo(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_example_is_deterministic_and_detects_missing_approval(self) -> None:
        first = self.client.get("/api/example").json()["result"]
        second = self.client.get("/api/example").json()["result"]
        self.assertEqual(first, second)
        self.assertEqual(first["verdict"], "unsupported")
        self.assertTrue(any(item["type"] == "authorization_expansion" for item in first["findings"]))
        self.assertEqual(len(first["report_sha256"]), 64)

    def test_upload_flow(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.json", json.dumps(SAMPLE_BASELINE), "application/json"),
                "candidate": ("candidate.json", json.dumps(SAMPLE_CANDIDATE), "application/json"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["verdict"], "unsupported")

    def test_rejects_non_json_uploads(self) -> None:
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.txt", "x", "text/plain"),
                "candidate": ("candidate.json", "{}", "application/json"),
            },
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
