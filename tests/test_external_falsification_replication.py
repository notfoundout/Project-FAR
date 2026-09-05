from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM_PATH = ROOT / "theory/evaluation/external-falsification-and-replication-program-v1.0.json"
FREEZE_PATH = ROOT / "theory/evaluation/external-falsification-and-replication-input-freeze-v1.0.json"
SECURITY_PATH = ROOT / "theory/evaluation/privileged-token-retirement-v1.0.json"
RETIREMENT_WORKFLOW = ROOT / ".github/workflows/retire-far-github-admin-token.yml"


class ExternalFalsificationReplicationTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_program_is_preregistered_successor_not_w7(self) -> None:
        data = self.load(PROGRAM_PATH)
        self.assertEqual(data["program_id"], "EXTERNAL-FALSIFICATION-AND-REPLICATION-001")
        self.assertEqual(data["status"], "PREREGISTERED_NOT_EXECUTED")
        self.assertIs(data["is_w7"], False)
        self.assertEqual(data["predecessor"]["status"], "COMPLETE_AT_SIX_REGISTERED_SCOPES")
        self.assertEqual(
            {item["id"] for item in data["tests"]},
            {"EFR-R1", "EFR-R2", "EFR-H1", "EFR-A1", "EFR-HD1", "EFR-U1", "EFR-C1", "EFR-N1"},
        )
        self.assertTrue(all(item["status"] == "PREREGISTERED_NOT_EXECUTED" for item in data["tests"]))

    def test_inputs_and_no_post_hoc_rules_are_frozen(self) -> None:
        data = self.load(PROGRAM_PATH)
        freeze = self.load(FREEZE_PATH)
        self.assertEqual(data["evidence_baseline"], freeze["evidence_baseline"])
        self.assertEqual(freeze["freeze_status"], "FROZEN_BEFORE_EXECUTION")
        self.assertTrue(freeze["selection_and_analysis_rules_frozen"])
        self.assertEqual(
            {slot["state"] for slot in freeze["external_input_slots"]},
            {"EMPTY_AWAITING_INDEPENDENT_CUSTODIAN_SEAL"},
        )
        rules = data["freeze_and_deviation_rules"]
        self.assertTrue(rules["selection_rules_frozen"])
        self.assertTrue(rules["inputs_must_be_custodian_hashed_before_unblinding"])
        self.assertTrue(rules["post_unblinding_case_replacement_prohibited"])
        self.assertTrue(rules["original_protocol_and_result_retained"])
        self.assertTrue(rules["favorable_post_hoc_reclassification_prohibited"])

    def test_every_family_has_explicit_acceptance_and_failure(self) -> None:
        data = self.load(PROGRAM_PATH)
        for test in data["tests"]:
            with self.subTest(test=test["id"]):
                self.assertIn("acceptance", test)
                self.assertIn("failure", test)
                self.assertTrue(test["acceptance"])
                self.assertTrue(test["failure"])
        cost = next(item for item in data["tests"] if item["id"] == "EFR-C1")
        self.assertIs(cost["no_scalarization"], True)
        novelty = next(item for item in data["tests"] if item["id"] == "EFR-N1")
        self.assertIs(novelty["no_positive_novelty_inference"], True)
        self.assertEqual(len(novelty["essential_elements"]), 4)

    def test_canonical_matrix_has_exact_six_rows_and_boundaries(self) -> None:
        text = (ROOT / "docs/governance/w1-w6-claim-evidence-matrix-v1.0.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| `PCA-W([1-6])[^\n]+$", text, flags=re.MULTILINE)
        self.assertEqual(rows, ["1", "2", "3", "4", "5", "6"])
        self.assertIn("I1 — Claimed Isolation", text)
        self.assertIn("not I3 external independent validation", text)
        self.assertIn("does **not** prove that every scalarization is impossible", text)
        self.assertIn("finite-corpus result, not a population estimate", text)

    def test_current_surfaces_link_canonical_matrix_and_program(self) -> None:
        for relative in ("README.md", "docs/project-status.md", "docs/ROADMAP.md", "docs/CANONICAL_MAP.md"):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("w1-w6-claim-evidence-matrix-v1.0.md", text)
                self.assertIn("external-falsification-and-replication-program-v1.0.md", text)

    def test_privileged_token_path_is_fail_closed(self) -> None:
        security = self.load(SECURITY_PATH)
        refs = set()
        for path in (ROOT / ".github/workflows").glob("*.yml"):
            if "FAR_GITHUB_ADMIN_TOKEN" in path.read_text(encoding="utf-8"):
                refs.add(path.name)
        legacy = {"canonical-branch-protection.yml", "configure-validation-protection.yml"}
        if RETIREMENT_WORKFLOW.exists():
            self.assertEqual(refs, legacy | {RETIREMENT_WORKFLOW.name})
            workflow = RETIREMENT_WORKFLOW.read_text(encoding="utf-8")
            self.assertNotIn("workflow_dispatch", workflow)
            self.assertNotIn("actions/checkout", workflow)
            self.assertIn("github.ref == 'refs/heads/main'", workflow)
            self.assertEqual(security["status"], "SCHEDULED_ON_FIRST_MAIN_MERGE")
            self.assertIs(security["accepted_receipt"], None)
        else:
            self.assertEqual(refs, legacy)
            self.assertEqual(security["status"], "ACCEPTED_RETIRED")
            self.assertTrue(security["accepted_receipt"]["secret_absent"])
            self.assertTrue(security["accepted_receipt"]["branch_protection_unchanged_and_enforced"])
            self.assertEqual(
                set(security["accepted_receipt"]["privileged_workflow_states"].values()),
                {"disabled_manually"},
            )


if __name__ == "__main__":
    unittest.main()
