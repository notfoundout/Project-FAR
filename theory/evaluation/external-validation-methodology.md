# External Validation Methodology

Status: v0.4.0 initial external-evaluation protocol.

## Purpose

External validation tests Project FAR against reasoning systems that were not designed for FAR. The objective is to use the existing FAR instrument rather than add new primitives or reshape the target systems to make them fit.

This methodology distinguishes internal fixtures from external systems. Internal fixtures show that FAR can represent curated examples. External validation asks whether independently established reasoning systems can be mapped without introducing a sixth primitive.

## Inclusion Criteria

A system may be included when it has:

- an identifiable reasoning objective or class of objectives;
- explicit representations or formal objects;
- explicit structure over those objects;
- an interpretation or semantics;
- rules, transformations, proof standards, or update procedures.

## Exclusion Criteria

A system should not be counted as external validation evidence when:

- the reasoning process is inaccessible or purely opaque;
- the example is invented solely to fit FAR;
- the source system lacks a stable description;
- the evaluation cannot identify what would count as success or failure.

## Evaluation Questions

Each evaluated system must answer:

1. What is the investigation?
2. What are the representations?
3. What is the representational structure?
4. What assigns interpretation?
5. What is the reasoning calculus?
6. Does the system fit FAR directly?
7. Does it require a conservative extension?
8. Is it unresolved?
9. Does it suggest a sixth primitive?

## Classification Rules

Use exactly one classification per system.

### `fits FAR`

The system maps to the five FAR primitives without requiring new derived concepts or domain-specific extension machinery.

### `conservative extension`

The system requires domain-specific interpretation policy, structure, calculus, or derived concepts, but does not require a new primitive.

### `unresolved`

The system appears mappable, but current analysis is not sufficient to decide whether the required machinery is conservative.

### `outside scope`

The system lacks explicit accessible reasoning, or FAR can only represent an output rather than the reasoning process.

### `candidate primitive failure`

Use this only when analysis shows that the reasoning is explicit and cannot be represented through Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus, existing derived concepts, or conservative extensions of those primitives.

## Evidence Standard

A candidate primitive failure requires a specific missing capability. Difficulty, complexity, unfamiliar notation, or domain-specific semantics are not enough.

A conservative extension is not a failure of primitive sufficiency. It means the system needs additional machinery expressible within the current primitive architecture.

## Reporting Standard

Every system report must include:

- primitive mapping;
- classification;
- justification;
- pressure points;
- confidence;
- remaining questions.

The final report must aggregate classifications without claiming universality. A finite external corpus can strengthen or weaken confidence, but it cannot prove that the primitive set covers every possible explicit reasoning system.