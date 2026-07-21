from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from far_validation.assured_engine import ValidationEngine
from far_validation.oracle import analyze_checker_path, analyze_checker_source
from far_validation.tracing import (
    RuntimePolicy,
    TraceReport,
    _matches,
    _normalize_observed,
    audit_trace,
    parse_strace,
)
from far_validation.trust import HMACTrust


class TraceContractRegressionTests(unittest.TestCase):
    def test_repository_root_metadata_is_not_a_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIsNone(_normalize_observed(str(root), root, root))

    def test_double_star_glob_matches_zero_nested_directories_and_parents(self) -> None:
        self.assertTrue(_matches("tools/check_one.py", ("tools/**/*.py",)))
        self.assertTrue(_matches("mechanization/model.py", ("mechanization/**/*.py",)))
        self.assertTrue(_matches("tools", ("tools/check_one.py",)))
        self.assertTrue(_matches("README.md", ("**/*",)))

    def test_directory_traversal_metadata_is_not_file_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "secret.txt").write_text("secret\n", encoding="utf-8")
            report = TraceReport(backend="test", reads=["docs", "secret.txt"])
            policy = RuntimePolicy((), (), ("python",), (), True)
            previous = Path.cwd()
            os.chdir(root)
            try:
                audited = audit_trace(
                    report,
                    declared_inputs=(),
                    command=("python", "check.py"),
                    policy=policy,
                    sandbox_copy=False,
                )
            finally:
                os.chdir(previous)
            self.assertEqual(audited.violations, ["undeclared read: secret.txt"])

    def test_process_cwd_tracking_excludes_temporary_child_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            outside = Path(directory) / "child"
            root.mkdir()
            outside.mkdir()
            raw = (
                "100 clone(child_stack=0, flags=SIGCHLD) = 101\n"
                f'101 chdir("{outside}") = 0\n'
                '101 openat(AT_FDCWD, "temporary.txt", O_RDONLY|O_CLOEXEC) = 3\n'
                f'100 openat(AT_FDCWD, "{root / "tracked.txt"}", O_RDONLY|O_CLOEXEC) = 3\n'
                '100 execve("/bin/definitely-missing", ["definitely-missing"], 0x0) = -1 ENOENT\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            self.assertEqual(report.reads, ["tracked.txt"])
            self.assertEqual(report.executables, [])

    def test_runtime_contract_participates_in_selection_and_cache_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "validation").mkdir()
            (root / "check.py").write_text("print('ok')\n", encoding="utf-8")
            extra = root / "extra.txt"
            extra.write_text("one\n", encoding="utf-8")
            manifest = {
                "schema_version": "1.0",
                "profiles": {"pr-fast": ["x"]},
                "protected_checks": [],
                "global_invalidation_paths": [],
                "checks": [{
                    "id": "x",
                    "title": "x",
                    "command": [sys.executable, "check.py"],
                    "profiles": ["pr-fast"],
                    "inputs": ["check.py"],
                }],
            }
            contracts = {
                "schema_version": "1.0",
                "checks": {"x": {"inputs": ["extra.txt"], "outputs": []}},
            }
            (root / "validation" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (root / "validation" / "runtime-dependencies.json").write_text(
                json.dumps(contracts), encoding="utf-8"
            )
            trust = HMACTrust(key=b"shared", trust_domain="test", key_id="test")
            engine = ValidationEngine(root, jobs=1, trust=trust)
            selected, _, fallback, _ = engine._select_changed("pr-fast", ["extra.txt"])
            self.assertEqual(selected, ["x"])
            self.assertFalse(fallback)
            first = engine.run(profile="pr-fast")
            second = engine.run(profile="pr-fast")
            self.assertTrue(first.successful)
            self.assertTrue(second.results[0].cache_hit)
            extra.write_text("two\n", encoding="utf-8")
            third = engine.run(profile="pr-fast")
            self.assertFalse(third.results[0].cache_hit)


class OracleDelegationRegressionTests(unittest.TestCase):
    def test_thin_wrapper_is_evaluated_with_local_delegate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools = root / "tools"
            tools.mkdir()
            (tools / "implementation.py").write_text(
                "from pathlib import Path\n"
                "def validate():\n"
                "    data = Path('evidence.txt').read_text()\n"
                "    if data != 'ok':\n"
                "        raise RuntimeError('bad evidence')\n",
                encoding="utf-8",
            )
            (tools / "check_wrapper.py").write_text(
                "from implementation import validate\n"
                "if __name__ == '__main__':\n"
                "    try:\n"
                "        validate()\n"
                "    except RuntimeError as exc:\n"
                "        raise SystemExit(str(exc))\n",
                encoding="utf-8",
            )
            finding = analyze_checker_path(root, "tools/check_wrapper.py")
            self.assertTrue(finding.accepted, finding.failures)
            self.assertIn("tools/implementation.py", finding.delegated_modules)

    def test_generator_contract_requires_output_but_not_local_failure_branch(self) -> None:
        source = (
            "from pathlib import Path\n"
            "target = Path('generated.txt')\n"
            "if target.exists():\n"
            "    text = target.read_text()\n"
            "else:\n"
            "    text = ''\n"
            "target.write_text(text + 'x')\n"
        )
        finding = analyze_checker_source(source, "generator.py", role="generator")
        self.assertTrue(finding.accepted, finding.failures)
        trivial = analyze_checker_source("print('PASS')\n", "generator.py", role="generator")
        self.assertFalse(trivial.accepted)


if __name__ == "__main__":
    unittest.main()
