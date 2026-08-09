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
SPEC = importlib.util.spec_from_file_location("swe_v3_root_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3RootContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.here = Path(self.tmp.name)
        for name in (
            "preregistration-v1.0.json",
            "treatment-capsule-contract-v1.0.json",
            "execution-gate-v1.0.json",
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

    def mutate_json(self, name: str, mutation) -> None:
        path = self.here / name
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def test_complete_pilot_contract_is_locked(self) -> None:
        mutations = (
            lambda d: d["pilot"].__setitem__("required", False),
            lambda d: d["pilot"].__setitem__("minimum_sacrificial_tasks", 0),
            lambda d: d["pilot"].pop("purpose"),
            lambda d: d["pilot"].__setitem__("model_calls_currently_prohibited", False),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.mutate_json("preregistration-v1.0.json", mutation)
                with mock.patch.object(verify_module, "HERE", self.here):
                    with self.assertRaises(verify_module.DesignError):
                        verify_module.verify_preregistration()

    def test_capsule_freeze_and_invalidation_rules_are_locked(self) -> None:
        mutations = (
            lambda d: d.__setitem__("freeze_sequence", []),
            lambda d: d.__setitem__("invalidation_rules", []),
            lambda d: d["freeze_sequence"].pop(),
            lambda d: d["invalidation_rules"].append(
                "operator may waive contamination after outcome reveal"
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.mutate_json("treatment-capsule-contract-v1.0.json", mutation)
                with mock.patch.object(verify_module, "HERE", self.here):
                    with self.assertRaises(verify_module.DesignError):
                        verify_module.verify_capsule_contract()

    def test_complete_execution_gate_policy_is_locked(self) -> None:
        mutations = (
            lambda d: d.__setitem__(
                "gate_rule", "execution is authorized when any one gate is true"
            ),
            lambda d: d.__setitem__("current_blockers", []),
            lambda d: d["forbidden_current_actions"].remove("pilot execution"),
            lambda d: d["gates"].__setitem__("manual_launch_authorization_recorded", True),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.mutate_json("execution-gate-v1.0.json", mutation)
                with mock.patch.object(verify_module, "HERE", self.here):
                    with self.assertRaises(verify_module.DesignError):
                        verify_module.verify_execution_gate()


if __name__ == "__main__":
    unittest.main()
