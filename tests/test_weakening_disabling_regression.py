"""Regressions for weakening that leaves every syntactic strength metric unchanged.

The adversarial probe (tools/assurance_adversarial_probe.py, V1 and U5) disabled a checker by
inserting an early exit before its body, and a test module by moving it out of `test_*.py`
discovery. Neither changed an assertion, branch, or failure-path count, so both passed.
"""
from __future__ import annotations

import ast
import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import weakening

CHECKER = (
    "import sys\n\n"
    "def main() -> int:\n"
    "    errors = []\n"
    "    if not sys.argv:\n"
    "        errors.append('no argv')\n"
    "    if errors:\n"
    "        raise SystemExit(1)\n"
    "    return 0\n"
)
TEST_MODULE = (
    "import unittest\n\n"
    "class T(unittest.TestCase):\n"
    "    def test_a(self):\n"
    "        self.assertEqual(1, 1)\n"
    "        self.assertTrue(True)\n"
)


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


class _Repository:
    def __init__(self, root: Path, files: dict[str, str]) -> None:
        self.root = root
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "assurance@example.invalid")
        _git(root, "config", "user.name", "Validator Assurance")
        self.write(files, "base")
        self.base = _git(root, "rev-parse", "HEAD")

    def write(self, files: dict[str, str], message: str) -> None:
        for path, text in files.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-qm", message)

    def failures(self) -> dict[str, list[str]]:
        report = weakening.detect_weakening(self.root, base=self.base)
        return {finding.path: finding.failures for finding in report.findings if finding.failures}


class UnreachableStatementTests(unittest.TestCase):
    def _count(self, source: str) -> int:
        return weakening.analyze(source, "x.py").unreachable

    def test_terminators_count_the_rest_of_their_own_block(self) -> None:
        self.assertEqual(self._count("def f():\n    return 1\n    a = 2\n    b = 3\n"), 2)
        self.assertEqual(self._count("def f():\n    raise SystemExit(0)\n    a = 2\n"), 1)
        self.assertEqual(self._count("import sys\nsys.exit(0)\nx = 1\n"), 1)
        self.assertEqual(self._count("def t(self):\n    self.skipTest('x')\n    self.assertTrue(1)\n"), 1)
        self.assertEqual(self._count("for i in x:\n    continue\n    y = i\nelse:\n    pass\n"), 1)
        self.assertEqual(self._count("try:\n    pass\nfinally:\n    return_value = 1\n"), 0)

    def test_conditional_exits_and_terminators_at_block_end_are_not_dead_code(self) -> None:
        self.assertEqual(self._count(CHECKER), 0)
        self.assertEqual(self._count("def f(x):\n    if x:\n        return 1\n    return 2\n"), 0)
        self.assertEqual(self._count(TEST_MODULE), 0)


class DisablingWithoutMetricChangeTests(unittest.TestCase):
    def test_early_exit_inserted_before_a_checker_body_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = _Repository(Path(directory), {"tools/check_example.py": CHECKER})
            repo.write({"tools/check_example.py": CHECKER.replace(
                "    errors = []\n", "    raise SystemExit(0)\n    errors = []\n", 1)}, "disable")
            failures = repo.failures()
            self.assertIn("tools/check_example.py", failures)
            self.assertIn("unreachable statement count increased: 0 -> 4", failures["tools/check_example.py"])

    def test_skip_or_return_inserted_before_assertions_is_rejected(self) -> None:
        for terminator in ("self.skipTest('later')", "return"):
            with self.subTest(terminator=terminator), tempfile.TemporaryDirectory() as directory:
                repo = _Repository(Path(directory), {"tests/test_example.py": TEST_MODULE})
                repo.write({"tests/test_example.py": TEST_MODULE.replace(
                    "        self.assertEqual", f"        {terminator}\n        self.assertEqual", 1)}, "disable")
                failures = repo.failures()
                self.assertIn("unreachable statement count increased: 0 -> 2", failures["tests/test_example.py"])

    def test_strengthening_and_unchanged_dead_code_pass(self) -> None:
        dead = TEST_MODULE + "        return\n        self.fail('dead')\n"
        with tempfile.TemporaryDirectory() as directory:
            repo = _Repository(Path(directory), {"tests/test_example.py": dead})
            repo.write({"tests/test_example.py": dead.replace(
                "        self.assertTrue(True)\n", "        self.assertTrue(True)\n        self.assertIn(1, [1])\n", 1)},
                "strengthen")
            # Only this file is judged: without an assurance lock the repin evaluation fails closed.
            self.assertNotIn("tests/test_example.py", repo.failures())

    def test_test_module_moved_out_of_discovery_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = _Repository(Path(directory), {"tests/test_example.py": TEST_MODULE})
            _git(repo.root, "mv", "tests/test_example.py", "tests/example_helpers.py")
            _git(repo.root, "commit", "-qm", "move out of test_*.py discovery")
            failures = repo.failures()
            self.assertIn("protected validation/test source deleted", failures.get("tests/test_example.py", []))

    def test_every_rename_is_judged_under_its_base_identity(self) -> None:
        # A rename that stays discoverable is also reported as a deletion: similarity-based
        # rename classification is what the move out of discovery hid behind.
        with tempfile.TemporaryDirectory() as directory:
            repo = _Repository(Path(directory), {"tests/test_example.py": TEST_MODULE})
            _git(repo.root, "mv", "tests/test_example.py", "tests/test_renamed.py")
            _git(repo.root, "commit", "-qm", "rename")
            changed = dict((path, status) for status, path in weakening._changed_python(repo.root, repo.base))
            self.assertEqual(changed, {"tests/test_example.py": "D", "tests/test_renamed.py": "A"})


class ConditionalEarlyExitTests(unittest.TestCase):
    """A guarded exit leaves the rest reachable, so the unreachable-statement count cannot see it."""

    def _failures(self, path: str, before: str, after: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            repo = _Repository(Path(directory), {path: before})
            repo.write({path: after}, "change")
            return repo.failures().get(path, [])

    def test_guarded_exit_before_a_tests_assertions_is_rejected(self) -> None:
        guards = (
            "if os.environ.get('CI'):\n            return",
            "if os.environ.get('CI'):\n            self.skipTest('ci')",
            "if os.environ.get('CI'):\n            raise unittest.SkipTest('ci')",
            "if not os.environ.get('CI'):\n            pass\n        else:\n            return",
        )
        for guard in guards:
            with self.subTest(guard=guard):
                after = "import os\n" + TEST_MODULE.replace(
                    "        self.assertEqual", f"        {guard}\n        self.assertEqual", 1)
                self.assertIn("conditional early exit added to T.test_a: 0 -> 1",
                              self._failures("tests/test_example.py", TEST_MODULE, after))

    def test_handler_that_returns_is_rejected(self) -> None:
        after = TEST_MODULE.replace(
            "        self.assertEqual(1, 1)\n        self.assertTrue(True)\n",
            "        try:\n            self.assertEqual(1, 1)\n            self.assertTrue(True)\n"
            "        except AssertionError:\n            return\n", 1)
        self.assertIn("conditional early exit added to T.test_a: 0 -> 1",
                      self._failures("tests/test_example.py", TEST_MODULE, after))

    def test_new_fixture_with_a_guard_is_rejected(self) -> None:
        after = "import os\n" + TEST_MODULE.replace(
            "    def test_a(self):\n",
            "    def setUp(self):\n        if os.environ.get('CI'):\n            self.skipTest('ci')\n\n"
            "    def test_a(self):\n", 1)
        self.assertIn("conditional early exit added to T.setUp: 0 -> 1",
                      self._failures("tests/test_example.py", TEST_MODULE, after))

    def test_guarded_success_exit_in_a_checkers_main_is_rejected(self) -> None:
        for guard in ("return 0", "return", "return False", "raise SystemExit(0)", "raise SystemExit", "sys.exit(0)", "sys.exit()"):
            with self.subTest(guard=guard):
                after = CHECKER.replace(
                    "    errors = []\n", f"    if len(sys.argv) > 5:\n        {guard}\n    errors = []\n", 1)
                self.assertIn("conditional early exit added to main: 0 -> 1",
                              self._failures("tools/check_example.py", CHECKER, after))

    def test_failing_exits_new_tests_and_nested_helpers_pass(self) -> None:
        for guard in ("return 1", "return True", "raise SystemExit(1)", "raise SystemExit('bad input')", "sys.exit('bad input')"):
            with self.subTest(guard=guard):
                after = CHECKER.replace(
                    "    errors = []\n", f"    if len(sys.argv) > 5:\n        {guard}\n    errors = []\n", 1)
                self.assertEqual([], self._failures("tools/check_example.py", CHECKER, after))
        new_test = TEST_MODULE + (
            "\n    def test_b(self):\n        if not os.path.exists('x'):\n            self.skipTest('no x')\n"
            "        self.assertTrue(True)\n")
        self.assertEqual([], self._failures("tests/test_example.py", TEST_MODULE, "import os\n" + new_test))
        nested = TEST_MODULE.replace(
            "        self.assertTrue(True)\n",
            "        def fake(value):\n            if value:\n                return value\n            return None\n"
            "        self.assertTrue(fake(True))\n", 1)
        self.assertEqual([], self._failures("tests/test_example.py", TEST_MODULE, nested))

    def test_existing_guards_are_not_counted_again(self) -> None:
        guarded = "import os\n" + TEST_MODULE.replace(
            "        self.assertEqual", "        if os.environ.get('CI'):\n            return\n        self.assertEqual", 1)
        after = guarded.replace("        self.assertTrue(True)\n", "        self.assertTrue(True)\n        self.assertIn(1, [1])\n", 1)
        self.assertEqual([], self._failures("tests/test_example.py", guarded, after))


if __name__ == "__main__":
    unittest.main()
