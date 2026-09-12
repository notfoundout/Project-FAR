import copy
import unittest

from far_build_backend import _entry_points
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
        "claim_parses": [{
            "id": "parse.a", "statement": "A R B",
            "term_ids": ["term.a", "term.r", "term.b"],
            "origin": "SURFACE", "derivation": None,
        }],
        "claim_parse_exclusions": [],
        "terms": [
            {"id": "term.a", "surface": "A", "material": True, "interpretation_ids": ["ia.1"]},
            {"id": "term.r", "surface": "R", "material": True, "interpretation_ids": ["ir.1"]},
            {"id": "term.b", "surface": "B", "material": True, "interpretation_ids": ["ib.1", "ib.2"]},
        ],
        "sources": [
            {"id": "src.1", "locator": "urn:example:source:1", "sha256": sha256_text("source one"),
             "source_type": "PRIMARY", "retrieved_at": "2026-09-12T10:00:00Z", "scope": "Defines A and R."},
            {"id": "src.2", "locator": "urn:example:source:2", "sha256": sha256_text("source two"),
             "source_type": "REFERENCE", "retrieved_at": "2026-09-12T10:05:00Z", "scope": "Defines two readings of B."},
        ],
        "interpretations": [
            {"id": "ia.1", "term_id": "term.a", "statement": "A reading one.", "origin": "SOURCE_EXPLICIT",
             "source_ids": ["src.1"], "derivation": None, "scope": "bounded example"},
            {"id": "ir.1", "term_id": "term.r", "statement": "R reading one.", "origin": "SOURCE_EXPLICIT",
             "source_ids": ["src.1"], "derivation": None, "scope": "bounded example"},
            {"id": "ib.1", "term_id": "term.b", "statement": "B reading one.", "origin": "SOURCE_EXPLICIT",
             "source_ids": ["src.2"], "derivation": None, "scope": "bounded example"},
            {"id": "ib.2", "term_id": "term.b", "statement": "B reading two.", "origin": "SOURCE_SYNTHESIS",
             "source_ids": ["src.2"], "derivation": "Combines source clauses without a new criterion.", "scope": "bounded example"},
        ],
        "interpretation_exclusions": [],
        "compatibility_exclusions": [],
        "assumptions": [{
            "id": "asm.scope", "statement": "The bounded source set is the evidence universe.",
            "status": "EXPLICIT", "source_ids": [],
            "effect_if_false": "Additional interpretations may enter the family.",
        }],
        "search_protocol": {
            "evidence_cutoff": "2026-09-12T11:00:00Z",
            "queries": [{
                "id": "q.1", "query": "A R B", "target": "material interpretations and parse coverage",
                "source_scope": "bounded source registry", "term_ids": ["term.a", "term.r", "term.b"],
                "claim_parse_ids": ["parse.a"],
            }],
            "stopping_rule": "Stop after a registered pass yields no new material parse or interpretation.",
            "saturation_observations": [{
                "round": 1, "observed_at": "2026-09-12T10:30:00Z", "query_ids": ["q.1"],
                "source_ids": ["src.1", "src.2"], "new_claim_parse_ids": [],
                "new_material_interpretation_ids": [],
            }],
            "limitations": ["Bounded search does not establish open-world semantic completeness."],
        },
        "contract_candidates": [],
    }
    for suffix, b_interp in (("1", "ib.1"), ("2", "ib.2")):
        contract = {
            "source_domain": {"kind": "described", "description": "bounded example"},
            "required_behavior": {"description": "evaluate A R B"},
            "interpretation_profile": {"A": "ia.1", "R": "ir.1", "B": b_interp},
        }
        m["discovery"]["contract_candidates"].append({
            "id": f"contract.{suffix}", "claim_parse_id": "parse.a",
            "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": b_interp},
            "contract": contract, "sha256": sha256_json(contract),
        })
    return m


def evaluated(outcomes=("PROVED", "PROVED"), *, unknown_assumption=False):
    m = complete_manifest()
    if unknown_assumption:
        m["discovery"]["assumptions"][0]["status"] = "Unknown"
    m = freeze_manifest(m, frozen_at=STAMP)
    for candidate, outcome in zip(m["discovery"]["contract_candidates"], outcomes):
        row = {
            "contract_id": candidate["id"], "contract_sha256": candidate["sha256"],
            "freeze_sha256": m["freeze"]["freeze_sha256"], "outcome": outcome,
            "evaluated_at": "2026-09-12T12:01:00Z",
            "evidence_refs": [] if outcome == "Unknown" else [f"evidence://{candidate['id']}"],
        }
        if outcome == "Unknown":
            row["notes"] = "Evidence is insufficient for a determinate outcome."
        m["evaluations"].append(row)
    return m


def add_zero_material_parse(m):
    m["discovery"]["claim_parses"].append({
        "id": "parse.fixed", "statement": "fixed reading", "term_ids": ["term.fixed"],
        "origin": "INFERENCE", "derivation": "A distinct parse whose only term has no outcome-changing alternatives.",
    })
    m["discovery"]["terms"].append(
        {"id": "term.fixed", "surface": "fixed", "material": False, "interpretation_ids": []}
    )
    m["discovery"]["search_protocol"]["queries"].append({
        "id": "q.2", "query": "fixed reading", "target": "claim parse completeness",
        "source_scope": "bounded source registry", "term_ids": [], "claim_parse_ids": ["parse.fixed"],
    })
    m["discovery"]["search_protocol"]["saturation_observations"][0]["query_ids"].append("q.2")


class IntakeV1Tests(unittest.TestCase):
    def assertHas(self, errors, text):
        self.assertTrue(any(text in error for error in errors), (text, errors))

    def test_entrypoints_match_project_scripts(self):
        text = _entry_points()
        self.assertIn("far-evidence = mechanization.far_mechanization.compare_adjudication:main", text)
        self.assertIn("far-intake = mechanization.far_mechanization.intake_v1:main", text)

    def test_draft_is_loss_explicit_and_valid(self):
        m = new_manifest("raw proposition", "INTAKE-001")
        self.assertEqual(m["raw_input"]["sha256"], sha256_text("raw proposition"))
        self.assertEqual(m["discovery"]["claim_parses"], [])
        self.assertEqual(m["discovery"]["interpretations"], [])
        self.assertEqual(validate_manifest(m), [])

    def test_complete_manifest_is_freeze_ready(self):
        self.assertEqual(validate_manifest(complete_manifest(), require_complete=True), [])

    def test_schema_precedes_semantics(self):
        mutations = []
        a = complete_manifest(); a["unexpected"] = True; mutations.append(a)
        b = complete_manifest(); del b["discovery"]["claim_parses"][0]["derivation"]; mutations.append(b)
        c = complete_manifest(); c["discovery"]["terms"] = "bad"; mutations.append(c)
        for manifest in mutations:
            with self.subTest(manifest=manifest):
                self.assertHas(validate_manifest(manifest, require_complete=True), "SCHEMA_CONSTRAINT_VIOLATION")

    def test_source_interpretation_requires_provenance(self):
        m = complete_manifest(); m["discovery"]["interpretations"][0]["source_ids"] = []
        self.assertHas(validate_manifest(m, require_complete=True), "requires source provenance")

    def test_synthesis_and_inference_require_derivation(self):
        for origin in ("SOURCE_SYNTHESIS", "INFERENCE"):
            m = complete_manifest(); row = m["discovery"]["interpretations"][0]
            row["origin"] = origin; row["derivation"] = None
            if origin == "INFERENCE": row["source_ids"] = []
            with self.subTest(origin=origin):
                self.assertHas(validate_manifest(m, require_complete=True), "requires explicit derivation")

    def test_silent_contract_pruning_is_rejected(self):
        m = complete_manifest(); m["discovery"]["contract_candidates"].pop()
        self.assertHas(validate_manifest(m, require_complete=True), "omits 1 admissible interpretation combination")

    def test_exclusion_requires_auditable_basis(self):
        for table, row in (
            ("interpretation_exclusions", {
                "interpretation_id": "ib.2", "reason_code": "UNSUPPORTED", "reason": "x",
                "basis": "SOURCE", "source_ids": [], "derivation": None,
            }),
            ("compatibility_exclusions", {
                "claim_parse_id": "parse.a", "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": "ib.2"},
                "reason": "x", "basis": "SOURCE", "source_ids": [], "derivation": None,
            }),
        ):
            m = complete_manifest(); m["discovery"][table].append(row)
            if table == "compatibility_exclusions": m["discovery"]["contract_candidates"].pop()
            with self.subTest(table=table):
                self.assertHas(validate_manifest(m, require_complete=True), "SOURCE basis requires source provenance")

    def test_inference_based_exclusion_requires_derivation(self):
        m = complete_manifest(); m["discovery"]["interpretation_exclusions"].append({
            "interpretation_id": "ib.2", "reason_code": "OTHER", "reason": "inferred exclusion",
            "basis": "INFERENCE", "source_ids": [], "derivation": None,
        })
        self.assertHas(validate_manifest(m, require_complete=True), "INFERENCE basis requires explicit derivation")

    def test_source_backed_compatibility_exclusion_can_prune(self):
        m = complete_manifest(); m["discovery"]["contract_candidates"].pop()
        m["discovery"]["compatibility_exclusions"].append({
            "claim_parse_id": "parse.a", "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": "ib.2"},
            "reason": "Source places this combination outside scope.", "basis": "SOURCE",
            "source_ids": ["src.2"], "derivation": None,
        })
        self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_parse_exclusion_is_explicit_and_covered(self):
        m = complete_manifest(); add_zero_material_parse(m)
        m["discovery"]["claim_parse_exclusions"].append({
            "claim_parse_id": "parse.fixed", "reason_code": "WRONG_DOMAIN", "reason": "Raw input excludes this parse.",
            "basis": "RAW_INPUT", "source_ids": [], "derivation": "The retained raw qualifier rules out this parse.",
        })
        self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_all_parses_cannot_be_excluded(self):
        m = complete_manifest(); m["discovery"]["claim_parse_exclusions"].append({
            "claim_parse_id": "parse.a", "reason_code": "OTHER", "reason": "remove all",
            "basis": "INFERENCE", "source_ids": [], "derivation": "test exclusion",
        })
        self.assertHas(validate_manifest(m, require_complete=True), "at least one active claim parse")

    def test_zero_material_parse_requires_singleton_contract(self):
        m = complete_manifest(); add_zero_material_parse(m)
        self.assertHas(validate_manifest(m, require_complete=True), "omits 1 admissible interpretation combination")
        contract = {"source_domain": {"kind": "described", "description": "fixed parse"}}
        m["discovery"]["contract_candidates"].append({
            "id": "contract.fixed", "claim_parse_id": "parse.fixed", "assignments": {},
            "contract": contract, "sha256": sha256_json(contract),
        })
        self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_material_term_requires_active_interpretation(self):
        m = complete_manifest(); m["discovery"]["interpretation_exclusions"].append({
            "interpretation_id": "ia.1", "reason_code": "UNSUPPORTED", "reason": "source-backed exclusion",
            "basis": "SOURCE", "source_ids": ["src.1"], "derivation": None,
        })
        self.assertHas(validate_manifest(m, require_complete=True), "has no active interpretation")

    def test_search_must_cover_active_parses_and_material_terms(self):
        a = complete_manifest(); a["discovery"]["search_protocol"]["queries"][0]["term_ids"].remove("term.b")
        self.assertHas(validate_manifest(a, require_complete=True), "active material terms lack recorded search coverage")
        b = complete_manifest(); b["discovery"]["search_protocol"]["queries"][0]["claim_parse_ids"] = []
        self.assertHas(validate_manifest(b, require_complete=True), "active claim parses lack recorded search coverage")

    def test_query_target_must_be_material_or_parse(self):
        m = complete_manifest(); m["discovery"]["search_protocol"]["queries"][0]["term_ids"] = []
        m["discovery"]["search_protocol"]["queries"][0]["claim_parse_ids"] = []
        self.assertHas(validate_manifest(m, require_complete=True), "must target at least one term or claim parse")

    def test_registered_queries_and_sources_need_saturation_provenance(self):
        a = complete_manifest(); a["discovery"]["search_protocol"]["saturation_observations"][0]["query_ids"] = []
        self.assertHas(validate_manifest(a, require_complete=True), "SCHEMA_CONSTRAINT_VIOLATION")
        b = complete_manifest(); b["discovery"]["search_protocol"]["saturation_observations"][0]["source_ids"] = ["src.1"]
        self.assertHas(validate_manifest(b, require_complete=True), "registered sources lack saturation provenance")

    def test_final_saturation_round_must_be_zero_new(self):
        m = complete_manifest(); m["discovery"]["search_protocol"]["saturation_observations"][0]["new_material_interpretation_ids"] = ["ib.2"]
        self.assertHas(validate_manifest(m, require_complete=True), "final saturation observation with no new")

    def test_saturation_rounds_are_ordered_unique(self):
        m = complete_manifest(); first = copy.deepcopy(m["discovery"]["search_protocol"]["saturation_observations"][0])
        m["discovery"]["search_protocol"]["saturation_observations"] = [first, copy.deepcopy(first)]
        self.assertHas(validate_manifest(m, require_complete=True), "unique and strictly increasing")

    def test_discovery_chronology_is_enforced(self):
        a = complete_manifest(); a["discovery"]["sources"][0]["retrieved_at"] = "2026-09-12T11:00:01Z"
        self.assertHas(validate_manifest(a, require_complete=True), "retrieved after evidence_cutoff")
        b = complete_manifest(); b["discovery"]["search_protocol"]["saturation_observations"][0]["observed_at"] = "2026-09-12T10:02:00Z"
        self.assertHas(validate_manifest(b, require_complete=True), "predates source retrieval src.2")
        c = complete_manifest(); c["discovery"]["search_protocol"]["saturation_observations"][0]["observed_at"] = "2026-09-12T11:00:01Z"
        self.assertHas(validate_manifest(c, require_complete=True), "occurred after evidence_cutoff")

    def test_freeze_cannot_predate_discovery(self):
        with self.assertRaisesRegex(ValueError, "cannot predate evidence_cutoff"):
            freeze_manifest(complete_manifest(), frozen_at="2026-09-12T10:59:59Z")

    def test_freeze_binds_raw_input_and_discovery(self):
        frozen = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        frozen["raw_input"]["text"] = "changed"; frozen["raw_input"]["sha256"] = sha256_text("changed")
        self.assertIn("freeze intake_sha256 mismatch", validate_manifest(frozen))
        frozen = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        frozen["discovery"]["terms"][0]["surface"] = "tampered"
        self.assertIn("freeze intake_sha256 mismatch", validate_manifest(frozen))

    def test_freeze_identity_binds_timestamp(self):
        frozen = freeze_manifest(complete_manifest(), frozen_at=STAMP)
        frozen["freeze"]["frozen_at"] = "2026-09-12T12:00:01Z"
        self.assertIn("freeze freeze_sha256 mismatch", validate_manifest(frozen))

    def test_evaluation_before_freeze_is_rejected(self):
        m = complete_manifest(); c = m["discovery"]["contract_candidates"][0]
        m["evaluations"] = [{
            "contract_id": c["id"], "contract_sha256": c["sha256"], "freeze_sha256": "0" * 64,
            "outcome": "PROVED", "evaluated_at": STAMP, "evidence_refs": ["evidence://pre-freeze"],
        }]
        self.assertIn("evaluations are prohibited before freeze", validate_manifest(m))

    def test_evaluation_binds_contract_and_freeze_hashes(self):
        m = evaluated(); m["evaluations"][0]["contract_sha256"] = "0" * 64
        self.assertHas(validate_manifest(m), "contract hash mismatch")
        m = evaluated(); m["evaluations"][0]["freeze_sha256"] = "0" * 64
        self.assertHas(validate_manifest(m), "freeze hash mismatch")

    def test_evaluation_chronology_and_evidence_are_enforced(self):
        a = evaluated(); a["evaluations"][0]["evaluated_at"] = "2026-09-12T11:59:59Z"
        self.assertHas(validate_manifest(a), "predates freeze")
        b = evaluated(); b["evaluations"][0]["evidence_refs"] = []
        self.assertHas(validate_manifest(b), "requires evidence_refs for non-Unknown outcome")

    def test_unknown_evaluation_requires_reason(self):
        m = evaluated(("Unknown", "Unknown")); del m["evaluations"][0]["notes"]
        self.assertHas(validate_manifest(m), "with Unknown outcome requires notes")

    def test_aggregation_is_fixed(self):
        cases = [
            (("PROVED", "PROVED"), "INVARIANTLY_PROVED"),
            (("REFUTED", "REFUTED"), "INVARIANTLY_REFUTED"),
            (("PROVED", "REFUTED"), "CONTRACT_SENSITIVE"),
            (("PROVED", "UNDERDETERMINED"), "UNDERDETERMINED"),
        ]
        for outcomes, expected in cases:
            with self.subTest(outcomes=outcomes):
                self.assertEqual(aggregate_manifest(evaluated(outcomes))["outcome"], expected)

    def test_aggregation_requires_every_candidate(self):
        m = evaluated(("PROVED", "REFUTED")); m["evaluations"].pop()
        self.assertEqual(aggregate_manifest(m)["outcome"], "INCOMPLETE")

    def test_unknown_assumption_blocks_invariant_promotion(self):
        result = aggregate_manifest(evaluated(unknown_assumption=True))
        self.assertEqual(result["outcome"], "UNDERDETERMINED")
        self.assertEqual(result["unresolved_assumptions"], ["asm.scope"])

    def test_non_json_contract_is_rejected_without_exception(self):
        m = complete_manifest(); m["discovery"]["contract_candidates"][0]["contract"]["bad"] = {1, 2}
        self.assertHas(validate_manifest(m, require_complete=True), "not canonical-JSON serializable")

    def test_freeze_does_not_mutate_input(self):
        m = complete_manifest(); before = copy.deepcopy(m); freeze_manifest(m, frozen_at=STAMP)
        self.assertEqual(m, before)

    def test_structural_mutations_fail_closed_without_exception(self):
        mutators = [
            lambda m: m.update({"discovery": None}),
            lambda m: m["discovery"].update({"sources": {}}),
            lambda m: m["discovery"].update({"claim_parses": [None]}),
            lambda m: m["discovery"].update({"search_protocol": []}),
            lambda m: m["discovery"]["search_protocol"].update({"queries": [None]}),
            lambda m: m["discovery"]["contract_candidates"][0].update({"assignments": []}),
            lambda m: m.update({"freeze": []}),
            lambda m: m.update({"evaluations": {}}),
        ]
        for mutate in mutators:
            m = complete_manifest(); mutate(m)
            with self.subTest(mutate=mutate):
                errors = validate_manifest(m, require_complete=True)
                self.assertTrue(errors)
                self.assertTrue(any("SCHEMA_CONSTRAINT_VIOLATION" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
