# AA-005 — Reasoning States Artifact Audit

## Status

Active Artifact Audit

## Target

`frameworks/FARA/reasoning-states.md`

## Objective

Audit the FARA Reasoning States document against Phase II standards using only the fetched repository contents.

This audit does not revise the target document directly.

## Source Evidence

The target document defines reasoning states within FARA. It says a reasoning state is the fundamental representational object through which reasoning is recorded and analyzed.

It also says reasoning states do not define how reasoning states are transformed or evaluated.

The central definition states that a reasoning state is the complete explicit representation of an investigation at a particular stage of reasoning.

## Audit Criteria

- hidden assumptions;
- dependency clarity;
- scope clarity;
- explicitness;
- category collapse under MI-001;
- grounding consistency with GP-005, GP-006, GP-007, and GP-008;
- knowledge traceability;
- revision justification.

## Findings

### AA-005-F1 — State and Representation Are Collapsed

The document defines a reasoning state as both a state and a representational object.

This is operationally useful, but Phase II grounding repeatedly separates a state from the representation of that state.

Relevant distinction:

Reasoning State is not identical to Reasoning State Representation.

Recommendation: future revision should distinguish reasoning state, reasoning state representation, and reasoning state record.

### AA-005-F2 — Completeness Is Investigation-Relative but Not Fully Scoped

The document uses completeness language in the central definition and again when saying the state contains the information required to continue or audit the investigation.

This is better than intrinsic completeness because it ties completeness to continuation and audit.

However, the scope of completeness remains underdefined.

Recommendation: define completeness relative to investigation, reasoning calculus, and audit objective.

### AA-005-F3 — Investigation and Stage Require Grounding

The definition depends on investigation and stage of reasoning.

GP-007 found that investigation should be decomposed into process, record, target, method, state, and outcome.

The document does not distinguish whether a reasoning state represents an investigation process, current investigation configuration, investigation record, or repository artifact.

Recommendation: incorporate the GP-007 distinction before canonizing the reasoning-state definition.

### AA-005-F4 — Positive Separation of Transformation and Evaluation

The document explicitly says reasoning states do not define how states are transformed or evaluated.

This is a strength.

It preserves the distinction between state, transformation, and evaluation.

### AA-005-F5 — Evolution Language Needs Type Separation

The document says reasoning states evolve through explicit transformations represented by transition signatures.

This is directionally sound, but GP-006 distinguishes transformation rule, transformation instance, transformation execution, and transformation representation.

A transition signature should likely be classified as a representation of a transition rather than the transition itself.

Recommendation: future revision should distinguish transformation occurrence, transformation rule, transformation instance, and transition signature.

### AA-005-F6 — Reasoning State Relationships Are Useful but Not Typed

The document says a reasoning state exists relative to an investigation, representational structure, interpretation, and reasoning calculus.

This is a useful dependency list.

However, the relation type is not specified.

For example, a reasoning state may be scoped by an investigation, encoded in a representational structure, interpreted under an interpretation, and constrained or advanced under a reasoning calculus.

Recommendation: type each dependency relation explicitly.

### AA-005-F7 — Knowledge Traceability Is Absent

The document delegates definitions to `theory/definitions/definitions.md`, but it does not link to grounding investigations or Knowledge Layer claim objects.

Relevant knowledge objects include C-001, C-002, E-001, and E-002.

Recommendation: after Knowledge Layer validation, add trace links from reasoning-state claims to supporting investigations and claim objects.

## Overall Assessment

The document is structurally useful and already contains one important separation: reasoning states do not define transformation or evaluation.

However, its central definition collapses reasoning state with representation of reasoning state.

That collapse is consistent with the category-collapse pattern identified in GP-005, GP-008, MI-001, and C-001.

## Revision Recommendation

A future revision is justified, but not immediately required before auditing related FARA documents.

Recommended future distinctions:

- Reasoning Configuration;
- Reasoning State;
- Reasoning State Representation;
- Reasoning State Record;
- Transition Signature;
- Transformation Instance;
- Transformation Execution.

## Audit Outcome

Status: Provisionally useful but conceptually unstable.

Requires revision after `transition-signatures.md` and `admissibility-structure.md` are audited.
