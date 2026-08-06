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
SPEC = importlib.util.spec_from_file_location("swe_v3_primary_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3PrimaryAndBehaviorContractTests(unittest.TestCase):
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

    def reset_fixture(self) -> None:
        self.tearDown()
        self.setUp()

    def mutate_preregistration(self, mutation) -> None:
        path = self.here / "preregistration-v1.0.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def test_primary_and_secondary_contrasts_are_exact(self) -> None:
        mutations = (
            lambda d: d.__setitem__("primary_contrast", "far_minus_baseline"),
            lambda d: d.__setitem__("secondary_contrasts", []),
            lambda d: d.__setitem__(
                "secondary_contrasts",
                ["placebo_minus_baseline", "far_minus_baseline"],
            ),
            lambda d: d["secondary_contrasts"].append("far_minus_historical_v2"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.mutate_preregistration(mutation)
                with mock.patch.object(verify_module, "HERE", self.here):
                    with self.assertRaises(verify_module.DesignError):
                        verify_module.verify_preregistration()

    def mutate_evidence(self, mutation) -> None:
        path = self.here / "evidence-and-analysis-plan-v1.0.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(mutation(text), encoding="utf-8", newline="\n")

    def assert_text_rejected(self, mutation) -> None:
        self.mutate_evidence(mutation)
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_text_boundaries()

    def test_semantically_duplicate_atx_headings_are_rejected(self) -> None:
        mutations = (
            lambda text: text + "\n## Evidence bundle per run ##\nConflict.\n",
            lambda text: text + "\n## Pre-submission behavior contract ##\nConflict.\n",
            lambda text: text + "\n## Placebo exposure matching ##\nConflict.\n",
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_text_rejected(mutation)

    def test_fenced_pseudo_headings_do_not_count(self) -> None:
        self.mutate_evidence(
            lambda text: text
            + "\n```text\n## Evidence bundle per run ##\n"
            + "## Pre-submission behavior contract ##\n"
            + "## Placebo exposure matching ##\n```\n"
        )
        with mock.patch.object(verify_module, "HERE", self.here):
            verify_module.verify_text_boundaries()

    def test_pre_submission_behavior_contract_is_exact(self) -> None:
        mutations = (
            lambda text: text.replace(
                "1. a reproduction attempt or explicit `reproduction_unavailable`;\n",
                "",
                1,
            ),
            lambda text: text.replace(
                "4. execution of the identified target test before submission, or "
                "explicit `target_test_unavailable`;\n",
                "4. execution of any available test before submission;\n",
                1,
            ),
            lambda text: text.replace(
                "6. a patch that modifies an intended repository path, unless the run "
                "terminates with an explicit no-patch failure.\n",
                "6. a patch that modifies an intended repository path, unless the run "
                "terminates with an explicit no-patch failure;\n"
                "7. operator-selected post-hoc guidance.\n",
                1,
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_text_rejected(mutation)


if __name__ == "__main__":
    unittest.main()
