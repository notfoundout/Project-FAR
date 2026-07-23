from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .operations import FixedWindowRateLimiter, OperationsStore, RuntimeMetrics
from .store import EvidenceStore
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
    parser.add_argument("--rate-limit", type=int, default=120)
    parser.add_argument("--rate-window-seconds", type=int, default=60)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    security = TenantSecurityStore(args.security_db)
    runtime = SecuredRuntime(
        security,
        EvidenceStore(args.evidence_db, args.blob_root),
        args.staging_root,
        OperationsStore(security),
        FixedWindowRateLimiter(args.rate_limit, args.rate_window_seconds),
        RuntimeMetrics(),
    )
    serve_secured(args.host, args.port, runtime)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
