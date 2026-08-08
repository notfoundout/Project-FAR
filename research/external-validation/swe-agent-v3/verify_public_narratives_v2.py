"""Current complete public-narrative oracle for FAR-SWE-V3-001.

Version 2 preserves the legacy exact per-run evidence section while retaining the
stronger repository-prohibition and launch-binding prose in the remainder of the
plan. Equality remains whole-document exact; this is not a substring validator.
"""
from __future__ import annotations

from pathlib import Path

import verify_public_narratives as base

HERE = Path(__file__).resolve().parent
NarrativeError = base.NarrativeError

OLD_EVIDENCE_PREFIX = '''## Evidence bundle per run

Every attempted run must retain immutable, hash-addressed copies of:

- task identity under sealed mapping, including the frozen task-manifest strata classification;
- frozen task-manifest Git blob identity and frozen sealed identity-ledger Git blob identity;
- retained task-population repository-prohibition audit report root;
- authoritative repository provider identity, canonical repository URL, exact commit, GitHub fork-source repository ID or null, and treatment-material audit result as reconstructed from the sealed identity ledger by the independent identity auditor;
- environment image digest and dependency lock;
- model provider, endpoint, model version, parameters, and provider request identifier;
- all system, agent, task, capsule, and tool instructions;
- capsule or placebo manifest and mount path;
- randomization position and repetition;
- stdout, stderr, ordered trajectory, commands, tool calls, model messages, timestamps, token usage, budget state, and cost;
- workspace status before and after the run;
- patch, prediction, changed-file inventory, internal exit status, outer exit status, and terminal reason;
- target, neighboring, regression, and hidden-grader results;
- grader version, grader logs, adjudication record, and final outcome;
- the critical-harm evaluation inputs and exact results required by `critical-harm-thresholds-v1.0.json`;
- bundle manifest and content-root digest.

Outer process success cannot override an inner execution failure. `budget_exhausted` is distinct from `resolved`. Missing required evidence makes the run `invalid`, never `resolved`.

'''

CURRENT_EVIDENCE_PREFIX = '''## Evidence bundle per run

Every attempted run must retain immutable, hash-addressed copies of:

- task identity under sealed mapping, including the frozen task-manifest strata classification;
- frozen task-manifest Git blob identity and frozen sealed identity-ledger Git blob identity;
- authoritative repository provider identity, canonical repository URL, and exact commit as reconstructed from the sealed identity ledger by the independent identity auditor;
- environment image digest and dependency lock;
- model provider, endpoint, model version, parameters, and provider request identifier;
- all system, agent, task, capsule, and tool instructions;
- capsule or placebo manifest and mount path;
- randomization position and repetition;
- stdout, stderr, ordered trajectory, commands, tool calls, model messages, timestamps, token usage, budget state, and cost;
- workspace status before and after the run;
- patch, prediction, changed-file inventory, internal exit status, outer exit status, and terminal reason;
- target, neighboring, regression, and hidden-grader results;
- grader version, grader logs, adjudication record, and final outcome;
- the critical-harm evaluation inputs and exact results required by `critical-harm-thresholds-v1.0.json`;
- bundle manifest and content-root digest.

Outer process success cannot override an inner execution failure. `budget_exhausted` is distinct from `resolved`. Missing required evidence makes the run `invalid`, never `resolved`.

'''

if base.EXPECTED_EVIDENCE_PLAN.count(OLD_EVIDENCE_PREFIX) != 1:
    raise RuntimeError("base public-narrative oracle does not contain the expected predecessor evidence section exactly once")

EXPECTED = dict(base.EXPECTED)
EXPECTED["evidence-and-analysis-plan-v1.0.md"] = base.EXPECTED_EVIDENCE_PLAN.replace(
    OLD_EVIDENCE_PREFIX, CURRENT_EVIDENCE_PREFIX, 1
)


def verify(here: Path = HERE) -> None:
    for name, expected in EXPECTED.items():
        path = here / name
        if path.is_symlink() or not path.is_file():
            raise NarrativeError(f"regular public narrative required: {name}")
        try:
            actual = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise NarrativeError(f"public narrative must be UTF-8: {name}") from exc
        if actual != expected:
            raise NarrativeError(f"complete public narrative contract drifted: {name}")


if __name__ == "__main__":
    try:
        verify()
    except NarrativeError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: all current FAR-SWE-V3-001 public narrative surfaces match their complete semantic oracles.")
