# FARA vocabulary sufficiency and extension pressure — generated report

**Status:** extension pressure with boundedly irreducible candidate additions

Each family is executed with its full registered behavior and again under the frozen vocabulary. Preservation and recovery are computed from those paired executions.

| ID | Family | Recovery | Pressure |
|---|---|---|---|
| VOC-BENCH-001 | deterministic_transition | exact | none |
| VOC-BENCH-002 | probabilistic_update | failed | uncertainty |
| VOC-BENCH-003 | nonmonotonic_retraction | failed | retraction |
| VOC-BENCH-004 | paraconsistent_consequence | failed | consequence_policy |
| VOC-BENCH-005 | causal_intervention | failed | intervention |
| VOC-BENCH-006 | changing_rules | failed | rule_version |
| VOC-BENCH-007 | changing_semantics | failed | semantic_version |
| VOC-BENCH-008 | evolving_ontology | failed | identity_criterion |
| VOC-BENCH-009 | identity_preserving_merge | exact | identity_criterion |
| VOC-BENCH-010 | identity_collapsing_merge | failed | identity_criterion |
| VOC-BENCH-011 | deletion_constraint_relaxation | exact | none |
| VOC-BENCH-012 | provenance_history | failed | provenance |
| VOC-BENCH-013 | distributed_partial_order | failed | partial_order |
| VOC-BENCH-014 | oracle_behavior | unknown | oracle_relation |
| VOC-BENCH-015 | continuous_hybrid | unknown | uncertainty |
| VOC-BENCH-016 | embodied_tacit | unknown | external_coupling |
| VOC-BENCH-017 | proof_identity_binding | failed | proof_object |
| VOC-BENCH-018 | higher_order_scope | failed | binding_scope |
| VOC-BENCH-019 | normative_authority | failed | authority_source |

## Nonclaims
- universal sufficiency
- global minimality
- global primitive necessity
- finite ablation establishes necessity
- serialization establishes expression
- reconstruction establishes expressive sufficiency
- candidate extensions are globally primitive

## Remaining obligations
- formalize canonical derivation and composition rules
- replicate mappings independently
- test nonfinite continuous semantics
- adjudicate environment-inclusive embodied coupling
- prove or refute extension irreducibility beyond the frozen model
- resolve circular primitive definitions identified by W1
