# Evidence Authority Model Investigation Report v1.1

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

## Frozen question

The campaign asked whether a non-self-activating Research candidate could cover governing dependencies, repository proof-registration pathways, proof-status separation, manifest provenance, equal-priority conflict failure, and experiment nonauthorization without claiming Acceptance, Promotion, or canonical Repository Change.

## Executed validation

The reproducible validator is `research/evidence-authority-model/validate_candidate.py`. Its machine-readable run record is `research/evidence-authority-model/validation-evidence-v1.0.json`.

The execution passed A1–A8 and discovered 51 registered proof artifacts through all nine required pathways:

- theorem metadata;
- lemma metadata;
- proposition metadata;
- dependency-registry proof objects;
- verifier-required T-001 through T-015 proof objects;
- general structured metadata;
- object-valued proof paths;
- self-registering proof records; and
- terminal Lean entrypoints.

Registered paths were collected before existence testing, so missing or misspelled targets cannot disappear from validation.

## Negative controls

The validator executed 21 mutations. Every fault was detected. The campaign separately removed each required governing domain, disabled each proof-discovery pathway, removed owner coverage, permitted incorrect equal-priority resolution, permitted dual authority, removed the manifest Acceptance gate, injected a missing registered target, and injected experiment authority.

This replaces the earlier unsupported assertion that the controls had passed. The current result is backed by executed mutation evidence.

## Observation

The source record supports a candidate construction, not active authority. The research-execution charter remains Provisional, the proof-assurance taxonomy remains Unknown, no bootstrap authority is selected, the candidate manifest remains Research and empty, and no external investigator has replicated the result.

The campaign therefore retains only research evidence and a reproducible research validator. It does not create canonical governance artifacts.

## Discovery

`bounded_candidate_supported`

At least one proposition-specific, non-self-activating Research candidate satisfies the frozen construction conditions for the current repository. This is a bounded research result. It does not establish that the candidate is correct, necessary, minimal, unique, universal, Accepted, Promoted, or ready for canonical implementation.

## Replication

A second deterministic clean repeat reproduced A1–A8 and the 21-control mutation campaign without importing the first result fields. This repeat is not externally independent. External replication remains mandatory before any later Acceptance.

## Lifecycle

| Stage | Status |
|---|---|
| Question | complete |
| Execution specification | frozen |
| Execution | complete |
| Observation | complete |
| Discovery | complete, bounded candidate only |
| Internal repeat | complete |
| External replication | pending |
| Acceptance | prohibited |
| Promotion | prohibited |
| Canonical Repository Change | deferred and prohibited by this campaign |
| Retained repository material | research evidence and reproducible research validator only |

## Nonclaims

This campaign does not establish an Accepted authority model, a Promoted registry, an authorized canonical Repository Change, a canonical dependency reconciliation, logical derivation of FAR or FARO from FARA, theorem truth, proof-assistant verification, necessity, minimality, uniqueness, universality, or experiment authorization or prohibition.
