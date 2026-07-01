# GP-008 — Representation Grounding Investigation

## Status

Active Grounding Investigation

## Phase

Phase II — Repository Grounding Program

## Concept Under Investigation

Representation

## Investigation Objective

Determine whether `Representation` is primitive or reducible, and separate it from the ontology, interpretation, and repository artifacts it has repeatedly been conflated with.

## Initial Observation

Throughout Phase I and early Phase II, one distinction has repeatedly survived independent investigations:

```text
Representation ≠ State
Representation ≠ Object
Representation ≠ Investigation
Representation ≠ Repository Artifact
```

Representation consistently behaves as a bridge rather than as the thing represented.

## Hidden Assumptions

Common uses of "representation" assume that:

- every representation represents something;
- representation implies interpretation;
- one representation corresponds to one represented entity;
- changing a representation changes the represented entity;
- repository artifacts are identical to representations.

These assumptions require testing.

## Attack 1 — Representation vs. Represented Entity

Different diagrams can represent the same graph.

Different equations can represent the same mathematical object.

Different encodings can represent the same state.

Therefore:

```text
represented entity ≠ representation
```

## Attack 2 — Representation vs. Interpretation

A string of symbols may exist without any assigned interpretation.

Interpretation supplies semantics.

Representation supplies form.

Therefore:

```text
representation ≠ interpretation
```

## Attack 3 — Representation vs. Repository Artifact

A markdown document may contain many representations.

The document itself is a repository artifact.

It is not identical to any one representation contained within it.

## Attack 4 — Representation Change

Changing notation does not necessarily change:

- the object;
- the state;
- the relation;
- the investigation outcome.

Representation change must therefore remain distinct from ontology change.

## Candidate Decomposition

Candidate distinctions:

- represented entity;
- representation;
- interpretation;
- representation medium;
- repository artifact.

## Candidate Weak Characterization

A representation is provisionally characterized as:

> An explicit artifact or structure intended to stand for, encode, or denote another entity under a specified interpretation.

This characterization remains provisional because the role of interpretation has not yet been grounded.

## Open Questions

1. Can a representation exist without interpretation?
2. Is interpretation part of representation or an external relation?
3. Can one representation legitimately represent multiple entities?
4. What distinguishes a representation from an arbitrary structure?
5. Does every repository artifact contain representations, or are some artifacts themselves representations?

## Interim Result

The strongest current result is the repeated separation:

```text
Representation ≠ Represented Entity ≠ Interpretation ≠ Repository Artifact
```

This split should be validated before any canonical rewrite.
