# Evidence Authority Model Investigation Report v1.7

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
- candidate proof-discovery schema: `b460ae67754579f0319beb679dcac5b8fcce7a0a`;
- validator entrypoint: `12754bd5a1ead5cd5313a8591ea430571686eec7`;
- reviewed v1 validator layer: `677d3f9a807ee0e488dc14b6f9f5babbf200ec45`;
- validator core: `1d078266a10d8b73e8d841ffa72abbbe434efc25`.

## Frozen execution boundary

Every proof-discovery input was read from frozen commit `787d8776f0aab7c78cea9d536762c323b62d8c37`, tree `2d7b5c1647f4bc5578e65cbe709299d0c7baea51`. The validator identified 372 blob-locked inputs and produced discovery-input digest `1f1bdb8185c4104d2ae843a288149dbb361a4fb8def784cf0130f138813d1dff`.

The mutable PR tree was not used as the proof-discovery source. Candidate artifacts were validated from the Research branch while investigated repository evidence remained frozen.

## Proof discovery

Both runs discovered 59 registered proof artifacts. The base contract covers theorem metadata, lemma metadata, status-blind proposition metadata including Proposed P-009, dependency-registry proof objects, verifier-required T-001 through T-015 objects, general structured metadata, object-valued paths, self-registering records, and terminal Lean entrypoints. Registered paths were collected before existence testing.

A separate inactive Research candidate extension declares three constrained schema-aware pathways.

The `proof_object_id` rule applies only under declared roots to JSON records carrying that identifier field. It recovered:

- `theory/evaluation/fara-vocabulary-sufficiency-v1.0.json`;
- `theory/evaluation/fara-w4-representation-boundary-v1.0.json`;
- `theory/evaluation/fara-w5-cross-representation-invariance-v1.0.json`.

The canonical top-level `id` rule applies only under declared roots to JSON files whose names contain `proof`. It recovered:

- `theory/evaluation/fara-core-formalization-proof-v1.0.json`;
- `theory/evaluation/fara-operator-w2-proof-v1.0.json`.

The hash-locked artifact-map rule traverses keys under the declared `historical_artifacts` mapping field, but only under declared source roots and only for JSON paths whose filenames contain `proof`. It recovered:

- `theory/evaluation/fara-expanded-bounded-campaign-proof-v1.0.json`;
- `theory/evaluation/fara-foundation-comparison-proof-v1.0.json`.

Disabling each schema pathway is detected by its own mutation control.

## Conflict and priority adjudication

Two equal-priority opposite claims with identical proposition identity fields adjudicated to `Unknown`.

A separate unequal-priority probe used priority 1 Accepted governance and priority 5 Research. The validator derives numeric direction from the candidate model's declaration that lower numeric rank means higher authority; priority 1 was therefore selected and the result was `Affirmed`. Reversing the candidate declaration was detected by a dedicated mutation control. The control no longer tests a private validator-only argument.

## Structural decision provenance

The non-operative synthetic activation probe contained 59 artifact entries and 60 resolvable decision records: one manifest-Acceptance decision and one status/designation decision per artifact.

Validation required manifest identity and version linkage, `Accepted` decision status, `governance_decision` authority class, `Accepted` governance authority status, independence from the candidate, exact artifact/status/designation linkage, ISO decision date, non-empty supporting evidence, non-empty scope, non-empty limitations, canonical manifest-digest linkage, and tamper-evident record digests.

Missing records, mismatched linkage, non-authoritative governance, broken digest locks, and omission of each required provenance field were independently injected and rejected. The synthetic bundle is explicitly non-operative and has no Acceptance, Promotion, or repository effect.

## Negative controls

The validator executed 43 mutations, all detected in both final runs. They covered six required governing domains, the base discovery pathways, owner coverage, equal-priority fail-closed behavior, candidate-declared numeric-priority direction, manifest gating, proof-status separation, decision existence/linkage/authority/hash checks, eight date/evidence/scope/limitations omission controls, missing registered targets, experiment-authority injection, disabling the `proof_object_id` schema, disabling the canonical-`id` schema, and disabling the hash-locked artifact-map-key schema.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the frozen repository state. This bounded result does not establish correctness, necessity, minimality, uniqueness, universality, Acceptance, Promotion, or readiness for canonical implementation.

## Internal repeat

Primary execution:

- commit `ddd4ced4a467f5a202e804bd333a1709509c05c3`;
- workflow run `30517745133`;
- job `90791242158`.

Repeat execution:

- commit `d4968f0334da2db56df8e6dcba313dd3a84c9e55`;
- workflow run `30517874492`;
- job `90791636534`.

Both used identical final candidate and validator blobs, frozen commit, frozen tree, 372-input digest, 59-path inventory, 60-record synthetic probe, and 43-control campaign. Both produced evidence digest `7c2deb179b15a2a08e6562d2af852f574384e679b4dc60b10fca737abb95b770`.

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
