from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "research" / "saturation-falsification-001"
FINDINGS = CAMPAIGN / "findings-v1.0.json"
FIXTURES = CAMPAIGN / "counterexamples-v1.0.json"
RECEIPTS = CAMPAIGN / "source-receipts-v1.0.json"
README = CAMPAIGN / "README.md"
BASELINE = ROOT / "docs" / "architecture" / "saturation-baseline-v0.5.md"
AMENDMENT = ROOT / "docs" / "architecture" / "saturation-baseline-v0.5-amendment-a1.md"

EXPECTED_FINDINGS = {
    "SF001-HS",
    "SF001-SC",
    "SF001-VA",
    "SF001-SF",
    "SF001-PRO",
    "SF001-CRV",
    "SF001-LEAN",
}
EXPECTED_ARXIV = {
    "SF001-HS": "ARXIV-2609.32495v1",
    "SF001-SC": "ARXIV-2609.30383v1",
    "SF001-VA": "ARXIV-2609.31937v1",
    "SF001-SF": "ARXIV-2609.31422v1",
    "SF001-PRO": "ARXIV-2607.09996v1",
    "SF001-CRV": "ARXIV-2609.32924v1",
}


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class SaturationFalsification001Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.findings = json.loads(FINDINGS.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.receipts = json.loads(RECEIPTS.read_text(encoding="utf-8"))
        cls.baseline_bytes = BASELINE.read_bytes()
        cls.baseline = cls.baseline_bytes.decode("utf-8")
        cls.amendment = AMENDMENT.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")

    def test_campaign_identity_and_frozen_base(self) -> None:
        self.assertEqual(self.findings["campaign_id"], "SATURATION-FALSIFICATION-001")
        self.assertEqual(self.findings["base_sha"], "8618384efe4576580f65ff67b02b22bac43ffc51")
        self.assertEqual(self.findings["baseline_blob_sha1"], "9d398e01f915e4f368dee44d35e9bd98de5b82ff")
        self.assertEqual(git_blob_sha1(self.baseline_bytes), self.findings["baseline_blob_sha1"])
        self.assertEqual(self.findings["status"], "RESEARCH_PROVISIONAL")

    def test_all_seven_findings_are_bounded_representable_no_change(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        self.assertEqual(set(rows), EXPECTED_FINDINGS)
        for finding_id, row in rows.items():
            self.assertEqual(row["disposition"], "REPRESENTABLE_NO_CHANGE", finding_id)
            self.assertIsNone(row["amendment_rule"], finding_id)
            self.assertFalse(row["new_capability_class"], finding_id)
            self.assertFalse(row["baseline_mapping"]["uses_opaque_metadata"], finding_id)
            self.assertTrue(row["baseline_mapping"]["representation_anchors"], finding_id)
            self.assertTrue(row["baseline_mapping"]["enforcement_anchors"], finding_id)

    def test_a1_is_withdrawn_nonoperative_and_contains_no_rules(self) -> None:
        self.assertIn("WITHDRAWN / NON-OPERATIVE", self.amendment)
        self.assertIn("has no operative rules", self.amendment)
        for index in range(1, 8):
            self.assertNotIn(f"SF001-R{index}", self.amendment)
        conclusion = self.findings["campaign_conclusion"]
        self.assertTrue(conclusion["bounded_no_change_saturation_survives"])
        self.assertEqual(conclusion["scope"], "these seven attacks against frozen v0.5 only")
        self.assertTrue(conclusion["capability_class_inventory_survives"])
        self.assertFalse(conclusion["amendment_required"])
        self.assertFalse(conclusion["v0_6_required"])
        self.assertFalse(conclusion["fara_core_status_change"])
        self.assertFalse(conclusion["efr_executed"])

    def test_every_mapping_anchor_literal_exists_in_frozen_baseline(self) -> None:
        for row in self.findings["findings"]:
            mapping = row["baseline_mapping"]
            for anchor in mapping["representation_anchors"] + mapping["enforcement_anchors"]:
                self.assertIn(anchor, self.baseline, (row["id"], anchor))

    def test_twenty_five_fixtures_are_bound_to_registered_baseline_anchors(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        fixtures = self.fixtures["fixtures"]
        self.assertEqual(len(fixtures), 25)
        self.assertEqual(len({row["id"] for row in fixtures}), 25)
        self.assertEqual({row["finding_id"] for row in fixtures}, EXPECTED_FINDINGS)
        for fixture in fixtures:
            self.assertTrue(fixture["baseline_handles"], fixture["id"])
            self.assertEqual(fixture["expected_disposition"], "REPRESENTABLE_NO_CHANGE")
            allowed = set(rows[fixture["finding_id"]]["baseline_mapping"]["representation_anchors"])
            allowed |= set(rows[fixture["finding_id"]]["baseline_mapping"]["enforcement_anchors"])
            self.assertLessEqual(set(fixture["required_baseline_anchors"]), allowed, fixture["id"])
            for anchor in fixture["required_baseline_anchors"]:
                self.assertIn(anchor, self.baseline, (fixture["id"], anchor))

    def test_primary_papers_are_bound_to_exact_arxiv_versions(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        manifest = self.findings["source_manifest"]
        for finding_id, source_id in EXPECTED_ARXIV.items():
            self.assertEqual(rows[finding_id]["source_ids"], [source_id])
            source = manifest[source_id]
            self.assertEqual(source["version"], "v1")
            self.assertTrue(source["version_url"].endswith("v1"))
            self.assertTrue(source["title"])
            self.assertTrue(source["authors"])
            self.assertTrue(source["submitted_at"].endswith("Z"))
            self.assertEqual(source["retrieved_on"], "2026-09-29")

    def test_mutable_lean_sources_are_bound_to_content_receipts(self) -> None:
        manifest = self.findings["source_manifest"]
        receipts = {item["id"]: item for item in self.receipts["receipts"]}
        for source_id in ("LEAN-ISSUE-14576", "LEAN-RELEASE-4.32.2", "LEAN-POSTMORTEM-14576"):
            receipt_id = manifest[source_id]["content_receipt_id"]
            self.assertIn(receipt_id, receipts)
            receipt = receipts[receipt_id]
            self.assertEqual(receipt["source_id"], source_id)
            digest = hashlib.sha256(receipt["excerpt"].encode("utf-8")).hexdigest()
            self.assertEqual(digest, receipt["excerpt_sha256"])

    def test_lean_boundary_does_not_reintroduce_zero_match_or_invalidity_claim(self) -> None:
        row = next(item for item in self.findings["findings"] if item["id"] == "SF001-LEAN")
        combined = json.dumps(row, sort_keys=True) + self.readme + (CAMPAIGN / "replication.md").read_text(encoding="utf-8")
        self.assertNotIn('"matches": 0', combined)
        self.assertIn("does not establish that any governed FAR proof", combined)

    def test_reconstruction_and_global_saturation_nonclaims_remain_explicit(self) -> None:
        self.assertIn("not a byte-for-byte recovery", self.readme)
        self.assertIn("globally saturated", self.readme)
        self.assertIn("FARA primitive/minimality questions remain separate", self.readme)
        self.assertIn("EFR and #518 remain unexecuted", self.readme)


if __name__ == "__main__":
    unittest.main()
