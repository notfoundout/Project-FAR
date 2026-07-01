# Grounding Result 2 — Necessity of FAR

## Status

Research

## Question

Given FARA-level representational structure, is a separate investigation methodology required?

## Objective

Ground FAR by testing whether explicit reasoning can be conducted, evaluated, audited, and resolved using FARA alone.

## Result

FARA supplies the representational architecture required to make reasoning objects explicit.

FARA does not by itself determine the order, procedure, or discipline by which an investigation is conducted.

A distinct methodology is required to govern the execution of reasoning over FARA-level structure.

That methodology is FAR.

## Distinction Between FARA and FAR

FARA answers:

> What must exist for reasoning to be explicitly represented?

FAR answers:

> What must be done to conduct an investigation over explicit reasoning representations?

Therefore, FARA provides the objects and structure, while FAR provides the procedure.

## Test Case

Assume a FARA-level system contains:

- an investigation;
- representations;
- a representational structure;
- interpretations;
- reasoning states;
- transitions;
- candidates;
- admissibility;
- resolution.

Now attempt to conduct the investigation:

> Determine whether claim C should be accepted, rejected, revised, or left unresolved.

The representational architecture allows the required objects to be represented.

However, it does not by itself specify:

- how the investigation begins;
- how representations are gathered;
- when interpretations are assigned;
- when a reasoning calculus is selected;
- how reasoning states are initialized;
- how transitions are applied;
- how candidates are generated;
- how admissibility is evaluated;
- when resolution occurs;
- how the final reasoning path is audited.

Those requirements are procedural rather than merely representational.

## Elimination Tests

### 1. Remove Investigation Procedure

Without a procedure, the system has explicit objects but no ordered method for using them.

Result:

The investigation can be represented but not disciplined.

A procedure is required.

### 2. Remove Stage Ordering

Without stage ordering, the investigation cannot distinguish preparation from evaluation, evaluation from resolution, or resolution from audit.

Result:

Reasoning steps may occur, but their procedural role is ambiguous.

Stage ordering is required.

### 3. Remove Methodological Constraints

Without methodological constraints, hidden assumptions, premature resolutions, unsupported transitions, and unrecorded candidate exclusions may enter the investigation.

Result:

The reasoning process cannot be audited as a controlled investigation.

Methodological constraints are required.

### 4. Remove Resolution Procedure

Without a resolution procedure, admissible candidates may exist without any disciplined account of how the investigation terminates.

Result:

The investigation cannot complete in an auditable way.

Resolution procedure is required.

### 5. Remove Audit Procedure

Without audit procedure, later reviewers cannot reconstruct how the investigation moved from initial representations to final resolution.

Result:

The investigation may produce an answer, but the answer is not fully inspectable or reproducible.

Audit procedure is required.

## Conclusion

FAR is justified as the methodology required to conduct investigations over FARA-level representational architecture.

Without FAR, FARA can represent the objects of reasoning, but it does not provide a disciplined process for beginning, developing, evaluating, resolving, and auditing an investigation.

This result does not prove that the current FAR workflow is complete or minimal.

It establishes only that a procedural layer distinct from FARA is necessary.

## Remaining Work

1. Determine whether the current FAR workflow stages are complete.
2. Determine whether any FAR stage can be eliminated or merged.
3. Formalize the boundary between FARA structure and FAR procedure.
4. Determine how FAR selects or records reasoning calculi.
5. Determine how FAR handles disputes over resolution-rule selection.
