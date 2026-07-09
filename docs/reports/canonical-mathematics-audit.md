# Executive Summary

This Phase 1 Step 4 audit classifies canonical mathematical artifacts without validating new mathematics. The audit found 129 accepted artifacts, 14 experimental artifacts, and 0 deprecated artifacts. Duplicate canonical identifiers found: 0. Repairs performed: none; no catalog inconsistency was repaired because the only material ambiguity is the known report-based AX-001 versus A1-A5 axiom-registration split, which requires a future canonicalization decision rather than an audit-only repair.

# Canonical Mathematics Inventory

| Identifier | Title | Artifact Type | Current Canonical Location | Current Status | Validation Status | Dependencies | Canonical Reference |
|---|---|---|---|---|---|---|---|
| A1 | Explicit Representation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A2 | Representational Organization | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP, D-STRUCT | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A3 | Interpretation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP, D-INT, D-INV | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A4 | Investigation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-INV | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A5 | Reasoning Calculus | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-CALC | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| AX-001 | Primitive Operation Foundation Evidence | Axiom | `docs/reports/ax001-validation-report.md; docs/reports/ax001-stability-review.md; docs/reports/ax001-wording-revision-report.md` | Accepted | Accepted by Phase 1 Step 3 evidence | None | `docs/reports/ax001-validation-report.md`; `docs/reports/ax001-stability-review.md`; `docs/reports/ax001-wording-revision-report.md` |
| DEF-001 | Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-002 | Property | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-003 | Relation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-004 | Structure | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-005 | Component | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-004 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-006 | System | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-004 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-007 | Class | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-008 | Domain | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-009 | Model | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-010 | Framework | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-011 | Theory | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-012 | Architecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-013 | Ontology | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-014 | Syntax | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-015 | Semantics | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-016 | Scope | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-017 | Universal | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-018 | Universal Architecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-012, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-019 | Minimal | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-004, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-020 | Candidate Primitive | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-021 | Established Primitive | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-022 | Derived Concept | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-023 | Reduction | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-024 | Independence | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-025 | Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-026 | Expressive Power | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-010, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-027 | Representation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-028 | Represented Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-029 | Representational Structure | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003, DEF-004, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-030 | Interpretation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-031 | Semantic Content | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-032 | Structural Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-025, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-033 | Semantic Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-025, DEF-030, DEF-031 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-034 | Representation Mapping | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-035 | Representation Transformation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-029, DEF-034 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-036 | Representation Invariance | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-034 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-037 | Representation Fidelity | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-028, DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-038 | Representation Completeness | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-016, DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-039 | Representation Consistency | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-040 | Representational Independence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-024, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-041 | Investigation | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-042 | Investigation State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-043 | Investigation Record | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-044 | Reasoning | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-045 | Reasoning Process | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-044 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-046 | Reasoning Calculus | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-047 | State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-048 | Reasoning State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-045, DEF-047 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-049 | Reasoning State Representation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-048 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-050 | Reasoning State Record | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-049 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-051 | Transformation Rule | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-052 | Transformation Execution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-045, DEF-051 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-053 | Transformation Result | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-052 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-054 | Transition Signature | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-049, DEF-052 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-055 | Reasoning Trace | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-045, DEF-054 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-056 | Candidate | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-057 | Criterion | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-058 | Classification | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-057 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-059 | Admissibility | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-046, DEF-057 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-060 | Admissibility Classification | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-056, DEF-058, DEF-059 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-061 | Admissibility Structure (Ω) | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-060 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-062 | Resolution Rule | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-061 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-063 | Resolution Execution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-061, DEF-062 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-064 | Resolution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-056, DEF-063 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-065 | Definition | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-010 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-066 | Principle | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-067 | Axiom | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-068 | Proposition | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-069 | Conjecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-070 | Lemma | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-071 | Theorem | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068, DEF-073 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-072 | Corollary | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-071 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-073 | Proof | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-046, DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-074 | Refutation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-075 | Claim | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-076 | Claim Type | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-077 | Evidence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-078 | Observation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-079 | Assumption | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-080 | Hypothesis | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-081 | Explanation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-075, DEF-079 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-082 | Prediction | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-083 | Counterexample | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-084 | Artifact | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-085 | Audit | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-086 | Grounding Investigation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-087 | Knowledge Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-088 | Traceability | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-089 | Revision | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DOC-FCA | Foundation Consistency Audit | Canonical Doctrine with mathematical force | `docs/reports/foundation-consistency-audit.md` | Accepted | Accepted by Phase 1 Step 3 evidence | Accepted foundation evidence | `docs/reports/foundation-consistency-audit.md` |
| DOC-ISO | Isolation Classification Doctrine | Canonical Doctrine with mathematical force | `docs/doctrine/isolation-classification.md` | Accepted | Accepted by Phase 1 Step 3 evidence | Accepted foundation evidence | `docs/doctrine/isolation-classification.md` |
| L-001 | Representation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A1, D-REP | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-002 | Structure Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A2, D-STRUCT | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-003 | Interpretation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A3, D-INT | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-004 | Investigation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A4, D-INV | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-005 | Calculus Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A5, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-006 | Canonical Role Pairing | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-007 | Finite Normalization Termination | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-008 | Transition Signature Construction | Lemma | `theory/lemmas/core-lemmas.md` | Experimental | Established | D-REP, D-STRUCT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| P-001 | Representation Requirement | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | A1, D-REP | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-002 | Structural Requirement | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | A2, D-REP, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-003 | Semantic Relativity | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-REP, D-INT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-004 | Investigation Relativity | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-INV, D-INT, D-CALC | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-005 | Calculus Relativity of Admissibility | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-CALC, D-INV | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-006 | Syntax/Semantics Separation | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-STRUCT, D-INT, P-003 | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-007 | Trace/Process Distinction | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-REP, D-STRUCT, D-CALC | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-008 | Resolution Dependence | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-CALC, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-009 | Representation Structure Independence | Proposition | `theory/theorems/propositions.md` | Experimental | Proposed | T-002, D-REP, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/theorems/propositions.md` |
| PRIM-INTERPRETATION | Interpretation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-INVESTIGATION | Investigation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REASONING-CALCULUS | Reasoning Calculus | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REPRESENTATION | Representation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REPRESENTATIONAL-STRUCTURE | Representational Structure | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| RULE-001 | definition_unfolding | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-002 | axiom_application | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-003 | prior_theorem | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-004 | lemma_application | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-005 | conjunction_intro | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-006 | universal_instantiation | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-007 | semantic_preservation | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-008 | registry_substitution | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-009 | modus_ponens | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| T-001 | Conditional Primitive Minimality | Theorem | `theory/proofs/T-001-primitive-minimality.md` | Accepted | Established | L-001, L-002, L-003, L-004, L-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-001-primitive-minimality.md` |
| T-002 | Conditional Primitive Independence | Theorem | `theory/proofs/T-002-primitive-independence.md` | Accepted | Established | T-001, L-001, L-002, L-003, L-004, L-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-002-primitive-independence.md` |
| T-003 | Representation Theorem | Theorem | `theory/proofs/T-003-representation-theorem.md` | Accepted | Established | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-003-representation-theorem.md` |
| T-004 | Semantic Preservation Theorem | Theorem | `theory/proofs/T-004-semantic-preservation.md` | Accepted | Established | DEF-030, DEF-031, DEF-034 | `theory/metadata/theorems.yaml`; `theory/proofs/T-004-semantic-preservation.md` |
| T-005 | Transition Completeness Theorem | Theorem | `theory/proofs/T-005-transition-completeness.md` | Accepted | Established | D-CALC, L-008, T-003 | `theory/metadata/theorems.yaml`; `theory/proofs/T-005-transition-completeness.md` |
| T-006 | Primitive Sufficiency Theorem | Theorem | `theory/proofs/T-006-primitive-sufficiency.md` | Accepted | Established | derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/theorems.yaml`; `theory/proofs/T-006-primitive-sufficiency.md` |
| T-007 | Primitive Completeness Theorem | Theorem | `theory/proofs/T-007-primitive-completeness.md` | Accepted | Established | T-003, T-006 | `theory/metadata/theorems.yaml`; `theory/proofs/T-007-primitive-completeness.md` |
| T-008 | Canonical Representation Equivalence | Theorem | `theory/proofs/T-008-canonical-representation-equivalence.md` | Accepted | Established | L-006, T-004 | `theory/metadata/theorems.yaml`; `theory/proofs/T-008-canonical-representation-equivalence.md` |
| T-009 | Canonical Normal Form Theorem | Theorem | `theory/proofs/T-009-canonical-normal-form.md` | Accepted | Established | L-007 | `theory/metadata/theorems.yaml`; `theory/proofs/T-009-canonical-normal-form.md` |
| T-010 | Reconstruction Theorem | Theorem | `theory/proofs/T-010-reconstruction-theorem.md` | Accepted | Established | T-003, T-004, P-007 | `theory/metadata/theorems.yaml`; `theory/proofs/T-010-reconstruction-theorem.md` |
| T-011 | Conservative Extension Theorem | Theorem | `theory/proofs/T-011-conservative-extension.md` | Accepted | Established | T-006, definition-policy | `theory/metadata/theorems.yaml`; `theory/proofs/T-011-conservative-extension.md` |
| T-012 | FAR Model Equivalence Theorem | Theorem | `theory/proofs/T-012-model-equivalence.md` | Accepted | Established | FAR-model-theory | `theory/metadata/theorems.yaml`; `theory/proofs/T-012-model-equivalence.md` |
| T-013 | Relative Soundness Theorem | Theorem | `theory/proofs/T-013-soundness.md` | Experimental | Established | D-CALC, T-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-013-soundness.md` |
| T-014 | Relative Completeness Theorem | Theorem | `theory/proofs/T-014-relative-completeness.md` | Experimental | Established | D-CALC, T-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-014-relative-completeness.md` |
| T-015 | Explicit Reasoning Meta-Theorem | Theorem | `theory/proofs/T-015-explicit-reasoning-meta-theorem.md` | Experimental | Established | T-003, T-007, FAR-model-theory | `theory/metadata/theorems.yaml`; `theory/proofs/T-015-explicit-reasoning-meta-theorem.md` |

# Accepted Artifacts

| Identifier | Title | Artifact Type | Current Canonical Location | Current Status | Validation Status | Dependencies | Canonical Reference |
|---|---|---|---|---|---|---|---|
| A1 | Explicit Representation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A2 | Representational Organization | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP, D-STRUCT | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A3 | Interpretation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-REP, D-INT, D-INV | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A4 | Investigation | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-INV | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| A5 | Reasoning Calculus | Axiom | `theory/axioms/axioms.md` | Accepted | Established | D-CALC | `theory/metadata/axioms.yaml`; `theory/axioms/axioms.md` |
| AX-001 | Primitive Operation Foundation Evidence | Axiom | `docs/reports/ax001-validation-report.md; docs/reports/ax001-stability-review.md; docs/reports/ax001-wording-revision-report.md` | Accepted | Accepted by Phase 1 Step 3 evidence | None | `docs/reports/ax001-validation-report.md`; `docs/reports/ax001-stability-review.md`; `docs/reports/ax001-wording-revision-report.md` |
| DEF-001 | Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-002 | Property | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-003 | Relation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-004 | Structure | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-005 | Component | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-004 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-006 | System | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-004 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-007 | Class | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-008 | Domain | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-009 | Model | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-010 | Framework | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-011 | Theory | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-012 | Architecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-013 | Ontology | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-014 | Syntax | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-015 | Semantics | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-016 | Scope | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-017 | Universal | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-008 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-018 | Universal Architecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-012, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-019 | Minimal | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-004, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-020 | Candidate Primitive | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-021 | Established Primitive | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-022 | Derived Concept | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-023 | Reduction | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-024 | Independence | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-025 | Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-026 | Expressive Power | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-010, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-027 | Representation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-028 | Represented Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-029 | Representational Structure | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-003, DEF-004, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-030 | Interpretation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-031 | Semantic Content | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-032 | Structural Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-025, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-033 | Semantic Equivalence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-025, DEF-030, DEF-031 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-034 | Representation Mapping | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-035 | Representation Transformation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-029, DEF-034 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-036 | Representation Invariance | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-034 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-037 | Representation Fidelity | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-028, DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-038 | Representation Completeness | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-016, DEF-030 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-039 | Representation Consistency | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-029 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-040 | Representational Independence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-024, DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-041 | Investigation | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-042 | Investigation State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-043 | Investigation Record | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-044 | Reasoning | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-045 | Reasoning Process | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-044 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-046 | Reasoning Calculus | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-047 | State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-016 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-048 | Reasoning State | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-045, DEF-047 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-049 | Reasoning State Representation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-048 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-050 | Reasoning State Record | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-049 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-051 | Transformation Rule | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-052 | Transformation Execution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-045, DEF-051 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-053 | Transformation Result | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-052 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-054 | Transition Signature | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-049, DEF-052 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-055 | Reasoning Trace | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-045, DEF-054 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-056 | Candidate | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-057 | Criterion | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-058 | Classification | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-057 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-059 | Admissibility | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-046, DEF-057 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-060 | Admissibility Classification | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-056, DEF-058, DEF-059 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-061 | Admissibility Structure (Ω) | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-060 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-062 | Resolution Rule | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-061 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-063 | Resolution Execution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-061, DEF-062 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-064 | Resolution | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-056, DEF-063 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-065 | Definition | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-010 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-066 | Principle | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-067 | Axiom | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-068 | Proposition | Definition | `theory/definitions/definitions.md` | Accepted | Established | None | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-069 | Conjecture | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-070 | Lemma | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-071 | Theorem | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068, DEF-073 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-072 | Corollary | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-071 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-073 | Proof | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-046, DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-074 | Refutation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-075 | Claim | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-068 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-076 | Claim Type | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-077 | Evidence | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-041, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-078 | Observation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-079 | Assumption | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-080 | Hypothesis | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-081 | Explanation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027, DEF-075, DEF-079 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-082 | Prediction | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-083 | Counterexample | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-001, DEF-075 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-084 | Artifact | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-027 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-085 | Audit | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-086 | Grounding Investigation | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-041 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-087 | Knowledge Object | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-088 | Traceability | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DEF-089 | Revision | Definition | `theory/definitions/definitions.md` | Accepted | Established | DEF-084 | `theory/metadata/definitions.yaml`; `theory/definitions/definitions.md` |
| DOC-FCA | Foundation Consistency Audit | Canonical Doctrine with mathematical force | `docs/reports/foundation-consistency-audit.md` | Accepted | Accepted by Phase 1 Step 3 evidence | Accepted foundation evidence | `docs/reports/foundation-consistency-audit.md` |
| DOC-ISO | Isolation Classification Doctrine | Canonical Doctrine with mathematical force | `docs/doctrine/isolation-classification.md` | Accepted | Accepted by Phase 1 Step 3 evidence | Accepted foundation evidence | `docs/doctrine/isolation-classification.md` |
| L-001 | Representation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A1, D-REP | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-002 | Structure Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A2, D-STRUCT | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-003 | Interpretation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A3, D-INT | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-004 | Investigation Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A4, D-INV | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-005 | Calculus Necessity | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | A5, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-006 | Canonical Role Pairing | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| L-007 | Finite Normalization Termination | Lemma | `theory/lemmas/core-lemmas.md` | Accepted | Established | D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| P-001 | Representation Requirement | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | A1, D-REP | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-002 | Structural Requirement | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | A2, D-REP, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-003 | Semantic Relativity | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-REP, D-INT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-004 | Investigation Relativity | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-INV, D-INT, D-CALC | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-005 | Calculus Relativity of Admissibility | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-CALC, D-INV | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-006 | Syntax/Semantics Separation | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-STRUCT, D-INT, P-003 | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-007 | Trace/Process Distinction | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-REP, D-STRUCT, D-CALC | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| P-008 | Resolution Dependence | Proposition | `theory/proofs/P-001-first-propositions.md` | Accepted | Established | D-CALC, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/proofs/P-001-first-propositions.md` |
| PRIM-INTERPRETATION | Interpretation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-INVESTIGATION | Investigation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REASONING-CALCULUS | Reasoning Calculus | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REPRESENTATION | Representation | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| PRIM-REPRESENTATIONAL-STRUCTURE | Representational Structure | Primitive | `theory/axioms/axioms.md` | Accepted | Canonical primitive architecture | None | `theory/axioms/axioms.md` |
| T-001 | Conditional Primitive Minimality | Theorem | `theory/proofs/T-001-primitive-minimality.md` | Accepted | Established | L-001, L-002, L-003, L-004, L-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-001-primitive-minimality.md` |
| T-002 | Conditional Primitive Independence | Theorem | `theory/proofs/T-002-primitive-independence.md` | Accepted | Established | T-001, L-001, L-002, L-003, L-004, L-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-002-primitive-independence.md` |
| T-003 | Representation Theorem | Theorem | `theory/proofs/T-003-representation-theorem.md` | Accepted | Established | A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-003-representation-theorem.md` |
| T-004 | Semantic Preservation Theorem | Theorem | `theory/proofs/T-004-semantic-preservation.md` | Accepted | Established | DEF-030, DEF-031, DEF-034 | `theory/metadata/theorems.yaml`; `theory/proofs/T-004-semantic-preservation.md` |
| T-005 | Transition Completeness Theorem | Theorem | `theory/proofs/T-005-transition-completeness.md` | Accepted | Established | D-CALC, L-008, T-003 | `theory/metadata/theorems.yaml`; `theory/proofs/T-005-transition-completeness.md` |
| T-006 | Primitive Sufficiency Theorem | Theorem | `theory/proofs/T-006-primitive-sufficiency.md` | Accepted | Established | derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC | `theory/metadata/theorems.yaml`; `theory/proofs/T-006-primitive-sufficiency.md` |
| T-007 | Primitive Completeness Theorem | Theorem | `theory/proofs/T-007-primitive-completeness.md` | Accepted | Established | T-003, T-006 | `theory/metadata/theorems.yaml`; `theory/proofs/T-007-primitive-completeness.md` |
| T-008 | Canonical Representation Equivalence | Theorem | `theory/proofs/T-008-canonical-representation-equivalence.md` | Accepted | Established | L-006, T-004 | `theory/metadata/theorems.yaml`; `theory/proofs/T-008-canonical-representation-equivalence.md` |
| T-009 | Canonical Normal Form Theorem | Theorem | `theory/proofs/T-009-canonical-normal-form.md` | Accepted | Established | L-007 | `theory/metadata/theorems.yaml`; `theory/proofs/T-009-canonical-normal-form.md` |
| T-010 | Reconstruction Theorem | Theorem | `theory/proofs/T-010-reconstruction-theorem.md` | Accepted | Established | T-003, T-004, P-007 | `theory/metadata/theorems.yaml`; `theory/proofs/T-010-reconstruction-theorem.md` |
| T-011 | Conservative Extension Theorem | Theorem | `theory/proofs/T-011-conservative-extension.md` | Accepted | Established | T-006, definition-policy | `theory/metadata/theorems.yaml`; `theory/proofs/T-011-conservative-extension.md` |
| T-012 | FAR Model Equivalence Theorem | Theorem | `theory/proofs/T-012-model-equivalence.md` | Accepted | Established | FAR-model-theory | `theory/metadata/theorems.yaml`; `theory/proofs/T-012-model-equivalence.md` |

# Experimental Artifacts

| Identifier | Title | Artifact Type | Current Canonical Location | Current Status | Validation Status | Dependencies | Canonical Reference |
|---|---|---|---|---|---|---|---|
| L-008 | Transition Signature Construction | Lemma | `theory/lemmas/core-lemmas.md` | Experimental | Established | D-REP, D-STRUCT, D-CALC | `theory/metadata/lemmas.yaml`; `theory/lemmas/core-lemmas.md` |
| P-009 | Representation Structure Independence | Proposition | `theory/theorems/propositions.md` | Experimental | Proposed | T-002, D-REP, D-STRUCT | `theory/metadata/propositions.yaml`; `theory/theorems/propositions.md` |
| RULE-001 | definition_unfolding | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-002 | axiom_application | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-003 | prior_theorem | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-004 | lemma_application | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-005 | conjunction_intro | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-006 | universal_instantiation | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-007 | semantic_preservation | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-008 | registry_substitution | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| RULE-009 | modus_ponens | Rule | `theory/proof-objects/proof-step-rules.md` | Experimental | Canonical rule pattern; proof-object subsystem status Provisional | Proof object validation context | `theory/proof-objects/proof-step-rules.md` |
| T-013 | Relative Soundness Theorem | Theorem | `theory/proofs/T-013-soundness.md` | Experimental | Established | D-CALC, T-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-013-soundness.md` |
| T-014 | Relative Completeness Theorem | Theorem | `theory/proofs/T-014-relative-completeness.md` | Experimental | Established | D-CALC, T-005 | `theory/metadata/theorems.yaml`; `theory/proofs/T-014-relative-completeness.md` |
| T-015 | Explicit Reasoning Meta-Theorem | Theorem | `theory/proofs/T-015-explicit-reasoning-meta-theorem.md` | Experimental | Established | T-003, T-007, FAR-model-theory | `theory/metadata/theorems.yaml`; `theory/proofs/T-015-explicit-reasoning-meta-theorem.md` |

# Deprecated Artifacts

No deprecated canonical mathematical artifacts were identified in the audited inventory.

# Duplicate Identifier Audit

No duplicate canonical identifiers were found within the compiled inventory. The audit also found no identifier collision among machine-readable metadata files for axioms, definitions, lemmas, propositions, and theorems.

# Canonical Reference Audit

Accepted definitions, A1-A5 axioms, L-001 through L-007, P-001 through P-008, and T-001 through T-012 appear in the generated canonical metadata indexes. Accepted theorem entries T-001 through T-012 each have a registered proof path, and the corresponding proof files exist. No accepted proof file lacking a corresponding accepted theorem was identified for T-001 through T-012.

The accepted AX-001 primitive-operation foundation is canonical by report evidence rather than by a single `theory/metadata/axioms.yaml` entry named `AX-001`; this ambiguity was already recorded by the Foundation Consistency Audit and remains unresolved by this audit-only PR.

# Repairs Performed

No repairs were performed.

# Remaining Issues

1. `AX-001` remains report-based and is not registered as a single machine-readable axiom metadata item. The existing machine-readable axiom registry uses `A1` through `A5`.
2. `L-008`, `P-009`, `T-013`, `T-014`, `T-015`, and proof-step rules are classified as Experimental for this audit because they are outside the accepted Phase 1 Step 4 foundation set even where local metadata says `Established`.
3. No deprecated mathematical artifacts were identified; therefore no deprecated artifact reference check can be completed beyond reporting zero deprecated inventory items.

# Final Canonical Mathematics Status

CANONICAL MATHEMATICS INCOMPLETE
