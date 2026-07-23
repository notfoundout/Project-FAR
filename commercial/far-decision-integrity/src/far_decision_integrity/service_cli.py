from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .service import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the FAR HTTP authorization service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--evidence-root", type=Path, default=Path("far-evidence/service"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not 0 <= args.port <= 65535:
        build_parser().error("--port must be between 0 and 65535")
    serve(args.host, args.port, args.evidence_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
