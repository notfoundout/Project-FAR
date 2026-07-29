# FARA Canonical-Kernel Clean-Room Replication

Status: **Research**

Replication: `FARA-CANONICAL-KERNEL-REPLICATION-001`

## Decision

**replicated**

The clean-room Node.js implementation reproduced the source campaign's candidate classifications and failed-gate sets across three neutral fixture scenarios. Agreement is computed only after the isolated execution.

## Independence achieved

- different implementation language from the source Python kernel;
- no source-kernel import;
- no source-proof access during execution;
- execution in a temporary directory containing only the protocol, neutral fixtures, and JavaScript implementation;
- neutral fixtures frozen in branch history before the protocol, implementation, and result;
- fresh isolated output must exactly match the committed raw result.

## Candidate agreement

| Candidate | Classification | Failed gates |
|---|---|---|
| `many-sorted-extensional-relational` | `noncanonical` | `identity_bearing_occurrences` |
| `typed-hypergraph` | `admissible-derived-view` | `encoding_neutrality` |
| `algebraic-state-transition` | `admissible-derived-view` | `architecture_operation_separation, calculus_independence, encoding_neutrality, explicit_provenance_and_order, identity_bearing_occurrences, interpretation_separation, representation_object_separation` |
| `identity-bearing-many-sorted-relational` | `provisional-canonical-candidate` | `none` |

## Remaining boundary

External investigator independence is **not established**. This PR completes only the repository's frozen implementation-independent replication criterion. Acceptance and Promotion require a separate adjudication PR. No canonical FARA authority changes here.

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
