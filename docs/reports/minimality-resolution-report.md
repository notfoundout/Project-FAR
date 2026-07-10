# Minimality Resolution Report

# Executive Summary

This report resolves the focused minimality cases that remained open after the Phase 1 Minimality Audit. It does not freeze Foundation v1.0, does not validate new theorems, and does not rewrite accepted mathematics.

This corrected report consumes the actual `docs/reports/minimality-audit.md` now present on `main`. The prior version of this PR incorrectly stated that the audit file was absent and reconstructed the unresolved set by count-matching. That reconstruction was invalid and is superseded here.

The Phase 1 Minimality Audit classified 126 artifacts: 112 Necessary, 9 Derivable from accepted artifacts, 4 Potentially redundant, and 1 Undetermined. The unresolved cases identified by the audit were:

- Derivable artifacts: DEF-028, DEF-032, DEF-033, DEF-035, DEF-036, P-003, P-004, P-005, and P-006.
- Potentially redundant artifacts: P-001, P-002, P-008, and T-007.
- Undetermined artifact: AX-001.

Resolution summary:

- The 9 derivable artifacts are retained as necessary or expository canonical interfaces.
- The 4 potentially redundant artifacts are not proven removable under accepted dependency and proof structure.
- AX-001 is necessary under current accepted primitive methodology and currently known competitors.
- No artifact is proven redundant and removable.
- No Foundation v1.0 freeze is performed in this PR.

Final status:

FOUNDATION MINIMALITY RESOLVED

# Prior Minimality Audit

The prior audit is `docs/reports/minimality-audit.md`.

It states that the audit covered 126 accepted artifacts: 5 primitives, 89 canonical definitions, AX-001, 8 lemmas, 8 propositions, and 15 theorems.

It classified:

| Classification | Count |
| --- | ---: |
| Necessary | 112 |
| Derivable from accepted artifacts | 9 |
| Potentially redundant | 4 |
| Undetermined | 1 |

The audit did not remove, demote, or rewrite any artifact. Its final status was `FOUNDATION MINIMALITY NOT YET ESTABLISHED` because the listed unresolved cases required focused review.

# Derivable Artifact Review

Derivable status does not by itself imply removability. A derivable artifact may remain justified when it serves as canonical terminology, a named interface, proof-complexity reduction, or dependency-stabilizing boundary.

| Artifact | Audit basis | Final classification | Resolution |
| --- | --- | --- | --- |
| DEF-028 — Represented Object | Derivable from DEF-001 and DEF-027. | Necessary canonical definition | Retain. It provides a canonical term for the object represented by a representation and prevents repeated informal restatement. |
| DEF-032 — Structural Equivalence | Derivable from DEF-025 and DEF-029. | Necessary canonical definition | Retain. It names the structural-equivalence relation used by representation-equivalence reasoning. |
| DEF-033 — Semantic Equivalence | Derivable from DEF-025, DEF-030, and DEF-031. | Necessary canonical definition | Retain. It supplies the canonical semantic-equivalence vocabulary required by semantic preservation and equivalence results. |
| DEF-035 — Representation Transformation | Derivable from DEF-029 and DEF-034. | Necessary canonical definition | Retain. It is the canonical named interface for transformations between representational structures. |
| DEF-036 — Representation Invariance | Derivable from DEF-034. | Necessary canonical definition | Retain. It provides the canonical invariance concept for preservation arguments. |
| P-003 — Semantic Relativity | Derivable from D-REP and D-INT. | Necessary despite derivability | Retain. It is used as a proposition-level interface for semantic-relativity reasoning and supports P-006. |
| P-004 — Investigation Relativity | Derivable from D-INV, D-INT, and D-CALC. | Necessary despite derivability | Retain. It provides a proposition-level bridge connecting investigation, interpretation, and reasoning calculus. |
| P-005 — Calculus Relativity of Admissibility | Derivable from D-CALC and D-INV. | Necessary despite derivability | Retain. It supplies the proposition-level admissibility bridge used by the representation theorem chain. |
| P-006 — Syntax/Semantics Separation | Derivable from D-STRUCT, D-INT, and P-003. | Expository retained result | Retain. It records a distinct named separation result that reduces proof complexity in later semantic/structural arguments. |

No derivable artifact is classified as redundant and removable.

# Potential Redundancy Review

The four potentially redundant artifacts were reviewed using conservative removal tests. A removal test asks whether the artifact can be removed while preserving accepted proof structure, dependency structure, and canonical theorem/proposition interfaces without rewriting accepted mathematics.

| Artifact | Removal test | Final classification | Resolution |
| --- | --- | --- | --- |
| P-001 — Representation Requirement | Removing it breaks T-003's proposition-level dependency structure and collapses A1's representation requirement directly into theorem proof text. | Necessary | Retain. It is not redundant under the accepted proof/dependency architecture. |
| P-002 — Structural Requirement | Removing it breaks T-003's proposition-level dependency structure and removes the named bridge from A2 to representational structure. | Necessary | Retain. It is not redundant under the accepted proof/dependency architecture. |
| P-008 — Resolution Dependence | Removing it would delete the accepted proposition-level statement that resolution depends on calculus/structure even if related content is inferable elsewhere. | Expository retained result | Retain. It is a named result preserving a distinct resolution-dependence interface. |
| T-007 — Primitive Completeness Theorem | Removing it breaks the accepted theorem chain and deletes the theorem-level primitive-completeness result built from T-003 and T-006. | Necessary | Retain. It is not removable without losing an accepted theorem-level result. |

No potentially redundant artifact is proven removable.

# AX-001 Primitive Minimality Review

AX-001 was the one Undetermined case in the Minimality Audit.

The standard applied here is not absolute metaphysical minimality. The relevant standard is:

> Within Project FAR's accepted methodology and currently known competitors, no accepted replacement strictly dominates AX-001.

AX-001 satisfies that standard for Foundation v1.0 purposes:

- Prior primitive-candidate adjudication retained Operation while identifying Transition, Rule-Licensed Transition, and Admissible Transition as live rivals.
- Those rivals remain burden-shifting alternatives rather than accepted replacements because they import unresolved dependence on reasoning state, admissibility, licensing, ordering, rulehood, or representation.
- The AX-001 wording revision avoided operation-adjacent reducers and clarified limits: Operation alone does not supply normativity, semantics, validity, or warrant.
- The AX-001 stability review passed, allowing downstream validation to proceed.
- No accepted current competitor strictly dominates Operation under the accepted primitive methodology.

Final classification:

- AX-001 — Necessary under current accepted primitive methodology.

This does not assert permanent irreducibility. It records that AX-001 is justified for Foundation v1.0 under current evidence and remains open to future primitive-pressure testing.

# Removal Tests

Removal testing was conservative and dependency-preserving. No canonical artifact was deleted or rewritten.

## Test 1 — Remove DEF-028, DEF-032, DEF-033, DEF-035, or DEF-036

Result: fail for Foundation v1.0 removal. Each is derivable, but each provides canonical terminology used to prevent repeated informal restatement and to stabilize representational, semantic, transformation, equivalence, or invariance reasoning. Removing any would reduce terminology stability and force later proofs to inline definitions.

## Test 2 — Remove P-003, P-004, P-005, or P-006

Result: fail for removal. These propositions supply proposition-level interfaces for semantic relativity, investigation relativity, calculus-relative admissibility, and syntax/semantics separation. Removing them would require rewriting accepted proof and dependency structure rather than merely deleting redundancy.

## Test 3 — Remove P-001 or P-002

Result: fail. T-003 depends on proposition-level representation and structural requirements. Removing P-001 or P-002 would collapse proposition structure into theorem proof text and disturb accepted dependency evidence.

## Test 4 — Remove P-008

Result: fail for removal; retain as expository accepted result. P-008 records resolution dependence as a distinct named proposition. It may not be load-bearing for every theorem, but it is not proven removable without loss of named explanatory structure.

## Test 5 — Remove T-007

Result: fail. T-007 is the accepted theorem-level primitive-completeness result built from T-003 and T-006. Removing it would delete a distinct accepted theorem, not merely simplify the foundation.

## Test 6 — Replace AX-001

Result: fail. No currently accepted alternative strictly dominates Operation without shifting unresolved primitive burden elsewhere.

# Final Classifications

| Artifact | Final classification |
| --- | --- |
| DEF-028 | Necessary canonical definition |
| DEF-032 | Necessary canonical definition |
| DEF-033 | Necessary canonical definition |
| DEF-035 | Necessary canonical definition |
| DEF-036 | Necessary canonical definition |
| P-003 | Necessary despite derivability |
| P-004 | Necessary despite derivability |
| P-005 | Necessary despite derivability |
| P-006 | Expository retained result |
| P-001 | Necessary |
| P-002 | Necessary |
| P-008 | Expository retained result |
| T-007 | Necessary |
| AX-001 | Necessary under current accepted primitive methodology |

# Remaining Issues

No focused minimality blocker remains for Foundation v1.0.

Non-blocking future research questions:

1. Future primitive-pressure testing may continue trying to replace AX-001 with a stricter primitive.
2. Future versions may decide whether expository retained results should remain in the frozen foundation or move to an explanatory layer.
3. Future mechanization may expose smaller formal bases, but that does not block Foundation v1.0 under the current accepted methodology.

# Final Minimality Resolution

The focused minimality-resolution criteria are satisfied:

- no artifact is proven removable;
- all nine derivable artifacts identified by the Minimality Audit are justified as necessary or expository retained results;
- all four potentially redundant artifacts identified by the Minimality Audit are resolved;
- AX-001 is justified under the current accepted primitive methodology and currently known competitors;
- Foundation v1.0 is not frozen in this PR.

FOUNDATION MINIMALITY RESOLVED
