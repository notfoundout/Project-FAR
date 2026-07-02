# Reasoning States

## Purpose

This document specifies the role of reasoning states within the Foundational Architecture of Reasoning Analysis (FARA).

Reasoning states describe the condition of an investigation throughout a reasoning process.

The canonical definitions of all terminology used here are maintained in:

`theory/definitions/definitions.md`

This document specifies the architectural role of reasoning states rather than redefining the underlying concepts.

---

## Overview

Every reasoning process occurs within an investigation.

At any stage of that reasoning process, the investigation possesses a particular reasoning state.

A reasoning state is distinct from:

- a reasoning state representation;
- a reasoning state record;
- a transition signature;
- a reasoning trace.

This distinction preserves the separation between an object and representations of that object.

---

## Definition

A **reasoning state** is the state of an investigation at a particular stage of a reasoning process.

A reasoning state is not itself a representation.

A reasoning state may be represented by one or more reasoning state representations.

---

## Reasoning State Representations

A **reasoning state representation** is a representation describing a reasoning state.

Different reasoning state representations may describe the same reasoning state.

Differences among representations do not necessarily imply differences in the underlying reasoning state.

---

## Reasoning State Records

A **reasoning state record** is a persistent representation of one or more reasoning state representations.

Reasoning state records exist for purposes including:

- documentation;
- auditing;
- reproducibility;
- verification;
- historical reconstruction.

Reasoning state records are repository artifacts.

They are not reasoning states.

---

## Relationships

A reasoning state exists relative to:

- an investigation;
- a reasoning process;
- a reasoning calculus;
- an interpretation;
- one or more reasoning state representations.

Reasoning states do not exist independently of investigations.

They remain distinct from every representation used to describe them.

---

## Progression

Reasoning processes progress through sequences of reasoning states.

Progression occurs through transformation executions governed by the applicable reasoning calculus.

Transition signatures record those transformation executions.

Reasoning states themselves do not perform transitions.

---

## Relationship to Transition Signatures

Transition signatures document transformation executions between reasoning state representations.

A transition signature represents a transition.

It is not itself the transition.

Multiple transition signatures may describe equivalent transformation executions.

---

## Relationship to Reasoning Traces

A reasoning trace is an ordered collection of transition signatures representing the progression of a reasoning process.

Reasoning traces document reasoning.

They do not constitute reasoning processes.

---

## Relationship to Admissibility

Reasoning states do not determine admissibility.

Admissibility is determined by the applicable reasoning calculus.

The Admissibility Structure (Ω) records admissibility classifications of candidates within an investigation.

See:

`admissibility-structure.md`

---

## Architectural Role

Within FARA, reasoning states provide reference points for describing the condition of an investigation throughout reasoning.

They provide the state-level context within which transformation executions, transition signatures, admissibility classifications, and resolutions can be represented and audited.

---

## Design Principles

Reasoning states should satisfy the following principles:

- **Explicit representability** — Every reasoning state should admit explicit representation.
- **Representational independence** — Multiple representations may describe the same reasoning state.
- **Auditability** — Reasoning state records should support independent reconstruction of reasoning.
- **Calculus independence** — The concept of a reasoning state does not depend upon any particular reasoning calculus.
- **Interpretation separation** — A reasoning state is distinct from interpretations assigned to its representations.

---

## Scope

This document specifies the architectural role of reasoning states within FARA.

It does not define:

- representation;
- interpretation;
- reasoning calculus;
- transformation execution;
- transition signature;
- admissibility;
- resolution.

Those concepts are defined by the canonical definitions and related architectural documents.

---

## Research Status

Current research investigates:

- minimal reasoning state representations;
- reasoning state equivalence;
- reasoning state composition;
- reasoning state decomposition;
- representation completeness for reasoning states;
- formal properties of reasoning state transitions.
