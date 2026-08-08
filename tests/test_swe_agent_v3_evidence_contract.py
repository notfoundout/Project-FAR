from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "research/external-validation/swe-agent-v3/verify_design.py"
)
SPEC = importlib.util.spec_from_file_location("swe_v3_evidence_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3EvidenceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.here = Path(self.tmp.name)
        for name in (
            "evidence-and-analysis-plan-v1.0.md",
            "README.md",
            "question-v1.0.md",
        ):
            shutil.copy2(MODULE_PATH.parent / name, self.here / name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def assert_evidence_mutation_rejected(self, old: str, new: str) -> None:
        path = self.here / "evidence-and-analysis-plan-v1.0.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(
            text.replace(old, new, 1),
            encoding="utf-8",
            newline="\n",
        )
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_text_boundaries()

    def test_complete_evidence_bundle_section_is_exact(self) -> None:
        mutations = (
            (
                "- authoritative repository provider identity, canonical repository URL, and exact commit;\n",
                "- canonical repository URL and exact commit;\n",
            ),
            (
                "- environment image digest and dependency lock;\n",
                "",
            ),
            (
                "- model provider, endpoint, model version, parameters, "
                "and provider request identifier;\n",
                "",
            ),
            (
                "- randomization position and repetition;\n",
                "- repetition only;\n",
            ),
            (
                "- bundle manifest and content-root digest.\n",
                "- bundle manifest and content-root digest;\n"
                "- operator-selected notes.\n",
            ),
        )
        for index, (old, new) in enumerate(mutations):
            with self.subTest(index=index):
                self.tearDown()
                self.setUp()
                self.assert_evidence_mutation_rejected(old, new)


if __name__ == "__main__":
    unittest.main()
