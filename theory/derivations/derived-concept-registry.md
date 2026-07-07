# Derived Concept Registry

## Purpose

This registry lists current non-primitive Project FAR concepts and records how each derives from the primitive architecture.

The primitive architecture is:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

A concept is admissible as derived only if it can be constructed from primitives or previously registered derived concepts.

---

# Primitive Concepts

These are not derived in the current theory.

| ID | Concept |
|---|---|
| PR-001 | Investigation |
| PR-002 | Representation |
| PR-003 | Representational Structure |
| PR-004 | Interpretation |
| PR-005 | Reasoning Calculus |

---

# First-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-001 | Semantic Content | Interpretation applied to Representation within Investigation |
| D-002 | Representation Collection | Set or ordered collection of Representations |
| D-003 | Structural Relation | Relation specified by Representational Structure over Representations |
| D-004 | Reasoning State | Representation Collection plus applicable structure and interpretation within an Investigation |
| D-005 | Transformation Rule | Rule belonging to a Reasoning Calculus |
| D-006 | Admissibility | Satisfaction of criteria supplied by a Reasoning Calculus within an Investigation |
| D-007 | Candidate | Representation evaluated under an Investigation and Reasoning Calculus |
| D-008 | Resolution Rule | Rule in a Reasoning Calculus that selects, rejects, ranks, or terminates candidates |

---

# Second-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-009 | Transformation Execution | Application of D-005 to D-004 under PR-005 |
| D-010 | Transformation Result | Output of D-009 |
| D-011 | Transition Signature | Representation of D-009 between reasoning states |
| D-012 | Reasoning Trace | Ordered collection of D-011 |
| D-013 | Admissibility Structure | Structure over candidates and admissibility statuses |
| D-014 | Resolution Execution | Application of D-008 to D-013 |
| D-015 | Resolution | Result of D-014 |
| D-016 | Representation Mapping | Function from one Representation Collection or Structure to another |
| D-017 | Semantic Equivalence | Preservation of D-001 under mapping |
| D-018 | Structural Equivalence | Preservation of D-003 under mapping |

---

# Third-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-019 | FAR Representation | Tuple `<I, Rep, S, Int, C, T>` using primitives plus D-012 |
| D-020 | FAR Model | FAR structure satisfying Project FAR axioms |
| D-021 | Satisfaction | Relation between FAR Model and statement under Interpretation and Calculus |
| D-022 | Validity | Satisfaction across a specified class of FAR Models |
| D-023 | Model Equivalence | Preservation of selected properties across FAR Models |
| D-024 | Canonical Representation | FAR Representation after redundancy-removal and canonical labeling |
| D-025 | Normal Form | Canonical Representation under total ordering and canonical labels |
| D-026 | Conservative Extension | Extension that adds no new primitive and preserves canonical definitions, axioms, and theorem dependencies |

---

# Hard-Case Derived Concepts

These concepts were added after candidate-counterexample analysis in `theory/falsification/candidate-counterexample-analysis.md`.

| ID | Concept | Derivation |
|---|---|---|
| D-027 | Semantic Instability | Condition where D-021 cannot assign a stable status under a selected PR-004/PR-005 pair; derived from PR-004, PR-005, D-001, and D-021 |
| D-028 | Guarded Self-Reference | Self-reference represented as an explicit D-003 reference relation constrained by PR-005 to avoid unbounded collapse; derived from PR-002, PR-003, PR-005, and D-027 |
| D-029 | Paraconsistent Calculus | Reasoning Calculus policy permitting controlled inference from inconsistent representation sets without automatic explosion; derived from PR-005, D-003, D-004, and D-006 |
| D-030 | Non-Explosive Inference | Transformation rule or admissibility policy that blocks arbitrary conclusions from contradiction; derived from D-005, D-006, and D-029 |
| D-031 | Explicit-Reasoning Scope Boundary | Boundary condition requiring accessible representations, structures, interpretations, and calculus-governed transitions before FAR treats a process as explicit reasoning; derived from PR-001 through PR-005 and D-012 |
| D-032 | Opaque Assertion | Representation of a conclusion without accessible derivation, transition signature, or calculus-governed trace; derived from PR-002, D-012 absence, and D-031 |

---

# Expanded-Fixture Derived Concepts

These concepts were added after v0.3.0 expanded fixture analysis in `theory/evaluation/expanded-fixture-analysis.md`. They record recurring pressure points that appear across multiple reasoning systems while remaining constructible from the five primitives.

| ID | Concept | Definition | Derivation Path | Dependency Chain | Affected Reasoning Systems |
|---|---|---|---|---|---|
| D-033 | Indexed Interpretation | Interpretation policy that evaluates a representation relative to an explicit index such as world, time, path, context, degree, or model point. | PR-004 applied to PR-002 under PR-003 index relations within PR-001; admissibility and transitions remain governed by PR-005. | PR-002 → PR-003 → PR-004, with D-001 and D-021 when satisfaction is evaluated at an index. | Modal Logic; Temporal Logic; Deontic Logic; Intuitionistic Logic; Fuzzy Logic; Type Theory |
| D-034 | Constraint Transition System | Structured collection of constraints plus calculus-governed transformations that search, update, propagate, compose, or check admissible states. | PR-003 organizes constraint relations over PR-002 representations; PR-005 supplies transition rules; D-004, D-005, D-009, D-011, and D-012 record states and traces. | PR-002 → PR-003 → D-004; PR-005 → D-005 → D-009 → D-011 → D-012. | SAT Solving; Causal Reasoning; Type Theory; Theorem Provers; Category-Theoretic Reasoning |
| D-035 | Modalized Admissibility | Admissibility judgment whose status depends on an explicit mode, norm, construction state, accessibility relation, or valuation degree rather than a single unindexed truth status. | D-006 evaluated under D-033 and selected PR-005 rules; no new primitive is added because the variation is carried by interpretation indices and calculus criteria. | D-033 → D-006, with PR-005 and D-021 for satisfaction-relative status. | Modal Logic; Temporal Logic; Deontic Logic; Intuitionistic Logic; Fuzzy Logic |

# Hard-Case Analysis Links

| Hard Case | Registry Concepts | Analysis Result |
|---|---|---|
| Paradoxical reasoning | D-027, D-028 | Conservative extension: requires semantic-instability handling, not a new primitive |
| Inconsistent calculus | D-029, D-030 | Conservative extension: contradiction handling is calculus policy |
| Opaque oracle reasoning | D-031, D-032 | Outside FAR scope unless hidden transitions become explicit |

---

# Registry Rule

A theorem may claim primitive sufficiency only for concepts listed in this registry or for concepts added later with an explicit derivation path.

If a term appears in Project FAR but does not appear in this registry, one of three actions is required:

1. add it as a derived concept with a valid derivation;
2. mark it as informal and non-canonical;
3. treat it as evidence that the primitive architecture may be incomplete.

---

# Current Sufficiency Result

The current registry supports T-006 for D-001 through D-035.

T-006 should not be read as covering unregistered future concepts.
