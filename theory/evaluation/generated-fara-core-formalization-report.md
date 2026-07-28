# FARA core formalization — generated report

**Terminal result:** multiple non-equivalent coherent formalizations remain
**Strongest established result:** the selected many-sorted specification is boundedly coherent under the frozen finite model class; three formally specified coherent foundations have explicit non-equivalence witnesses

## Authority and discrepancy
Authorized repository obligations: formalize canonical derivation and composition rules, resolve circular primitive definitions identified by W1. Repository authority records these as separate remaining obligations, not one designated next workstream; the prompt authorizes their combined execution. No W7 designation is used.

## Frozen target
finite typed first-order relational signature; model class: finite structures with each carrier cardinality 0..2, disjoint source/token/meaning carriers, typed total equality, partial interpretation, finite rules and transitions.

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
- **many-sorted relational**: typed=True, coherent=True; witness: edge identity is extensional.
- **typed hypergraph**: typed=True, coherent=True; witness: parallel hyperedges remain distinct.
- **algebraic state-transition**: typed=True, coherent=True; witness: operation composition is primitive.

## W1 re-evaluation
| Candidate | Adjudication |
|---|---|
| Object | not derivable under the frozen bounded model class |
| Property | derivable under the frozen theory |
| Relation | not derivable under the frozen bounded model class |
| Representation | not derivable under the frozen bounded model class |
| Interpretation | not derivable under the frozen bounded model class |
| Investigation | derivable under the frozen theory |
| ReasoningCalculus | not derivable under the frozen bounded model class |

All five non-derivability records include machine-checkable paired models whose reducts agree after removing the target while their target interpretations differ.

## Executable adversarial models
12 finite families were constructed and executed with source models, results, and execution digests. 2 external/nonfinite families remain Unknown. No family receives Pass from its name alone.

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
