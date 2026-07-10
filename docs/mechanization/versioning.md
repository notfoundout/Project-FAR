# Purpose

Phase 3 reports distinct version values for different mechanization surfaces.

# Versions

- Foundation version: `v1.0`; this identifies the frozen mathematical foundation boundary.
- Interchange format version: `far-ir/1.0`; this identifies the external JSON/YAML contract.
- Schema version: `far-ir/1.0`; the schema implements the interchange contract.
- Mechanization package version: `0.6.0`; this identifies the Phase 3 MVP package code.
- CLI version: `0.6.0`; this identifies the Phase 3 CLI surface.

# Policy

Foundation, schema, package, and CLI versions are not interchangeable. `far version` reports them separately so downstream tools can reason about compatibility without treating all artifacts as Foundation v1.0.
