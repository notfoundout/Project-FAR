# Theory/Dependency Authority Audit Report v1.0

Status: **Research**

Outcome: **failure report**

Investigation: `FAR-THEORY-DEPENDENCY-AUDIT-001`

Base commit: `5e8f27b617632a76e76760779dcbb24dedbb6786`

Executable result: [`result-v1.0.json`](result-v1.0.json)

## Lifecycle

| Stage | Status |
|---|---|
| Question | complete |
| Execution | complete |
| Observation | complete |
| Discovery | complete |
| Outcome | failure report |
| Replication | blocked pending separately preregistered source-complete campaign |
| Acceptance | prohibited |
| Promotion | prohibited |
| Repository Change | prohibited except Research evidence and validation wiring |

This Research artifact does not support a theory/dependency reconciliation. It records why the frozen design is insufficient and stops before Acceptance, Promotion, canonical correction, experiment preregistration, or execution.

## Preregistration provenance

The Question and frozen Execution specification are committed before the executor, observation, result, report, tests, or validation wiring. Repository tests verify that ancestry directly and fail if execution evidence appears in the preregistration parent commit.

## Frozen evidence

The campaign reads each selected source from the stated base commit with `git show <base>:<path>`. A shallow checkout fetches the exact base commit when necessary. Current working-tree versions are never substituted for historical evidence.

All nine selected files match their preregistered Git blob identities. Identity verification does not establish Acceptance.

Source admissibility:

- explicitly Accepted: 4;
- explicitly provisional: 1;
- Acceptance unverified within the frozen source set: 4.

The FARA primitive registry explicitly declares candidate status provisional. Acceptance is not verified within the selected evidence for the definitions artifact, semantic registry, FAR dependency graph, or FARO dependency graph.

The authoritative theorem/proof-status register was not selected or hash-locked. It cannot be imported after observing the outcome without violating the frozen design.

## Results

Raw content checks:

- C1: Pass
- C2: Pass
- C3: Fail
- C4: Pass
- C5: Pass
- C6: Pass
- C7: Pass

Evidence-admissibility adjudication:

- C1: Unknown
- C2: Unknown
- C3: Unknown
- C4: Pass
- C5: Unknown
- C6: Unknown
- C7: Pass

Candidate adjudication:

- `undifferentiated_owner`: **Unknown**
- `split_authority`: **Unknown**
- `logical_derivation`: **Unknown**
- `artifact_workflow_contract`: **Unknown**
- `unclassified_dependency`: **Unknown**

Discovery:

`no_reconciliation_discovery_supported`

Failure mode:

`source_admissibility_and_proof_scope_incomplete`

Any earlier split-authority or artifact-contract conclusion from this campaign is withdrawn.

## Why no post-hoc repair was made

The missing Accepted-status authority and proof inventory are outcome-relevant evidence. Adding them to this execution after observation would contaminate the preregistration. A new campaign must select and hash-lock them before execution.

## Required next campaign

A separately preregistered campaign must:

1. select and hash-lock the authoritative Accepted-status or promotion-provenance authority;
2. select and hash-lock `docs/governance/theorem-proof-status-register.md` and any proof objects it makes authoritative for the tested claims;
3. define how conflicting, provisional, canonical-only, superseded, and unstated statuses are adjudicated;
4. preserve `Unknown` whenever Acceptance, proof presence, proof absence, or source completeness is not verified;
5. reproduce or falsify C1–C7 without importing this executor's outcomes;
6. remain Research until separate replication, Acceptance, and Promotion stages are completed.

## Validation

The committed result is regenerated exactly from the frozen base blobs. Focused tests cover:

- preregistration ancestry;
- exact result regeneration and determinism;
- historical Git-blob identity;
- independence from mutable working-tree copies;
- Accepted, Provisional, and Unknown source states;
- omitted proof scope;
- tri-state checks and all-Unknown candidate output;
- source/status mutations;
- standard validation wiring;
- lifecycle status and nonclaims.

`health`, `health-fast`, and `research-check` explicitly run the executor and focused test module.

## Nonclaims

This report does not establish an Accepted authority model, an Accepted dependency classification, proof presence, proof absence, a canonical repository correction, experiment preregistration authorization, experiment execution authorization, global universality, primitive necessity, minimality, independence, irreducibility, or external-investigator independence.
