# Reasoning States

## Purpose

This document defines the concept of a reasoning state within FARA.

A reasoning state is the fundamental object through which reasoning is represented and analyzed.

It does not define how reasoning states are transformed or evaluated.

---

## Definition

A reasoning state is the complete explicit representation of an investigation at a particular stage of reasoning.

It contains all representations that participate in the investigation at that stage.

The formal definition of a reasoning state is maintained in:

`theory/definitions.md`

---

## Properties

A reasoning state should satisfy the following properties.

### Explicitness

Every representation participating in the reasoning process is explicitly represented.

---

### Completeness

The reasoning state contains the information required to continue or audit the investigation.

---

### Auditability

Every representation has an identifiable origin within the investigation.

---

### Reconstructibility

Another investigator using the same reasoning state and reasoning calculus should be able to reconstruct the reasoning process.

---

## Relationship to Other Components

A reasoning state exists relative to:

- a representational structure,
- an interpretation,
- an investigation,
- and a reasoning calculus.

These concepts are defined elsewhere within the architecture.

---

## Evolution

Reasoning states change through explicit transitions.

The representation of those transitions is defined in:

`transition-signatures.md`

---

## Evaluation

Reasoning states are evaluated according to the reasoning calculus.

The resulting admissibility structure is defined in:

`omega.md`

---

## Research Status

Current research investigates:

- minimal representations of reasoning states,
- equivalence between reasoning states,
- reasoning state algebra,
- and formal properties of reasoning state transitions.
