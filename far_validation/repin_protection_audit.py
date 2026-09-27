#!/usr/bin/env python3
"""Bootstrap-safe protection audit for the owner-operated protected-repin gate.

This wrapper changes only audit semantics. Operational evaluation continues through
``repin_gate_app.py`` unchanged.

During the bootstrap sequence, ``protected-repin-gate`` is intentionally not yet a
required check. A baseline audit therefore accepts the absence of that context while
still enforcing the invariants that must already hold: strict status checks,
administrator enforcement, no force pushes, and no branch deletion. If any
``protected-repin-gate`` context is already present, it must be bound exactly to the
dedicated App ID; a same-named check from another source is rejected.

After the owner binds the required App check, the same audit automatically becomes a
bound-state audit because the context is present and must match the dedicated App.
"""
from __future__ import annotations

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


def main() -> int:
    gate_app.check_protection = phase_aware_check_protection
    return gate_app.run_actions("audit")


if __name__ == "__main__":
    raise SystemExit(main())
