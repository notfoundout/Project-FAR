# Evidence, Replication, and Theory Freeze Standard v1.0

## Purpose

This standard fixes the evidential meaning of Project FAR results, distinguishes replication levels, and prevents theory repair after result exposure from being reported as success of the original frozen theory.

## Evidence classes

Every research result must be classified as exactly one primary class:

- **Exploratory** — used to develop theory, discover cases, debug procedures, or refine metrics.
- **Confirmatory** — executed prospectively under a frozen preregistration, theory version, source contract, metrics, and decision rules.
- **Implementation** — establishes software behavior, conformance, determinism, or robustness without independently validating the underlying theory.
- **Replication** — repeats a frozen result under the declared replication layer.
- **Boundary** — identifies limits, pressure points, or scope conditions.
- **Counterexample** — establishes a protected failure within justified scope.
- **Unresolved** — evidence is insufficient, conflicting, or incomparable.

Secondary tags may be added, but the primary class may not be omitted.

## Replication layers

### R1 — Internal rerun

The same implementation and team repeat the execution.

Supports: repeatability under the same path.

### R2 — Internal isolated implementation replication

Separately implemented encoders, compilers, lowerers, or verifiers operate without access to each other's generated artifacts.

Supports: implementation-path robustness.

Does not support: human, organizational, or conceptual independence.

### R3 — Independent technical replication

A separate person or organization implements and executes the frozen specification without using generated repository artifacts or unpublished repair knowledge.

Supports: independent technical reproducibility within the frozen design.

### R4 — Adversarial conceptual replication

Researchers not committed to FAR's framing design or control source cases, competitor specifications, objections, or adjudication.

Supports: resistance to framing and proponent bias.

### R5 — Cross-context replication

Independent teams reproduce relevant findings across materially different domains, source systems, or experimental designs.

Supports: broader robustness, but not universality by itself.

## Theory freeze

Every confirmatory experiment must identify a protected theory package containing:

- theory version;
- vocabulary semantics version;
- definitions and admissibility rules;
- compiler and verifier contracts;
- content digests;
- freeze commit;
- freeze date;
- authorized errata policy.

Material changes after result exposure create a new theory or experiment version. The earlier result remains immutable and is classified on its original terms.

## Material changes

A change is material when it can alter:

- candidate expressibility;
- preservation scoring;
- accepted transitions;
- failure conditions;
- cost accounting;
- equivalence classification;
- negative-control outcomes;
- claim interpretation.

Renaming or formatting changes are nonmaterial only when demonstrated incapable of changing these outcomes.

## Failure preservation

A failed frozen experiment must retain:

- the original package;
- all outputs and diagnostics;
- the failure classification;
- proposed repairs;
- the new version that incorporates any repair;
- an explicit statement that later success does not overwrite the earlier failure.

## Claim restrictions

- Implementation results must not be described as independent validation.
- R2 must not be described as R3 or R4.
- Confirmatory status cannot be assigned retrospectively.
- A bounded success must not be described as universality.
- A successful representation must not be described as necessity.
- Low primitive count must not be described as minimality without full-cost comparison.
- Failure to find a counterexample must not be described as proof.

## Evidence release requirements

Every release containing research claims must include:

- evidence class;
- replication layer;
- frozen versions;
- supported claims;
- unsupported claims;
- unfavorable results;
- unresolved questions;
- scope and assumptions;
- next decisive test.

## Governance

Any dispute over evidence class, replication layer, or materiality must be recorded. The more conservative classification controls until resolved.