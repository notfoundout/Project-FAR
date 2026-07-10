# Purpose

This document defines Prompt 3 deterministic normalization for FAR mechanization documents.

# Normalization Boundary

Normalization is structural only. It operates after parsing, schema validation, typed external model construction, canonical IR conversion, and local IR validation.

# Semantics-Preserving Rules

Normalization may sort collections whose order is not semantically meaningful, sort metadata and extension keys for deterministic serialization, and render enum values canonically. It does not repair invalid input.

# Ordered Collections

Reasoning steps preserve their existing sequence because the `order` field is meaningful. Serialization preserves that sequence.

# Unordered Collections

Representations, structures, interpretations, claims, assumptions, evidence, operations, dependencies, proofs, graph nodes, and graph edges are sorted by identifier for deterministic output.

# Identifier Preservation

Identifiers are never renamed, case-normalized, inferred, or repaired.

# Metadata and Extensions

Metadata and extension mappings are serialized with stable key ordering. Their values are not semantically interpreted by normalization.

# Optional Field Policy

Optional empty collections and absent optional values are omitted from serialized output where omission is lossless under `far-ir/1.0`. Present source provenance and non-empty metadata or extensions are preserved.

# Diagnostic Behavior

Normalization returns structured diagnostics if conversion to the external model or back to canonical IR cannot proceed safely. It does not silently discard invalid data.

# Idempotence

Normalization is idempotent: normalizing an already normalized document produces an equal normalized document.

# Deferred Semantic Normalization

Reference resolution, dependency validation, graph reachability, proof verification, semantic duplicate removal, and any mathematical normalization are deferred.
