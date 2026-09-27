#!/usr/bin/env python3
"""Protection audit for the owner-operated protected-repin gate.

This wrapper changes only audit semantics. Operational evaluation continues through
``repin_gate_app.py`` unchanged.

By default the audit is the bound-state audit: ``protected-repin-gate`` must be a required check
bound exactly to the dedicated App, the checks must be strict, administrator enforcement must be
on, and force pushes and deletion must be off. That is ``repin_gate_app.check_protection``.

``--bootstrap`` selects the bootstrap audit, for the period before the owner binds the App check
(the first bootstrap, or a rotation to a new App). It accepts the absence of that context while
still enforcing strict status checks, administrator enforcement, no force pushes, and no branch
deletion. If any ``protected-repin-gate`` context is already present, it must be bound exactly to
the dedicated App ID; a same-named check from another source is rejected.

The bootstrap audit used to be the only mode. Once the App check was bound it could no longer
detect that check being removed, because it accepts the check's absence.
"""
from __future__ import annotations

import argparse

try:
    from . import repin_gate_app as gate_app
except ImportError:  # Executed directly from the deployment checkout.
    import repin_gate_app as gate_app


def phase_aware_check_protection(protection: dict, app_id: int) -> list[str]:
    """Validate baseline protection and, when present, the App-bound gate check."""
    problems: list[str] = []
    checks = protection.get("required_status_checks") or {}
    ours = [c for c in checks.get("checks", []) if c.get("context") == gate_app.CHECK_NAME]

    if ours and ours != [{"context": gate_app.CHECK_NAME, "app_id": app_id}]:
        problems.append(
            "protected-repin-gate, when present, must be bound exactly to "
            f"app_id {app_id}; found {ours}"
        )
    if checks.get("strict") is not True:
        problems.append("required status checks must be strict (branches up to date before merging)")
    if not (protection.get("enforce_admins") or {}).get("enabled"):
        problems.append("enforce_admins must be enabled")
    if (protection.get("allow_force_pushes") or {}).get("enabled"):
        problems.append("force pushes must be disabled")
    if (protection.get("allow_deletions") or {}).get("enabled"):
        problems.append("branch deletion must be disabled")
    return problems


bound_check_protection = gate_app.check_protection


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit main's protection for the protected-repin gate")
    parser.add_argument("--bootstrap", action="store_true",
                        help="accept an unbound protected-repin-gate context (before the owner binds the App check)")
    args = parser.parse_args(argv)
    gate_app.check_protection = phase_aware_check_protection if args.bootstrap else bound_check_protection
    return gate_app.run_actions("audit")


if __name__ == "__main__":
    raise SystemExit(main())
