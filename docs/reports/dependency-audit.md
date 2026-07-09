# Dependency Audit

## Correction Note

This report was previously committed directly to `main` by mistake instead of being introduced through a review branch. This revision repairs that process mistake through the `codex/repair-phase1-dependency-audit-mistake` branch and corrects the report framing without changing theorem, proof, dependency, or mathematical substance.

## Executive Summary

This report records the Phase 1 Step 6 repository-wide Dependency Audit for Project FAR.

The audit inspected the canonical dependency graph and theorem metadata. It found broad synchronization between `theory/metadata/theorems.yaml` and `theory/dependencies/dependency-graph.md` for T-001 through T-015.

The important finding is not that the repository dependency graph is broken merely because the Phase 1 audit plan stopped too early. The dependency graph exposed an incomplete Phase 1 foundation boundary: the Phase 1 accepted-foundation validation scope used for this audit covered AX-001, accepted definitions, L-001 through L-007, P-001 through P-008, and T-001 through T-012, while the repository also contains L-008 and established theorem records T-013, T-014, and T-015.

L-008 must be included in the foundation validation scope because T-005 depends on it. T-013, T-014, and T-015 must be handled before Foundation 1.0 because they are registered as established theorems.

The correct next action is to extend validation to L-008 and T-013 through T-015, not to remove, demote, deprecate, or downgrade those artifacts.

No dependency metadata was changed in this report because validating L-008 or T-013 through T-015 is outside this audit-only repair scope.

Final status: **PHASE 1 FOUNDATION BOUNDARY INCOMPLETE**.

## Dependency Inventory

The dependency graph records:

- primitive definition aliases: D-INV, D-REP, D-STRUCT, D-INT, D-CALC;
- core axioms: A1 through A5;
- propositions: P-001 through P-008;
- lemmas: L-001 through L-008;
- theorems: T-001 through T-015.

The theorem metadata records:

- T-001 through T-015 as `Established`.

This inventory is larger than the Phase 1 accepted foundation list supplied to this audit, which ends at T-012 and L-007. Therefore the validation boundary must be extended before Foundation 1.0 can honestly be frozen.

## Logical Dependency Audit

The following theorem dependency records were checked for metadata/graph synchronization:

| Artifact | Metadata Dependencies | Graph Dependencies | Synchronization |
| --- | --- | --- | --- |
| T-001 | L-001, L-002, L-003, L-004, L-005 | L-001, L-002, L-003, L-004, L-005 | PASS |
| T-002 | T-001, L-001, L-002, L-003, L-004, L-005 | T-001, L-001, L-002, L-003, L-004, L-005 | PASS |
| T-003 | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | PASS |
| T-004 | DEF-030, DEF-031, DEF-034 | DEF-030, DEF-031, DEF-034 | PASS |
| T-005 | D-CALC, L-008, T-003 | D-CALC, L-008, T-003 | PASS; shows L-008 must be in foundation validation scope |
| T-006 | derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | derived-concept registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | PASS with naming normalization note |
| T-007 | T-003, T-006 | T-003, T-006 | PASS |
| T-008 | L-006, T-004 | L-006, T-004 | PASS |
| T-009 | L-007 | L-007 | PASS |
| T-010 | T-003, T-004, P-007 | T-003, T-004, P-007 | PASS |
| T-011 | T-006, definition-policy | T-006, definition policy | PASS with naming normalization note |
| T-012 | FAR-model-theory | FAR model theory | PASS with naming normalization note |
| T-013 | D-CALC, T-005 | D-CALC, T-005 | PASS; established theorem outside incomplete Phase 1 validation boundary |
| T-014 | D-CALC, T-005 | D-CALC, T-005 | PASS; established theorem outside incomplete Phase 1 validation boundary |
| T-015 | T-003, T-007, FAR-model-theory | T-003, T-007, FAR model theory | PASS; established theorem outside incomplete Phase 1 validation boundary |

The graph and metadata are largely synchronized. The issue is that the Phase 1 boundary used for validation was incomplete relative to the established artifacts already registered in the repository.

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

Boundary finding:

- T-005 depends on L-008, while the accepted Phase 1 foundation supplied to this audit includes L-001 through L-007. Because L-008 appears in the dependency graph and is used by an established theorem, Phase 1 cannot claim a complete foundation validation boundary while excluding L-008.

This does not require removing L-008 or changing T-005. It requires extending the Phase 1 validation sequence to include L-008.

## Proof Dependency Audit

This connector-executed audit did not run local proof-object tooling. It inspected the repository metadata and dependency graph available through the GitHub connector.

Known limitation: proof-object synchronization must be confirmed by repository checks or a later proof audit.

No proof dependency repair was made here.

## Repairs Performed

This repair revised the audit framing and final status only.

No theorem, proof, dependency, metadata, or mathematical substance was changed. No mathematical artifacts were removed, demoted, deprecated, downgraded, or validated.

The corrected finding is that the Phase 1 foundation boundary is incomplete:

1. L-008 is present as a dependency of T-005 but was not included in the Phase 1 validation boundary supplied to this audit.
2. T-013 through T-015 are registered as established theorems but were not included in the Phase 1 theorem-validation chain ending at T-012.

The appropriate repair path is to validate the omitted established artifacts before Foundation 1.0, not to alter their status in this PR.

## Remaining Issues

Blocking Phase 1 boundary issues:

1. `L-008` appears in the dependency graph and is a declared dependency of established T-005, but the Phase 1 accepted foundation supplied to this audit includes only L-001 through L-007.
2. `T-013`, `T-014`, and `T-015` are registered as `Established` in theorem metadata and dependency graph, but the Phase 1 accepted foundation supplied to this audit ends at T-012.

Non-blocking issues:

1. The dependency graph uses human-readable labels such as `derived-concept registry`, `definition policy`, and `FAR model theory`, while metadata uses identifier-like labels such as `derived-concept-registry`, `definition-policy`, and `FAR-model-theory`.
2. Informative and historical dependency classifications are not uniformly encoded in the dependency graph.
3. Proof-object dependency consistency was not mechanically checked in this connector execution.

## Corrected Next Validation Sequence

1. Validate L-008.
2. Validate T-013.
3. Validate T-014.
4. Validate T-015.
5. Rerun the dependency audit.
6. Then continue Phase 1 Step 7.

## Final Dependency Status

**PHASE 1 FOUNDATION BOUNDARY INCOMPLETE**

Phase 1 Step 7, Proof Audit, should not begin until the validation boundary has been extended through L-008 and T-013 through T-015, followed by a rerun dependency audit.
