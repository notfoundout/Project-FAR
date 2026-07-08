# Dependency Report

Generated from [theory/dependencies/dependency-registry.yaml](../../theory/dependencies/dependency-registry.yaml) using [tools/generate_dependency_report.py](../../tools/generate_dependency_report.py).

This report is repository-infrastructure evidence only. It does not infer controversial semantic dependencies or alter accepted theory content.

## Registry Inputs

- Schema: [theory/dependencies/dependency-schema.yaml](../../theory/dependencies/dependency-schema.yaml)
- Registry: [theory/dependencies/dependency-registry.yaml](../../theory/dependencies/dependency-registry.yaml)

## Summary

- Dependency records: 21
- Registry nodes: 30
- Registry edges: 21

## Counts by Source Type

| Value | Count |
|---|---:|
| `document` | 2 |
| `proof_object` | 5 |
| `release` | 2 |
| `report` | 3 |
| `tool` | 5 |
| `workflow` | 4 |

## Counts by Target Type

| Value | Count |
|---|---:|
| `document` | 3 |
| `registry` | 2 |
| `release` | 1 |
| `report` | 6 |
| `theorem` | 5 |
| `tool` | 4 |

## Counts by Relationship

| Value | Count |
|---|---:|
| `depends_on` | 5 |
| `documents` | 2 |
| `generates` | 5 |
| `references` | 5 |
| `uses` | 4 |

## High-Confidence Dependencies

Dependency details are generated from the registry. Run `python tools/generate_dependency_report.py` to refresh this report.

## Provisional Dependencies

| ID | Source | Relationship | Target | Evidence |
|---|---|---|---|---|
| None |  |  |  |  |

## Needs-Review Dependencies

| ID | Source | Relationship | Target | Evidence |
|---|---|---|---|---|
| None |  |  |  |  |

## Known Limitations

- The registry is intentionally seeded from explicit repository structure only.
- Absence of a dependency record does not imply absence of a real dependency.
- Relationship labels are infrastructure classifications, not final semantic conclusions.
- Generated graph outputs are derived from registry records and inherit registry incompleteness.
- Future v0.4 tooling must distinguish accepted evidence from provisional or needs-review records.
