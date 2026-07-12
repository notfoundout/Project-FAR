# External Validation Methodology

Status: v0.4.1 investigation-evaluation protocol.

## Purpose

External validation tests Project FAR against reasoning systems that were not designed for FAR. The objective is to use the existing FAR instrument rather than add new primitives or reshape the target systems to make them fit.

This methodology distinguishes internal fixtures from external systems. Internal fixtures show that FAR can represent curated examples. External validation asks whether independently established reasoning systems can be mapped without introducing a sixth primitive.

## Relationship to Other Methodologies

This document is an investigation methodology for evaluating external reasoning systems against FAR/FARA. It does not replace:

- FAR investigation validation, which checks whether a completed FAR investigation is reconstructible and methodologically complete;
- proof methodology, which governs acceptance of propositions, constructions, theorems, and formal objects;
- adversarial methodology, which prioritizes attempts to falsify primitive sufficiency;
- repository governance, which controls canonical locations, artifact status, promotion, and protected boundaries.

A successful external representation is evidence about the evaluated system only. It does not prove universality, necessity, or minimality.

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

## Investigation Record Requirements

Each external-system investigation must record the following fields, either as substantive content or as explicitly justified `Not applicable`, `Unknown`, or `Unresolved` entries:

1. independent description of the target reasoning system;
2. assumptions used by the evaluator;
3. source evidence used to describe the system;
4. FAR/FARA representation;
5. representation fidelity;
6. semantic preservation;
7. structural preservation;
8. operational preservation;
9. dependency preservation;
10. information preservation;
11. required FAR/FARA components;
12. unused FAR/FARA components;
13. alternative representations considered;
14. potential counterexamples;
15. counterexample classification;
16. limitations;
17. implications for universality, necessity, and minimality.

The required template is maintained in `external-system-investigation-template.md`.

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

## Preservation Review

The evaluation must distinguish the following preservation claims:

- representation fidelity: whether the FAR/FARA representation records the target system without ad hoc reshaping;
- semantic preservation: whether meaning, truth conditions, validity standards, or other semantics are preserved or explicitly scoped;
- structural preservation: whether objects, relations, ordering, dependency, context, or other target structure are preserved;
- operational preservation: whether rules, transitions, updates, proof steps, or procedures are preserved;
- dependency preservation: whether source dependencies and internal dependencies are explicit;
- information preservation: whether the mapping loses information relevant to the target reasoning process.

A failure in any preservation dimension must be classified as a limitation, unresolved issue, conservative extension pressure, outside-scope reason, or candidate primitive failure according to the classification rules below.

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

## Counterexample Classification

Potential counterexamples must be classified as one of:

- `not a counterexample`: the case maps under existing primitives without unresolved pressure;
- `conservative extension pressure`: the case requires domain-specific interpretation, structure, calculus, or derived concepts but no new primitive;
- `unresolved`: the case cannot yet be classified from available evidence;
- `outside scope`: the case lacks accessible explicit reasoning or stable description;
- `candidate primitive failure`: the case satisfies the primitive failure standard.

## Universality, Necessity, and Minimality Discipline

External validation must keep these claims separate:

- representation success does not imply universality;
- universality does not imply minimality;
- minimality requires separate justification under the applicable proof and primitive-evaluation standards.

An investigation may strengthen or weaken evidence relevant to universality, necessity, or minimality, but it may not promote any of those claims by classification alone.

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
