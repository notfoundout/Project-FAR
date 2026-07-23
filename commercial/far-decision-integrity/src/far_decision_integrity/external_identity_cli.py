from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .external_identity import (
    EnvironmentSecretProvider,
    ExternalIdentityError,
    HMACIdentityProvider,
    HashChainedJSONLExporter,
    assertion_payload,
)

INVALID_INPUT_EXIT = 40
VERIFY_FAILURE_EXIT = 41


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far-external-identity")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify-token")
    verify.add_argument("token")
    verify.add_argument("--issuer", required=True)
    verify.add_argument("--secret-prefix", default="FAR_SECRET_")
    verify.add_argument("--max-lifetime-seconds", type=int, default=3600)

    emit = subparsers.add_parser("emit-event")
    emit.add_argument("--log", type=Path, required=True)
    emit.add_argument("--event-type", required=True)
    emit.add_argument("--payload", required=True, help="JSON object")

    check = subparsers.add_parser("verify-log")
    check.add_argument("log", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "verify-token":
            provider = EnvironmentSecretProvider(args.secret_prefix)
            assertion = HMACIdentityProvider(
                args.issuer,
                provider.get,
                max_lifetime_seconds=args.max_lifetime_seconds,
            ).verify(args.token)
            payload = assertion_payload(assertion)
        elif args.command == "emit-event":
            decoded = json.loads(args.payload)
            if not isinstance(decoded, dict):
                raise ExternalIdentityError("event payload must be a JSON object")
            payload = HashChainedJSONLExporter(args.log).emit(args.event_type, decoded)
        else:
            payload = HashChainedJSONLExporter(args.log).verify()
            print(json.dumps(payload, sort_keys=True))
            return 0 if payload["valid"] else VERIFY_FAILURE_EXIT
    except (ExternalIdentityError, json.JSONDecodeError, OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, sort_keys=True))
        return INVALID_INPUT_EXIT
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
