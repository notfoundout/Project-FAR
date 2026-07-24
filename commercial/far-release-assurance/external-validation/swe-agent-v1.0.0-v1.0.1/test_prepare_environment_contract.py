from __future__ import annotations

import unittest

from prepare_environment import REQUIRED_TEST_SPEC_PROPERTIES, verify_test_spec_contract


class FakeSpec:
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
    def test_exact_export_contract_passes(self) -> None:
        verify_test_spec_contract(FakeSpec())
        self.assertIn("install_repo_script", REQUIRED_TEST_SPEC_PROPERTIES)
        self.assertNotIn("setup_repo_script", REQUIRED_TEST_SPEC_PROPERTIES)

    def test_missing_property_fails(self) -> None:
        class BrokenSpec(FakeSpec):
            install_repo_script = None

        with self.assertRaisesRegex(SystemExit, "empty"):
            verify_test_spec_contract(BrokenSpec())


if __name__ == "__main__":
    unittest.main()
