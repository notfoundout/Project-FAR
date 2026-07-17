# CRE-004 Hidden Reintroduction Rules

Hidden reintroduction occurs when a candidate advertised as lacking a registered function preserves the distinction by adding machinery that performs that same function under another name or representation.

## Functional test

The test is behavioral and commitment-based, not lexical. A mechanism counts as reintroduction when it performs one or more of these functions:

- stores explicit reasoning objects;
- organizes those objects or their relations;
- assigns meaning or denotation;
- defines the objective or success condition;
- determines permitted inference or transition steps.

A renamed field, edge type, state variable, annotation, constraint, procedure, or external convention can therefore count as reintroduction.

## Evaluator role

Evaluators identify visible mechanisms using plain-language labels. They do not decide the final hidden-reintroduction status.

When `other` is selected, the follow-up asks whether the mechanism performs one of the five functions. The scorer derives:

- a listed function: `true`;
- `none`: `false`;
- `cannot_determine`: `unknown`.

## Limits

Reintroduction is not inferred merely because a translation is complex, unfamiliar, or successful. It requires an identified functional equivalence. Disagreement or insufficient visibility remains `unknown`; it must not be forced to `true` or `false`.