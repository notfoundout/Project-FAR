from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from far_decision_integrity.external_identity import (
    EnvironmentSecretProvider,
    ExternalIdentityError,
    HMACIdentityProvider,
    HashChainedJSONLExporter,
    IdentityAssertion,
    MappingSecretProvider,
)


class ExternalIdentityTests(unittest.TestCase):
    def test_short_lived_token_round_trip(self) -> None:
        provider = HMACIdentityProvider("issuer-a", MappingSecretProvider({"k1": "secret"}).get, now=lambda: 1000)
        token = provider.issue(subject="user-1", tenant_id="tenant-a", scopes=("authorize", "policy:read"), lifetime_seconds=60, token_id="jti-1", key_id="k1")
        assertion = provider.verify(token)
        self.assertEqual(assertion.tenant_id, "tenant-a")
        self.assertEqual(assertion.scopes, ("authorize", "policy:read"))
        self.assertEqual(assertion.expires_at, 1060)

    def test_tampered_token_is_rejected(self) -> None:
        provider = HMACIdentityProvider("issuer-a", MappingSecretProvider({"default": "secret"}).get, now=lambda: 1000)
        token = provider.issue(subject="user", tenant_id="tenant", scopes=("authorize",), token_id="jti")
        with self.assertRaises(ExternalIdentityError):
            provider.verify(token[:-1] + ("0" if token[-1] != "0" else "1"))

    def test_expired_token_is_rejected(self) -> None:
        secrets = MappingSecretProvider({"default": "secret"})
        issuer = HMACIdentityProvider("issuer-a", secrets.get, now=lambda: 1000)
        token = issuer.issue(subject="user", tenant_id="tenant", scopes=("authorize",), lifetime_seconds=10, token_id="jti")
        verifier = HMACIdentityProvider("issuer-a", secrets.get, now=lambda: 1100)
        with self.assertRaises(ExternalIdentityError):
            verifier.verify(token)

    def test_assertion_converts_to_existing_principal(self) -> None:
        assertion = IdentityAssertion("issuer", "subject", "tenant", ("authorize",), 1, 4102444800, "jti")
        principal = assertion.principal()
        self.assertEqual(principal.tenant_id, "tenant")
        self.assertEqual(principal.key_id, "issuer:subject")

    def test_environment_secret_provider_is_explicit(self) -> None:
        with patch.dict(os.environ, {"FAR_SECRET_SIGNING_KEY": "value"}, clear=False):
            self.assertEqual(EnvironmentSecretProvider().get("signing-key"), "value")
        with self.assertRaises(ExternalIdentityError):
            EnvironmentSecretProvider("MISSING_").get("key")

    def test_hash_chained_export_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            exporter = HashChainedJSONLExporter(path)
            first = exporter.emit("identity.verified", {"tenant_id": "tenant-a"}, occurred_at=1)
            second = exporter.emit("authorization.completed", {"disposition": "allow"}, occurred_at=2)
            self.assertEqual(second["previous_hash"], first["event_hash"])
            self.assertTrue(exporter.verify()["valid"])
            path.write_text(path.read_text().replace("allow", "block"), encoding="utf-8")
            self.assertFalse(exporter.verify()["valid"])


if __name__ == "__main__":
    unittest.main()
