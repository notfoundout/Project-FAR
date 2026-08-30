from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from mechanization.far_mechanization.contract_v2 import contract_sha256
from tools.check_pca_w4_domain_contracts import RESULTS, audit_document, load_json, validate_campaign

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

    def test_records_remain_exact_and_do_not_claim_w5_semantics(self) -> None:
        for path in RESULTS.glob("*.json"):
            if path.name == "manifest.json":
                continue
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(document["contract"]["mode"], "exact")
            self.assertNotIn("approximation", document["contract"])
            self.assertNotIn("minimal", document["report"]["evidence"]["notes"].lower())

    def test_w4_is_complete_and_w5_is_next_in_machine_authority(self) -> None:
        program = load_json(
            ROOT
            / "theory"
            / "evaluation"
            / "post-closure-assurance-and-application-program-v1.0.json"
        )
        workstreams = {item["id"]: item for item in program["workstreams"]}
        self.assertEqual(workstreams["PCA-W4-DOMAIN-CONTRACTS"]["state"], "complete")
        self.assertEqual(program["next_action"]["workstream"], "PCA-W5-APPROXIMATION-AND-COST")


if __name__ == "__main__":
    unittest.main()
