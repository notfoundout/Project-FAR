from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from far_decision_integrity.adjudicate import adjudicate
from far_decision_integrity.cli import main
from far_decision_integrity.model import (
    LEGACY_SCHEMA_VERSION,
    SCHEMA_VERSION,
    DecisionPackage,
    IntegrityStatus,
    PackageValidationError,
)
from far_decision_integrity.report import report_payload
from far_decision_integrity.semantic_audit import (
    SemanticDisposition,
    SemanticVerifierUnavailable,
)


def payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "decision_id": "semantic-case-001",
        "decision_type": "external_agent_action",
        "policy_version": "policy/1",
        "decision_root": "conclusion",
        "proposed_action": {"kind": "complete_task"},
        "nodes": [
            {"node_id": "evidence", "kind": "evidence", "statement": "Evidence observed."},
            {"node_id": "rule", "kind": "rule", "statement": "Evidence is required."},
            {"node_id": "conclusion", "kind": "conclusion", "statement": "Complete task."},
        ],
        "dependencies": [
            {"source_id": "evidence", "target_id": "conclusion", "relation": "supports"},
            {"source_id": "rule", "target_id": "conclusion", "relation": "authorizes"},
        ],
        "authorization_requirements": ["evidence", "rule"],
        "unknowns": [],
        "trace_completeness": 1.0,
        "semantic_contracts": [],
        "metadata": {},
    }


def fixture(relative: str) -> dict:
    return json.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))


def binding(
    record: dict,
    *,
    purpose: str = "exact_sufficiency",
    selected_candidate_id: str | None = None,
    target_node_id: str = "conclusion",
    binding_id: str = "semantic.binding.1",
) -> dict:
    result = {
        "binding_id": binding_id,
        "target_node_id": target_node_id,
        "purpose": purpose,
        "record": record,
    }
    if selected_candidate_id is not None:
        result["selected_candidate_id"] = selected_candidate_id
    return result


class TestSemanticAudit(unittest.TestCase):
    def test_legacy_package_remains_readable(self):
        data = payload()
        data["schema_version"] = LEGACY_SCHEMA_VERSION
        data.pop("semantic_contracts")
        package = DecisionPackage.from_dict(data)
        self.assertEqual(package.schema_version, LEGACY_SCHEMA_VERSION)
        self.assertEqual(package.semantic_contracts, ())
        self.assertEqual(adjudicate(package).status, IntegrityStatus.JUSTIFIED)

    def test_legacy_package_cannot_silently_gain_semantic_contracts(self):
        data = payload()
        data["schema_version"] = LEGACY_SCHEMA_VERSION
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/valid-factorization.json"))
        ]
        with self.assertRaisesRegex(PackageValidationError, "predates semantic_contracts"):
            DecisionPackage.from_dict(data)

    def test_binding_must_target_declared_decision_node(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(
                fixture("conformance/far-ir-2.0/valid-factorization.json"),
                target_node_id="missing",
            )
        ]
        with self.assertRaisesRegex(PackageValidationError, "targets undeclared node"):
            DecisionPackage.from_dict(data)

    def test_factorization_clears_exact_semantic_gate_and_binds_verifier(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/valid-factorization.json"))
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.JUSTIFIED)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.SATISFIES)
        self.assertEqual(result.semantic_audits[0].target_node_id, "conclusion")
        roles = {artifact.role for artifact in result.semantic_audits[0].verifier_artifacts}
        self.assertEqual(roles, {"semantic-verifier", "semantic-schema"})
        for artifact in result.semantic_audits[0].verifier_artifacts:
            self.assertRegex(artifact.sha256, r"^[0-9a-f]{64}$")

    def test_valid_collision_forces_unsupported(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/valid-collision.json"))
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.MATERIAL_LOSS)
        self.assertIn("semantic-material-loss", {finding.rule_id for finding in result.findings})

    def test_quotient_is_verified_analysis_but_not_exact_sufficiency(self):
        quotient = fixture("conformance/far-ir-2.0/valid-quotient.json")
        data = payload()
        data["semantic_contracts"] = [binding(quotient, purpose="analysis_only")]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.VERIFIED_ANALYSIS)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertIn("semantic-contract-required", {finding.rule_id for finding in result.findings})

        data = payload()
        data["semantic_contracts"] = [binding(quotient, purpose="exact_sufficiency")]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.INVALID)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertIn(
            "SEMANTIC_PURPOSE_EVIDENCE_MISMATCH",
            {item.code for item in result.semantic_audits[0].diagnostics},
        )

    def test_invalid_factorization_fails_closed_and_preserves_diagnostic(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/invalid-factorization.json"))
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.INVALID)
        codes = {item.code for item in result.semantic_audits[0].diagnostics}
        self.assertIn("FACTORIZATION_FAILURE", codes)
        encoded = report_payload(result)
        self.assertIn(
            "FACTORIZATION_FAILURE",
            {item["code"] for item in encoded["semantic_audits"][0]["diagnostics"]},
        )

    def test_v21_selected_feasible_candidate_clears_gate(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(
                fixture("conformance/far-ir-2.1/valid-frontier.json"),
                purpose="approximation_candidate",
                selected_candidate_id="randomized",
            )
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.JUSTIFIED)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.SATISFIES)
        roles = {artifact.role for artifact in result.semantic_audits[0].verifier_artifacts}
        self.assertEqual(
            roles,
            {"semantic-verifier", "semantic-schema", "shared-exact-verifier"},
        )

    def test_v21_selected_infeasible_candidate_forces_unsupported(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(
                fixture("conformance/far-ir-2.1/valid-zero-boundary.json"),
                purpose="approximation_candidate",
                selected_candidate_id="randomized",
            )
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.OUTSIDE_TOLERANCE)
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)
        self.assertIn("semantic-outside-tolerance", {finding.rule_id for finding in result.findings})

    def test_v21_unknown_selected_candidate_is_unverifiable(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(
                fixture("conformance/far-ir-2.1/valid-frontier.json"),
                purpose="approximation_candidate",
                selected_candidate_id="not-a-candidate",
            )
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.INVALID)
        self.assertIn(
            "SEMANTIC_SELECTED_CANDIDATE_UNKNOWN",
            {item.code for item in result.semantic_audits[0].diagnostics},
        )

    def test_unsupported_ir_version_is_unverifiable(self):
        data = payload()
        data["semantic_contracts"] = [
            binding({"format_version": "far-ir/999"}, purpose="analysis_only")
        ]
        result = adjudicate(DecisionPackage.from_dict(data))
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.INVALID)

    def test_required_missing_semantic_contract_is_unverifiable(self):
        result = adjudicate(DecisionPackage.from_dict(payload()), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertIn("semantic-contract-required", {finding.rule_id for finding in result.findings})

    def test_canonical_verifier_unavailable_fails_closed(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/valid-factorization.json"))
        ]
        with patch(
            "far_decision_integrity.semantic_audit._load_validator",
            side_effect=SemanticVerifierUnavailable("controlled verifier outage"),
        ):
            result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNVERIFIABLE)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.UNAVAILABLE)

    def test_semantic_success_cannot_override_contradicted_evidence(self):
        data = payload()
        data["nodes"][0]["attributes"] = {"contradicted": True}
        data["semantic_contracts"] = [
            binding(fixture("conformance/far-ir-2.0/valid-factorization.json"))
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.semantic_audits[0].disposition, SemanticDisposition.SATISFIES)
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)

    def test_any_material_loss_dominates_a_satisfying_contract(self):
        data = payload()
        data["semantic_contracts"] = [
            binding(
                fixture("conformance/far-ir-2.0/valid-factorization.json"),
                binding_id="semantic.binding.good",
            ),
            binding(
                fixture("conformance/far-ir-2.0/valid-collision.json"),
                binding_id="semantic.binding.bad",
            ),
        ]
        result = adjudicate(DecisionPackage.from_dict(data), require_semantic_contract=True)
        self.assertEqual(result.status, IntegrityStatus.UNSUPPORTED)

    def test_cli_require_semantic_contract_uses_unverifiable_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "package.json"
            source.write_text(json.dumps(payload()), encoding="utf-8")
            self.assertEqual(main([str(source), "--require-semantic-contract"]), 32)


if __name__ == "__main__":
    unittest.main()
