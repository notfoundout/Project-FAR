#!/usr/bin/env python3
"""Superseded: branch protection is owner-managed and audited by the protected-repin-gate App.

This tool once wrote `main`'s protection with a repository admin token. The policy it wrote
required only `merge-authority`, so running it now would drop the App-bound
`protected-repin-gate` required check, the repository's only merge authority. Two later
decisions retired that path:

- the administrator token it used was revoked (docs/governance/privileged-token-retirement-2026-09-05.md);
- protection is changed only by the owner, following docs/governance/protected-repin-procedure.md,
  and read back by the App-authored `protected-repin-audit` check.

A locked file cannot be removed through the owner-signed repin gate, so this file stays as an
inert tombstone. It never contacts GitHub and always exits non-zero, so the two disabled legacy
workflows that invoke it fail closed if they are ever re-enabled.
"""
from __future__ import annotations

import sys

MESSAGE = (
    "configure_validation_protection.py is superseded and makes no change. Change main's protection "
    "by hand as described in docs/governance/protected-repin-procedure.md, then verify it with the "
    "protected-repin-audit check or tools/check_validation_protection.py --gate-app-id <App ID>."
)


def main(argv: list[str] | None = None) -> int:
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
