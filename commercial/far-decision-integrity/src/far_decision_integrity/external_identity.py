from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Mapping, Protocol

from .security import Principal, SecurityError

EXTERNAL_IDENTITY_SCHEMA_VERSION = "far-external-identity/0.1"
OBSERVABILITY_SCHEMA_VERSION = "far-observability-export/0.1"


class ExternalIdentityError(SecurityError):
    """Raised when external identity, secrets, or observability data is invalid."""


@dataclass(frozen=True, slots=True)
class IdentityAssertion:
    issuer: str
    subject: str
    tenant_id: str
    scopes: tuple[str, ...]
    issued_at: int
    expires_at: int
    token_id: str

    def validate(self, *, now: int | None = None, clock_skew_seconds: int = 30) -> None:
        current = int(time.time() if now is None else now)
        if not self.issuer or not self.subject or not self.tenant_id or not self.token_id:
            raise ExternalIdentityError("identity assertion fields must be non-empty")
        if not self.scopes:
            raise ExternalIdentityError("identity assertion requires at least one scope")
        if self.expires_at <= self.issued_at:
            raise ExternalIdentityError("identity assertion expiry must follow issue time")
        if self.issued_at > current + clock_skew_seconds:
            raise ExternalIdentityError("identity assertion is not yet valid")
        if self.expires_at <= current - clock_skew_seconds:
            raise ExternalIdentityError("identity assertion has expired")

    def principal(self) -> Principal:
        self.validate()
        return Principal(self.tenant_id, f"{self.issuer}:{self.subject}", self.scopes)


class IdentityProvider(Protocol):
    def verify(self, token: str) -> IdentityAssertion: ...


class HMACIdentityProvider:
    """Reference short-lived token adapter for tests and controlled deployments.

    This is not an OIDC implementation. It verifies a compact signed assertion using
    an externally supplied secret resolver.
    """

    def __init__(
        self,
        issuer: str,
        secret_resolver: Callable[[str], str],
        *,
        now: Callable[[], float] = time.time,
        max_lifetime_seconds: int = 3600,
    ) -> None:
        if not issuer.strip() or max_lifetime_seconds < 1:
            raise ExternalIdentityError("issuer and positive max lifetime are required")
        self.issuer = issuer.strip()
        self.secret_resolver = secret_resolver
        self.now = now
        self.max_lifetime_seconds = max_lifetime_seconds

    def issue(
        self,
        *,
        subject: str,
        tenant_id: str,
        scopes: tuple[str, ...],
        lifetime_seconds: int = 300,
        token_id: str,
        key_id: str = "default",
    ) -> str:
        if lifetime_seconds < 1 or lifetime_seconds > self.max_lifetime_seconds:
            raise ExternalIdentityError("token lifetime exceeds provider policy")
        issued = int(self.now())
        payload = {
            "iss": self.issuer,
            "sub": _text(subject, "subject"),
            "tenant": _text(tenant_id, "tenant_id"),
            "scopes": sorted({_text(scope, "scope") for scope in scopes}),
            "iat": issued,
            "exp": issued + lifetime_seconds,
            "jti": _text(token_id, "token_id"),
            "kid": _text(key_id, "key_id"),
        }
        if not payload["scopes"]:
            raise ExternalIdentityError("at least one scope is required")
        encoded = _encode(payload)
        signature = hmac.new(self.secret_resolver(payload["kid"]).encode(), encoded.encode(), hashlib.sha256).hexdigest()
        return f"{encoded}.{signature}"

    def verify(self, token: str) -> IdentityAssertion:
        try:
            encoded, signature = _text(token, "token").rsplit(".", 1)
            payload = json.loads(bytes.fromhex(encoded).decode("utf-8"))
            key_id = _text(payload.get("kid"), "key_id")
            expected = hmac.new(self.secret_resolver(key_id).encode(), encoded.encode(), hashlib.sha256).hexdigest()
        except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
            raise ExternalIdentityError("invalid external identity token") from exc
        if not hmac.compare_digest(signature, expected):
            raise ExternalIdentityError("invalid external identity signature")
        if payload.get("iss") != self.issuer:
            raise ExternalIdentityError("external identity issuer mismatch")
        scopes = payload.get("scopes")
        if not isinstance(scopes, list) or not all(isinstance(scope, str) and scope for scope in scopes):
            raise ExternalIdentityError("external identity scopes are invalid")
        assertion = IdentityAssertion(
            issuer=self.issuer,
            subject=_text(payload.get("sub"), "subject"),
            tenant_id=_text(payload.get("tenant"), "tenant_id"),
            scopes=tuple(sorted(set(scopes))),
            issued_at=int(payload.get("iat")),
            expires_at=int(payload.get("exp")),
            token_id=_text(payload.get("jti"), "token_id"),
        )
        if assertion.expires_at - assertion.issued_at > self.max_lifetime_seconds:
            raise ExternalIdentityError("external identity lifetime exceeds provider policy")
        assertion.validate(now=int(self.now()))
        return assertion


class EnvironmentSecretProvider:
    def __init__(self, prefix: str = "FAR_SECRET_") -> None:
        self.prefix = prefix

    def get(self, key_id: str) -> str:
        name = self.prefix + _text(key_id, "key_id").upper().replace("-", "_")
        value = os.environ.get(name)
        if not value:
            raise ExternalIdentityError(f"secret {name!r} is unavailable")
        return value


class MappingSecretProvider:
    def __init__(self, secrets: Mapping[str, str]) -> None:
        self._secrets = dict(secrets)

    def get(self, key_id: str) -> str:
        try:
            return _text(self._secrets[_text(key_id, "key_id")], "secret")
        except KeyError as exc:
            raise ExternalIdentityError("secret key is unavailable") from exc


class HashChainedJSONLExporter:
    """Append-only durable reference exporter with per-record hash chaining."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def emit(self, event_type: str, payload: Mapping[str, Any], *, occurred_at: int | None = None) -> dict[str, Any]:
        event_type = _text(event_type, "event_type")
        if not isinstance(payload, Mapping):
            raise ExternalIdentityError("observability payload must be a mapping")
        with self._lock:
            previous = self._last_hash()
            event = {
                "schema_version": OBSERVABILITY_SCHEMA_VERSION,
                "event_type": event_type,
                "occurred_at": int(time.time() if occurred_at is None else occurred_at),
                "payload": dict(payload),
                "previous_hash": previous,
            }
            canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
            event["event_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(event, sort_keys=True) + "\n")
            return event

    def verify(self) -> dict[str, Any]:
        previous: str | None = None
        failures: list[int] = []
        count = 0
        if not self.path.exists():
            return {"schema_version": OBSERVABILITY_SCHEMA_VERSION, "valid": True, "records": 0, "failures": []}
        for count, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            try:
                event = json.loads(line)
                claimed = event.pop("event_hash")
                canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
                actual = hashlib.sha256(canonical.encode()).hexdigest()
                if claimed != actual or event.get("previous_hash") != previous:
                    failures.append(count)
                previous = claimed
            except (json.JSONDecodeError, KeyError, TypeError):
                failures.append(count)
        return {"schema_version": OBSERVABILITY_SCHEMA_VERSION, "valid": not failures, "records": count, "failures": failures}

    def _last_hash(self) -> str | None:
        if not self.path.exists():
            return None
        lines = self.path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return None
        try:
            return json.loads(lines[-1])["event_hash"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ExternalIdentityError("existing observability log is corrupt") from exc


def assertion_payload(assertion: IdentityAssertion) -> dict[str, Any]:
    return {"schema_version": EXTERNAL_IDENTITY_SCHEMA_VERSION, **asdict(assertion)}


def _encode(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8").hex()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExternalIdentityError(f"{field} must be a non-empty string")
    return value.strip()
