from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

STORE_SCHEMA_VERSION = "far-evidence-store/0.1"
_SELECT = """SELECT evidence_id, decision_id, disposition, input_type,
created_at, retain_until, manifest_sha256, files_json FROM evidence_records"""


class EvidenceStoreError(ValueError):
    """Raised when persistent evidence cannot be stored or verified safely."""


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    decision_id: str
    disposition: str
    input_type: str
    created_at: str
    retain_until: str | None
    manifest_sha256: str
    files: tuple[str, ...]


class EvidenceStore:
    def __init__(self, database: str | Path, blob_root: str | Path) -> None:
        self.database = Path(database)
        self.blob_root = Path(blob_root)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.blob_root.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS evidence_records (
                evidence_id TEXT PRIMARY KEY, decision_id TEXT NOT NULL,
                disposition TEXT NOT NULL, input_type TEXT NOT NULL,
                created_at TEXT NOT NULL, retain_until TEXT,
                manifest_sha256 TEXT NOT NULL, files_json TEXT NOT NULL)""")
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_evidence_decision ON evidence_records(decision_id)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_evidence_retention ON evidence_records(retain_until)"
            )

    def put_directory(
        self,
        evidence_directory: str | Path,
        *,
        retention_days: int | None = None,
        created_at: datetime | None = None,
    ) -> EvidenceRecord:
        source = Path(evidence_directory)
        try:
            manifest_bytes = (source / "manifest.json").read_bytes()
            manifest = json.loads(manifest_bytes)
        except (OSError, json.JSONDecodeError) as exc:
            raise EvidenceStoreError(f"unable to load evidence manifest: {exc}") from exc
        if not isinstance(manifest, dict):
            raise EvidenceStoreError("evidence manifest must be a JSON object")

        evidence_id = _text(manifest, "evidence_id")
        decision_id = _text(manifest, "decision_id")
        disposition = _text(manifest, "disposition")
        input_type = _text(manifest, "input_type")
        file_hashes = manifest.get("files")
        if not isinstance(file_hashes, dict) or not file_hashes:
            raise EvidenceStoreError("manifest files must be a non-empty object")

        blobs: dict[str, bytes] = {}
        for name, expected in sorted(file_hashes.items()):
            if not isinstance(name, str) or not name or Path(name).name != name:
                raise EvidenceStoreError("manifest file names must be simple file names")
            if not isinstance(expected, str) or len(expected) != 64:
                raise EvidenceStoreError(f"manifest digest for {name!r} must be SHA-256 hex")
            try:
                data = (source / name).read_bytes()
            except OSError as exc:
                raise EvidenceStoreError(f"unable to read evidence file {name!r}: {exc}") from exc
            actual = hashlib.sha256(data).hexdigest()
            if actual != expected:
                raise EvidenceStoreError(
                    f"evidence file {name!r} hash mismatch: expected {expected}, got {actual}"
                )
            blobs[name] = data

        if retention_days is not None and retention_days < 0:
            raise EvidenceStoreError("retention_days must be non-negative")
        timestamp = (created_at or datetime.now(UTC)).astimezone(UTC)
        record = EvidenceRecord(
            evidence_id=evidence_id,
            decision_id=decision_id,
            disposition=disposition,
            input_type=input_type,
            created_at=timestamp.isoformat(),
            retain_until=(timestamp + timedelta(days=retention_days)).isoformat()
            if retention_days is not None
            else None,
            manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
            files=tuple(blobs),
        )

        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                _SELECT + " WHERE evidence_id = ?", (evidence_id,)
            ).fetchone()
            if row is not None:
                existing = _record(row)
                if existing.manifest_sha256 != record.manifest_sha256:
                    raise EvidenceStoreError(
                        f"evidence_id {evidence_id!r} already exists with different content"
                    )
                return existing

            target = self.blob_root / evidence_id
            try:
                target.mkdir(parents=True, exist_ok=False)
                (target / "manifest.json").write_bytes(manifest_bytes)
                for name, data in blobs.items():
                    (target / name).write_bytes(data)
                connection.execute(
                    """INSERT INTO evidence_records (
                    evidence_id, decision_id, disposition, input_type, created_at,
                    retain_until, manifest_sha256, files_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        record.evidence_id,
                        record.decision_id,
                        record.disposition,
                        record.input_type,
                        record.created_at,
                        record.retain_until,
                        record.manifest_sha256,
                        json.dumps(record.files),
                    ),
                )
            except (OSError, sqlite3.Error) as exc:
                raise EvidenceStoreError(f"unable to persist evidence record: {exc}") from exc
        return record

    def get(self, evidence_id: str) -> EvidenceRecord:
        with self._connect() as connection:
            row = connection.execute(
                _SELECT + " WHERE evidence_id = ?", (evidence_id,)
            ).fetchone()
        if row is None:
            raise EvidenceStoreError(f"unknown evidence_id {evidence_id!r}")
        return _record(row)

    def list_by_decision(self, decision_id: str) -> tuple[EvidenceRecord, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                _SELECT + " WHERE decision_id = ? ORDER BY created_at, evidence_id",
                (decision_id,),
            ).fetchall()
        return tuple(_record(row) for row in rows)

    def verify(self, evidence_id: str) -> dict[str, Any]:
        record = self.get(evidence_id)
        directory = self.blob_root / evidence_id
        failures: list[str] = []
        try:
            manifest_bytes = (directory / "manifest.json").read_bytes()
            manifest = json.loads(manifest_bytes)
        except (OSError, json.JSONDecodeError) as exc:
            return {"evidence_id": evidence_id, "valid": False, "failures": [str(exc)]}
        if hashlib.sha256(manifest_bytes).hexdigest() != record.manifest_sha256:
            failures.append("manifest_sha256_mismatch")
        hashes = manifest.get("files") if isinstance(manifest, dict) else None
        if not isinstance(hashes, dict):
            failures.append("manifest_files_invalid")
        else:
            for name in record.files:
                try:
                    actual = hashlib.sha256((directory / name).read_bytes()).hexdigest()
                except OSError:
                    failures.append(f"missing:{name}")
                    continue
                if actual != hashes.get(name):
                    failures.append(f"hash_mismatch:{name}")
        return {"evidence_id": evidence_id, "valid": not failures, "failures": failures}

    def expired(self, *, as_of: datetime | None = None) -> tuple[EvidenceRecord, ...]:
        cutoff = (as_of or datetime.now(UTC)).astimezone(UTC).isoformat()
        with self._connect() as connection:
            rows = connection.execute(
                _SELECT
                + " WHERE retain_until IS NOT NULL AND retain_until <= ? ORDER BY retain_until, evidence_id",
                (cutoff,),
            ).fetchall()
        return tuple(_record(row) for row in rows)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection


def record_payload(record: EvidenceRecord) -> dict[str, Any]:
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "evidence_id": record.evidence_id,
        "decision_id": record.decision_id,
        "disposition": record.disposition,
        "input_type": record.input_type,
        "created_at": record.created_at,
        "retain_until": record.retain_until,
        "manifest_sha256": record.manifest_sha256,
        "files": list(record.files),
    }


def _record(row: tuple[Any, ...]) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=row[0], decision_id=row[1], disposition=row[2], input_type=row[3],
        created_at=row[4], retain_until=row[5], manifest_sha256=row[6],
        files=tuple(json.loads(row[7])),
    )


def _text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EvidenceStoreError(f"manifest {key} must be a non-empty string")
    return value
