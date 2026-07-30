# Evidence Authority Model Investigation Report v1.2

Status: **Research**

Investigation: `FAR-EVIDENCE-AUTHORITY-MODEL-001`

Discovery: **bounded candidate supported**

External replication: **pending**

Acceptance: **prohibited**

Promotion: **prohibited**

Canonical Repository Change: **deferred**

## Provenance

The investigation question was committed at `791906aa7f483c7906650bd0a55c8ba1505e2e62`. The frozen execution specification was committed at `2fe84b72a58e370f814b05a53aa0cf104b17afb1` before the execution, observation, result, repeat, and post-preregistration candidate revision.

Any authority-model draft predating the frozen specification is withdrawn as an unvalidated design sketch and supplies no evidence to this result.

The candidate is retained only under `research/evidence-authority-model/candidate/`. The corresponding canonical governance paths are absent. Permanent canonical test wiring is also absent. Canonical implementation requires external replication, Acceptance, Promotion, and an authorized Repository Change.

## Frozen execution boundary

Every proof-discovery input was read from preregistered frozen commit `787d8776f0aab7c78cea9d536762c323b62d8c37`, tree `2d7b5c1647f4bc5578e65cbe709299d0c7baea51`. The validator identified 372 JSON, YAML, YML, and verifier inputs by Git blob SHA and produced discovery-input digest `1f1bdb8185c4104d2ae843a288149dbb361a4fb8def784cf0130f138813d1dff`.

The mutable PR working tree was not used as the proof-discovery source. Candidate model, registry, and manifest artifacts were validated from the research branch, while the investigated repository evidence remained frozen.

## Frozen question

The campaign asked whether a non-self-activating Research candidate could cover governing dependencies, repository proof-registration pathways, proof-status separation, manifest provenance, equal-priority conflict failure, and experiment nonauthorization without claiming Acceptance, Promotion, or canonical Repository Change.

## Executed validation

The reproducible validator is `research/evidence-authority-model/validate_candidate.py`, Git blob `1d078266a10d8b73e8d841ffa72abbbe434efc25`.

Primary evidence is recorded in `validation-evidence-v1.0.json`. Separate repeat evidence is recorded in `repeat-validation-evidence-v1.0.json`. Their comparison is recorded in `replication-comparison-v1.0.json`.

The executions passed A1–A8 and discovered 52 registered proof artifacts through all nine required pathways:

- theorem metadata;
- lemma metadata;
- status-blind proposition metadata, including Proposed P-009 and `theory/theorems/propositions.md`;
- dependency-registry proof objects;
- verifier-required T-001 through T-015 proof objects;
- general structured metadata;
- object-valued proof paths;
- self-registering proof records; and
- terminal Lean entrypoints.

Registered paths were collected before existence testing, so missing or misspelled targets cannot disappear from validation.

## Concrete conflict adjudication

The validator injected two claims with the same proposition identifier, scope, premises, version, and priority but opposite polarities. The candidate conflict policy adjudicated the pair as `Unknown` with reason `equal_priority_contradiction`.

Two mutations then disabled fail-closed behavior: one changed the unresolved result, and one permitted dual authority. Both were detected through the concrete claim adjudicator, not merely through string comparison.

## Proof-status separation

The validator generated a complete 52-entry activation-manifest probe. Every artifact appeared exactly once with a charter status, authority-bearing designation, decision record, scope, and limitations. One artifact was authority-bearing and `Accepted`; the remaining Research artifacts were explicitly non-authority-bearing and excluded from active proof authority.

The valid probe passed. Three independent mutations were rejected:

- authority was granted to a `Research` proof artifact;
- the authority-bearing designation was removed; and
- the registry policy was weakened to allow a non-`Accepted` authority-bearing status.

The candidate manifest itself remains empty, inactive, and Research. The probe tests the activation rules; it does not populate or Accept the candidate manifest.

## Negative controls

The validator executed 24 mutations. Every fault was detected. The campaign separately:

- removed each of six required governing domains;
- disabled each of nine proof-discovery pathways;
- removed proof-owner coverage;
- injected concrete contradictory claims under two non-fail-closed policies;
- removed the manifest Acceptance gate;
- granted authority to an unaccepted proof;
- omitted the authority-bearing designation;
- weakened the authority-bearing status policy;
- injected a missing registered target; and
- injected experiment authority.

This evidence replaces earlier unsupported assertions about control execution.

## Observation

The source record supports a candidate construction, not active authority. The research-execution charter remains Provisional, the proof-assurance taxonomy remains Unknown, no bootstrap authority is selected, the candidate manifest remains Research and empty, and no external investigator has replicated the result.

The campaign therefore retains only research evidence and a reproducible research validator. It does not create canonical governance artifacts.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the frozen repository state. This is a bounded research result. It does not establish that the candidate is correct, necessary, minimal, unique, universal, Accepted, Promoted, or ready for canonical implementation.

## Internal repeat

The primary execution used commit `687d3cd50ff5b8eb7e485cd5b6a8db3def87db64`, workflow run `30503257408`, job `90747380558`.

The repeat used commit `ba528f5e4891b14c33791716097b6a5a3e2b035e`, workflow run `30503397417`, job `90747810604`.

Both runs used the identical validator blob, frozen commit, frozen tree, 372-input digest, 52-path inventory, and 24-control campaign. Both produced evidence digest `8ba33d1d14d3e97d3adf4d0a16cd3b1f340c41370be698708e1d5c11ea9894a6`.

The repeat is separately identified and reproducible, but it is not externally independent. External replication remains mandatory before any later Acceptance.

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
| Retained repository material | research evidence and reproducible research validator only |

## Nonclaims

This campaign does not establish an Accepted authority model, a Promoted registry, an authorized canonical Repository Change, a canonical dependency reconciliation, logical derivation of FAR or FARO from FARA, theorem truth, proof-assistant verification, necessity, minimality, uniqueness, universality, or experiment authorization or prohibition.
