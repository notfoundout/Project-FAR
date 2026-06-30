# Proofs

## Purpose

This document records formal proofs, proof attempts, failed proofs, and proof sketches developed within Project FAR.

Unlike theorems, proofs describe the logical derivation supporting a claim.

Failed proofs are preserved because they identify gaps in the current theory and frequently motivate improvements.

---

# Proof Standards

Every proof should identify:

- the statement being proven,
- all assumptions,
- all referenced definitions,
- every inference,
- the conclusion.

Proofs relying upon undefined concepts or implicit assumptions should be regarded as incomplete.

## Canonical Prerequisites

Canonical proofs must reference the current canonical definitions in `../definitions/definitions.md`, current canonical axioms in `../axioms/axioms.md`, and the theorem, proposition, or proof obligation being proved. Legacy proof attempts that do not satisfy this requirement are non-authoritative until revised.

---


# Categories

Proofs are classified into four categories.

## Formal Proof

A complete proof satisfying the project's standards.

---

## Proof Sketch

An outline believed to admit completion but currently incomplete.

---

## Failed Proof

An attempted proof containing an identified defect.

Failed proofs remain valuable because they expose weaknesses in the framework.

---

## Open Proof Obligation

A statement believed to require proof but for which no satisfactory derivation currently exists.

---

# Current Proof Obligations

The following represent the highest-priority proof obligations within Project FAR.

---

## PO-1

Representation Theorem

Show that every structured, explicit, auditable reasoning process within scope admits representation within FARA.

Status:

Open.

---

## PO-2

Primitive Independence

Prove that each candidate primitive is independent of the remaining primitives.

Status:

Open.

---

## PO-3

Ω Irreducibility

Show that every reasoning framework satisfying the scope contains an object equivalent in expressive power to Ω.

Status:

Open.

---

## PO-4

Reasoning State Sufficiency

Show that every investigation can proceed entirely through explicitly represented reasoning states.

Status:

Open.

---

## PO-5

Transition Completeness

Show that every valid reasoning transition admits an explicit transition signature.

Status:

Open.

---

## PO-6

Semantic Preservation

Define semantic preservation formally and prove that admissible reasoning transitions preserve meaning.

Status:

Open.

---

## PO-7

Minimality

Show that no architecture with fewer primitive assumptions possesses equivalent expressive power over the stated scope.

Status:

Open.

---

# Research Policy

No proof obligation should be considered complete until independently reviewable.

Likewise, failure to prove a statement should not be interpreted as evidence that the statement is false.

It demonstrates only that the current argument is insufficient.

---

# Philosophy

Project FAR distinguishes sharply between:

- definitions,
- assumptions,
- conjectures,
- proofs,
- and established theorems.

This distinction is intended to keep the research program transparent.

A failed proof is regarded as progress if it reveals an incorrect assumption, an ambiguous definition, or a missing concept.
