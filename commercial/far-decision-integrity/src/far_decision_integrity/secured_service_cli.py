from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .external_identity import HashChainedJSONLExporter
from .oidc import OIDCConfig, OIDCIdentityProvider, OTLPHTTPExporter
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
    parser.add_argument("--identity-config", type=Path, help="JSON OIDC deployment configuration")
    parser.add_argument("--observability-log", type=Path, default=Path("var/far/observability/events.jsonl"))
    parser.add_argument("--otlp-endpoint")
    parser.add_argument("--otlp-header", action="append", default=[], metavar="NAME=VALUE")
    return parser


def _headers(values: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--otlp-header must use NAME=VALUE")
        name, content = value.split("=", 1)
        if not name.strip() or not content:
            raise ValueError("--otlp-header must use non-empty NAME=VALUE")
        headers[name.strip()] = content
    return headers


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    identity_provider = None
    if args.identity_config:
        try:
            payload = json.loads(args.identity_config.read_text(encoding="utf-8"))
            identity_provider = OIDCIdentityProvider(OIDCConfig(**payload))
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            parser.error(f"invalid --identity-config: {exc}")
    try:
        exporters = [HashChainedJSONLExporter(args.observability_log)]
        if args.otlp_endpoint:
            exporters.append(OTLPHTTPExporter(args.otlp_endpoint, headers=_headers(args.otlp_header)))
    except ValueError as exc:
        parser.error(str(exc))
    security = TenantSecurityStore(args.security_db)
    runtime = SecuredRuntime(
        security,
        EvidenceStore(args.evidence_db, args.blob_root),
        args.staging_root,
        OperationsStore(security),
        FixedWindowRateLimiter(args.rate_limit, args.rate_window_seconds),
        RuntimeMetrics(),
        identity_provider,
        tuple(exporters),
    )
    serve_secured(args.host, args.port, runtime)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
