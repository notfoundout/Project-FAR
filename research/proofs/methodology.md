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

Every formal proof shall contain:

- identifier;
- title;
- status;
- statement;
- purpose;
- dependencies;
- assumptions;
- proof strategy;
- numbered proof steps;
- conclusion;
- consequences;
- limitations;
- related results.

---

# Proof Strategy

Every proof shall explicitly state its proof strategy.

Permitted strategies include:

- direct proof;
- proof by contradiction;
- proof by contrapositive;
- proof by construction;
- case analysis;
- induction, when explicitly justified.

---

# Numbered Proof Steps

Every proof shall be written as numbered steps.

Each step shall contain:

1. the claim established at that step;
2. a justification identifying the dependency, assumption, or inference rule used.

No inference may be implicit.

---

# Dependency Discipline

Every proof shall list every definition, lemma, proposition, theorem, corollary, or assumption used by the proof.

No dependency may be implicit.

Proofs shall not depend on later results.

Circular reasoning is prohibited.

---

# Termination

Every completed proof shall end with:

**Q.E.D.**

A draft may include Q.E.D. only if the argument is intended as a complete proof rather than a partial attempt.

---

# Proof Standards

Every proof should satisfy:

- explicitness;
- traceability;
- dependency discipline;
- minimal assumptions;
- justified generality;
- reproducibility.

---

# Invalid Proof Practices

The following are prohibited:

- circular reasoning;
- equivocation;
- undefined terminology;
- hidden assumptions;
- dependency cycles;
- unsupported generalization;
- contradiction without explicit resolution;
- appeal to examples as proof of universal claims.

---

# Relationship to Validation

Validation investigations provide evidence regarding architectural claims.

Formal proofs establish logical necessity.

Evidence alone does not constitute proof.

Validation and proof complement one another but remain distinct.

---

# Revision Policy

Proofs may be revised only when:

- an error is identified;
- a stronger proof is discovered;
- dependencies change;
- assumptions are reduced;
- a counterexample is discovered;
- proof style is normalized across the proof library.

Superseded proofs should be retained for historical traceability when they contain unique information.

---

# Guiding Principle

Every accepted theorem should be reproducible from explicitly documented assumptions through valid logical inference.
