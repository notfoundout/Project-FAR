# Theory Impact Analysis

## Purpose

The Theory Impact Analyzer predicts the downstream repository impact of changing a registered artifact. It is a maintenance tool, not a theory artifact, and it does not alter FAR theory, definitions, proofs, theorem text, or registries.

The analyzer writes `docs/reports/theory-impact-report.md` from `theory/dependencies/dependency-registry.yaml`.

## Algorithm

1. Load `theory/dependencies/dependency-registry.yaml`.
2. Treat each dependency record as a directed registry edge from `source` to `target`.
3. For impact analysis, traverse downstream through reverse edges: if `A` depends on `B`, then a change to `B` can affect `A`.
4. Use breadth-first traversal to compute the minimum dependency depth for each affected node.
5. Count directly affected nodes at depth 1 and indirectly affected nodes at depth greater than 1.
6. Aggregate relationship, confidence, and status values only from traversed registry records.
7. Sort all output deterministically.

## Traversal Rules

- The registry is the only input.
- The analyzer never scans repository content to infer new dependency edges.
- The analyzer never infers semantic dependence from file names, links, proof text, or directory placement.
- Direct impact means a registry record has the queried node as `target` and another node as `source`.
- Indirect impact means the analyzer reaches a node through one or more intermediate registered dependencies.
- Dependency depth is the shortest registered reverse-edge distance from the queried node to an affected node.

## Diagnostics

The report includes checks for:

- circular dependency chains;
- broken references to missing repository paths;
- dependency records missing `source` or `target` nodes;
- duplicate dependency IDs;
- registered nodes with no incoming edges;
- registered nodes with no outgoing edges;
- orphan registry entries under the analyzer definition.

## Limitations

The analyzer reports registered structural impact only. Results are based only on registered dependencies and do not imply semantic dependence.

Important consequences:

- If the registry omits an edge, the analyzer treats the impact as unknown rather than absent.
- If the registry includes a provisional or generated edge, the analyzer reports it with its recorded status rather than promoting it to accepted theory.
- File existence diagnostics do not validate mathematical, philosophical, or proof correctness.
- The analyzer does not rank intellectual importance; it ranks registered downstream reachability.

## Why Registry Evidence Is Authoritative

Project FAR v0.4 introduced the dependency registry as the explicit repository evidence source for dependency tooling. For this analyzer, registry evidence is authoritative because the objective is to measure impact from accepted registry records without introducing unsupported assumptions. This preserves reproducibility and prevents automation from silently creating semantic claims.

## Future Semantic Expansion

Future work may add semantic impact analysis only if a separate accepted evidence source is introduced through the Project FAR research lifecycle. Any future semantic analyzer should remain separate from this registry-only tool unless the registry schema is explicitly expanded to encode semantic dependencies with auditable provenance.
