#!/usr/bin/env python3
"""Canonical Project FAR unittest runner."""
from __future__ import annotations

import argparse
import importlib.util
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class DiagnosticTextTestResult(unittest.TextTestResult):
    """Collect and print complete, test-addressable failure diagnostics."""

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        super().addFailure(test, err)
        self._print_structured_problem("FAILURE", test, err)

    def addError(self, test: unittest.case.TestCase, err) -> None:
        super().addError(test, err)
        self._print_structured_problem("ERROR", test, err)

    def _print_structured_problem(self, kind: str, test: unittest.case.TestCase, err) -> None:
        test_id = test.id()
        traceback_text = self._exc_info_to_string(err, test).rstrip()
        self.stream.writeln()
        self.stream.writeln(f"PROJECT_FAR_TEST_{kind}")
        self.stream.writeln(f"test: {test_id}")
        self.stream.writeln(f"location: {test_id.rsplit('.', 2)[0]}")
        self.stream.writeln("details:")
        for line in traceback_text.splitlines():
            self.stream.writeln(f"  {line}")
        self.stream.writeln(f"END_PROJECT_FAR_TEST_{kind}")


class DiagnosticTextTestRunner(unittest.TextTestRunner):
    resultclass = DiagnosticTextTestResult


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
    parser.add_argument(
        "--fast",
        action="store_true",
        help="reserved for future slow-test exclusion; currently runs the full test suite",
    )
    parser.parse_args(argv)
    suite = discover_suite()
    total = count_tests(suite)
    print(f"Project FAR test discovery: {total} tests")
    if total == 0:
        print("PROJECT FAR TESTS FAILED: zero tests discovered", file=sys.stderr)
        return 1
    start = time.monotonic()
    result = DiagnosticTextTestRunner(verbosity=2, buffer=False).run(suite)
    elapsed = time.monotonic() - start
    print(f"Project FAR tests run: {result.testsRun} in {elapsed:.3f}s")
    if result.testsRun == 0:
        print("PROJECT FAR TESTS FAILED: zero tests executed", file=sys.stderr)
        return 1
    if not result.wasSuccessful():
        print("PROJECT FAR TEST FAILURE SUMMARY", file=sys.stderr)
        print(f"failures: {len(result.failures)}", file=sys.stderr)
        print(f"errors: {len(result.errors)}", file=sys.stderr)
        print(f"skipped: {len(result.skipped)}", file=sys.stderr)
        for kind, entries in (("FAILURE", result.failures), ("ERROR", result.errors)):
            for test, traceback_text in entries:
                print(f"{kind}: {test.id()}", file=sys.stderr)
                print(traceback_text.rstrip(), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
