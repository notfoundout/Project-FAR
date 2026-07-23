from __future__ import annotations

import argparse
import json
from pathlib import Path

from .operations import OperationsError, OperationsStore, audit_payload, create_backup, verify_backup
from .security import SecurityError, TenantSecurityStore

INVALID_INPUT_EXIT = 40
VERIFY_FAILURE_EXIT = 41


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far-operations")
    parser.add_argument("--security-db", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    rotate = subparsers.add_parser("rotate-key")
    rotate.add_argument("--token", required=True)
    rotate.add_argument("--old-key-id", required=True)
    rotate.add_argument("--new-key-id", required=True)
    rotate.add_argument("--new-secret", required=True)
    rotate.add_argument("--scope", action="append", required=True)

    revoke = subparsers.add_parser("revoke-key")
    revoke.add_argument("--token", required=True)
    revoke.add_argument("--key-id", required=True)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--token", required=True)
    audit.add_argument("--limit", type=int, default=100)

    backup = subparsers.add_parser("backup")
    backup.add_argument("--evidence-db", type=Path, required=True)
    backup.add_argument("--blob-root", type=Path, required=True)
    backup.add_argument("--output", type=Path, required=True)

    verify = subparsers.add_parser("verify-backup")
    verify.add_argument("directory", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "backup":
            payload = create_backup(args.security_db, args.evidence_db, args.blob_root, args.output)
        elif args.command == "verify-backup":
            payload = verify_backup(args.directory)
            print(json.dumps(payload, sort_keys=True))
            return 0 if payload["valid"] else VERIFY_FAILURE_EXIT
        else:
            security = TenantSecurityStore(args.security_db)
            actor = security.authenticate(args.token)
            operations = OperationsStore(security)
            if args.command == "rotate-key":
                payload = audit_payload(
                    operations.rotate_key(
                        actor,
                        args.old_key_id,
                        args.new_key_id,
                        args.new_secret,
                        tuple(args.scope),
                    )
                )
            elif args.command == "revoke-key":
                payload = audit_payload(operations.revoke_key(actor, args.key_id))
            else:
                payload = {"records": [audit_payload(record) for record in operations.audit_log(actor, limit=args.limit)]}
    except (OperationsError, SecurityError, OSError) as exc:
        print(json.dumps({"error": str(exc), "status": "invalid"}, sort_keys=True))
        return INVALID_INPUT_EXIT
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
