# Project Roadmap

## Purpose

This document describes the long-term development plan of Project FAR.

It identifies the major phases of the project, their objectives, and their current status.

Unlike the formal theory, this document serves as a project management and planning resource.

## Governing Research Direction

The [Central Research Program](governance/central-research-program.md), [Anti-Self-Validation Standard](governance/anti-self-validation-standard.md), and [Research Priority Reset](governance/research-priority-reset.md) govern future major work.

Project FAR exists to determine whether reasoning instantiates a common underlying structure and, if so, whether that structure is universal and minimal. Roadmap work must therefore be classified as one of:

- core research advancing existence, universality, necessity, minimality, nontriviality, or boundary analysis;
- supporting engineering enabling reproducible research;
- maintenance preserving repository and implementation integrity;
- applications demonstrating or testing bounded use cases.

Completion of infrastructure, validation, or mechanization does not by itself resolve the central research question.

## Current Research Reset

The active milestone is a decisive prospective test of nontrivial adequacy, local necessity, comparative economy, and independence. The controlling gate registry is [`theory/evaluation/research-gates.json`](../theory/evaluation/research-gates.json).

The active sequence is:

1. freeze a vocabulary-neutral external observation contract;
2. register positive and negative controls;
3. freeze full-cost accounting and anti-reintroduction rules;
4. complete an explicitly nonconfirmatory internal pilot;
5. freeze a confirmatory package;
6. execute independent and adversarial replications;
7. publish the full result distribution, failures, unresolved outcomes, and nonclaims;
8. decide whether to continue, revise, restrict, reduce, or reject the candidate theory.

New certification layers, dashboards, release packaging, favorable-case expansion, generic cleanup, and unrelated applications are paused by default unless required for this sequence.

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

🟡 In Progress, but theory strengthening is subordinate to current falsification and comparative gates.

---

# Phase III — Validation

## Objective

Evaluate the applicability of Project FAR across existing reasoning frameworks without allowing successful representation alone to count as universality, necessity, minimality, or superiority.

### Validation Studies

- Scientific Method
- Mathematical Proof
- Bayesian Reasoning
- Legal Reasoning
- Historical Method
- Software Engineering
- Additional reasoning frameworks

### Status

Bounded internal and external-validation work exists. Confirmatory independence and nontriviality remain unsatisfied. Current completion state is recorded in `project-status.md` and `theory/evaluation/research-gates.json`.

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

Current completion state is recorded in `project-status.md`. New favorable examples are not an active priority unless they serve a frozen boundary or negative-control experiment.

---

# Phase V — Decisive Research

## Objective

Evaluate the central hypothesis under the [Central Research Program](governance/central-research-program.md) and prevent the project from becoming its own sole source of theory, cases, metrics, verification, and adjudication.

### Required Gates

- external observation contract;
- nontriviality and negative controls;
- local primitive ablation with anti-reintroduction review;
- full-cost comparative accounting;
- independent implementation or evaluation;
- private-holdout counterexample challenge;
- nonclaim audit before evidence release.

### Status

🟡 Active. All gates are prospectively registered as not satisfied until evidence is recorded.

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

⚪ Deferred for central-claim publication until the required evidential gates are satisfied. Bounded engineering or methods publications must retain explicit nonclaims.

---

# Release Track

## Current Release

v0.4.0 is the current release baseline. The v0.4.0 milestone is complete and is documented in [`docs/releases/project-far-v0.4.0.md`](releases/project-far-v0.4.0.md). The previous v0.3.0 internal-validation baseline remains documented in [`docs/releases/project-far-v0.3.0.md`](releases/project-far-v0.3.0.md).

## Current Phase

Post-v0.4.0 work has produced deterministic comparative-representation infrastructure and bounded prospective evidence. The next phase is not general expansion. It is execution of the registered anti-self-validation research gates.

## Completed v0.3 Milestones

- v0.3.0 internal validation baseline: complete.
- Primitive-sufficiency evaluation: complete for the analyzed internal corpus.
- Dashboard, planning, repository-health, and release-readiness automation: complete for the v0.3 release checkpoint.
- Release documentation and GitHub release notes: complete.

## v0.4 Objectives

Status: ✅ Complete as v0.4.0.

The historical v0.4.0 objectives are preserved:

- Preserve v0.3.0 as the internal-validation baseline.
- Execute external validation without silently rewriting v0.3 conclusions.
- Separate external evidence from internal fixture evidence.
- Identify recurring external pressure points.

Completed v0.4.0 work also exceeded the original milestone by adopting CRP v1.0 as the frozen canonical methodology for future comparative representation studies and registering comparative experiments. Later work completed deterministic implementation at registered scopes.

## Next Development Milestone

Complete the external observation contract, negative-control suite, full-cost model, and anti-reintroduction ablation method; then package and run the first prospective pilot governed by the anti-self-validation standard. Do not prioritize the next evidence release before these gates generate a result worth releasing.

# Long-Term Goal

Reach the strongest justified conclusion about whether a common structure of reasoning exists, whether FAR captures it within an explicitly justified scope, whether every retained component is necessary, and whether any simpler competing structure has equal expressive power.

Project success is measured by answering that question rigorously, not by forcing confirmation of FAR.

## Comparative Representation Evaluation Roadmap

Comparative Representation Protocol v1.0 remains a registered baseline. Completed deterministic implementation and bounded experiments remain preserved evidence, but they do not satisfy the new prospective gates by themselves. Legacy external-validation evidence remains preliminary rather than prospective independent comparative evidence. Future confirmatory work must use the confirmatory research package, the research-gate registry, full-cost accounting, negative controls, and declared independence levels.
