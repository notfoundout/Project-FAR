# Purpose

This document defines the Phase 3 Prompt 2 external interchange contract for Project FAR mechanization. It complements, but does not replace, the canonical storage-independent IR.

# Format Version

The only supported interchange-format version is `far-ir/1.0`. This version identifies the external JSON/YAML contract and is not Foundation v1.0.

# Canonical JSON Contract

`schemas/far-document.schema.json` is the canonical JSON Schema for `far-ir/1.0`. It defines required fields, object-kind discriminators, identifier patterns, typed references, source locations, metadata, extensions, graph node kinds, graph edge kinds, and unknown-field rejection.

# YAML Serialization

YAML is an alternative serialization of the same external model. It has no separate semantic model. YAML parsing is deferred to Prompt 3. This prompt defines the contract and typed conversion layer only.

# Root Document

A root document contains `format_version`, `id`, one `investigation`, and ordered object arrays for representations, structures, interpretations, claims, assumptions, evidence, operations, reasoning steps, dependencies, proofs, and an optional reasoning graph.

# Object Kinds

External objects preserve discriminators in the `kind` field. Supported object kinds are representation, structure, interpretation, investigation, claim, assumption, evidence, operation, reasoning_step, dependency, and proof.

# Identifier Rules

Identifiers use the canonical Prompt 1 rule `^[A-Za-z][A-Za-z0-9_.:-]*$`. They are stable, case-sensitive, and are not silently normalized.

# Reference Encoding

A reference is an object with `identifier`, optional `expected_kind`, and optional `source`. Prompt 2 does not resolve references.

# Provenance Encoding

Provenance uses `source`, optional one-based `line` and `column`, and optional one-based `end_line` and `end_column`.

# Metadata and Extensions

`metadata` is a controlled mapping for canonical metadata. `extensions` is the only extension point for non-core fields. Core objects reject unknown fields.

# Ordering Rules

Arrays preserve source order. Reasoning steps use their explicit `order` field and are not reordered by conversion.

# Unknown Field Policy

Canonical typed objects use `additionalProperties: false`. Unknown core fields produce external-shape diagnostics or schema failures.

# Conversion to Canonical IR

Typed external models convert deterministically to canonical IR records. The conversion preserves identifiers, order, metadata, source provenance, and supported graph records. The canonical IR remains independent of JSON and YAML.

# Compatibility Policy

`far-ir/1.0` is the only accepted version in Prompt 2. Unsupported versions produce diagnostics and must not be silently accepted.

# Examples

Examples are provided in `examples/mechanization/minimal-investigation.json` and `examples/mechanization/minimal-investigation.yaml`. The YAML example is semantically equivalent to the JSON example, but YAML parsing remains deferred.

# Deferred Features

Parser pipeline, YAML parsing, normalization, serialization, reference resolution, graph validation, dependency-cycle checks, proof verification, CLI, API, storage, and execution engine behavior remain deferred.
