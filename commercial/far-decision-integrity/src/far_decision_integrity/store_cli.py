from __future__ import annotations

import argparse
import json
from pathlib import Path

from .store import EvidenceStore, EvidenceStoreError, record_payload

INVALID_INPUT_EXIT = 40
INTEGRITY_FAILURE_EXIT = 41


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-evidence-store")
    parser.add_argument("--database", required=True)
    parser.add_argument("--blob-root", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    put = subparsers.add_parser("put")
    put.add_argument("evidence_directory")
    put.add_argument("--retention-days", type=int)

    get = subparsers.add_parser("get")
    get.add_argument("evidence_id")

    decision = subparsers.add_parser("list-decision")
    decision.add_argument("decision_id")

    verify = subparsers.add_parser("verify")
    verify.add_argument("evidence_id")

    expired = subparsers.add_parser("expired")
    args = parser.parse_args(argv)
    store = EvidenceStore(args.database, args.blob_root)

    try:
        if args.command == "put":
            payload = record_payload(
                store.put_directory(
                    Path(args.evidence_directory),
                    retention_days=args.retention_days,
                )
            )
        elif args.command == "get":
            payload = record_payload(store.get(args.evidence_id))
        elif args.command == "list-decision":
            payload = {
                "records": [record_payload(record) for record in store.list_by_decision(args.decision_id)]
            }
        elif args.command == "verify":
            payload = store.verify(args.evidence_id)
            print(json.dumps(payload, sort_keys=True))
            return 0 if payload["valid"] else INTEGRITY_FAILURE_EXIT
        else:
            payload = {"records": [record_payload(record) for record in store.expired()]}
    except EvidenceStoreError as exc:
        print(json.dumps({"error": str(exc), "status": "invalid"}, sort_keys=True))
        return INVALID_INPUT_EXIT

    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
