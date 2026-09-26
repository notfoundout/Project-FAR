from __future__ import annotations

import copy
import json
import pathlib
import unittest

from tools.validate_exact_1_0_candidate import validate_readiness

ROOT = pathlib.Path(__file__).resolve().parents[1]
READINESS = ROOT / "docs" / "releases" / "1.0-readiness.json"
FINDINGS = ROOT / "research" / "external-validation" / "trace-candidate-002" / "findings.md"


class TestRelease10Readiness(unittest.TestCase):
    def test_next_public_release_is_1_0_0(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        self.assertEqual(payload["target_version"], "1.0.0")
        self.assertEqual(payload["previous_public_version"], "0.4.0")
        self.assertFalse(payload["intermediate_public_releases_permitted"])

        if payload["status"] == "publication-authorized":
            self.assertTrue(payload["release_allowed"])
            self.assertEqual(payload["remaining"], {})
            self.assertTrue(payload["completed"]["exact_release_commit_validation"])
            self.assertTrue(payload["completed"]["explicit_publication_authorization"])
        else:
            self.assertFalse(payload["release_allowed"])

    def test_exact_candidate_validator_accepts_current_readiness(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        validate_readiness(payload)

    def test_exact_candidate_validator_rejects_inconsistent_authorization(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        payload = copy.deepcopy(payload)
        payload["status"] = "publication-authorized"
        payload["release_allowed"] = False
        with self.assertRaisesRegex(SystemExit, "must allow release"):
            validate_readiness(payload)

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
