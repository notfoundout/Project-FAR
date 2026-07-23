from __future__ import annotations

import argparse
import json

from .adjudicate import adjudicate
from .authorization import EXIT_CODES as AUTHORIZATION_EXIT_CODES
from .authorization import authorize_refund, load_refund_request
from .io import load_package
from .model import IntegrityStatus, PackageValidationError
from .report import report_payload, write_report

ADJUDICATION_EXIT_CODES = {
    IntegrityStatus.JUSTIFIED: 0,
    IntegrityStatus.UNSUPPORTED: 30,
    IntegrityStatus.UNDERDETERMINED: 31,
    IntegrityStatus.UNVERIFIABLE: 32,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-decision")
    subparsers = parser.add_subparsers(dest="command")

    audit = subparsers.add_parser("audit")
    audit.add_argument("package")
    audit.add_argument("--output")

    authorize = subparsers.add_parser("authorize-refund")
    authorize.add_argument("request")
    authorize.add_argument("--output-directory", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "authorize-refund":
            result = authorize_refund(load_refund_request(args.request), args.output_directory)
            print(json.dumps({
                "decision_id": result.adjudication.decision_id,
                "integrity_status": result.adjudication.status.value,
                "disposition": result.disposition,
                "evidence_directory": str(result.evidence_directory),
            }, sort_keys=True))
            return AUTHORIZATION_EXIT_CODES[result.disposition]

        if args.command == "audit":
            result = adjudicate(load_package(args.package))
            if args.output:
                write_report(result, args.output)
            print(json.dumps(report_payload(result), sort_keys=True))
            return ADJUDICATION_EXIT_CODES[result.status]
    except PackageValidationError as exc:
        print(json.dumps({"status": "invalid-package", "error": str(exc)}, sort_keys=True))
        return 40

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
