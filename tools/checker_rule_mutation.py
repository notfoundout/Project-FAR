#!/usr/bin/env python3
"""Measure whether tests notice when individual checker rules are deleted.

Each single-line `errors.append(...)` style statement in a registered checker is replaced by
`pass`, one at a time, inside a disposable copy of the repository, and the checker's paired
test modules are run. A mutant is killed when those tests fail. The working tree is never
modified. Unlike `far_validation mutations`, which scores fixed source-independent texts
against a static heuristic, every mutant here is derived from the checker's own source.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = re.compile(r"^(\s*)(errors|failures|problems|issues)\.(append|extend)\(.*\)\s*$")

# Governance checkers whose rules must be detectable by their paired tests.
REGISTRY: dict[str, dict[str, object]] = {
    "tools/check_claim_status_ceiling.py": {"tests": ["tests.test_claim_status_ceiling"], "min_kill": 1.0},
    "tools/check_semantic_consistency.py": {"tests": ["tests.test_semantic_consistency"], "min_kill": 1.0},
    "tools/check_governance_register_integrity.py": {"tests": ["tests.test_governance_register_integrity"], "min_kill": 1.0},
    "tools/check_project_far_theory_closure.py": {"tests": ["tests.test_project_far_theory_closure", "tests.test_project_far_theory_closure_rules"], "min_kill": 1.0},
    "tools/check_far_core_v11_formalization.py": {"tests": ["tests.test_far_core_v11_formalization", "tests.test_far_core_v11_formalization_rules"], "min_kill": 1.0},
}


@dataclass
class Mutant:
    checker: str
    line: int
    source: str
    killed: bool


def rule_lines(source: str) -> list[int]:
    return [index for index, line in enumerate(source.split("\n")) if RULE.match(line)]


def mutate(source: str, index: int) -> str:
    lines = source.split("\n")
    match = RULE.match(lines[index])
    if match is None:
        raise ValueError(f"line {index + 1} is not a mutable rule")
    lines[index] = match.group(1) + "pass"
    return "\n".join(lines)


def _copy_repository(destination: Path) -> None:
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".far", "*.pyc")
    shutil.copytree(ROOT, destination, ignore=ignore, dirs_exist_ok=True)


def _tests_pass(root: Path, tests: list[str], timeout: int) -> bool:
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", *tests],
        cwd=root, capture_output=True, text=True, timeout=timeout, check=False,
    )
    return completed.returncode == 0


def run(checkers: list[str], timeout: int = 600) -> dict[str, list[Mutant]]:
    results: dict[str, list[Mutant]] = {}
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "repo"
        _copy_repository(root)
        for checker in checkers:
            tests = list(REGISTRY[checker]["tests"])
            path = root / checker
            original = path.read_text(encoding="utf-8")
            if not _tests_pass(root, tests, timeout):
                raise RuntimeError(f"{checker}: paired tests fail before mutation")
            mutants: list[Mutant] = []
            try:
                for index in rule_lines(original):
                    path.write_text(mutate(original, index), encoding="utf-8")
                    killed = not _tests_pass(root, tests, timeout)
                    mutants.append(Mutant(checker, index + 1, original.split("\n")[index].strip(), killed))
            finally:
                path.write_text(original, encoding="utf-8")
            results[checker] = mutants
    return results


def evaluate(results: dict[str, list[Mutant]]) -> list[str]:
    failures: list[str] = []
    for checker, mutants in results.items():
        if not mutants:
            failures.append(f"{checker}: no mutable rules found; the registry entry is vacuous")
            continue
        score = sum(m.killed for m in mutants) / len(mutants)
        floor = float(REGISTRY[checker]["min_kill"])
        if score < floor:
            failures.append(f"{checker}: kill rate {score:.2f} below floor {floor:.2f}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("checkers", nargs="*", help="registered checker paths (default: all)")
    parser.add_argument("--json", type=Path, help="write the full mutant report here")
    args = parser.parse_args(argv)
    checkers = args.checkers or sorted(REGISTRY)
    unknown = sorted(set(checkers) - set(REGISTRY))
    if unknown:
        parser.error("unregistered checker(s): " + ", ".join(unknown))
    results = run(checkers)
    for checker, mutants in results.items():
        killed = sum(m.killed for m in mutants)
        print(f"{checker}: {killed}/{len(mutants)} rule deletions detected")
        for mutant in mutants:
            if not mutant.killed:
                print(f"  SURVIVED line {mutant.line}: {mutant.source}")
    if args.json:
        args.json.write_text(json.dumps({k: [asdict(m) for m in v] for k, v in results.items()}, indent=2) + "\n", encoding="utf-8")
    failures = evaluate(results)
    for failure in failures:
        print(f"FAIL {failure}")
    print("Result:", "FAIL" if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
