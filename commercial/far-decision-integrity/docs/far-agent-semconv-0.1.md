# FAR agent trace semantic convention 0.1

Status: experimental

This contract defines FAR attributes carried by flat span JSON or OTLP JSON. It does not claim that ordinary OpenTelemetry or OpenInference traces contain FAR decision evidence. Producers must explicitly instrument the attributes below.

## Epistemic boundary

Ingestion preserves disclosed commitments. It does not infer hidden reasoning, establish the truth of evidence, prove that authorization occurred, or prove semantic completeness. `far.trace.completeness` is a producer claim and is preserved separately from mechanically validated schema coverage.

## Required root-span attributes

Exactly one span in the payload must set `far.decision.root_span=true`. That span must also disclose:

- `far.decision.id`: stable decision identifier;
- `far.decision.type`: decision class;
- `far.policy.version`: policy identifier and version;
- `far.decision.root`: node identifier for the decision conclusion;
- at least one `far.action.*` attribute describing the proposed action.

Every span must disclose a non-empty trace ID and span ID. Every FAR-marked span must belong to the same trace as the root span.

## Decision-node attributes

A span representing a decision node must disclose all of:

- `far.node.id`;
- `far.node.kind`;
- `far.node.statement`.

Optional node attributes use the `far.node.attribute.*` prefix. The ingester adds `_far_source.trace_id` and `_far_source.span_id` to every normalized node for provenance.

## Declared dependencies

A node span may disclose one dependency using both:

- `far.dependency.target`;
- `far.dependency.relation`.

Telemetry parent-child relationships are preserved as observed execution topology. They are not interpreted as logical dependencies.

## Authorization and unknowns

`far.authorization.required=true` marks the node as an authorization requirement. This records a requirement only; it does not establish that authorization was requested, granted, current, or valid.

`far.node.unknown=true` marks the node identifier as unknown. The root may also disclose `far.unknowns` as an array of non-empty strings or a comma-separated string. String unknowns are transitional in schema 0.1 and do not yet encode typed unknown semantics.

## Completeness fields

The normalized package uses:

- `trace_completeness`: mechanical schema-field coverage for accepted FAR commitments;
- `metadata.producer_claimed_completeness`: optional producer assertion from `far.trace.completeness`;
- `metadata.semantic_completeness_verified`: always `false` in version 0.1.

An accepted package can have complete required fields while still omitting undisclosed reasoning, evidence, alternatives, dependencies, or authorization facts.

## Provenance

The normalized metadata includes:

- ingestion and semantic-convention versions;
- transport format;
- source trace and root span identifiers;
- canonical source-payload SHA-256 digest;
- source and input span counts;
- execution topology;
- explicit semantic-completeness status.

## Supported transports

Version 0.1 accepts:

- flat JSON with a top-level `spans` array;
- OTLP JSON with `resourceSpans/scopeSpans/spans` or legacy `instrumentationLibrarySpans`.

Transport compatibility is not semantic compatibility. Uninstrumented OpenTelemetry or OpenInference traces are not sufficient inputs.
