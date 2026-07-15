#!/usr/bin/env python3
"""Canonical Project FAR unittest runner."""
from __future__ import annotations
import argparse, importlib.util, sys, time, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def discover_suite(start: Path = TESTS) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for index, path in enumerate(sorted(start.rglob("test_*.py"))):
        module_name = "project_far_test_" + str(index) + "_" + path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot import test module {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def count_tests(suite: unittest.TestSuite) -> int:
    return suite.countTestCases()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all intended Project FAR tests.")
    parser.add_argument("--fast", action="store_true", help="reserved for future slow-test exclusion; currently runs the full test suite")
    args = parser.parse_args(argv)
    suite = discover_suite()
    total = count_tests(suite)
    print(f"Project FAR test discovery: {total} tests")
    if total == 0:
        print("PROJECT FAR TESTS FAILED: zero tests discovered", file=sys.stderr)
        return 1
    start = time.monotonic()
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    elapsed = time.monotonic() - start
    print(f"Project FAR tests run: {result.testsRun} in {elapsed:.3f}s")
    if result.testsRun == 0:
        print("PROJECT FAR TESTS FAILED: zero tests executed", file=sys.stderr)
        return 1
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
