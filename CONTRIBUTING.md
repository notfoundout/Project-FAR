# Contributing to Project FAR

## Purpose

Thank you for your interest in contributing to Project FAR.

Project FAR is a research project developing a rigorous, minimal, and universal framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

Contributions should strengthen the framework while preserving its logical consistency, minimality, and formal rigor.

---

# Before You Contribute

Before proposing changes, contributors should become familiar with the project.

Recommended reading order:

1. `README.md`
2. `docs/ROADMAP.md`
3. `theory/definitions/definitions.md`
4. The README for the relevant directory
5. `docs/DECISION_LOG.md` (for architectural changes)

---

# Guiding Principles

All contributions should follow these principles.

- Definitions precede conclusions.
- Simplicity is preferred over complexity.
- Reduction is preferred over expansion.
- Every concept has one canonical definition.
- New concepts require explicit justification.
- Formal claims should ultimately be supported by proof.
- Avoid circular dependencies.
- Preserve internal consistency.

---

# Repository Organization

| Directory | Purpose |
|-----------|---------|
| `docs/` | Project documentation |
| `theory/` | Formal theory |
| `frameworks/FARA/` | Architectural framework |
| `frameworks/FAR/` | Investigation methodology |
| `frameworks/FARO/` | Reasoning operations |
| `examples/` | Worked examples |
| `methodology/validation/` | Validation studies |
| `research/` | Active research |
| `papers/` | Publications |

---

# Canonical Definitions

All formal terminology is defined exclusively in:

```text
theory/definitions/definitions.md
```

Do not redefine technical terms elsewhere.

If a new concept is required, add it to the canonical definitions before using it throughout the repository.

---

# Architectural Contributions

Architectural changes should satisfy all of the following:

- Address a demonstrated limitation.
- Preserve or increase expressive power.
- Minimize additional complexity.
- Avoid introducing circular dependencies.
- Remain consistent with existing definitions.

Whenever possible, derive existing concepts before introducing new primitive concepts.

---

# Formal Theory

Changes to the formal theory should identify dependencies where appropriate.

Examples include:

- Definitions
- Axioms
- Propositions
- Lemmas
- Theorems
- Proofs

The goal
