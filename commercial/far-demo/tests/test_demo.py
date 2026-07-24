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
        self.assertEqual(
            first["headline"],
            "The updated agent refunded $420 without recorded supervisor approval.",
        )
        self.assertEqual(len(first["structural_changes"]), 1)
        self.assertEqual(first["structural_changes"][0]["type"], "authorization_dependency_removed")
        self.assertGreaterEqual(len(first["rule_findings"]), 1)
        self.assertEqual(first["changes"], first["structural_changes"] + first["rule_findings"])
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
        payload = response.json()
        self.assertEqual(payload["status"], "unsupported")
        self.assertEqual(
            payload["headline"],
            "The candidate decision is unsupported by the supplied dependency record.",
        )
        self.assertIn("customer-refund", payload["plain_summary"])
        self.assertIn("1 dependency", payload["plain_summary"])
        self.assertNotIn("dependencyy", payload["plain_summary"])
        self.assertNotIn("$420", payload["headline"])
        self.assertNotIn("supervisor", payload["headline"].lower())
        self.assertEqual(len(payload["structural_changes"]), 1)

    def test_uploaded_non_refund_packages_never_receive_sample_facts(self) -> None:
        baseline = {
            "schema_version": "far-decision-package/0.1",
            "decision_id": "access-baseline",
            "decision_type": "database-access",
            "policy_version": "access-policy-v2",
            "decision_root": "grant-access",
            "proposed_action": {"type": "grant_database_access", "resource": "analytics"},
            "nodes": [
                {
                    "node_id": "request",
                    "kind": "evidence",
                    "statement": "An analyst requested analytics database access.",
                    "attributes": {"valid": True},
                },
                {
                    "node_id": "approval",
                    "kind": "authorization",
                    "statement": "The data owner approved access.",
                    "attributes": {"valid": True},
                },
                {
                    "node_id": "grant-access",
                    "kind": "decision",
                    "statement": "Grant analytics database access.",
                    "attributes": {"valid": True},
                },
            ],
            "dependencies": [
                {"source_id": "request", "target_id": "grant-access", "relation": "supports"},
                {"source_id": "approval", "target_id": "grant-access", "relation": "authorizes"},
            ],
            "authorization_requirements": ["approval"],
            "unknowns": [],
            "trace_completeness": 1.0,
            "metadata": {},
        }
        candidate = {
            **baseline,
            "decision_id": "access-candidate",
            "dependencies": [
                {"source_id": "request", "target_id": "grant-access", "relation": "supports"},
            ],
            "unknowns": ["Whether approval was recorded elsewhere."],
            "trace_completeness": 0.8,
        }
        response = self.client.post(
            "/api/analyze",
            files={
                "baseline": ("baseline.json", json.dumps(baseline), "application/json"),
                "candidate": ("candidate.json", json.dumps(candidate), "application/json"),
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        combined = " ".join(
            [payload["headline"], payload["plain_summary"], payload["why_it_matters"]]
        ).lower()
        self.assertIn("database-access", combined)
        self.assertIn("data owner approved access", combined)
        self.assertIn("1 dependency", combined)
        self.assertNotIn("dependencyy", combined)
        self.assertNotIn("refund", combined)
        self.assertNotIn("$420", combined)
        self.assertNotIn("supervisor", combined)
        self.assertEqual(len(payload["structural_changes"]), 1)
        self.assertGreaterEqual(len(payload["rule_findings"]), 1)

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
