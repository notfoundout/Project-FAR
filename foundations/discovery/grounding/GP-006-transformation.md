# GP-006 — Transformation Grounding Investigation

## Status

Active Grounding Investigation

## Phase

Phase II — Repository Grounding Program

## Concept Under Investigation

Transformation

## Current Repository Definition

`theory/definitions/definitions.md` currently defines transformation as:

> A transformation is a rule or process that maps one state to another.

## Investigation Objective

Determine whether `Transformation` is primitive, reducible, split into multiple concepts, or retained as a derived concept within Project FAR's foundational ontology.

This investigation does not revise the canonical definition directly.

## Initial Finding

The current definition is not foundational.

It depends on at least four ungrounded or partially grounded concepts:

```text
Transformation
  ↓
Rule
Process
Map
State
```

`State` has already been partially reduced in prior grounding work to a particular assignment within a specified structure. Therefore `Transformation` should not be grounded until its relation to state-change, rule-governance, and representation is clarified.

## Hidden Assumptions

The current definition assumes:

- transformation is either a rule or a process;
- rules and processes are equivalent enough to appear in one definition;
- transformation maps states;
- states are the correct operands of transformation;
- every transformation has a source state and target state;
- transformation is directional;
- transformation is representable;
- transformation is distinct from its description;
- transformation is distinct from evaluation of the transformation.

None of these assumptions is accepted yet.

## Attack 1 — Rule and Process Are Not Equivalent

A rule can specify permitted transformations without any transformation occurring.

A process can occur without an explicitly stated rule.

Therefore:

```text
rule ≠ process
```

The definition collapses a specification with an execution.

### Result

Transformation must be separated from:

- transformation rule;
- transformation process;
- transformation instance;
- transformation description.

## Attack 2 — Mapping Is Too Abstract

A mapping can exist as a mathematical object without any execution.

Example:

```text
f: A → B
```

The mapping exists even if no input is actually transformed.

Therefore mapping alone does not capture transformation execution.

### Result

Transformation may require separate handling of:

- transformation type;
- transformation instance;
- transformation execution;
- transformation representation.

## Attack 3 — State-to-State May Be Too Narrow

The definition assumes transformations map one state to another.

Counterexamples to test:

- transformation of a representation without changing the represented state;
- transformation of a relation type;
- transformation of a question into a hypothesis;
- transformation of an investigation state;
- transformation of a proof trace.

Some transformations operate on representations, questions, symbols, or structures, not merely states.

### Result

`state-to-state` is likely a special case, not the general definition.

## Attack 4 — Transformation vs. Representation Change

Two textual representations can change while the represented state remains identical.

Example:

```text
{"a": 1, "b": 2}
{"b": 2, "a": 1}
```

The representation changes.

The represented state may not.

Therefore transformation of representation and transformation of state must remain separate.

### Result

A transformation must specify its target layer:

- ontology transformation;
- representation transformation;
- investigation transformation;
- repository transformation.

## Attack 5 — Transformation vs. Evaluation

A transformation can occur without being evaluated.

An evaluator can evaluate a transformation without executing it.

Therefore:

```text
transformation ≠ evaluation
```

### Result

Transformation belongs primarily to execution or structural change.

Evaluation belongs to a distinct investigation/evaluation layer.

## Candidate Decomposition

The concept `Transformation` should be decomposed into at least:

```text
Transformation Type
  specification of possible transformations

Transformation Instance
  particular transition from one configuration to another

Transformation Rule
  criterion or rule governing permitted transformation instances

Transformation Execution
  occurrence or enactment of a transformation instance

Transformation Representation
  artifact describing or encoding a transformation
```

These are not yet canonical categories.

They are decomposition candidates.

## Candidate Weak Characterization

A transformation is currently best characterized as:

> A relation between configurations in which one configuration is treated as replaced, produced, modified, or succeeded by another under a specified layer and interpretation.

This remains provisional.

It avoids defining transformation as only a rule, only a process, or only a state mapping.

## Current Dependency Hypothesis

```text
Structure
  ↓
Configuration / State
  ↓
Transformation Type
  ↓
Transformation Instance
  ↓
Transformation Execution
```

Representation and evaluation are cross-layer relations, not parts of transformation itself.

## Open Questions

1. Is transformation reducible to relation plus ordered configurations?
2. Is transformation necessarily directional?
3. Can transformation exist without time?
4. Does every transformation require a source and target?
5. Are rule-governed transformations a subclass rather than the general case?
6. Does Project FAR need `Transformation` as a primitive, or only as a derived relation type?
7. What distinguishes transformation from ordinary relation?
8. What layer is transformed: ontology, representation, investigation, or repository?

## Interim Result

`Transformation` is not currently grounded as primitive.

The repository definition is useful but too compressed.

The strongest current result is a split:

```text
Transformation Rule ≠ Transformation Instance ≠ Transformation Execution ≠ Transformation Representation
```

This split should be tested before any canonical rewrite.

## Methodology Audit

### Did the investigation expose hidden assumptions?

Yes.

The current definition hides assumptions about rules, processes, mappings, states, directionality, and execution.

### Did it reduce the concept?

Partially.

Transformation appears reducible or at least decomposable into relation-like structures over configurations, but this is not yet proven.

### Did it identify collapsed dimensions?

Yes.

The definition collapses rule, process, mapping, execution, and representation.

### Did it justify a repository revision?

Not yet.

The correct immediate action is to preserve this investigation and test the decomposition against downstream concepts such as reasoning state, transition signature, reasoning calculus, and FARA.
