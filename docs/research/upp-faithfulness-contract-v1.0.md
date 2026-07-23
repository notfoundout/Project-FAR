# UPP Faithfulness Contract v1.0

## Status

Frozen output of `UPP-W3-CONTRACT`. This document defines `P*`; it does not prove that RCCD or any other kernel is necessary.

## Decision rule

A representation passes only when every registered clause passes with positive evidence. Any failed clause yields Fail. When no clause fails but at least one remains unresolved, the aggregate result is Unknown. Unknown is not Partial and cannot be promoted by absence of a counterexample.

## Clauses

1. Structural fidelity preserves registered entities, relations, state variables, and admissibility distinctions.
2. Semantic fidelity preserves registered meanings and commitment contents under the later-frozen semantic equivalence relation.
3. Operational fidelity preserves answers about permitted, forbidden, and realized changes.
4. Dependency fidelity preserves support, defeat, and revision-relevant dependence questions.
5. Information fidelity prevents omission and fabrication across the registered fact inventory.
6. Historical fidelity preserves provenance and path-sensitive identity questions.
7. Query totality requires an answer or explicit failure for every registered query.
8. Error/Unknown separation distinguishes falsehood, failed access, unresolved evidence, and out-of-domain requests.

## Independence controls

The clauses are stated without the target conclusion's vocabulary. C* membership does not imply a pass. A pass does not identify a kernel. A failure does not identify which machinery is absent. Behavioral equivalence alone does not satisfy semantic fidelity. Each clause has a registered witness showing how it can fail while neighboring clauses remain satisfiable.

## Assumptions

The contract exposes definitional, logical, computational, normative, empirical, and methodological assumptions separately. The empirical assumption concerns whether a concrete artifact supplies adequate evidence; this definition does not settle that question.

## Nonclaims

This workstream does not define E*, machinery closure, or representation equivalence. It does not establish necessity, sufficiency, irreducibility, maximality, actual-process correspondence, or unrestricted universality.
