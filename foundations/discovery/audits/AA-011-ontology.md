# AA-011 — Ontology Artifact Audit

## Status

Active Artifact Audit

## Target

`frameworks/FARA/ontology.md`

## Objective

Audit the FARA Ontology document against Phase II standards using only the fetched repository contents.

This audit does not revise the target document directly.

## Source Evidence

The document defines the ontological structure of FARA.

It distinguishes primitive concepts from derived concepts and delegates terminology to `theory/definitions/definitions.md`.

It identifies five current candidate primitives:

- Investigation;
- Representation;
- Representational Structure;
- Interpretation;
- Reasoning Calculus.

It identifies derived concepts including Reasoning State, Transition Signature, Candidate, Admissibility Structure, Resolution Rule, and Resolution.

## Audit Criteria

- primitive and derived distinction;
- dependency clarity;
- reduction pressure;
- category collapse under MI-001;
- consistency with `primitives.md`;
- grounding consistency with GP-001 through GP-012;
- knowledge traceability;
- revision justification.

## Findings

### AA-011-F1 — Ontology Is Stronger Than the Primitive Registry

Unlike `primitives.md`, this document narrows the primitive set to five concepts and classifies several FARA components as derived.

This is a major improvement because Reasoning State, Transition Signature, Candidate, Admissibility Structure, Resolution Rule, and Resolution are treated as derived rather than primitive.

### AA-011-F2 — Conflict with `primitives.md`

`primitives.md` lists eleven candidate primitives, while `ontology.md` lists five candidate primitives and treats the remaining six as derived.

This is an internal inconsistency.

Recommendation: reconcile the primitive registry with the ontology after the current audit wave.

### AA-011-F3 — Candidate Primitive Status Needs More Explicit Wording

The document says the five primitive concepts are presently regarded as irreducible within the framework.

It later says the ontology is provisional and every candidate primitive remains subject to revision.

The latter statement is methodologically stronger.

Recommendation: replace or qualify "presently regarded as irreducible" with "currently treated as candidate primitives pending reduction testing."

### AA-011-F4 — Derived Concepts Include Epistemic Objects

The document includes Evidence, Observation, Hypothesis, Proof, Argument, Explanation, Model, Theory, Prediction, and Counterexample as derived concepts.

This overlaps with the Knowledge Layer introduced by KA-001.

Recommendation: distinguish FARA ontological concepts from Knowledge Layer epistemic objects.

### AA-011-F5 — Reduction Principle Is Strong

The document states that Project FAR prefers reduction over expansion and that a concept should be regarded as primitive only after reasonable derivation attempts fail.

This aligns with Phase II methodology and prevents premature primitive inflation.

### AA-011-F6 — Traceability Is Still Missing

The document identifies primitive and derived concepts but does not link them to grounding investigations, audits, or Knowledge Layer objects.

Recommendation: after Knowledge Layer validation, each primitive and derived concept should include grounding status and evidence links.

## Overall Assessment

This is one of the stronger FARA documents because it imposes a cleaner primitive-derived split than `primitives.md`.

However, it creates a direct inconsistency with `primitives.md`.

The ontology should likely guide revision of the primitive registry, not the other way around.

## Revision Recommendation

A future revision is justified.

Recommended changes:

- reconcile primitive set with `primitives.md`;
- qualify candidate primitive language;
- distinguish ontology from Knowledge Layer epistemic objects;
- add grounding-status links after Knowledge Layer validation.

## Audit Outcome

Status: Strong but inconsistent with `primitives.md`.

The core ontology direction is sound, but the repository must reconcile primitive counts and concept typing before FARA can stabilize.
