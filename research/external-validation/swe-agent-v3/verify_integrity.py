"""Compatibility wrapper that extends FAR-SWE-V3-001 integrity with additive prospective contracts."""
from __future__ import annotations

import verify_integrity_legacy as _legacy

_CLASSIFICATION_DIGEST_CONTRACT = (
    "research/external-validation/swe-agent-v3/classification-input-digest-contract-v1.0.json"
)
_legacy.REQUIRED_ARTIFACTS = set(_legacy.REQUIRED_ARTIFACTS) | {_CLASSIFICATION_DIGEST_CONTRACT}

for _name, _value in vars(_legacy).items():
    if not _name.startswith("__"):
        globals()[_name] = _value

REQUIRED_ARTIFACTS = _legacy.REQUIRED_ARTIFACTS
