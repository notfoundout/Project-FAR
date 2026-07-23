from __future__ import annotations

import json
import os
import shutil
import sqlite3
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .operations import OperationsError, verify_backup

HARDENING_SCHEMA_VERSION = "far-recovery-hardening/0.1"
CURRENT_DATABASE_SCHEMA = 1


@dataclass(frozen=True, slots=True)
class RestoreResult:
    destination: Path
    files_restored: tuple[str, ...]
    verified: bool


def migrate_database(path: str | Path, role: str) -> dict[str, Any]:
    database = Path(path)
    database.parent.mkdir(parents=True, exist_ok=True)
    if role not in {"security", "evidence"}:
        raise OperationsError("role must be security or evidence")
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS far_schema_migrations ("
            "role TEXT NOT NULL, version INTEGER NOT NULL, applied_at TEXT NOT NULL, "
            "PRIMARY KEY (role, version))"
        )
        rows = connection.execute(
            "SELECT version FROM far_schema_migrations WHERE role = ? ORDER BY version", (role,)
        ).fetchall()
        applied = {row[0] for row in rows}
        if CURRENT_DATABASE_SCHEMA not in applied:
            connection.execute(
                "INSERT INTO far_schema_migrations (role, version, applied_at) VALUES (?, ?, ?)",
                (role, CURRENT_DATABASE_SCHEMA, datetime.now(UTC).isoformat()),
            )
        integrity = connection.execute("PRAGMA integrity_check").fetchone()
    if integrity is None or integrity[0] != "ok":
        raise OperationsError(f"{role} database failed integrity check")
    return {
        "schema_version": HARDENING_SCHEMA_VERSION,
        "role": role,
        "database_schema": CURRENT_DATABASE_SCHEMA,
        "migrated": CURRENT_DATABASE_SCHEMA not in applied,
    }


def restore_backup(backup: str | Path, destination: str | Path) -> RestoreResult:
    source = Path(backup)
    target = Path(destination)
    verification = verify_backup(source)
    if not verification["valid"]:
        raise OperationsError(f"backup verification failed: {verification['failures']}")
    if target.exists() and any(target.iterdir()):
        raise OperationsError("restore destination must be empty")
    target.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="far-restore-", dir=target.parent))
    try:
        for name in ("security.db", "evidence.db"):
            shutil.copy2(source / name, staging / name)
        if (source / "blobs").exists():
            shutil.copytree(source / "blobs", staging / "blobs")
        restored = sorted(path.relative_to(staging).as_posix() for path in staging.rglob("*") if path.is_file())
        for child in staging.iterdir():
            child.replace(target / child.name)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    migrate_database(target / "security.db", "security")
    migrate_database(target / "evidence.db", "evidence")
    return RestoreResult(target, tuple(restored), True)


def enforce_retention(
    evidence_db: str | Path,
    blob_root: str | Path,
    *,
    as_of: datetime | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    cutoff = (as_of or datetime.now(UTC)).astimezone(UTC).isoformat()
    database = Path(evidence_db)
    blobs = Path(blob_root)
    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            "SELECT evidence_id FROM evidence_records "
            "WHERE retain_until IS NOT NULL AND retain_until <= ? ORDER BY evidence_id",
            (cutoff,),
        ).fetchall()
        evidence_ids = [row[0] for row in rows]
        if not dry_run:
            connection.execute("BEGIN IMMEDIATE")
            connection.executemany("DELETE FROM evidence_records WHERE evidence_id = ?", ((item,) for item in evidence_ids))
    if not dry_run:
        for evidence_id in evidence_ids:
            shutil.rmtree(blobs / evidence_id, ignore_errors=True)
    return {
        "schema_version": HARDENING_SCHEMA_VERSION,
        "cutoff": cutoff,
        "dry_run": dry_run,
        "deleted": evidence_ids,
    }


def readiness_report(
    security_db: str | Path,
    evidence_db: str | Path,
    blob_root: str | Path,
    staging_root: str | Path,
) -> dict[str, Any]:
    failures: list[str] = []
    for role, path in (("security", Path(security_db)), ("evidence", Path(evidence_db))):
        try:
            migrate_database(path, role)
            with sqlite3.connect(path) as connection:
                if connection.execute("PRAGMA query_only").fetchone() is None:
                    failures.append(f"{role}:query")
        except (OSError, sqlite3.Error, OperationsError) as exc:
            failures.append(f"{role}:{exc}")
    for name, path in (("blob_root", Path(blob_root)), ("staging_root", Path(staging_root))):
        try:
            path.mkdir(parents=True, exist_ok=True)
            probe = path / f".far-readiness-{os.getpid()}"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
        except OSError as exc:
            failures.append(f"{name}:{exc}")
    return {
        "schema_version": HARDENING_SCHEMA_VERSION,
        "ready": not failures,
        "failures": failures,
    }


def restore_payload(result: RestoreResult) -> dict[str, Any]:
    return {
        "schema_version": HARDENING_SCHEMA_VERSION,
        "destination": str(result.destination),
        "files_restored": list(result.files_restored),
        "verified": result.verified,
    }
