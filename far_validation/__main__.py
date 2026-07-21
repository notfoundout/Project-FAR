from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .certificate import main as certificate_main
from .diagnostics import format_diagnosis, load_latest
from .engine import ValidationEngine, ValidationEngineError, format_text
from .formal_model import main as formal_main
from .manifest import ManifestError
from .mutations import main as mutations_main
from .oracle import main as oracle_main
from .trust import HMACTrust, TrustError
from .weakening import main as weakening_main


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
    validate.add_argument("--trace-dependencies", action="store_true")
    validate.add_argument("--require-trace", action="store_true")
    validate.add_argument("--require-signed-cache", action="store_true")
    validate.add_argument("--format", choices=("text", "json"), default="text")

    diagnose = subparsers.add_parser("diagnose", help="explain the most recent failures")
    diagnose.add_argument("failure_code", nargs="?")

    oracle = subparsers.add_parser("oracle", help="independently validate every legacy checker")
    oracle.add_argument("--execute", action="store_true")
    oracle.add_argument("--json", action="store_true")

    mutations = subparsers.add_parser("mutations", help="run the complete registered hostile-acceptance campaign")
    mutations.add_argument("--json", action="store_true")
    mutations.add_argument("--report", type=Path)

    weakening = subparsers.add_parser("weakening", help="detect deleted or weakened tests and validators")
    weakening.add_argument("--base")
    weakening.add_argument("--json", action="store_true")

    formal = subparsers.add_parser("formal", help="model-check the abstract validation engine")
    formal.add_argument("--max-checks", type=int, default=4)
    formal.add_argument("--json", action="store_true")

    certificate = subparsers.add_parser("certificate", help="create or verify signed validation certificates")
    certificate.add_argument("action", choices=("create", "verify"))
    certificate.add_argument("--run", type=Path)
    certificate.add_argument("--certificate", type=Path)
    certificate.add_argument("--expected-commit")
    certificate.add_argument("--expected-tree")
    certificate.add_argument("--require-signed", action="store_true")
    certificate.add_argument("--required-check", action="append", default=[])
    certificate.add_argument("--required-evidence", action="append", default=[])

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
        if command == "oracle":
            delegated = ["--root", str(root)]
            if args.execute:
                delegated.append("--execute")
            if args.json:
                delegated.append("--json")
            return oracle_main(delegated)
        if command == "mutations":
            delegated = ["--root", str(root)]
            if args.json:
                delegated.append("--json")
            if args.report:
                delegated.extend(["--report", str(args.report)])
            return mutations_main(delegated)
        if command == "weakening":
            delegated = ["--root", str(root)]
            if args.base:
                delegated.extend(["--base", args.base])
            if args.json:
                delegated.append("--json")
            return weakening_main(delegated)
        if command == "formal":
            delegated = ["--max-checks", str(args.max_checks)]
            if args.json:
                delegated.append("--json")
            return formal_main(delegated)
        if command == "certificate":
            delegated = [args.action, "--root", str(root)]
            for option, value in (
                ("--run", args.run),
                ("--certificate", args.certificate),
                ("--expected-commit", args.expected_commit),
                ("--expected-tree", args.expected_tree),
            ):
                if value:
                    delegated.extend([option, str(value)])
            if args.require_signed:
                delegated.append("--require-signed")
            for check_id in args.required_check:
                delegated.extend(["--required-check", check_id])
            for evidence_id in args.required_evidence:
                delegated.extend(["--required-evidence", evidence_id])
            return certificate_main(delegated)

        trust = HMACTrust.from_environment(
            require_signature=getattr(args, "require_signed_cache", False)
        )
        engine = ValidationEngine(
            root=root,
            jobs=getattr(args, "jobs", None),
            use_cache=not getattr(args, "no_cache", False),
            trace_dependencies=getattr(args, "trace_dependencies", False),
            require_trace_backend=getattr(args, "require_trace", False),
            require_signed_cache=getattr(args, "require_signed_cache", False),
            trust=trust,
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
    except (ManifestError, ValidationEngineError, FileNotFoundError, TrustError) as exc:
        print(f"FAR-VAL-ENGINE-001: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
