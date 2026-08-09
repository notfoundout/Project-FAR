"""Compatibility wrapper that extends FAR-SWE-V3-001 integrity with additive prospective contracts.

The legacy implementation remains the semantic authority for the frozen base
contract.  This wrapper adds the prospective classification-input contract and,
critically, synchronizes the active verification context before delegating so
fixture/mutation verification cannot accidentally read the real checkout.
"""
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
_legacy_verify_manifest = _legacy.verify_manifest
_legacy_verify_byte_policy = _legacy.verify_byte_policy


def _sync_legacy_context() -> None:
    """Bind delegated checks to this wrapper's current verification context.

    Tests and callers intentionally replace ROOT/HERE/MANIFEST and the committed
    blob reader to exercise mutations.  Re-exported legacy functions retain the
    legacy module's globals, so failing to synchronize them makes a mutation
    test inspect the repository checkout instead of the supplied fixture.
    """
    _legacy.ROOT = ROOT
    _legacy.HERE = HERE
    _legacy.MANIFEST = MANIFEST
    _legacy._committed_blob_bytes = _committed_blob_bytes
    _legacy.REQUIRED_ARTIFACTS = REQUIRED_ARTIFACTS


def verify_manifest():
    _sync_legacy_context()
    index = _legacy_verify_manifest()
    try:
        import verify_review_closure_hardened as hardening
    except ImportError as exc:
        raise DesignError("mandatory additive review-closure hardening is unavailable") from exc
    hardening.validate()
    return index


def verify_byte_policy() -> None:
    _sync_legacy_context()
    _legacy_verify_byte_policy()
