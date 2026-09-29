"""One targeted mutation per rule of tools/check_far_core_v11_formalization.py."""
from __future__ import annotations

import copy
import unittest
from unittest import mock

from tools import check_far_core_v11_formalization as checker

LEDGER = checker.load(checker.LEDGER_PATH)
ASSURANCE = checker.load(checker.ASSURANCE_PATH)
CORE = checker.load(checker.CORE_PATH)
GENERATED = checker.inventory(LEDGER)


def by_id(data: dict, identifier: str) -> dict:
    return next(item for item in data["claims"] if item["id"] == identifier)


def valid_axiom_output() -> str:
    lines = []
    for declaration, axioms in sorted(checker.EXPECTED_DECLARATION_AXIOMS.items()):
        if axioms:
            lines.append(f"'{declaration}' depends on axioms: [{', '.join(sorted(axioms))}]")
        else:
            lines.append(f"'{declaration}' does not depend on any axioms")
    return "\n".join(lines) + "\n"


class AlignmentRuleTest(unittest.TestCase):
    def errors(self, ledger=LEDGER, assurance=ASSURANCE, core=CORE, generated=GENERATED):
        return checker.alignment_errors(ledger, assurance, core, generated)

    def assertRejected(self, expected, **mutated):
        errors = self.errors(**mutated)
        self.assertTrue(any(expected in error for error in errors), errors)

    def copies(self):
        return copy.deepcopy(LEDGER), copy.deepcopy(ASSURANCE), copy.deepcopy(CORE), copy.deepcopy(GENERATED)

    def test_repository_is_aligned(self):
        self.assertEqual([], self.errors())

    def test_claim_order_is_enforced(self):
        ledger = copy.deepcopy(LEDGER)
        ledger["claims"][0], ledger["claims"][1] = ledger["claims"][1], ledger["claims"][0]
        self.assertRejected("must cover FAR-CORE-001 through 014 in order", ledger=ledger)

    def test_cross_ledger_coverage_is_enforced(self):
        core = copy.deepcopy(CORE)
        core["claims"].append(dict(core["claims"][0], id="FAR-CORE-015"))
        self.assertRejected("core/assurance/formalization claim coverage differs", core=core)

    def test_canonical_prose_drift_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-004")["canonical_prose_statement"] += " Universally."
        self.assertRejected("FAR-CORE-004: canonical prose drift", ledger=ledger)

    def test_missing_lean_module_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-005")["intended_lean_module"] = "mechanization/lean/Absent.lean"
        self.assertRejected("FAR-CORE-005: missing Lean module mechanization/lean/Absent.lean", ledger=ledger)

    def test_missing_declaration_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-005")["lean_declarations"].append("FARCoreV11.absent_theorem")
        self.assertRejected("FAR-CORE-005: missing declaration FARCoreV11.absent_theorem", ledger=ledger)

    def test_kernel_assumption_drift_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-005")["kernel_axioms"] = ["propext"]
        self.assertRejected("FAR-CORE-005: recorded kernel assumptions drifted", ledger=ledger)

    def test_assurance_status_drift_is_rejected(self):
        assurance = copy.deepcopy(ASSURANCE)
        by_id(assurance, "FAR-CORE-006")["formalization_status"] = "PARTIAL_OBSTRUCTION"
        self.assertRejected("FAR-CORE-006: assurance/formalization status drift", assurance=assurance)

    def test_assurance_declaration_drift_is_rejected(self):
        assurance = copy.deepcopy(ASSURANCE)
        by_id(assurance, "FAR-CORE-006")["lean_declarations"] = []
        self.assertRejected("FAR-CORE-006: assurance/ledger Lean declaration drift", assurance=assurance)

    def test_source_hash_drift_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-007")["source_locations"][0]["sha256"] = "0" * 64
        self.assertRejected("FAR-CORE-007: canonical source hash drift", ledger=ledger)

    def test_formalized_claim_with_obstruction_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-008")["obstruction"]["classification"] = "encoding_gap"
        self.assertRejected("FAR-CORE-008: formalized claim retains an obstruction", ledger=ledger)

    def test_partial_formalization_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-009")["formalization_status"] = "PARTIAL/OBSTRUCTION"
        self.assertRejected("must be FORMALIZED after the governed MLL bridge compiles", ledger=ledger)

    def test_far_core_014_obstruction_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-014")["obstruction"]["classification"] = "encoding_gap"
        self.assertRejected("FAR-CORE-014 formalized status retains a classified obstruction", ledger=ledger)

    def test_far_core_014_provenance_overwrite_is_rejected(self):
        core = copy.deepcopy(CORE)
        by_id(core, "FAR-CORE-014")["status"] = "proved"
        self.assertRejected("FAR-CORE-014 historical/application provenance status was overwritten", core=core)

    def test_far_core_014_truth_conflation_is_rejected(self):
        assurance = copy.deepcopy(ASSURANCE)
        by_id(assurance, "FAR-CORE-014")["truth_disposition"] = "OPEN"
        self.assertRejected("FAR-CORE-014 truth disposition was conflated with provenance", assurance=assurance)

    def test_inventory_summary_with_placeholder_is_rejected(self):
        generated = copy.deepcopy(GENERATED)
        generated["w2_summary"]["forbidden_placeholders"] = 1
        self.assertRejected("unexpected W2 inventory summary", generated=generated)

    def test_missing_mutation_control_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-010")["mutation_negative_controls"].append("FARCoreV11Mutations.absent_control")
        self.assertRejected("FAR-CORE-010: missing mutation control FARCoreV11Mutations.absent_control", ledger=ledger)


class AxiomContractRuleTest(unittest.TestCase):
    def test_repeated_declaration_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-002")["lean_declarations"].append(by_id(ledger, "FAR-CORE-001")["lean_declarations"][0])
        self.assertIn("formalization ledger repeats a Lean declaration", checker.axiom_contract_errors(ledger))

    def test_declaration_coverage_drift_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-003")["lean_declarations"].pop()
        self.assertTrue(any("declaration-level axiom contract coverage drift" in e for e in checker.axiom_contract_errors(ledger)))

    def test_claim_axiom_union_mismatch_is_rejected(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-005")["kernel_axioms"] = ["propext"]
        self.assertTrue(any(e.startswith("FAR-CORE-005: declaration-level axiom union") for e in checker.axiom_contract_errors(ledger)))

    def test_duplicate_runtime_output_is_rejected(self):
        output = valid_axiom_output()
        first = output.splitlines()[0]
        self.assertTrue(any("duplicate #print axioms output" in e for e in checker.axiom_output_errors(output + first + "\n", LEDGER)))

    def test_runtime_check_also_enforces_the_ledger_axiom_contract(self):
        ledger = copy.deepcopy(LEDGER)
        by_id(ledger, "FAR-CORE-005")["kernel_axioms"] = ["propext"]
        self.assertTrue(any(e.startswith("FAR-CORE-005: declaration-level axiom union") for e in checker.axiom_output_errors(valid_axiom_output(), ledger)))

    def test_alignment_enforces_generated_axiom_audit_source(self):
        with mock.patch.object(checker, "axiom_audit_source_errors", return_value=["forged audit source"]):
            self.assertIn("forged audit source", checker.alignment_errors(LEDGER, ASSURANCE, CORE, GENERATED))

    def test_missing_runtime_output_is_rejected(self):
        output = "\n".join(valid_axiom_output().splitlines()[1:]) + "\n"
        self.assertTrue(any("runtime #print axioms coverage drift" in e for e in checker.axiom_output_errors(output, LEDGER)))


class ForbiddenPlaceholderTest(unittest.TestCase):
    def count(self, text: str) -> int:
        return len(checker.FORBIDDEN.findall(checker.lean_code(text)))

    def test_placeholders_are_found_anywhere_in_code(self):
        for text in (
            "theorem t : False := by sorry",
            "theorem t : False := sorry",
            "  exact sorry",
            "  admit",
            "axiom h : False",
            "private axiom h : False",
            "@[simp] axiom h : False",
            "noncomputable axiom h : False",
            "constant hidden : False",
            "unsafe def f : Nat := 1",
        ):
            self.assertEqual(1, self.count(text), text)

    def test_prose_strings_and_identifiers_are_not_placeholders(self):
        for text in (
            "-- no sorry here",
            "/- sorry, axiom -/ theorem t : True := trivial",
            "/-- docstring mentioning sorry -/ def x := 1",
            'def s : String := "sorry"',
            "theorem sorryFree : True := trivial",
            "def axiomatic := 1",
        ):
            self.assertEqual(0, self.count(text), text)

    def test_repository_lean_sources_have_no_placeholders(self):
        self.assertEqual(0, GENERATED["w2_summary"]["forbidden_placeholders"])


if __name__ == "__main__":
    unittest.main()
