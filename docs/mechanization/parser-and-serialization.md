# Purpose

This document describes the Prompt 3 parser, normalization, and deterministic serialization pipeline for Project FAR mechanization.

# Supported Formats

The parser supports JSON text, JSON files, YAML text, and YAML files for the same `far-ir/1.0` external contract.

# Parsing Pipeline

The pipeline is: input acquisition, format detection or explicit format selection, syntax parsing, root-type validation, JSON Schema validation, typed external-model construction, canonical IR conversion, local IR validation, normalization, and parse-result construction.

# Format Detection

Explicit format selection takes precedence. File extensions `.json`, `.yaml`, and `.yml` are recognized. Unknown extensions and ambiguous content produce diagnostics instead of silently selecting a parser.

# Schema Validation

Parsed primitive data is validated against `schemas/far-document.schema.json` using the declared `jsonschema` interface. Diagnostics include deterministic error ordering and path/schema-path details when available.

# External Model Construction

Validated primitive data is converted into Prompt 2 typed external models. Raw dictionaries are not used after typed construction except for metadata and extensions.

# Canonical IR Conversion

Typed external models convert to canonical IR through the Prompt 2 conversion layer. Canonical local IR validation still executes after external shape validation.

# Source Provenance

Parser diagnostics include the source path or source label and line/column information when supplied by the JSON or YAML parser. User-authored `SourceLocation` values inside documents remain distinct and are not overwritten by parser-origin metadata.

# Normalization

Normalization is structural, deterministic, and idempotent. It preserves identifiers and reasoning-step order while sorting unordered collections and metadata/extension keys for stable output.

# JSON Serialization

JSON serialization uses UTF-8 text, two-space indentation, sorted keys, Unicode preservation, no NaN/Infinity, and a terminal newline.

# YAML Serialization

YAML serialization uses PyYAML safe dumping, safe loading compatibility, deterministic key ordering, no Python-specific tags, no intentional aliases, Unicode preservation, and a terminal newline.

# Round-Trip Guarantees

Normalized JSON and YAML output parse back to equal canonical IR. Cross-format round trips compare canonical IR equality, not byte equality with original unnormalized input.

# Diagnostic Model

Parser and serializer failures use the existing structured diagnostic model. Ordinary invalid input returns diagnostics rather than crashing the process.

# Security Considerations

YAML uses safe loading and dumping. The parser does not permit arbitrary object construction. Input-size limits are deferred. Document content is never executed. Untrusted files are read as UTF-8 text and syntax/schema failures are reported as diagnostics.

# Deferred Features

Cross-reference resolution, dependency-cycle detection, graph reachability, proof verification, CLI commands, REST API, storage, and arbitrary operation execution remain deferred.
