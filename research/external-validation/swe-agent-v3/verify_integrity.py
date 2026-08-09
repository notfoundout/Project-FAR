"""Compatibility wrapper that extends FAR-SWE-V3-001 integrity with additive prospective contracts.

The legacy implementation remains the semantic authority for the frozen base
contract. This wrapper adds the prospective classification-input contract and
binds delegated checks to the caller's active verification context without
leaking fixture state into later validations.
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


def _push_legacy_context():
    """Temporarily bind legacy checks to the wrapper's active context."""
    prior = (
        _legacy.ROOT,
        _legacy.HERE,
        _legacy.MANIFEST,
        _legacy._committed_blob_bytes,
        _legacy.REQUIRED_ARTIFACTS,
    )
    _legacy.ROOT = ROOT
    _legacy.HERE = HERE
    _legacy.MANIFEST = MANIFEST
    _legacy._committed_blob_bytes = _committed_blob_bytes
    _legacy.REQUIRED_ARTIFACTS = REQUIRED_ARTIFACTS
    return prior


def _pop_legacy_context(prior) -> None:
    (
        _legacy.ROOT,
        _legacy.HERE,
        _legacy.MANIFEST,
        _legacy._committed_blob_bytes,
        _legacy.REQUIRED_ARTIFACTS,
    ) = prior


def verify_manifest():
    prior = _push_legacy_context()
    try:
        index = _legacy_verify_manifest()
        try:
            import verify_review_closure_hardened as hardening
        except ImportError as exc:
            raise DesignError("mandatory additive review-closure hardening is unavailable") from exc
        hardening.validate(here=HERE)
        return index
    finally:
        _pop_legacy_context(prior)


def verify_byte_policy() -> None:
    prior = _push_legacy_context()
    try:
        _legacy_verify_byte_policy()
    finally:
        _pop_legacy_context(prior)
