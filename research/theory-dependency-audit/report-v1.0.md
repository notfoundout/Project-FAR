# Theory/Dependency Authority Audit Report v1.0

Status: **Research**

Investigation: `FAR-THEORY-DEPENDENCY-AUDIT-001`

Base commit: `5e8f27b617632a76e76760779dcbb24dedbb6786`

Executable result: [`result-v1.0.json`](result-v1.0.json)

## Lifecycle

| Stage | Status |
|---|---|
| Question | complete |
| Execution | complete |
| Observation | complete |
| Discovery | Research finding |
| Replication | pending separate implementation |
| Acceptance | prohibited |
| Promotion | prohibited |
| Repository Change | prohibited except Research evidence |

This report stops at Discovery. It does not change canonical authority, dependency classification, framework documentation, project status, the preregistration gate, or experiment authorization.

## Execution

The audit evaluated nine accepted artifacts locked by Git blob identity:

- shared-theory definitions;
- the FARA primitive registry;
- the Accepted scoped FARA formal kernel;
- canonical terminology;
- the semantic-consistency registry;
- framework boundaries;
- the derivation-status matrix;
- the FAR dependency graph;
- the FARO dependency graph.

Seven preregistered checks evaluated canonical definition authority, FARA candidate classification, adequacy of the current owner registry, the formal-kernel role boundary, FAR dependency kind, FARO dependency kind, and protocol-derivation boundaries.

## Observations

1. Shared theory explicitly claims repository-wide canonical definition authority and contains definitions for all seven FARA candidate-primitive terms.
2. FARA separately lists the same seven terms as candidate primitives while pointing canonical definitions back to shared theory.
3. The accepted semantic registry marks only Object, Property, Relation, and Representation as candidate primitives. Interpretation, Investigation, and Reasoning Calculus are absent from that candidate-primitive registry.
4. The semantic registry exposes one undifferentiated `owner` field. It cannot record shared-theory definition authority and FARA candidate-classification authority simultaneously.
5. The Accepted FARA formal kernel is scoped to finite, explicit, auditable Project FAR v1.0 architecture and explicitly does not reclassify the seven candidate primitives or establish their global primitive properties.
6. FAR's dependency graph says FARA provides architecture that FAR applies methodologically and does not modify.
7. FARO's dependency graph says FARA supplies representation and FAR supplies methodology.
8. Accepted framework-boundary and derivation records reject treating FAR procedures as FARA theorems or FARO operations as necessary consequences of FARA/FAR.
9. Canonicalization, CIR, evaluator controls, Pareto comparison, preregistration, and fail reporting are classified as methodology or governance choices rather than canonical theory.

## Candidate adjudication

| Candidate | Result | Reason |
|---|---|---|
| undifferentiated owner | Fail | Cannot preserve both shared-theory definition authority and FARA candidate classification; omits three candidate primitives from the semantic registry. |
| split authority | Pass at frozen Research scope | Directly reconstructs definition, classification, formalization, methodology, operation, protocol, and governance roles from accepted artifacts. |
| logical derivation of FAR/FARO | Fail | No accepted derivation proof is recorded; accepted boundary/derivation authority rejects the necessity claim. |
| artifact/workflow contract | Pass at frozen Research scope | Accepted dependency documents record use of FARA representations and FAR investigation context while preserving independent downstream procedural ownership. |
| unclassified dependency | Fail | Accepted sources determine a contractual, non-derivational relationship. |

## Research discovery

The source execution supports the Research finding:

`split_authority_and_artifact_contract_model_supported_at_frozen_repository_scope`

Proposed authority relations for replication are:

- canonical definition → shared theory;
- candidate-primitive classification → FARA;
- formal representation kernel → FARA;
- investigation methodology → FAR;
- operational interface → FARO;
- experiment protocol and decision rules → CRP/methodology;
- Acceptance, Promotion, and freezes → governance.

Proposed dependency kinds for replication are:

- FARA → FAR: representation-artifact contract;
- FARA → FARO: representation-artifact contract;
- FAR → FARO: investigation-artifact and workflow contract.

## Failures discovered

- The current undifferentiated owner model loses authority information.
- The current semantic candidate-primitive registry is incomplete relative to the accepted FARA primitive registry.
- No accepted proof supports downstream procedural derivation from FARA.

These failures are successful research outcomes. They justify a separate replication; they do not authorize immediate correction.

## Required next stage

A separate replication must:

1. use an implementation that does not import this Python executor;
2. consume the same hash-locked accepted sources or independently verify equivalent source identities;
3. reproduce or falsify every check, observation, candidate classification, failure, and nonclaim;
4. preserve the Research status of this result;
5. avoid canonical repository changes.

Only after successful replication may Acceptance be considered. Acceptance, Promotion, canonical repository change, experiment preregistration, and experiment execution remain prohibited.

## Nonclaims

This report does not establish an Accepted authority model, an Accepted dependency classification, a canonical repository correction, experiment preregistration authorization, experiment execution authorization, global universality, primitive necessity, primitive minimality, primitive independence, or external-investigator independence.
