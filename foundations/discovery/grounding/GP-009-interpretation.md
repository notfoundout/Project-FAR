# GP-009 — Interpretation Grounding Investigation

## Status
Active Grounding Investigation

## Investigation Objective
Determine whether Interpretation is primitive or a derived relation between representations and what they denote.

## Central Hypothesis
Interpretation is neither a representation nor a represented entity. It is the relation that assigns semantic significance to a representation.

## Hidden Assumptions
- Every representation has an interpretation.
- Interpretation is unique.
- Interpretation is intrinsic to a representation.
- Interpretation changes whenever a representation changes.
- Interpretation is identical to meaning.

These assumptions require testing.

## Attack 1 — Representation Without Interpretation
A sequence of symbols may exist without any assigned semantics.

Result:

Representation may exist without interpretation.

## Attack 2 — Multiple Interpretations
The same representation may legitimately receive different interpretations under different formal systems.

Result:

Interpretation is context-dependent rather than intrinsic.

## Attack 3 — Interpretation vs Meaning
Meaning is what is obtained under an interpretation.
Interpretation is the mapping or assignment process.

Result:

Interpretation ≠ Meaning.

## Candidate Decomposition
- Representation
- Interpretation
- Semantic Domain
- Denoted Entity
- Meaning

## Candidate Weak Characterization
Interpretation is provisionally characterized as:

> A relation that associates one or more representations with entities, structures, or meanings under explicitly specified semantic conventions.

## Dependency Hypothesis
Representation
↓
Interpretation
↓
Meaning / Denoted Entity

## Open Questions
1. Is interpretation fundamentally a relation?
2. Can one interpretation map many representations?
3. Can one representation map to many meanings?
4. What role does context play?
5. Is interpretation required for every repository artifact?

## Interim Result
The strongest current separation is:

Representation ≠ Interpretation ≠ Meaning ≠ Denoted Entity

No canonical revision is justified until downstream concepts such as Model and Theory are tested against this split.