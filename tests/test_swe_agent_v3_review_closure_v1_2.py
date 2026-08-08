from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
PATH = DIR / "verify_review_closure_v1_2.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_review_closure_v1_2", PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class ReviewClosureV12Tests(unittest.TestCase):
    def _mutated_amendment_fails(self, mutator) -> None:
        data = json.loads((DIR / "review-closure-amendment-v1.2.json").read_text(encoding="utf-8"))
        altered = copy.deepcopy(data)
        mutator(altered)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "amendment.json"
            path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(module.DesignError):
                module.validate(path)

    def test_canonical_closure_passes(self) -> None:
        module.validate()

    def test_historical_authority_is_snapshot_rooted(self) -> None:
        for path, expected_blob in module.HISTORICAL:
            self.assertEqual(module._blob(path), expected_blob)
            self.assertEqual(module._current_blob(path), expected_blob)

    def test_seed_input_binding_is_immutable(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["bootstrap_seed_effective_contract"]["inputs"][1].__setitem__(
                "git_blob_sha1", "0" * 40
            )
        )

    def test_seed_authority_correction_cannot_be_removed(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["bootstrap_seed_effective_contract"].__setitem__(
                "authority_correction", "all other fields remained unchanged"
            )
        )

    def test_task_identity_is_unique_independently_of_strata(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_identity_contract"].__setitem__(
                "strata_excluded_from_identity", False
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_identity_contract"].__setitem__(
                "uniqueness_rule", "task_bundle_root_sha256 is unique"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_identity_contract"].__setitem__(
                "descriptor_required_keys_exactly",
                module.TASK_IDENTITY_KEYS + ["task_strata"],
            )
        )

    def test_effective_descriptor_keys_are_exact_locked(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_bundle_root_extension"].__setitem__(
                "descriptor_required_keys_exactly",
                ["algorithm_id", "task_identity_sha256", "task_strata", "arbitrary_key"],
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_identity_contract"].__setitem__(
                "descriptor_required_keys_exactly",
                [
                    "algorithm_id",
                    "repository_provider",
                    "repository_provider_id",
                    "canonical_repository_url",
                    "arbitrary_key",
                    "task_payload_sha256",
                    "task_payload_bytes",
                ],
            )
        )

    def test_task_strata_classifier_is_deterministic_and_multilabel(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_strata"].__setitem__(
                "allowed_values_exactly", module.REQUIRED_STRATA[:-1]
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_strata"].__setitem__(
                "classification_inputs_required", module.CLASSIFICATION_INPUTS[:-1]
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_strata"]["deterministic_mapping"].__setitem__(
                "multi_file_change", "operator decides"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_strata"].__setitem__(
                "multi_label_rule", "choose one primary label"
            )
        )

    def test_task_preexecution_validation_is_exact(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"].__setitem__(
                "preexecution_validation_extension",
                d["task_manifest_effective_contract"]["preexecution_validation_extension"][:-1],
            )
        )

    def test_harm_thresholds_and_slot_construction_are_exact(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"]["rate_harms"]["invalid_run_rate"].__setitem__(
                "threshold", {"numerator": 1, "denominator": 5}
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"]["rate_harms"]["invalid_run_rate"].__setitem__(
                "denominator_rule", "complete valid runs only"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"]["rate_harms"]["regression_introduction"].__setitem__(
                "event_rule", "task indicator is 1 if any repetition regresses"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"].__setitem__(
                "pairing_rule", "pair tasks when convenient"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"].__setitem__(
                "replacement_rule", "replacement adds a new denominator run"
            )
        )

    def test_harm_missingness_and_retention_fail_closed(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"].__setitem__(
                "missing_harm_evidence_rule", "missing evidence may be ignored"
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"].__setitem__(
                "retained_evidence",
                d["critical_harm_threshold_contract"]["retained_evidence"][:-1],
            )
        )

    def test_launch_prerequisite_contents_are_exact_locked(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["execution_gate_extension"].__setitem__(
                "pilot_prerequisites", ["no prerequisite"] * 3
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["execution_gate_extension"].__setitem__(
                "confirmatory_prerequisites", ["no prerequisite"] * 3
            )
        )

    def test_execution_and_theory_boundaries_remain_closed(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["authority"].__setitem__("model_calls_authorized", True)
        )
        self._mutated_amendment_fails(
            lambda d: d["execution_gate_extension"].__setitem__("current_execution_authorized", True)
        )
        self._mutated_amendment_fails(
            lambda d: d.__setitem__(
                "nonclaims",
                [x for x in d["nonclaims"] if "accepted Project FAR theory" not in x],
            )
        )


if __name__ == "__main__":
    unittest.main()
