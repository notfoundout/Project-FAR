# Decision Log

## Purpose

This document records significant architectural and theoretical decisions made during the development of Project FAR.

Each entry records the decision, its rationale, and its impact on the framework.

The purpose of this log is to preserve design history, prevent repeated discussions of previously resolved issues, and document the evolution of the project.

---

# Decision 1

## Decision

Adopt `theory/definitions/definitions.md` as the canonical source for shared formal terminology.

---

## Rationale

Maintaining a single canonical source eliminates redundant definitions and ensures consistency throughout the repository.

---

## Impact

All architectural, methodological, operational, and documentation files now reference the canonical definitions instead of redefining terms.

---

# Decision 2

## Decision

Separate Project FAR into four primary components:

- FARA
- FAR
- FARO
- Theory

---

## Rationale

Each component has a distinct responsibility.

Separating them reduces redundancy and establishes a clear dependency structure.

---

## Impact

The repository now distinguishes architecture, methodology, operations, and formal theory.

---

# Decision 3

## Decision

Replace **Candidate Resolution** with **Candidate**.

---

## Rationale

The previous terminology introduced an unnecessary circular dependency.

A candidate exists before admissibility is evaluated or a resolution is selected.

---

## Impact

The dependency graph became acyclic and conceptually simpler.

---

# Decision 4

## Decision

Remove **Possibility Space** as a primitive architectural concept.

---

## Rationale

The concept was reducible to the collection of candidates admitted for consideration within an investigation.

Maintaining it as an independent concept added unnecessary complexity.

---

## Impact

The architecture was simplified without reducing expressive power.

---

# Decision 5

## Decision

Rename **Ω** to **Admissibility Structure (Ω)** on first reference.

---

## Rationale

The descriptive name communicates the purpose of Ω while preserving the symbolic notation.

---

## Impact

Repository terminology became clearer and more self-explanatory.

---

# Decision 6

## Decision

Introduce **Resolution Rules** as a concept distinct from the reasoning calculus.

---

## Rationale

Determining candidate admissibility and selecting a final resolution are logically distinct operations.

Separating them simplifies the architecture and clarifies the reasoning process.

---

## Impact

The workflow now distinguishes:

- Candidate classification
- Resolution selection

---

# Decision 7

## Decision

Replace **Fundamental Objects** with **Primitive Concepts**.

---

## Rationale

"Primitive" has a precise meaning within formal systems.

"Fundamental" is broader and may refer only to importance.

---

## Impact

Repository terminology now aligns with formal mathematical practice.

---

# Decision 8

## Decision

Organize the repository according to a directed dependency structure.

---

## Rationale

Every component should depend only upon lower-level components.

This minimizes circular dependencies and simplifies maintenance.

---

## Impact

The repository now follows the dependency order:

- Theory
- FARA
- FAR
- FARO
- Documentation
