from __future__ import annotations

import importlib.util
import unittest

from prepare_environment import OUTCOME_BEARING_FIELDS, public_task_record
from test_spec_contract import (
    REQUIRED_TEST_SPEC_PROPERTIES,
    successful_instance_ids,
    verify_build_result,
    verify_test_spec_contract,
)


class FakeSpec:
    instance_id = "scikit-learn__scikit-learn-14125"
    base_dockerfile = "FROM scratch\n"
    env_dockerfile = "FROM scratch\n"
    instance_dockerfile = "FROM scratch\n"
    setup_env_script = "#!/bin/bash\n"
    install_repo_script = "#!/bin/bash\n"
    eval_script = "#!/bin/bash\n"
    base_image_key = "base"
    env_image_key = "env"
    instance_image_key = "instance"
    platform = "linux/x86_64"


class TestSpecContractTests(unittest.TestCase):
    def test_contract_module_has_no_runtime_dependencies(self) -> None:
        self.assertIsNone(importlib.util.find_spec("docker"))
        self.assertIn("install_repo_script", REQUIRED_TEST_SPEC_PROPERTIES)

    def test_exact_export_contract_passes(self) -> None:
        verify_test_spec_contract(FakeSpec())
        self.assertIn("install_repo_script", REQUIRED_TEST_SPEC_PROPERTIES)
        self.assertNotIn("setup_repo_script", REQUIRED_TEST_SPEC_PROPERTIES)

    def test_missing_property_fails(self) -> None:
        class BrokenSpec(FakeSpec):
            install_repo_script = None

        with self.assertRaisesRegex(SystemExit, "empty"):
            verify_test_spec_contract(BrokenSpec())

    def test_direct_testspec_build_result_is_supported(self) -> None:
        successful = [FakeSpec()]
        self.assertEqual(successful_instance_ids(successful), {FakeSpec.instance_id})
        verify_build_result(successful, [], FakeSpec.instance_id)

    def test_exact_observed_tuple_build_result_is_supported(self) -> None:
        successful = [(FakeSpec(), "build metadata")]
        self.assertEqual(successful_instance_ids(successful), {FakeSpec.instance_id})
        verify_build_result(successful, [], FakeSpec.instance_id)

    def test_string_build_result_is_rejected(self) -> None:
        with self.assertRaisesRegex(SystemExit, "tuple whose first element"):
            verify_build_result(["instance-image-key"], [], FakeSpec.instance_id)

    def test_failed_build_result_is_fatal(self) -> None:
        with self.assertRaisesRegex(SystemExit, "reported failures"):
            verify_build_result([(FakeSpec(), "metadata")], {FakeSpec.instance_id: "failure"}, FakeSpec.instance_id)

    def test_public_task_record_redacts_outcome_fields(self) -> None:
        record = {
            "instance_id": FakeSpec.instance_id,
            "repo": "scikit-learn/scikit-learn",
            "base_commit": "abc",
            "problem_statement": "public issue text",
            "patch": "gold patch",
            "test_patch": "gold tests",
            "FAIL_TO_PASS": "[\"test_x\"]",
            "PASS_TO_PASS": "[\"test_y\"]",
        }
        public = public_task_record(record)
        for field in OUTCOME_BEARING_FIELDS:
            self.assertNotIn(field, public)
        self.assertFalse(public["outcome_fields_included"])
        self.assertEqual(public["problem_statement"], "public issue text")


if __name__ == "__main__":
    unittest.main()
