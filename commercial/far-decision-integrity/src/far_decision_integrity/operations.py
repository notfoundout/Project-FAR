from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Callable

from .security import Principal, SecurityError, TenantSecurityStore

OPERATIONS_SCHEMA_VERSION = "far-production-operations/0.1"


class OperationsError(ValueError):
    """Raised when an administrative or recovery operation fails."""


@dataclass(frozen=True, slots=True)
class AuditRecord:
    sequence: int
    tenant_id: str
    actor_key_id: str
    action: str
    target: str
    detail: dict[str, Any]
    created_unix: int


class OperationsStore:
    def __init__(self, security: TenantSecurityStore) -> None:
        self.security = security
        self.database = security.database
        self._initialize()

    def revoke_key(self, actor: Principal, key_id: str) -> AuditRecord:
        actor.require("keys:write")
        key_id = _text(key_id, "key_id")
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE api_keys SET enabled = 0 WHERE tenant_id = ? AND key_id = ? AND enabled = 1",
                (actor.tenant_id, key_id),
            )
            if cursor.rowcount != 1:
                raise OperationsError("enabled key not found for authenticated tenant")
            return self._audit(connection, actor, "key.revoked", key_id, {})

    def rotate_key(
        self,
        actor: Principal,
        old_key_id: str,
        new_key_id: str,
        new_secret: str,
        scopes: tuple[str, ...],
    ) -> AuditRecord:
        actor.require("keys:write")
        old_key_id = _text(old_key_id, "old_key_id")
        new_key_id = _text(new_key_id, "new_key_id")
        new_secret = _text(new_secret, "new_secret")
        normalized = tuple(sorted({_text(scope, "scope") for scope in scopes}))
        if not normalized:
            raise OperationsError("at least one scope is required")
        digest = hashlib.sha256(new_secret.encode("utf-8")).hexdigest()
        try:
            with self._connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                row = connection.execute(
                    "SELECT enabled FROM api_keys WHERE tenant_id = ? AND key_id = ?",
                    (actor.tenant_id, old_key_id),
                ).fetchone()
                if row is None or not row[0]:
                    raise OperationsError("enabled old key not found for authenticated tenant")
                connection.execute(
                    "INSERT INTO api_keys (tenant_id, key_id, secret_sha256, scopes_json, enabled) VALUES (?, ?, ?, ?, 1)",
                    (actor.tenant_id, new_key_id, digest, json.dumps(normalized)),
                )
                connection.execute(
                    "UPDATE api_keys SET enabled = 0 WHERE tenant_id = ? AND key_id = ?",
                    (actor.tenant_id, old_key_id),
                )
                return self._audit(
                    connection,
                    actor,
                    "key.rotated",
                    old_key_id,
                    {"replacement_key_id": new_key_id, "scopes": list(normalized)},
                )
        except sqlite3.IntegrityError as exc:
            raise OperationsError("replacement key already exists") from exc

    def register_policy(
        self,
        actor: Principal,
        policy_id: str,
        version: str,
        payload: dict[str, Any],
        *,
        activate: bool = False,
    ) -> AuditRecord:
        record = self.security.register_policy(actor, policy_id, version, payload, activate=activate)
        with self._connect() as connection:
            return self._audit(
                connection,
                actor,
                "policy.registered",
                f"{record.policy_id}/{record.version}",
                {"sha256": record.sha256, "active": record.active},
            )

    def activate_policy(self, actor: Principal, policy_id: str, version: str) -> AuditRecord:
        record = self.security.activate_policy(actor, policy_id, version)
        with self._connect() as connection:
            return self._audit(
                connection,
                actor,
                "policy.activated",
                f"{record.policy_id}/{record.version}",
                {"sha256": record.sha256},
            )

    def audit_log(self, actor: Principal, *, limit: int = 100) -> list[AuditRecord]:
        actor.require("audit:read")
        if limit < 1 or limit > 1000:
            raise OperationsError("limit must be between 1 and 1000")
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT sequence, tenant_id, actor_key_id, action, target, detail_json, created_unix "
                "FROM operations_audit WHERE tenant_id = ? ORDER BY sequence DESC LIMIT ?",
                (actor.tenant_id, limit),
            ).fetchall()
        return [AuditRecord(row[0], row[1], row[2], row[3], row[4], json.loads(row[5]), row[6]) for row in rows]

    def _audit(
        self,
        connection: sqlite3.Connection,
        actor: Principal,
        action: str,
        target: str,
        detail: dict[str, Any],
    ) -> AuditRecord:
        created = int(time.time())
        cursor = connection.execute(
            "INSERT INTO operations_audit (tenant_id, actor_key_id, action, target, detail_json, created_unix) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (actor.tenant_id, actor.key_id, action, target, json.dumps(detail, sort_keys=True), created),
        )
        return AuditRecord(cursor.lastrowid, actor.tenant_id, actor.key_id, action, target, detail, created)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS operations_audit (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT NOT NULL,
                    actor_key_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    target TEXT NOT NULL,
                    detail_json TEXT NOT NULL,
                    created_unix INTEGER NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_operations_audit_tenant ON operations_audit(tenant_id, sequence)"
            )


class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, clock: Callable[[], float] = time.time) -> None:
        if limit < 1 or window_seconds < 1:
            raise OperationsError("rate limit and window must be positive")
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self._lock = Lock()
        self._buckets: dict[str, tuple[int, int]] = {}

    def allow(self, key: str) -> bool:
        now = int(self.clock())
        window = now // self.window_seconds
        with self._lock:
            stored_window, count = self._buckets.get(key, (window, 0))
            if stored_window != window:
                stored_window, count = window, 0
            if count >= self.limit:
                self._buckets[key] = (stored_window, count)
                return False
            self._buckets[key] = (stored_window, count + 1)
            return True


class RuntimeMetrics:
    def __init__(self) -> None:
        self._lock = Lock()
        self._counters: dict[str, int] = {}

    def increment(self, name: str, amount: int = 1) -> None:
        if amount < 0:
            raise OperationsError("metric increments must be non-negative")
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            counters = dict(sorted(self._counters.items()))
        return {"schema_version": OPERATIONS_SCHEMA_VERSION, "counters": counters}


def create_backup(
    security_db: str | Path,
    evidence_db: str | Path,
    blob_root: str | Path,
    destination: str | Path,
) -> dict[str, Any]:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    files: dict[str, str] = {}
    for name, source in (("security.db", Path(security_db)), ("evidence.db", Path(evidence_db))):
        if not source.is_file():
            raise OperationsError(f"missing database {source}")
        target = destination / name
        with sqlite3.connect(source) as source_connection, sqlite3.connect(target) as target_connection:
            source_connection.backup(target_connection)
        files[name] = _sha256(target)
    source_blobs = Path(blob_root)
    target_blobs = destination / "blobs"
    if source_blobs.exists():
        shutil.copytree(source_blobs, target_blobs)
        for path in sorted(target_blobs.rglob("*")):
            if path.is_file():
                files[path.relative_to(destination).as_posix()] = _sha256(path)
    manifest = {"schema_version": OPERATIONS_SCHEMA_VERSION, "files": files}
    (destination / "backup-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def verify_backup(directory: str | Path) -> dict[str, Any]:
    directory = Path(directory)
    try:
        manifest = json.loads((directory / "backup-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OperationsError(f"invalid backup manifest: {exc}") from exc
    failures: list[str] = []
    for relative, expected in sorted(manifest.get("files", {}).items()):
        path = directory / relative
        if not path.is_file() or _sha256(path) != expected:
            failures.append(relative)
    for database in ("security.db", "evidence.db"):
        try:
            with sqlite3.connect(directory / database) as connection:
                result = connection.execute("PRAGMA integrity_check").fetchone()
            if result is None or result[0] != "ok":
                failures.append(f"{database}:integrity")
        except sqlite3.DatabaseError:
            failures.append(f"{database}:integrity")
    return {
        "schema_version": OPERATIONS_SCHEMA_VERSION,
        "valid": not failures,
        "failures": sorted(set(failures)),
    }


def audit_payload(record: AuditRecord) -> dict[str, Any]:
    return {"schema_version": OPERATIONS_SCHEMA_VERSION, **asdict(record)}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OperationsError(f"{field} must be a non-empty string")
    return value.strip()
