from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "research" / "external-validation"


class TestTraceCandidate002Freeze(unittest.TestCase):
    def test_candidate_001_result_is_recorded_with_boundary(self):
        findings = json.loads(
            (VALIDATION / "trace-candidate-001" / "findings.json").read_text(encoding="utf-8")
        )
        self.assertEqual(findings["result"], "unverifiable")
        self.assertEqual(findings["trace_completeness"], 0.0)
        self.assertFalse(findings["semantic_completeness_verified"])
        self.assertFalse(findings["blind_detection_value_permitted"])
        self.assertEqual(
            set(findings["finding_ids"]), {"declared-unknowns", "trace-incomplete"}
        )

    def test_candidate_002_is_frozen_before_identity_and_outcome(self):
        protocol = json.loads(
            (VALIDATION / "trace-candidate-002" / "protocol.json").read_text(encoding="utf-8")
        )
        self.assertEqual(protocol["status"], "frozen-before-outcome-inspection")
        self.assertTrue(protocol["blind_execution_required"])
        self.assertFalse(protocol["contamination"]["candidate_identity_known_before_freeze"])
        self.assertFalse(protocol["contamination"]["outcome_known_before_freeze"])
        forbidden = set(protocol["selection"]["outcome_fields_forbidden_before_freeze"])
        self.assertIn("resolved", forbidden)
        self.assertIn("exit_status", forbidden)

    def test_candidate_002_claims_preserve_unknowns_and_stage_order(self):
        payload = json.loads(
            (VALIDATION / "trace-candidate-002" / "claims.json").read_text(encoding="utf-8")
        )
        self.assertTrue(payload["frozen_before_selection_and_outcome_inspection"])
        claims = {claim["claim_id"]: claim for claim in payload["claims"]}
        self.assertEqual(set(claims), {
            "C002-01", "C002-02", "C002-03", "C002-04", "C002-05", "C002-06"
        })
        self.assertEqual(claims["C002-01"]["absence_rule"], "unverifiable-not-false")
        self.assertEqual(claims["C002-04"]["expected_status"], "unverifiable")
        self.assertEqual(claims["C002-06"]["absence_rule"], "invalidate-blind-claim")


if __name__ == "__main__":
    unittest.main()
