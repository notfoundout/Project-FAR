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
SPEC = importlib.util.spec_from_file_location("swe_v3_contract_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3ContractLockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.here = Path(self.tmp.name)
        for name in (
            "preregistration-v1.0.json",
            "treatment-capsule-contract-v1.0.json",
        ):
            shutil.copy2(MODULE_PATH.parent / name, self.here / name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def mutate(self, name: str, mutation) -> None:
        path = self.here / name
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def assert_preregistration_rejected(self, mutation) -> None:
        self.mutate("preregistration-v1.0.json", mutation)
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_preregistration()

    def assert_capsule_rejected(self, mutation) -> None:
        self.mutate("treatment-capsule-contract-v1.0.json", mutation)
        with mock.patch.object(verify_module, "HERE", self.here):
            with self.assertRaises(verify_module.DesignError):
                verify_module.verify_capsule_contract()

    def reset_fixture(self) -> None:
        self.tearDown()
        self.setUp()

    def test_blinding_contract_is_exact(self) -> None:
        mutations = (
            lambda d: d.pop("blinding"),
            lambda d: d.__setitem__("blinding", {}),
            lambda d: d["blinding"].pop("arm_labels_blinded_to_graders"),
            lambda d: d["blinding"].__setitem__(
                "arm_labels_blinded_to_graders", False
            ),
            lambda d: d["blinding"].__setitem__(
                "operator_identity_blinded", True
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_preregistration_rejected(mutation)

    def test_capsule_required_outputs_are_exact(self) -> None:
        mutations = (
            lambda d: d.pop("required_outputs"),
            lambda d: d.__setitem__("required_outputs", {}),
            lambda d: d["required_outputs"].pop("capsule_root_sha256"),
            lambda d: d["required_outputs"].__setitem__(
                "capsule_root_sha256", "premature"
            ),
            lambda d: d["required_outputs"].__setitem__(
                "archive_format", "zip"
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_capsule_rejected(mutation)

    def test_arm_treatment_semantics_are_exact(self) -> None:
        mutations = (
            lambda d: d["arms"][2].__setitem__("extra_capsule", None),
            lambda d: d["arms"][2].pop("capsule_contract"),
            lambda d: d["arms"][0].__setitem__("extra_capsule", "far"),
            lambda d: d["arms"][1].__setitem__("extra_capsule", None),
            lambda d: d["arms"][2].__setitem__("budget", "larger_than_other_arms"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_preregistration_rejected(mutation)

    def test_outcome_contract_is_exact(self) -> None:
        mutations = (
            lambda d: d.pop("outcomes"),
            lambda d: d["outcomes"]["primary"].__setitem__(
                "invalid_is_not_resolved", False
            ),
            lambda d: d["outcomes"]["primary"].__setitem__(
                "source", "operator_judgment"
            ),
            lambda d: d["outcomes"]["primary"]["values"].remove("invalid"),
            lambda d: d["outcomes"]["secondary"].remove("budget_exhausted"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_preregistration_rejected(mutation)

    def test_capsule_forbidden_content_boundary_is_exact(self) -> None:
        mutations = (
            lambda d: d.pop("forbidden_content_classes"),
            lambda d: d["forbidden_content_classes"].remove(
                "confirmatory repository names"
            ),
            lambda d: d["forbidden_content_classes"].remove(
                "issue text from confirmatory tasks"
            ),
            lambda d: d["forbidden_content_classes"].remove(
                "provider-specific hidden memory"
            ),
            lambda d: d["forbidden_content_classes"].append(
                "operator-selected contextual hints"
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture()
                self.assert_capsule_rejected(mutation)


if __name__ == "__main__":
    unittest.main()
