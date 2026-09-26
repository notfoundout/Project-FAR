from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from mechanization.far_mechanization.contract_conformance import MANIFEST_PATH, run_manifest
from mechanization.far_mechanization.contract_v2 import SCHEMA_PATH, contract_sha256, validate_contract
from mechanization.far_mechanization.migrate_v1_to_v2 import migrate

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "far-ir-2.0"
LEGACY_SCHEMA = ROOT / "schemas" / "far-document.schema.json"
LEGACY_MINIMAL = ROOT / "conformance" / "far-ir-1.0" / "valid" / "minimal.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class FARContractV2Tests(unittest.TestCase):
    def test_schema_is_draft_2020_12_and_versioned_successor(self) -> None:
        schema = load(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        self.assertEqual(schema["properties"]["format_version"]["const"], "far-ir/2.0")
        legacy = load(LEGACY_SCHEMA)
        self.assertEqual(legacy["properties"]["format_version"]["const"], "far-ir/1.0")
        self.assertNotEqual(schema["$id"], legacy["$id"])

    def test_required_w3_contract_dimensions_are_schema_explicit(self) -> None:
        schema = load(SCHEMA_PATH)
        contract = schema["$defs"]["Contract"]
        required = set(contract["required"])
        self.assertTrue({
            "id", "contract_version", "mode", "source_domain", "required_behavior",
            "representation", "observation_contexts", "admitted_transformations",
            "interpretation_profile", "target_model_class", "frame"
        }.issubset(required))
        self.assertIn("approximation", contract["properties"])
        report = schema["$defs"]["Report"]
        self.assertTrue({"outcome", "evidence", "failure_report"}.issubset(report["required"]))
        self.assertIn("Unknown", schema["$defs"]["TypedOutcome"]["enum"])

    def test_registered_conformance_suite(self) -> None:
        results = run_manifest(MANIFEST_PATH)
        failures = [result for result in results if not result.passed]
        self.assertEqual(failures, [], failures)
        self.assertGreaterEqual(len(results), 4)

    def test_factorization_witness_is_recomputed(self) -> None:
        document = load(FIXTURES / "valid-factorization.json")
        self.assertTrue(validate_contract(document).success)
        broken = copy.deepcopy(document)
        broken["report"]["evidence"]["decoder_table"][1]["behavior_value"] = "even"
        codes = {d.code for d in validate_contract(broken).diagnostics}
        self.assertIn("FACTORIZATION_FAILURE", codes)

    def test_collision_witness_requires_same_representation_and_different_behavior(self) -> None:
        document = load(FIXTURES / "valid-collision.json")
        self.assertTrue(validate_contract(document).success)
        broken = copy.deepcopy(document)
        broken["contract"]["representation"]["table"][1]["value"] = "different"
        broken["freeze"]["contract_sha256"] = contract_sha256(broken["contract"])
        codes = {d.code for d in validate_contract(broken).diagnostics}
        self.assertIn("COLLISION_REPRESENTATION_DIFFERS", codes)

    def test_exact_quotient_is_beta_kernel_not_merely_a_partition(self) -> None:
        document = load(FIXTURES / "valid-quotient.json")
        self.assertTrue(validate_contract(document).success)
        broken = copy.deepcopy(document)
        broken["report"]["evidence"]["classes"] = [
            {"id": "class.left", "case_ids": ["case.a", "case.c"]},
            {"id": "class.right", "case_ids": ["case.b", "case.d"]},
        ]
        codes = {d.code for d in validate_contract(broken).diagnostics}
        self.assertIn("QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT", codes)
        self.assertIn("QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL", codes)

    def test_freeze_hash_binds_contract(self) -> None:
        document = load(FIXTURES / "valid-factorization.json")
        self.assertEqual(document["freeze"]["contract_sha256"], contract_sha256(document["contract"]))
        broken = copy.deepcopy(document)
        broken["contract"]["frame"]["description"] = "silently changed frame"
        codes = {d.code for d in validate_contract(broken).diagnostics}
        self.assertIn("FREEZE_HASH_MISMATCH", codes)

    def test_approximation_declarations_cannot_self_certify_w5(self) -> None:
        document = load(FIXTURES / "valid-factorization.json")
        document["contract"]["mode"] = "approximate"
        document["contract"]["approximation"] = {
            "status": "DECLARED_ONLY", "w5_semantics_established": False,
            "metric": "declared metric", "loss": None, "cost": None
        }
        document["freeze"]["contract_sha256"] = contract_sha256(document["contract"])
        codes = {d.code for d in validate_contract(document).diagnostics}
        self.assertIn("W5_SEMANTICS_NOT_ESTABLISHED", codes)

    def test_v1_migration_preserves_payload_and_marks_missing_semantics_unknown(self) -> None:
        legacy = load(LEGACY_MINIMAL)
        migrated = migrate(legacy, source_path="conformance/far-ir-1.0/valid/minimal.json", created_at="2026-08-29T20:00:00Z")
        self.assertTrue(validate_contract(migrated).success)
        self.assertEqual(migrated["legacy_document"], legacy)
        self.assertEqual(migrated["format_version"], "far-ir/2.0")
        self.assertEqual(migrated["contract"]["mode"], "Unknown")
        self.assertEqual(migrated["report"]["outcome"], "Unknown")
        self.assertEqual(migrated["report"]["evidence"]["kind"], "unknown")
        self.assertEqual(migrated["freeze"]["status"], "DRAFT")
        self.assertIsNone(migrated["freeze"]["contract_sha256"])

    def test_unknown_evidence_cannot_certify_non_unknown_outcome(self) -> None:
        legacy = load(LEGACY_MINIMAL)
        migrated = migrate(legacy, created_at="2026-08-29T20:00:00Z")
        migrated["report"]["outcome"] = "PROVED"
        codes = {d.code for d in validate_contract(migrated).diagnostics}
        self.assertIn("UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME", codes)


if __name__ == "__main__":
    unittest.main()
