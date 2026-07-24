from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
READINESS = ROOT / "docs" / "releases" / "1.0-readiness.json"
FINDINGS = ROOT / "research" / "external-validation" / "trace-candidate-002" / "findings.md"


class TestRelease10Readiness(unittest.TestCase):
    def test_next_public_release_is_1_0_0(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        self.assertEqual(payload["target_version"], "1.0.0")
        self.assertEqual(payload["previous_public_version"], "0.4.0")
        self.assertFalse(payload["intermediate_public_releases_permitted"])
        self.assertFalse(payload["release_allowed"])

    def test_external_candidates_are_completed(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        completed = payload["completed"]
        self.assertTrue(completed["candidate_001_completed"])
        self.assertTrue(completed["candidate_002_blind_stage_completed"])

    def test_candidate_002_finding_preserves_claim_boundary(self):
        text = FINDINGS.read_text(encoding="utf-8")
        self.assertIn("FAR returned `unverifiable` before benchmark outcome reveal", text)
        self.assertIn("`resolved`: `false`", text)
        self.assertIn("blind stage ordering preserved", text.lower())
        self.assertIn("does not yet establish broad external failure-detection accuracy", text)


if __name__ == "__main__":
    unittest.main()
