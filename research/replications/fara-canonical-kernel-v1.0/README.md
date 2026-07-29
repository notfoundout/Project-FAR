# FARA Canonical-Kernel Clean-Room Replication

Status: **Research**

Replication: `FARA-CANONICAL-KERNEL-REPLICATION-001`

## Decision

**replicated**

The clean-room Node.js implementation reproduced the source campaign's candidate classifications and failed-gate sets across three neutral fixture scenarios. Agreement was computed only after isolated execution.

## Independence achieved

- different implementation language from the source Python kernel;
- no source-kernel import or source-proof access during execution;
- isolated temporary-directory execution;
- fresh output exactly equals the committed raw result;
- Git ancestry proves fixture commit `10e28b1827834430d4b4e08e447ab4b219361c46` precedes implementation commit `d6bd162811cda81cb697687e690bf25e73a7ad54`;
- the frozen fixture bytes remain unchanged and the implementation was absent at the freeze commit.

## Candidate agreement

| Candidate | Classification | Failed gates |
|---|---|---|
| `many-sorted-extensional-relational` | `noncanonical` | `identity_bearing_occurrences` |
| `typed-hypergraph` | `admissible-derived-view` | `encoding_neutrality` |
| `algebraic-state-transition` | `admissible-derived-view` | `architecture_operation_separation, calculus_independence, encoding_neutrality, explicit_provenance_and_order, identity_bearing_occurrences, interpretation_separation, representation_object_separation` |
| `identity-bearing-many-sorted-relational` | `provisional-canonical-candidate` | `none` |

## Merge requirement

Merge commit required; squash or rebase would destroy the reachable staged-history evidence.

## Remaining boundary

External investigator independence is **not established**. Acceptance and Promotion require a separate adjudication PR. No canonical FARA authority changes here.

## Validation errors

None.

## Nonclaims

- external investigator independence
- accepted canonical repository foundation
- global uniqueness
- universal representation
- primitive necessity
- global minimality
- completeness
- nonfinite continuous semantics
- live-oracle semantics
- embodied environment semantics
