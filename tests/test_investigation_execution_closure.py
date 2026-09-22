from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.check_investigation_execution import (
    CLOSURE_CONTRACT,
    PRE_CORRECTION_EXECUTION_BLOBS,
    ROOT,
    validate_manifest,
)


class InvestigationExecutionClosureTests(unittest.TestCase):
    def _fixture(self, *, investigation: str = "VI-900", result: str = "pass") -> tuple[dict, str]:
        evidence_path = "research/validation/evidence/closure-test-record.md"
        manifest = {
            "schema_version": 1,
            "investigation": investigation,
            "status": "Accepted" if result == "pass" else "Research",
            "result": result,
            "upstream_dependencies": [],
            "required_steps": [
                {
                    "id": "evaluate",
                    "requirement": "Execute the registered evaluation.",
                    "status": "complete" if result == "pass" else "not_executed",
                    "evidence": ([{"path": evidence_path, "locator": "Evaluation"}] if result == "pass" else []),
                }
            ],
        }
        return manifest, evidence_path

    def _complete_closure(self, evidence_path: str) -> dict:
        evidence = [{"path": evidence_path, "locator": "Evidence closure"}]
        return {
            "contract": CLOSURE_CONTRACT,
            "evidence": evidence,
            "search_frame": {
                "evidence_cutoff": "2026-09-22T00:00:00Z",
                "stopping_rule": "Stop only after the registered classes produce no new material item.",
                "inclusion_rules": ["Material evidence within the frozen scope."],
                "exclusion_rules": [],
            },
            "claim_disposition_separate": True,
            "decisive_evidence_scope_recorded": True,
            "denominator_directness_checked": True,
            "measurement_classification_checked": True,
            "strongest_support_recorded": True,
            "strongest_counterevidence_recorded": True,
            "alternative_explanations_checked": True,
            "surviving_propositions_recorded": True,
            "residual_uncertainty_recorded": True,
            "measurement_limitations": [],
            "measurement_limitations_basis": "No material measurement or classification limitation remained in the frozen scope.",
            "strongest_support": ["Support item S1 recorded in the closure evidence."],
            "strongest_counterevidence": ["Counterevidence item C1 recorded in the closure evidence."],
            "alternative_explanations": [],
            "alternative_explanations_basis": "No material alternative explanation applied to the frozen claim form.",
            "surviving_propositions": [],
            "surviving_propositions_basis": "No narrower proposition survived the adjudication within the frozen scope.",
            "residual_uncertainty": ["Generalization outside the frozen scope remains unresolved."],
            "evidence_search_classes": [
                {
                    "id": "direct_evidence",
                    "status": "executed",
                    "evidence": evidence,
                },
                {
                    "id": "inapplicable_class",
                    "status": "not_applicable",
                    "reason": "The frozen claim contains no causal component.",
                },
            ],
            "terminal_saturation": {
                "completed": True,
                "new_material_evidence": False,
                "new_claim_decomposition": False,
                "new_alternative_explanation": False,
                "new_residual_uncertainty": False,
                "evidence": evidence,
            },
            "methodology_audit": {
                "completed": True,
                "evidence": evidence,
            },
        }

    def _write_fixture(self, root: Path, manifest: dict, evidence_path: str) -> Path:
        evidence = root / evidence_path
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text("# Closure test record\n", encoding="utf-8")
        path = root / "research/validation/executions" / f"{manifest['investigation']}.execution.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        return path

    def test_pre_correction_manifests_are_pinned_and_remain_valid(self) -> None:
        self.assertEqual(set(PRE_CORRECTION_EXECUTION_BLOBS), {"VI-001", "VI-002"})
        for investigation in sorted(PRE_CORRECTION_EXECUTION_BLOBS):
            path = ROOT / "research/validation/executions" / f"{investigation}.execution.yaml"
            self.assertEqual(validate_manifest(path, ROOT), [])

    def test_mutating_pinned_pass_manifest_removes_legacy_exemption(self) -> None:
        source = ROOT / "research/validation/executions/VI-001.execution.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VI-001.execution.yaml"
            path.write_bytes(source.read_bytes() + b"\n# mutation\n")
            errors = validate_manifest(path, ROOT, manifest_results={})
            self.assertIn(
                f"VI-001: PASS requires evidence_closure contract {CLOSURE_CONTRACT}",
                errors,
            )

    def test_future_pass_without_closure_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture()
            path = self._write_fixture(root, manifest, evidence_path)
            errors = validate_manifest(path, root, manifest_results={})
            self.assertIn(
                f"VI-900: PASS requires evidence_closure contract {CLOSURE_CONTRACT}",
                errors,
            )

    def test_future_pass_with_complete_closure_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture()
            manifest["evidence_closure"] = self._complete_closure(evidence_path)
            path = self._write_fixture(root, manifest, evidence_path)
            self.assertEqual(validate_manifest(path, root, manifest_results={}), [])

    def test_terminal_saturation_with_new_material_item_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture()
            closure = self._complete_closure(evidence_path)
            closure["terminal_saturation"]["new_material_evidence"] = True
            manifest["evidence_closure"] = closure
            path = self._write_fixture(root, manifest, evidence_path)
            self.assertIn(
                "VI-900: evidence_closure.terminal_saturation.new_material_evidence must be false",
                validate_manifest(path, root, manifest_results={}),
            )

    def test_not_applicable_search_class_requires_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture()
            closure = self._complete_closure(evidence_path)
            closure["evidence_search_classes"][1].pop("reason")
            manifest["evidence_closure"] = closure
            path = self._write_fixture(root, manifest, evidence_path)
            self.assertIn(
                "VI-900: evidence/search class inapplicable_class NOT_APPLICABLE requires a reason",
                validate_manifest(path, root, manifest_results={}),
            )

    def test_empty_recorded_list_requires_basis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture()
            closure = self._complete_closure(evidence_path)
            closure.pop("surviving_propositions_basis")
            manifest["evidence_closure"] = closure
            path = self._write_fixture(root, manifest, evidence_path)
            self.assertIn(
                "VI-900: empty evidence_closure.surviving_propositions requires surviving_propositions_basis",
                validate_manifest(path, root, manifest_results={}),
            )

    def test_incomplete_execution_does_not_fake_closure_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture(result="incomplete")
            path = self._write_fixture(root, manifest, evidence_path)
            errors = validate_manifest(path, root, manifest_results={})
            self.assertFalse(any("evidence_closure" in error for error in errors))

    def test_legacy_exemption_cannot_be_reused_by_new_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, evidence_path = self._fixture(investigation="VI-003")
            path = self._write_fixture(root, copy.deepcopy(manifest), evidence_path)
            errors = validate_manifest(path, root, manifest_results={})
            self.assertIn(
                f"VI-003: PASS requires evidence_closure contract {CLOSURE_CONTRACT}",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
