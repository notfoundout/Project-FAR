# GP-010 — Model Grounding Investigation

## Status
Active Grounding Investigation

## Objective
Determine whether a model is a primitive concept or a derived representational construct.

## Initial Observation
Previous investigations consistently separated:

- object from representation;
- representation from interpretation;
- investigation from record.

This suggests a model may itself be a structured representational artifact rather than a foundational primitive.

## Hidden Assumptions
- Every model represents reality.
- A model is identical to the system it models.
- Every representation is a model.
- Every model has one correct interpretation.
- Models are inherently explanatory.

## Attack 1 — Model vs Represented System
A flight simulator is not an aircraft.
A graph model is not the network.
A mathematical model is not the physical system.

Result:

Model ≠ Represented System.

## Attack 2 — Model vs Representation
A single diagram is a representation.
A model generally consists of many coordinated representations, assumptions, constraints, and interpretation rules.

Result:

Model ≠ Representation.

## Attack 3 — Model vs Theory
A theory may justify why a model is appropriate.
A model operationalizes or instantiates assumptions from a theory.

Result:

Model ≠ Theory.

## Candidate Decomposition
- Represented System
- Model
- Representations
- Interpretation
- Assumptions
- Constraints

## Candidate Weak Characterization
A model is provisionally characterized as:

> A structured representational construct that, under specified assumptions and interpretation, is intended to correspond to selected aspects of a target domain.

## Dependency Hypothesis
Target Domain
↓
Model
↓
Representations
↓
Interpretation

## Interim Result
The strongest current separation is:

Model ≠ Representation ≠ Theory ≠ Represented System

No canonical revision is recommended until GP-011 (Theory) tests whether theory and model remain consistently separable across the repository.