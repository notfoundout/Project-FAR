# Schemas

This directory contains canonical machine-readable interchange schemas for Project FAR mechanization.

`far-document.schema.json` defines the historical/current `far-ir/1.0` external FAR reasoning-document contract. The schema is an interchange contract for JSON documents and for YAML documents that serialize the same data model. It is distinct from Foundation v1.0 and does not modify accepted theory. W3 preserves this file and its semantics; it is not silently reinterpreted.

`far-contract-v2.schema.json` defines the `far-ir/2.0` comparison-contract successor introduced by `PCA-W3-CONTRACT-SCHEMA`. It explicitly records contract identity/version, source/case domain, required behavior, representation, observation contexts, admitted transformations/equivalences, interpretation profile, target/model class, frame, typed outcome including `Unknown`, factorization/collision/quotient evidence, failure reporting, provenance/freeze metadata, and optional approximation/loss/cost declarations. W3's semantic verifier recomputes checked finite-explicit witnesses. Abstract declarations and v1 migrations cannot self-certify a theorem result.

Core typed objects reject unknown fields with `additionalProperties: false`. Extensibility is available only through explicit `extensions` mappings. The v2 `legacy_document` field is a migration envelope: migration first validates the embedded primitive payload against the unchanged v1 schema, preserves it exactly as primitive data, and marks contract semantics absent from v1 as `Unknown`.

The v1 schema remains used by its executable parser, normalizer, serialization, graph, CLI, and conformance suite. `far-ir/2.0` is intentionally separate: `mechanization.far_mechanization.contract_v2` validates its schema and finite-explicit comparison evidence, `migrate_v1_to_v2` performs loss-explicit migration, and `contract_conformance` runs the registered v2 fixtures.

Both schemas use JSON Schema Draft 2020-12 and local `#/$defs/...` references only; ordinary validation must not fetch remote schemas. Software conformance is assurance for the encoded contract, not mathematical proof of application correspondence, novelty, empirical utility, or contract-free universality.

`far-contract-v2.1.schema.json` is the additive `far-ir/2.1` W5 successor for checked finite-explicit approximation and cost semantics. It does not alter either predecessor. `mechanization.far_mechanization.contract_v21` recomputes exact-rational losses, feasibility, Pareto minima, least elements, and exact recovery.
