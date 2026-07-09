# Dependency Audit

## Executive Summary

This report records the Phase 1 Step 6 repository-wide Dependency Audit for Project FAR.

The audit inspected the canonical dependency graph and theorem metadata. It found broad synchronization between `theory/metadata/theorems.yaml` and `theory/dependencies/dependency-graph.md` for T-001 through T-015.

However, the Phase 1 accepted-foundation assumption for this audit covers AX-001, accepted definitions, L-001 through L-007, P-001 through P-008, and T-001 through T-012. The repository metadata and dependency graph also register T-013, T-014, and T-015 as `Established` theorems.

That is a blocker for declaring the dependency graph fully consistent at the Phase 1 foundation-freeze boundary, because the canonical dependency registry currently contains established theorem records outside the accepted validation scope used for Phase 1.

No dependency metadata was changed in this report because reclassifying, validating, or deprecating T-013 through T-015 is a mathematical/governance decision outside this audit-only repair scope.

Final status: **DEPENDENCY GRAPH INCONSISTENT**.

## Dependency Inventory

The dependency graph records:

- primitive definition aliases: D-INV, D-REP, D-STRUCT, D-INT, D-CALC;
- core axioms: A1 through A5;
- propositions: P-001 through P-008;
- lemmas: L-001 through L-008;
- theorems: T-001 through T-015.

The theorem metadata records:

- T-001 through T-015 as `Established`.

This inventory is larger than the Phase 1 accepted foundation list supplied to this audit, which ends at T-012 and L-007.

## Logical Dependency Audit

The following theorem dependency records were checked for metadata/graph synchronization:

| Artifact | Metadata Dependencies | Graph Dependencies | Synchronization |
| --- | --- | --- | --- |
| T-001 | L-001, L-002, L-003, L-004, L-005 | L-001, L-002, L-003, L-004, L-005 | PASS |
| T-002 | T-001, L-001, L-002, L-003, L-004, L-005 | T-001, L-001, L-002, L-003, L-004, L-005 | PASS |
| T-003 | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | PASS |
| T-004 | DEF-030, DEF-031, DEF-034 | DEF-030, DEF-031, DEF-034 | PASS |
| T-005 | D-CALC, L-008, T-003 | D-CALC, L-008, T-003 | PASS |
| T-006 | derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | derived-concept registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | PASS with naming normalization note |
| T-007 | T-003, T-006 | T-003, T-006 | PASS |
| T-008 | L-006, T-004 | L-006, T-004 | PASS |
| T-009 | L-007 | L-007 | PASS |
| T-010 | T-003, T-004, P-007 | T-003, T-004, P-007 | PASS |
| T-011 | T-006, definition-policy | T-006, definition policy | PASS with naming normalization note |
| T-012 | FAR-model-theory | FAR model theory | PASS with naming normalization note |
| T-013 | D-CALC, T-005 | D-CALC, T-005 | PASS but outside Phase 1 accepted-foundation scope |
| T-014 | D-CALC, T-005 | D-CALC, T-005 | PASS but outside Phase 1 accepted-foundation scope |
| T-015 | T-003, T-007, FAR-model-theory | T-003, T-007, FAR model theory | PASS but outside Phase 1 accepted-foundation scope |

The graph and metadata are largely synchronized, but the presence of T-013 through T-015 as established records creates a Phase 1 scope inconsistency.

## Informative Dependency Audit

The dependency graph primarily records direct dependencies rather than a full informative/historical classification table. Earlier validation reports classify several dependencies as informative or historical, but those classifications are not uniformly represented in `theory/dependencies/dependency-graph.md`.

No repair was made because this audit did not establish an existing repository rule requiring the graph to encode informative/historical edges.

Non-blocking issue: a later dependency-model audit should decide whether the dependency graph should represent only direct logical dependencies or all classified dependency relations.

## Historical Dependency Audit

Historical dependencies are preserved mainly in validation reports rather than in the dependency graph.

No direct graph inconsistency was found for historical dependencies because the current graph does not appear to be designed as a historical-edge registry.

Non-blocking issue: if historical dependencies are expected to be machine-readable, a separate metadata design decision is required.

## Graph Consistency Audit

The graph is internally ordered and does not visibly cite higher-numbered theorems from lower-numbered theorems.

No self-citation was found in the inspected theorem dependency records.

Potential blocker:

- T-005 depends on L-008, while the accepted Phase 1 foundation supplied to this audit includes L-001 through L-007. Because L-008 appears in the dependency graph and is used by an established theorem, Phase 1 cannot claim a complete dependency audit while excluding L-008 from the accepted foundation unless L-008 is explicitly reclassified, validated, or removed from the established dependency chain.

This is separate from T-013 through T-015 and strengthens the conclusion that the dependency graph is not fully consistent with the stated Phase 1 accepted-foundation boundary.

## Proof Dependency Audit

This connector-executed audit did not run local proof-object tooling. It inspected the repository metadata and dependency graph available through the GitHub connector.

Known limitation: proof-object synchronization must be confirmed by repository checks or a later proof audit.

No proof dependency repair was made here.

## Repairs Performed

No repairs were performed.

Reason: the observed issues are not simple metadata typos. They involve foundation-boundary decisions:

1. L-008 is present as a dependency of T-005 but was not included in the accepted Phase 1 foundation list supplied to this audit.
2. T-013 through T-015 are registered as established theorems but were not included in the accepted Phase 1 theorem-validation chain ending at T-012.

Resolving those issues requires one of the following future actions:

- validate L-008 and T-013 through T-015;
- explicitly classify them as post-Foundation-1.0 artifacts;
- deprecate or demote them from established status;
- revise the Phase 1 accepted-foundation boundary to include them, with evidence.

## Remaining Issues

Blocking issues:

1. `L-008` appears in the dependency graph and is a declared dependency of established T-005, but the Phase 1 accepted foundation supplied to this audit includes only L-001 through L-007.
2. `T-013`, `T-014`, and `T-015` are registered as `Established` in theorem metadata and dependency graph, but the Phase 1 accepted foundation supplied to this audit ends at T-012.

Non-blocking issues:

1. The dependency graph uses human-readable labels such as `derived-concept registry`, `definition policy`, and `FAR model theory`, while metadata uses identifier-like labels such as `derived-concept-registry`, `definition-policy`, and `FAR-model-theory`.
2. Informative and historical dependency classifications are not uniformly encoded in the dependency graph.
3. Proof-object dependency consistency was not mechanically checked in this connector execution.

## Final Dependency Status

**DEPENDENCY GRAPH INCONSISTENT**

Phase 1 Step 7, Proof Audit, should not begin until the Phase 1 foundation boundary is repaired or clarified.
