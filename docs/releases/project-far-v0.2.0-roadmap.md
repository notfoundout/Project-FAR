# Project FAR v0.2.0 Roadmap

Status: Provisional

The v0.2.0 target is the transition from proof-object shape checking toward semantic proof checking.

Milestone scope:

- define FAR Intermediate Representation (FIR) as the bridge between Markdown theory, YAML proof objects, metadata, parser output, checker input, reasoning-engine data, and future Lean artifacts;
- add minimal machine-readable statement objects for theorems, propositions, lemmas, definitions, and axioms;
- strengthen proof-object checking from structural validation to rule-pattern validation plus initial semantic validation;
- keep exact theorem-prover behavior out of scope until the repository contains sufficiently formal statements.

Validation layers are distinguished as follows:

1. structural validation verifies proof-object shape and local references;
2. rule-pattern validation verifies that declared rules have reliable source kinds and minimum input patterns;
3. semantic validation compares proof-step claims with metadata statement objects and required semantic vocabulary, using warnings where exact matching is not yet reproducible.

## Universal-structure hypothesis testing

v0.2.0 begins testing whether explicit reasoning systems share a universal structure. The new fixture harness maps external systems into FAR primitives, records clean mappings and gaps, and classifies each case as fitting FAR, extending FAR, falsifying FAR, or remaining draft.

A system becomes a falsification candidate only when it is explicit reasoning, cannot be represented by current primitives, cannot be reduced to registered derived concepts, cannot be handled by conservative extension, and requires a genuinely new primitive.
