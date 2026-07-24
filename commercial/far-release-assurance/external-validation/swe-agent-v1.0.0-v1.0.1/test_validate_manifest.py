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

    def test_frozen_protocol_manifest_is_valid(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
