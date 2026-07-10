# Implemented Capabilities

Phase 3 implements canonical IR records, local validation, structured diagnostics, the `far-ir/1.0` external model and schema, JSON/YAML parsing, deterministic normalization and serialization, reference resolution, graph construction, dependency validation, cycle detection, reachability, graph statistics, CLI commands, conformance execution, and end-to-end regression tests.

# Unsupported Capabilities

Unsupported capabilities include semantic proof verification, operation execution semantics, automated reasoning, proof search, REST APIs, persistent storage, distributed execution, web interfaces, plugin systems, production hardening, and independent external implementations.

# Public Python APIs

Public APIs include `parse_file`, `parse_document`, `parse_json_text`, `parse_yaml_text`, `serialize_json`, `serialize_yaml`, `build_graph`, `resolve_references`, `validate_graph`, `validate_dependencies`, `detect_cycles`, `compute_reachability`, `dependency_closure`, `graph_statistics`, and `run_conformance`.

# CLI Commands

The `far` CLI exposes `validate`, `parse`, `normalize`, `graph`, `diagnostics`, `stats`, `export`, `inspect`, `conformance`, `version`, and `help`.

# Versions

Format version: `far-ir/1.0`. Package version: `0.6.0`. CLI version: `0.6.0`.

# Test and Conformance Counts

The Phase 3 mechanization suite contains 69 pytest tests plus 12 subtests. The conformance suite contains 58 cases; the completion run reported 58 passed and 0 failed.

# Known Limitations

The implementation is an MVP. It intentionally omits proof checking, automated reasoning, operation execution, REST/API/storage layers, production hardening, and independent external implementation validation.

# Next Phase Boundary

Phase 4 should build a reference implementation and applied engine on top of the Phase 3 parsing, IR, graph, dependency, diagnostics, CLI, and conformance foundations without changing Foundation v1.0 mathematics.
