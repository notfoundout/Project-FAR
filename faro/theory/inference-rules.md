# FARO Inference Rules

## Purpose

This document defines the admissible inference rules governing operational reasoning within FARO.

These rules specialize the general proof system established by the Project FAR meta-theory.

Every operational proof shall consist of a finite sequence of justified inference steps.

Each step shall be licensed by one or more inference rules defined herein.

---

# Scope

These rules govern proofs concerning:

- operational expressions;
- operational composition;
- operational equivalence;
- operational semantics;
- operational rewriting; and
- operational theorems.

General logical inference remains governed by the Project FAR proof system.

---

# Design Principles

The inference rules shall satisfy the following principles.

- Soundness.
- Explicitness.
- Local applicability.
- Reproducibility.
- Finite verification.
- Minimality.

No inference rule should duplicate another.

---

# Primitive Rule Classes

The primitive inference rules remain under investigation.

Current candidate classes include:

## Structural Rules

Rules governing the formation and manipulation of operational expressions.

---

## Composition Rules

Rules governing operational composition.

---

## Equivalence Rules

Rules preserving operational equivalence.

---

## Rewrite Rules

Rules permitting replacement by operationally equivalent expressions.

---

## Semantic Rules

Rules connecting operational syntax with operational meaning.

---

## Normalization Rules

Rules governing the reduction of operational expressions to normal form.

---

# Candidate Primitive Rules

No primitive inference rules have yet been accepted.

Candidate rules remain within the FARO research program until formally justified.

---

# Relationship to Proofs

Every operational proof shall explicitly identify the inference rule justifying each proof step.

A proof containing an unjustified step is not a valid FARO proof.

---

# Relationship to the Meta-Theory

The admissibility of these inference rules is determined by the Project FAR meta-theory.

Accordingly, FARO extends the general proof system rather than replacing it.

---

# Current Status

The operational inference system remains under active investigation.

This document presently specifies the intended structure of the canonical inference system rather than the inference rules themselves.
