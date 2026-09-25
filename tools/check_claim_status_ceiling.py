#!/usr/bin/env python3
"""Reject promotion of central claims above their governed status ceilings.

`central-claim-registry.json` declares `update_policy.stronger_status_requires_linked_artifacts`,
but no field in the registry links artifacts to a status, so that policy cannot be checked
from the registry alone. This checker makes promotion fail closed instead: every registered
claim has a ceiling here, a status may equal or fall below its ceiling (demotion is always
allowed), and raising a ceiling is a reviewed code change naming its authorizing record.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"

# Support rank of each registered status. Rank 0 carries no positive support.
STATUS_RANK = {
    "refuted": 0,
    "weakened": 0,
    "not_established": 0,
    "not_established_generally": 0,
    "unresolved": 0,
    "partially_supported": 1,
    "supported_at_registered_control_scope": 2,
    "supported": 3,
}

# Governed ceilings, equal to the statuses on main when this checker was introduced.
# Raising a ceiling requires an authorizing governance record; name it in the same change.
CEILINGS = {
    "CLM-REP-CAPACITY": "partially_supported",
    "CLM-UNIVERSAL-STRUCTURE": "unresolved",
    "CLM-EXISTENCE": "unresolved",
    "CLM-SUFFICIENCY": "partially_supported",
    "CLM-UNIVERSALITY": "not_established",
    "CLM-NECESSITY": "not_established",
    "CLM-MINIMALITY": "not_established",
    "CLM-NONTRIVIALITY": "supported_at_registered_control_scope",
    "CLM-ECONOMY": "not_established",
    "CLM-INDEPENDENCE": "not_established_generally",
}


def validate(data: dict | None = None) -> list[str]:
    if data is None:
        data = json.loads(CLAIMS.read_text(encoding="utf-8"))
    errors: list[str] = []
    claims = data.get("claims")
    if not isinstance(claims, list):
        return ["central claim registry requires a claims list"]
    seen: set[str] = set()
    for claim in claims:
        cid = claim.get("id")
        status = claim.get("current_status")
        if cid in seen:
            errors.append(f"duplicate claim id: {cid}")
        seen.add(cid)
        if cid not in CEILINGS:
            errors.append(f"{cid}: no governed status ceiling; register one before adding the claim")
            continue
        if status not in STATUS_RANK:
            errors.append(f"{cid}: unranked status {status!r}")
            continue
        ceiling = CEILINGS[cid]
        if STATUS_RANK[status] > STATUS_RANK[ceiling]:
            errors.append(f"{cid}: status {status!r} exceeds governed ceiling {ceiling!r}")
        scope = claim.get("maximum_supported_scope")
        if isinstance(scope, str) and scope.strip().lower().startswith("none") and STATUS_RANK[status] > 0:
            errors.append(f"{cid}: positive status {status!r} with no supported scope")
    if missing := sorted(set(CEILINGS) - seen):
        errors.append("claims removed from registry: " + ", ".join(missing))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("claim status ceiling: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"claim status ceiling: PASS ({len(CEILINGS)} claims at or below governed ceilings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
