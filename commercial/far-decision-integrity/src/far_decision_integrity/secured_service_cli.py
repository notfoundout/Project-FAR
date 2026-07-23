from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .evidence_store import EvidenceStore
from .secured_service import SecuredRuntime, serve_secured
from .security import TenantSecurityStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the secured FAR authorization service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--security-db", type=Path, default=Path("var/far/security.db"))
    parser.add_argument("--evidence-db", type=Path, default=Path("var/far/evidence.db"))
    parser.add_argument("--blob-root", type=Path, default=Path("var/far/blobs"))
    parser.add_argument("--staging-root", type=Path, default=Path("far-evidence/secured-service"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    runtime = SecuredRuntime(
        TenantSecurityStore(args.security_db),
        EvidenceStore(args.evidence_db, args.blob_root),
        args.staging_root,
    )
    serve_secured(args.host, args.port, runtime)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
