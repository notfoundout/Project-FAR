# FAR external identity and observability

This package defines strict adapter boundaries for external identity, secret resolution, and durable observability export.

## Identity contract

An external provider must produce an explicit assertion containing issuer, subject, tenant, scopes, issue time, expiry, and token ID. FAR does not infer tenant or permissions from display names, email domains, or token text.

`IdentityAssertion.principal()` converts a verified assertion into the existing FAR `Principal` model, preserving tenant and scope enforcement.

The included `HMACIdentityProvider` is a reference implementation for controlled deployments and tests. It is not an OIDC implementation. Production adapters should verify their provider's signature, issuer, audience, expiry, revocation policy, and key rotation before constructing an assertion.

## Secret providers

`EnvironmentSecretProvider` and `MappingSecretProvider` demonstrate the resolver interface. Secret values are never written to assertions or observability events.

## Short-lived credentials

Reference tokens have a configurable maximum lifetime and are rejected when expired, not yet valid, malformed, signed by an unknown key, or signed by a mismatched issuer.

## Durable observability

`HashChainedJSONLExporter` appends canonical JSON events with a SHA-256 link to the previous event. The verifier detects record edits, deletion/reordering within the retained chain, and malformed records.

Example:

```bash
far-external-identity emit-event \
  --log /var/lib/far/observability/events.jsonl \
  --event-type authorization.completed \
  --payload '{"tenant_id":"tenant-a","disposition":"allow"}'

far-external-identity verify-log /var/lib/far/observability/events.jsonl
```

## Claim boundary

This slice does not implement OIDC discovery, JWT/JWKS processing, OAuth token exchange, cloud secret-manager clients, HSM signing, distributed revocation, encrypted logging, remote telemetry delivery, or compliance certification. It provides explicit interfaces and a deterministic reference implementation that production provider adapters can satisfy.
