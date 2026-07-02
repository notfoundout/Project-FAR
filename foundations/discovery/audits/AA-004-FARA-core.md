# AA-004 — FARA Core Artifact Audit

## Status

Active Artifact Audit

## Target

`frameworks/FARA/README.md`

## Objective

Audit the FARA top-level core document against Phase II standards using only the document as fetched from the repository.

This audit does not revise FARA directly.

## Source Evidence

The target document states that FARA is the Foundational Architecture of Reasoning Analysis and that it investigates whether structured, explicit, auditable reasoning can be represented by a common minimal architecture.

It also states that the architecture is defined through primitive concepts, derived concepts, and relationships, with formal definitions maintained in `theory/definitions/definitions.md`.

## Audit Criteria

- hidden assumptions;
- dependency clarity;
- scope clarity;
- explicitness;
- category collapse under MI-001;
- grounding consistency with GP-001 through GP-012;
- knowledge traceability;
- revision justification.

## Findings

### AA-004-F1 — Purpose Is Clear but Scope Is Broad

The README gives a clear high-level purpose: FARA investigates whether structured, explicit, auditable reasoning can be represented by a common minimal architecture.

However, the scope of `reasoning` is not bounded inside the README.

This creates scope ambiguity because FARA may apply to mathematical reasoning, empirical reasoning, legal reasoning, informal argument, AI reasoning, or repository self-analysis, but the README does not specify whether all are intended.

Recommendation: future revisions should state whether FARA is universal, domain-general, or currently limited to Project FAR internal reasoning artifacts.

### AA-004-F2 — Primitive and Derived Concepts Are Referenced but Not Grounded Here

The README says FARA is defined through primitive concepts, derived concepts, and their relationships.

This is structurally useful, but the README does not identify the current primitive set or its research status.

Given Phase II grounding, many candidate primitives are still under investigation or have been decomposed.

Recommendation: add a status note distinguishing canonical primitives from candidate primitives and grounded concepts.

### AA-004-F3 — Definitions Are Delegated Without Traceability

The README delegates formal definitions to `theory/definitions/definitions.md`.

That is appropriate for avoiding duplication, but it does not provide a trace to grounding investigations, audits, or knowledge claims.

Recommendation: after the Knowledge Layer pilot is validated, FARA should link major architectural claims to supporting investigations or claim objects.

### AA-004-F4 — Category Collapse Risk: Architecture vs Investigation

The README states that FARA "investigates" whether reasoning can be represented by a common minimal architecture, while also saying the directory "defines" the architecture.

This creates a possible category tension:

```text
FARA as investigation
FARA as architecture
FARA as repository directory
```

These are not necessarily the same object.

Recommendation: distinguish the FARA research program from the FARA architecture and from the repository directory that records it.

### AA-004-F5 — Category Collapse Risk: Representation vs Architecture

The README asks whether reasoning can be "represented by" a common minimal architecture.

This is close to GP-008 and C-001 territory.

It should remain clear that:

```text
reasoning process ≠ representation of reasoning process ≠ architecture used to analyze reasoning
```

Recommendation: future FARA documents should preserve the representation/entity distinction explicitly.

### AA-004-F6 — Transition and State Documents Require Follow-Up Audits

The README lists `reasoning-states.md`, `transition-signatures.md`, and `admissibility-structure.md`.

These directly depend on GP-005 and GP-006 findings.

Recommendation: audit those files next before revising the README, because the README itself functions mainly as an index.

## Knowledge Layer Use

The pilot Knowledge Layer improved this audit by providing specific checks:

- C-001 exposed the representation/entity risk;
- C-002 exposed the need to audit transition and execution language;
- H-001 provided the category-collapse diagnostic;
- Q-001 flagged unresolved interpretation requirements.

This supports continuing the Knowledge Layer pilot during AA-005 and deeper FARA subfile audits.

## Overall Assessment

`frameworks/FARA/README.md` is structurally sound as a top-level index.

It is not sufficient as a full FARA core specification.

The document is useful, but it currently lacks explicit scope boundaries, grounding status, and traceability from architectural claims to supporting investigations.

## Revision Recommendation

No immediate rewrite is required.

A targeted future revision is justified after auditing the listed FARA subdocuments.

Recommended future additions:

- scope statement;
- distinction between FARA as research program, architecture, and repository directory;
- primitive/concept status note;
- links to grounding investigations or Knowledge Layer claim objects.

## Audit Outcome

Status: Provisionally sound as an index.

Requires deeper audit of FARA subdocuments before framework-level revision.
