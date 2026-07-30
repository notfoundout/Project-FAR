# Evidence Authority Model Investigation Report v1.5

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

## Exact validated candidate

Both final executions validated identical blobs:

- candidate model: `3ff99dd626e26cc74b47f4e1f978737926a3b663`;
- candidate registry: `798ddae550304981df78cd539b1fab34768b3745`;
- candidate manifest: `68ac0a4bfa0b4e033be185ccc71b117e22b8552d`;
- candidate proof-discovery schema: `f220701b36fdb21a1a5035849c776183348d55cf`;
- validator entrypoint: `88cc42d24afc006c0dbcb3ce64d9120e9e5119bb`;
- reviewed v1 validator layer: `677d3f9a807ee0e488dc14b6f9f5babbf200ec45`;
- validator core: `1d078266a10d8b73e8d841ffa72abbbe434efc25`.

## Frozen execution boundary

Every proof-discovery input was read from frozen commit `787d8776f0aab7c78cea9d536762c323b62d8c37`, tree `2d7b5c1647f4bc5578e65cbe709299d0c7baea51`. The validator identified 372 blob-locked inputs and produced discovery-input digest `1f1bdb8185c4104d2ae843a288149dbb361a4fb8def784cf0130f138813d1dff`.

The mutable PR tree was not used as the proof-discovery source. Candidate artifacts were validated from the Research branch while investigated repository evidence remained frozen.

## Proof discovery

Both runs discovered 54 registered proof artifacts. The base contract covers theorem metadata, lemma metadata, status-blind proposition metadata including Proposed P-009, dependency-registry proof objects, verifier-required T-001 through T-015 objects, general structured metadata, object-valued paths, self-registering records, and terminal Lean entrypoints. Registered paths were collected before existence testing.

A separate inactive Research candidate extension declares constrained discovery for proof records that self-register through a canonical top-level `id` field. The rule applies only under declared roots, to JSON files whose names contain `proof`. It recovered two records omitted by the earlier inventory:

- `theory/evaluation/fara-core-formalization-proof-v1.0.json`;
- `theory/evaluation/fara-operator-w2-proof-v1.0.json`.

Disabling that schema pathway is detected by a dedicated mutation control.

## Conflict and priority adjudication

Two equal-priority opposite claims with identical proposition identity fields adjudicated to `Unknown`.

A separate unequal-priority probe used priority 1 Accepted governance and priority 5 Research. Because lower numeric rank is higher authority, priority 1 was selected and the result was `Affirmed`. Reversing the numeric ordering was detected by a dedicated mutation control.

## Structural decision provenance

The non-operative synthetic activation probe contained 54 artifact entries and 55 resolvable decision records: one manifest-Acceptance decision and one status/designation decision per artifact.

Validation required manifest identity and version linkage, `Accepted` decision status, `governance_decision` authority class, `Accepted` governance authority status, independence from the candidate, exact artifact/status/designation linkage, ISO decision date, non-empty supporting evidence, non-empty scope, non-empty limitations, canonical manifest-digest linkage, and tamper-evident record digests.

Missing records, mismatched linkage, non-authoritative governance, broken digest locks, and omission of each required provenance field were independently injected and rejected. The synthetic bundle is explicitly non-operative and has no Acceptance, Promotion, or repository effect.

## Negative controls

The validator executed 41 mutations, all detected in both final runs. They covered six required governing domains, the base discovery pathways, owner coverage, equal-priority fail-closed behavior, numeric-priority direction, manifest gating, proof-status separation, decision existence/linkage/authority/hash checks, eight date/evidence/scope/limitations omission controls, missing registered targets, experiment-authority injection, and disabling the canonical-`id` proof-record schema.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the frozen repository state. This bounded result does not establish correctness, necessity, minimality, uniqueness, universality, Acceptance, Promotion, or readiness for canonical implementation.

## Internal repeat

Primary execution:

- commit `5f715d740a9a1d08c096351889ea8c84b0ba0478`;
- workflow run `30514345750`;
- job `90780772893`.

Repeat execution:

- commit `97116189e6debb33067ceaa8f16e3e4e52054d8d`;
- workflow run `30514438925`;
- job `90781052642`.

Both used identical final candidate and validator blobs, frozen commit, frozen tree, 372-input digest, 54-path inventory, 55-record synthetic probe, and 41-control campaign. Both produced evidence digest `565befa500cec5da8af44671ff7ba3696e2c828525c5eea82460f1491fe416d9`.

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
