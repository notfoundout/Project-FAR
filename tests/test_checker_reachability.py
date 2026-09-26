"""Every tools/check_*.py must be reached by something that runs or imports it.

An unreferenced checker gives no assurance and can rot unnoticed: before this test, eleven
UPP checkers failed on main while no Makefile target, manifest check, workflow, health list,
test, or other tool invoked them.
"""
from __future__ import annotations

import ast
import fnmatch
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOB = re.compile(r"check_[A-Za-z0-9_]*\*[A-Za-z0-9_*]*\.py")


def reference_texts() -> dict[str, str]:
    sources = [ROOT / "Makefile", ROOT / "validation/manifest.json"]
    sources += sorted((ROOT / ".github/workflows").glob("*.yml"))
    sources += sorted((ROOT / "tests").rglob("*.py"))
    sources += sorted((ROOT / "tools").glob("*.py"))
    sources += sorted((ROOT / "far_validation").glob("*.py"))
    return {path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8") for path in sources if path.is_file()}


def unreached_checkers() -> list[str]:
    texts = reference_texts()
    # Specific globs such as glob("check_upp_w*.py") reach every checker they match. The
    # catch-all "check_*.py" (used by static inventories and by this test) reaches nothing.
    patterns = {match for text in texts.values() for match in GLOB.findall(text)} - {"check_*.py"}
    unreached = []
    for checker in sorted((ROOT / "tools").glob("check_*.py")):
        own = checker.relative_to(ROOT).as_posix()
        name = re.compile(rf"\b{re.escape(checker.stem)}\b")
        if any(name.search(text) for path, text in texts.items() if path != own):
            continue
        if any(fnmatch.fnmatch(checker.name, pattern) for pattern in patterns):
            continue
        unreached.append(own)
    return unreached


SUBPROCESS_CALLS = {"run", "call", "check_call", "check_output", "Popen"}


def subprocess_strings(path: Path) -> set[str]:
    """String constants passed to subprocess calls in `path`."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if name in SUBPROCESS_CALLS:
                found.update(item.value for item in ast.walk(node) if isinstance(item, ast.Constant) and isinstance(item.value, str))
    return found


def mutual_invocations() -> list[tuple[str, str]]:
    """Checker/test pairs that each execute the other in a subprocess, which recurses without bound."""
    pairs = []
    for checker in sorted((ROOT / "tools").glob("check_*.py")):
        invoked = " ".join(subprocess_strings(checker))
        for test in sorted((ROOT / "tests").rglob("test_*.py")):
            if test.name in invoked and checker.name in " ".join(subprocess_strings(test)):
                pairs.append((checker.relative_to(ROOT).as_posix(), test.relative_to(ROOT).as_posix()))
    return pairs


class CheckerReachabilityTest(unittest.TestCase):
    def test_every_checker_is_reached(self):
        self.assertEqual([], unreached_checkers())

    def test_no_checker_and_test_invoke_each_other(self):
        self.assertEqual([], mutual_invocations())

    def test_mutual_invocation_detection_is_not_vacuous(self):
        with tempfile.TemporaryDirectory() as directory:
            checker = Path(directory) / "check_x.py"
            checker.write_text('import subprocess, sys\nsubprocess.run([sys.executable, "-m", "unittest", "tests/test_x.py"])\n', encoding="utf-8")
            self.assertIn("tests/test_x.py", subprocess_strings(checker))

    def test_detection_is_not_vacuous(self):
        texts = reference_texts()
        self.assertIn("tools/check_claim_status_ceiling.py", texts)
        orphan = ROOT / "tools/check_claim_status_ceiling.py"
        name = re.compile(rf"\b{orphan.stem}\b")
        referencing = [path for path, text in texts.items() if path != "tools/check_claim_status_ceiling.py" and name.search(text)]
        self.assertTrue(referencing)
        self.assertNotIn("tools/check_claim_status_ceiling.py", unreached_checkers())


if __name__ == "__main__":
    unittest.main()
