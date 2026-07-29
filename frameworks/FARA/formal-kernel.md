# FARA Formal Kernel v1.0

Status: **Accepted**

Canonical claim: `FARA-FORMAL-KERNEL-001`

Promotion record: `docs/governance/fara-formal-kernel-promotion-v1.0.md`

## Scope

This document defines FARA's canonical formal kernel for **finite, explicit, auditable representational architectures in Project FAR v1.0**.

It does not claim to be the unique or universally correct foundation of reasoning. Its authority is limited to the stated scope and the accepted evidence record.

## Kernel kind

The canonical kernel is an **identity-bearing many-sorted relational structure**.

It is many-sorted because FARA's mandatory architectural categories remain explicitly separated. It is relational because architecture is represented through typed relations rather than a fixed operation algebra. It is identity-bearing because distinct relation occurrences and transformation executions must remain distinguishable even when their extensional participants coincide.

## Formal carriers

The kernel contains the following disjoint carriers:

- `Object`
- `Representation`
- `Meaning`
- `Interpretation`
- `ReasoningCalculus`
- `Rule`
- `State`
- `Event`
- `Investigation`
- `Objective`
- `Condition`
- `RelationType`
- `RelationOccurrence`
- `Role`
- `Provenance`

These are formal carrier names. Their canonical conceptual correspondences are:

| Formal carrier | FARA correspondence |
|---|---|
| `Meaning` | Semantic Content |
| `Rule` | Transformation Rule or another explicitly declared rule kind |
| `State` | Reasoning State within the represented investigation |
| `Event` | Transformation Execution or another explicitly declared execution event |
| `RelationType` | an explicitly specified relation kind |
| `RelationOccurrence` | an identity-bearing occurrence of a relation |
| `Role` | an explicit participant position within a relation occurrence |
| `Provenance` | an explicit source or derivational record attached to an event |

The formal carrier names do not reclassify FARA's seven candidate primitives.

## Relation signature

The canonical relation signature is:

| Relation | Signature |
|---|---|
| `denotes` | `Representation × Object` |
| `assigns` | `Interpretation × Representation × Meaning` |
| `contains_rule` | `ReasoningCalculus × Rule` |
| `applies` | `Event × Rule` |
| `input_state` | `Event × State` |
| `output_state` | `Event × State` |
| `occurs_in` | `Event × Investigation` |
| `uses_calculus` | `Investigation × ReasoningCalculus` |
| `objective_of` | `Investigation × Objective` |
| `condition_of` | `Investigation × Condition` |
| `instance_of` | `RelationOccurrence × RelationType` |
| `participant` | `RelationOccurrence × Role × Object` |
| `precedes` | `Event × Event` |
| `provenance_of` | `Event × Provenance` |
| `represents_event` | `Representation × Event` |

## Admission constraints

A model is admitted only when all of the following hold:

1. Every carrier member has one identity and belongs to exactly one carrier.
2. Every relation tuple has the declared arity and types.
3. Duplicate extensional facts are rejected within a relation.
4. Every `RelationOccurrence` has exactly one `RelationType`.
5. Every `RelationOccurrence` has at least one participant.
6. Every `Event` has exactly one applied `Rule`.
7. Every `Event` has exactly one input `State`.
8. Every `Event` has exactly one output `State`.
9. Every `Event` occurs in exactly one `Investigation`.
10. Every `Event` has at least one explicit `Provenance` record.
11. `precedes` is acyclic.

These constraints preserve FARA's required category separations and make reasoning traces auditable without treating operation composition as primitive architecture.

## Architectural gates

The kernel is canonical within scope because it satisfies the eight accepted gates:

- representation/object separation;
- rule/execution/result separation;
- interpretation separation;
- calculus independence;
- architecture/operation separation;
- identity-bearing occurrences;
- explicit provenance and order;
- encoding neutrality.

## Derived concepts and views

The kernel licenses the following scoped derivations:

- a Property may be represented as a unary relation occurrence;
- Semantic Content is represented by an interpretation assignment;
- a Transition Signature is a representation of an Event;
- a Reasoning Trace is an ordered collection of Events under `precedes`;
- typed-hypergraph form is an optional derived incidence view;
- algebraic/state-transition form is an optional derived operational/backend view when all omitted commitments are preserved explicitly.

These are formal representation choices. They do not, by themselves, prove global conceptual reductions or primitive minimality.

## Noncanonical projections

A pure extensional relational projection is not the canonical kernel because extensionally identical parallel occurrences can collapse.

Typed-hypergraph and algebraic/state-transition representations are not canonical foundations because they make graph or operation scaffolding native. They remain admissible derived views when explicit translations preserve the registered commitments.

## Evidence and provenance

The accepted kernel is supported by:

- source campaign `FARA-CANONICAL-KERNEL-001`, merge commit `775c24b26a30339a3fc0117e1faf4febece0a33c`;
- source specification Git blob `49e10b34ac9920fed85a5c8be5e5200f59aedfbe`;
- source proof Git blob `36b046f0efc32fa9464cd0943aef30af398c63bf`;
- replication `FARA-CANONICAL-KERNEL-REPLICATION-001`, merge commit `5932e6b2111c6d7da8b1c9a443474b395f02880e`;
- replication adjudication Git blob `d4737e680ece1510c23eb8571470e0f175d7f663`;
- Acceptance record Git blob `4958a71434f9c5572aba6edc1e51572736e24b3a`;
- Promotion record Git blob `490f1749ed462c29c7ec1c8af7eaa88af9b672e5`.

The underlying Research artifacts remain immutable Research evidence. Promotion does not relabel or rewrite them.

## Primitive and theory boundary

The candidate primitive registry remains:

- Object
- Property
- Relation
- Representation
- Interpretation
- Investigation
- Reasoning Calculus

This kernel selection does not establish their global independence, necessity, minimality, or irreducibility.

## Nonclaims

This document does not establish:

- global uniqueness;
- universality outside the stated scope;
- global primitive necessity or minimality;
- completeness;
- full-signature or unbounded adequacy;
- nonfinite continuous semantics;
- live-oracle semantics;
- embodied or environment-inclusive semantics;
- external-investigator independence;
- superiority under every possible representation-cost criterion.

## Change control

Any revision to this kernel requires the Project FAR discovery lifecycle, FARM change control, preservation of the immutable source and replication evidence, and explicit impact analysis across FARA, FAR, and FARO.