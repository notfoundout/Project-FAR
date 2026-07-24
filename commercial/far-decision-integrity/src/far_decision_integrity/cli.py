from __future__ import annotations

import argparse
import json

from .adjudicate import adjudicate
from .io import load_package
from .model import IntegrityStatus, PackageValidationError
from .report import report_payload, write_report

EXIT_CODES = {
    IntegrityStatus.JUSTIFIED: 0,
    IntegrityStatus.UNSUPPORTED: 30,
    IntegrityStatus.UNDERDETERMINED: 31,
    IntegrityStatus.UNVERIFIABLE: 32,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-decision")
    parser.add_argument("package")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        result = adjudicate(load_package(args.package))
    except PackageValidationError as exc:
        print(json.dumps({"status": "invalid-package", "error": str(exc)}, sort_keys=True))
        return 40
    if args.output:
        write_report(result, args.output)
    print(json.dumps(report_payload(result), sort_keys=True))
    return EXIT_CODES[result.status]


if __name__ == "__main__":
    raise SystemExit(main())
