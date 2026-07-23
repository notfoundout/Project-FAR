from __future__ import annotations

import pathlib
import sys
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_release_assurance.cli import build_parser, entrypoint, main


class TestPackagingContract(unittest.TestCase):
    def test_pyproject_declares_console_script(self):
        payload = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(payload["project"]["name"], "far-release-assurance")
        self.assertEqual(payload["project"]["requires-python"], ">=3.11")
        self.assertEqual(
            payload["project"]["scripts"]["far-release"],
            "far_release_assurance.cli:entrypoint",
        )

    def test_readme_documents_gate_exit_codes_and_scope(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for code in ("`0`", "`20`", "`30`", "`40`"):
            self.assertIn(code, text)
        self.assertIn("does not establish hidden cognition", text)

    def test_entrypoint_and_module_parser_share_program_name(self):
        self.assertTrue(callable(entrypoint))
        self.assertTrue(callable(main))
        self.assertEqual(build_parser().prog, "far-release")


if __name__ == "__main__":
    unittest.main()
