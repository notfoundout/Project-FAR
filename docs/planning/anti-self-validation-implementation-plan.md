# Anti-Self-Validation Implementation Plan

## Objective

Convert the anti-self-validation standard from a governance statement into an enforced research workflow.

This plan does not declare existing experiments invalid. It classifies their maximum evidential force and defines the work required before stronger claims may be made.

## Current Baseline

Project FAR already distinguishes bounded mechanized results from universality, necessity, minimality, and external independence. The remaining risk is procedural: project-authored theories, scenarios, mappings, compilers, verifiers, and interpretations can still form a closed validation loop.

The implementation program therefore prioritizes controls that can produce unfavorable results.

## Workstream 1 — Governance Adoption

### Deliverables

- adopt `docs/governance/anti-self-validation-standard.md`;
- add it as a dependency of the Central Research Program;
- require a compliance statement in every new confirmatory experiment;
- classify legacy experiments against the new evidential classes;
- prohibit retrospective relabeling of internal replication as external replication.

### Completion criteria

Every active confirmatory experiment identifies the standard version and states any unmet requirement.

## Workstream 2 — Claim Ledger

### Deliverables

Create a canonical claim ledger directory and instantiate entries for:

- existence of a common reasoning structure;
- FAR bounded sufficiency;
- FAR universality;
- necessity of each proposed primitive;
- FAR minimality;
- FAR nontrivial constraint;
- comparative economy;
- independent replication.

Use `docs/templates/claim-ledger-entry.md`.

### Completion criteria

Every central claim has evidence for, evidence against, falsification conditions, nonclaims, and a next decisive test.

## Workstream 3 — External Observation Contracts

### Deliverables

For each confirmatory experiment:

- define observables from the source system before candidate mappings;
- identify distinctions that must survive translation;
- separate behavioral equivalence from commitment equivalence;
- register failure effects for every observable;
- prevent FAR-native categories from defining success by construction.

### Completion criteria

All candidates are evaluated against the same frozen source-facing contract.

## Workstream 4 — Full-Cost Accounting

### Deliverables

Extend comparative representation records to count:

- primitives;
- derived constructs;
- operations;
- semantic description length;
- hidden state;
- ambiguity and adjudication policies;
- external interpreter machinery;
- exceptions and case-specific patches.

### Completion criteria

No candidate receives a lower apparent cost by relocating commitments into derived machinery, metadata, compiler behavior, or verifier assumptions.

## Workstream 5 — Negative Controls

### Deliverables

Add mandatory invalid encodings for:

- lookup-table reproduction;
- dependency collapse;
- history erasure;
- hidden rule modification;
- label-only semantics;
- unrestricted interpreter use;
- hidden auxiliary state;
- provenance deletion;
- output-equivalent process substitution.

### Completion criteria

The verifier rejects the registered invalid encodings for the registered reasons. Any unexpected pass blocks a nontrivial-constraint claim.

## Workstream 6 — Ablation and Reintroduction Detection

### Deliverables

For every primitive ablation:

- register forbidden aliases;
- inspect derived relations;
- inspect hidden state;
- inspect compiler behavior;
- inspect verifier assumptions;
- inspect metadata and external code;
- perform semantic-equivalence review.

### Completion criteria

Ablation conclusions distinguish genuine removal from renamed or relocated reintroduction.

## Workstream 7 — Competitor Independence

### Deliverables

- obtain authoritative competitor specifications;
- invite advocates or qualified reviewers to challenge reconstructions;
- allow competitors equivalent clarification rights;
- record whether FAR authors designed or repaired the baseline;
- label project-authored competitors as internal benchmarks.

### Completion criteria

No superiority claim depends only on a competitor defined by FAR proponents.

## Workstream 8 — Replication Layers

### Internal implementation replication

Use separately implemented encoders, compilers, and verifiers with artifact isolation.

Permitted conclusion: implementation-path robustness.

### Independent technical replication

A separate person or group implements the frozen specification without using generated repository artifacts.

Permitted conclusion: independent technical reproducibility.

### Adversarial conceptual replication

Researchers who do not accept FAR’s framing design or review cases, competitors, and objections.

Permitted conclusion: resistance to conceptual framing bias.

### Completion criteria

Each replication result is labeled by the layer actually achieved.

## Workstream 9 — Holdout Counterexample Challenge

### Deliverables

- appoint a holdout custodian;
- generate boundary-focused cases privately;
- freeze theory, metrics, and failure rules before exposure;
- include hostile reasoning classes;
- publish all holdout cases and outcomes after execution.

### Completion criteria

The FAR team cannot alter the protected theory or scoring rules after seeing the holdout.

## Workstream 10 — Immutable Failure Registry

### Deliverables

Record permanently:

- failed frozen experiments;
- unresolved mappings;
- exclusions;
- discarded evaluator responses;
- adjudication disputes;
- post hoc scope changes;
- negative controls that passed;
- theory revisions triggered by failure.

### Completion criteria

A later successful version links to but does not overwrite the earlier failure.

## Workstream 11 — Nonclaim Audit

### Deliverables

Before every evidence release, audit whether wording implies:

- universality from bounded cases;
- necessity from successful use;
- minimality from low primitive count;
- independence from isolated internal implementations;
- truth from mechanized conformance;
- commercial readiness from technical functionality.

### Completion criteria

Every release includes explicit nonclaims proportionate to the result.

## Workstream 12 — Infrastructure Constraint

### Rule

Every new dashboard, certification, audit, registry, or governance artifact must identify the active research experiment it enables.

### Completion criteria

Infrastructure work that does not advance a current research gate is classified as maintenance or deferred.

## Research Gate Status

The following status labels are conservative and should be updated only through claim-ledger review.

| Gate | Question | Current status |
|---|---|---|
| 1 | Can FAR be specified and implemented coherently? | substantially supported internally |
| 2 | Can FAR preserve bounded frozen systems? | partially supported; scope and derived machinery matter |
| 3 | Can FAR reject invalid output-equivalent encodings? | not established generally |
| 4 | Are primitives locally necessary under reintroduction controls? | not established |
| 5 | Is FAR comparatively economical against strong alternatives? | not established |
| 6 | Can independent outsiders reproduce results? | not established generally |
| 7 | Are failure boundaries known? | incomplete |
| 8 | Is a universality or minimality conclusion justified? | not established |

## Immediate Sequence

1. Merge the governance standard and templates.
2. Create canonical claim-ledger entries.
3. Select one bounded experiment as the pilot conversion.
4. Freeze its external observation contract.
5. add full-cost accounting and negative controls;
6. run hidden-reintroduction review;
7. perform internal isolated implementation replication;
8. seek independent technical replication;
9. run a private holdout challenge;
10. update the claim ledger without deleting failures.

## Pilot Recommendation

Use the next unexecuted comparative-representation experiment rather than retrofitting a completed result as the first full pilot.

Legacy experiments should be audited and classified, but a new prospective study provides the cleanest test of whether the controls work before results are known.

## Success Condition

This implementation succeeds when Project FAR can produce and preserve a result that weakens FAR under the same machinery used to recognize a favorable result.