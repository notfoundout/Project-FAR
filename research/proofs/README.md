# Formal Proofs

## Purpose

This directory contains the formal proof system of Project FAR.

Its objective is to establish mathematically justified results concerning the Foundational Architecture of Reasoning Analysis (FARA) and related components of Project FAR.

Unlike the validation investigations, which collect empirical and structural evidence, this directory contains formal mathematical arguments.

---

# Relationship to Validation

Validation investigations provide evidence.

Formal proofs establish conclusions.

A successful validation investigation does not constitute a proof.

Likewise, a failed validation investigation does not necessarily refute a theorem.

Validation and proof are complementary activities.

---

# Scope

This directory contains:

- formal definitions used within proofs;
- lemmas;
- propositions;
- theorems;
- corollaries;
- proof attempts;
- counterexamples;
- unresolved conjectures.

---

# Organization

```
proofs/
├── README.md
├── methodology.md
├── theorem-catalog.md
├── conjectures.md
├── proof-obligations.md
├── lemmas/
├── propositions/
├── theorems/
├── corollaries/
├── counterexamples/
└── proof-attempts/
```

---

# Proof Hierarchy

The proof hierarchy follows:

Definition

↓

Lemma

↓

Proposition

↓

Theorem

↓

Corollary

Each level may depend only upon previously established results.

Circular reasoning is prohibited.

---

# Acceptable Evidence

A proof may rely upon:

- accepted canonical definitions;
- previously established lemmas;
- previously established propositions;
- previously established theorems;
- explicitly stated assumptions.

A proof may not rely upon:

- intuition;
- authority;
- consensus;
- undocumented assumptions;
- examples alone.

---

# Proof Status

Every proof artifact shall possess one of the following statuses.

- Draft
- Under Review
- Accepted
- Refuted
- Superseded

---

# Guiding Principle

The objective of this directory is not to accumulate proofs.

The objective is to identify which conclusions follow necessarily from the accepted foundations of Project FAR.