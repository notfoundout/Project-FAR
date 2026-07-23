# FAR runtime operations

The secured service now integrates production-operations controls into the live HTTP runtime.

## Runtime controls

- Every authenticated request is subject to a fixed-window per-principal rate limit.
- Runtime counters record authentication outcomes, HTTP status classes, authorization dispositions, rate-limit denials, and administration actions.
- Administrative mutations are tenant-scoped and append an audit record.

## Endpoints

- `GET /metrics` requires `metrics:read`.
- `GET /v1/admin/audit?limit=100` requires `audit:read`.
- `POST /v1/admin/keys/rotate` requires `keys:write`.
- `POST /v1/admin/keys/revoke` requires `keys:write`.
- `POST /v1/admin/policies/register` requires `policy:write`.
- `POST /v1/admin/policies/activate` requires `policy:write`.

The service is configured with `--rate-limit` and `--rate-window-seconds`.

## Claim boundary

The limiter is process-local and resets on restart. Metrics are in-memory counters rather than a durable observability backend. Administration still uses reference API keys and does not provide OAuth/OIDC, HSM-backed secrets, distributed coordination, approval workflows, or external audit-log shipping.
