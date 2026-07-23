# FAR Secured MVP

The secured MVP binds each authorization request to an authenticated tenant, an immutable policy version, and a persistently verifiable evidence record.

## Runtime contract

- `GET /healthz` is public.
- `POST /v1/authorize` requires `Authorization: Bearer <key_id>.<secret>` and the `authorize` scope.
- `GET /v1/policies/<policy_id>` requires `policy:read`; use `?version=<version>` for an explicit version.
- `GET /v1/evidence/<evidence_id>` and `/manifest` require `evidence:read` and reject evidence owned by another tenant.

An authorization body includes `policy_id`, optional `policy_version`, `input_type`, and `payload`. The active tenant policy is used when no version is supplied. The response includes the tenant, immutable policy digest, disposition, and protected evidence URL.

## Local deployment

```bash
cd commercial/far-decision-integrity
docker compose up --build
```

The service stores security metadata, policy versions, evidence metadata, and immutable blobs in the `far-data` volume.

Before serving traffic, provision API keys and policies with `TenantSecurityStore` from a trusted administrative process. The public service intentionally has no key-creation or policy-write HTTP endpoint.

## Example request

```bash
curl -X POST http://127.0.0.1:8080/v1/authorize \
  -H 'Authorization: Bearer app-key.secret' \
  -H 'Content-Type: application/json' \
  --data @authorization-request.json
```

## Claim boundary

This is a deployable reference MVP, not a complete production security perimeter. It does not provide TLS termination, OAuth/OIDC, automated key rotation, rate limiting, encrypted volumes, backups, replication, legal holds, policy administration endpoints, or external factual verification. Deploy behind a TLS reverse proxy and manage secrets outside the repository.
