# Reasoning States

## Purpose

This document defines reasoning states within the Foundational Architecture of Reasoning Analysis (FARA).

A reasoning state is the fundamental representational object through which reasoning is recorded and analyzed.

It does not define how reasoning states are transformed or evaluated.

---

## Definition

A **reasoning state** is the complete explicit representation of an investigation at a particular stage of reasoning.

The canonical definition of a reasoning state is maintained in:

`theory/definitions.md`

---

## Objective

The purpose of a reasoning state is to provide a complete, explicit snapshot of an investigation at a particular stage of analysis.

Every subsequent stage of reasoning is represented by a new reasoning state.

---

## Properties

A reasoning state should satisfy the following properties.

### Explicitness

Every representation participating in the investigation is explicitly represented.

---

### Completeness

The reasoning state contains the information required to continue or audit the investigation.

---

### Traceability

Every representation possesses an identifiable origin within the investigation.

---

### Reconstructibility

Another investigator using the same reasoning calculus should be capable of reconstructing the reasoning process from the recorded reasoning states and transition signatures.

---

## Relationships

A reasoning state exists relative to:

- an investigation,
- a representational structure,
- an interpretation,
- and a reasoning calculus.

These concepts are defined in:

`theory/definitions.md`

---

## Evolution

Reasoning states evolve through explicit transformations represented by transition signatures.

The representation of those transformations is defined in:

`transition-signatures.md`

---

## Admissibility

Reasoning states do not determine admissibility.

The candidates represented within a reasoning state are classified by the Admissibility Structure (Ω).

See:

`admissibility-structure.md`

---

## Research Status

Current research investigates:

- minimal reasoning state representations,
- reasoning state equivalence,
- reasoning state composition,
- reasoning state decomposition,
- and formal properties of reasoning state transformations.
