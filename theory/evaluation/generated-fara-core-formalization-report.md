# FARA core formalization — generated report

**Terminal result:** multiple non-equivalent coherent formalizations remain
**Strongest established result:** the selected many-sorted specification is boundedly coherent under the frozen finite model class; three materially non-equivalent coherent foundations remain

## Authority and discrepancy
Authorized repository obligations: formalize canonical derivation and composition rules, resolve circular primitive definitions identified by W1. Repository authority records these as separate remaining obligations, not one designated next workstream; the prompt authorizes their combined execution. No W7 designation is used.

## Frozen target
finite typed first-order relational signature; model class: finite structures with each carrier cardinality 0..2, disjoint source/token/meaning carriers, typed total equality, partial interpretation, finite rules and transitions. Object language, metalanguage, source data, representation data, interpretation, operations, investigation context, and external dependencies are separated.

## Pre-formalization dependency graph
- `Object` → Representation
- `Property` → Object
- `Relation` → Object
- `Representation` → Object, Interpretation
- `Interpretation` → Representation
- `Investigation` → ReasoningCalculus
- `ReasoningCalculus` → Investigation

## Post-formalization dependency DAG
- `Object` → ∅
- `Property` → Object
- `Relation` → Object
- `Representation` → Object
- `Interpretation` → Representation
- `ReasoningCalculus` → ∅
- `Investigation` → ReasoningCalculus
- `SemanticContent` → Interpretation, Representation
- `Execution` → ReasoningCalculus
- `Result` → Execution

## Foundation comparison
- **many-sorted relational**: native disjoint carriers and typed finite relations; cost 14; failure: nonfinite and embodied behavior external.
- **typed hypergraph**: native typed nodes, ports, hyperedges; cost 19; failure: semantic composition requires extra path machinery.
- **algebraic state-transition**: native states, partial operations, transition algebra; cost 17; failure: source/representation distinction is non-native.

## W1 re-evaluation (new bounded target only)
| Candidate | Adjudication |
|---|---|
| Object | not derivable under the frozen bounded model class |
| Property | derivable under the frozen theory |
| Relation | not derivable under the frozen bounded model class |
| Representation | not derivable under the frozen bounded model class |
| Interpretation | not derivable under the frozen bounded model class |
| Investigation | derivable under the frozen theory |
| ReasoningCalculus | not derivable under the frozen bounded model class |

Original W1 remains unresolved and authoritative for its scope. Property and Investigation are derived only in this selected specification. Five paired reduct countermodels are bounded to carriers of size at most two.

## Conservativity, non-vacuity, and adversarial execution
Typed disjoint carriers are **nonconservative**; Property is conservative; Investigation and the complete prose comparison are unresolved. Catch-all payloads, opaque meanings, hidden decoders, whole-source constants, arbitrary higher-order predicates, and unconstrained candidate primitives are rejected. Twelve finite adversarial families pass the frozen checks; oracle-dependent and continuous/embodied cases are Unknown. All six preservation dimensions are recorded per model.

## Refuted and unresolved claims
Refuted: the formal target is conservative in every respect, the foundations are notational variants, all adversarial families are internal to the finite model class.
Unresolved: which foundation matches intended FARA, unbounded independence, complete prose conservativity, continuous, embodied and oracle semantics.

## Exact nonclaims
- canonical uniqueness
- primitive necessity
- global independence
- global minimality
- completeness
- universality

## Remaining obligations
- choose among non-equivalent coherent foundations by substantive evidence
- extend bounded derivability beyond cardinality two
- supply nonfinite continuous semantics
- supply environment-inclusive embodied semantics
- independently replicate model and countermodel executions
- prove conservativity against a formalization of the complete old prose theory
