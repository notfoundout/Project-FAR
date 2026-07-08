# Dependency Infrastructure

## Purpose

The v0.4 dependency infrastructure records explicit repository-level dependencies in a machine-readable form. It supports later impact analysis, semantic consistency auditing, knowledge graphs, visualization, and query tooling without changing Project FAR theory content.

This infrastructure is intentionally conservative. It records dependencies that are visible from repository structure, generated artifacts, workflow commands, and documented references. It does not infer controversial semantic dependencies.

## Schema

The dependency schema is maintained at [`theory/dependencies/dependency-schema.yaml`](../../theory/dependencies/dependency-schema.yaml).

Each record contains:

- `id`
- `source`
- `source_type`
- `target`
- `target_type`
- `relationship`
- `confidence`
- `status`
- `evidence`
- `notes`

The schema restricts source and target types, relationships, statuses, and confidence values so downstream tools can validate and query dependency data consistently.

## Registry

The dependency registry is maintained at [`theory/dependencies/dependency-registry.yaml`](../../theory/dependencies/dependency-registry.yaml).

The initial registry is seeded only with high-confidence dependencies from existing repository structure. Examples include proof-object files depending on the theorem catalog they prove against, reports referencing registries they summarize, tools generating reports they explicitly write, the README command center referencing generated reports, workflows invoking visible Make targets or tools, and release documents documenting releases.

## Validator

Run the validator with:

```bash
python tools/check_dependency_registry.py
```

The validator checks that:

- the registry exists;
- the schema exists;
- required fields are present;
- repository-path sources and targets exist;
- relationship values are allowed;
- source and target types are allowed;
- status values are allowed;
- confidence values are allowed;
- dependency IDs are unique;
- self-dependencies are not present unless explicitly justified in notes.

## Report Generator

Run the report generator with:

```bash
python tools/generate_dependency_report.py
```

It writes [`docs/reports/dependency-report.md`](../reports/dependency-report.md), including counts by type and relationship, high-confidence dependencies, provisional and needs-review records, orphan-like registry nodes, top referenced targets, and known limitations.

## Graph Generator

Run the graph generator with:

```bash
python tools/generate_dependency_graph.py
```

It writes:

- [`docs/reports/dependency-graph.json`](../reports/dependency-graph.json)
- [`docs/reports/dependency-graph.mmd`](../reports/dependency-graph.mmd)

The JSON graph contains `metadata`, `nodes`, and `edges`. The Mermaid graph groups nodes by type to keep the initial visualization readable.

## Future v0.4 Consumption Rules

Future v0.4 tools should consume dependency data as explicit repository evidence. They may:

- trace file-level or artifact-level impact;
- identify missing or stale generated outputs;
- compare registry records with references discovered by search;
- visualize accepted, generated, provisional, and needs-review relationships separately;
- flag candidate inconsistencies for review.

Future tools must preserve status and confidence distinctions. A `generated` or `provisional` dependency is not equivalent to an accepted theory dependency.

## What Not to Infer Automatically

Do not automatically infer:

- new primitives;
- changes to definitions, axioms, theorem statements, or proof objects;
- semantic equivalence between artifacts;
- contradiction between artifacts without direct textual evidence;
- dependency direction from citation order alone;
- accepted theory status from generated reports;
- evaluation conclusions from graph centrality or registry connectivity.

Unknown, incomplete, or absent dependency data should remain explicit rather than being filled with speculative edges.
