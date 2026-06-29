# Contributing to Project FAR

## Purpose

Thank you for your interest in contributing to Project FAR.

Project FAR is a research project developing a rigorous, minimal, and universal framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

Contributions should strengthen the framework while preserving its internal consistency, minimality, and formal rigor.

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
- Preserve consistency throughout the repository.

---

# Repository Structure

The repository is organized into the following components.

| Directory | Purpose |
|-----------|---------|
| `docs/` | Project documentation |
| `theory/` | Formal theory |
| `fara/` | Foundational Architecture of Reasoning Analysis |
| `far/` | Foundational Analysis of Reasoning |
| `faro/` | Foundational Analysis of Reasoning Operations |
| `examples/` | Worked examples |
| `validation/` | Validation studies |
| `research/` | Ongoing research |
| `papers/` | Publications |

---

# Before Contributing

Before making changes, contributors should:

- Read the root `README.md`.
- Read `ROADMAP.md`.
- Read `theory/definitions.md`.
- Review the relevant directory README.
- Review `research/decision-log.md` if proposing architectural changes.

---

# Definitions

Formal terminology is defined only in:

```text
theory/definitions.md
```

Do not redefine terms elsewhere in the repository.

Instead, reference the canonical definition.

---

# Architectural Changes

Architectural changes should satisfy the following criteria.

- Solve a demonstrated problem.
- Preserve or increase expressive power.
- Avoid unnecessary complexity.
- Avoid introducing circular dependencies.
- Be consistent with existing definitions.

Whenever possible, prefer reducing existing concepts before introducing new ones.

---

# Theory

Changes to the formal theory should maintain logical consistency.

New:

- Definitions
- Axioms
- Conjectures
- Propositions
- Lemmas
- Theorems
- Proofs

should identify their dependencies where appropriate.

---

# Validation

Validation studies should describe existing reasoning frameworks.

They should not modify Project FAR.

Potential improvements identified during validation should instead be documented within the research directory.

---

# Examples

Examples should demonstrate the framework.

They should not introduce new concepts or modify the formal theory.

---

# Documentation

Documentation should remain:

- accurate,
- concise,
- internally consistent,
- and synchronized with the formal theory.

---

# Pull Requests

Pull requests should include:

- A summary of the proposed changes.
- The motivation for the changes.
- The affected files.
- Any new dependencies introduced.
- Any unresolved questions.

---

# Reporting Issues

When reporting an issue, include:

- A clear description.
- The affected files.
- The observed problem.
- The expected behavior.
- Any suggested resolution.

---

# Code of Conduct

Contributors are expected to engage respectfully and constructively.

Discussion should focus on improving the framework through evidence, logical analysis, and clear reasoning.

Disagreements should be resolved through explicit argumentation rather than authority or preference.
