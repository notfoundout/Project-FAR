# Theorem Catalog

## Purpose

This document serves as the canonical index of formal results within Project FAR.

Its purpose is to maintain a complete inventory of every accepted, proposed, superseded, or refuted formal result.

This document is a navigation artifact.

It does not contain proofs.

---

# Organization

Formal results are organized according to the following hierarchy:

- Lemma;
- Proposition;
- Theorem;
- Corollary.

Each result receives a unique identifier.

Identifiers shall never be reused.

---

# Status Classifications

Every formal result shall possess exactly one status:

- Draft;
- Under Review;
- Accepted;
- Refuted;
- Superseded.

---

# Lemmas

| ID | Title | Status | Dependencies | File |
|----|-------|--------|--------------|------|
| L-001 | Representation/Object Distinction | Draft | Object; Representation; Interpretation | `lemmas/L-001-representation-object-distinction.md` |
| L-002 | Interpretation/Representation Distinction | Draft | Representation; Interpretation; L-001 | `lemmas/L-002-interpretation-representation-distinction.md` |
| L-003 | Object/Property Distinction | Draft | Object; Property; L-001; L-002 | `lemmas/L-003-object-property-distinction.md` |
| L-004 | Relation Non-Identity | Draft | Object; Property; Relation; L-001; L-003 | `lemmas/L-004-relation-non-identity.md` |
| L-005 | Investigation/Reasoning Calculus Distinction | Draft | Investigation; Reasoning Calculus; L-001; L-002; L-003; L-004 | `lemmas/L-005-investigation-reasoning-calculus-distinction.md` |
| L-006 | Representations Require Explicit Structure | Draft | Representation; Representational Structure; L-001; L-002 | `lemmas/L-006-representations-require-explicit-structure.md` |
| L-007 | Interpretation Preserves Representational Identity | Draft | Representation; Interpretation; L-001; L-002; L-006 | `lemmas/L-007-interpretation-preserves-representational-identity.md` |

---

# Propositions

| ID | Title | Status | Dependencies | File |
|----|-------|--------|--------------|------|
| P-001 | Representational Integrity | Draft | Representation; Representational Structure; Interpretation; L-001; L-002; L-006; L-007 | `propositions/P-001-representational-integrity.md` |

---

# Theorems

| ID | Title | Status | Dependencies | File |
|----|-------|--------|--------------|------|
| T-001 | Representational Integrity Theorem | Draft | Representation; Representational Structure; Interpretation; L-001; L-002; L-006; L-007; P-001 | `theorems/T-001-representational-integrity-theorem.md` |

---

# Corollaries

| ID | Title | Status | Dependencies | File |
|----|-------|--------|--------------|------|
| None | — | — | — | — |

---

# Numbering Convention

The following prefixes shall be used:

- L-XXX — Lemma;
- P-XXX — Proposition;
- T-XXX — Theorem;
- C-XXX — Corollary.

Identifiers are assigned sequentially.

Numbers are never recycled.

---

# Dependency Policy

Every formal result shall list every dependency required for its proof.

Dependencies may include:

- canonical definitions;
- accepted lemmas;
- accepted propositions;
- accepted theorems;
- accepted corollaries;
- explicitly stated assumptions.

No dependency may be implicit.

---

# Current Status

The initial proof library has been normalized.

Current artifacts:

- seven draft lemmas;
- one draft proposition;
- one draft theorem.

No formal result has yet been accepted.
