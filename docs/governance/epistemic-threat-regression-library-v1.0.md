# Epistemic threat regression library v1.0

Status: **Permanent active regression controls**

Machine registry:
[`epistemic-threats-v1.0.json`](../../research/registry/epistemic-threats-v1.0.json).

The registry preserves known reasoning failures as named negative controls. It is not a source
of new theory and does not make an automated linter an epistemic authority. Each entry binds a
failure mode to the protected boundary, a detection mechanism, a concrete mutation, and the
expected failure.

Executable controls cover schema/status separation, immutable campaign hashes, staged path
denial, finite-contract collisions, prohibited opportunity promotion, exact-scope alignment,
and harness failure/replay behavior. Some semantic threats, such as whether a domain's
preference orientation is independently justified, remain human-governed checks; automation
can require the field and provenance but cannot supply the judgment.

Removing a threat requires a versioned governance decision showing that the protected boundary
was superseded. Passing the controls is repository consistency evidence, not proof that every
future reasoning error has been excluded.
