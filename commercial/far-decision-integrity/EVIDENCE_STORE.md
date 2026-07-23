# FAR persistent evidence store

`far-evidence-store/0.1` persists authorization evidence produced by the FAR runtime or HTTP service.

The store uses SQLite for indexed metadata and an immutable directory per `evidence_id` for canonical evidence bytes. Insertion verifies every SHA-256 digest declared by the evidence manifest before writing. Repeating the same insertion is idempotent; reusing an `evidence_id` with different manifest content is rejected.

## Usage

```bash
far-evidence-store \
  --database var/far/evidence.db \
  --blob-root var/far/blobs \
  put far-evidence/service/refund-1-abcd \
  --retention-days 365

far-evidence-store --database var/far/evidence.db --blob-root var/far/blobs get refund-1-abcd
far-evidence-store --database var/far/evidence.db --blob-root var/far/blobs verify refund-1-abcd
far-evidence-store --database var/far/evidence.db --blob-root var/far/blobs list-decision refund-1
far-evidence-store --database var/far/evidence.db --blob-root var/far/blobs expired
```

Retention is recorded as metadata. This version reports expired records but does not automatically delete them. Deletion, legal holds, replication, encryption, access control, backups, and multi-tenant isolation remain deployment responsibilities.

Integrity verification checks the stored manifest digest and every evidence-file digest. It detects post-write corruption or tampering but does not prove the truth of the recorded facts.
