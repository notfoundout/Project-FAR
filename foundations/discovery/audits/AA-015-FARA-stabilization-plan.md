# AA-015 — FARA Stabilization Plan

## Purpose

Convert the completed audit wave (AA-004 through AA-014) into an implementation roadmap for stabilizing FARA.

## Stable Artifacts

No immediate conceptual revision justified:
- frameworks/FARA/architecture.md
- frameworks/FARA/semantics.md
- Most of frameworks/FARA/admissibility-structure.md

## Targeted Revision Required

- theory/definitions/definitions.md
- frameworks/FARA/reasoning-states.md
- frameworks/FARA/transition-signatures.md
- frameworks/FARA/primitives.md

## Repository Inconsistencies

1. Primitive registry and ontology disagree on the current primitive set.
2. Reasoning state is repeatedly conflated with its representation.
3. Transformation definitions conflate rules with processes/executions.
4. The ontological type of Ω should be made explicit.
5. Grounding traceability is largely absent from canonical artifacts.

## Ordered Revision Plan

### Phase A
Revise canonical definitions to resolve audited category collapses.

### Phase B
Update dependent FARA documents to reference the revised definitions.

### Phase C
Re-run affected audits (AA-005, AA-006, AA-007, AA-010, AA-011, AA-014).

### Phase D
Reconcile the primitive registry with the ontology.

## Exit Criteria for FARA v1.0

- Canonical definitions pass audit.
- No unresolved category-collapse findings remain.
- Primitive registry matches ontology.
- Core architectural concepts trace to grounding investigations.
- Audit findings are either resolved or explicitly deferred.

## Outcome

The project should now transition from discovery-oriented architecture expansion to evidence-driven stabilization. Future changes should be justified by audit evidence rather than introducing new architectural concepts.