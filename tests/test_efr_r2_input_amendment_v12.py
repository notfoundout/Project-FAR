"""EFR-R2 input amendment v1.2 must be versioned successor material that alters no frozen object.

v1.2 supersedes only the permitted R2 specification package. It keeps every v1.1-bound byte,
adds versioned errata, is layered on comparator amendment v2.0 without changing it, and binds the
reference verifiers that must generate the R2 frozen expected result. v1.1 itself stays valid on
its own bytes; ``tests/test_efr_r2_input_amendment.py`` checks that independently.

The canonical pre-execution state is checked against canonical repository authority only; these
tests do not claim to prove the global nonexistence of unregistered external activity.
"""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "theory/evaluation"
AMENDMENT = EVAL / "external-falsification-and-replication-r2-input-amendment-v1.2.json"
AMENDMENT_DOC = ROOT / "docs/governance/external-falsification-and-replication-r2-input-amendment-v1.2.md"
V1_1 = EVAL / "external-falsification-and-replication-r2-input-amendment-v1.1.json"
V2_0 = EVAL / "external-falsification-and-replication-comparator-amendment-v2.0.json"
PROGRAM = EVAL / "external-falsification-and-replication-program-v1.0.json"
FREEZE = EVAL / "external-falsification-and-replication-input-freeze-v1.0.json"

ERRATA = {"docs/specification/far-ir-2.0-errata-1.md", "docs/specification/far-ir-2.1-errata-1.md"}
FROZEN_VERIFIER_BLOBS = {
    "mechanization/far_mechanization/contract_v2.py": "31a4c00dcbee9adfe9e7c19fcacb4c04578e3b61",
    "mechanization/far_mechanization/contract_v2_strict.py": "06c69ea6c99cdd878365ad3cc2cbe04b4fc1bccc",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: str) -> str:
    return subprocess.run(["git", "hash-object", path], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


class EFRR2InputAmendmentV12Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.amendment = load(AMENDMENT)
        self.v11 = load(V1_1)
        self.v20 = load(V2_0)

    def test_scope_is_the_r2_input_specification_only(self) -> None:
        self.assertEqual(self.amendment["amends_test"], "EFR-R2")
        self.assertEqual(self.amendment["amends_scope"], "input_specification_only")
        self.assertEqual(self.amendment["frozen_v1_0_artifacts_modified"], [])
        self.assertEqual(self.amendment["status"], "PREREGISTERED_AMENDMENT_NOT_EXECUTED")

    def test_v1_1_package_is_kept_byte_for_byte_and_only_errata_are_added(self) -> None:
        old = {e["path"]: e["git_blob_sha"] for e in self.v11["bound_specification_package"]}
        new = {e["path"]: e for e in self.amendment["bound_specification_package"]}
        self.assertEqual(set(new), set(old) | ERRATA)
        for path, blob in old.items():
            with self.subTest(path=path):
                self.assertEqual(new[path]["git_blob_sha"], blob)
                self.assertNotEqual(new[path]["provenance"], "added_by_amendment_1_2")
        for path in ERRATA:
            self.assertEqual(new[path]["provenance"], "added_by_amendment_1_2")

    def test_every_bound_and_preserved_blob_matches_the_working_tree(self) -> None:
        entries = (
            self.amendment["bound_specification_package"]
            + self.amendment["preserved_objects"]
            + self.amendment["reference_verifiers"]["verifiers"]
        )
        for entry in entries:
            with self.subTest(path=entry["path"]):
                self.assertEqual(git_blob(entry["path"]), entry["git_blob_sha"])

    def test_superseded_and_layered_amendments_are_preserved(self) -> None:
        preserved = {e["path"]: e["git_blob_sha"] for e in self.amendment["preserved_objects"]}
        for path in (
            "theory/evaluation/external-falsification-and-replication-r2-input-amendment-v1.1.json",
            "docs/governance/external-falsification-and-replication-r2-input-amendment-v1.1.md",
            "theory/evaluation/external-falsification-and-replication-comparator-amendment-v2.0.json",
            "docs/governance/external-falsification-and-replication-comparator-amendment-v2.0.md",
            "mechanization/far_mechanization/contract_v21.py",
            *FROZEN_VERIFIER_BLOBS,
        ):
            self.assertIn(path, preserved)
        for path, blob in FROZEN_VERIFIER_BLOBS.items():
            self.assertEqual(preserved[path], blob)
        # v2.0 still binds the frozen baseline and rule v1.0 verifier this amendment preserves.
        v20_bound = {e["path"]: e["git_blob_sha"] for e in self.v20["bound_artifacts"]}
        for path, blob in FROZEN_VERIFIER_BLOBS.items():
            self.assertEqual(v20_bound[path], blob)
        self.assertEqual(self.amendment["superseded_amendment"]["amendment_id"], self.v11["amendment_id"])
        self.assertEqual(self.amendment["layered_on"]["amendment_id"], self.v20["amendment_id"])

    def test_unamended_tests_are_the_tests_registered_after_comparator_amendment_v2_0(self) -> None:
        program_tests = {test["id"] for test in load(PROGRAM)["tests"]}
        superseded = set(self.v20["superseded_tests"])
        replacements = {test["id"] for test in self.v20["replacement_tests"]}
        registered = (program_tests - superseded) | replacements
        self.assertEqual(set(self.amendment["unamended_tests"]), registered - {"EFR-R2"})
        self.assertEqual(self.amendment["superseded_tests_untouched"], self.v20["superseded_tests"])

    def test_reference_verifiers_wrap_the_frozen_verifiers_and_are_not_r2_inputs(self) -> None:
        verifiers = {e["path"]: e for e in self.amendment["reference_verifiers"]["verifiers"]}
        self.assertEqual(
            {e["wraps"] for e in verifiers.values()},
            {"mechanization/far_mechanization/contract_v2.py", "mechanization/far_mechanization/contract_v21.py"},
        )
        for path in verifiers:
            source = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn(Path(verifiers[path]["wraps"]).stem, source)
        package = {e["path"] for e in self.amendment["bound_specification_package"]}
        self.assertTrue(self.amendment["permitted_package_is_specification_and_schema_only"])
        self.assertFalse(any(path.startswith("mechanization/") for path in package))
        self.assertIn("never supplied to clean-room teams", self.amendment["reference_verifiers"]["rule"])

    def test_mandatory_consequence_is_not_discretionary(self) -> None:
        consequence = self.amendment["mandatory_consequence"]
        self.assertFalse(consequence["discretionary"])
        self.assertIn("MUST NOT execute", consequence["rule"])
        self.assertIn(
            "**`EFR-R2` MUST NOT execute against the v1.2-corrected specifications under "
            "amendment v1.1 or the unamended v1.0 freeze.**",
            AMENDMENT_DOC.read_text(encoding="utf-8"),
        )

    def test_canonical_pre_execution_state_matches_frozen_authorities(self) -> None:
        evidence = self.amendment["canonical_pre_execution_state"]["machine_checked_evidence"]
        program, freeze = load(PROGRAM), load(FREEZE)
        self.assertEqual({test["status"] for test in program["tests"]}, {evidence["all_test_statuses"]})
        slot = next(s for s in freeze["external_input_slots"] if s["test_id"] == "EFR-R2")
        self.assertEqual(slot["state"], evidence["efr_r2_input_slot_state"])
        self.assertEqual(freeze["current_results"]["tests_executed"], evidence["current_results_tests_executed"])
        self.assertEqual(freeze["current_results"]["external_cases"], evidence["current_results_external_cases"])
        self.assertEqual(self.v20["current_results"]["tests_executed"], 0)
        self.assertIn("do not establish the global nonexistence", self.amendment["canonical_pre_execution_state"]["scope_boundary"])

    def test_amendment_claims_no_assurance_upgrade(self) -> None:
        nonclaims = " ".join(self.amendment["nonclaims"])
        for phrase in ("does not execute EFR-R2", "does not close OP-28", "does not alter any v1.0, v1.1, or v2.0 frozen object"):
            self.assertIn(phrase, nonclaims)


if __name__ == "__main__":
    unittest.main()
