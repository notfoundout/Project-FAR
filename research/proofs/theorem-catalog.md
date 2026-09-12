# Research Proof Catalog

Status: Research; non-canonical

## Purpose

This document preserves proposed proof topics and research identifiers within `research/proofs/`. It is a research-planning and navigation record, not the Project FAR canonical theorem/proof index.

Current accepted theorem/proof status is governed by the [Theorem and Proof-Status Register](../../docs/governance/theorem-proof-status-register.md), with canonical locations resolved through the [Canonical Map](../../docs/CANONICAL_MAP.md).

The entries below do not assert that a corresponding proof artifact exists, do not establish the listed statement, and do not create accepted identifiers or statuses outside this research record.

---

## Research status vocabulary

This catalog uses the following local research states:

- Proposed — a proof topic has been recorded, but no proof artifact is represented here;
- Draft — an actual research proof artifact exists and is incomplete or unaccepted;
- Under Review — an actual research proof artifact is undergoing review;
- Refuted — research evidence records a refutation, subject to the applicable canonical status authority;
- Superseded — this research record has been replaced while retained for provenance.

No local research state is equivalent to accepted canonical theorem/proof status.

---

## Proposed lemmas

| Research ID | Topic | Research state | Dependencies recorded for investigation | Proof artifact |
|---|---|---|---|---|
| L-001 | Representation/Object Distinction | Proposed | Object; Representation; Interpretation | None recorded |
| L-002 | Interpretation/Representation Distinction | Proposed | Representation; Interpretation; L-001 | None recorded |
| L-003 | Object/Property Distinction | Proposed | Object; Property; L-001; L-002 | None recorded |
| L-004 | Relation Non-Identity | Proposed | Object; Property; Relation; L-001; L-003 | None recorded |
| L-005 | Investigation/Reasoning Calculus Distinction | Proposed | Investigation; Reasoning Calculus; L-001; L-002; L-003; L-004 | None recorded |
| L-006 | Representations Require Explicit Structure | Proposed | Representation; Representational Structure; L-001; L-002 | None recorded |
| L-007 | Interpretation Preserves Representational Identity | Proposed | Representation; Interpretation; L-001; L-002; L-006 | None recorded |

---

## Proposed propositions

| Research ID | Topic | Research state | Dependencies recorded for investigation | Proof artifact |
|---|---|---|---|---|
| P-001 | Representational Integrity | Proposed | Representation; Representational Structure; Interpretation; L-001; L-002; L-006; L-007 | None recorded |

---

## Proposed theorems

| Research ID | Topic | Research state | Dependencies recorded for investigation | Proof artifact |
|---|---|---|---|---|
| T-001 | Representational Integrity Theorem | Proposed | Representation; Representational Structure; Interpretation; L-001; L-002; L-006; L-007; P-001 | None recorded |

---

## Proposed corollaries

No research corollary topic is currently recorded in this catalog.

---

## Identifier boundary

The L-/P-/T- identifiers above are retained as local research identifiers for provenance. Their presence here does not reserve or establish a canonical theorem/proof identifier. Any promoted result must use the identity and status assigned by the applicable governed acceptance process.

Dependencies listed above are research-planning records. They are not assertions that the dependencies are proved, accepted, sufficient, or currently available as proof objects.

---

## Current repository state

At this catalog revision, `research/proofs/` contains research/navigation Markdown files but no lemma, proposition, theorem, or corollary proof artifact corresponding to the proposed entries above. The catalog therefore does not link to nonexistent proof files or describe the proposed entries as an existing normalized proof library.

No result is accepted or promoted by this document. If a proof artifact is later created, this catalog should record the artifact that actually exists and preserve its research status until the governed acceptance path changes that status.
