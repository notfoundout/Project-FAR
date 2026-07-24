from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from validate_manifest import validate

MANIFEST = Path(__file__).with_name("manifest.json")


class ManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_selected_inputs_manifest_is_valid(self) -> None:
        validate(self.payload)

    def test_rejects_nested_pre_freeze_outcome_field(self) -> None:
        leaked = copy.deepcopy(self.payload)
        leaked["execution_record"] = {"nested": {"reward": 1}}
        with self.assertRaisesRegex(AssertionError, "execution_record.nested.reward"):
            validate(leaked)

    def test_declaration_list_remains_allowed(self) -> None:
        declared = copy.deepcopy(self.payload)
        self.assertIn("reward", declared["forbidden_before_primary_freeze"])
        validate(declared)

    def test_rejects_non_frozen_model_choice(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["model"] = "gemini/gemini-flash-latest"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_rejects_nonzero_cost_limit(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["model_parameters"]["total_cost_limit_usd"] = 1.0
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_rejects_false_free_tier_privacy_claim(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["free_tier_constraints"][
            "provider_may_use_inputs_and_outputs_to_improve_products"
        ] = False
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_frozen_status_requires_lock_hash_and_image_id(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["status"] = "execution_inputs_frozen"
        changed["frozen_inputs"]["environment_lock_sha256"] = "bad"
        changed["frozen_inputs"]["local_image_id"] = "sha256:bad"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_rejects_remote_image_assumption(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["environment_image_reference"] = "swebench/nonexistent:latest"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_run_matrix_is_commit_bound(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["execution_requirements"]["runs"][0]["commit"] = "deadbee"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_rejects_parallel_free_tier_execution(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["execution_requirements"]["sequential_runs_required"] = False
        with self.assertRaises(AssertionError):
            validate(changed)


if __name__ == "__main__":
    unittest.main()
