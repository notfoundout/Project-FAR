# AA-014 — Canonical Definitions Artifact Audit

## Status

Active Artifact Audit

## Target

`theory/definitions/definitions.md`

## Objective

Audit the canonical definitions file against Phase II standards and the completed FARA audit wave.

This audit does not revise the target document directly.

## Source Evidence

The target document states that it contains the canonical definitions of formal terminology used throughout Project FAR.

It also states that canonical usage does not mean every definition has been derived from first principles or proven necessary, and that definitions remain subject to revision when audits, proof attempts, counterexamples, or methodology work expose problems.

## Audit Criteria

- authority clarity;
- grounding status;
- hidden assumptions;
- circularity;
- category collapse under MI-001;
- consistency with FARA audits AA-004 through AA-012;
- primitive and derived concept consistency;
- traceability to grounding investigations and Knowledge Layer objects.

## High-Level Findings

### AA-014-F1 — Authority Notice Is Strong

The authority notice correctly distinguishes canonical repository usage from first-principles grounding.

This prevents the definitions file from overclaiming proof, necessity, or finality.

This is a major strength.

### AA-014-F2 — Definitions Are Well Layered but Not Fully Typed

The file is organized into foundational, framework, formal, representational, reasoning, and decision concepts.

This improves readability and reduces accidental mixing.

However, several definitions still require stronger type separation.

### AA-014-F3 — Representation Definition Requires Refinement

Representation is defined as an explicitly distinguishable object used to represent information within an investigation.

This is useful, but it introduces the term information without defining it.

It also risks tying representation too tightly to investigation.

Recommendation: clarify whether representations can exist outside investigations, or whether Project FAR only concerns representations as used within investigations.

### AA-014-F4 — Investigation Definition Is Underdecomposed

Investigation is defined as specifying the object of analysis together with the criteria by which reasoning is organized.

GP-007 and later audits indicate that investigation should likely be decomposed into process, record, target, method, state, and outcome.

Recommendation: revise or supplement the definition after GP-007 findings are incorporated.

### AA-014-F5 — Transformation Definition Collapses Rule and Process

Transformation is defined as a rule or process that maps one state to another.

This directly reproduces the rule/process collapse found in prior grounding and FARA audits.

Recommendation: distinguish transformation rule, transformation instance, transformation execution, and transformation representation.

### AA-014-F6 — Reasoning State Definition Repeats Known Collapse

Reasoning State is defined as the complete explicit representation of an investigation at a particular stage of reasoning, and as a specialized form of state.

AA-005 found this unstable because reasoning state is collapsed with representation of reasoning state.

Recommendation: distinguish reasoning configuration, reasoning state, reasoning state representation, and reasoning state record.

### AA-014-F7 — Transition Signature Definition Is Directionally Sound

Transition Signature is defined as the explicit description of the transformation between two reasoning states.

This is mostly compatible with AA-006 because it treats the signature as a description.

However, it depends on the transformation definition being corrected.

### AA-014-F8 — Admissibility Structure Definition Is Mostly Stable

Ω is defined as classifying admitted candidates according to the applicable reasoning calculus and recording each candidate's admissibility status.

This aligns with AA-007.

Remaining issue: specify whether Ω is a relation, classification state, representation, or record.

### AA-014-F9 — Primitive and Ontology Tension Remains

The file defines primitive as a concept not derived from simpler concepts within the framework.

This is sound in isolation.

However, the repository still contains tension between `primitives.md` and `ontology.md` over which concepts currently count as primitives.

Recommendation: reconcile the primitive registry with the ontology after definition revisions.

### AA-014-F10 — Scope and Universality Definitions Are Strong

Scope, Universal, Universal Architecture, Minimal, Equivalence, and Expressive Power are relatively strong because they explicitly require a stated domain, relation, or scope.

These definitions should be retained with minimal change.

## Stable Definition Families

Currently stable or nearly stable:

- Scope;
- Universal;
- Universal Architecture;
- Minimal;
- Equivalence;
- Expressive Power;
- Syntax;
- Semantics;
- Interpretation;
- Candidate;
- Criterion;
- Classification;
- Resolution Rule;
- Resolution.

## Definitions Requiring Priority Review

High-priority revision candidates:

- Representation;
- Investigation;
- Transformation;
- Reasoning State;
- Transition Signature;
- Admissibility Structure;
- Primitive;
- Derived Concept;
- Reduction;
- Independence.

## Knowledge Layer Impact

The audit confirms the usefulness of the Knowledge Layer pilot.

C-001, C-002, E-001, E-002, H-001, and Q-001 all provided direct checks against the canonical definitions.

The canonical definitions file should eventually link to relevant grounding investigations and Knowledge Layer objects.

## Revision Decision

A definitions revision is justified.

However, it should be targeted, not global.

Recommended priority:

1. Correct category collapses in Transformation and Reasoning State.
2. Decompose Investigation using GP-007.
3. Clarify Representation and Information.
4. Type Ω more explicitly.
5. Reconcile primitive registry and ontology.

## Audit Outcome

Status: structurally strong but conceptually mixed.

The file is appropriate as a canonical usage layer, but several definitions remain framework-internal specifications rather than grounded foundational results.

A targeted revision pass is justified before declaring FARA stable.
