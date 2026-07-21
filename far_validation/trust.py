from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TRUST_SCHEMA = "far-validation-attestation-v1"


class TrustError(ValueError):
    """Raised when an attestation cannot be trusted."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


@dataclass(frozen=True)
class HMACTrust:
    key: bytes | None
    trust_domain: str
    key_id: str
    require_signature: bool = False

    @classmethod
    def from_environment(
        cls,
        *,
        key_env: str = "FAR_VALIDATION_CACHE_SIGNING_KEY",
        trust_domain_env: str = "FAR_VALIDATION_TRUST_DOMAIN",
        require_signature: bool = False,
    ) -> "HMACTrust":
        raw = os.environ.get(key_env, "")
        key = raw.encode("utf-8") if raw else None
        domain = os.environ.get(trust_domain_env) or (
            f"local:{platform.node()}" if key is None else "project-far-ci"
        )
        key_id = hashlib.sha256(key).hexdigest()[:20] if key else "unsigned-local"
        if require_signature and not key:
            raise TrustError(f"required signing key is missing from {key_env}")
        return cls(key=key, trust_domain=domain, key_id=key_id, require_signature=require_signature)

    @property
    def signed(self) -> bool:
        return self.key is not None

    def envelope(self, kind: str, payload: dict[str, Any], metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        body = {
            "schema": TRUST_SCHEMA,
            "kind": kind,
            "trust_domain": self.trust_domain,
            "key_id": self.key_id,
            "metadata": metadata or {},
            "payload": payload,
        }
        if self.key is None:
            body["signature"] = None
            return body
        body["signature"] = hmac.new(self.key, canonical_json(body), hashlib.sha256).hexdigest()
        return body

    def verify(self, envelope: dict[str, Any], *, kind: str) -> dict[str, Any]:
        if envelope.get("schema") != TRUST_SCHEMA:
            raise TrustError("unsupported attestation schema")
        if envelope.get("kind") != kind:
            raise TrustError(f"attestation kind mismatch: expected {kind!r}")
        if envelope.get("trust_domain") != self.trust_domain:
            raise TrustError("attestation trust domain mismatch")
        signature = envelope.get("signature")
        if signature is None:
            if self.require_signature or self.key is not None:
                raise TrustError("unsigned attestation is not trusted")
            payload = envelope.get("payload")
            if not isinstance(payload, dict):
                raise TrustError("attestation payload must be an object")
            return payload
        if self.key is None:
            raise TrustError("cannot verify signed attestation without a key")
        if envelope.get("key_id") != self.key_id:
            raise TrustError("attestation key identifier mismatch")
        unsigned = dict(envelope)
        unsigned.pop("signature", None)
        expected = hmac.new(self.key, canonical_json(unsigned), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(str(signature), expected):
            raise TrustError("attestation signature mismatch")
        payload = envelope.get("payload")
        if not isinstance(payload, dict):
            raise TrustError("attestation payload must be an object")
        return payload


def write_attestation(
    path: Path,
    *,
    trust: HMACTrust,
    kind: str,
    payload: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    envelope = trust.envelope(kind, payload, metadata)
    path.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")


def read_attestation(path: Path, *, trust: HMACTrust, kind: str) -> dict[str, Any]:
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TrustError(f"cannot load attestation {path}: {exc}") from exc
    if not isinstance(envelope, dict):
        raise TrustError("attestation root must be an object")
    return trust.verify(envelope, kind=kind)
