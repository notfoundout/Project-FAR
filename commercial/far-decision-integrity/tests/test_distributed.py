from __future__ import annotations

import hashlib
import unittest

from far_decision_integrity.distributed import (
    DistributedEvidenceRecord,
    DistributedRuntimeError,
    PostgreSQLMetadataStore,
    SharedFixedWindowRateLimiter,
    VerifiedObjectStore,
    distributed_readiness,
)


class Cursor:
    def __init__(self, row=None):
        self.row = row

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, *, existing=None, migration_markers=None, fail=False):
        self.existing = existing
        self.migration_markers = set(migration_markers or ())
        self.fail = fail
        self.statements = []
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def execute(self, query, parameters=()):
        if self.fail:
            raise RuntimeError("database unavailable")
        self.statements.append((query, tuple(parameters)))
        if query.startswith("SELECT 1 FROM far_schema_migrations"):
            return Cursor((1,) if parameters[1] in self.migration_markers else None)
        if query.startswith("SELECT decision_id"):
            return Cursor(self.existing)
        return Cursor()

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class MemoryObjects:
    def __init__(self, *, corrupt=False):
        self.objects = {}
        self.corrupt = corrupt

    def put(self, key, body, metadata):
        self.objects[key] = (body, dict(metadata))

    def get(self, key):
        body, metadata = self.objects[key]
        return ((body + b"x") if self.corrupt else body, metadata)

    def delete(self, key):
        self.objects.pop(key, None)


class MemoryCounter:
    def __init__(self):
        self.values = {}
        self.expiries = {}

    def increment(self, key, *, expires_at):
        self.values[key] = self.values.get(key, 0) + 1
        self.expiries[key] = expires_at
        return self.values[key]


class DistributedRuntimeTests(unittest.TestCase):
    def test_migrations_are_idempotent(self):
        connection = FakeConnection(migration_markers={1, 2, 3})
        result = PostgreSQLMetadataStore(lambda: connection).migrate(now=10)
        self.assertEqual(result["applied"], [])
        self.assertTrue(connection.committed)
        self.assertTrue(connection.closed)

    def test_new_migrations_are_recorded(self):
        connection = FakeConnection(migration_markers={1})
        result = PostgreSQLMetadataStore(lambda: connection).migrate(now=11)
        self.assertEqual(result["applied"], [2, 3])
        inserts = [item for item in connection.statements if item[0].startswith("INSERT INTO far_schema_migrations")]
        self.assertEqual(len(inserts), 2)

    def test_metadata_put_is_retry_safe(self):
        digest = "a" * 64
        record = DistributedEvidenceRecord("tenant", "evidence", "decision", digest, "far/tenant/evidence", 5)
        connection = FakeConnection(existing=("decision", digest, "far/tenant/evidence", 5))
        self.assertEqual(PostgreSQLMetadataStore(lambda: connection).put(record), record)
        self.assertTrue(connection.committed)

    def test_metadata_conflict_rolls_back(self):
        record = DistributedEvidenceRecord("tenant", "evidence", "decision", "a" * 64, "far/tenant/evidence", 5)
        connection = FakeConnection(existing=("other", "b" * 64, "far/tenant/evidence", 5))
        with self.assertRaises(DistributedRuntimeError):
            PostgreSQLMetadataStore(lambda: connection).put(record)
        self.assertTrue(connection.rolled_back)

    def test_object_store_verifies_round_trip(self):
        transport = MemoryObjects()
        result = VerifiedObjectStore(transport).put("tenant", "evidence", {"manifest.json": b"{}", "report.json": b"ok"})
        expected = {"manifest.json": hashlib.sha256(b"{}").hexdigest(), "report.json": hashlib.sha256(b"ok").hexdigest()}
        self.assertEqual(result["files"], expected)
        self.assertEqual(len(transport.objects), 2)

    def test_object_store_rejects_corruption(self):
        with self.assertRaises(DistributedRuntimeError):
            VerifiedObjectStore(MemoryObjects(corrupt=True)).put("tenant", "evidence", {"manifest.json": b"{}"})

    def test_shared_rate_limit_is_consistent_across_instances(self):
        backend = MemoryCounter()
        first = SharedFixedWindowRateLimiter(backend, 2, 60, now=lambda: 120)
        second = SharedFixedWindowRateLimiter(backend, 2, 60, now=lambda: 120)
        self.assertTrue(first.allow("tenant:subject"))
        self.assertTrue(second.allow("tenant:subject"))
        self.assertFalse(first.allow("tenant:subject"))
        self.assertEqual(set(backend.expiries.values()), {180})

    def test_readiness_reports_each_dependency(self):
        result = distributed_readiness(lambda: True, lambda: False, lambda: True)
        self.assertFalse(result["ready"])
        self.assertEqual(result["checks"], {"metadata": True, "object_storage": False, "coordination": True})

    def test_database_failures_roll_back(self):
        connection = FakeConnection(fail=True)
        with self.assertRaises(DistributedRuntimeError):
            PostgreSQLMetadataStore(lambda: connection).migrate()
        self.assertTrue(connection.rolled_back)
        self.assertTrue(connection.closed)


if __name__ == "__main__":
    unittest.main()
