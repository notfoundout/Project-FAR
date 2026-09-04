from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_post_w6_audit_hardening.py"
SPEC = importlib.util.spec_from_file_location("post_w6_audit_hardening", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
HARDENING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARDENING)


class PostW6AuditHardeningTests(unittest.TestCase):
    def test_complete_hardening_record_passes(self) -> None:
        self.assertEqual(HARDENING.check(), [])

    def test_frozen_w6_result_identity_is_preserved(self) -> None:
        self.assertEqual(
            HARDENING.sha256(HARDENING.W6_RESULTS),
            HARDENING.EXPECTED_W6_RESULTS_SHA256,
        )
        self.assertEqual(
            HARDENING.sha256(HARDENING.W6_EXECUTION),
            HARDENING.EXPECTED_W6_EXECUTION_SHA256,
        )

    def test_incident_ledger_distinguishes_scientific_deviations(self) -> None:
        ledger = HARDENING.load_json(HARDENING.INCIDENT_LEDGER)
        self.assertEqual(ledger["scientific_deviations"], [])
        self.assertEqual(
            tuple(item["id"] for item in ledger["execution_incidents"]),
            HARDENING.EXPECTED_INCIDENT_IDS,
        )
        self.assertTrue(
            all(item["changed_scientific_condition"] is False for item in ledger["execution_incidents"])
        )

    def test_branch_protection_cannot_be_relabelled_repository_local(self) -> None:
        record = HARDENING.load_json(HARDENING.HARDENING_RECORD)
        repair = record["repairs"]["control_plane_branch_protection"]
        self.assertEqual(repair["status"], "BLOCKED_EXTERNAL_CONFIGURATION")
        self.assertTrue(repair["required_state"]["protected"])
        self.assertIn("GitHub control-plane read", repair["completion_condition"])
        self.assertIn("Repository files or CI", repair["completion_condition"])

    def test_missing_incident_would_fail_projection(self) -> None:
        ledger = HARDENING.load_json(HARDENING.INCIDENT_LEDGER)
        broken = copy.deepcopy(ledger)
        broken["execution_incidents"] = broken["execution_incidents"][:-1]
        ids = tuple(item["id"] for item in broken["execution_incidents"])
        self.assertNotEqual(ids, HARDENING.EXPECTED_INCIDENT_IDS)

    def test_hardening_does_not_claim_theory_or_w6_result_change(self) -> None:
        record = HARDENING.load_json(HARDENING.HARDENING_RECORD)
        for finding in record["findings"]:
            self.assertEqual(finding["theory_impact"], "NONE")
            self.assertEqual(finding["w6_scientific_result_impact"], "NONE")


if __name__ == "__main__":
    unittest.main()
