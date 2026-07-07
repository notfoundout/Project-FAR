# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.3.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/verify-theory.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/verify-theory.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This repository is organized as the Version 1.0 canonical architecture for the project. Each document has one canonical location; superseded material is retained in [`archive/`](archive/) when it is meaningful and not an exact duplicate.

---

## Latest Release

**Project FAR v0.3.0** is the current internal-validation milestone. It evaluates primitive sufficiency across the reasoning-system corpus and adversarial suite, adds cross-domain consistency analysis, and records provisional independence and minimality analysis for the five FAR primitives.

Canonical release document: [`docs/releases/project-far-v0.3.0.md`](docs/releases/project-far-v0.3.0.md)

Synthesis report: [`docs/reports/project-far-v0.3.0-synthesis.md`](docs/reports/project-far-v0.3.0-synthesis.md)

---

## Current Development Status

The current framework stack is:

| Framework | Role | Status | Entry Point |
|---|---|---|---|
| FARA | Representation | Stable | [`frameworks/FARA/README.md`](frameworks/FARA/README.md) |
| FAR | Methodology | Stable | [`frameworks/FAR/README.md`](frameworks/FAR/README.md) |
| FARO | Operations | Stable | [`frameworks/FARO/README.md`](frameworks/FARO/README.md) |
| FARE | Mathematics | Frozen, requirement-driven | [`frameworks/FARE/README.md`](frameworks/FARE/README.md) |
| FARM | Meta-framework coordination | Stable | [`frameworks/FARM/README.md`](frameworks/FARM/README.md) |

Current development is preparing for external validation after the v0.3.0 internal-validation baseline.

Future FARE mathematical work is requirement-driven:

- no new MDEFs unless FAR, FARO, FARA, or FARM requires them;
- new theorems only when they justify or extend FAR, FARO, FARA, or FARM;
- existing mathematical definitions change only through formal review.

---

## Releases

- [`v0.3.0 — Internal Validation Release`](https://github.com/notfoundout/Project-FAR/releases/tag/v0.3.0)
- [`v0.2.0 — Evidence Framework Release`](https://github.com/notfoundout/Project-FAR/releases/tag/v0.2.0)
- [`v0.1.0 — Initial Public Release`](https://github.com/notfoundout/Project-FAR/releases/tag/v0.1.0)

---

## Primary Navigation

- [`docs/maintenance/repository-health-checks.md`](docs/maintenance/repository-health-checks.md) — Repository health-check commands and failure remediation.
- [`docs/project-status.md`](docs/project-status.md) — Current project status and governance.
- [`docs/CANONICAL_MAP.md`](docs/CANONICAL_MAP.md) — Linked canonical-location index.
- [`docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md`](docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md) — Post-v1.0 repository audit.
- [`docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md`](docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md) — Framework navigation audit.

---

## Milestones

- [`docs/milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md`](docs/milestones/FAR-MILESTONE-001-FARE-v0.1-Frozen.md)
- [`docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`](docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md)
- [`docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md`](docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md)
- [`docs/milestones/FARM-v1.0-Stable.md`](docs/milestones/FARM-v1.0-Stable.md)

---

## Repository Navigation

- [`docs/`](docs/) — Project-level architecture, roadmap, status, changelog, decision log, style guide, canonical map, audits, and milestones.
- [`foundations/`](foundations/) — Motivation, assumptions, primitive foundations, representations, and foundational investigations.
- [`theory/`](theory/) — Canonical definitions, axioms, semantics, operators, notation, theorems, proofs, and consistency material.
- [`frameworks/`](frameworks/) — Framework-specific material for FARA, FAR, FARE, FARO, and FARM.
- [`methodology/`](methodology/) — Proof standards, validation, falsification, and comparison methodology.
- [`examples/`](examples/) — Worked examples of Project FAR usage.
- [`research/`](research/) — Exploratory literature, notes, comparisons, bibliography, and open problems.
- [`tests/`](tests/) — Counterexamples, simulations, edge cases, and regression material.
- [`papers/`](papers/) — Paper drafts and publication-oriented writing.
- [`archive/`](archive/) — Meaningful superseded material retained for historical context.

---

## Recommended Reading Order

1. [`docs/OVERVIEW.md`](docs/OVERVIEW.md)
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
3. [`docs/CANONICAL_MAP.md`](docs/CANONICAL_MAP.md)
4. [`docs/project-status.md`](docs/project-status.md)
5. [`frameworks/FARA/README.md`](frameworks/FARA/README.md)
6. [`frameworks/FAR/README.md`](frameworks/FAR/README.md)
7. [`frameworks/FARO/README.md`](frameworks/FARO/README.md)
8. [`frameworks/FARE/README.md`](frameworks/FARE/README.md)
9. [`frameworks/FARM/README.md`](frameworks/FARM/README.md)
10. [`examples/`](examples/)

---

## Core Principle

Canonical theory and accepted framework definitions live in [`foundations/`](foundations/), [`theory/`](theory/), and [`frameworks/`](frameworks/). Exploratory or provisional work lives in [`research/`](research/). Superseded but meaningful material lives in [`archive/`](archive/).


## Self-Advancement Planning

- [Planning overview](docs/planning/README.md)
- [Generated project status](docs/reports/project-status-generated.md)
- [Research gap report](docs/reports/research-gap-report.md)
- [Next actions](docs/planning/next-actions.md)
- [Planner maintenance](docs/maintenance/self-advancement-planner.md)
