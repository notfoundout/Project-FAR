# IKD-W3 Common-Factor Search v1.0

## Status

Executed prospectively by PR #263 under `POST-USD-IKD-001`.

## Question

Do FARA, LTS-PROV, and COALG-DYN share a nontrivial reasoning-relevant commitment after labels, implementation details, and architecture-specific ontology are removed?

## Result

The bounded search supports one candidate-neutral factor: **RCCD-001 — recoverable constrained commitment dynamics**.

RCCD-001 requires:

1. a distinguishable configuration with recoverable commitment content;
2. declared admissibility conditions constraining evolution;
3. preservation or explicit revision of grounds and dependencies;
4. queryable supersession and historical identity;
5. one uniform bounded-query recovery interface without source-specific, unrestricted, or future-information oracles.

The factor is operational rather than lexical. FARA realizes it through typed commitments, interpretation, calculus, and provenance/history. LTS-PROV realizes it through commitment-bearing states, constrained transitions, provenance, and supersession events. COALG-DYN realizes it through observable commitment behavior, a coalgebraic evolution map, and charged dependency/history observations.

## Rejected weaker factors

Generic graph structure, bare state transition, provenance alone, and unrestricted interpretation were rejected. Each either omits a registered preservation obligation or can encode arbitrary systems without imposing a nontrivial reasoning constraint.

## Claim boundary

This result supports one common-factor candidate only on the frozen bounded scope. It does not establish uniqueness, global necessity, global minimality, cross-feature compositional closure, actual-process correspondence, or universal structure.

## Next action

PR #264 must directly test RCCD-001 on simultaneous cross-feature conjunctions. Separate featurewise success is not compositional closure.
