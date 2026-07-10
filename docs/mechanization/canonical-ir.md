# Purpose

This document defines the canonical Phase 3 Prompt 1 FAR Intermediate Representation implemented in `mechanization/far_mechanization/`.

# Design Principles

The IR is executable Python domain data, not a JSON, YAML, database, CLI, or API schema. It is immutable by default, uses explicit identifiers, records source provenance when available, returns diagnostics for ordinary invalid input, and avoids reference resolution or proof checking.

# Canonical Types

The implemented canonical types are:

- `SourceLocation`: storage-neutral provenance with optional line and column range.
- `DiagnosticSeverity`: `info`, `warning`, and `error`.
- `Diagnostic`: stable code, severity, message, optional source, related identifier, and details.
- `Identifier`: stable, case-sensitive identifier value.
- `Reference`: unresolved typed reference to an identifier and optional expected target kind.
- `Representation`: representation content.
- `RepresentationalStructure`: structure over referenced representations.
- `Interpretation`: meaning assigned to a referenced representation.
- `Investigation`: question and optional scope.
- `Claim`: claim statement.
- `Assumption`: assumption statement.
- `Evidence`: evidence description and optional citations.
- `Operation`: operation description with input and output references.
- `ReasoningStep`: ordered step with optional operation, premises, conclusions, and rationale.
- `Dependency`: local dependency record between references.
- `Proof`: proof record referencing a claim, steps, assumptions, and evidence.
- `ReasoningGraph`: graph nodes and edges as data only.
- `FARDocument`: local aggregate containing one investigation and IR collections.

# Identifier Model

Identifiers must be non-empty and match `^[A-Za-z][A-Za-z0-9_.:-]*$`. They are case-sensitive, stable, and never silently normalized. Equality is deterministic dataclass equality over the exact identifier string.

# Reference Model

A reference records the referenced `Identifier`, an optional expected `IRKind`, and optional `SourceLocation`. Prompt 1 does not resolve references; it only validates local reference shape.

# Provenance Model

`SourceLocation` records a source label and optional one-based line and column ranges. Invalid ranges produce diagnostics rather than parser exceptions.

# Graph Representation

Graph data is represented by `GraphNode`, `GraphEdge`, and `ReasoningGraph`. The minimum Phase 3 MVP node taxonomy is: representation, structure, interpretation, investigation, claim, assumption, evidence, operation, reasoning step, and proof.

The minimum Phase 3 MVP edge taxonomy is: depends_on, supports, contradicts, interprets, scopes, transforms, derives, cites, and records. This taxonomy is not claimed to be mathematically exhaustive.

# Validation Invariants

Local validation covers identifier validity, required text fields, source ranges, non-negative reasoning-step order, duplicate identifiers inside one `FARDocument`, duplicate graph node identifiers, and local reference object shape.

Validation deliberately does not cover reference resolution, dependency cycles, proof verification, graph reachability, schema validation, parser errors, or execution semantics.

# Diagnostic Model

Diagnostics contain stable codes, severity, human-readable messages, optional source location, optional related identifier, and optional details. The initial IR registry is limited to invalid identifiers, missing required fields, duplicate local identifiers, invalid enum values, invalid internal object shape, and invalid source ranges.

# Serialization Independence

The IR uses Python dataclasses, tuples, enums, and immutable metadata mappings. It does not expose JSON or YAML conversion behavior and does not require JSON/YAML-compatible metadata values.

# Deferred Semantics

Phase 3 Prompt 1 defers parser semantics, normalization, serialization, schemas, graph validation, dependency validation, reference resolution, proof checking, CLI behavior, API behavior, storage, and execution.
