"""The EFR-R2 input amendment must preserve frozen v1.0 and stay prospective.

`EFR-001` v1.0 permits later intake to supply only identities, dates, sources and
observations, and permits no later scientific design choices. Correcting which specification
bytes a clean-room team receives is such a choice, so it requires a separately versioned
amendment rather than an edit to the frozen program.

These tests enforce the three properties that make the amendment legitimate:

1. every content-addressed v1.0 artifact is byte-identical to its registered blob;
2. the amendment binds the corrected specification-and-schema bytes actually present in the tree;
3. the canonical EFR authorities still record R2 as pre-execution with an empty input slot and
   zero executed tests/external cases.

Property 3 is deliberately scoped to canonical repository authority. These tests do not claim to
prove the global nonexistence of unregistered external files, communications, or private activity.
"""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "theory/evaluation/external-falsification-and-replication-input-freeze-v1.0.json"
PROGRAM = ROOT / "theory/evaluation/external-falsification-and-replication-program-v1.0.json"
AMENDMENT = ROOT / "theory/evaluation/external-falsification-and-replication-r2-input-amendment-v1.1.json"
AMENDMENT_DOC = ROOT / "docs/governance/external-falsification-and-replication-r2-input-amendment-v1.1.md"

EXPECTED_R2_PACKAGE = {
    "docs/specification/far-ir-2.0-contract.md",
    "docs/specification/far-ir-2.1-approximation-cost.md",
    "schemas/far-contract-v2.schema.json",
    "schemas/far-contract-v2.1.schema.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "hash-object", path], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


class EFRR2InputAmendmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.freeze = load(FREEZE)
        self.program = load(PROGRAM)
        self.amendment = load(AMENDMENT)

    def test_frozen_v1_0_artifacts_are_byte_identical(self) -> None:
        """The amendment must not have edited any frozen EFR v1.0 artifact."""
        for artifact in self.freeze["artifact_objects"]:
            with self.subTest(path=artifact["path"]):
                self.assertEqual(
                    git_blob(artifact["path"]),
                    artifact["git_blob_sha"],
                    f"frozen EFR v1.0 artifact drifted: {artifact['path']}",
                )

    def test_amendment_records_no_frozen_artifact_modification(self) -> None:
        self.assertTrue(self.amendment["frozen_v1_0_preserved"])
        self.assertEqual(self.amendment["frozen_v1_0_artifacts_modified"], [])

    def test_amendment_scope_is_the_r2_input_specification_only(self) -> None:
        self.assertEqual(self.amendment["amends_test"], "EFR-R2")
        self.assertEqual(self.amendment["amends_scope"], "input_specification_only")
        untouched = set(self.amendment["unamended_tests"])
        registered = {test["id"] for test in self.program["tests"]}
        self.assertEqual(untouched, registered - {"EFR-R2"})

    def test_bound_specification_bytes_match_the_working_tree(self) -> None:
        """A bound blob that no longer matches means the package drifted after amendment."""
        for entry in self.amendment["bound_specification_package"]:
            with self.subTest(path=entry["path"]):
                self.assertEqual(
                    git_blob(entry["path"]),
                    entry["git_blob_sha"],
                    f"bound R2 specification byte drift: {entry['path']}",
                )

    def test_schemas_are_unchanged_from_the_v1_0_baseline(self) -> None:
        """Only the two specification documents may differ from the v1.0 package surfaces."""
        by_path = {e["path"]: e for e in self.amendment["bound_specification_package"]}
        for path in ("schemas/far-contract-v2.schema.json", "schemas/far-contract-v2.1.schema.json"):
            self.assertEqual(by_path[path]["provenance"], "unchanged_from_v1.0_baseline")

    def test_mandatory_consequence_is_not_discretionary(self) -> None:
        """The review disposition: 'the owner must decide' is not an acceptable disposition."""
        consequence = self.amendment["mandatory_consequence"]
        self.assertFalse(consequence["discretionary"])
        self.assertIn("MUST NOT execute", consequence["rule"])
        text = AMENDMENT_DOC.read_text(encoding="utf-8")
        self.assertIn(
            "**`EFR-R2` MUST NOT execute against the corrected specifications under the "
            "unamended v1.0 freeze.**",
            text,
        )

    def test_canonical_pre_execution_state_matches_frozen_authorities(self) -> None:
        """Fail closed if canonical EFR authority no longer records the pre-execution state."""
        state = self.amendment["canonical_pre_execution_state"]
        evidence = state["machine_checked_evidence"]
        self.assertEqual(
            set(evidence),
            {
                "efr_r2_status",
                "all_test_statuses",
                "efr_r2_input_slot_state",
                "current_results_tests_executed",
                "current_results_external_cases",
            },
        )

        r2 = next(test for test in self.program["tests"] if test["id"] == "EFR-R2")
        self.assertEqual(r2["status"], evidence["efr_r2_status"])
        self.assertEqual(r2["status"], "PREREGISTERED_NOT_EXECUTED")

        statuses = {test["status"] for test in self.program["tests"]}
        self.assertEqual(statuses, {evidence["all_test_statuses"]})
        self.assertEqual(statuses, {"PREREGISTERED_NOT_EXECUTED"})

        slot = next(s for s in self.freeze["external_input_slots"] if s["test_id"] == "EFR-R2")
        self.assertEqual(slot["state"], evidence["efr_r2_input_slot_state"])
        self.assertEqual(slot["state"], "EMPTY_AWAITING_INDEPENDENT_CUSTODIAN_SEAL")

        results = self.freeze["current_results"]
        self.assertEqual(results["tests_executed"], evidence["current_results_tests_executed"])
        self.assertEqual(results["tests_executed"], 0)
        self.assertEqual(results["external_cases"], evidence["current_results_external_cases"])
        self.assertEqual(results["external_cases"], 0)

    def test_prospectivity_claim_is_scoped_to_canonical_authority(self) -> None:
        state = self.amendment["canonical_pre_execution_state"]
        self.assertIn("canonical EFR authorities", state["claim"])
        self.assertIn("do not establish the global nonexistence", state["scope_boundary"])
        text = AMENDMENT_DOC.read_text(encoding="utf-8")
        self.assertIn("These checks prove what the repository can prove", text)
        self.assertIn("do not prove the global nonexistence", text)

    def test_amendment_claims_no_assurance_upgrade(self) -> None:
        nonclaims = " ".join(self.amendment["nonclaims"])
        self.assertIn("does not execute EFR-R2", nonclaims)
        self.assertIn("does not establish global nonexistence", nonclaims)
        self.assertIn("does not close OP-28", nonclaims)
        self.assertEqual(self.amendment["status"], "PREREGISTERED_AMENDMENT_NOT_EXECUTED")

    def test_permitted_package_contains_only_specs_and_schemas(self) -> None:
        self.assertTrue(self.amendment["permitted_package_is_specification_and_schema_only"])
        prohibited = self.amendment["prohibited_inputs_unchanged"]
        self.assertIn("generated expected outputs", prohibited)
        self.assertIn("another team's code", prohibited)
        bound = {e["path"] for e in self.amendment["bound_specification_package"]}
        self.assertEqual(bound, EXPECTED_R2_PACKAGE)
        self.assertFalse(any(path.startswith("mechanization/") for path in bound))
        self.assertNotIn("mechanization/far_mechanization/diagnostic_vocabulary.py", bound)
        self.assertIn(
            "not supplied to clean-room teams",
            self.amendment["internal_declaration_not_in_r2_package"],
        )


if __name__ == "__main__":
    unittest.main()
