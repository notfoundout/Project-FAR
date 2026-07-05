# Project FAR

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This repository is organized as the Version 1.0 canonical architecture for the project. Each document has one canonical location; superseded material is retained in `archive/` when it is meaningful and not an exact duplicate.

## Current Development Status

FARE Mathematics v0.1 is frozen as the current stable mathematical foundation.

FAR v1.0 Stable has been recorded as the canonical methodology layer of Project FAR.

FARO v1.0 Stable has been recorded as the canonical operational layer of Project FAR.

FARM v1.0 Stable has been recorded as the canonical meta-framework coordination layer of Project FAR.

Active development now shifts to worked examples and downstream validation.

Future FARE mathematical work is requirement-driven:

- no new MDEFs unless FAR, FARO, FARA, or FARM requires them;
- new theorems only when they justify or extend FAR, FARO, FARA, or FARM;
- existing mathematical definitions change only through formal review.

See:

- `docs/project-status.md`
- `docs/milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md`
- `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`
- `docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md`
- `docs/milestones/FARM-v1.0-Stable.md`

## Navigation

- `docs/` — project-level architecture, roadmap, status, changelog, decision log, style guide, and canonical map.
- `foundations/` — motivation, assumptions, primitive foundations, representations, and foundational investigations.
- `theory/` — canonical definitions, axioms, semantics, operators, notation, theorems, proofs, and consistency material.
- `frameworks/` — framework-specific material for FAR, FARA, FARO, and FARM.
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
6. `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`
7. `docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md`
8. `docs/milestones/FARM-v1.0-Stable.md`
9. `foundations/README.md`
10. `theory/README.md`
11. `frameworks/FARA/README.md`
12. `frameworks/FAR/README.md`
13. `frameworks/FARO/README.md`
14. `frameworks/FARM/README.md`
15. `methodology/README.md`
16. `research/README.md`

## Core Principle

Canonical theory and accepted framework definitions live in `foundations/`, `theory/`, and `frameworks`. Exploratory or provisional work lives in `research`. Superseded but meaningful material lives in `archive/`.
