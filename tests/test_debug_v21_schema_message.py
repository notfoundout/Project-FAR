from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from mechanization.far_mechanization import contract_v2, contract_v21

ROOT = Path(__file__).resolve().parents[1]


class DebugV21SchemaMessage(unittest.TestCase):
    def test_expose_schema_message(self) -> None:
        document = json.loads(
            (ROOT / "conformance" / "far-ir-2.1" / "valid-frontier.json").read_text(
                encoding="utf-8"
            )
        )
        document = copy.deepcopy(document)
        document["report"]["evidence"]["candidates"][0]["costs"] = document["report"][
            "evidence"
        ]["candidates"][0]["costs"][:1]
        document["freeze"]["contract_sha256"] = contract_v2.contract_sha256(document["contract"])
        diagnostics = contract_v21.validate_contract(document).diagnostics
        self.fail(repr([(item.code, item.message, item.path) for item in diagnostics]))


if __name__ == "__main__":
    unittest.main()
