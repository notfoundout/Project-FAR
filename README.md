# Project FAR

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This repository is organized as the Version 1.0 canonical architecture for the project. Each document has one canonical location; superseded material is retained in `archive/` when it is meaningful and not an exact duplicate.

## Current Development Status

FARE Mathematics v0.1 is frozen as the current stable mathematical foundation.

Active development has shifted back to the FAR core framework.

Future FARE mathematical work is requirement-driven:

- no new MDEFs unless FAR requires them;
- new theorems only when they justify or extend FAR;
- existing mathematical definitions change only through formal review.

See:

- `docs/project-status.md`
- `docs/milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md`

## Navigation

- `docs/` — project-level architecture, roadmap, status, changelog, decision log, style guide, and canonical map.
- `foundations/` — motivation, assumptions, primitive foundations, representations, and foundational investigations.
- `theory/` — canonical definitions, axioms, semantics, operators, notation, theorems, proofs, and consistency material.
- `frameworks/` — framework-specific material for FAR, FARA, and FARO.
- `methodology/` — proof standards, validation, falsification, and comparison methodology.
- `examples/` — worked examples of Project FAR usage.
- `research/` — exploratory literature, notes, comparisons, bibliography, and open problems.
- `tests/` — counterexamples, simulations, edge cases, and regression material.
- `papers/` — paper drafts and publication-oriented writing.
- `archive/` — meaningful superseded material retained for historical context.

## Recommended Reading Order

1. `docs/OVERVIEW.md`
2. `docs/ARCHITECTURE.md`
3. `docs/CANONICAL_MAP.md`
4. `docs/project-status.md`
5. `docs/milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md`
6. `foundations/README.md`
7. `theory/README.md`
8. `frameworks/FARA/README.md`
9. `frameworks/FAR/README.md`
10. `frameworks/FARO/README.md`
11. `methodology/README.md`
12. `research/README.md`

## Core Principle

Canonical theory and accepted framework definitions live in `foundations/`, `theory/`, and `frameworks/`. Exploratory or provisional work lives in `research/`. Superseded but meaningful material lives in `archive/`.
