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
    "SF001-SF": "REPRESENTABLE_NO_CHANGE",
    "SF001-PRO": "SPECIFICATION_REPAIR",
    "SF001-CRV": "REPRESENTABLE_NO_CHANGE",
    "SF001-LEAN": "SPECIFICATION_REPAIR",
}
EXPECTED_RULES = {f"SF001-R{i}" for i in range(1, 6)}
EXPECTED_ARXIV = {
    "SF001-HS": "ARXIV-2609.32495v1",
    "SF001-SC": "ARXIV-2609.30383v1",
    "SF001-VA": "ARXIV-2609.31937v1",
    "SF001-SF": "ARXIV-2609.31422v1",
    "SF001-PRO": "ARXIV-2607.09996v1",
    "SF001-CRV": "ARXIV-2609.32924v1",
}
RULE_SEMANTIC_ANCHORS = {
    "SF001-R1": ("outside the audited actor's unilateral control", "independent corroboration"),
    "SF001-R2": ("consequential composition", "Component-level passes cannot be promoted into a composition-level pass"),
    "SF001-R3": ("does not redefine FARA's term", "authoritative or reliance-bearing state", "successful validation event"),
    "SF001-R4": ("`detected_at` and `origin_attributed_to` are distinct", "evidence or intervention"),
    "SF001-R5": ("known material checker/toolchain limitation", "does not by itself establish"),
}


def baseline_accepts(row: dict[str, object]) -> bool:
    finding = row["finding_id"]
    facts = row["facts"]
    assert isinstance(facts, dict)
    if finding == "SF001-SF":
        return not (bool(facts["strengthens_claim"]) or bool(facts["erases_disagreement"]) or bool(facts["drops_material_uncertainty_or_abstention"]))
    if finding == "SF001-CRV":
        return not (bool(facts["coverage_substituted_for_realization"]) or bool(facts["realization_substituted_for_validity"]))
    if finding == "SF001-LEAN":
        return bool(facts["checker_identity_version_retained"])
    if finding in {"SF001-HS", "SF001-SC", "SF001-VA", "SF001-PRO"}:
        return True
    raise AssertionError(f"unknown finding: {finding}")


def amended_accepts(row: dict[str, object]) -> bool:
    finding = row["finding_id"]
    facts = row["facts"]
    assert isinstance(facts, dict)
    if finding == "SF001-HS":
        return not (bool(facts["externally_observable_execution"]) and bool(facts["actor_controls_sole_record"]) and not bool(facts["independent_observation_or_corroboration"]))
    if finding == "SF001-SC":
        return not (bool(facts["consequential_composition"]) and not bool(facts["composition_assured"]))
    if finding == "SF001-VA":
        return not (bool(facts["consequential_proposal"]) and bool(facts["promoted_to_authoritative_state"]) and not bool(facts["required_validation_succeeded"]))
    if finding == "SF001-SF":
        return baseline_accepts(row)
    if finding == "SF001-PRO":
        return not (bool(facts["origin_claim_present"]) and not bool(facts["origin_evidence_or_intervention_present"]))
    if finding == "SF001-CRV":
        return baseline_accepts(row)
    if finding == "SF001-LEAN":
        if not bool(facts["checker_identity_version_retained"]):
            return False
        return not (bool(facts["known_material_limitation_relevant"]) and not bool(facts["limitation_retained"]))
    raise AssertionError(f"unknown finding: {finding}")


class SaturationFalsification001Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.findings = json.loads(FINDINGS.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.amendment = AMENDMENT.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")

    def test_campaign_identity_and_base_are_frozen(self) -> None:
        self.assertEqual(self.findings["campaign_id"], "SATURATION-FALSIFICATION-001")
        self.assertEqual(self.findings["base_sha"], "8618384efe4576580f65ff67b02b22bac43ffc51")
        self.assertEqual(self.findings["status"], "RESEARCH_PROVISIONAL")

    def test_disposition_vocabulary_is_exact(self) -> None:
        self.assertEqual(set(self.findings["allowed_dispositions"]), ALLOWED)
        self.assertLessEqual({item["disposition"] for item in self.findings["findings"]}, ALLOWED)

    def test_all_seven_findings_have_corrected_bounded_dispositions(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        self.assertEqual(set(rows), set(EXPECTED_FINDINGS))
        for finding_id, expected in EXPECTED_FINDINGS.items():
            self.assertEqual(rows[finding_id]["disposition"], expected)
            self.assertFalse(rows[finding_id]["new_capability_class"])
            self.assertTrue(rows[finding_id]["source_ids"])
            self.assertTrue(rows[finding_id]["counterexample"].strip())
            self.assertTrue(rows[finding_id]["minimal_repair"].strip())

    def test_only_five_findings_create_amendment_rules(self) -> None:
        rows = {item["id"]: item for item in self.findings["findings"]}
        observed = {row["amendment_rule"] for row in rows.values() if row["amendment_rule"]}
        self.assertEqual(observed, EXPECTED_RULES)
        self.assertIsNone(rows["SF001-SF"]["amendment_rule"])
        self.assertIsNone(rows["SF001-CRV"]["amendment_rule"])

    def test_no_new_capability_class_or_v06_is_promoted(self) -> None:
        conclusion = self.findings["campaign_conclusion"]
        self.assertFalse(conclusion["no_change_saturation_survives"])
        self.assertTrue(conclusion["capability_class_inventory_survives"])
        self.assertFalse(conclusion["v0_6_required"])
        self.assertFalse(conclusion["fara_core_status_change"])
        self.assertFalse(conclusion["efr_executed"])

    def test_amendment_contains_machine_bound_rule_semantics(self) -> None:
        for rule, anchors in RULE_SEMANTIC_ANCHORS.items():
            self.assertIn(rule, self.amendment)
            for anchor in anchors:
                self.assertIn(anchor, self.amendment, (rule, anchor))

    def test_amendment_does_not_redefine_fara_candidate_admission(self) -> None:
        self.assertIn('does not redefine FARA\'s term "admitted for consideration."', self.amendment)
        self.assertIn("authoritative or reliance-bearing state", self.amendment)

    def test_amendment_keeps_theory_and_empirical_boundaries_explicit(self) -> None:
        for phrase in ("does not change FAR-CORE", "FARA's governed theorem", "EFR status", "#518 status", "does not claim any FAR theorem was invalidated"):
            self.assertIn(phrase, self.amendment)

    def test_twenty_five_counterexample_and_control_fixtures_are_frozen(self) -> None:
        fixtures = self.fixtures["fixtures"]
        self.assertEqual(len(fixtures), 25)
        self.assertEqual(len({row["id"] for row in fixtures}), 25)
        self.assertEqual({row["finding_id"] for row in fixtures}, set(EXPECTED_FINDINGS))

    def test_structured_fixtures_match_executable_baseline_and_amended_semantics(self) -> None:
        for row in self.fixtures["fixtures"]:
            self.assertEqual(baseline_accepts(row), row["baseline_accepts"], row["id"])
            self.assertEqual(amended_accepts(row), row["amended_accepts"], row["id"])

    def test_representable_no_change_findings_are_already_rejected_by_baseline(self) -> None:
        for finding_id in ("SF001-SF", "SF001-CRV"):
            rows = [row for row in self.fixtures["fixtures"] if row["finding_id"] == finding_id]
            negatives = [row for row in rows if not row["amended_accepts"]]
            self.assertTrue(negatives, finding_id)
            for row in negatives:
                self.assertFalse(row["baseline_accepts"], row["id"])
                self.assertIsNone(row["rule"], row["id"])

    def test_actual_repairs_have_attack_and_control_coverage(self) -> None:
        by_rule: dict[str, list[dict[str, object]]] = {}
        for row in self.fixtures["fixtures"]:
            if row["rule"] is not None:
                by_rule.setdefault(row["rule"], []).append(row)
        self.assertEqual(set(by_rule), EXPECTED_RULES)
        for rule, rows in by_rule.items():
            self.assertTrue(any(r["baseline_accepts"] and not r["amended_accepts"] for r in rows), rule)
            self.assertTrue(any(r["amended_accepts"] for r in rows), rule)

    def test_lean_negative_case_is_known_limitation_disclosure_not_identity_version(self) -> None:
        row = next(item for item in self.fixtures["fixtures"] if item["id"] == "LEAN-01")
        facts = row["facts"]
        self.assertTrue(facts["checker_identity_version_retained"])
        self.assertTrue(facts["known_material_limitation_relevant"])
        self.assertFalse(facts["limitation_retained"])
        self.assertTrue(row["baseline_accepts"])
        self.assertFalse(row["amended_accepts"])

    def test_lean_finding_does_not_make_false_zero_match_or_invalidity_claim(self) -> None:
        row = next(item for item in self.findings["findings"] if item["id"] == "SF001-LEAN")
        scan = row["bounded_repo_scan"]
        self.assertNotIn("matches", scan)
        self.assertIn("No zero-match claim is made", scan["claim"])
        self.assertIn("does not demonstrate", row["evidence"])
        self.assertIn("not a proof of exploitability or non-exploitability", scan["interpretation"])

    def test_primary_sources_are_bound_to_exact_versions(self) -> None:
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

    def test_mutable_lean_sources_have_freeze_metadata(self) -> None:
        manifest = self.findings["source_manifest"]
        issue = manifest["LEAN-ISSUE-14576"]
        self.assertEqual(issue["issue_id"], 4994570410)
        self.assertEqual(issue["node_id"], "I_kwDOB7kabM8AAAABKbMYqg")
        self.assertEqual(issue["updated_at"], "2026-07-28T13:39:10Z")
        self.assertEqual(issue["retrieved_on"], "2026-09-29")
        self.assertEqual(manifest["LEAN-RELEASE-4.32.2"]["version"], "4.32.2")
        self.assertEqual(manifest["LEAN-POSTMORTEM-14576"]["published_on"], "2026-08-01")

    def test_reconstruction_boundary_is_not_hidden(self) -> None:
        self.assertIn("not a byte-for-byte recovery", self.readme)
        self.assertIn("unavailable", (CAMPAIGN / "replication.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
