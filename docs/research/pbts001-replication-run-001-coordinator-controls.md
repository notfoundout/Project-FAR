# PBTS-001 Independent Replication RUN-001 Coordinator Controls

## Status

Frozen coordinator-control package for `PBTS-001-REP-001-RUN-001`.

No replicator is registered, calibrated, assigned, or authorized to submit by this artifact. No replication judgment, result, or evidence classification is recorded. All execution and representation-theorem gates remain closed.

## Purpose

This document defines the controls required to register real independent replicators and execute the frozen `PBTS-001-REP-001` package without inventing participants, overstating independence, exposing one replicator to another's work, or modifying PB-001, PBTS-001, or the replication package after exposure.

## Frozen dependencies

RUN-001 depends on the unchanged versions registered in:

- `theory/evaluation/pbts001-independent-replication-registry.json`;
- `docs/research/pbts001-independent-replication-package-v1.0.md`;
- `docs/research/pbts001-independent-replication-calibration-v1.0.md`;
- `theory/evaluation/pbts001-independent-replication-response-schema.json`.

RUN-001 may not revise those artifacts. Material repair requires a new package or run version, while preserving this run's record.

## Roles

The following roles are distinct even when practical constraints require one person to hold more than one nonconflicting role:

1. package coordinator;
2. primary replicator;
3. calibration scorer;
4. independence auditor;
5. submission custodian;
6. adjudicator;
7. aggregation operator;
8. red-team reviewer.

A primary replicator may not score their own calibration, audit their own independence, adjudicate their own disputed response, or aggregate results before all primary submissions are frozen.

The package coordinator may administer files and deadlines but may not repair a replicator's reasoning, suggest favorable judgments, or disclose another submission before the mutual embargo is lifted.

## Primary slots

RUN-001 contains exactly three primary slots:

- `REP-A`;
- `REP-B`;
- `REP-C`.

These are opaque public identifiers. A slot is not a participant. It becomes active only after a real person or independent organization satisfies registration, exposure, competence, and independence controls.

No placeholder, simulated identity, assistant persona, repeated pass by one agent, or isolated implementation authored by the project team may be counted as a distinct primary replicator.

## Registration requirements

A registration must contain:

- stable registration ID;
- slot requested;
- real-person or organization attestation;
- competency statement covering formal specifications and state-transition or reasoning-system analysis;
- current affiliation or documented unaffiliated status;
- prior relationship to Project FAR, FARA, PB-001, PBTS-001, and their authors;
- funding, employment, collaboration, and conflict disclosures;
- tools, models, assistants, and code-generation systems expected to be used;
- declaration that the registrant did not author the frozen package;
- signed nonclaim and failure-preservation acknowledgement;
- timestamp and immutable content digest.

Public records may use an opaque participant ID, but the independence auditor must have sufficient identity evidence to prevent duplicate or fictitious enrollment. Any private identity record must be committed by digest and retained under a stated custody policy.

## Exposure declaration

Before calibration, each registrant must separately declare whether they accessed:

- the RUN-001 report;
- RUN-001 records or summary;
- commentary or derivative summaries containing RUN-001 judgments;
- another replication submission;
- unpublished repair guidance;
- prior Project FAR mapping or adjudication material relevant to PBTS-001.

A declaration of no exposure is an attestation, not guaranteed blinding, because the repository is public.

Known exposure does not erase the submission. It requires preservation and downgrade to the strongest justified replication layer. Deliberately false exposure statements invalidate R3 eligibility and trigger a permanent rejection or downgrade record.

## Independence audit

The auditor assigns the strongest justified layer using the frozen evidence standard:

- `R1`: same team and implementation path;
- `R2`: isolated implementation paths without human or organizational independence;
- `R3`: separate person or organization executing the frozen specification without unpublished repair knowledge or prior-result exposure;
- `R4`: adversarial conceptual replication by parties not committed to the Project FAR framing;
- `R5`: cross-context replication across materially different domains or designs;
- `unresolved`: evidence is insufficient to classify.

The target for each primary slot is at least R3. A lower classification remains scientifically useful but cannot satisfy the R3 gate.

At least two distinct organizational affiliations are required across the three primary slots unless the auditor documents why independently unaffiliated replicators satisfy an equivalent separation standard.

## Calibration controls

Calibration uses the frozen six-item instrument and rubric.

A primary replicator qualifies only when:

- at least five of six items are correct;
- the critical observation-versus-inference item is correct;
- no more than one retest is used;
- the scorer is not the registrant;
- only the calibration result, not coaching or repair, is communicated before qualification.

Calibration demonstrates minimum protocol-reading competence. It does not establish independence, scientific authority, or correctness of later judgments.

## Assignment plan

Every qualified primary replicator receives the full suite. Assignment randomizes section order rather than case ownership so that all three submissions remain independently complete.

The frozen order-generation procedure is:

1. canonical sections are `PAIR`, `ABLATION`, `DOMAIN`, `COUNTERMODEL`, `HIDDEN_RECOVERY`, `ADDITION_SEARCH`, `P8`, and `DISCLOSURES`;
2. use deterministic Fisher-Yates permutation with SHA-256 counter-mode bytes;
3. seed material is `PBTS-001-REP-001-RUN-001|slot-id|order-v1`;
4. generate one permutation independently for REP-A, REP-B, and REP-C;
5. write the generated orders only after each slot is qualified;
6. never use results, identities, affiliations, or expected conclusions as seed material.

No replicator receives another slot's order, registration, calibration detail, or submission before all primary submissions are frozen.

## Participant-facing bundle

The participant-facing bundle includes only:

- frozen protected inputs;
- replication protocol;
- calibration instructions after registration;
- response schema;
- the slot's generated section order;
- submission instructions;
- explicit nonclaims.

It excludes the three RUN-001 result artifacts and any derivative summary of their judgments.

## Append-only channels

RUN-001 uses separate machine-readable channels for:

- registrations;
- exposure declarations;
- calibration records;
- independence audits;
- assignments;
- submissions;
- rejections and withdrawals;
- adjudications;
- aggregation and results.

Each accepted record requires:

- stable record ID;
- referenced slot and registration ID where applicable;
- timestamp;
- status;
- content digest;
- supersedes field, if any;
- actor role;
- reason for rejection, downgrade, withdrawal, or amendment.

Records may be superseded but not deleted or silently replaced. Corrections append a new record and retain the prior record.

## Submission embargo

Primary replicators work without access to one another's submissions.

A submission is frozen when the submission custodian records its digest and timestamp. Content may not be amended after freeze except through an append-only deviation or supersession record. All three frozen submissions, or the permanent failure of a slot to submit, must be recorded before cross-submission comparison begins.

## Rejection and downgrade rules

A record is rejected or downgraded when any of the following occurs:

- fictitious or duplicate identity;
- failed calibration after the allowed retest;
- material undeclared exposure;
- package modification;
- missing required suite family;
- evaluator repair supplied by the coordinator or another replicator;
- uncounted hidden machinery;
- submission access before the mutual embargo is lifted;
- unresolved identity or independence evidence;
- prohibited deletion or replacement of an unfavorable answer.

Rejected records remain preserved. A rejected primary slot may be replaced only through a new registration record and explicit slot-reassignment record.

## Aggregation lock

Aggregation is forbidden until:

- three primary submissions are frozen or permanently classified as unavailable;
- exposure and independence audits are complete;
- all rejections and downgrades are recorded;
- the red-team reviewer confirms that no hidden repair or result-dependent exclusion occurred.

Aggregation reports full distributions. It does not replace `Unknown` with an ordered score, discard disagreement, or reduce P1-P8 to an unregistered scalar.

## P8 decision control

Each primary submission must independently classify P8 as:

- ordinary preservation coordinate;
- cross-cutting evidential qualifier;
- separate evidence contract;
- axis revision required;
- unresolved.

The coordinator may not provide RUN-001's P8 interpretation before submission freeze. Material disagreement is a result and keeps P8-dependent theorem obligations unresolved unless alternatives are formally registered.

## Advance gates

The run may begin only after:

- at least three real registrants are recorded;
- all three pass calibration;
- all three exposure declarations are recorded;
- all three independence audits classify the strongest justified layer;
- all three assignments are generated and frozen;
- append-only channels are operational;
- participant-facing bundles are verified to exclude prior results;
- the representation-theorem gate remains closed.

The representation-theorem gate may be reconsidered only after completed submissions, adjudication, aggregation, unfavorable-result publication, and an explicit gate decision under the frozen replication package.

## Current status

No registrants exist. No calibration has been administered. No assignments have been generated. No submission channel contains a response. No independent replication result exists.

The next action is external: recruit and register qualified real replicators under these controls. Repository automation cannot manufacture genuine human, organizational, or conceptual independence.

## Nonclaims

Freezing these controls does not establish:

- participant qualification;
- independent replication;
- R3, R4, or R5 evidence;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- resolution of P8;
- FARA compliance;
- a representation theorem;
- universality, global minimality, superiority, or comparative economy.
