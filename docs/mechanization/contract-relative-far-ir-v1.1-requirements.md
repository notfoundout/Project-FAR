# Contract-Relative FAR IR v1.1 Requirements

Status: **Provisional implementation specification**

Governing theory: [Project FAR Core Theory v1.0](../../theory/theorems/Project-FAR-Theory-Closure-v1.0.md)

This specification defines the minimum successor requirements needed for a machine-readable FAR artifact to support contract-relative adequacy claims. It does not change the frozen \`far-ir/1.0\` format and does not claim that an implementation exists.

## Compatibility boundary

\`far-ir/1.0\` remains a valid storage and graph-conformance format. It records investigations, representations, interpretations, claims, evidence, operations, steps, dependencies, and proofs. It does **not** natively require a complete comparison contract, behavior map, decoder, collision witness, observational quotient, or cost order. A conforming v1.0 document therefore cannot by conformance alone certify \`FAR-CORE-001\` or \`FAR-CORE-002\`.

A v1.1 implementation must use a new format identifier and explicit migration. It must not silently reinterpret v1.0 documents.

## Required contract object

A contract record must contain:

- stable contract and version identifiers;
- a declared case domain or case-set reference;
- tests, contexts, continuations, or interventions;
- typed outcome definitions;
- observation semantics or a reference to an executable/declared observation relation;
- calculus, semantics, query mode, and execution-choice parameters when consequence-affecting;
- admitted mappings, transformations, equivalences, or morphisms;
- target class, comparison language, interpretation profile, and interface frame for cross-system claims;
- a metric, loss, tolerance, or cost preorder for approximate or implementation-minimal claims;
- provenance, evidence cutoff, scope, and nonclaims.

## Typed outcomes

The schema must permit distinct values for determinate absence, falsity, inapplicability, failure, unresolved, and epistemic Unknown whenever the contract distinguishes them. It must not impose one universal status vocabulary.

## Representation assessment

Each assessed representation must record:

- the mapping \(\rho\) or a reproducible reference to it;
- the represented image;
- the declared behavior \(\beta_C\) or a reproducible reference;
- a decoder \(d\), a collision witness, or \`OPEN\`;
- the exact verdict and its scope;
- all analyst-supplied tags, interpreters, sidecars, or hidden machinery;
- preservation and loss findings.

A \`PROVED\` exact-sufficiency verdict requires evidence that \(\beta_C=d\circ\rho\). A \`REFUTED\` verdict requires two in-scope cases with the same representation and different declared behavior. Absence of either certificate is \`OPEN\`.

## Quotient and minimality assessment

A quotient record must identify the observational equivalence relation, quotient classes or a reproducible characterization, decoder, and proof/assurance level. “Minimal” without an objective is invalid. Information minimality, cardinality, runtime, storage, cognitive, and explanatory cost must remain separate dimensions.

## Materialized views

Ω may be serialized as a classification/provenance view. The record must identify the calculus output from which it was materialized. Ω must not be treated as the cause of a classification or consequence.

## Terminal report

The format must support \`PROVED\`, \`REFUTED\`, \`OPEN\`, \`BLOCKED\`, \`UNDERDETERMINED\`, \`NOT_APPLICABLE\`, and \`HISTORICAL_SUPERSEDED\`, plus scope, premises, profile, frame, decoder, loss/cost order, evidence, provenance, falsifier, and unresolved boundaries.

## Conformance obligations

A future implementation requires:

1. a versioned JSON Schema;
2. valid and invalid fixtures for every required field;
3. positive factorization and negative collision fixtures;
4. determinate-absence/Unknown separation fixtures;
5. Ω-derived-view fixtures;
6. deterministic normalization and serialization;
7. migration tests proving v1.0 is not silently reinterpreted;
8. explicit nonclaims that schema conformance is not mathematical proof.

Until those artifacts exist, \`PCA-W3-CONTRACT-SCHEMA\` remains open.
