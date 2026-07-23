from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_decision_integrity.store import EvidenceStore, EvidenceStoreError
from far_decision_integrity.store_cli import main


def evidence(directory: pathlib.Path, evidence_id: str = "refund-1-abcd") -> pathlib.Path:
    directory.mkdir(parents=True, exist_ok=True)
    package = b'{"decision_id":"refund-1"}\n'
    authorization = b'{"disposition":"allow"}\n'
    (directory / "decision-package.json").write_bytes(package)
    (directory / "authorization.json").write_bytes(authorization)
    manifest = {
        "schema_version": "far-authorization-evidence/0.2",
        "evidence_id": evidence_id,
        "decision_id": "refund-1",
        "input_type": "decision_package",
        "disposition": "allow",
        "files": {
            "authorization.json": hashlib.sha256(authorization).hexdigest(),
            "decision-package.json": hashlib.sha256(package).hexdigest(),
        },
    }
    (directory / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return directory


class TestEvidenceStore(unittest.TestCase):
    def test_put_get_verify_and_list(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            store = EvidenceStore(root / "store.db", root / "blobs")
            record = store.put_directory(
                evidence(root / "source"),
                retention_days=30,
                created_at=datetime(2026, 7, 23, tzinfo=UTC),
            )
            self.assertEqual(record.evidence_id, "refund-1-abcd")
            self.assertEqual(store.get(record.evidence_id), record)
            self.assertEqual(store.list_by_decision("refund-1"), (record,))
            self.assertTrue(store.verify(record.evidence_id)["valid"])

    def test_idempotent_duplicate_is_safe(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            store = EvidenceStore(root / "store.db", root / "blobs")
            source = evidence(root / "source")
            first = store.put_directory(source)
            second = store.put_directory(source)
            self.assertEqual(first.manifest_sha256, second.manifest_sha256)
            self.assertEqual(len(store.list_by_decision("refund-1")), 1)

    def test_conflicting_duplicate_is_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            store = EvidenceStore(root / "store.db", root / "blobs")
            source = evidence(root / "source")
            store.put_directory(source)
            original = (root / "blobs" / "refund-1-abcd" / "authorization.json").read_bytes()
            changed = evidence(root / "changed")
            payload = json.loads((changed / "manifest.json").read_text())
            changed_bytes = b'{"disposition":"block"}\n'
            (changed / "authorization.json").write_bytes(changed_bytes)
            payload["files"]["authorization.json"] = hashlib.sha256(changed_bytes).hexdigest()
            (changed / "manifest.json").write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
            with self.assertRaises(EvidenceStoreError):
                store.put_directory(changed)
            self.assertEqual(
                (root / "blobs" / "refund-1-abcd" / "authorization.json").read_bytes(),
                original,
            )

    def test_tamper_detection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            store = EvidenceStore(root / "store.db", root / "blobs")
            record = store.put_directory(evidence(root / "source"))
            (root / "blobs" / record.evidence_id / "authorization.json").write_text("tampered")
            result = store.verify(record.evidence_id)
            self.assertFalse(result["valid"])
            self.assertIn("hash_mismatch:authorization.json", result["failures"])

    def test_expired_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            store = EvidenceStore(root / "store.db", root / "blobs")
            record = store.put_directory(
                evidence(root / "source"),
                retention_days=1,
                created_at=datetime(2026, 7, 20, tzinfo=UTC),
            )
            self.assertEqual(
                store.expired(as_of=datetime(2026, 7, 22, tzinfo=UTC)),
                (record,),
            )

    def test_bad_source_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source = evidence(root / "source")
            (source / "authorization.json").write_text("tampered")
            store = EvidenceStore(root / "store.db", root / "blobs")
            with self.assertRaises(EvidenceStoreError):
                store.put_directory(source)

    def test_cli_put_get_and_verify(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            database = root / "store.db"
            blobs = root / "blobs"
            source = evidence(root / "source")
            common = ["--database", str(database), "--blob-root", str(blobs)]
            self.assertEqual(main(common + ["put", str(source)]), 0)
            self.assertEqual(main(common + ["get", "refund-1-abcd"]), 0)
            self.assertEqual(main(common + ["verify", "refund-1-abcd"]), 0)


if __name__ == "__main__":
    unittest.main()
