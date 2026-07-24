from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
READINESS = ROOT / "docs" / "releases" / "1.0-readiness.json"
AUTHORIZATION = ROOT / "docs" / "releases" / "1.0-publication-authorization.md"
PYPROJECT = ROOT / "commercial" / "far-decision-integrity" / "pyproject.toml"


class TestRelease10PublicationAuthorization(unittest.TestCase):
    def test_release_is_explicitly_authorized(self):
        payload = json.loads(READINESS.read_text(encoding="utf-8"))
        self.assertEqual(payload["target_version"], "1.0.0")
        self.assertEqual(payload["previous_public_version"], "0.4.0")
        self.assertEqual(payload["status"], "publication-authorized")
        self.assertTrue(payload["release_allowed"])
        self.assertEqual(payload["remaining"], {})
        self.assertTrue(payload["completed"]["exact_release_commit_validation"])
        self.assertTrue(payload["completed"]["explicit_publication_authorization"])

    def test_authorization_preserves_claim_boundary(self):
        text = AUTHORIZATION.read_text(encoding="utf-8")
        self.assertIn("exact merge commit", text)
        self.assertIn("does not expand Project FAR's scientific claims", text)
        self.assertIn("unrestricted universality", text)

    def test_package_version_is_1_0_0(self):
        text = PYPROJECT.read_text(encoding="utf-8")
        self.assertIn('version = "1.0.0"', text)


if __name__ == "__main__":
    unittest.main()
