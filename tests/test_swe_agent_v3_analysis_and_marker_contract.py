from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "research/external-validation/swe-agent-v3/verify_design.py"
)
SPEC = importlib.util.spec_from_file_location("swe_v3_analysis_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3AnalysisAndMarkerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.here = Path(self.tmp.name)
        for name in (
            "preregistration-v1.0.json",
            "evidence-and-analysis-plan-v1.0.md",
            "README.md",
            "question-v1.0.md",
        ):
            shutil.copy2(MODULE_PATH.parent / name, self.here / name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def mutate_preregistration(self, mutation) -> None:
        path = self.here / "preregistration-v1.0.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def assert_preregistration_rejected(self, mutation) -> None:
        self.mutate_preregistration(mutation)
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_preregistration()

    def reset_fixture(self) -> None:
        self.tearDown()
        self.setUp()

    def test_analysis_key_set_and_multiplicity_policy_are_exact(self) -> None:
        mutations = (
            lambda d: d["analysis"].__setitem__(
                "multiple_comparison_policy",
                "all primary and secondary contrasts are confirmatory",
            ),
            lambda d: d["analysis"].pop("multiple_comparison_policy"),
            lambda d: d["analysis"].__setitem__(
                "post_hoc_subgroup_selection_permitted", True
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_preregistration_rejected(mutation)

    def test_retained_evidence_markers_must_be_unique(self) -> None:
        path = self.here / "evidence-and-analysis-plan-v1.0.md"
        original = path.read_text(encoding="utf-8")
        duplicate = (
            "\n## Evidence bundle per run\n\n"
            "Conflicting duplicate evidence contract.\n\n"
            "## Pre-submission behavior contract\n"
        )
        path.write_text(original + duplicate, encoding="utf-8", newline="\n")
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_text_boundaries()


if __name__ == "__main__":
    unittest.main()
