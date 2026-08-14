#!/usr/bin/env python3
"""Entry point for the Presenting FAR adversarial relay.

Subcommands:

    status      print the live noncanonical ledger summary
    calibrate   run preregistered blind historical calibration cases
    run         continue the investigation from the live ledger
    replay      reproduce recorded invocations from raw evidence, no providers

Nothing here promotes, merges, or mutates canonical theory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import calibration  # noqa: E402
from far_adversarial.evidence import EvidenceStore  # noqa: E402
from far_adversarial.ledger import Ledger, Target  # noqa: E402
from far_adversarial.orchestrator import Orchestrator, replay_run  # noqa: E402
from far_adversarial.providers import ClaudeCodeProvider, OpenAIProvider  # noqa: E402

STATE_ROOT = ROOT / ".far" / "research" / "presenting-far"
LEDGER_PATH = STATE_ROOT / "live-theory-state.json"
EVIDENCE_ROOT = STATE_ROOT / "evidence"


def _source_freeze() -> str:
    import subprocess

    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
            check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


def _evidence_loader(target: Target) -> dict[str, str]:
    """Load the eligible frozen evidence for a target.

    Every path is declared in the ledger and resolved under the repository
    root; a target cannot reach outside it.
    """
    from far_adversarial.safety import resolve_within

    evidence: dict[str, str] = {}
    for relative in target.source_dependencies:
        if not relative.startswith(("docs/", "theory/", "frameworks/", "foundations/",
                                    ".far/")):
            continue
        try:
            path = resolve_within(ROOT, relative)
        except ValueError:
            continue
        if path.is_file():
            evidence[relative] = path.read_text(encoding="utf-8", errors="replace")
    return evidence


def cmd_status(_args) -> int:
    if not LEDGER_PATH.exists():
        print(f"no live ledger at {LEDGER_PATH}")
        return 1
    ledger = Ledger.load(LEDGER_PATH)
    print(f"ledger digest: {ledger.digest()}")
    print(f"targets: {len(ledger.targets)}  issues: {len(ledger.issues)}")
    for tid, target in sorted(ledger.targets.items()):
        live = len(ledger.live_issues_for(tid))
        flag = "authorized" if target.authorized else "NOT-AUTHORIZED"
        print(f"  {tid:<24} {target.status:<32} live-issues={live} {flag}")
    nxt = ledger.next_target()
    print(f"next dependency-valid target: {nxt.id if nxt else 'NONE'}")
    return 0


def cmd_calibrate(args) -> int:
    import tempfile

    store = EvidenceStore(EVIDENCE_ROOT)
    # The calibration lane must not be able to reach the repository: the
    # recorded historical answer, the reconstructed ledger, and the graded
    # marker list all live there.
    sandbox = tempfile.mkdtemp(prefix="far-calibration-")
    provider = ClaudeCodeProvider(model=args.claude_model, sandbox_cwd=sandbox)
    case_ids = list(calibration.CASES)
    digest = calibration.preregistration_digest(case_ids)
    print(f"preregistration digest: {digest}")
    results = []
    for cid in case_ids:
        result = calibration.run_case(calibration.CASES[cid], provider, store, _source_freeze())
        results.append(result)
        verdict = "PASS" if result.passed else "MISS"
        if result.execution_failure:
            verdict = f"EXECUTION_FAILURE:{result.execution_failure}"
        print(f"  {cid}: {verdict} missed_groups={result.missed_groups} "
              f"failure_markers={result.fired_failure_markers}")
    report = calibration.write_report(
        STATE_ROOT / "calibration-report.json",
        results=results,
        digest=digest,
        notes=list(args.note or []),
    )
    print(f"report: {report}")
    return 0 if all(r.passed for r in results) else 2


def cmd_run(args) -> int:
    if not LEDGER_PATH.exists():
        print(f"no live ledger at {LEDGER_PATH}", file=sys.stderr)
        return 1
    ledger = Ledger.load(LEDGER_PATH)
    gpt = OpenAIProvider(model=args.gpt_model)
    ok, why = gpt.available()
    if not ok:
        print(why, file=sys.stderr)
        return 3
    orchestrator = Orchestrator(
        ledger=ledger,
        store=EvidenceStore(EVIDENCE_ROOT),
        claude=ClaudeCodeProvider(model=args.claude_model),
        gpt=gpt,
        evidence_loader=_evidence_loader,
        source_freeze=_source_freeze(),
        max_rounds_per_target=args.max_rounds,
    )
    reports = orchestrator.run(max_targets=args.max_targets)
    for report in reports:
        print(f"{report.stop_reason}: {report.detail} "
              f"(epistemic={report.is_epistemic_stop})")
    ledger.save()
    return 0


def cmd_replay(_args) -> int:
    summary = replay_run(EvidenceStore(EVIDENCE_ROOT))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["replayable"] else 4


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    p_cal = sub.add_parser("calibrate")
    p_cal.add_argument("--claude-model", default="claude-opus-5")
    p_cal.add_argument("--note", action="append")
    p_cal.set_defaults(func=cmd_calibrate)

    p_run = sub.add_parser("run")
    p_run.add_argument("--claude-model", default="claude-opus-5")
    p_run.add_argument("--gpt-model", default="gpt-5")
    p_run.add_argument("--max-rounds", type=int, default=4)
    p_run.add_argument("--max-targets", type=int, default=8)
    p_run.set_defaults(func=cmd_run)

    p_replay = sub.add_parser("replay")
    p_replay.set_defaults(func=cmd_replay)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
