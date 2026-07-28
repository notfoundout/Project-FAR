# FARA vocabulary sufficiency and extension pressure — generated report

**Status:** extension pressure with boundedly irreducible candidate additions  
**Authority:** UQ-T7: determine whether registered difficult systems can be represented without material expressive loss  
**Discrepancy:** Repository authority does not designate vocabulary sufficiency as FARA W6; this execution is unnumbered and addresses the closest authorized objective, UQ-T7.

The seven frozen candidate primitives are: Object, Property, Relation, Representation, Interpretation, Investigation, Reasoning Calculus. Coverage requires exposed operational structure; opaque serialization is rejected. All W0–W5 records remain unchanged.

## Executable mapping matrix
| ID | family | recovery | pressure |
|---|---|---|---|
| VOC-BENCH-001 | deterministic_transition | exact | none |
| VOC-BENCH-002 | probabilistic_update | failed | uncertainty |
| VOC-BENCH-003 | nonmonotonic_retraction | failed | retraction |
| VOC-BENCH-004 | paraconsistent_consequence | failed | consequence_policy |
| VOC-BENCH-005 | causal_intervention | failed | intervention |
| VOC-BENCH-006 | changing_rules | failed | rule_version |
| VOC-BENCH-007 | changing_semantics | failed | semantic_version |
| VOC-BENCH-008 | evolving_ontology | failed | identity_criterion |
| VOC-BENCH-009 | identity_preserving_merge | failed | identity_criterion |
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

## Extension ledger
| candidate | classification |
|---|---|
| temporal_order | derivable |
| uncertainty | boundedly irreducible under the frozen model |
| retraction | boundedly irreducible under the frozen model |
| consequence_policy | boundedly irreducible under the frozen model |
| intervention | boundedly irreducible under the frozen model |
| rule_version | boundedly irreducible under the frozen model |
| semantic_version | boundedly irreducible under the frozen model |
| identity_criterion | boundedly irreducible under the frozen model |
| provenance | boundedly irreducible under the frozen model |
| partial_order | boundedly irreducible under the frozen model |
| oracle_relation | external dependency |
| external_coupling | external dependency |
| proof_object | boundedly irreducible under the frozen model |
| binding_scope | boundedly irreducible under the frozen model |
| authority_source | boundedly irreducible under the frozen model |

All six preservation dimensions and structural-accounting totals are recorded per benchmark in the proof object. All seven escape-hatch mutations were rejected. Retained witnesses include intervention/correlation, proof/proposition identity, partial/total order, and decoder-held semantic-change collapses.

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
