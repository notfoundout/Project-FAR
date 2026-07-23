from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SECURITY_SCHEMA_VERSION = "far-tenant-security/0.1"
POLICY_SCHEMA_VERSION = "far-policy-registry/0.1"


class SecurityError(ValueError):
    """Raised when authentication, authorization, or policy resolution fails."""


@dataclass(frozen=True, slots=True)
class Principal:
    tenant_id: str
    key_id: str
    scopes: tuple[str, ...]

    def require(self, scope: str) -> None:
        if scope not in self.scopes:
            raise SecurityError(f"principal lacks required scope {scope!r}")


@dataclass(frozen=True, slots=True)
class PolicyRecord:
    tenant_id: str
    policy_id: str
    version: str
    sha256: str
    payload: dict[str, Any]
    active: bool


class TenantSecurityStore:
    def __init__(self, database: str | Path) -> None:
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def register_key(self, tenant_id: str, key_id: str, secret: str, scopes: tuple[str, ...]) -> None:
        tenant_id = _text(tenant_id, "tenant_id")
        key_id = _text(key_id, "key_id")
        secret = _text(secret, "secret")
        normalized_scopes = tuple(sorted({_text(scope, "scope") for scope in scopes}))
        if not normalized_scopes:
            raise SecurityError("at least one scope is required")
        digest = _secret_digest(secret)
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO api_keys (tenant_id, key_id, secret_sha256, scopes_json, enabled) VALUES (?, ?, ?, ?, 1)",
                    (tenant_id, key_id, digest, json.dumps(normalized_scopes)),
                )
        except sqlite3.IntegrityError as exc:
            raise SecurityError(f"key {tenant_id!r}/{key_id!r} already exists") from exc

    def authenticate(self, bearer_token: str) -> Principal:
        token = _text(bearer_token, "bearer_token")
        if "." not in token:
            raise SecurityError("bearer token must have key_id.secret form")
        key_id, secret = token.split(".", 1)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT tenant_id, secret_sha256, scopes_json FROM api_keys WHERE key_id = ? AND enabled = 1",
                (key_id,),
            ).fetchall()
        matches = [row for row in rows if hmac.compare_digest(row[1], _secret_digest(secret))]
        if len(matches) != 1:
            raise SecurityError("invalid bearer token")
        tenant_id, _, scopes_json = matches[0]
        return Principal(tenant_id=tenant_id, key_id=key_id, scopes=tuple(json.loads(scopes_json)))

    def register_policy(
        self,
        principal: Principal,
        policy_id: str,
        version: str,
        payload: dict[str, Any],
        *,
        activate: bool = False,
    ) -> PolicyRecord:
        principal.require("policy:write")
        policy_id = _text(policy_id, "policy_id")
        version = _text(version, "version")
        if not isinstance(payload, dict) or not payload:
            raise SecurityError("policy payload must be a non-empty object")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        try:
            with self._connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                if activate:
                    connection.execute(
                        "UPDATE policies SET active = 0 WHERE tenant_id = ? AND policy_id = ?",
                        (principal.tenant_id, policy_id),
                    )
                connection.execute(
                    "INSERT INTO policies (tenant_id, policy_id, version, sha256, payload_json, active) VALUES (?, ?, ?, ?, ?, ?)",
                    (principal.tenant_id, policy_id, version, digest, canonical, int(activate)),
                )
        except sqlite3.IntegrityError as exc:
            raise SecurityError(
                f"policy {principal.tenant_id!r}/{policy_id!r}/{version!r} already exists"
            ) from exc
        return PolicyRecord(principal.tenant_id, policy_id, version, digest, payload, activate)

    def resolve_policy(self, principal: Principal, policy_id: str, version: str | None = None) -> PolicyRecord:
        principal.require("policy:read")
        policy_id = _text(policy_id, "policy_id")
        with self._connect() as connection:
            if version is None:
                row = connection.execute(
                    "SELECT tenant_id, policy_id, version, sha256, payload_json, active FROM policies WHERE tenant_id = ? AND policy_id = ? AND active = 1",
                    (principal.tenant_id, policy_id),
                ).fetchone()
            else:
                row = connection.execute(
                    "SELECT tenant_id, policy_id, version, sha256, payload_json, active FROM policies WHERE tenant_id = ? AND policy_id = ? AND version = ?",
                    (principal.tenant_id, policy_id, _text(version, "version")),
                ).fetchone()
        if row is None:
            raise SecurityError("policy not found for authenticated tenant")
        return PolicyRecord(row[0], row[1], row[2], row[3], json.loads(row[4]), bool(row[5]))

    def activate_policy(self, principal: Principal, policy_id: str, version: str) -> PolicyRecord:
        principal.require("policy:write")
        record = self.resolve_policy(
            Principal(principal.tenant_id, principal.key_id, tuple(set(principal.scopes) | {"policy:read"})),
            policy_id,
            version,
        )
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "UPDATE policies SET active = 0 WHERE tenant_id = ? AND policy_id = ?",
                (principal.tenant_id, policy_id),
            )
            connection.execute(
                "UPDATE policies SET active = 1 WHERE tenant_id = ? AND policy_id = ? AND version = ?",
                (principal.tenant_id, policy_id, version),
            )
        return PolicyRecord(record.tenant_id, record.policy_id, record.version, record.sha256, record.payload, True)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS api_keys (
                    tenant_id TEXT NOT NULL,
                    key_id TEXT NOT NULL,
                    secret_sha256 TEXT NOT NULL,
                    scopes_json TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    PRIMARY KEY (tenant_id, key_id)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS policies (
                    tenant_id TEXT NOT NULL,
                    policy_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    active INTEGER NOT NULL,
                    PRIMARY KEY (tenant_id, policy_id, version),
                    UNIQUE (tenant_id, policy_id, sha256)
                )
                """
            )
            connection.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_one_active_policy ON policies(tenant_id, policy_id) WHERE active = 1"
            )


def tenant_evidence_id(tenant_id: str, evidence_id: str) -> str:
    tenant = _text(tenant_id, "tenant_id")
    evidence = _text(evidence_id, "evidence_id")
    digest = hashlib.sha256(f"{tenant}\0{evidence}".encode("utf-8")).hexdigest()[:16]
    return f"{tenant}-{digest}-{evidence}"


def _secret_digest(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SecurityError(f"{field} must be a non-empty string")
    return value.strip()
