# FAR distributed runtime

This package defines the first production-distribution boundary for FAR.

## Contracts

- `PostgreSQLMetadataStore` uses injected DB-API connections, transactional writes, row locking, immutable evidence identity, and an idempotent migration ledger.
- `VerifiedObjectStore` writes canonical evidence objects through an injected object transport and verifies the stored bytes and SHA-256 metadata before returning success.
- `SharedFixedWindowRateLimiter` uses an injected atomic counter backend so multiple service instances share one principal limit.
- `distributed_readiness` reports metadata, object-storage, and coordination readiness independently.

Validate deployment configuration with:

```bash
far-distributed-runtime deploy/distributed-runtime.json
```

`deploy/kubernetes.yaml` provides a three-replica reference deployment with readiness and liveness probes, a disruption budget, non-root execution, a read-only root filesystem, bounded temporary storage, dropped capabilities, and resource limits.

## Required provider guarantees

PostgreSQL connections must use TLS and transactions. The object transport must provide read-after-write consistency for newly written evidence and preserve SHA-256 metadata. The counter backend must implement atomic increment plus expiry. Secrets must be supplied by the deployment environment rather than committed configuration.

## Claim boundary

This PR defines and tests provider-neutral production contracts. It does not bundle PostgreSQL, Redis, or S3 clients; provision infrastructure; prove a recovery-time objective; implement distributed tracing queues; provide multi-region consensus; or establish cloud-provider certification. Concrete provider clients and load/failover testing remain separate work.
