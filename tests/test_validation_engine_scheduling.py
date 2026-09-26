"""Exhaustive behavioral check of the real ValidationEngine scheduler.

`far_validation/formal_model.py` model-checks its own `simulate()` reimplementation, which the
engine never calls, so it cannot detect a scheduling defect in `engine.py`. This module drives
`ValidationEngine.run` itself over every dependency DAG on up to three checks (edges oriented
by a fixed order, IDs chosen so alphabetical and topological order disagree) and every
pass/fail outcome, observing execution through marker files the check commands write.
"""
from __future__ import annotations

import itertools
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from far_validation.engine import ValidationEngine  # noqa: E402

# Reverse-alphabetical IDs: node 0 must run first but sorts last.
IDS = ("zeta", "mu", "alpha")

COMMAND = (
    "import pathlib, sys\n"
    "deps = {deps!r}\n"
    "missing = [d for d in deps if not pathlib.Path(d).exists()]\n"
    "if missing: sys.exit(3)\n"
    "pathlib.Path({marker!r}).write_text('ran')\n"
    "sys.exit({code})\n"
)


def dags(size: int):
    edges = [(left, right) for left in range(size) for right in range(left + 1, size)]
    for bits in itertools.product((False, True), repeat=len(edges)):
        deps: list[list[int]] = [[] for _ in range(size)]
        for enabled, (left, right) in zip(bits, edges):
            if enabled:
                deps[right].append(left)
        yield deps


class ValidationEngineSchedulingTest(unittest.TestCase):
    def run_case(self, root: Path, deps: list[list[int]], outcomes: tuple[bool, ...]):
        markers = root / "markers"
        markers.mkdir(exist_ok=True)
        for marker in markers.iterdir():
            marker.unlink()
        size = len(deps)
        checks = []
        for index in range(size):
            source = COMMAND.format(
                deps=[str(markers / IDS[d]) for d in deps[index]],
                marker=str(markers / IDS[index]),
                code=0 if outcomes[index] else 1,
            )
            checks.append({
                "id": IDS[index],
                "title": IDS[index],
                "command": [sys.executable, "-c", source],
                "profiles": ["pr-fast"],
                "depends_on": [IDS[d] for d in deps[index]],
                "cacheable": False,
            })
        manifest = {
            "schema_version": "1.0",
            "profiles": {"pr-fast": [IDS[i] for i in range(size)]},
            "protected_checks": [],
            "global_invalidation_paths": ["validation/**"],
            "checks": checks,
        }
        (root / "validation" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        summary = ValidationEngine(root, jobs=2, use_cache=False).run(profile="pr-fast")
        status = {result.check_id: result.status for result in summary.results}
        ran = {path.name for path in markers.iterdir()}
        return summary, status, ran

    def test_scheduler_invariants_hold_for_every_small_dag_and_outcome(self):
        runs = 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "validation").mkdir()
            for size in range(1, len(IDS) + 1):
                for deps in dags(size):
                    for outcomes in itertools.product((False, True), repeat=size):
                        summary, status, ran = self.run_case(root, deps, outcomes)
                        runs += 1
                        context = (deps, outcomes, status)
                        expected: dict[str, str] = {}
                        for index in range(size):
                            if all(expected[IDS[d]] == "passed" for d in deps[index]):
                                expected[IDS[index]] = "passed" if outcomes[index] else "validation_failure"
                            else:
                                expected[IDS[index]] = "blocked_by_root_failure"
                        self.assertEqual(expected, status, context)
                        # A blocked check never executes; every executed check saw its dependencies first
                        # (a dependency that had not run would make it exit 3, i.e. an unexpected failure).
                        self.assertEqual({i for i, s in expected.items() if s != "blocked_by_root_failure"}, ran, context)
                        self.assertEqual(all(s == "passed" for s in expected.values()), summary.successful, context)
        self.assertEqual(2 + 2 * 4 + 8 * 8, runs)


if __name__ == "__main__":
    unittest.main()
