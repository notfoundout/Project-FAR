# Identity-Bearing FARA Relational Kernel Research Campaign

Status: **Research**

Campaign: `FARA-CANONICAL-KERNEL-001`

## Objective

Test whether an identity-bearing many-sorted relational kernel satisfies the existing Project FAR v1.0 architectural constraints more directly than the three frozen historical foundation candidates.

This artifact records Execution, Observation, and a provisional Discovery. It does not record independent Replication, Acceptance, Promotion, or canonical repository change.

## Lifecycle record

| Stage | Status | Evidence |
|---|---|---|
| Question | recorded | `UQ-T11` and the unresolved selection obligation in the historical core formalization |
| Execution | complete | executable kernel, translations, counterexamples, checker, proof object, and mutation tests in this campaign |
| Observation | complete | proof-derived gate matrix and reconstruction outcomes |
| Discovery | provisional Research finding | one candidate passes every frozen gate in the registered fixtures |
| Replication | pending | requires an independent implementation and neutral fixtures |
| Acceptance | pending | prohibited until replication is recorded and reviewed |
| Promotion | pending | no canonical FARA artifact is changed by this campaign |
| Repository change | Research artifacts only | implementation and evidence are isolated under Research status |

## Frozen architectural gates

The campaign operationalizes eight existing FARA requirements:

1. representation/object separation;
2. rule/execution/result separation;
3. interpretation separation;
4. calculus independence;
5. architecture/operation separation;
6. identity-bearing occurrences;
7. explicit provenance and order;
8. encoding neutrality.

The specification does not assign gate truth values. `kernel.py` derives every result from executable predicates, model validation, round trips, mutation rejection, schema inspection under the frozen contract, and observed reconstruction loss.

## Event and occurrence contract

Every admitted Event must possess exactly one Rule, input State, output State, and Investigation reference, plus at least one explicit provenance record. Event order must be acyclic. Every RelationOccurrence must possess exactly one RelationType and at least one participant.

These constraints prevent dictionary overwrite from silently changing algebraic round trips and prevent models without provenance from passing the proposed kernel's own admission contract.

## Observations

- The identity-bearing many-sorted relational candidate passes all eight gates in the registered executable fixtures.
- Pure extensional relational projection preserves the direct FARA schema but collapses two parallel relation occurrences into one extensional fact.
- The typed-hypergraph view performs an exact round trip but requires Node/Port/Hyperedge scaffolding and therefore fails the frozen encoding-neutrality gate.
- The bare algebraic/state-transition view preserves event/operation/state fields but omits representation/object separation, interpretation, provenance, relation-occurrence identity, and architecture/operation separation. An explicit sidecar enables exact reconstruction as a derived backend.

## Provisional discovery

Within the registered finite explicit fixtures and frozen gates, the identity-bearing many-sorted relational kernel is the sole provisional canonical candidate.

This is not Accepted theory. The next lifecycle step is independent replication. Until that succeeds and a later Acceptance/Promotion record is merged, the current canonical FARA documents, primitive registry, ontology, and `UQ-T11` status remain unchanged.

## Historical compatibility

`FARA-FOUNDATION-COMP-001` remains valid Research evidence about its three frozen implementations. Its terminal result—multiple foundations remain Pareto-incomparable—is not rewritten. This campaign evaluates a repaired fourth candidate under mandatory gates rather than reranking the historical three through altered Pareto weights.

The expanded bounded campaign is also pinned by immutable Git blob identities and remains unchanged.

## Nonclaims

This campaign does not establish:

- an Accepted canonical repository foundation;
- global uniqueness;
- universal representation;
- primitive necessity or minimality;
- completeness;
- nonfinite continuous, live-oracle, or embodied semantics;
- independent replication.
