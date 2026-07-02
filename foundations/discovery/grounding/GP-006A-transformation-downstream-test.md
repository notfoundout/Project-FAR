# GP-006A — Transformation Split Downstream Test

## Status

Active Grounding Test

## Parent Investigation

`GP-006-transformation.md`

## Test Objective

Test whether the GP-006 transformation split improves analysis of downstream concepts without introducing unnecessary complexity.

The split under test is:

```text
Transformation Rule ≠ Transformation Instance ≠ Transformation Execution ≠ Transformation Representation
```

## Downstream Concepts Tested

- Transition Signature
- Reasoning State
- Reasoning Calculus
- FARA transition architecture

This test does not revise canonical definitions.

---

# Test 1 — Transition Signature

Current repository definition:

> A transition signature is the explicit description of the transformation between two reasoning states.

## Hidden Collapse

This definition collapses:

- the transformation itself;
- the description of the transformation;
- the source and target states;
- the representation of the transition;
- the rule or process that produced the transition.

## Split Application

A transition signature is not a transformation.

It is a transformation representation.

More precisely, it appears to be:

> an explicit representation of a transformation instance or transformation type between specified reasoning states.

## Result

The split improves precision.

It prevents the project from confusing a transition with its description.

## Revision Pressure

Future definitions should distinguish:

```text
transition instance
transition rule
transition execution
transition signature
```

---

# Test 2 — Reasoning State

Current repository definition:

> A reasoning state is the complete explicit representation of an investigation at a particular stage of reasoning.

## Hidden Collapse

This definition collapses:

- state;
- representation of state;
- investigation stage;
- reasoning process;
- completeness relative to scope.

## Split Application

A reasoning state should not be identical to its explicit representation.

A representation may encode a reasoning state, but the state and the encoding are distinct.

Two different representations may represent the same reasoning state.

## Result

The transformation split exposes a deeper state/representation collapse.

This confirms GP-005's result:

```text
State ≠ Representation of State
```

## Revision Pressure

Future definitions should distinguish:

```text
reasoning configuration
reasoning state
reasoning state representation
reasoning stage
```

---

# Test 3 — Reasoning Calculus

Current repository definition:

> A reasoning calculus is a collection of rules governing admissible reasoning transitions.

## Hidden Collapse

This definition is stronger than the previous two because it already treats calculus as rule-governance rather than execution.

However, it still depends on:

- rule;
- admissibility;
- transition;
- reasoning.

## Split Application

A reasoning calculus belongs to the transformation-rule layer, not the transformation-execution layer.

It specifies which transition instances are permitted, licensed, or generated under a given system.

It does not itself execute a transition.

## Result

The split improves precision.

It separates:

```text
calculus as rule set
transition as instance
execution as occurrence
signature as representation
```

## Revision Pressure

Future definitions should make clear that a reasoning calculus governs transformations but is not itself a transformation execution.

---

# Test 4 — FARA Transition Architecture

## Current Risk

FARA depends heavily on transitions, admissibility, candidate movement, and resolution.

If transformation remains collapsed, FARA risks treating rule, execution, representation, and evaluation as one object.

## Split Application

FARA should eventually distinguish:

- admissibility criteria;
- transition rules;
- transition instances;
- transition executions;
- transition signatures;
- evaluation of transition validity;
- decision procedures using evaluated transitions.

## Result

The split exposes likely downstream cleanup work in FARA.

It does not prove FARA wrong.

It shows FARA requires typed transition artifacts before its architecture can be fully grounded.

---

# Consolidated Result

The GP-006 transformation split survived its first downstream test.

It improved precision across all tested concepts:

- Transition Signature becomes a representation of a transition, not the transition itself.
- Reasoning State requires separation from representation.
- Reasoning Calculus becomes a rule-governance artifact, not an execution artifact.
- FARA requires typed transition artifacts to avoid conflating rules, executions, representations, and evaluations.

## Current Status of Transformation

`Transformation` should remain ungrounded until the following are investigated:

- transformation type;
- transformation instance;
- transformation execution;
- transformation representation;
- transformation rule;
- transition;
- admissibility.

## Methodology Result

The decomposition is useful.

It exposed real downstream conflations without requiring speculative architecture expansion.

This provides evidence that Phase II grounding can improve repository precision by testing concept splits against existing artifacts.
