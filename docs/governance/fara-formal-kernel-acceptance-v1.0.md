# FARA Formal-Kernel Acceptance v1.0

Status: **Accepted**

Claim: `FARA-FORMAL-KERNEL-001`

Scope: **Project FAR v1.0 finite, explicit, auditable representational architecture**

## Accepted claim

Within the stated scope and the eight registered architectural gates, the identity-bearing many-sorted relational kernel is accepted as the formal foundation that most directly preserves FARA's mandatory architectural distinctions without making graph scaffolding or operational composition primitive.

The Accepted kernel uses typed, occurrence-sensitive identity. Literal identifier spelling is not semantic. Its canonical model-equivalence relation is sort-preserving relational isomorphism: one bijection per carrier sort that preserves and reflects every declared relation. This preserves event and relation-occurrence cardinality, participant roles, provenance, and precedence while permitting consistent identity renaming.

The accepted claim is scoped. It is not a claim that this kernel is the unique or universally correct foundation of reasoning.

## Lifecycle record

| Stage | Status | Evidence |
|---|---|---|
| Question | complete | `UQ-T11`, `OP-10`, and the selection obligation retained by the bounded foundation work |
| Execution | complete | `FARA-CANONICAL-KERNEL-001`, merged as `775c24b26a30339a3fc0117e1faf4febece0a33c` |
| Observation | complete | executable gate matrix, reconstruction results, identity-loss counterexample, and mutation evidence |
| Discovery | complete | identity-bearing many-sorted relational was the sole registered candidate passing all eight gates |
| Replication | complete | `FARA-CANONICAL-KERNEL-REPLICATION-001`, merged as `5932e6b2111c6d7da8b1c9a443474b395f02880e` |
| Acceptance | complete | this record, including explicit identity and equivalence criteria |
| Promotion | pending | requires a separate promotion record |
| Repository change | pending | prohibited until Promotion |

No stage is skipped.

## Acceptance basis

Acceptance is justified because all of the following are established within the registered scope:

1. The candidate's gate results are derived by executable predicates rather than candidate-authored booleans.
2. The candidate preserves representation/object, rule/execution/result, and interpretation separations.
3. It remains independent of a fixed reasoning calculus and separates architecture from operation.
4. It preserves identity-bearing relation occurrences and explicit event provenance/order.
5. Typed-hypergraph translation round-trips exactly but adds universal graph scaffolding.
6. Bare algebraic/state-transition representation omits required nonoperational commitments; exact reconstruction requires an explicit sidecar.
7. Pure extensional relational projection collapses distinct parallel occurrence identities.
8. A clean-room Node.js implementation using three neutral scenarios reproduced every candidate classification and failed-gate set.
9. Git ancestry proves that the neutral fixtures preceded the replication implementation.
10. Source and replication campaigns passed fail-closed regression, mutation, repository-health, unified-validation, Lean-assurance, model-checking, and exact-commit/tree gates.
11. Typed identity follows from the mandatory category separations and occurrence-identity gate: identity tokens cannot cross sorts, and parallel Event or RelationOccurrence identities cannot be merged by extensional equality.
12. Sort-preserving relational isomorphism is the accepted equivalence relation because it permits arbitrary consistent renaming while preserving and reflecting the complete admitted structure. Exact normalized equality is its identity-map special case.

## Identity and equivalence adjudication

| Question | Accepted answer within scope |
|---|---|
| What constitutes identity? | Explicit carrier membership plus distinct identity token; Event and RelationOccurrence identities remain occurrence-sensitive. |
| Does token spelling carry semantic content? | No. Consistent sort-preserving renaming is permitted. |
| May equivalent models merge or split identities? | No. Equivalence requires a bijection per sort. |
| What is the model-equivalence relation? | Sort-preserving relational isomorphism preserving and reflecting every declared relation. |
| Are behavioral or commitment-equivalent projections automatically kernel-equivalent? | No. They require separately declared relations and cannot replace canonical kernel-equivalence. |

## Candidate adjudication

| Candidate | Accepted role |
|---|---|
| identity-bearing many-sorted relational | canonical formal-kernel candidate within the stated scope |
| typed hypergraph | admissible derived representation |
| algebraic/state-transition | admissible derived execution/backend view only with explicit preservation machinery |
| pure extensional many-sorted relational | noncanonical because parallel occurrence identity can collapse |

## Independence boundary

The registered replication requirement was an independent implementation plus neutral fixtures. That requirement is satisfied.

External-investigator independence is not established and is not silently inferred. It remains a limitation and a valid target for later criticism or replication. Its absence limits confidence and generality; it does not negate the recorded implementation-independent replication result.

## Primitive boundary

This Acceptance does not establish that FARA's seven candidate primitives are independent, necessary, minimal, or irreducible. It selects a formal carrier architecture. It does not promote the research campaign's provisional reductions of Property, Investigation, Reasoning Trace, Semantic Content, or Transition Signature into accepted primitive reductions.

## Nonclaims

This Acceptance does not establish:

- global uniqueness;
- universal representation of every reasoning system;
- global primitive necessity or minimality;
- completeness;
- unbounded or full-signature adequacy;
- nonfinite continuous semantics;
- live-oracle semantics;
- environment-inclusive embodied semantics;
- external-investigator independence;
- superiority under every possible comparison criterion.

## Acceptance decision

`FARA-FORMAL-KERNEL-001`—including its scoped carrier architecture, typed occurrence-sensitive identity criteria, and sort-preserving relational-isomorphism equivalence relation—is **Accepted at the stated scope**.

Promotion and canonical repository change require a separate, traceable record.
