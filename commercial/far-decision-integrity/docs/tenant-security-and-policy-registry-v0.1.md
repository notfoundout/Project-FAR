# Tenant Security and Policy Registry v0.1

This contract adds explicit tenant boundaries around FAR authorization and policy selection.

## Authentication

API credentials use a `key_id.secret` bearer-token form. Only SHA-256 secret digests are stored. Authentication returns a tenant-bound principal with explicit scopes.

Supported reference scopes include:

- `authorize`
- `policy:read`
- `policy:write`
- `evidence:read`

Every protected operation must require its corresponding scope.

## Tenant isolation

Policies are indexed by tenant, policy identifier, and immutable version. Active-policy selection is scoped to the authenticated tenant. A policy registered for one tenant cannot be resolved through another tenant's principal.

Evidence identifiers should be namespaced with `tenant_evidence_id()` before persistence or retrieval to prevent cross-tenant identifier collisions.

## Policy registry

Policy payloads are canonicalized and SHA-256 hashed. A registered version is immutable. Reusing a tenant, policy identifier, and version is rejected. Exactly one version may be active for each tenant and policy identifier.

## Claim boundary

This reference contract does not implement OAuth, secret rotation, rate limiting, encryption at rest, external identity federation, or a network-facing administration API. SHA-256 secret storage is a minimal deterministic test contract, not a production password-hashing recommendation.
