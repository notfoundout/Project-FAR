from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json"
EXTENSION = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
ORIGINAL = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002/execution/cre002-comparison.json"
REQUIRED = {"D_nondeterminism", "D_concurrency", "D_priority", "D_provenance", "D_rule_modification"}


class VocabularySemanticsBaseline11Tests(unittest.TestCase):
    def test_regression_checker_passes(self) -> None:
        cp = subprocess.run([sys.executable, "tools/check_vocabulary_semantics_baseline_1_1.py"], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_five_missing_constructs_are_defined(self) -> None:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        constructs = {item["identifier"]: item for item in data["derived_constructs"]}
        self.assertEqual(set(constructs), REQUIRED)
        for item in constructs.values():
            self.assertEqual(item["classification"], "derived")
            self.assertTrue(item["required_fields"])
            self.assertTrue(item["operational_constraints"])
            self.assertTrue(item["forbidden_imports"])

    def test_all_vocabularies_have_explicit_bounded_licensing(self) -> None:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.assertEqual(len(data["vocabulary_licensing"]), 3)
        for record in data["vocabulary_licensing"].values():
            self.assertEqual(set(record["licensed_derived_constructs"]), REQUIRED)
            self.assertIn("finite", (record["construction_rule"] + " " + record["limitation"]).lower())

    def test_original_cre002_result_remains_unsupported(self) -> None:
        result = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.assertEqual(result["artifact_id"], "CRE-002-COMPARISON-1.0")
        self.assertEqual(result["aggregate"]["unsupported_candidates"], 3)
        self.assertEqual(result["aggregate"]["complete_candidates"], 0)
        self.assertTrue(all(row["outcome"] == "unsupported" for row in result["candidates"]))

    def test_extension_phase_is_valid(self) -> None:
        lock = json.loads((EXTENSION / "execution-lock.json").read_text(encoding="utf-8"))
        if lock["execution_permitted"]:
            audit = json.loads((EXTENSION / "execution-unlock-audit.json").read_text(encoding="utf-8"))
            self.assertTrue(lock["compiler_implementation_permitted"])
            self.assertEqual(lock["authorization_status"], "authorized")
            self.assertTrue(audit["immutable_package_lock_verified"])
            self.assertFalse(audit["scientific_results_created_by_unlock"])
            if lock["official_results_present"]:
                self.assertEqual(lock["status"], "execution-complete")
                self.assertTrue((EXTENSION / lock["official_result"]).is_file())
            else:
                self.assertEqual(lock["status"], "execution-authorized")
        else:
            self.assertFalse(lock["compiler_implementation_permitted"])
            self.assertFalse(lock["official_results_present"])

    def test_nonclaims_prevent_retroactive_validation(self) -> None:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        self.assertIn("retrospective validation of CRE-002", data["nonclaims"])
        self.assertFalse(data["scope"]["primitive_only_claim"])
        self.assertEqual(data["chronology"]["first_eligible_experiment"].split()[0], "CRE-002-EXT-001")


if __name__ == "__main__":
    unittest.main()
