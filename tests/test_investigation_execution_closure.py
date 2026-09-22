from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.check_investigation_execution import (
    LEGACY_PASS_BLOBS,
    is_legacy_pass_manifest,
    validate_manifest,
)


class InvestigationExecutionClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "research/validation/executions").mkdir(parents=True)
        (self.root / "evidence").mkdir(parents=True)
        (self.root / "evidence/audit.md").write_text("# audit\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def evidence_ref() -> list[dict[str, str]]:
        return [{"path": "evidence/audit.md", "locator": "closure evidence"}]

    def valid_closure(self) -> dict:
        evidence = self.evidence_ref()
        evidence_classes = {
            class_id: {"status": "covered", "evidence": copy.deepcopy(evidence)}
            for class_id in (
                "direct_primary_evidence",
                "opposing_disconfirming_evidence",
                "measurement_data_quality",
                "denominator_directness_construct_alignment",
                "alternative_explanations",
                "surviving_narrower_propositions",
                "residual_uncertainty",
            )
        }
        return {
            "status": "resolved",
            "logical_disposition": {
                "outcome": "SUPPORTED",
                "evidence": copy.deepcopy(evidence),
            },
            "search_frame": {
                "scope": "bounded registered corpus",
                "sources_or_spaces": ["registered corpus", "declared counterexample space"],
                "stopping_rule": "repeat bounded search until a terminal pass yields no new material finding",
                "evidence_cutoff": "2026-09-22T20:00:00Z",
            },
            "evidence_classes": evidence_classes,
            "strongest_opposing_evidence": {
                "findings": ["One bounded objection was tested and did not defeat the scoped result."],
                "none_found_basis": None,
            },
            "measurement_and_classification_limits": {
                "findings": ["The result is limited to the registered finite corpus."],
                "none_found_basis": None,
            },
            "alternative_explanations": {
                "findings": ["A competing explanation was tested under the same frozen scope."],
                "none_found_basis": None,
            },
            "surviving_narrower_propositions": {
                "findings": ["No broader proposition is promoted by this result."],
                "none_found_basis": None,
            },
            "residual_uncertainty": {
                "findings": ["Open-domain generalization remains unresolved."],
                "none_found_basis": None,
            },
            "interpretive_closure": {
                "status": "complete",
                "evidence": copy.deepcopy(evidence),
            },
            "terminal_saturation": {
                "status": "complete",
                "new_material_findings": 0,
                "evidence": copy.deepcopy(evidence),
            },
        }

    def valid_manifest(self, investigation: str = "VI-900") -> dict:
        return {
            "schema_version": 1,
            "investigation": investigation,
            "title": "Synthetic closure regression",
            "status": "Research",
            "result": "pass",
            "scope": "synthetic bounded scope",
            "upstream_dependencies": [],
            "required_steps": [
                {
                    "id": "execute",
                    "requirement": "Execute the bounded synthetic investigation.",
                    "status": "complete",
                    "evidence": [{"path": "evidence/audit.md", "locator": "execution"}],
                }
            ],
            "closure": self.valid_closure(),
        }

    def write_manifest(self, data: dict, investigation: str = "VI-900") -> Path:
        path = self.root / f"research/validation/executions/{investigation}.execution.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def errors_for(self, data: dict) -> list[str]:
        investigation = str(data.get("investigation", "VI-900"))
        path = self.write_manifest(data, investigation)
        return validate_manifest(path, root=self.root, manifest_results={investigation: str(data.get("result", ""))})

    def test_valid_new_pass_requires_and_accepts_complete_closure(self) -> None:
        self.assertEqual(self.errors_for(self.valid_manifest()), [])

    def test_pass_without_closure_fails(self) -> None:
        manifest = self.valid_manifest()
        del manifest["closure"]
        errors = self.errors_for(manifest)
        self.assertTrue(any("PASS requires a closure mapping" in error for error in errors), errors)

    def test_atomic_disposition_alone_does_not_close_investigation(self) -> None:
        manifest = self.valid_manifest()
        manifest["closure"] = {
            "status": "resolved",
            "logical_disposition": {
                "outcome": "FALSIFIED",
                "evidence": self.evidence_ref(),
            },
        }
        errors = self.errors_for(manifest)
        self.assertTrue(any("closure.search_frame" in error for error in errors), errors)
        self.assertTrue(any("closure.terminal_saturation" in error for error in errors), errors)

    def test_missing_mandatory_evidence_class_fails(self) -> None:
        manifest = self.valid_manifest()
        del manifest["closure"]["evidence_classes"]["opposing_disconfirming_evidence"]
        errors = self.errors_for(manifest)
        self.assertTrue(any("opposing_disconfirming_evidence is required" in error for error in errors), errors)

    def test_not_applicable_evidence_class_requires_reason(self) -> None:
        manifest = self.valid_manifest()
        manifest["closure"]["evidence_classes"]["denominator_directness_construct_alignment"] = {
            "status": "not_applicable"
        }
        errors = self.errors_for(manifest)
        self.assertTrue(any("not_applicable requires a reason" in error for error in errors), errors)

    def test_not_applicable_evidence_class_with_reason_passes(self) -> None:
        manifest = self.valid_manifest()
        manifest["closure"]["evidence_classes"]["denominator_directness_construct_alignment"] = {
            "status": "not_applicable",
            "reason": "The synthetic claim is not empirical, statistical, or comparative.",
        }
        self.assertEqual(self.errors_for(manifest), [])

    def test_empty_inventory_requires_basis(self) -> None:
        manifest = self.valid_manifest()
        manifest["closure"]["alternative_explanations"] = {
            "findings": [],
            "none_found_basis": "",
        }
        errors = self.errors_for(manifest)
        self.assertTrue(any("alternative_explanations is empty" in error for error in errors), errors)

    def test_terminal_pass_must_find_zero_new_material_items(self) -> None:
        manifest = self.valid_manifest()
        manifest["closure"]["terminal_saturation"]["new_material_findings"] = 1
        errors = self.errors_for(manifest)
        self.assertTrue(any("new_material_findings must be integer 0" in error for error in errors), errors)

    def test_incomplete_result_does_not_require_closure(self) -> None:
        manifest = self.valid_manifest()
        manifest["result"] = "incomplete"
        del manifest["closure"]
        self.assertEqual(self.errors_for(manifest), [])

    def test_historical_pass_exemption_is_exact_blob_bound(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        historical = repository_root / "research/validation/executions/VI-001.execution.yaml"
        self.assertIn("research/validation/executions/VI-001.execution.yaml", LEGACY_PASS_BLOBS)
        self.assertTrue(is_legacy_pass_manifest(historical, repository_root))

        target = self.root / "research/validation/executions/VI-001.execution.yaml"
        target.write_bytes(historical.read_bytes() + b"\n")
        self.assertFalse(is_legacy_pass_manifest(target, self.root))
        errors = validate_manifest(target, root=self.root, manifest_results={"VI-001": "pass"})
        self.assertTrue(any("PASS requires a closure mapping" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
