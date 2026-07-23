# FAR Authorization Service

The service exposes a narrow HTTP boundary around FAR decision integrity.

## Run

```bash
far-authorization-service \
  --host 127.0.0.1 \
  --port 8080 \
  --evidence-root far-evidence/service
```

## Endpoints

- `GET /healthz`
- `POST /v1/authorize`

The authorization endpoint accepts one of two explicit input forms:

```json
{
  "input_type": "decision_package",
  "payload": {"schema_version": "far-decision-package/0.1"}
}
```

```json
{
  "input_type": "trace",
  "payload": {"spans": []}
}
```

A valid request returns HTTP 200 with `allow`, `block`, or `escalate`, the four-state integrity result, and relative references to a deterministic evidence directory. Invalid JSON, malformed packages, malformed traces, unsupported input types, incorrect content types, and oversized bodies return HTTP 400.

Identical inputs produce the same evidence identifier and may be retried safely. The evidence directory contains the normalized decision package, authorization report, and a SHA-256 manifest.

## Claim boundary

The service adjudicates supplied FAR packages or explicitly disclosed FAR trace attributes. It does not authenticate callers, isolate tenants, verify external factual truth, infer hidden reasoning, or provide a durable evidence store. Those remain separate deployment concerns.
