from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "research" / "saturation-falsification-001"
FINDINGS = CAMPAIGN / "findings-v1.0.json"
FIXTURES = CAMPAIGN / "counterexamples-v1.0.json"
README = CAMPAIGN / "README.md"
AMENDMENT = ROOT / "docs" / "architecture" / "saturation-baseline-v0.5-amendment-a1.md"

ALLOWED = {
    "REPRESENTABLE_NO_CHANGE",
    "SPECIFICATION_REPAIR",
    "ASSURANCE_BOUNDARY_CHANGE",
    "EXTENSION_INTERFACE_CHANGE",
    "NEW_CAPABILITY_CLASS_REQUIRED",
    "INDETERMINATE",
}
EXPECTED_FINDINGS = {
    "SF001-HS": "ASSURANCE_BOUNDARY_CHANGE",
    "SF001-SC": "ASSURANCE_BOUNDARY_CHANGE",
    "SF001-VA": "SPECIFICATION_REPAIR",
    "SF001-SF": "SPECIFICATION_REPAIR",
    "SF001-PRO": "SPECIFICATION_REPAIR",
    "SF001-CRV": "SPECIFICATION_REPAIR",
    "SF001-LEAN": "SPECIFICATION_REPAIR",
}
EXPECTED_RULES = {f"SF001-R{i}" for i in range(1, 8)}
EXPECTED_ARXIV = {
    "SF001-HS": "https://arxiv.org/abs/2609.32495",
    "SF001-SC": "https://arxiv.org/abs/2609.30383",
    "SF001-VA": "https://arxiv.org/abs/2609.31937",
    "SF001-SF": "https://arxiv.org/abs/2609.31422",
    "SF001-PRO": "https://arxiv.org/abs/2607.09996",
    "SF001-CRV": "https://arxiv.org/abs/2609.32924",
}


class SaturationFalsification001Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.findings = json.loads(FINDINGS.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.amendment = AMENDMENT.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")

    def test_campaign_identity_and_base_are_frozen(self) -> None:
        self.assertEqual(self.findings["campaign_id"], "SATURATION-FALSIFICATION-001")
        self.assertEqual(
            self.findings["base_sha"],
            "8618384efe4576580f65ff67b02b22bac43ffc51",
        )
        self.assertEqual(self.findings["status"], "RESEARCH_PROVISIONAL")

    def test_disposition_vocabulary_is_exact(self) -> None:
        self.assertEqual(set(self.findings["allowed_dispositions"]), ALLOWED)
        observed = {item["disposition"] for item in self.findings["findings"]}
        self.assertLessEqual(observed, ALLOWED)

    def test_all_seven_findings_have_exact_bounded_dispositions(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        self.assertEqual(set(rows), set(EXPECTED_FINDINGS))
        for finding_id, expected in EXPECTED_FINDINGS.items():
            self.assertEqual(rows[finding_id]["disposition"], expected)
            self.assertFalse(rows[finding_id]["new_capability_class"])
            self.assertTrue(rows[finding_id]["primary_sources"])
            self.assertTrue(rows[finding_id]["counterexample"].strip())
            self.assertTrue(rows[finding_id]["minimal_repair"].strip())

    def test_no_new_capability_class_or_v06_is_promoted(self) -> None:
        conclusion = self.findings["campaign_conclusion"]
        self.assertFalse(conclusion["no_change_saturation_survives"])
        self.assertTrue(conclusion["capability_class_inventory_survives"])
        self.assertFalse(conclusion["v0_6_required"])
        self.assertFalse(conclusion["fara_core_status_change"])
        self.assertFalse(conclusion["efr_executed"])
        self.assertNotIn("`NEW_CAPABILITY_CLASS_REQUIRED` |", self.readme)

    def test_amendment_contains_every_rule_as_a_literal_anchor(self) -> None:
        for rule in sorted(EXPECTED_RULES):
            self.assertEqual(self.amendment.count(rule), 2, rule)

    def test_amendment_keeps_theory_and_empirical_boundaries_explicit(self) -> None:
        required = (
            "does not change FAR-CORE",
            "FARA's governed theorem",
            "EFR status",
            "#518 status",
            "does not claim any FAR theorem was invalidated",
        )
        for phrase in required:
            self.assertIn(phrase, self.amendment)

    def test_twenty_five_counterexample_and_control_fixtures_are_frozen(self) -> None:
        fixtures = self.fixtures["fixtures"]
        self.assertEqual(len(fixtures), 25)
        self.assertEqual(len({row["id"] for row in fixtures}), 25)
        self.assertEqual({row["rule"] for row in fixtures}, EXPECTED_RULES)

    def test_amendment_closes_every_negative_fixture(self) -> None:
        negatives = [row for row in self.fixtures["fixtures"] if not row["amended_accepts"]]
        self.assertGreater(len(negatives), 0)
        for row in negatives:
            self.assertTrue(row["old_accepts"], row["id"])
            self.assertIn(row["rule"], self.amendment)
            self.assertTrue(row["reason"].strip())

    def test_controls_remain_accepted(self) -> None:
        controls = [row for row in self.fixtures["fixtures"] if row["amended_accepts"]]
        self.assertGreater(len(controls), 0)
        for row in controls:
            self.assertTrue(row["old_accepts"], row["id"])

    def test_each_rule_has_both_attack_or_control_coverage(self) -> None:
        by_rule: dict[str, list[dict[str, object]]] = {}
        for row in self.fixtures["fixtures"]:
            by_rule.setdefault(row["rule"], []).append(row)
        self.assertEqual(set(by_rule), EXPECTED_RULES)
        for rule, rows in by_rule.items():
            self.assertTrue(any(not row["amended_accepts"] for row in rows), rule)
            self.assertTrue(any(row["amended_accepts"] for row in rows), rule)

    def test_lean_finding_does_not_launder_version_risk_into_invalidity(self) -> None:
        row = next(item for item in self.findings["findings"] if item["id"] == "SF001-LEAN")
        evidence = row["evidence"]
        self.assertIn("does not demonstrate", evidence)
        self.assertIn("not proof of non-exploitability", row["bounded_repo_scan"]["interpretation"])
        self.assertEqual(row["bounded_repo_scan"]["matches"], 0)
        self.assertEqual(row["bounded_repo_scan"]["queries"], ["Lean.Meta", "run_tac", "unsafe"])

    def test_primary_sources_are_bound_to_expected_identifiers(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        for finding_id, source in EXPECTED_ARXIV.items():
            self.assertEqual(rows[finding_id]["primary_sources"], [source])
        lean_sources = rows["SF001-LEAN"]["primary_sources"]
        self.assertTrue(any("github.com/leanprover/lean4/issues/14576" in source for source in lean_sources))
        self.assertTrue(any("leodemoura.github.io" in source for source in lean_sources))

    def test_reconstruction_boundary_is_not_hidden(self) -> None:
        self.assertIn("not a byte-for-byte recovery", self.readme)
        self.assertIn("unavailable", (CAMPAIGN / "replication.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
