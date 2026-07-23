from __future__ import annotations

import base64
import json
import time
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .external_identity import ExternalIdentityError, IdentityAssertion

OIDC_SCHEMA_VERSION = "far-oidc-jwks/0.1"
OTLP_SCHEMA_VERSION = "far-otlp-export/0.1"


def _b64url(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExternalIdentityError(f"{field} must be a non-empty string")
    return value.strip()


def _default_fetch_json(url: str) -> Mapping[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


@dataclass(frozen=True, slots=True)
class OIDCConfig:
    issuer: str
    audience: str
    tenant_claim: str = "tenant_id"
    scopes_claim: str = "scope"
    subject_claim: str = "sub"
    discovery_url: str | None = None
    max_lifetime_seconds: int = 3600
    clock_skew_seconds: int = 30


class OIDCIdentityProvider:
    """OIDC discovery and RS256 JWKS verification adapter."""

    def __init__(
        self,
        config: OIDCConfig,
        *,
        fetch_json: Callable[[str], Mapping[str, Any]] = _default_fetch_json,
        now: Callable[[], float] = time.time,
    ) -> None:
        if config.max_lifetime_seconds < 1 or config.clock_skew_seconds < 0:
            raise ExternalIdentityError("OIDC lifetime and clock-skew settings are invalid")
        self.config = config
        self.fetch_json = fetch_json
        self.now = now
        self._jwks_uri: str | None = None
        self._keys: dict[str, Mapping[str, Any]] = {}

    def verify(self, token: str) -> IdentityAssertion:
        try:
            encoded_header, encoded_payload, encoded_signature = _text(token, "token").split(".")
            header = json.loads(_b64url(encoded_header))
            payload = json.loads(_b64url(encoded_payload))
            signature = _b64url(encoded_signature)
        except (ValueError, TypeError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ExternalIdentityError("invalid OIDC JWT") from exc
        if header.get("alg") != "RS256":
            raise ExternalIdentityError("OIDC JWT algorithm must be RS256")
        key_id = _text(header.get("kid"), "JWT key id")
        key = self._key(key_id)
        try:
            modulus = int.from_bytes(_b64url(_text(key.get("n"), "JWK modulus")), "big")
            exponent = int.from_bytes(_b64url(_text(key.get("e"), "JWK exponent")), "big")
            public_key = rsa.RSAPublicNumbers(exponent, modulus).public_key()
            public_key.verify(
                signature,
                f"{encoded_header}.{encoded_payload}".encode("ascii"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except Exception as exc:  # cryptography exposes several verification errors
            raise ExternalIdentityError("invalid OIDC JWT signature") from exc
        issuer = _text(payload.get("iss"), "issuer")
        if issuer.rstrip("/") != self.config.issuer.rstrip("/"):
            raise ExternalIdentityError("OIDC issuer mismatch")
        audience = payload.get("aud")
        audiences = [audience] if isinstance(audience, str) else audience
        if not isinstance(audiences, list) or self.config.audience not in audiences:
            raise ExternalIdentityError("OIDC audience mismatch")
        issued_at = int(payload.get("iat"))
        expires_at = int(payload.get("exp"))
        if expires_at - issued_at > self.config.max_lifetime_seconds:
            raise ExternalIdentityError("OIDC token lifetime exceeds provider policy")
        scopes_value = payload.get(self.config.scopes_claim)
        if isinstance(scopes_value, str):
            scopes = tuple(sorted(set(scopes_value.split())))
        elif isinstance(scopes_value, list) and all(isinstance(item, str) for item in scopes_value):
            scopes = tuple(sorted(set(scopes_value)))
        else:
            raise ExternalIdentityError("OIDC scopes claim is invalid")
        assertion = IdentityAssertion(
            issuer=issuer,
            subject=_text(payload.get(self.config.subject_claim), "subject"),
            tenant_id=_text(payload.get(self.config.tenant_claim), "tenant claim"),
            scopes=scopes,
            issued_at=issued_at,
            expires_at=expires_at,
            token_id=_text(payload.get("jti"), "token id"),
        )
        assertion.validate(now=int(self.now()), clock_skew_seconds=self.config.clock_skew_seconds)
        return assertion

    def _key(self, key_id: str) -> Mapping[str, Any]:
        if key_id not in self._keys:
            self._refresh()
        try:
            return self._keys[key_id]
        except KeyError as exc:
            self._refresh()
            try:
                return self._keys[key_id]
            except KeyError as inner:
                raise ExternalIdentityError("OIDC signing key is unavailable") from inner

    def _refresh(self) -> None:
        if self._jwks_uri is None:
            discovery = self.fetch_json(
                self.config.discovery_url
                or self.config.issuer.rstrip("/") + "/.well-known/openid-configuration"
            )
            discovered_issuer = _text(discovery.get("issuer"), "discovered issuer")
            if discovered_issuer.rstrip("/") != self.config.issuer.rstrip("/"):
                raise ExternalIdentityError("OIDC discovery issuer mismatch")
            self._jwks_uri = _text(discovery.get("jwks_uri"), "JWKS URI")
        jwks = self.fetch_json(self._jwks_uri)
        keys = jwks.get("keys")
        if not isinstance(keys, list):
            raise ExternalIdentityError("JWKS keys must be a list")
        self._keys = {
            _text(key.get("kid"), "JWK key id"): key
            for key in keys
            if isinstance(key, Mapping) and key.get("kty") == "RSA" and key.get("use", "sig") == "sig"
        }


class OTLPHTTPExporter:
    """Synchronous OTLP/HTTP JSON log exporter with injectable transport."""

    def __init__(
        self,
        endpoint: str,
        *,
        headers: Mapping[str, str] | None = None,
        service_name: str = "far-secured-service",
        transport: Callable[[str, bytes, Mapping[str, str]], None] | None = None,
    ) -> None:
        self.endpoint = _text(endpoint, "OTLP endpoint")
        self.headers = dict(headers or {})
        self.service_name = _text(service_name, "service name")
        self.transport = transport or self._send

    def emit(self, event_type: str, payload: Mapping[str, Any], *, occurred_at: int | None = None) -> dict[str, Any]:
        timestamp = int(time.time() if occurred_at is None else occurred_at)
        attributes = [{"key": key, "value": {"stringValue": json.dumps(value, sort_keys=True)}} for key, value in sorted(payload.items())]
        envelope = {
            "resourceLogs": [{
                "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": self.service_name}}]},
                "scopeLogs": [{
                    "scope": {"name": "project-far", "version": OTLP_SCHEMA_VERSION},
                    "logRecords": [{
                        "timeUnixNano": str(timestamp * 1_000_000_000),
                        "severityText": "INFO",
                        "body": {"stringValue": _text(event_type, "event_type")},
                        "attributes": attributes,
                    }],
                }],
            }]
        }
        body = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("utf-8")
        headers = {"Content-Type": "application/json", **self.headers}
        self.transport(self.endpoint, body, headers)
        return {"schema_version": OTLP_SCHEMA_VERSION, "event_type": event_type, "bytes": len(body)}

    @staticmethod
    def _send(endpoint: str, body: bytes, headers: Mapping[str, str]) -> None:
        request = urllib.request.Request(endpoint, data=body, headers=dict(headers), method="POST")
        with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310
            if not 200 <= response.status < 300:
                raise ExternalIdentityError(f"OTLP exporter returned HTTP {response.status}")
