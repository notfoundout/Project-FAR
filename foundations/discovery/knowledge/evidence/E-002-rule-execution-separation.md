# E-002 — Rule/Execution Separation Evidence

## Status

Pilot Evidence Object

## Evidence Statement

Transformation analysis and downstream testing show that rules governing transformations are distinct from the execution or occurrence of transformations.

## Produced By

- GP-006 — Transformation Grounding Investigation
- GP-006A — Transformation Split Downstream Test

## Supports

- C-002 — Rule Is Distinct from Execution

## Evidence Type

Grounding investigation plus downstream test.

## Strength

Moderate.

## Supporting Observations

- A rule can specify permitted transformations without any transformation occurring.
- A process can occur without an explicitly stated rule.
- A mathematical mapping may exist without execution.
- Reasoning calculus governs transition rules but is not itself transition execution.

## Limitations

The split has not yet been fully tested against FARA and FARO canonical artifacts.

## Open Questions

- Are rule-governed transformations a subclass of transformation?
- Is transformation reducible to relation plus ordered configurations?
