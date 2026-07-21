from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .diagnostics import format_diagnosis, load_latest
from .engine import ValidationEngine, ValidationEngineError, format_text
from .manifest import ManifestError


def repository_root() -> Path:
    return Path.cwd()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far", description="Project FAR validation platform")
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate", help="run registered validation checks")
    validate.add_argument("checks", nargs="*", help="specific check IDs")
    validate.add_argument("--profile", default="pr-fast")
    validate.add_argument("--changed", metavar="BASE", help="run affected checks against BASE")
    validate.add_argument("--no-cache", action="store_true")
    validate.add_argument("--jobs", type=int, default=None)
    validate.add_argument("--explain", action="store_true")
    validate.add_argument("--continue-after-failure", action="store_true")
    validate.add_argument("--format", choices=("text", "json"), default="text")

    diagnose = subparsers.add_parser("diagnose", help="explain the most recent failures")
    diagnose.add_argument("failure_code", nargs="?")

    subparsers.add_parser("doctor", help="verify the local validation environment")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = (args.root or repository_root()).resolve()
    command = args.command or "validate"
    try:
        if command == "diagnose":
            payload = load_latest(root)
            print(format_diagnosis(payload, args.failure_code))
            return 0
        engine = ValidationEngine(
            root=root,
            jobs=getattr(args, "jobs", None),
            use_cache=not getattr(args, "no_cache", False),
        )
        if command == "doctor":
            summary = engine.run(check_ids=["environment.doctor"], profile="doctor")
        else:
            summary = engine.run(
                profile=args.profile,
                check_ids=args.checks or None,
                changed_base=args.changed,
                explain=args.explain,
                continue_after_failure=args.continue_after_failure,
            )
        if getattr(args, "format", "text") == "json":
            print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_text(summary))
        return 0 if summary.successful else 1
    except (ManifestError, ValidationEngineError, FileNotFoundError) as exc:
        print(f"FAR-VAL-ENGINE-001: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
