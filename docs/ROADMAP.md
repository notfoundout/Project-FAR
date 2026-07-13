# Project Roadmap

## Purpose

This document describes the long-term development plan of Project FAR.

It identifies the major phases of the project, their objectives, and their current status.

Unlike the formal theory, this document serves as a project management and planning resource.

## Governing Research Direction

The [Central Research Program](governance/central-research-program.md) governs future major work.

Project FAR exists to determine whether reasoning instantiates a common underlying structure and, if so, whether that structure is universal and minimal. Roadmap work must therefore be classified as one of:

- core research advancing existence, universality, necessity, minimality, or boundary analysis;
- supporting engineering enabling reproducible research;
- maintenance preserving repository and implementation integrity;
- applications demonstrating or testing bounded use cases.

Completion of infrastructure, validation, or mechanization does not by itself resolve the central research question.

---

# Phase I — Repository Architecture

## Objective

Establish the organizational and conceptual structure of Project FAR.

### Components

- Documentation (`docs/`)
- Foundational Architecture of Reasoning Analysis (`frameworks/FARA/`)
- Foundational Analysis of Reasoning (`frameworks/FAR/`)
- Foundational Analysis of Reasoning Operations (`frameworks/FARO/`)
- Repository organization
- Canonical terminology
- Dependency structure

### Status

✅ Complete

---

# Phase II — Formal Theory

## Objective

Develop the mathematical foundation of Project FAR.

### Components

- Definitions
- Axioms
- Conjectures
- Propositions
- Lemmas
- Theorems
- Proofs

### Status

🟡 In Progress

---

# Phase III — Validation

## Objective

Evaluate the applicability of Project FAR across existing reasoning frameworks.

### Validation Studies

- Scientific Method
- Mathematical Proof
- Bayesian Reasoning
- Legal Reasoning
- Historical Method
- Software Engineering
- Additional reasoning frameworks

### Status

Current completion state is recorded in `PROJECT_STATUS.md`.

---

# Phase IV — Examples

## Objective

Demonstrate Project FAR through complete worked investigations.

### Examples

- Simple Investigation
- Mathematical Proof
- Scientific Investigation
- Historical Analysis
- Disagreement Analysis

### Status

Current completion state is recorded in `PROJECT_STATUS.md`.

---

# Phase V — Research

## Objective

Evaluate the central hypothesis under the [Central Research Program](governance/central-research-program.md).

### Areas of Research

- existence of a common reasoning structure
- universality across reasoning processes
- primitive and assumption necessity
- architectural and semantic minimality
- counterexample construction
- boundary identification
- competing simpler structures
- expressive power
- alternative formulations
- unresolved uncertainty

### Status

🟡 Ongoing

---

# Phase VI — Publication

## Objective

Prepare mature portions of Project FAR for public dissemination.

### Deliverables

- Technical papers
- Reference manual
- Tutorials
- Case studies
- External documentation

### Status

⚪ Planned

---

---

# Release Track

## Current Release

v0.3.0 is the current release baseline. The v0.3.0 milestone is complete and is documented in [`docs/releases/project-far-v0.3.0.md`](releases/project-far-v0.3.0.md).

## Current Phase

v0.4 is the current development phase. Its objective is external validation preparation and execution against reasoning systems, arguments, and practices not constructed for FAR.

## Completed v0.3 Milestones

- v0.3.0 internal validation baseline: complete.
- Primitive-sufficiency evaluation: complete for the analyzed internal corpus.
- Dashboard, planning, repository-health, and release-readiness automation: complete for the v0.3 release checkpoint.
- Release documentation and GitHub release notes: complete.

## v0.4 Objectives

- Preserve v0.3.0 as the internal-validation baseline.
- Execute external validation without silently rewriting v0.3 conclusions.
- Separate external evidence from internal fixture evidence.
- Identify recurring external pressure points.

# Long-Term Goal

Reach the strongest justified conclusion about whether a common structure of reasoning exists, whether FAR captures it within an explicitly justified scope, whether every retained component is necessary, and whether any simpler competing structure has equal expressive power.

Project success is measured by answering that question rigorously, not by forcing confirmation of FAR.
## Comparative Representation Evaluation Roadmap

Comparative Representation Protocol v1.0 is registered under `theory/evaluation/comparative-representation/protocol-v1.0.md`. The next research step is CRE-001 execution after evaluator-facing materials are frozen and assignments are isolated. Experiment 1 has not yet been executed, and legacy external-validation evidence remains preliminary rather than comparative.
