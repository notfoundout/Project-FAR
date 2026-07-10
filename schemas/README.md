# Schemas

This directory contains canonical machine-readable interchange schemas for Project FAR mechanization.

`far-document.schema.json` defines the `far-ir/1.0` external FAR document contract. The schema is an interchange contract for JSON documents and for YAML documents that serialize the same data model. It is distinct from Foundation v1.0 and does not modify accepted theory.

Core typed objects reject unknown fields with `additionalProperties: false`. Extensibility is available only through the explicit `extensions` mapping.

The current schema is used by executable Prompt 2 tests and fixtures. Parser, normalization, serialization, graph validation, dependency validation, proof checking, CLI, API, storage, and execution behavior remain deferred.

Prompt 3 parser code validates parsed JSON and YAML primitive data against `far-document.schema.json` before typed external-model construction. YAML is treated as another serialization of the same schema-governed data model.
