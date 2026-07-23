from __future__ import annotations

import base64
import json
import tempfile
import time
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from far_decision_integrity.external_identity import ExternalIdentityError
from far_decision_integrity.oidc import OIDCConfig, OIDCIdentityProvider, OTLPHTTPExporter
from far_decision_integrity.secured_service import SecuredRuntime
from far_decision_integrity.security import TenantSecurityStore
from far_decision_integrity.store import EvidenceStore


def b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def jwt(private_key: rsa.RSAPrivateKey, payload: dict[str, object], kid: str = "key-1") -> str:
    header = b64(json.dumps({"alg": "RS256", "kid": kid, "typ": "JWT"}, separators=(",", ":")).encode())
    body = b64(json.dumps(payload, separators=(",", ":")).encode())
    signature = private_key.sign(f"{header}.{body}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{header}.{body}.{b64(signature)}"


class OIDCTest(unittest.TestCase):
    def setUp(self) -> None:
        self.now = int(time.time())
        self.private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        numbers = self.private.public_key().public_numbers()
        self.jwk = {
            "kty": "RSA", "use": "sig", "kid": "key-1",
            "n": b64(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")),
            "e": b64(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")),
        }
        self.responses = {
            "https://issuer.example/.well-known/openid-configuration": {
                "issuer": "https://issuer.example", "jwks_uri": "https://issuer.example/jwks"
            },
            "https://issuer.example/jwks": {"keys": [self.jwk]},
        }
        self.provider = OIDCIdentityProvider(
            OIDCConfig("https://issuer.example", "far-api"),
            fetch_json=lambda url: self.responses[url],
            now=lambda: self.now,
        )

    def token(self, **changes: object) -> str:
        payload: dict[str, object] = {
            "iss": "https://issuer.example", "aud": "far-api", "sub": "operator-1",
            "tenant_id": "tenant-a", "scope": "authorize policy:read", "iat": self.now,
            "exp": self.now + 300, "jti": "token-1",
        }
        payload.update(changes)
        return jwt(self.private, payload)

    def test_verifies_rs256_jwks_and_maps_principal(self) -> None:
        assertion = self.provider.verify(self.token())
        self.assertEqual(assertion.tenant_id, "tenant-a")
        self.assertEqual(assertion.principal().key_id, "https://issuer.example:operator-1")
        self.assertIn("authorize", assertion.scopes)

    def test_rejects_audience_signature_and_lifetime(self) -> None:
        with self.assertRaises(ExternalIdentityError):
            self.provider.verify(self.token(aud="other"))
        other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with self.assertRaises(ExternalIdentityError):
            self.provider.verify(jwt(other, json.loads(base64.urlsafe_b64decode(self.token().split('.')[1] + '=='))))
        with self.assertRaises(ExternalIdentityError):
            self.provider.verify(self.token(exp=self.now + 7200))

    def test_secured_runtime_uses_external_provider(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = SecuredRuntime(
                TenantSecurityStore(root / "security.db"),
                EvidenceStore(root / "evidence.db", root / "blobs"),
                root / "staging",
                identity_provider=self.provider,
            )
            principal = runtime.authenticate("Bearer " + self.token(), "authorize")
            self.assertEqual(principal.tenant_id, "tenant-a")


class OTLPTest(unittest.TestCase):
    def test_emits_otlp_http_json(self) -> None:
        captured: list[tuple[str, bytes, dict[str, str]]] = []
        exporter = OTLPHTTPExporter(
            "https://collector.example/v1/logs",
            headers={"Authorization": "Bearer collector"},
            transport=lambda endpoint, body, headers: captured.append((endpoint, body, dict(headers))),
        )
        result = exporter.emit("authorization.completed", {"tenant_id": "tenant-a", "disposition": "allow"}, occurred_at=10)
        endpoint, body, headers = captured[0]
        payload = json.loads(body)
        record = payload["resourceLogs"][0]["scopeLogs"][0]["logRecords"][0]
        self.assertEqual(endpoint, "https://collector.example/v1/logs")
        self.assertEqual(record["body"]["stringValue"], "authorization.completed")
        self.assertEqual(record["timeUnixNano"], "10000000000")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertGreater(result["bytes"], 0)


if __name__ == "__main__":
    unittest.main()
