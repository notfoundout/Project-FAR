#!/usr/bin/env python3
"""Entry point for the Presenting FAR adversarial relay.

Subcommands:

    status      print the live noncanonical ledger summary
    freeze      write a campaign manifest pinning the frozen source
    calibrate   run preregistered blind historical calibration cases
    run         continue the investigation from the live ledger
    replay      reconstruct a recorded run from raw evidence, no providers

Nothing here promotes, merges, or mutates canonical theory.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import calibration  # noqa: E402
from far_adversarial.evidence import EvidenceStore, RunRecord  # noqa: E402
from far_adversarial.frozen_source import (  # noqa: E402
    FrozenSource,
    GitFrozenSource,
    SourceIntegrityError,
    load_campaign,
)
from far_adversarial.ledger import Ledger, Target  # noqa: E402
from far_adversarial.orchestrator import Orchestrator, new_run_id  # noqa: E402
from far_adversarial.providers import ClaudeCodeProvider, OpenAIProvider  # noqa: E402
from far_adversarial.replay import replay  # noqa: E402

STATE_ROOT = ROOT / ".far" / "research" / "presenting-far"
LEDGER_PATH = STATE_ROOT / "live-theory-state.json"
EVIDENCE_ROOT = STATE_ROOT / "evidence"
CAMPAIGN_PATH = STATE_ROOT / "campaign.json"


def _make_evidence_loader(source: FrozenSource):
    """Read a target's declared evidence out of the frozen source only.

    The working tree is never consulted. Editing a file mid-campaign cannot
    change what a lane is shown; a path the target did not declare is refused;
    a path missing from the frozen commit is a source-integrity failure.
    """

    def load(target: Target) -> dict[str, str]:
        evidence: dict[str, str] = {}
        for relative in sorted(target.frozen_evidence_paths):
            evidence[relative] = source.read(relative)
        return evidence

    return load


def _sandbox_provider(model: str) -> ClaudeCodeProvider:
    """Claude lane, isolated to the same evidence contract as the GPT lane.

    Outside the repository and with every tool denied, so it cannot auto-load
    project instruction files, session state, or anything else GPT never sees.
    """
    return ClaudeCodeProvider(model=model,
                              sandbox_cwd=tempfile.mkdtemp(prefix="far-lane-"))


def cmd_status(_args) -> int:
    if not LEDGER_PATH.exists():
        print(f"no live ledger at {LEDGER_PATH}")
        return 1
    ledger = Ledger.load(LEDGER_PATH)
    print(f"ledger digest: {ledger.digest()}")
    print(f"targets: {len(ledger.targets)}  issues: {len(ledger.issues)}  "
          f"obligations: {len(ledger.obligations)}  candidates: {len(ledger.candidates)}")
    for tid, target in sorted(ledger.targets.items()):
        live = len(ledger.live_issues_for(tid))
        blocking = len(ledger.blocking_obligations_for(tid))
        flag = "authorized" if target.authorized else "NOT-AUTHORIZED"
        print(f"  {tid:<24} {target.status:<32} live-issues={live} "
              f"blocking-obligations={blocking} {flag}")
        for dep, status, ok in ledger.dependency_report(tid):
            mark = "satisfied" if ok else "UNMET"
            print(f"      needs {dep.target_id} in {sorted(dep.requires)} "
                  f"(is {status}) -> {mark}")
    nxt = ledger.next_target()
    print(f"next dependency-valid target: {nxt.id if nxt else 'NONE'}")
    return 0


def cmd_freeze(args) -> int:
    """Register the campaign source explicitly.

    There is no implicit default. A commit becomes the campaign source only by
    being written here, which is what makes 'the run used HEAD' impossible to
    do by accident.
    """
    if not LEDGER_PATH.exists():
        print(f"no live ledger at {LEDGER_PATH}", file=sys.stderr)
        return 1
    ledger = Ledger.load(LEDGER_PATH)
    declared = sorted({p for t in ledger.targets.values() for p in t.frozen_evidence_paths})
    commit = subprocess.run(["git", "rev-parse", args.commit], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    if commit.returncode != 0:
        print(f"cannot resolve {args.commit!r}", file=sys.stderr)
        return 1
    resolved = commit.stdout.strip()
    source = GitFrozenSource(ROOT, resolved, declared)
    try:
        source.verify()
        for path in declared:
            source.read(path)
    except SourceIntegrityError as exc:
        print(f"SOURCE_INTEGRITY_FAILURE: {exc}", file=sys.stderr)
        return 4
    campaign = {
        "source_kind": "git",
        "source_commit": resolved,
        "source_identity": source.identity(),
        "declared_evidence_paths": declared,
        "registered_at_ref": args.commit,
    }
    CAMPAIGN_PATH.parent.mkdir(parents=True, exist_ok=True)
    CAMPAIGN_PATH.write_text(json.dumps(campaign, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
    print(f"campaign source registered: {source.identity()}")
    print(f"declared evidence paths: {len(declared)}")
    return 0


def cmd_calibrate(args) -> int:
    store = EvidenceStore(EVIDENCE_ROOT)
    provider = _sandbox_provider(args.claude_model)
    case_ids = list(calibration.CASES)
    digest = calibration.preregistration_digest(case_ids)
    print(f"preregistration digest: {digest}")
    results = []
    for cid in case_ids:
        result = calibration.run_case(calibration.CASES[cid], provider, store,
                                      "calibration:no-frozen-source")
        results.append(result)
        verdict = "PASS" if result.passed else "MISS"
        if result.execution_failure:
            verdict = f"EXECUTION_FAILURE:{result.execution_failure}"
        print(f"  {cid}: {verdict} missed_groups={result.missed_groups} "
              f"failure_markers={result.fired_failure_markers}")
    report = calibration.write_report(
        STATE_ROOT / "calibration-report.json", results=results, digest=digest,
        notes=list(args.note or []),
    )
    print(f"report: {report}")
    return 0 if all(r.passed for r in results) else 2


def _load_source() -> tuple[FrozenSource, dict] | None:
    if not CAMPAIGN_PATH.exists():
        print(
            "SOURCE_INTEGRITY_FAILURE: no registered campaign source. "
            "Run 'freeze <commit>' first; the current HEAD is never used implicitly.",
            file=sys.stderr,
        )
        return None
    try:
        return load_campaign(CAMPAIGN_PATH, ROOT)
    except SourceIntegrityError as exc:
        print(f"SOURCE_INTEGRITY_FAILURE: {exc}", file=sys.stderr)
        return None


def cmd_run(args) -> int:
    if not LEDGER_PATH.exists():
        print(f"no live ledger at {LEDGER_PATH}", file=sys.stderr)
        return 1
    loaded = _load_source()
    if loaded is None:
        return 4
    source, _campaign = loaded
    gpt = OpenAIProvider(model=args.gpt_model, require_schema=True)
    ok, why = gpt.available()
    if not ok:
        print(why, file=sys.stderr)
        return 3
    ledger = Ledger.load(LEDGER_PATH)
    baseline_digest = ledger.digest()
    orchestrator = Orchestrator(
        ledger=ledger,
        store=EvidenceStore(EVIDENCE_ROOT),
        claude=_sandbox_provider(args.claude_model),
        gpt=gpt,
        evidence_loader=_make_evidence_loader(source),
        source_freeze=source.identity(),
        max_rounds_per_target=args.max_rounds,
    )
    reports = orchestrator.run(max_targets=args.max_targets)
    for report in reports:
        print(f"{report.stop_reason}: {report.detail} "
              f"(epistemic={report.is_epistemic_stop}, resumable={report.resumable})")
    ledger.save()
    record = orchestrator.run_record(new_run_id(), baseline_digest, reports)
    print(f"run record: {record.save(STATE_ROOT)}")
    return 0


def cmd_replay(args) -> int:
    loaded = _load_source()
    if loaded is None:
        return 4
    source, _campaign = loaded
    record = RunRecord.load(Path(args.run_record))
    baseline = Ledger.load(Path(args.baseline))
    result = replay(
        store=EvidenceStore(EVIDENCE_ROOT),
        record=record,
        baseline_ledger=baseline,
        frozen_source=source,
        evidence_loader=_make_evidence_loader(source),
        max_rounds_per_target=args.max_rounds,
        allow_migration=args.allow_migration,
    )
    print(json.dumps({
        "ok": result.ok,
        "reason": result.reason,
        "expected_digest": result.expected_digest,
        "reconstructed_digest": result.reconstructed_digest,
        "integrity_problems": result.integrity_problems,
    }, indent=2, sort_keys=True))
    return 0 if result.ok else 4


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status").set_defaults(func=cmd_status)

    p_freeze = sub.add_parser("freeze")
    p_freeze.add_argument("commit")
    p_freeze.set_defaults(func=cmd_freeze)

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
    p_replay.add_argument("run_record")
    p_replay.add_argument("baseline")
    p_replay.add_argument("--max-rounds", type=int, default=4)
    p_replay.add_argument("--allow-migration", action="store_true")
    p_replay.set_defaults(func=cmd_replay)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
