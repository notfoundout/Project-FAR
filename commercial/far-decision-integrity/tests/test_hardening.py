from __future__ import annotations

import json
import pathlib
import sqlite3
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.hardening import (
    enforce_retention,
    migrate_database,
    readiness_report,
    restore_backup,
)
from far_decision_integrity.operations import OperationsError, create_backup
from far_decision_integrity.security import TenantSecurityStore
from far_decision_integrity.store import EvidenceStore


def evidence_directory(root: pathlib.Path, evidence_id: str = "evidence-1") -> pathlib.Path:
    directory = root / evidence_id
    directory.mkdir()
    payload = b'{}\n'
    import hashlib

    manifest = {
        "evidence_id": evidence_id,
        "decision_id": "decision-1",
        "disposition": "allow",
        "input_type": "decision_package",
        "files": {"authorization.json": hashlib.sha256(payload).hexdigest()},
    }
    (directory / "authorization.json").write_bytes(payload)
    (directory / "manifest.json").write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    return directory


class TestHardening(unittest.TestCase):
    def test_migrations_are_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            database = pathlib.Path(directory) / "security.db"
            first = migrate_database(database, "security")
            second = migrate_database(database, "security")
            self.assertTrue(first["migrated"])
            self.assertFalse(second["migrated"])

    def test_verified_backup_restores_into_empty_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            security = TenantSecurityStore(root / "security.db")
            security.register_key("tenant", "key", "secret", ("authorize",))
            store = EvidenceStore(root / "evidence.db", root / "blobs")
            store.put_directory(evidence_directory(root))
            backup = root / "backup"
            create_backup(root / "security.db", root / "evidence.db", root / "blobs", backup)
            result = restore_backup(backup, root / "restored")
            self.assertTrue(result.verified)
            self.assertTrue((root / "restored" / "security.db").is_file())
            self.assertTrue((root / "restored" / "blobs" / "evidence-1").is_dir())

    def test_restore_rejects_nonempty_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            TenantSecurityStore(root / "security.db")
            EvidenceStore(root / "evidence.db", root / "blobs")
            backup = root / "backup"
            create_backup(root / "security.db", root / "evidence.db", root / "blobs", backup)
            destination = root / "restored"
            destination.mkdir()
            (destination / "occupied").write_text("x", encoding="utf-8")
            with self.assertRaises(OperationsError):
                restore_backup(backup, destination)

    def test_retention_dry_run_and_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            store = EvidenceStore(root / "evidence.db", root / "blobs")
            created = datetime.now(UTC) - timedelta(days=3)
            store.put_directory(evidence_directory(root), retention_days=1, created_at=created)
            preview = enforce_retention(root / "evidence.db", root / "blobs", dry_run=True)
            self.assertEqual(preview["deleted"], ["evidence-1"])
            self.assertTrue((root / "blobs" / "evidence-1").exists())
            applied = enforce_retention(root / "evidence.db", root / "blobs")
            self.assertEqual(applied["deleted"], ["evidence-1"])
            self.assertFalse((root / "blobs" / "evidence-1").exists())
            with sqlite3.connect(root / "evidence.db") as connection:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM evidence_records").fetchone()[0], 0)

    def test_readiness_checks_databases_and_writable_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            report = readiness_report(
                root / "security.db",
                root / "evidence.db",
                root / "blobs",
                root / "staging",
            )
            self.assertTrue(report["ready"])
            self.assertEqual(report["failures"], [])


if __name__ == "__main__":
    unittest.main()
