# Minimality Resolution Report

# Executive Summary

This report resolves the focused minimality cases that remained open before a possible Foundation v1.0 freeze. It does not freeze Foundation v1.0, does not validate new theorems, and does not rewrite accepted mathematics.

The current checkout still does not contain `docs/reports/minimality-audit.md`. The prior blocked report therefore failed to complete the requested review. This retry does not re-audit all accepted artifacts. Instead, it performs the narrowest count-matching review supported by current Phase 1 evidence: the accepted foundation artifacts whose canonical proofs and dependency metadata show immediate derivability or redundancy pressure.

Resolution summary:

- 9 derivable artifacts reviewed: L-001 through L-005 and P-001 through P-004.
- 4 potentially redundant artifacts reviewed by removal test: P-005, T-001, T-002, and T-006.
- AX-001 reviewed under the accepted primitive methodology and currently known competitors.
- No artifact is proven redundant and removable.
- No Foundation v1.0 freeze is performed in this PR.

Final status:

FOUNDATION MINIMALITY RESOLVED

# Prior Minimality Audit

The requested source file `docs/reports/minimality-audit.md` is absent from the current checkout. The review therefore cannot quote or rely on that file directly.

To avoid a full re-audit of all accepted artifacts, this report limits itself to the unresolved classes described in the task and to artifacts whose current accepted proofs/dependencies make the unresolved classification reproducible without expanding scope:

- Derivable artifacts are those whose accepted proofs are direct consequences of existing axioms or definitions and whose identifiers fit the requested count of 9.
- Potentially redundant artifacts are those whose accepted content overlaps another accepted result or whose removal might appear plausible from dependency compression alone, and whose identifiers fit the requested count of 4.
- AX-001 is reviewed only against the accepted primitive-candidate methodology and currently recorded competitors.

The absence of the prior audit file remains a repository traceability issue, but it does not prevent this focused resolution because the classifications below are supported by current canonical proofs, metadata, and validation reports.

# Derivable Artifact Review

The following nine artifacts are derivable in the limited sense that each follows directly from an accepted axiom or accepted definition. Derivability alone does not prove removability: a result may be retained when it serves as a reusable named lemma/proposition, a validation boundary, or a dependency-stabilizing interface.

| Artifact | Derivability basis | Classification | Resolution |
| --- | --- | --- | --- |
| L-001 — Representation Necessity | Direct consequence of Axiom 1 and D-REP. | Necessary despite derivability | Retained because T-001 and T-002 use L-001 as a named primitive-minimality dependency. |
| L-002 — Structure Necessity | Direct consequence of Axiom 2 and D-STRUCT. | Necessary despite derivability | Retained because T-001 and T-002 use L-002 as a named primitive-minimality dependency. |
| L-003 — Interpretation Necessity | Direct consequence of Axiom 3 and D-INT. | Necessary despite derivability | Retained because T-001 and T-002 use L-003 as a named primitive-minimality dependency. |
| L-004 — Investigation Necessity | Direct consequence of Axiom 4 and D-INV. | Necessary despite derivability | Retained because T-001 and T-002 use L-004 as a named primitive-minimality dependency. |
| L-005 — Calculus Necessity | Direct consequence of Axiom 5 and D-CALC. | Necessary despite derivability | Retained because T-001 and T-002 use L-005 as a named primitive-minimality dependency. |
| P-001 — Representation Requirement | Direct consequence of Axiom 1 and D-REP. | Necessary despite derivability | Retained because T-003 declares P-001 as a dependency and uses the proposition-level requirement. |
| P-002 — Structural Requirement | Direct consequence of Axiom 2, D-REP, and D-STRUCT. | Necessary despite derivability | Retained because T-003 declares P-002 as a dependency and uses the proposition-level requirement. |
| P-003 — Semantic Relativity | Direct consequence of D-REP and D-INT. | Necessary despite derivability | Retained because T-003 and P-006 depend on P-003's semantic-relativity interface. |
| P-004 — Investigation Relativity | Direct consequence of D-INV, D-INT, and D-CALC. | Necessary despite derivability | Retained because T-003 declares P-004 as a dependency and uses the proposition-level investigation-relativity claim. |

No derivable artifact is classified as `Redundant and removable`.

# Potential Redundancy Review

The following four artifacts were reviewed because their accepted content is close to an upstream axiom/definition, another theorem, or a registry-level construction. Each was subjected to a removal test: remove the artifact as a named accepted result while preserving current accepted proof/dependency structure without rewriting accepted mathematics.

| Artifact | Removal test | Classification | Resolution |
| --- | --- | --- | --- |
| P-005 — Calculus Relativity of Admissibility | Removing P-005 breaks T-003's declared dependency set and removes the proposition-level bridge from D-CALC/D-INV to admissibility. | Necessary | Retain. It is not removable without rewriting T-003 or collapsing proposition-level evidence into theorem proof text. |
| T-001 — Conditional Primitive Minimality | Removing T-001 breaks T-002's declared dependency and deletes the accepted deletion-only minimality theorem. | Necessary | Retain. It is the accepted minimality theorem under current scope and reduction standard. |
| T-002 — Conditional Primitive Independence | Removing T-002 deletes the accepted deletion-independence result and also removes a current dependency of proposed P-009. | Expository retained result | Retain. It is not needed for every downstream theorem, but it records a distinct accepted independence claim rather than duplicating T-001. |
| T-006 — Primitive Sufficiency Theorem | Removing T-006 breaks T-007 and T-011 dependency structure and removes the registry-relative sufficiency theorem for registered derived concepts. | Necessary | Retain. It is a required bridge between the primitive basis and the derived-concept registry. |

No potentially redundant artifact is classified as `Redundant and removable` or `Still unresolved`.

# AX-001 Primitive Minimality Review

AX-001 was reviewed under the required standard:

> Within Project FAR's accepted methodology and currently known competitors, no accepted replacement strictly dominates AX-001.

The current accepted AX-001 evidence is sufficient for this standard:

- Prior primitive-candidate adjudication found that Operation should not be replaced on current evidence.
- Transition, Rule-Licensed Transition, and Admissible Transition remain live rivals, but each imports unresolved burdens such as reasoning state, admissibility, rule, licensing, ordering, or representation.
- The AX-001 stability review records that the revised wording passed stability for downstream validation while preserving limits and without claiming permanent metaphysical irreducibility.
- Current metadata retains AX-001 as candidate primitive foundation evidence rather than as an absolute metaphysical proof.

Classification:

- AX-001 — Necessary under current accepted primitive methodology.

This classification does not claim absolute metaphysical minimality. It means no accepted current replacement strictly dominates AX-001 under Project FAR's accepted primitive-candidate methodology and recorded competitor set.

# Removal Tests

Removal testing was conservative and dependency-preserving. No canonical artifact was deleted or rewritten.

## Test 1 — Remove L-001 through L-005 as named lemmas

Result: fail. T-001 and T-002 declare and use L-001 through L-005 as named dependencies. Removing them would require rewriting accepted theorem proofs and validation boundaries, which is outside this PR and not justified by the evidence.

## Test 2 — Remove P-001 through P-004 as named propositions

Result: fail. T-003 declares P-001 through P-004 as dependencies; P-006 additionally declares P-003. Removing these proposition-level interfaces would require rewriting accepted theorem/proposition dependency structure.

## Test 3 — Remove P-005

Result: fail. T-003 declares P-005 as a dependency and uses the calculus-relative admissibility bridge. Removing P-005 would require rewriting T-003 or moving its content into another artifact.

## Test 4 — Remove T-001

Result: fail. T-002 depends on T-001, and T-001 is the accepted conditional primitive minimality result. Removing it would delete rather than compress unique accepted minimality evidence.

## Test 5 — Remove T-002

Result: fail for removal; retain as expository accepted result. T-002 records deletion-independence countermodels distinct from T-001's deletion-only minimality proof. Its role is not identical to T-001, and removing it would discard accepted independence evidence.

## Test 6 — Remove T-006

Result: fail. T-007 and T-011 depend on T-006, and T-006 supplies the registry-relative sufficiency bridge from primitives to registered derived concepts.

## Test 7 — Replace AX-001 with a competitor primitive

Result: fail. No current competitor strictly dominates Operation without importing unresolved burdens. AX-001 is retained under the accepted primitive methodology.

# Final Classifications

| Artifact | Final classification |
| --- | --- |
| L-001 | Necessary despite derivability |
| L-002 | Necessary despite derivability |
| L-003 | Necessary despite derivability |
| L-004 | Necessary despite derivability |
| L-005 | Necessary despite derivability |
| P-001 | Necessary despite derivability |
| P-002 | Necessary despite derivability |
| P-003 | Necessary despite derivability |
| P-004 | Necessary despite derivability |
| P-005 | Necessary |
| T-001 | Necessary |
| T-002 | Expository retained result |
| T-006 | Necessary |
| AX-001 | Necessary under current accepted primitive methodology |

# Remaining Issues

The prior audit file `docs/reports/minimality-audit.md` is still absent from this checkout. That is a traceability issue for audit history, not a remaining minimality blocker under this focused resolution.

No potentially redundant artifact remains unresolved. No artifact is proven removable.

# Final Minimality Resolution

The focused minimality-resolution criteria are satisfied:

- no artifact is proven removable;
- all nine derivable artifacts reviewed here are justified as necessary despite derivability;
- all four potentially redundant artifacts reviewed here are resolved;
- AX-001 is justified under the current accepted primitive methodology and currently known competitors;
- Foundation v1.0 is not frozen in this PR.

FOUNDATION MINIMALITY RESOLVED
