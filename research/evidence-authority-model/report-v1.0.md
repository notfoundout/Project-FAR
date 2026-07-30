# Evidence Authority Model Investigation Report v1.3

Status: **Research**

Investigation: `FAR-EVIDENCE-AUTHORITY-MODEL-001`

Discovery: **bounded candidate supported**

External replication: **pending**

Acceptance: **prohibited**

Promotion: **prohibited**

Canonical Repository Change: **deferred**

## Provenance

The investigation question was committed at `791906aa7f483c7906650bd0a55c8ba1505e2e62`. The frozen execution specification was committed at `2fe84b72a58e370f814b05a53aa0cf104b17afb1` before execution and evidence capture.

Pre-preregistration authority-model drafts are withdrawn design sketches and supply no evidence. Candidate artifacts remain under `research/evidence-authority-model/candidate/`; canonical governance paths remain absent.

## Frozen execution boundary

Every proof-discovery input was read from frozen commit `787d8776f0aab7c78cea9d536762c323b62d8c37`, tree `2d7b5c1647f4bc5578e65cbe709299d0c7baea51`. The validator identified 372 blob-locked inputs and produced discovery-input digest `1f1bdb8185c4104d2ae843a288149dbb361a4fb8def784cf0130f138813d1dff`.

The mutable PR tree was not used as the proof-discovery source. Candidate artifacts were validated from the Research branch while investigated repository evidence remained frozen.

## Executed validator

The public entrypoint is `research/evidence-authority-model/validate_candidate.py`, blob `1ec1acfed37091dc6820c3bb70950301e9897e67`. Its retained base engine is `research/evidence-authority-model/validator_core_v1.py`, blob `1d078266a10d8b73e8d841ffa72abbbe434efc25`.

The entrypoint explicitly replaces the two authority-sensitive operations exposed by review: numeric-priority adjudication and decision-record provenance validation. It does not install governance.

Primary evidence is recorded in `validation-evidence-v1.0.json`; repeat evidence is recorded in `repeat-validation-evidence-v1.0.json`; their comparison is recorded in `replication-comparison-v1.0.json`.

## Proof discovery

Both runs discovered 52 registered proof artifacts through all nine pathways:

- theorem metadata;
- lemma metadata;
- status-blind proposition metadata, including Proposed P-009;
- dependency-registry proof objects;
- verifier-required T-001 through T-015 proof objects;
- general structured metadata;
- object-valued proof paths;
- self-registering proof records; and
- terminal Lean entrypoints.

Registered paths were collected before existence testing.

## Conflict and priority adjudication

Two equal-priority opposite claims with identical proposition identity fields adjudicated to `Unknown`.

A separate unequal-priority probe used priority 1 Accepted governance and priority 5 Research. Because lower numeric rank is higher authority, priority 1 was selected and the result was `Affirmed`. Reversing the numeric ordering was detected by a dedicated mutation control.

## Structural decision provenance

The non-operative synthetic activation probe contained 52 artifact entries and 53 resolvable decision records: one manifest-Acceptance decision and one status/designation decision per artifact.

Validation required:

- manifest identifier and version linkage;
- `Accepted` decision status;
- `governance_decision` authority class and `Accepted` governance authority status;
- independence from the candidate;
- exact artifact, charter-status, and authority-bearing linkage for entry decisions;
- canonical manifest-digest linkage; and
- tamper-evident digest verification for every decision record.

Missing records, mismatched versions or artifact linkage, non-authoritative governance, and broken digest locks were independently injected and rejected. The synthetic bundle is explicitly non-operative and has no Acceptance, Promotion, or repository effect.

## Negative controls

The validator executed 32 mutations, all detected in both runs. They covered:

- six required governing domains;
- nine discovery pathways;
- proof-owner coverage;
- equal-priority fail-closed behavior;
- numeric-priority direction;
- manifest Acceptance gating;
- proof-status and authority-bearing separation;
- manifest and entry decision existence, linkage, authority, and hash locks;
- missing registered targets; and
- experiment-authority injection.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the frozen repository state. This bounded result does not establish correctness, necessity, minimality, uniqueness, universality, Acceptance, Promotion, or readiness for canonical implementation.

## Internal repeat

Primary execution:

- commit `3cb1999f51645f1aa84de97b1f7b418e38b88e26`;
- workflow run `30506960124`;
- job `90758711922`.

Repeat execution:

- commit `58aa3a15d69d2dd71668adf0d7b9501a52c52e57`;
- workflow run `30507130512`;
- job `90759219738`.

Both used identical entrypoint and core blobs, frozen commit, frozen tree, 372-input digest, 52-path inventory, 53-record synthetic probe, and 32-control campaign. Both produced evidence digest `8399794130250807c8b64d316a762bf39459e1b6def3e61a8d012c0e1e9915cf`.

The repeat is separately captured but is not externally independent. External replication remains mandatory before any later Acceptance.

## Lifecycle

| Stage | Status |
|---|---|
| Question | complete |
| Execution specification | frozen |
| Primary execution | complete, separately captured |
| Observation | complete |
| Discovery | complete, bounded candidate only |
| Internal repeat | complete, separately captured and compared |
| External replication | pending |
| Acceptance | prohibited |
| Promotion | prohibited |
| Canonical Repository Change | deferred and prohibited by this campaign |
| Retained repository material | Research evidence and reproducible Research validator only |

## Nonclaims

This campaign does not establish an Accepted authority model, a Promoted registry, authorized canonical Repository Change, canonical dependency reconciliation, logical derivation of FAR or FARO from FARA, theorem truth, proof-assistant verification, necessity, minimality, uniqueness, universality, or experiment authorization or prohibition.
