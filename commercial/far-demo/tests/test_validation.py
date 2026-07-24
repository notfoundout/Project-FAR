from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from far_demo.validation_app import app


class TestValidationFeedback(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.payload = {
            "role": "ai_engineering",
            "organization_type": "ai_startup",
            "strongest_use_case": "release_assurance",
            "clarity_score": 5,
            "trust_score": 4,
            "release_action": "block_release",
            "would_share_authorized_artifacts": True,
            "budget_owner_identified": "yes",
            "design_partner_interest": True,
            "contact_email": "tester@example.com",
            "source": "founder-outreach-01",
            "session_id": "session-12345678",
            "consent_to_store": True,
        }

    def test_validation_page_includes_structured_study(self) -> None:
        response = self.client.get("/?source=founder-outreach-01")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Would this change a real release decision?", response.text)
        self.assertIn("release_assurance", response.text)
        self.assertIn("does not collect uploaded package contents", response.text)

    def test_validation_config_declares_privacy_boundary(self) -> None:
        response = self.client.get("/api/validation-config")
        self.assertEqual(response.status_code, 200)
        privacy = response.json()["privacy"]
        self.assertFalse(privacy["uploaded_package_contents_collected"])
        self.assertFalse(privacy["uploaded_filenames_collected"])
        self.assertFalse(privacy["free_text_collected"])

    def test_feedback_returns_deterministic_receipt_shape_and_logs_structured_event(self) -> None:
        with patch("far_demo.validation_app.logger.info") as info:
            response = self.client.post("/api/feedback", json=self.payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "recorded")
        self.assertEqual(len(body["receipt"]), 64)
        info.assert_called_once()
        logged = info.call_args.args[1]
        self.assertIn('"strongest_use_case":"release_assurance"', logged)
        self.assertNotIn("uploaded", logged)

    def test_feedback_requires_consent(self) -> None:
        payload = {**self.payload, "consent_to_store": False}
        response = self.client.post("/api/feedback", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Consent is required", response.json()["detail"])

    def test_feedback_rejects_out_of_range_scores(self) -> None:
        payload = {**self.payload, "clarity_score": 6}
        response = self.client.post("/api/feedback", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_feedback_rejects_free_form_tracking_values(self) -> None:
        payload = {**self.payload, "source": "<script>alert(1)</script>"}
        response = self.client.post("/api/feedback", json=payload)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
