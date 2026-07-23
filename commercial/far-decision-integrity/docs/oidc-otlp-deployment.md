# OIDC and OTLP deployment

The secured service can authenticate either local FAR API keys or externally issued OIDC access tokens. Local keys remain the default. Supplying `--identity-config` enables OIDC mode for every authenticated endpoint.

```bash
far-secured-service \
  --identity-config deploy/oidc.json \
  --observability-log /var/lib/far/observability/events.jsonl \
  --otlp-endpoint https://collector.example.com/v1/logs \
  --otlp-header Authorization="Bearer ${OTLP_TOKEN}"
```

The OIDC adapter performs discovery, loads the issuer JWKS, accepts only RS256, validates the key ID and signature, and requires matching issuer and audience. It also enforces issue time, expiry, maximum lifetime, tenant, subject, token ID and explicit scopes. The configured tenant and scope claims are converted into the existing FAR `Principal`, so downstream tenant isolation and scope checks are unchanged.

The local hash-chained JSONL log remains enabled. When an OTLP endpoint is configured, the same authentication, rate-limit, authorization and administration events are also sent as OTLP/HTTP JSON log records. Export failures increment `observability.export_failed` and do not alter an authorization result.

Deployment requirements:

- use HTTPS for issuer discovery, JWKS and OTLP endpoints;
- mount the identity configuration read-only;
- inject collector credentials through the deployment secret mechanism rather than committing them;
- restrict accepted audiences to the FAR service;
- keep token lifetimes short;
- ensure the identity provider supplies tenant and scope claims explicitly;
- monitor `observability.export_failed` and preserve the local hash-chain log.

Claim boundary: this adapter does not implement token revocation, DPoP, mTLS-bound access tokens, encrypted local logs, asynchronous OTLP buffering, retry queues, certificate pinning, or identity-provider-specific group-to-scope translation.
