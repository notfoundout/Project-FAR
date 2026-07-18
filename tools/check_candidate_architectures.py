#!/usr/bin/env python3
"""Validate architecture-neutral research and candidate registry invariants."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/candidate-architecture-registry.json"
CLAIMS = ROOT / "theory/evaluation/central-claim-registry.json"
REQUIRED = [
    ROOT / "docs/governance/research-architecture.md",
    ROOT / "docs/governance/candidate-architecture-standard-v1.0.md",
    ROOT / "docs/architecture/architecture-neutral-research-engine-blueprint.md",
    ROOT / "docs/planning/architecture-neutral-research-roadmap.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"candidate-architecture check failed: {message}")


def main() -> None:
    for path in REQUIRED:
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    statuses = set(data.get("allowed_statuses", []))
    if data.get("project", {}).get("candidate") is not False:
        fail("Project FAR must not be registered as a candidate")

    candidates = data.get("candidates", [])
    keys: set[tuple[str, str]] = set()
    fara = None
    for candidate in candidates:
        key = (candidate.get("id", ""), candidate.get("version", ""))
        if not all(key):
            fail("candidate id and version are required")
        if key in keys:
            fail(f"duplicate candidate id/version: {key}")
        keys.add(key)
        if candidate.get("status") not in statuses:
            fail(f"invalid status for {key}: {candidate.get('status')}")
        if candidate.get("id") == "FARA":
            fara = candidate

    if fara is None:
        fail("FARA must be registered")
    forbidden = {"established", "proven", "confirmed", "universal", "minimal", "necessary", "uniquely-optimal"}
    for claim, value in fara.get("claim_status", {}).items():
        normalized = str(value).lower()
        if claim in {"universality", "necessity", "minimality", "comparative_economy", "independent_replication"}:
            if normalized in forbidden or normalized.startswith("established"):
                fail(f"FARA claim exceeds current gates: {claim}={value}")

    if data.get("blinding_constraints", {}).get("cre004_candidate_identity_key_exposed") is not False:
        fail("CRE-004 candidate identity key must remain unexposed")

    blueprint = REQUIRED[2].read_text(encoding="utf-8")
    independent_pos = blueprint.find("Independent reasoning-domain specification")
    fara_pos = blueprint.find("FARA enters only as one candidate")
    if independent_pos < 0 or fara_pos < 0:
        fail("blueprint must preserve the independent-domain/FARA boundary")

    if not CLAIMS.is_file():
        fail("central claim registry is missing")

    print("candidate-architecture check: PASS")


if __name__ == "__main__":
    main()
