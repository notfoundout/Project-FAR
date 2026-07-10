# Purpose

This document records the bounded executable architecture introduced for Phase 3 Prompt 1: a canonical, storage-independent Intermediate Representation (IR) for Project FAR mechanization.

# Frozen Foundation Boundary

Foundation v1.0 artifacts remain frozen. This work does not modify axioms, definitions, lemmas, propositions, theorems, proofs, proof objects, dependency metadata, doctrine, or Foundation v1.0 release documents. The mechanization package represents accepted artifact names without adding new mathematics.

# Repository Architecture Discovered

Inspection found the repository currently uses Python scripts under `tools/`, including `tools/far_core.py` for machine-readable FAR objects and `tools/parse_far.py` for YAML parsing. Repository metadata is stored under `theory/metadata/`, and validation is performed by standalone tools such as `tools/validate_docs.py`, `tools/check_dependencies.py`, and `tools/verify_theory.py`.

The only declared runtime dependency is PyYAML in `requirements.txt`, used by existing parser tooling. No existing package model or dataclass validation dependency was found. The new implementation therefore uses Python 3.11 standard-library dataclasses, enums, immutable mappings, and type hints.

# Mechanization Architecture

Executable Phase 3 IR code lives under `mechanization/far_mechanization/`. The package is intentionally separate from `tools/` parser scripts because this prompt does not implement parser, CLI, storage, API, proof-checking, or execution behavior.

The package introduces only the modules required by Prompt 1:

- `core.py` for identifiers, typed references, IR kind taxonomy, and metadata freezing.
- `diagnostics.py` for source provenance and structured diagnostics.
- `errors.py` for programmer-error exceptions only.
- `ir.py` for immutable canonical IR records and local validation.

# Module Responsibilities

`diagnostics.py` defines `SourceLocation`, `DiagnosticSeverity`, `DiagnosticCode`, and `Diagnostic`. Diagnostics are returned for ordinary invalid input.

`core.py` defines `Identifier`, `Reference`, and `IRKind`. Identifier validation is stable, case-sensitive, and non-normalizing.

`ir.py` defines domain records: `Representation`, `RepresentationalStructure`, `Interpretation`, `Investigation`, `Claim`, `Assumption`, `Evidence`, `Operation`, `ReasoningStep`, `Dependency`, `Proof`, `GraphNode`, `GraphEdge`, `ReasoningGraph`, and `FARDocument`.

`errors.py` defines `FARMechanizationError` for impossible internal states or programmer errors. Ordinary malformed user data is represented by diagnostics instead.

# Dependency Direction

The dependency direction is one-way:

1. `diagnostics.py` has no mechanization package dependencies.
2. `core.py` depends on `diagnostics.py`.
3. `ir.py` depends on `core.py` and `diagnostics.py`.
4. Parser, CLI, schema, storage, and API layers are deferred and must depend on the IR rather than the IR depending on them.

# Error and Diagnostic Policy

Local validation returns tuples of `Diagnostic` instances and does not terminate the process for ordinary invalid user input. Exceptions are reserved for programmer errors, mutation attempts on frozen dataclasses, or impossible internal states.

The Phase 3 Prompt 1 diagnostic registry includes:

- `FAR-IR-001` invalid identifier.
- `FAR-IR-002` missing required field.
- `FAR-IR-003` duplicate local identifier.
- `FAR-IR-004` invalid enum value.
- `FAR-IR-005` invalid internal object shape.
- `FAR-IR-006` invalid source range.

# Deferred Components

This prompt deliberately does not implement parsers, graph validation algorithms, dependency-cycle detection, reference resolution, proof verification, CLI behavior, API behavior, storage, JSON/YAML schemas, or an execution engine.

# Architecture Decision Summary

The implementation reuses repository naming from accepted FAR artifacts and existing Python practice. It introduces an executable package because the existing `tools/` code is parser-oriented and YAML-coupled. The new IR is immutable, diagnostic-oriented, storage-independent, and minimal enough to support later Phase 3 prompts without claiming that later work is complete.

Prompt 3 extends the mechanization package with parser, normalization, and serialization modules. These modules depend on the Prompt 1 canonical IR and Prompt 2 external models; the IR remains independent of JSON, YAML, schema validation, and file I/O.

Prompt 4 extends the package with `graph_engine.py`. The graph engine depends on canonical IR records and diagnostics, constructs executable reasoning graphs, resolves typed references, validates dependencies, computes reachability, detects cycles, and reports graph statistics. It does not implement proof verification, CLI behavior, storage, APIs, or arbitrary operation execution.

Prompt 5 adds `cli.py` and the `far` executable entrypoint. The CLI depends on the parser, normalization, serialization, graph engine, and diagnostic modules. It does not add proof verification, automated reasoning, REST API, or persistent storage.
