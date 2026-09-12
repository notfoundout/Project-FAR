import copy
import unittest

from mechanization.far_mechanization.intake_v1 import (
    aggregate_manifest,
    freeze_manifest,
    new_manifest,
    sha256_json,
    sha256_text,
    validate_manifest,
)


STAMP = "2026-09-12T12:00:00Z"


def complete_manifest():
    m = new_manifest("Entity A bears relation R to category B.", "INTAKE-GENERIC-001")
    m["discovery"] = {
        "claim_parses": [
            {
                "id": "parse.a",
                "statement": "A R B",
                "term_ids": ["term.a", "term.r", "term.b"],
                "origin": "SURFACE",
                "derivation": None,
            }
        ],
        "terms": [
            {"id": "term.a", "surface": "A", "material": True, "interpretation_ids": ["ia.1"]},
            {"id": "term.r", "surface": "R", "material": True, "interpretation_ids": ["ir.1"]},
            {"id": "term.b", "surface": "B", "material": True, "interpretation_ids": ["ib.1", "ib.2"]},
        ],
        "sources": [
            {
                "id": "src.1",
                "locator": "urn:example:source:1",
                "sha256": sha256_text("source one"),
                "source_type": "PRIMARY",
                "retrieved_at": "2026-09-12T10:00:00Z",
                "scope": "Defines A and R in the bounded example.",
            },
            {
                "id": "src.2",
                "locator": "urn:example:source:2",
                "sha256": sha256_text("source two"),
                "source_type": "REFERENCE",
                "retrieved_at": "2026-09-12T10:05:00Z",
                "scope": "Records two materially distinct readings of B.",
            },
        ],
        "interpretations": [
            {
                "id": "ia.1",
                "term_id": "term.a",
                "statement": "A under source-defined reading one.",
                "origin": "SOURCE_EXPLICIT",
                "source_ids": ["src.1"],
                "derivation": None,
                "scope": "bounded example",
            },
            {
                "id": "ir.1",
                "term_id": "term.r",
                "statement": "R under source-defined reading one.",
                "origin": "SOURCE_EXPLICIT",
                "source_ids": ["src.1"],
                "derivation": None,
                "scope": "bounded example",
            },
            {
                "id": "ib.1",
                "term_id": "term.b",
                "statement": "B under reading one.",
                "origin": "SOURCE_EXPLICIT",
                "source_ids": ["src.2"],
                "derivation": None,
                "scope": "bounded example",
            },
            {
                "id": "ib.2",
                "term_id": "term.b",
                "statement": "B under reading two.",
                "origin": "SOURCE_SYNTHESIS",
                "source_ids": ["src.2"],
                "derivation": "Combines two explicit clauses from src.2 without adding a new criterion.",
                "scope": "bounded example",
            },
        ],
        "interpretation_exclusions": [],
        "compatibility_exclusions": [],
        "assumptions": [
            {
                "id": "asm.scope",
                "statement": "The bounded source set is the evidence universe for this intake.",
                "status": "EXPLICIT",
                "source_ids": [],
                "effect_if_false": "Additional interpretations may enter the contract family.",
            }
        ],
        "search_protocol": {
            "evidence_cutoff": "2026-09-12T11:00:00Z",
            "queries": [
                {"id": "q.1", "query": "A R B", "target": "material interpretations", "source_scope": "bounded source registry"}
            ],
            "stopping_rule": "Stop when the registered search pass yields no new materially distinct supported interpretation.",
            "saturation_observations": [
                {"round": 1, "new_material_interpretation_ids": []}
            ],
            "limitations": ["Bounded source search does not establish open-world semantic completeness."],
        },
        "contract_candidates": [],
    }
    for suffix, b_interp in (("1", "ib.1"), ("2", "ib.2")):
        contract = {
            "source_domain": {"kind": "described", "description": "bounded example"},
            "required_behavior": {"description": "evaluate A R B"},
            "interpretation_profile": {"A": "ia.1", "R": "ir.1", "B": b_interp},
        }
        m["discovery"]["contract_candidates"].append(
            {
                "id": f"contract.{suffix}",
                "claim_parse_id": "parse.a",
                "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": b_interp},
                "contract": contract,
                "sha256": sha256_json(contract),
            }
        )
    return m


class IntakeV1Tests(unittest.TestCase):
    def test_init_preserves_raw_input_and_introduces_no_interpretation(self):
        m = new_manifest("raw proposition", "INTAKE-001")
        self.assertEqual(m["raw_input"]["sha256"], sha256_text("raw proposition"))
        self.assertEqual(m["discovery"]["interpretations"], [])
        self.assertEqual(m["freeze"]["status"], "DRAFT")

    def test_complete_manifest_is_freeze_ready(self):
        self.assertEqual(validate_manifest(complete_manifest(), require_complete=True), [])

    def test_source_derived_interpretation_requires_provenance(self):
        m = complete_manifest()
        m["discovery"]["interpretations"][0]["source_ids"] = []
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("requires source provenance" in error for error in errors))

    def test_inference_requires_derivation(self):
        m = complete_manifest()
        row = m["discovery"]["interpretations"][0]
        row["origin"] = "INFERENCE"
        row["source_ids"] = []
        row["derivation"] = None
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("requires explicit derivation" in error for error in errors))

    def test_silent_contract_pruning_is_rejected(self):
        m = complete_manifest()
        m["discovery"]["contract_candidates"].pop()
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("omits 1 admissible interpretation combination" in error for error in errors))

    def test_explicit_compatibility_exclusion_can_remove_combination(self):
        m = complete_manifest()
        m["discovery"]["contract_candidates"].pop()
        m["discovery"]["compatibility_exclusions"].append(
            {
                "claim_parse_id": "parse.a",
                "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": "ib.2"},
                "reason": "The source states that this combination is outside the bounded scope.",
                "source_ids": ["src.2"],
            }
        )
        self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_freeze_binds_all_discovery_inputs(self):
        frozen = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        self.assertEqual(frozen["freeze"]["status"], "FROZEN")
        self.assertEqual(frozen["freeze"]["intake_sha256"], sha256_json({"raw_input": frozen["raw_input"], "discovery": frozen["discovery"]}))
        frozen["discovery"]["terms"][0]["surface"] = "tampered"
        errors = validate_manifest(frozen)
        self.assertIn("freeze intake_sha256 mismatch", errors)

    def test_freeze_binds_raw_input_as_well_as_discovery(self):
        frozen = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        frozen["raw_input"]["text"] = "changed input"
        frozen["raw_input"]["sha256"] = sha256_text("changed input")
        errors = validate_manifest(frozen)
        self.assertIn("freeze intake_sha256 mismatch", errors)

    def test_evaluation_before_freeze_is_rejected(self):
        m = complete_manifest()
        c = m["discovery"]["contract_candidates"][0]
        m["evaluations"] = [
            {
                "contract_id": c["id"],
                "contract_sha256": c["sha256"],
                "outcome": "PROVED",
                "evaluated_at": STAMP,
                "evidence_refs": [],
            }
        ]
        errors = validate_manifest(m)
        self.assertIn("evaluations are prohibited before freeze", errors)

    def test_evaluation_is_hash_bound_and_post_freeze(self):
        m = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        c = m["discovery"]["contract_candidates"][0]
        m["evaluations"] = [
            {
                "contract_id": c["id"],
                "contract_sha256": "0" * 64,
                "outcome": "PROVED",
                "evaluated_at": "2026-09-12T11:59:59Z",
                "evidence_refs": [],
            }
        ]
        errors = validate_manifest(m)
        self.assertTrue(any("contract hash mismatch" in error for error in errors))
        self.assertTrue(any("predates freeze" in error for error in errors))

    def _evaluated(self, outcomes):
        m = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        m["evaluations"] = []
        for candidate, outcome in zip(m["discovery"]["contract_candidates"], outcomes):
            m["evaluations"].append(
                {
                    "contract_id": candidate["id"],
                    "contract_sha256": candidate["sha256"],
                    "outcome": outcome,
                    "evaluated_at": "2026-09-12T12:01:00Z",
                    "evidence_refs": [],
                }
            )
        return m

    def test_aggregation_is_mechanical(self):
        self.assertEqual(aggregate_manifest(self._evaluated(["PROVED", "PROVED"]))["outcome"], "INVARIANTLY_PROVED")
        self.assertEqual(aggregate_manifest(self._evaluated(["REFUTED", "REFUTED"]))["outcome"], "INVARIANTLY_REFUTED")
        self.assertEqual(aggregate_manifest(self._evaluated(["PROVED", "REFUTED"]))["outcome"], "CONTRACT_SENSITIVE")
        self.assertEqual(aggregate_manifest(self._evaluated(["PROVED", "UNDERDETERMINED"]))["outcome"], "UNDERDETERMINED")

    def test_aggregation_requires_every_frozen_contract(self):
        m = self._evaluated(["PROVED", "REFUTED"])
        m["evaluations"].pop()
        result = aggregate_manifest(m)
        self.assertEqual(result["outcome"], "INCOMPLETE")
        self.assertTrue(result["errors"])

    def test_source_after_evidence_cutoff_is_rejected(self):
        m = complete_manifest()
        m["discovery"]["sources"][0]["retrieved_at"] = "2026-09-12T11:00:01Z"
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("retrieved after evidence_cutoff" in error for error in errors))

    def test_unreferenced_material_term_is_rejected_at_freeze(self):
        m = complete_manifest()
        m["discovery"]["terms"].append(
            {"id": "term.extra", "surface": "extra", "material": True, "interpretation_ids": ["iextra.1"]}
        )
        m["discovery"]["interpretations"].append(
            {
                "id": "iextra.1",
                "term_id": "term.extra",
                "statement": "Extra material reading.",
                "origin": "SOURCE_EXPLICIT",
                "source_ids": ["src.1"],
                "derivation": None,
                "scope": "bounded example",
            }
        )
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("is not referenced by any claim parse" in error for error in errors))

    def test_compatibility_exclusion_must_use_valid_complete_assignments(self):
        m = complete_manifest()
        m["discovery"]["compatibility_exclusions"].append(
            {
                "claim_parse_id": "parse.a",
                "assignments": {"term.b": "ib.2"},
                "reason": "Incomplete exclusion must not prune a combination.",
                "source_ids": ["src.2"],
            }
        )
        errors = validate_manifest(m, require_complete=True)
        self.assertTrue(any("assignments must exactly cover material terms" in error for error in errors))

    def test_original_object_is_not_mutated_by_freeze(self):
        m = complete_manifest()
        before = copy.deepcopy(m)
        freeze_manifest(m, frozen_at=STAMP)
        self.assertEqual(m, before)


if __name__ == "__main__":
    unittest.main()
