"""One targeted mutation per rule of tools/check_project_far_theory_closure.py.

Each case mutates a disposable copy of the authority surfaces and requires the specific
diagnostic, so deleting any rule from the checker fails this module.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("theory_closure_rules", ROOT / "tools/check_project_far_theory_closure.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)

SURFACES = [
    MODULE.HISTORICAL_THEORY, MODULE.HISTORICAL_LEDGER, MODULE.CURRENT_THEORY, MODULE.CURRENT_LEDGER,
    MODULE.REGRESSIONS, MODULE.REPLICATION, MODULE.ACCEPTANCE, MODULE.CORRECTION_AUDIT, MODULE.PROGRAM,
    MODULE.W1_PROMOTION, MODULE.W1_REVIEW, MODULE.ASSURANCE_LEDGER, MODULE.FORMALIZATION_LEDGER,
    MODULE.OLD_PROGRAM, MODULE.REPOSITORY_TRUTH, MODULE.EXPORT_MANIFEST,
]
TEXT_SURFACES = ["README.md", "docs/project-status.md", "docs/ROADMAP.md"]

CURRENT_LEDGER = MODULE.CURRENT_LEDGER.relative_to(ROOT).as_posix()
REGRESSIONS = MODULE.REGRESSIONS.relative_to(ROOT).as_posix()
PROGRAM = MODULE.PROGRAM.relative_to(ROOT).as_posix()
TRUTH = MODULE.REPOSITORY_TRUTH.relative_to(ROOT).as_posix()
EXPORT = MODULE.EXPORT_MANIFEST.relative_to(ROOT).as_posix()
ASSURANCE = MODULE.ASSURANCE_LEDGER.relative_to(ROOT).as_posix()
FORMALIZATION = MODULE.FORMALIZATION_LEDGER.relative_to(ROOT).as_posix()


def case(data: dict, case_id: str) -> dict:
    return next(row for row in data["cases"] if row["id"] == case_id)


def claim(data: dict, claim_id: str) -> dict:
    return next(row for row in data["claims"] if row["id"] == claim_id)


def artifact(data: dict, path: str) -> dict:
    return next(row for row in data["artifacts"] if row["path"] == path)


C4 = "CE-CORE-004-IDENTITY-SUFFICES"
C10 = "CE-CORE-010-FRAME-DOES-NOT-INDEX-T"

# (relative path, mutation kind, mutation, expected diagnostic substring)
JSON_CASES = [
    (REGRESSIONS, lambda d: d["cases"].remove(case(d, C4)), "missing FAR-CORE-004 identity regression"),
    (REGRESSIONS, lambda d: case(d, C4)["representation"].update({"x0": "r0", "x1": "r0"}), "identity must be sufficient for injective"),
    (REGRESSIONS, lambda d: case(d, C4)["expected"].update({"representation_minimal_for_constant": True}), "nonminimal for constant observer"),
    (REGRESSIONS, lambda d: case(d, C4)["expected"].update({"no_single_representation_minimal_for_both": False}), "incompatible-minima expectation"),
    (REGRESSIONS, lambda d: d["cases"].remove(case(d, C10)), "missing FAR-CORE-010 frame regression"),
    (REGRESSIONS, lambda d: case(d, C10)["expected"].update({"exact_theory_same_under_frames": False}), "preserve exact theory under frame-only change"),
    (REGRESSIONS, lambda d: case(d, C10)["expected"]["residue_Gamma0"].append("chi"), "Gamma0 residue fixture mismatch"),
    (REGRESSIONS, lambda d: case(d, C10)["expected"]["residue_Gamma1"].append("chi"), "Gamma1 residue fixture mismatch"),
    (REGRESSIONS, lambda d: case(d, C10)["expected"].update({"residue_changes_with_frame": False}), "frame-sensitive residue"),
    (MODULE.HISTORICAL_LEDGER.relative_to(ROOT).as_posix(), lambda d: d.update({"theory_id": "X"}), "historical v1.0 ledger identity drifted"),
    (CURRENT_LEDGER, lambda d: d.update({"theory_id": "X"}), "current core theory identity mismatch"),
    (CURRENT_LEDGER, lambda d: d.update({"terminal_verdict": "X"}), "terminal verdict mismatch"),
    (CURRENT_LEDGER, lambda d: d["preserved_base"].update({"sha256": "0" * 64}), "does not pin immutable v1.0"),
    (CURRENT_LEDGER, lambda d: d.update({"independent_review_status": "open"}), "independent-review promotion drifted"),
    (CURRENT_LEDGER, lambda d: d.update({"claims": d["claims"] + [dict(d["claims"][0], id="FAR-CORE-015")]}), "core claim set mismatch"),
    (CURRENT_LEDGER, lambda d: claim(d, "FAR-CORE-001").update({"status": "open"}), "FAR-CORE-001..013 must remain exactly the proved claim set"),
    (CURRENT_LEDGER, lambda d: claim(d, "FAR-CORE-014").update({"status": "proved"}), "FAR-CORE-014 must remain supported_derived"),
    (CURRENT_LEDGER, lambda d: claim(d, "FAR-CORE-004").update({"claim": claim(d, "FAR-CORE-004")["claim"].replace("universal sufficiency alone is not denied", "")}), "FAR-CORE-004 corrected minimality/sufficiency boundary drifted"),
    (CURRENT_LEDGER, lambda d: claim(d, "FAR-CORE-010").update({"claim": claim(d, "FAR-CORE-010")["claim"].replace("L,J,I", "L")}), "FAR-CORE-010 exact-theory/residue dependency split drifted"),
    (PROGRAM, lambda d: d.update({"status": "active"}), "post-closure program identity/terminal status mismatch"),
    (PROGRAM, lambda d: d.update({"governing_theory": "PROJECT-FAR-CORE-THEORY-1.0"}), "does not govern v1.1"),
    (PROGRAM, lambda d: d.update({"core_theory_closed": False}), "reopens the terminal kernel"),
    (PROGRAM, lambda d: next(w for w in d["workstreams"] if w["id"] == "PCA-W4-DOMAIN-CONTRACTS").update({"state": "active"}), "PCA-W4 must reflect the completed finite-explicit domain-contract campaign"),
    (PROGRAM, lambda d: d["next_action"].update({"workstream": "PCA-W7"}), "must have no registered workstream"),
    (PROGRAM, lambda d: d["next_action"].update({"obligation": "none"}), "must preserve downstream OP-28"),
    (MODULE.W1_PROMOTION.relative_to(ROOT).as_posix(), lambda d: d["terminal_counts"].update({"OPEN": 1}), "W1 promotion disposition/counts drifted"),
    (MODULE.W1_REVIEW.relative_to(ROOT).as_posix(), lambda d: d["final"]["claim_counts"].update({"REFUTED": 1}), "sealed W1 final-review counts drifted"),
    (ASSURANCE, lambda d: d["claims"].pop(), "assurance/formalization ledger coverage drifted"),
    (ASSURANCE, lambda d: claim(d, "FAR-CORE-003").update({"truth_disposition": "OPEN"}), "FAR-CORE-003: promoted truth disposition drifted"),
    (FORMALIZATION, lambda d: claim(d, "FAR-CORE-003").update({"kernel_check": "FAIL"}), "FAR-CORE-003: W2 outcome/kernel status drifted"),
    (MODULE.OLD_PROGRAM.relative_to(ROOT).as_posix(), lambda d: d.update({"status": "active"}), "historical post-terminal program is still current"),
    (TRUTH, lambda d: d["project_status"].update({"governing_core": "X"}), "does not point to v1.1"),
    (TRUTH, lambda d: d["project_status"].update({"historical_core_sha256": "0" * 64}), "does not preserve v1.0 hash"),
    (TRUTH, lambda d: d["project_status"].update({"completed_contract_schema_workstream": None}), "does not record completed W3"),
    (TRUTH, lambda d: d["project_status"].update({"completed_domain_contracts_workstream": None}), "does not record completed W4"),
    (TRUTH, lambda d: d["project_status"].update({"completed_approximation_cost_workstream": None}), "does not record completed W5"),
    (TRUTH, lambda d: d["project_status"].update({"completed_audit_utility_workstream": None}), "does not record completed W6"),
    (TRUTH, lambda d: d["project_status"].update({"active_workstream": "PCA-W7"}), "must have no active POST-CLOSURE workstream"),
    (TRUTH, lambda d: d["project_status"].update({"current_phase": "X"}), "terminal phase mismatch"),
    (TRUTH, lambda d: d["project_status"].update({"formalization_status": "X"}), "does not record completed W2 formalization"),
    (TRUTH, lambda d: d["project_status"].update({"domain_contracts_status": "X"}), "does not record the bounded W4 result"),
    (TRUTH, lambda d: d["project_status"].update({"audit_utility_status": "human_utility_established"}), "does not preserve the bounded W6 result/nonclaims"),
    (TRUTH, lambda d: d["specification_export"].update({"export_version": "9.9.9"}), "repository truth authority export version mismatch"),
    (TRUTH, lambda d: d["specification_export"].update({"governing_core": "X"}), "export does not mirror v1.1"),
    (TRUTH, lambda d: d["specification_export"].update({"historical_core_status": "canonical"}), "does not mark embedded v1.0 export historical"),
    (EXPORT, lambda d: d.update({"export_version": "9.9.9"}), "must be regenerated at version 1.2.0"),
    (EXPORT, lambda d: d.update({"core_theory_id": "X"}), "does not identify v1.1 as governing core"),
    (EXPORT, lambda d: artifact(d, "theorems/Project-FAR-Theory-Closure-v1.0.md").update({"status": "canonical"}), "preserve v1.0 exactly as historical"),
    (EXPORT, lambda d: artifact(d, "theorems/Project-FAR-Theory-Closure-v1.1.md").update({"status": "historical"}), "carry v1.1 as canonical theorem"),
    (EXPORT, lambda d: artifact(d, "theorems/project-far-core-theory-v1.1.json").update({"status": "historical"}), "carry v1.1 machine ledger as canonical"),
]

TEXT_CASES = [
    (MODULE.HISTORICAL_THEORY.relative_to(ROOT).as_posix(), lambda t: t + "\nedited\n", "historical v1.0 theory bytes changed"),
    (MODULE.HISTORICAL_THEORY.relative_to(ROOT).as_posix(), lambda t: t.replace(MODULE.EXPECTED_VERDICT, "X"), "historical v1.0 theory lost terminal verdict"),
    (MODULE.CURRENT_THEORY.relative_to(ROOT).as_posix(), lambda t: t.replace("10.1214/aoms/1177729032", "X"), "current v1.1 theory missing '10.1214/aoms/1177729032'"),
    (MODULE.REPLICATION.relative_to(ROOT).as_posix(), lambda t: t.replace("not independent review", "X"), "correction replication record missing 'not independent review'"),
    (MODULE.ACCEPTANCE.relative_to(ROOT).as_posix(), lambda t: t.replace("internally replicated", "X"), "acceptance/promotion record missing 'internally replicated'"),
    ("README.md", lambda t: t.replace("Historical v1.0", "X"), "README.md: missing 'Historical v1.0'"),
]


class TheoryClosureRuleTest(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.root = Path(self._directory.name)
        relatives = [p.relative_to(ROOT).as_posix() for p in SURFACES] + TEXT_SURFACES
        relatives += [r for r in ("docs/governance/project-far-theory-closure-acceptance-v1.1.md", "docs/audits/project-far-core-theory-v1.1-correction-audit.md")]
        for relative in relatives:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def tearDown(self):
        self._directory.cleanup()

    def test_unmutated_copy_passes(self):
        self.assertEqual([], MODULE.validate(self.root))

    def test_every_json_rule_is_enforced(self):
        for relative, change, expected in JSON_CASES:
            with self.subTest(expected=expected):
                path = self.root / relative
                original = path.read_bytes()
                data = json.loads(original)
                change(data)
                path.write_text(json.dumps(data), encoding="utf-8")
                try:
                    errors = MODULE.validate(self.root)
                finally:
                    path.write_bytes(original)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_every_text_rule_is_enforced(self):
        for relative, change, expected in TEXT_CASES:
            with self.subTest(expected=expected):
                path = self.root / relative
                original = path.read_bytes()
                path.write_text(change(original.decode("utf-8")), encoding="utf-8")
                try:
                    errors = MODULE.validate(self.root)
                finally:
                    path.write_bytes(original)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_missing_authority_surface_is_rejected(self):
        (self.root / MODULE.REPLICATION.relative_to(ROOT)).unlink()
        self.assertTrue(any("missing authority/provenance surface" in e for e in MODULE.validate(self.root)))

    def test_missing_current_text_surface_is_rejected(self):
        (self.root / "docs/ROADMAP.md").unlink()
        self.assertIn("missing current authority surface: docs/ROADMAP.md", MODULE.validate(self.root))


if __name__ == "__main__":
    unittest.main()
