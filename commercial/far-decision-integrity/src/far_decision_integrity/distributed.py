from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol, Sequence

DISTRIBUTED_SCHEMA_VERSION = "far-distributed-runtime/0.1"


class DistributedRuntimeError(ValueError):
    """Raised when distributed persistence or coordination cannot be completed safely."""


class SQLConnection(Protocol):
    def execute(self, query: str, parameters: Sequence[Any] = ()) -> Any: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...


class ObjectTransport(Protocol):
    def put(self, key: str, body: bytes, metadata: Mapping[str, str]) -> None: ...
    def get(self, key: str) -> tuple[bytes, Mapping[str, str]]: ...
    def delete(self, key: str) -> None: ...


class CounterBackend(Protocol):
    def increment(self, key: str, *, expires_at: int) -> int: ...


@dataclass(frozen=True, slots=True)
class DistributedEvidenceRecord:
    tenant_id: str
    evidence_id: str
    decision_id: str
    manifest_sha256: str
    object_prefix: str
    created_at: int


class PostgreSQLMetadataStore:
    """DB-API compatible PostgreSQL metadata adapter.

    The connection factory is injected so tests do not require a running database and
    deployments can choose psycopg connection policy, pooling, and TLS configuration.
    """

    MIGRATIONS = (
        """CREATE TABLE IF NOT EXISTS far_schema_migrations (
            component TEXT NOT NULL, version INTEGER NOT NULL,
            applied_at BIGINT NOT NULL, PRIMARY KEY (component, version))""",
        """CREATE TABLE IF NOT EXISTS far_evidence_records (
            tenant_id TEXT NOT NULL, evidence_id TEXT NOT NULL,
            decision_id TEXT NOT NULL, manifest_sha256 TEXT NOT NULL,
            object_prefix TEXT NOT NULL, created_at BIGINT NOT NULL,
            PRIMARY KEY (tenant_id, evidence_id))""",
        "CREATE INDEX IF NOT EXISTS idx_far_evidence_decision ON far_evidence_records(tenant_id, decision_id)",
    )

    def __init__(self, connection_factory: Callable[[], SQLConnection]) -> None:
        self.connection_factory = connection_factory

    def migrate(self, *, now: int | None = None) -> dict[str, Any]:
        connection = self.connection_factory()
        applied: list[int] = []
        try:
            for version, statement in enumerate(self.MIGRATIONS, start=1):
                connection.execute(statement)
                marker = connection.execute(
                    "SELECT 1 FROM far_schema_migrations WHERE component = %s AND version = %s",
                    (DISTRIBUTED_SCHEMA_VERSION, version),
                )
                exists = bool(getattr(marker, "fetchone", lambda: None)())
                if not exists:
                    connection.execute(
                        "INSERT INTO far_schema_migrations(component, version, applied_at) VALUES (%s, %s, %s)",
                        (DISTRIBUTED_SCHEMA_VERSION, version, int(time.time() if now is None else now)),
                    )
                    applied.append(version)
            connection.commit()
        except Exception as exc:
            connection.rollback()
            raise DistributedRuntimeError(f"metadata migration failed: {exc}") from exc
        finally:
            connection.close()
        return {"schema_version": DISTRIBUTED_SCHEMA_VERSION, "applied": applied}

    def put(self, record: DistributedEvidenceRecord) -> DistributedEvidenceRecord:
        _validate_record(record)
        connection = self.connection_factory()
        try:
            cursor = connection.execute(
                "SELECT decision_id, manifest_sha256, object_prefix, created_at FROM far_evidence_records WHERE tenant_id = %s AND evidence_id = %s FOR UPDATE",
                (record.tenant_id, record.evidence_id),
            )
            existing = getattr(cursor, "fetchone", lambda: None)()
            if existing is not None:
                candidate = DistributedEvidenceRecord(
                    record.tenant_id, record.evidence_id, existing[0], existing[1], existing[2], int(existing[3])
                )
                if candidate != record:
                    raise DistributedRuntimeError("evidence identity already exists with different metadata")
                connection.commit()
                return candidate
            connection.execute(
                "INSERT INTO far_evidence_records(tenant_id, evidence_id, decision_id, manifest_sha256, object_prefix, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                (record.tenant_id, record.evidence_id, record.decision_id, record.manifest_sha256, record.object_prefix, record.created_at),
            )
            connection.commit()
            return record
        except DistributedRuntimeError:
            connection.rollback()
            raise
        except Exception as exc:
            connection.rollback()
            raise DistributedRuntimeError(f"metadata write failed: {exc}") from exc
        finally:
            connection.close()


class VerifiedObjectStore:
    def __init__(self, transport: ObjectTransport, *, prefix: str = "far") -> None:
        self.transport = transport
        self.prefix = prefix.strip("/")
        if not self.prefix:
            raise DistributedRuntimeError("object prefix must be non-empty")

    def put(self, tenant_id: str, evidence_id: str, files: Mapping[str, bytes]) -> dict[str, Any]:
        tenant = _text(tenant_id, "tenant_id")
        evidence = _text(evidence_id, "evidence_id")
        if not files:
            raise DistributedRuntimeError("at least one object is required")
        digests: dict[str, str] = {}
        for name, body in sorted(files.items()):
            if not isinstance(name, str) or not name or "/" in name or ".." in name:
                raise DistributedRuntimeError("object names must be simple file names")
            if not isinstance(body, bytes):
                raise DistributedRuntimeError("object bodies must be bytes")
            digest = hashlib.sha256(body).hexdigest()
            key = f"{self.prefix}/{tenant}/{evidence}/{name}"
            self.transport.put(key, body, {"sha256": digest})
            stored, metadata = self.transport.get(key)
            if stored != body or metadata.get("sha256") != digest:
                raise DistributedRuntimeError(f"object verification failed for {name!r}")
            digests[name] = digest
        canonical = json.dumps(digests, sort_keys=True, separators=(",", ":")).encode()
        return {
            "schema_version": DISTRIBUTED_SCHEMA_VERSION,
            "object_prefix": f"{self.prefix}/{tenant}/{evidence}",
            "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
            "files": digests,
        }


class SharedFixedWindowRateLimiter:
    def __init__(self, backend: CounterBackend, limit: int, window_seconds: int, *, now: Callable[[], float] = time.time) -> None:
        if limit < 1 or window_seconds < 1:
            raise DistributedRuntimeError("positive rate limit and window are required")
        self.backend = backend
        self.limit = limit
        self.window_seconds = window_seconds
        self.now = now

    def allow(self, principal_key: str) -> bool:
        principal = _text(principal_key, "principal_key")
        current = int(self.now())
        window = current // self.window_seconds
        expires_at = (window + 1) * self.window_seconds
        count = self.backend.increment(f"far:rate:{principal}:{window}", expires_at=expires_at)
        if not isinstance(count, int) or count < 1:
            raise DistributedRuntimeError("counter backend returned an invalid value")
        return count <= self.limit


def distributed_readiness(metadata_probe: Callable[[], bool], object_probe: Callable[[], bool], counter_probe: Callable[[], bool]) -> dict[str, Any]:
    checks = {
        "metadata": bool(metadata_probe()),
        "object_storage": bool(object_probe()),
        "coordination": bool(counter_probe()),
    }
    return {"schema_version": DISTRIBUTED_SCHEMA_VERSION, "ready": all(checks.values()), "checks": checks}


def _validate_record(record: DistributedEvidenceRecord) -> None:
    for field in (record.tenant_id, record.evidence_id, record.decision_id, record.object_prefix):
        _text(field, "record field")
    if len(record.manifest_sha256) != 64 or any(character not in "0123456789abcdef" for character in record.manifest_sha256):
        raise DistributedRuntimeError("manifest_sha256 must be lowercase SHA-256 hex")
    if record.created_at < 0:
        raise DistributedRuntimeError("created_at must be non-negative")


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DistributedRuntimeError(f"{field} must be a non-empty string")
    return value.strip()
