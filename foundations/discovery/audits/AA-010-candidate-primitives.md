# AA-010 — Candidate Primitives Artifact Audit

## Status

Active Artifact Audit

## Target

`frameworks/FARA/primitives.md`

## Objective

Audit the FARA Candidate Primitives document against Phase II standards using only the fetched repository contents.

This audit does not revise the target document directly.

## Source Evidence

The document identifies the current candidate primitive concepts of FARA.

It defines a primitive as a concept that has not yet been derived from simpler concepts within the framework.

It explicitly states that candidate primitives are provisional and remain subject to reduction, replacement, or elimination.

## Audit Criteria

- primitive status clarity;
- dependency clarity;
- reduction pressure;
- category collapse under MI-001;
- grounding consistency with GP-001 through GP-012;
- knowledge traceability;
- revision justification.

## Findings

### AA-010-F1 — Candidate Status Is Correctly Preserved

The document avoids the major error of treating current primitives as permanently irreducible.

It explicitly says no candidate primitive should be regarded as permanently irreducible.

This is structurally strong.

### AA-010-F2 — Several Candidate Primitives Are Already Under Reduction Pressure

The current primitive list includes concepts that Phase II grounding has already decomposed or pressured:

- Investigation;
- Representation;
- Interpretation;
- Reasoning State;
- Transition Signature;
- Admissibility Structure;
- Resolution.

This does not make the list invalid, but it means the list should be treated as a research snapshot, not as an architectural foundation.

### AA-010-F3 — Derived Concepts Appear in the Primitive List

Reasoning State, Transition Signature, Admissibility Structure, Resolution Rule, and Resolution appear to be architectural constructs built from more basic concepts.

They may be necessary components of FARA, but necessity is not the same as primitiveness.

Recommendation: distinguish candidate primitive concepts from required architectural components.

### AA-010-F4 — Candidate Primitive Dependencies Are Not Shown

The document lists candidates but does not show dependency or reducibility relations among them.

For example:

- Reasoning State depends on Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus.
- Transition Signature depends on Reasoning State and Transformation.
- Admissibility Structure depends on Candidate, Investigation, Reasoning Calculus, and Reasoning State.

Recommendation: add a dependency table or graph after grounding stabilizes.

### AA-010-F5 — The Primitive Criterion Needs Operational Tests

The document says a primitive is a concept not yet derived from simpler concepts within the framework.

That is appropriate, but the document does not define what counts as a successful derivation or loss of expressive power.

Recommendation: define primitive-retention tests, reduction tests, and expressive-loss tests.

### AA-010-F6 — Knowledge Traceability Is Absent

The document does not link each candidate primitive to its grounding investigation, audit result, or Knowledge Layer object.

Recommendation: after the Knowledge Layer pilot is validated, each candidate primitive should link to its grounding status.

## Overall Assessment

This document is conceptually disciplined because it treats primitives as provisional.

However, the current list mixes probable primitives, candidate primitives, and required architectural components.

The main defect is not overclaiming irreducibility. The main defect is insufficient typing of the list.

## Revision Recommendation

A future revision is justified after completing audits of ontology, semantics, and canonical definitions.

Recommended future sections:

- Candidate Primitive;
- Derived Architectural Component;
- Under Reduction;
- Rejected Primitive;
- Grounding Status;
- Dependency Status;
- Expressive Role.

## Audit Outcome

Status: Strong cautionary artifact, weak primitive registry.

The document correctly preserves provisionality, but the primitive list should not be treated as stable until reduction and dependency tests are completed.
