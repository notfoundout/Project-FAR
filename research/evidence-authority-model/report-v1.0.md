# Evidence Authority Model Investigation Report v1.8

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
- validator entrypoint: `d4197968646c555f133ff416df32627d4dec8118`;
- reviewed v1 validator layer: `677d3f9a807ee0e488dc14b6f9f5babbf200ec45`;
- validator core: `1d078266a10d8b73e8d841ffa72abbbe434efc25`.

## Frozen execution boundary

Every proof-discovery input was read from frozen commit `787d8776f0aab7c78cea9d536762c323b62d8c37`, tree `2d7b5c1647f4bc5578e65cbe709299d0c7baea51`. The validator identified 372 blob-locked inputs and produced discovery-input digest `1f1bdb8185c4104d2ae843a288149dbb361a4fb8def784cf0130f138813d1dff`.

The mutable PR tree was not used as the proof-discovery source. Candidate artifacts were validated from the Research branch while investigated repository evidence remained frozen.

## Frozen A1-A3 contract enforcement

The final validator does not allow the candidate to define its own success conditions.

For A1, it parses and enforces four exact model-header declarations: `Status: Research`, `Candidacy: Inactive candidate`, `Promotion completed: No`, and `Canonical governance implementation: Deferred`. Mutating each declaration independently caused validation failure.

For A2, it independently requires a bootstrap authority that predates and is independent of the candidate, requires preregistration and hash locking, and compares the registry against the complete frozen activation and promotion requirement sets. Self-referential authority, disabling the hash-lock gate, clearing activation requirements, and clearing promotion requirements were all detected.

For A3, the six governing domains are a fixed validator oracle derived from the preregistered design, not from `required_governing_domains`. Removing each domain from both the candidate declaration and the owner map was independently detected.

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

A separate unequal-priority probe used priority 1 Accepted governance and priority 5 Research. The validator derives numeric direction from the candidate model's declaration that lower numeric rank means higher authority; priority 1 was therefore selected and the result was `Affirmed`. Reversing the candidate declaration was detected by a dedicated mutation control. The control does not use a private validator-only priority argument.

## Structural decision provenance

The non-operative synthetic activation probe contained 59 artifact entries and 60 resolvable decision records: one manifest-Acceptance decision and one status/designation decision per artifact.

Validation required manifest identity and version linkage, `Accepted` decision status, `governance_decision` authority class, `Accepted` governance authority status, independence from the candidate, exact artifact/status/designation linkage, ISO decision date, non-empty supporting evidence, non-empty scope, non-empty limitations, canonical manifest-digest linkage, and tamper-evident record digests.

Missing records, mismatched linkage, non-authoritative governance, broken digest locks, and omission of each required provenance field were independently injected and rejected. The synthetic bundle is explicitly non-operative and has no Acceptance, Promotion, or repository effect.

## Negative controls

The validator executed 57 mutations, all detected in both final runs. The campaign includes the prior governance, discovery, ownership, conflict, priority, manifest, status-separation, provenance, missing-target, and experiment-boundary controls, plus:

- three schema-aware proof-discovery disable controls;
- four model-header mutations;
- four external-bootstrap and lifecycle-declaration mutations; and
- six candidate-controlled A3 bypass mutations, one for each frozen governing domain.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the frozen repository state. This bounded result does not establish correctness, necessity, minimality, uniqueness, universality, Acceptance, Promotion, or readiness for canonical implementation.

## Internal repeat

Primary execution:

- commit `f916fe2b2e8e6cb02ad753e9114fa9adbb5fd186`;
- workflow run `30519399225`;
- job `90796266056`.

Repeat execution:

- commit `bbaee75cf16dd76658ab97beac11e42ec22e266d`;
- workflow run `30519531630`;
- job `90796656093`.

Both used identical final candidate and validator blobs, frozen commit, frozen tree, 372-input digest, 59-path inventory, 60-record synthetic probe, and 57-control campaign. Both produced evidence digest `bec322a704c4f3932a716b3798f1cd9bd81136635e486ddc862eac38bdab53a0`.

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
