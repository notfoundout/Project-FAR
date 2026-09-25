"""Checkers that validate with bare `assert` must refuse to run under `python -O`.

`python -O` (or PYTHONOPTIMIZE) strips assert statements, so an assert-based checker would
print PASS without checking anything; for example a claim promotion in a frozen result passed
tools/check_usd_w1_semantic_change.py under -O before the guard existed.
"""
from __future__ import annotations

import ast
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Protected governance checker; its guard is prepared in the pending integration patches and
# lands only after the security/bootstrap task reconciles protected files.
PENDING_PROTECTED = {"tools/check_s_core_w4.py"}


def assert_checkers() -> list[Path]:
    found = []
    for path in sorted((ROOT / "tools").glob("check_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            found.append(path)
    return found


def has_module_guard(tree: ast.Module) -> bool:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return False
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.UnaryOp)
            and isinstance(node.test.op, ast.Not)
            and isinstance(node.test.operand, ast.Name)
            and node.test.operand.id == "__debug__"
            and any(isinstance(item, ast.Raise) for item in node.body)
        ):
            return True
    return False


class CheckerOptimizationGuardTest(unittest.TestCase):
    def test_assert_based_checkers_exist(self):
        self.assertGreater(len(assert_checkers()), 40)

    def test_every_assert_based_checker_guards_before_its_logic(self):
        missing = [
            path.relative_to(ROOT).as_posix()
            for path in assert_checkers()
            if path.relative_to(ROOT).as_posix() not in PENDING_PROTECTED
            and not has_module_guard(ast.parse(path.read_text(encoding="utf-8")))
        ]
        self.assertEqual([], missing)

    def test_guarded_checkers_fail_closed_under_optimization(self):
        failures = []
        for path in assert_checkers():
            relative = path.relative_to(ROOT).as_posix()
            if relative in PENDING_PROTECTED:
                continue
            completed = subprocess.run([sys.executable, "-O", relative], cwd=ROOT, capture_output=True, text=True, timeout=120)
            if completed.returncode == 0 or "refusing to run under python -O" not in completed.stdout + completed.stderr:
                failures.append(relative)
        self.assertEqual([], failures)

    def test_pending_list_names_real_assert_checkers(self):
        names = {path.relative_to(ROOT).as_posix() for path in assert_checkers()}
        self.assertLessEqual(PENDING_PROTECTED, names)


if __name__ == "__main__":
    unittest.main()
