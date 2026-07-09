# Executive Summary

This report records the repository-wide rerun of the Project FAR Dependency Audit after the full theorem-validation chain was supplied as accepted foundation.

Accepted foundation for this rerun: AX-001; all canonical definitions; L-001 through L-008; P-001 through P-008; T-001 through T-015; Isolation Classification doctrine; Foundation Consistency Audit; Canonical Mathematics Audit; Definition Audit; Repository Health Verification; and Phase 1 Boundary Repair.

This audit consumes prior accepted evidence and does not repeat theorem validation, create new mathematics, create new theorems, create new lemmas, or create new propositions.

The repository dependency model is now consistent after two proof-object status synchronizations: T-014 and T-015 proof objects were still marked draft while theorem metadata and accepted validation context treat them as established. They were synchronized to accepted status only. No theorem statement, proof argument, dependency set, or mathematical substance was changed.

# Prior Audit Comparison

The previous dependency audit found that the dependency records themselves were broadly synchronized, but the Phase 1 accepted-foundation boundary was incomplete because L-008 and T-013 through T-015 had not yet been validated inside the supplied accepted foundation.

That earlier finding was correct for its execution context. It identified a process-boundary problem rather than a demonstrated mathematical dependency-graph defect. Its blocking issues were:

1. T-005 depended on L-008 while the then-supplied accepted boundary stopped at L-007.
2. T-013, T-014, and T-015 were registered as established theorem records while the then-supplied accepted boundary stopped at T-012.

This rerun differs because the accepted foundation now explicitly includes L-008 and T-013 through T-015. Therefore the earlier Phase 1 boundary issue is resolved.

# Dependency Inventory

Repository dependency-bearing artifacts audited in this rerun include:

- theorem metadata in `theory/metadata/theorems.yaml`;
- lemma metadata in `theory/metadata/lemmas.yaml`;
- proposition metadata in `theory/metadata/propositions.yaml`;
- canonical dependency graph in `theory/dependencies/dependency-graph.md`;
- theorem proof objects in `theory/proof-objects/T-001.proof.yaml` through `theory/proof-objects/T-015.proof.yaml`;
- generated axiom, definition, lemma, proposition, and theorem indexes in `theory/metadata/generated-*.md`;
- validation reports in `docs/reports/*validation-report.md`, `docs/reports/*audit.md`, and boundary-repair reports relevant to accepted foundation state;
- repository dependency registry in `theory/dependencies/dependency-registry.yaml`;
- generated registry-derived dependency graph and report in `docs/reports/dependency-graph.json`, `docs/reports/dependency-graph.mmd`, and `docs/reports/dependency-report.md`.

Inventory status:

- AX-001 / A1-A5 are present as accepted foundation identifiers.
- L-001 through L-008 are present in lemma metadata and dependency graph.
- P-001 through P-008 are present as established propositions in metadata and dependency graph.
- T-001 through T-015 are present as established theorems in metadata and dependency graph.
- P-009 remains proposed and is not part of the accepted Phase 1 foundation boundary.

# Logical Dependency Audit

Logical dependencies in lemma, proposition, and theorem metadata were compared against the canonical dependency graph and accepted validation reports.

Lemma logical dependencies:

| Artifact | Logical dependencies | Status |
| --- | --- | --- |
| L-001 | A1, D-REP | Consistent |
| L-002 | A2, D-STRUCT | Consistent |
| L-003 | A3, D-INT | Consistent |
| L-004 | A4, D-INV | Consistent |
| L-005 | A5, D-CALC | Consistent |
| L-006 | D-REP, D-STRUCT, D-INT, D-CALC | Consistent |
| L-007 | D-REP, D-STRUCT, D-INT, D-CALC | Consistent |
| L-008 | D-REP, D-CALC | Consistent with accepted L-008 revision; prior D-STRUCT inflation is absent |

Proposition logical dependencies:

| Artifact | Logical dependencies | Status |
| --- | --- | --- |
| P-001 | A1, D-REP | Consistent |
| P-002 | A2, D-REP, D-STRUCT | Consistent |
| P-003 | D-REP, D-INT | Consistent |
| P-004 | D-INV, D-INT, D-CALC | Consistent |
| P-005 | D-CALC, D-INV | Consistent |
| P-006 | D-STRUCT, D-INT, P-003 | Consistent |
| P-007 | D-REP, D-STRUCT, D-CALC | Consistent |
| P-008 | D-CALC, D-STRUCT | Consistent |

Theorem logical dependencies:

| Artifact | Logical dependencies | Status |
| --- | --- | --- |
| T-001 | L-001, L-002, L-003, L-004, L-005 | Consistent |
| T-002 | T-001, L-001, L-002, L-003, L-004, L-005 | Consistent |
| T-003 | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | Consistent |
| T-004 | DEF-030, DEF-031, DEF-034 | Consistent |
| T-005 | D-CALC, L-008, T-003 | Consistent now that L-008 is accepted |
| T-006 | derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | Consistent; graph uses the human-readable label `derived-concept registry` |
| T-007 | T-003, T-006 | Consistent |
| T-008 | L-006, T-004 | Consistent |
| T-009 | L-007 | Consistent |
| T-010 | T-003, T-004, P-007 | Consistent |
| T-011 | T-006, definition-policy | Consistent; graph uses the human-readable phrase `definition policy` |
| T-012 | FAR-model-theory | Consistent; graph uses the human-readable phrase `FAR model theory` |
| T-013 | D-CALC | Consistent with accepted T-013 revision; prior T-005 inflation is absent |
| T-014 | D-CALC | Consistent with accepted T-014 revision; prior T-005 inflation is absent |
| T-015 | T-003, T-007, FAR-model-theory | Consistent |

No inflated logical dependency remains in the accepted metadata. No missing logical dependency was demonstrated by this audit.

# Informative Dependency Audit

Informative dependencies identified by prior accepted validation evidence are not encoded as logical metadata dependencies. This is consistent with the repository's current dependency model, which records direct logical dependencies in lemma, proposition, theorem metadata, and the canonical dependency graph.

Accepted informative classifications confirmed in this rerun:

- L-008 no longer records D-STRUCT as a logical dependency; prior accepted evidence classified D-STRUCT as informative for L-008.
- T-013 no longer records T-005 as a logical dependency; prior accepted evidence classified T-005 as informative for T-013.
- T-014 no longer records T-005 as a logical dependency; prior accepted evidence classified T-005 as informative for T-014.

No informative dependency was found to be incorrectly retained as a required logical dependency.

# Historical Dependency Audit

Historical dependencies and prior audit history remain in validation and audit reports rather than canonical logical dependency metadata. This is consistent with the current repository model.

Historical records audited include the previous dependency audit, the Phase 1 Boundary Repair Report, L-008 validation, T-013 validation, and T-014 validation. Those reports preserve why earlier dependency states were revised without requiring old dependencies to remain in canonical logical metadata.

No historical dependency was found masquerading as a current logical dependency.

# Graph Consistency Audit

The canonical dependency graph agrees with lemma, proposition, and theorem metadata after normalizing three prose labels:

- `derived-concept registry` corresponds to metadata `derived-concept-registry`.
- `definition policy` corresponds to metadata `definition-policy`.
- `FAR model theory` corresponds to metadata `FAR-model-theory`.

The graph contains no self-dependencies among audited accepted artifacts. The theorem ordering rule is respected: no theorem T-001 through T-015 depends on a later-numbered theorem. The only theorem-to-theorem edges point backward or to accepted earlier artifacts.

The registry-derived generated graph and report validate separately through repository tooling. They describe repository-structure dependencies and do not conflict with canonical logical dependency metadata.

# Proof Dependency Audit

Proof-object dependency synchronization was audited for T-001 through T-015.

Proof objects for T-001 through T-013 were already synchronized with accepted status. T-014 and T-015 proof objects still carried `status: draft` even though theorem metadata lists them as established and this rerun's accepted foundation includes T-014 and T-015. This was a proof-object synchronization inconsistency, not a mathematical proof change.

Repair performed:

- `theory/proof-objects/T-014.proof.yaml` status changed from `draft` to `accepted`.
- `theory/proof-objects/T-015.proof.yaml` status changed from `draft` to `accepted`.

After this repair, proof-object status agrees with theorem metadata and the accepted validation context. No proof-object premise, step, conclusion, theorem statement, or dependency edge was changed.

# Repairs Performed

Repairs were limited to demonstrated synchronization inconsistencies:

1. Synchronized T-014 proof-object status to `accepted`.
2. Synchronized T-015 proof-object status to `accepted`.
3. Regenerated dependency and theorem/index outputs with repository tooling; no substantive generated dependency changes were required beyond normal confirmation of current metadata.
4. Added this rerun audit report.

No mathematical content was strengthened. No mathematical content was weakened. No accepted proof was rewritten. No new theorem, lemma, proposition, or definition was created.

# Remaining Issues

No blocking dependency-model issues remain.

Non-blocking observations:

1. The canonical dependency graph uses prose labels for three metadata identifiers, but repository checks pass and the mapping is unambiguous.
2. Informative and historical dependency classifications remain report-level classifications rather than machine-readable metadata fields. This is not inconsistent with the current repository model.
3. P-009 remains proposed and outside the accepted Phase 1 foundation boundary.

Newly introduced issues: none found.

Pre-existing warnings: none blocking the dependency model were found by the required checks.

# Final Dependency Status

The previous Phase 1 boundary issue is resolved because L-008 and T-013 through T-015 are now included in the accepted foundation consumed by this rerun.

Phase 1 Step 7, Proof Audit, may begin after review and acceptance of this rerun audit.

DEPENDENCY GRAPH CONSISTENT
