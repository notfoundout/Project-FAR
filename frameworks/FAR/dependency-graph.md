# FAR Dependency Graph

## Purpose

This document records the dependency structure among the core documents and concepts of the Foundational Analysis of Reasoning (FAR).

It is a maintenance artifact intended to prevent circular definitions, duplicated stage definitions, and methodological drift.

This document does not introduce new definitions.

---

## Document Dependency Order

The FAR document dependency order is:

```text
theory/definitions/definitions.md
  -> theory/theorems/Project-FAR-Theory-Closure-v1.0.md
  -> frameworks/FARA/
  -> methodology/contract-discovery-protocol.md
  -> frameworks/FAR/workflow.md
  -> frameworks/FAR/methodology.md
  -> frameworks/FAR/application.md
```

This order is a document-maintenance order.

It does not assert philosophical priority, conceptual fundamentality, or chronological rigidity.

`contract-discovery-protocol.md` governs the pre-contract boundary only when supplied input leaves result-determining contract parameters open. `workflow.md` remains the canonical source for the FAR stage sequence. `methodology.md` governs the principles for using that workflow.

Navigation and maintenance documents depend on the whole FAR set:

```text
frameworks/FAR/README.md
frameworks/FAR/dependency-graph.md
frameworks/FAR/design-principles.md
frameworks/FAR/FAR-v1.0-criteria.md
frameworks/FAR/faro-boundary.md
frameworks/FAR/example-standard.md
frameworks/FAR/investigation-validation.md
```

---

## Dependency Roles

### Canonical Definitions

Repository-wide technical terminology is defined in:

`theory/definitions/definitions.md`

FAR documents use these definitions rather than redefining them.

---

### Shared theory and FARA

Shared theory supplies contracts, behavior maps, factorization, observational quotients, and boundary theorems. FARA provides the selected v1 representation target used by FAR when applicable.

FAR depends on FARA for concepts such as:

- reasoning states;
- transition signatures;
- admissibility structure;
- resolution rules;
- resolution executions;
- resolutions.

FAR applies these roles methodologically and must separately establish adequacy under the declared contract.

It does not modify their definitions.

---

### Contract discovery

`methodology/contract-discovery-protocol.md` governs the transition from under-specified input to an explicit frozen family of comparison contracts when that transition is required.

It preserves raw input, material ambiguities, provenance, exclusions, assumptions, search boundaries, contract-family coverage, freeze order, and deterministic cross-contract aggregation.

It does not define application-domain truth and does not replace the downstream contract semantics.

---

### Workflow

`workflow.md` is the canonical source for the ordered FAR investigation stages.

Other FAR documents may summarize the workflow, but they should not maintain independent stage definitions.

Candidate generation belongs within Stage 6 — Perform Reasoning.

Stage 7 materializes calculus-produced classifications and provenance through the derived Admissibility Structure (Ω).

---

### Methodology

`methodology.md` defines the principles governing use of the FAR workflow.

It explains how investigations should remain explicit, auditable, reconstructible, neutral, and reproducible.

It depends on `workflow.md` for the canonical stage sequence and on the contract-discovery protocol for the governed pre-contract boundary when applicable.

---

### Application

`application.md` describes how FAR is applied across domains.

It depends on `workflow.md` for stage structure and on `methodology.md` for methodological principles.

---

## Concept Dependency Flow

When a complete comparison contract is supplied, the core methodological dependency flow remains:

```text
Investigation
  -> Representational Structure
  -> Interpretation
  -> Reasoning Calculus
  -> Reasoning State
  -> Transition Signature
  -> Candidate Generation
  -> Admissibility Structure (Ω)
  -> Resolution Rule
  -> Resolution
```

When result-determining contract parameters are under-specified, the governed precondition is:

```text
Raw Input
  -> Material Parse / Interpretation Discovery
  -> Provenance / Exclusions / Assumptions
  -> Complete Bounded Contract Family
  -> Intake Freeze
  -> Investigation
```

These flows describe methodological dependence, not strict chronological irreversibility.

Candidate generation is included within reasoning activity rather than elevated to a separate universal stage. Pre-contract interpretation discovery is distinct from Stage 6 candidate generation.

FAR investigations may iterate and revisit earlier stages. A material change to frozen intake invalidates dependent evaluations.

---

## Dependency Constraints

The following constraints must be preserved:

- FAR shall not redefine terms canonically defined in `theory/definitions/definitions.md`.
- FAR shall not redefine architectural concepts defined by FARA.
- FAR shall not introduce new primitives.
- FAR shall not silently complete result-determining contract parameters left open by supplied input.
- FAR shall not collapse reasoning states with reasoning state representations.
- FAR shall not collapse transition signatures with transformation executions.
- FAR shall not collapse admissibility with the Admissibility Structure (Ω).
- FAR shall not collapse resolution rules, resolution executions, and resolutions.
- FARO shall not be developed as an operational layer until FAR is stable.

---

## Maintenance Policy

This dependency graph should be updated whenever:

- a FAR document is added, removed, or re-scoped;
- the canonical workflow changes;
- FAR's dependency on FARA changes;
- a relevant canonical definition changes;
- a methodological stage is added, removed, or renamed;
- the governed pre-contract intake boundary changes.

Dependency updates should be justified by artifact audits, framework revisions, or explicit architectural review.

## Contract-relative dependency

A sufficiency claim depends on the comparison contract, behavior map, representation mapping, and decoder/collision evidence. A minimality claim additionally depends on the observational equivalence or a declared cost order. None may depend on a downstream implementation's success as a substitute for the theorem.

When the supplied input does not determine the comparison contract, any non-`Unknown` cross-contract result additionally depends on a valid frozen governed intake record covering the active material interpretation family.
