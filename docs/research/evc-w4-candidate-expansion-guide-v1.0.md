# EVC-W4 Candidate Expansion Guide v1.0

Status: frozen, unexecuted, and unreleased.

This workstream tests whether a materially new architecture changes the bounded FARA/LTS-PROV frontier. It is not a search for a cosmetic third notation and it does not presume that the existing frontier is correct.

A proposal must declare its primitives, operations, state and transition commitments, semantic interfaces, dependencies, history and revision machinery, admissibility conditions, provenance, and conceptual source before benchmark execution. Renamings, regroupings, low-cost commitment-equivalent encodings, and uncharged imports of FARA or LTS-PROV are not materially new.

Every admitted candidate receives the same preservation contract, negative controls, componentwise cost preorder, commitment-equivalence analysis, invariance transformations, ablation tests, and frontier computation. All helpers, adapters, decoders, bridges, hidden state, canonicalizers, and derived machinery are charged. No scalar score or preferred-vocabulary tie breaker is permitted.

Substantive repair after freeze creates a new candidate version. The original failure or limitation remains in the record. Failure to find a successful candidate is evidence only about this bounded search, not global exhaustiveness, universal structure, or global minimality.

Possible outcomes are frontier unchanged, a new equivalent minimum, a new incomparable minimum, a new dominant candidate, no successful new candidate, or unresolved. Formal success does not establish actual-process correspondence.
