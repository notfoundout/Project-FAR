from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANDIDATE_ROOT = ROOT / "research" / "external-validation" / "trace-candidate-001"


class TestTraceCandidate001Freeze(unittest.TestCase):
    def test_candidate_identity_and_source_are_frozen(self):
        candidate = json.loads((CANDIDATE_ROOT / "candidate.json").read_text(encoding="utf-8"))
        self.assertEqual(candidate["candidate_id"], "trace-candidate-001")
        self.assertEqual(candidate["instance_id"], "django__django-15044")
        self.assertEqual(candidate["submission"], "20240402_sweagent_gpt4")
        self.assertEqual(candidate["source"]["revision"], "04eb93d")
        self.assertEqual(candidate["source"]["selection"]["filename"], "django__django-15044.traj")

    def test_contamination_boundary_blocks_blind_claim(self):
        candidate = json.loads((CANDIDATE_ROOT / "candidate.json").read_text(encoding="utf-8"))
        contamination = candidate["contamination"]
        self.assertTrue(contamination["outcome_exposed_before_freeze"])
        self.assertFalse(contamination["decisive_blind_detection_claim_permitted"])

    def test_claims_are_frozen_and_preserve_absence_boundary(self):
        payload = json.loads((CANDIDATE_ROOT / "claims.json").read_text(encoding="utf-8"))
        self.assertTrue(payload["frozen_before_acquisition"])
        claims = {claim["claim_id"]: claim for claim in payload["claims"]}
        self.assertEqual(set(claims), {"C001", "C002", "C003", "C004", "C005"})
        self.assertEqual(claims["C001"]["absence_rule"], "unverifiable-not-false")
        self.assertEqual(claims["C002"]["absence_rule"], "unverifiable-not-false")
        self.assertEqual(claims["C004"]["expected_status"], "unverifiable")

    def test_acquisition_script_pins_dataset_revision(self):
        script = (CANDIDATE_ROOT / "acquire_candidate.py").read_text(encoding="utf-8")
        self.assertIn('revision=source["revision"]', script)
        self.assertIn('"downloaded_sha256": _sha256(parquet_path)', script)
        self.assertIn('expected exactly one candidate row', script)


if __name__ == "__main__":
    unittest.main()
