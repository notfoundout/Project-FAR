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

    def test_rejects_mutable_model_alias(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["model"] = "claude-opus-4-5"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_rejects_wrong_extended_thinking_temperature(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["frozen_inputs"]["model_parameters"]["temperature"] = 0.0
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_frozen_status_requires_valid_sha256_digest(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["status"] = "execution_inputs_frozen"
        changed["frozen_inputs"]["environment_image_digest"] = "sha256:bad"
        with self.assertRaises(AssertionError):
            validate(changed)

    def test_run_matrix_is_commit_bound(self) -> None:
        changed = copy.deepcopy(self.payload)
        changed["execution_requirements"]["runs"][0]["commit"] = "deadbee"
        with self.assertRaises(AssertionError):
            validate(changed)


if __name__ == "__main__":
    unittest.main()
