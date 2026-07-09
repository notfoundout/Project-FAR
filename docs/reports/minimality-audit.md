# Executive Summary

This Phase 1 Step 9 Minimality Audit is audit-only. It consumes the accepted foundation and prior audits without revalidating theorem proofs or introducing new mathematics. The audit covers 126 accepted artifacts: 5 primitives, 89 canonical definitions, AX-001, 8 lemmas, 8 propositions, and 15 theorems.

| Classification | Count |
|---|---:|
| Necessary | 112 |
| Derivable from accepted artifacts | 9 |
| Potentially redundant | 4 |
| Undetermined | 1 |

The final status is FOUNDATION MINIMALITY NOT YET ESTABLISHED because AX-001 remains a provisional primitive-candidate artifact; P-001, P-002, P-008, and T-007 are potential redundancies; and DEF-028, DEF-032, DEF-033, DEF-035, DEF-036, P-003, P-004, P-005, and P-006 are derivable artifacts whose retention may be justified by canonical naming and proof-complexity reduction rather than independent necessity. No artifact is removed, demoted, or rewritten.

# Primitive Minimality

| Artifact | Classification | Justification |
|---|---|---|
| Investigation | Necessary | Direct primitive of the current primitive architecture; removing it breaks the axiom/lemma/theorem chain that names the corresponding role, and T-001/T-002 currently support only conditional minimality and independence rather than a reduction. |
| Representation | Necessary | Direct primitive of the current primitive architecture; removing it breaks the axiom/lemma/theorem chain that names the corresponding role, and T-001/T-002 currently support only conditional minimality and independence rather than a reduction. |
| Representational Structure | Necessary | Direct primitive of the current primitive architecture; removing it breaks the axiom/lemma/theorem chain that names the corresponding role, and T-001/T-002 currently support only conditional minimality and independence rather than a reduction. |
| Interpretation | Necessary | Direct primitive of the current primitive architecture; removing it breaks the axiom/lemma/theorem chain that names the corresponding role, and T-001/T-002 currently support only conditional minimality and independence rather than a reduction. |
| Reasoning Calculus | Necessary | Direct primitive of the current primitive architecture; removing it breaks the axiom/lemma/theorem chain that names the corresponding role, and T-001/T-002 currently support only conditional minimality and independence rather than a reduction. |

# Definition Minimality

Canonical definitions are audited as accepted vocabulary artifacts. Definitions that merely unfold prior vocabulary are classified as derivable when their own metadata declares dependencies sufficient to reconstruct their role; they are still necessary as canonical terminology unless conclusive consolidation evidence exists.

| Artifact | Classification | Justification |
|---|---|---|
| DEF-001 — Object | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-002 — Property | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-003 — Relation | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-004 — Structure | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001, DEF-003. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-005 — Component | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001, DEF-004. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-006 — System | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001, DEF-004. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-007 — Class | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-008 — Domain | Necessary | Canonical vocabulary for foundational vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-009 — Model | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-010 — Framework | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-003. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-011 — Theory | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-008. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-012 — Architecture | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-001, DEF-003. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-013 — Ontology | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-014 — Syntax | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-015 — Semantics | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-030. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-016 — Scope | Necessary | Canonical vocabulary for framework vocabulary; declared dependencies: DEF-008. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-017 — Universal | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-008. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-018 — Universal Architecture | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-012, DEF-016. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-019 — Minimal | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-004, DEF-016. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-020 — Candidate Primitive | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-021 — Established Primitive | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-022 — Derived Concept | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-023 — Reduction | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-016. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-024 — Independence | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-025 — Equivalence | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-003. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-026 — Expressive Power | Necessary | Canonical vocabulary for formal vocabulary; declared dependencies: DEF-010, DEF-016. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-027 — Representation | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-001. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-028 — Represented Object | Derivable from accepted artifacts | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-001, DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-029 — Representational Structure | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-003, DEF-004, DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-030 — Interpretation | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-031 — Semantic Content | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-030. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-032 — Structural Equivalence | Derivable from accepted artifacts | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-025, DEF-029. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-033 — Semantic Equivalence | Derivable from accepted artifacts | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-025, DEF-030, DEF-031. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-034 — Representation Mapping | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-027, DEF-029. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-035 — Representation Transformation | Derivable from accepted artifacts | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-029, DEF-034. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-036 — Representation Invariance | Derivable from accepted artifacts | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-034. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-037 — Representation Fidelity | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-027, DEF-028, DEF-030. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-038 — Representation Completeness | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-027, DEF-016, DEF-030. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-039 — Representation Consistency | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-027, DEF-029. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-040 — Representational Independence | Necessary | Canonical vocabulary for representational vocabulary; declared dependencies: DEF-024, DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-041 — Investigation | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-042 — Investigation State | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-043 — Investigation Record | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-044 — Reasoning | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-045 — Reasoning Process | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-041, DEF-044. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-046 — Reasoning Calculus | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-047 — State | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-001, DEF-016. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-048 — Reasoning State | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-041, DEF-045, DEF-047. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-049 — Reasoning State Representation | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-048. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-050 — Reasoning State Record | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-049. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-051 — Transformation Rule | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-052 — Transformation Execution | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-045, DEF-051. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-053 — Transformation Result | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-052. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-054 — Transition Signature | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-027, DEF-049, DEF-052. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-055 — Reasoning Trace | Necessary | Canonical vocabulary for reasoning vocabulary; declared dependencies: DEF-045, DEF-054. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-056 — Candidate | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-001, DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-057 — Criterion | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-058 — Classification | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-001, DEF-057. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-059 — Admissibility | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-041, DEF-046, DEF-057. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-060 — Admissibility Classification | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-056, DEF-058, DEF-059. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-061 — Admissibility Structure (Ω) | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-041, DEF-060. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-062 — Resolution Rule | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-061. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-063 — Resolution Execution | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-061, DEF-062. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-064 — Resolution | Necessary | Canonical vocabulary for decision vocabulary; declared dependencies: DEF-056, DEF-063. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-065 — Definition | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-010. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-066 — Principle | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-067 — Axiom | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-068 — Proposition | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: none. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-069 — Conjecture | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-068. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-070 — Lemma | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-068. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-071 — Theorem | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-068, DEF-073. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-072 — Corollary | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-071. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-073 — Proof | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-046, DEF-068. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-074 — Refutation | Necessary | Canonical vocabulary for meta vocabulary; declared dependencies: DEF-068. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-075 — Claim | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-041, DEF-068. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-076 — Claim Type | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-077 — Evidence | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-027, DEF-041, DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-078 — Observation | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-079 — Assumption | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-041, DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-080 — Hypothesis | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-081 — Explanation | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-027, DEF-075, DEF-079. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-082 — Prediction | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-083 — Counterexample | Necessary | Canonical vocabulary for evidence vocabulary; declared dependencies: DEF-001, DEF-075. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-084 — Artifact | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-027. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-085 — Audit | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-084. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-086 — Grounding Investigation | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-041. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-087 — Knowledge Object | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-084. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-088 — Traceability | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-084. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |
| DEF-089 — Revision | Necessary | Canonical vocabulary for methodology vocabulary; declared dependencies: DEF-084. Removal would make repository references ambiguous even where the definition unfolds accepted vocabulary. |

# Axiom Minimality

| Artifact | Classification | Justification |
|---|---|---|
| AX-001 — Primitive Operation | Undetermined | Prior AX-001 evidence found no successful non-circular reduction but also records provisionality, circularity pressure, and open sufficiency questions. It remains accepted evidence, but minimality is not established conclusively. |

# Lemma Minimality

| Artifact | Classification | Justification |
|---|---|---|
| L-001 — Representation Necessity | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: A1, D-REP. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-002 — Structure Necessity | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: A2, D-STRUCT. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-003 — Interpretation Necessity | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: A3, D-INT. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-004 — Investigation Necessity | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: A4, D-INV. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-005 — Calculus Necessity | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: A5, D-CALC. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-006 — Canonical Role Pairing | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: D-REP, D-STRUCT, D-INT, D-CALC. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-007 — Finite Normalization Termination | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: D-REP, D-STRUCT, D-INT, D-CALC. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |
| L-008 — Transition Signature Construction | Necessary | Used directly or as accepted local bridge in the foundation; declared dependencies: D-REP, D-CALC. Removing it would force downstream proofs/audits to repeat the corresponding axiom or construction consequence. |

# Proposition Minimality

| Artifact | Classification | Justification |
|---|---|---|
| P-001 — Representation Requirement | Potentially redundant | Validation evidence notes close overlap with the corresponding necessity lemma/axiom consequence. It may reduce proof complexity, but independent necessity beyond the lemma-level artifact is not established. Declared dependencies: A1, D-REP. |
| P-002 — Structural Requirement | Potentially redundant | Validation evidence notes close overlap with the corresponding necessity lemma/axiom consequence. It may reduce proof complexity, but independent necessity beyond the lemma-level artifact is not established. Declared dependencies: A2, D-REP, D-STRUCT. |
| P-003 — Semantic Relativity | Derivable from accepted artifacts | Appears to unfold accepted definitions and axiomatic scope. It remains useful as a named bridge, but current evidence supports derivability rather than independent primitive necessity. Declared dependencies: D-REP, D-INT. |
| P-004 — Investigation Relativity | Derivable from accepted artifacts | Appears to unfold accepted definitions and axiomatic scope. It remains useful as a named bridge, but current evidence supports derivability rather than independent primitive necessity. Declared dependencies: D-INV, D-INT, D-CALC. |
| P-005 — Calculus Relativity of Admissibility | Derivable from accepted artifacts | Appears to unfold accepted definitions and axiomatic scope. It remains useful as a named bridge, but current evidence supports derivability rather than independent primitive necessity. Declared dependencies: D-CALC, D-INV. |
| P-006 — Syntax/Semantics Separation | Derivable from accepted artifacts | Depends on P-003 plus structure/interpretation definitions; its content appears derived from accepted syntax/semantics separation evidence. Declared dependencies: D-STRUCT, D-INT, P-003. |
| P-007 — Trace/Process Distinction | Necessary | Supplies accepted proposition-level bridge used by theorem proofs or audit evidence; removing it would increase proof complexity or break direct references. Declared dependencies: D-REP, D-STRUCT, D-CALC. |
| P-008 — Resolution Dependence | Potentially redundant | Resolution-dependence content appears close to reasoning-calculus and admissibility vocabulary; conclusive removal evidence is absent. Declared dependencies: D-CALC, D-STRUCT. |

# Theorem Minimality

| Artifact | Classification | Justification |
|---|---|---|
| T-001 — Conditional Primitive Minimality | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: L-001, L-002, L-003, L-004, L-005. |
| T-002 — Conditional Primitive Independence | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: T-001, L-001, L-002, L-003, L-004, L-005. |
| T-003 — Representation Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005. |
| T-004 — Semantic Preservation Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: DEF-030, DEF-031, DEF-034. |
| T-005 — Transition Completeness Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: D-CALC, L-008, T-003. |
| T-006 — Primitive Sufficiency Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: derived-concept-registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC. |
| T-007 — Primitive Completeness Theorem | Potentially redundant | T-015 validation classified T-007 as informative rather than logically required for T-015, while T-007 remains directly tied to primitive completeness. Necessity is plausible but not conclusively independent. Declared dependencies: T-003, T-006. |
| T-008 — Canonical Representation Equivalence | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: L-006, T-004. |
| T-009 — Canonical Normal Form Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: L-007. |
| T-010 — Reconstruction Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: T-003, T-004, P-007. |
| T-011 — Conservative Extension Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: T-006, definition-policy. |
| T-012 — FAR Model Equivalence Theorem | Necessary | Accepted as a definitional theorem over preservation profiles; necessary as the canonical model-equivalence boundary even though its proof is definition-unfolding. Declared dependencies: FAR-model-theory. |
| T-013 — Relative Soundness Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: D-CALC. |
| T-014 — Relative Completeness Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: D-CALC. |
| T-015 — Explicit Reasoning Meta-Theorem | Necessary | Accepted theorem supplies a named result used directly, transitively, or as a canonical boundary for the foundation. Declared dependencies: T-003, FAR-model-theory. |

# Candidate Redundancies

- P-001 may duplicate L-001/Axiom 1 representation-necessity content at proposition level; retention may still reduce proof complexity.
- P-002 may duplicate L-002/Axiom 2 structural-necessity content at proposition level; retention may still reduce proof complexity.
- P-008 may duplicate calculus/resolution-dependence vocabulary unless a downstream theorem requires the named proposition specifically.
- T-007 may be redundant for T-015 but not necessarily redundant for the foundation because it packages primitive completeness.
- DEF-028, DEF-032, DEF-033, DEF-035, and DEF-036 are derivable representational definitions that could be consolidation candidates only if references and theorem statements no longer need their names.

# Undetermined Cases

- AX-001 — Primitive Operation: accepted evidence supports retention but not conclusive minimality because prior reports preserve provisionality, unresolved circularity pressure, and open sufficiency questions.

# Remaining Research Questions

- Can AX-001 be shown non-circular and sufficient, or reduced, without changing accepted mathematics?
- Are P-001 and P-002 independently needed as proposition-level artifacts once L-001 and L-002 are accepted?
- Does P-008 have direct downstream use that cannot be handled by accepted definitions and D-CALC?
- Is T-007 independently necessary outside its role as primitive-completeness packaging?
- Should derivable representational definitions remain as canonical names for clarity even when their content unfolds from prior definitions?

# Final Minimality Status

Unresolved artifacts: AX-001, P-001, P-002, P-008, T-007, DEF-028, DEF-032, DEF-033, DEF-035, DEF-036, P-003, P-004, P-005, and P-006. AX-001 is undetermined; P-001, P-002, P-008, and T-007 are potentially redundant; and the listed definition/proposition artifacts are derivable or definition-unfolding artifacts whose retention has usefulness evidence but not conclusive independent-necessity evidence under the current audit-only standard. Phase 1 Step 10 should not begin until these unresolved minimality questions are accepted as non-blocking by human review or resolved by later evidence.

FOUNDATION MINIMALITY NOT YET ESTABLISHED
