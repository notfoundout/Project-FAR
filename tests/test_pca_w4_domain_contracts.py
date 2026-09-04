from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from mechanization.far_mechanization.contract_v2 import contract_sha256
from tools.check_pca_w4_domain_contracts import (
    RESULTS,
    audit_document,
    load_json,
    manifest_integrity_errors,
    manifest_record_set_errors,
    validate_campaign,
    validate_program_progression,
)

ROOT = Path(__file__).resolve().parents[1]


class PCAW4DomainContractTests(unittest.TestCase):
    def test_complete_campaign_passes(self) -> None:
        self.assertEqual(validate_campaign(ROOT), [])
        self.assertEqual(
            len([path for path in RESULTS.glob("*.json") if path.name != "manifest.json"]),
            12,
        )

    def test_all_six_domains_have_checked_collision_and_repair(self) -> None:
        for lossy_path in sorted(RESULTS.glob("*-lossy.json")):
            repaired_path = RESULTS / lossy_path.name.replace("-lossy.json", "-repaired.json")
            lossy, repaired = load_json(lossy_path), load_json(repaired_path)
            self.assertEqual(lossy["report"]["outcome"], "REFUTED")
            self.assertEqual(lossy["report"]["evidence"]["kind"], "collision")
            self.assertEqual(lossy["report"]["evidence"]["status"], "CHECKED_FINITE_EXPLICIT")
            self.assertEqual(repaired["report"]["outcome"], "PROVED")
            self.assertEqual(repaired["report"]["evidence"]["kind"], "factorization")
            self.assertEqual(repaired["report"]["evidence"]["status"], "CHECKED_FINITE_EXPLICIT")

    def test_native_recomputation_rejects_changed_causal_behavior(self) -> None:
        document = load_json(RESULTS / "bayesian-causal-lossy.json")
        broken = copy.deepcopy(document)
        broken["contract"]["required_behavior"]["table"][1]["value"] = {"numerator": 0, "denominator": 1}
        broken["freeze"]["contract_sha256"] = contract_sha256(broken["contract"])
        codes = {item["code"] for item in audit_document(broken)}
        self.assertIn("W4_NATIVE_BEHAVIOR_MISMATCH", codes)

    def test_native_recomputation_honors_declared_causal_distribution(self) -> None:
        document = load_json(RESULTS / "bayesian-causal-lossy.json")
        broken = copy.deepcopy(document)
        for case in broken["contract"]["source_domain"]["cases"]:
            case["value"]["u_distribution"] = [
                {"u": 0, "probability": "3/4"},
                {"u": 1, "probability": "1/4"},
            ]
        broken["freeze"]["contract_sha256"] = contract_sha256(broken["contract"])
        codes = {item["code"] for item in audit_document(broken)}
        self.assertIn("W4_NATIVE_BEHAVIOR_MISMATCH", codes)
        self.assertIn("W4_NATIVE_REPRESENTATION_MISMATCH", codes)

    def test_native_recomputation_rejects_invalid_causal_distribution(self) -> None:
        document = load_json(RESULTS / "bayesian-causal-lossy.json")
        broken = copy.deepcopy(document)
        broken["contract"]["source_domain"]["cases"][0]["value"]["u_distribution"] = [
            {"u": 0, "probability": "3/4"},
            {"u": 1, "probability": "1/2"},
        ]
        broken["freeze"]["contract_sha256"] = contract_sha256(broken["contract"])
        codes = {item["code"] for item in audit_document(broken)}
        self.assertIn("W4_NATIVE_CASE_INVALID", codes)

    def test_native_recomputation_rejects_changed_repair(self) -> None:
        document = load_json(RESULTS / "argumentation-repaired.json")
        broken = copy.deepcopy(document)
        broken["contract"]["representation"]["table"][1]["value"]["defeats"] = [["A", "B"]]
        broken["report"]["evidence"]["decoder_table"][1]["representation_value"]["defeats"] = [["A", "B"]]
        broken["freeze"]["contract_sha256"] = contract_sha256(broken["contract"])
        codes = {item["code"] for item in audit_document(broken)}
        self.assertIn("W4_NATIVE_REPRESENTATION_MISMATCH", codes)

    def test_provenance_hash_mutation_is_detected(self) -> None:
        document = load_json(RESULTS / "proof-theory-lossy.json")
        broken = copy.deepcopy(document)
        broken["provenance"]["sources"][0]["sha256"] = "0" * 64
        codes = {item["code"] for item in audit_document(broken)}
        self.assertIn("W4_SOURCE_HASH_MISMATCH", codes)

    def test_manifest_requires_every_frozen_result(self) -> None:
        manifest = load_json(RESULTS / "manifest.json")
        broken = copy.deepcopy(manifest)
        broken["records"] = broken["records"][:-1]
        codes = {item["code"] for item in manifest_record_set_errors(broken)}
        self.assertIn("W4_MANIFEST_RECORD_SET_MISMATCH", codes)

    def test_frozen_record_hash_drift_never_becomes_mutable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "frozen.json"
            path.write_text("mutated\n", encoding="utf-8")
            manifest = {
                "records": [{"path": "frozen.json", "sha256": "0" * 64}],
                "supporting_artifacts": [],
            }
            codes = {
                item["code"]
                for item in manifest_integrity_errors(
                    manifest, root, allow_w6_mutable_support_drift=True
                )
            }
            self.assertIn("W4_MANIFEST_HASH_MISMATCH", codes)

    def test_arbitrary_support_hash_drift_remains_rejected_after_w6(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "arbitrary.txt"
            path.write_text("mutated\n", encoding="utf-8")
            manifest = {
                "records": [],
                "supporting_artifacts": [
                    {"path": "arbitrary.txt", "sha256": "0" * 64}
                ],
            }
            codes = {
                item["code"]
                for item in manifest_integrity_errors(
                    manifest, root, allow_w6_mutable_support_drift=True
                )
            }
            self.assertIn("W4_MANIFEST_HASH_MISMATCH", codes)

    def test_allowlisted_support_drift_requires_terminal_w6(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "README.md"
            path.write_text("downstream governed state\n", encoding="utf-8")
            manifest = {
                "records": [],
                "supporting_artifacts": [
                    {"path": "README.md", "sha256": "0" * 64}
                ],
            }
            before_codes = {
                item["code"]
                for item in manifest_integrity_errors(
                    manifest, root, allow_w6_mutable_support_drift=False
                )
            }
            after_errors = manifest_integrity_errors(
                manifest, root, allow_w6_mutable_support_drift=True
            )
            self.assertIn("W4_MANIFEST_HASH_MISMATCH", before_codes)
            self.assertEqual(after_errors, [])

    def test_matching_support_hash_is_always_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "support.txt"
            path.write_text("frozen\n", encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest = {
                "records": [],
                "supporting_artifacts": [
                    {"path": "support.txt", "sha256": digest}
                ],
            }
            self.assertEqual(
                manifest_integrity_errors(
                    manifest, root, allow_w6_mutable_support_drift=False
                ),
                [],
            )

    def test_records_remain_exact_and_do_not_claim_w5_semantics(self) -> None:
        for path in RESULTS.glob("*.json"):
            if path.name == "manifest.json":
                continue
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(document["contract"]["mode"], "exact")
            self.assertNotIn("approximation", document["contract"])
            self.assertNotIn("minimal", document["report"]["evidence"]["notes"].lower())

    def test_w4_remains_complete_after_terminal_w6(self) -> None:
        program = load_json(
            ROOT
            / "theory"
            / "evaluation"
            / "post-closure-assurance-and-application-program-v1.0.json"
        )
        workstreams = {item["id"]: item for item in program["workstreams"]}
        self.assertEqual(workstreams["PCA-W4-DOMAIN-CONTRACTS"]["state"], "complete")
        self.assertEqual(workstreams["PCA-W5-APPROXIMATION-AND-COST"]["state"], "complete")
        self.assertEqual(workstreams["PCA-W6-EMPIRICAL-AUDIT-UTILITY"]["state"], "complete")
        self.assertEqual(program["status"], "complete_registered_workstreams")
        self.assertIsNone(program["next_action"]["workstream"])
        self.assertEqual(validate_program_progression(program), [])

    def test_w4_remains_complete_after_w5_progression(self) -> None:
        """Preserve the W5-era regression ID while checking the stronger W6 state."""
        self.test_w4_remains_complete_after_terminal_w6()

    def test_w4_is_complete_and_w5_is_next_in_machine_authority(self) -> None:
        """Stable regression ID retained while asserting the terminal W6 state."""
        self.test_w4_remains_complete_after_terminal_w6()


if __name__ == "__main__":
    unittest.main()
