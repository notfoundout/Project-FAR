# Proof Methodology

## Purpose

This document defines the methodology governing formal proofs within Project FAR.

Its purpose is to establish uniform standards for constructing, evaluating, and maintaining formal proofs.

Unless explicitly stated otherwise, canonical terminology is defined in:

`theory/definitions/definitions.md`

---

# Objective

The objective of a formal proof is to demonstrate that a conclusion follows necessarily from explicitly stated premises according to valid rules of inference.

Proofs establish necessity rather than plausibility.

---

# Scope

This methodology applies to:

- lemmas;
- propositions;
- theorems;
- corollaries;
- proof attempts;
- proof revisions.

It does not govern exploratory research or validation investigations.

---

# Required Structure

Every formal proof shall contain the following sections.

## Statement

The precise claim being proven.

---

## Status

One of:

- Draft
- Under Review
- Accepted
- Refuted
- Superseded

---

## Dependencies

Every definition, lemma, proposition, theorem, or assumption used by the proof.

No dependency may be implicit.

---

## Assumptions

Every assumption not already established by accepted results.

Assumptions should be minimized.

---

## Proof

A complete logical argument.

Every inference should follow from:

- accepted definitions;
- accepted results;
- explicitly stated assumptions;
- valid rules of inference.

---

## Conclusion

The final proven result.

The conclusion shall not exceed the scope established by the assumptions.

---

## Limitations

Every proof should explicitly state what it does not establish.

---

# Proof Standards

Every proof should satisfy the following requirements.

## Explicitness

No inference should depend upon unstated assumptions.

---

## Traceability

Every inference should identify its justification.

---

## Dependency Discipline

Proofs shall depend only upon previously accepted artifacts.

Circular reasoning is prohibited.

---

## Minimal Assumptions

Proofs should minimize the number of assumptions required.

---

## Generality

A proof should establish the strongest justified conclusion.

Claims extending beyond the proven result are prohibited.

---

## Reproducibility

An independent reviewer should be capable of reconstructing the proof using only the documented dependencies.

---

# Permitted Dependencies

A proof may depend upon:

- canonical definitions;
- accepted lemmas;
- accepted propositions;
- accepted theorems;
- accepted corollaries;
- explicitly stated assumptions.

A proof may not depend upon:

- intuition;
- authority;
- consensus;
- undocumented assumptions;
- examples alone.

---

# Proof Classification

Formal proof artifacts are organized as follows.

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

---

# Invalid Proof Practices

The following are prohibited.

- circular reasoning;
- equivocation;
- undefined terminology;
- hidden assumptions;
- dependency cycles;
- unsupported generalization;
- contradiction without explicit resolution.

---

# Relationship to Validation

Validation investigations provide evidence regarding architectural claims.

Formal proofs establish logical necessity.

Evidence alone does not constitute proof.

Likewise, a failed validation investigation does not automatically refute a theorem.

Validation and proof complement one another but remain distinct.

---

# Revision Policy

Proofs may be revised only when:

- an error is identified;
- a stronger proof is discovered;
- dependencies change;
- assumptions are reduced;
- a counterexample is discovered.

Superseded proofs should be retained for historical traceability.

---

# Guiding Principle

Every accepted theorem should be reproducible from explicitly documented assumptions through valid logical inference.

The strength of a theorem is determined not by the significance of its conclusion but by the rigor of its proof.

