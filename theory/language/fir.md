# FAR Intermediate Representation (FIR)

Status: Provisional

FAR Intermediate Representation (FIR) is the machine-readable layer used by Project FAR tools to inspect explicit reasoning without replacing canonical Markdown theory.

## Representation objects

Representation objects record explicit reasoning items. Minimal fields are `id`, `kind`, `content`, and optionally `statement`.

## Statement objects

Statement objects provide structured semantic anchors using `kind`, `claim`, and optional `subject`, `predicate`, and `scope`. Prose statements remain valid fallback inputs.

## Proof-step objects

Proof-step objects record `id`, `rule`, `inputs`, `statement`, and `justification`. The proof-object checker uses them to validate local availability, rule input patterns, and soft semantic alignment.

## Dependency objects

Dependency objects record source identifiers, derived-concept registry references, and approved contextual sources used by premises and proof steps.

## Transition objects

Transition objects record `id`, `source`, `rule`, `target`, `status`, and `order`. They support derivation ordering and proof-trace output.

## Derivation objects

Derivation objects are ordered transition traces. They expose how a reasoning state changes under declared rules.

## Reasoning-system mappings

Reasoning-system mappings record how an external system maps into FAR primitives:

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

A mapping also records a provisional verdict: `fits FAR`, `extends FAR`, `falsifies FAR`, or `draft`.

## Proof traces

Proof traces are machine-readable outputs containing investigation text, FIR representations, dependency edges, detected cycles, and derivation trees.
