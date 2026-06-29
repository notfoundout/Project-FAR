# Theory

## Purpose

This directory contains the formal theoretical foundation of Project FAR.

It defines the canonical terminology, assumptions, formal statements, and mathematical structure upon which the remainder of the framework is built.

All architectural, methodological, and operational components of Project FAR ultimately depend upon the theory contained within this directory.

---

# Objectives

The formal theory aims to:

- Establish a precise vocabulary.
- Minimize ambiguity through canonical definitions.
- State the foundational assumptions of the framework.
- Develop formally derived results.
- Support rigorous proofs.
- Provide a stable foundation for future theoretical development.

---

# Directory Structure

```text
theory/
├── README.md
├── definitions.md
├── notation.md
├── axioms.md
├── conjectures.md
├── propositions.md
├── theorems.md
└── proofs/
    └── README.md
```

---

# Reading Order

Readers are encouraged to proceed in the following order.

1. `definitions.md`
2. `notation.md`
3. `axioms.md`
4. `conjectures.md`
5. `propositions.md`
6. `theorems.md`
7. `proofs/`

Each document builds upon the preceding documents.

---

# Components

## Definitions

Provides the canonical definitions used throughout Project FAR.

Every technical term appearing elsewhere in the repository refers to these definitions unless explicitly stated otherwise.

---

## Notation

Defines the symbols, identifiers, and naming conventions used throughout the formal theory.

---

## Axioms

States the foundational assumptions accepted by the framework.

Axioms are not proved within Project FAR.

---

## Conjectures

Records statements believed to be true but not yet formally established.

Conjectures represent active research rather than accepted results.

---

## Propositions

Records formal results that follow directly from the canonical definitions and axioms.

Propositions establish immediate consequences of the framework and provide the foundation for later theoretical development.

---

## Theorems

Records formally established results derived from the definitions, axioms, propositions, and previously established theorems.

Every theorem should be accompanied by a complete formal proof.

---

## Proofs

Contains the complete formal proofs supporting the theorems of Project FAR.

Each substantial theorem should have its own proof document.

---

# Dependency Structure

The formal theory develops according to the following progression.

```text
Definitions
      ↓
Notation
      ↓
Axioms
      ↓
Conjectures
      ↓
Propositions
      ↓
Theorems
      ↓
Proofs
```

---

# Design Principles

The formal theory is developed according to the following principles.

- Definitions precede conclusions.
- Simplicity is preferred over complexity.
- Reduction is preferred over expansion.
- Every concept has one canonical definition.
- Formal statements should identify their dependencies whenever practical.
- Every theorem should ultimately be supported by a complete formal proof.

---

# Current Status

The foundational structure of the formal theory has been established.

Current research is focused on strengthening propositions, proving conjectures, developing theorems, and constructing formal proofs.# Theory

## Purpose

This directory contains the formal development of Project FAR.

Unlike the documentation and architectural directories, the contents of this directory are organized according to the conventions of formal mathematical and logical theories.

Definitions, assumptions, propositions, lemmas, conjectures, theorems, and proofs are maintained separately to preserve conceptual clarity.

---

## Contents

- `definitions.md` — Formal definitions.
- `axioms.md` — Foundational assumptions.
- `propositions.md` — Intermediate formal results.
- `lemmas.md` — Supporting formal results.
- `theorems.md` — Principal formal results.
- `conjectures.md` — Unproven statements.
- `proofs.md` — Formal proofs and proof obligations.
