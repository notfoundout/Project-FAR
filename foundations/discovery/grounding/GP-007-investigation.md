# GP-007 — Investigation Grounding Investigation

## Status

Active Grounding Investigation

## Phase

Phase II — Repository Grounding Program

## Concept Under Investigation

Investigation

## Current Repository Definition

`theory/definitions/definitions.md` currently defines investigation as:

> An investigation specifies the object of analysis together with the criteria by which reasoning is organized.

## Investigation Objective

Determine whether `Investigation` is primitive, reducible, split into multiple concepts, or retained as a derived methodology concept within Project FAR.

This investigation does not revise the canonical definition directly.

## Initial Finding

The current definition is operationally useful but not grounded.

It depends on at least:

```text
Investigation
  ↓
object of analysis
criteria
reasoning
organization
```

Several of these dependencies have already shown instability during Phase I and early Phase II.

In particular, the phrase `object of analysis` is likely too narrow because investigations may target relations, questions, dependencies, contradictions, methods, or artifact states rather than objects alone.

## Hidden Assumptions

The current definition assumes:

- every investigation has an object;
- the target is an object rather than a relation or question;
- criteria are present from the beginning;
- reasoning is already defined;
- investigation organizes reasoning rather than discovery, testing, reduction, or evaluation;
- investigation is singular rather than a network of modes;
- investigation and governance are separate, but the definition does not state that separation.

None of these assumptions is fully grounded yet.

## Attack 1 — Object of Analysis Is Too Narrow

Some investigations ask:

- whether X depends on Y;
- whether a definition is circular;
- whether a methodology rule improves artifact analysis;
- whether a relation is reducible;
- whether two concepts are equivalent;
- whether a contradiction exists.

These are not simply investigations of an object.

They are investigations of a relation, question, hypothesis, or dependency.

### Result

`object of analysis` should be weakened to `target of inquiry` or expanded into typed targets.

Candidate target types include:

- object;
- relation;
- question;
- hypothesis;
- definition;
- theorem;
- dependency;
- contradiction;
- methodology rule;
- artifact state.

## Attack 2 — Criteria May Not Exist at the Start

The current definition says an investigation specifies criteria.

But discovery investigations may begin precisely because criteria are missing or contested.

Example:

FI-000 asks what the correct foundational research question is.

The criteria for evaluating candidate questions are partly discovered during the investigation.

### Result

Criteria may be:

- initial;
- discovered;
- revised;
- absent but sought;
- inherited from methodology.

Therefore criteria should not be treated as a fixed defining component of all investigations.

## Attack 3 — Investigation Is Not Identical to Reasoning

The current definition organizes investigation around reasoning.

However, an investigation can include:

- observation;
- decomposition;
- reduction;
- counterexample search;
- artifact audit;
- dependency mapping;
- compression;
- governance preparation.

These are not all reasoning in the same sense unless `reasoning` is broadened so far that it loses precision.

### Result

Investigation should not be defined by reasoning until reasoning itself is grounded.

## Attack 4 — Investigation Has Modes

Prior Phase I work identified that investigations move among modes:

- discovery;
- clarification;
- reduction;
- derivation;
- refutation;
- comparison;
- integration;
- audit;
- compression.

These modes are not strictly sequential.

An investigation is better modeled as a structured inquiry process that can transition between modes in response to findings.

### Result

Investigation is probably not a linear object but a managed inquiry structure.

## Attack 5 — Investigation vs. Repository Artifact

An investigation as an intellectual process is not identical to the repository artifact recording it.

For example:

- GP-006 is an investigation;
- `GP-006-transformation.md` is a repository artifact representing that investigation.

These must remain separate.

### Result

Project FAR must distinguish:

```text
investigation process
investigation record
investigation artifact
investigation state
```

## Candidate Decomposition

`Investigation` should be decomposed into at least:

```text
Investigation Question
  the question or problem motivating inquiry

Investigation Target
  the object, relation, claim, artifact, or structure under inquiry

Investigation Method
  the procedures or methodology applied

Investigation State
  the current research state of the inquiry

Investigation Record
  the repository artifact documenting the inquiry

Investigation Outcome
  the result, non-result, reduction, rejection, split, or residual candidate produced
```

These are decomposition candidates, not canonical categories.

## Candidate Weak Characterization

An investigation is currently best characterized as:

> A structured inquiry process directed at one or more explicit questions or targets, using stated or discoverable methods to produce traceable outcomes under a specified scope.

This remains provisional.

It avoids assuming that the target must be an object, that criteria are fixed at the start, or that reasoning is already grounded.

## Current Dependency Hypothesis

```text
Question / Problem
  ↓
Investigation Target
  ↓
Investigation Method
  ↓
Investigation Process
  ↓
Investigation Record
  ↓
Investigation Outcome
```

This is not necessarily a strict sequence.

The actual structure may be a network with feedback loops.

## Open Questions

1. Can an investigation exist without an explicit question?
2. Can an investigation begin without criteria?
3. Is an investigation defined by its target, method, question, or outcome?
4. Are investigation modes primitive, derived, or operational conveniences?
5. What distinguishes investigation from reasoning?
6. What distinguishes investigation from evaluation?
7. What distinguishes investigation from governance?
8. Is investigation a methodology concept rather than an ontology concept?
9. What makes an investigation complete, provisionally stable, or reopened?

## Interim Result

`Investigation` is not currently grounded as primitive.

The canonical definition is too narrow and too dependent on ungrounded reasoning concepts.

The strongest current result is a split:

```text
Investigation Process ≠ Investigation Record ≠ Investigation Target ≠ Investigation Outcome
```

This split should be tested against existing FI, GP, AA, CP, and DGA artifacts before any canonical rewrite.

## Methodology Audit

### Did the investigation expose hidden assumptions?

Yes.

It exposed hidden assumptions about object targets, fixed criteria, reasoning-dependence, and artifact/process collapse.

### Did it reduce the concept?

Partially.

Investigation appears reducible or decomposable into question, target, method, process, record, and outcome.

### Did it identify collapsed dimensions?

Yes.

The current definition collapses process, record, target, criteria, and reasoning organization.

### Did it justify a repository revision?

Not yet.

The immediate action is to preserve the grounding investigation and test the decomposition against existing discovery artifacts.
