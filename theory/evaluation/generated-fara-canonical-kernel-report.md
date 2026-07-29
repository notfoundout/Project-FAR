# Generated FARA Canonical Kernel Report

Status: **Accepted for Project FAR v1.0**

Campaign: `FARA-CANONICAL-KERNEL-001`
Kernel: `fara-identity-bearing-many-sorted-relational/1.0`

## Adjudication

| Candidate | Classification | Failed canonical gates |
|---|---|---|
| many-sorted-extensional-relational | noncanonical | identity_bearing_occurrences |
| typed-hypergraph | admissible-derived-view | encoding_neutrality |
| algebraic-state-transition | admissible-derived-view | representation_object_separation, rule_execution_result_separation, interpretation_separation, calculus_independence, architecture_operation_separation, identity_bearing_occurrences, explicit_provenance_and_order |
| identity-bearing-many-sorted-relational | canonical-candidate | none |

## Executable translation evidence

- Typed-hypergraph exact round trip: `True`.
- Algebraic/state-transition exact round trip with explicit sidecar: `True`.
- Algebraic/state-transition standalone completeness: `False`.
- Extensional relation-occurrence identity loss detected: `True`.

## Canonical decision

For Project FAR v1.0, FARA's canonical formal foundation is the identity-bearing many-sorted relational kernel. Typed-hypergraph and algebraic/state-transition forms are admissible derived views when their translations and required sidecars are explicit and commitment-preserving.

## Historical evidence policy

The earlier Pareto comparison remains valid for its three frozen implementations. This decision does not rewrite that result; it applies FARA's mandatory architectural gates to select the Project FAR v1.0 kernel after repairing occurrence identity.

## Nonclaims

- globally unique foundation of reasoning
- universal representation of every reasoning system
- global primitive necessity
- global minimality
- completeness
- coverage of nonfinite continuous semantics
- coverage of live-oracle semantics
- coverage of embodied environment semantics
- independent replication
