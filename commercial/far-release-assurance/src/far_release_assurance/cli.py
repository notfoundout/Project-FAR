"""Local CLI for FAR release-package operations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .closure import assess_closure
from .compare import compare_releases, comparison_to_dict
from .io import ReleasePackageError, canonical_json, load_package, package_digest, package_to_dict
from .model import Decision
from .report import build_report_bundle, write_report_bundle

GATE_EXIT_CODES = {
    Decision.PASS: 0,
    Decision.REVIEW_REQUIRED: 20,
    Decision.BLOCKED: 30,
    Decision.UNKNOWN: 40,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far-release")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate one release package")
    validate.add_argument("package")

    normalize = subparsers.add_parser("normalize", help="write canonical JSON")
    normalize.add_argument("package")
    normalize.add_argument("--output")

    inventory = subparsers.add_parser("inventory", help="emit machinery inventory and closure")
    inventory.add_argument("package")
    inventory.add_argument("--output")

    digest = subparsers.add_parser("digest", help="emit canonical SHA-256 digest")
    digest.add_argument("package")

    compare = subparsers.add_parser("compare", help="compare baseline and candidate packages")
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--candidate", required=True)
    compare.add_argument("--output")

    report = subparsers.add_parser("report", help="write report.json, report.md, and manifest.json")
    report.add_argument("--baseline", required=True)
    report.add_argument("--candidate", required=True)
    report.add_argument("--output-directory", required=True)

    gate = subparsers.add_parser("gate", help="write a report bundle and exit by FAR decision")
    gate.add_argument("--baseline", required=True)
    gate.add_argument("--candidate", required=True)
    gate.add_argument("--output-directory", required=True)

    return parser


def _write(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command in {"compare", "report", "gate"}:
            baseline = load_package(args.baseline)
            candidate = load_package(args.candidate)
            summary = compare_releases(baseline, candidate)
            if args.command == "compare":
                payload = comparison_to_dict(summary)
                _write(json.dumps(payload, sort_keys=True, indent=2) + "\n", args.output)
                return 0
            bundle = build_report_bundle(baseline, candidate, summary)
            write_report_bundle(bundle, args.output_directory)
            sys.stdout.write(
                f"{args.command.upper()} {candidate.release_id} "
                f"{summary.comparison.decision.value} {args.output_directory}\n"
            )
            if args.command == "gate":
                return GATE_EXIT_CODES[summary.comparison.decision]
            return 0

        package = load_package(args.package)
        if args.command == "validate":
            sys.stdout.write(f"VALID {package.release_id} {package_digest(package)}\n")
            return 0
        if args.command == "normalize":
            _write(canonical_json(package), args.output)
            return 0
        if args.command == "digest":
            sys.stdout.write(package_digest(package) + "\n")
            return 0
        if args.command == "inventory":
            closure = assess_closure(package.machinery, package.decision_roots + package.release_roots)
            payload = {
                "schema_version": "far-machinery-inventory/0.1",
                "release_id": package.release_id,
                "source_commit": package.source_commit,
                "package_digest": package_digest(package),
                "closure": {
                    "status": closure.status.value,
                    "reached": list(closure.reached),
                    "unresolved": list(closure.unresolved),
                    "defects": list(closure.defects),
                    "duplicates": list(closure.duplicates),
                    "undeclared_roots": list(closure.undeclared_roots),
                },
                "machinery": package_to_dict(package)["machinery"],
            }
            _write(json.dumps(payload, sort_keys=True, indent=2) + "\n", args.output)
            return 0
    except ReleasePackageError as exc:
        sys.stderr.write(f"INVALID: {exc}\n")
        return 10
    return 11


if __name__ == "__main__":
    raise SystemExit(main())
