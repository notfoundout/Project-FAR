# FAR production operations

The `far-operations` command adds the first operator-facing controls around the secured FAR MVP.

## Key lifecycle

Keys can be rotated atomically so the replacement key is inserted before the old key is disabled. Keys can also be revoked explicitly. Both actions are tenant-scoped and recorded in the append-only operations audit table.

```bash
far-operations --security-db var/far/security.db rotate-key \
  --token admin.current-secret \
  --old-key-id admin \
  --new-key-id admin-2026-08 \
  --new-secret "$NEW_SECRET" \
  --scope authorize --scope policy:read --scope policy:write \
  --scope evidence:read --scope keys:write --scope audit:read
```

## Policy audit

Policy registration and activation can be routed through `OperationsStore` to create tenant-bound audit records containing the actor, target version, policy hash, and activation state.

## Backup and verification

Backups use SQLite's online backup API, copy immutable evidence blobs, and generate a SHA-256 manifest. Verification checks every declared file and runs `PRAGMA integrity_check` on both databases.

```bash
far-operations --security-db var/far/security.db backup \
  --evidence-db var/far/evidence.db \
  --blob-root var/far/blobs \
  --output backups/2026-07-23

far-operations --security-db var/far/security.db verify-backup backups/2026-07-23
```

A valid backup is not a complete disaster-recovery program. Operators still need off-host replication, encryption, retention policy, restore drills, and recovery objectives.

## Rate limiting and metrics

`FixedWindowRateLimiter` provides a deterministic in-process limiter suitable for the reference runtime. `RuntimeMetrics` provides thread-safe counters for request, denial, authorization, and error totals. Distributed deployments require shared rate-limit state and a production metrics exporter.

## Claim boundary

This implementation does not provide HSM-backed secrets, OAuth/OIDC, distributed rate limiting, encrypted backups, automatic scheduling, external log shipping, high availability, or compliance certification.
