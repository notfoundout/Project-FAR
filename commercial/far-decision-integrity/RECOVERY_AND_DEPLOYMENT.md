# FAR Recovery and Deployment Hardening

This release adds verifiable single-node recovery controls around the secured FAR runtime.

## Database migrations

Run the idempotent migration command before starting a newly deployed version:

```bash
far-operations --security-db /var/lib/far/security.db migrate \
  --evidence-db /var/lib/far/evidence.db
```

The migration ledger is stored in each SQLite database. Repeating the command is safe.

## Readiness

Readiness checks database integrity and confirms that blob and staging paths are writable:

```bash
far-operations --security-db /var/lib/far/security.db readiness \
  --evidence-db /var/lib/far/evidence.db \
  --blob-root /var/lib/far/blobs \
  --staging-root /var/lib/far/staging
```

The container and Compose health checks use this command.

## Backup and restore drill

Create and verify a backup:

```bash
far-operations --security-db /var/lib/far/security.db backup \
  --evidence-db /var/lib/far/evidence.db \
  --blob-root /var/lib/far/blobs \
  --output /backup/far-$(date +%Y%m%d%H%M%S)

far-operations --security-db /var/lib/far/security.db verify-backup /backup/far-20260723
```

Restore only into an empty destination:

```bash
far-operations --security-db /var/lib/far/security.db restore-backup \
  /backup/far-20260723 \
  --destination /restore-drill
```

Restoration first verifies the manifest and SQLite integrity, copies through a staging directory, then applies idempotent schema migrations.

## Retention enforcement

Preview expired evidence before deleting it:

```bash
far-operations --security-db /var/lib/far/security.db enforce-retention \
  --evidence-db /var/lib/far/evidence.db \
  --blob-root /var/lib/far/blobs \
  --dry-run
```

Remove expired database records and their corresponding immutable blob directories by omitting `--dry-run`.

## Container posture

The reference container runs as a non-root user. The Compose deployment uses a read-only root filesystem, drops all Linux capabilities, enables `no-new-privileges`, places temporary files on a bounded tmpfs, and provides a 30-second stop grace period.

## Claim boundary

These controls verify local SQLite backups and single-node restoration. They do not provide off-site backup scheduling, encrypted backup transport, multi-region recovery, PostgreSQL migration, zero-downtime schema changes, orchestration-level disruption budgets, or a measured recovery-time guarantee.
