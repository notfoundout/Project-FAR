import copy
import unittest

from far_build_backend import _entry_points
from mechanization.far_mechanization.intake_v1 import aggregate_manifest, freeze_manifest, new_manifest, sha256_json, sha256_text, validate_manifest

STAMP = "2026-09-12T12:00:00Z"


def term(id_, surface, interpretations, *, material=True):
    return {
        "id": id_, "surface": surface, "material": material,
        "interpretation_ids": interpretations,
        "materiality_basis": "RAW_INPUT" if material else "INFERENCE",
        "materiality_source_ids": [],
        "materiality_derivation": "The preserved input makes this result-relevant." if material else "No supported variation changes the bounded result.",
        "effect_if_misclassified": "A result-changing alternative could be omitted.",
    }


def provenance(b_interp):
    return [
        {"path": "/source_domain/kind", "basis": "ASSUMPTION", "source_ids": [], "interpretation_ids": [], "assumption_ids": ["asm.domain"], "derivation": "Bound by asm.domain."},
        {"path": "/source_domain/description", "basis": "ASSUMPTION", "source_ids": [], "interpretation_ids": [], "assumption_ids": ["asm.domain"], "derivation": "Bound by asm.domain."},
        {"path": "/required_behavior/description", "basis": "ASSUMPTION", "source_ids": [], "interpretation_ids": [], "assumption_ids": ["asm.behavior"], "derivation": "Bound by asm.behavior."},
        {"path": "/interpretation_profile/A", "basis": "INTERPRETATION", "source_ids": [], "interpretation_ids": ["ia.1"], "assumption_ids": [], "derivation": "Direct assignment."},
        {"path": "/interpretation_profile/R", "basis": "INTERPRETATION", "source_ids": [], "interpretation_ids": ["ir.1"], "assumption_ids": [], "derivation": "Direct assignment."},
        {"path": "/interpretation_profile/B", "basis": "INTERPRETATION", "source_ids": [], "interpretation_ids": [b_interp], "assumption_ids": [], "derivation": "Direct assignment."},
    ]


def manifest():
    m = new_manifest("Entity A bears relation R to category B.", "INTAKE-GENERIC-001")
    m["discovery"] = {
        "claim_parses": [{"id": "parse.a", "statement": "A R B", "term_ids": ["term.a", "term.r", "term.b"], "origin": "SURFACE", "derivation": None}],
        "claim_parse_exclusions": [],
        "terms": [term("term.a", "A", ["ia.1"]), term("term.r", "R", ["ir.1"]), term("term.b", "B", ["ib.1", "ib.2"])],
        "sources": [
            {"id": "src.1", "locator": "urn:example:1", "sha256": sha256_text("one"), "source_type": "PRIMARY", "retrieved_at": "2026-09-12T10:00:00Z", "scope": "A and R"},
            {"id": "src.2", "locator": "urn:example:2", "sha256": sha256_text("two"), "source_type": "REFERENCE", "retrieved_at": "2026-09-12T10:05:00Z", "scope": "B readings"},
        ],
        "interpretations": [
            {"id": "ia.1", "term_id": "term.a", "statement": "A1", "origin": "SOURCE_EXPLICIT", "source_ids": ["src.1"], "derivation": None, "scope": "bounded"},
            {"id": "ir.1", "term_id": "term.r", "statement": "R1", "origin": "SOURCE_EXPLICIT", "source_ids": ["src.1"], "derivation": None, "scope": "bounded"},
            {"id": "ib.1", "term_id": "term.b", "statement": "B1", "origin": "SOURCE_EXPLICIT", "source_ids": ["src.2"], "derivation": None, "scope": "bounded"},
            {"id": "ib.2", "term_id": "term.b", "statement": "B2", "origin": "SOURCE_SYNTHESIS", "source_ids": ["src.2"], "derivation": "Source synthesis.", "scope": "bounded"},
        ],
        "interpretation_exclusions": [], "compatibility_exclusions": [],
        "assumptions": [
            {"id": "asm.scope", "statement": "Bounded evidence universe.", "status": "EXPLICIT", "source_ids": [], "effect_if_false": "More interpretations may enter."},
            {"id": "asm.domain", "statement": "Bounded source domain.", "status": "EXPLICIT", "source_ids": [], "effect_if_false": "Domain changes."},
            {"id": "asm.behavior", "statement": "Evaluate A R B.", "status": "EXPLICIT", "source_ids": [], "effect_if_false": "Behavior changes."},
        ],
        "search_protocol": {
            "evidence_cutoff": "2026-09-12T11:00:00Z",
            "queries": [{"id": "q.1", "query": "A R B", "target": "parse and interpretations", "source_scope": "bounded registry", "term_ids": ["term.a", "term.r", "term.b"], "claim_parse_ids": ["parse.a"]}],
            "stopping_rule": "Stop after a registered pass yields no new material alternative.",
            "saturation_observations": [{"round": 1, "observed_at": "2026-09-12T10:30:00Z", "query_ids": ["q.1"], "source_ids": ["src.1", "src.2"], "new_claim_parse_ids": [], "new_material_interpretation_ids": []}],
            "limitations": ["Bounded search is not open-world completeness."],
        },
        "contract_candidates": [],
    }
    for n, b in (("1", "ib.1"), ("2", "ib.2")):
        c = {"source_domain": {"kind": "described", "description": "bounded"}, "required_behavior": {"description": "evaluate A R B"}, "interpretation_profile": {"A": "ia.1", "R": "ir.1", "B": b}}
        m["discovery"]["contract_candidates"].append({"id": f"contract.{n}", "claim_parse_id": "parse.a", "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": b}, "contract": c, "sha256": sha256_json(c), "parameter_provenance": provenance(b)})
    return m


def evaluated(outcomes=("PROVED", "PROVED"), unknown_assumption=False):
    m = manifest()
    if unknown_assumption:
        m["discovery"]["assumptions"][0]["status"] = "Unknown"
    m = freeze_manifest(m, frozen_at=STAMP)
    for c, outcome in zip(m["discovery"]["contract_candidates"], outcomes):
        row = {"contract_id": c["id"], "contract_sha256": c["sha256"], "freeze_sha256": m["freeze"]["freeze_sha256"], "outcome": outcome, "evaluated_at": "2026-09-12T12:01:00Z", "evidence_refs": [] if outcome == "Unknown" else ["evidence://bounded"]}
        if outcome == "Unknown": row["notes"] = "Insufficient evidence."
        m["evaluations"].append(row)
    return m


class IntakeV1Tests(unittest.TestCase):
    def has(self, errors, text):
        self.assertTrue(any(text in e for e in errors), (text, errors))

    def test_entrypoints(self):
        e = _entry_points(); self.assertIn("far-evidence =", e); self.assertIn("far-intake =", e)

    def test_draft_is_loss_explicit(self):
        m = new_manifest("raw", "INTAKE-001"); self.assertEqual(validate_manifest(m), []); self.assertEqual(m["discovery"]["interpretations"], [])

    def test_complete_manifest_is_ready(self):
        self.assertEqual(validate_manifest(manifest(), require_complete=True), [])

    def test_schema_fails_closed(self):
        for mutate in (lambda m: m.update({"unexpected": 1}), lambda m: m["discovery"].update({"terms": "bad"}), lambda m: m.update({"freeze": []})):
            m = manifest(); mutate(m); self.has(validate_manifest(m, require_complete=True), "SCHEMA_CONSTRAINT_VIOLATION")

    def test_interpretation_provenance_and_derivation(self):
        m = manifest(); m["discovery"]["interpretations"][0]["source_ids"] = []; self.has(validate_manifest(m, require_complete=True), "requires source provenance")
        m = manifest(); r = m["discovery"]["interpretations"][0]; r["origin"] = "INFERENCE"; r["source_ids"] = []; r["derivation"] = None; self.has(validate_manifest(m, require_complete=True), "requires explicit derivation")

    def test_materiality_is_auditable(self):
        m = manifest(); m["discovery"]["terms"][0]["materiality_derivation"] = None; self.has(validate_manifest(m, require_complete=True), "materiality requires explicit derivation")
        m = manifest(); t = m["discovery"]["terms"][0]; t["materiality_basis"] = "SOURCE"; t["materiality_source_ids"] = []; self.has(validate_manifest(m, require_complete=True), "materiality requires source provenance")

    def test_contract_parameter_provenance_is_complete(self):
        m = manifest(); m["discovery"]["contract_candidates"][0]["parameter_provenance"].pop(); self.has(validate_manifest(m, require_complete=True), "lacks parameter provenance")
        m = manifest(); m["discovery"]["contract_candidates"][0]["parameter_provenance"][-1]["interpretation_ids"] = ["ib.2"]; self.has(validate_manifest(m, require_complete=True), "outside candidate assignments")

    def test_silent_contract_pruning_is_rejected(self):
        m = manifest(); m["discovery"]["contract_candidates"].pop(); self.has(validate_manifest(m, require_complete=True), "omits 1 admissible")

    def test_exclusion_requires_auditable_basis(self):
        m = manifest(); m["discovery"]["contract_candidates"].pop(); m["discovery"]["compatibility_exclusions"].append({"claim_parse_id": "parse.a", "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": "ib.2"}, "reason": "x", "basis": "SOURCE", "source_ids": [], "derivation": None}); self.has(validate_manifest(m, require_complete=True), "SOURCE basis requires source provenance")

    def test_source_backed_exclusion_can_prune(self):
        m = manifest(); m["discovery"]["contract_candidates"].pop(); m["discovery"]["compatibility_exclusions"].append({"claim_parse_id": "parse.a", "assignments": {"term.a": "ia.1", "term.r": "ir.1", "term.b": "ib.2"}, "reason": "out of scope", "basis": "SOURCE", "source_ids": ["src.2"], "derivation": None}); self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_search_and_saturation_coverage(self):
        m = manifest(); m["discovery"]["search_protocol"]["queries"][0]["term_ids"].remove("term.b"); self.has(validate_manifest(m, require_complete=True), "material terms lack recorded search coverage")
        m = manifest(); m["discovery"]["search_protocol"]["saturation_observations"][0]["source_ids"] = ["src.1"]; self.has(validate_manifest(m, require_complete=True), "sources lack saturation provenance")

    def test_final_saturation_is_zero_new(self):
        m = manifest(); m["discovery"]["search_protocol"]["saturation_observations"][0]["new_material_interpretation_ids"] = ["ib.2"]; self.has(validate_manifest(m, require_complete=True), "final saturation observation")

    def test_discovery_chronology(self):
        m = manifest(); m["discovery"]["sources"][0]["retrieved_at"] = "2026-09-12T11:00:01Z"; self.has(validate_manifest(m, require_complete=True), "after evidence_cutoff")
        m = manifest(); m["discovery"]["search_protocol"]["saturation_observations"][0]["observed_at"] = "2026-09-12T10:02:00Z"; self.has(validate_manifest(m, require_complete=True), "predates source retrieval")

    def test_zero_material_parse_yields_singleton_candidate(self):
        m = manifest(); m["discovery"]["claim_parses"].append({"id": "parse.fixed", "statement": "fixed", "term_ids": ["term.fixed"], "origin": "INFERENCE", "derivation": "distinct parse"}); m["discovery"]["terms"].append(term("term.fixed", "fixed", [], material=False)); m["discovery"]["search_protocol"]["queries"].append({"id": "q.2", "query": "fixed", "target": "parse", "source_scope": "bounded", "term_ids": [], "claim_parse_ids": ["parse.fixed"]}); m["discovery"]["search_protocol"]["saturation_observations"][0]["query_ids"].append("q.2"); self.has(validate_manifest(m, require_complete=True), "omits 1 admissible")

    def test_freeze_binds_input_discovery_and_time(self):
        m = freeze_manifest(manifest(), frozen_at=STAMP); m["raw_input"]["text"] = "changed"; m["raw_input"]["sha256"] = sha256_text("changed"); self.assertIn("freeze intake_sha256 mismatch", validate_manifest(m))
        m = freeze_manifest(manifest(), frozen_at=STAMP); m["freeze"]["frozen_at"] = "2026-09-12T12:00:01Z"; self.assertIn("freeze freeze_sha256 mismatch", validate_manifest(m))

    def test_freeze_cannot_predate_discovery(self):
        with self.assertRaisesRegex(ValueError, "cannot predate evidence_cutoff"): freeze_manifest(manifest(), frozen_at="2026-09-12T10:59:59Z")

    def test_evaluation_binding_and_evidence(self):
        m = evaluated(); m["evaluations"][0]["contract_sha256"] = "0" * 64; self.has(validate_manifest(m), "contract hash mismatch")
        m = evaluated(); m["evaluations"][0]["freeze_sha256"] = "0" * 64; self.has(validate_manifest(m), "freeze hash mismatch")
        m = evaluated(); m["evaluations"][0]["evidence_refs"] = []; self.has(validate_manifest(m), "requires evidence_refs")

    def test_evaluation_before_freeze_and_before_time_are_rejected(self):
        m = manifest(); c = m["discovery"]["contract_candidates"][0]; m["evaluations"] = [{"contract_id": c["id"], "contract_sha256": c["sha256"], "freeze_sha256": "0" * 64, "outcome": "PROVED", "evaluated_at": STAMP, "evidence_refs": ["evidence://x"]}]; self.assertIn("evaluations are prohibited before freeze", validate_manifest(m))
        m = evaluated(); m["evaluations"][0]["evaluated_at"] = "2026-09-12T11:59:59Z"; self.has(validate_manifest(m), "predates freeze")

    def test_unknown_requires_note(self):
        m = evaluated(("Unknown", "Unknown")); del m["evaluations"][0]["notes"]; self.has(validate_manifest(m), "requires notes")

    def test_aggregation_is_mechanical_and_complete(self):
        for outcomes, expected in [(("PROVED", "PROVED"), "INVARIANTLY_PROVED"), (("REFUTED", "REFUTED"), "INVARIANTLY_REFUTED"), (("PROVED", "REFUTED"), "CONTRACT_SENSITIVE"), (("PROVED", "UNDERDETERMINED"), "UNDERDETERMINED")]: self.assertEqual(aggregate_manifest(evaluated(outcomes))["outcome"], expected)
        m = evaluated(); m["evaluations"].pop(); self.assertEqual(aggregate_manifest(m)["outcome"], "INCOMPLETE")

    def test_unknown_assumption_blocks_invariant_promotion(self):
        r = aggregate_manifest(evaluated(unknown_assumption=True)); self.assertEqual(r["outcome"], "UNDERDETERMINED"); self.assertEqual(r["unresolved_assumptions"], ["asm.scope"])

    def test_non_json_contract_fails_closed(self):
        m = manifest(); m["discovery"]["contract_candidates"][0]["contract"]["bad"] = {1, 2}; self.has(validate_manifest(m, require_complete=True), "not canonical-JSON serializable")

    def test_non_finite_contract_numbers_fail_closed(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                m = manifest()
                m["discovery"]["contract_candidates"][0]["contract"]["bad"] = value
                self.has(
                    validate_manifest(m, require_complete=True),
                    "not canonical-JSON serializable",
                )

    def test_freeze_does_not_mutate_input(self):
        m = manifest(); before = copy.deepcopy(m); freeze_manifest(m, frozen_at=STAMP); self.assertEqual(m, before)


if __name__ == "__main__": unittest.main()
