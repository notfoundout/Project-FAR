# Primitive Necessity and Reintroduction Protocol v1.0

## Purpose

This protocol governs local necessity tests for FAR primitives and prevents an ablated primitive from being silently reintroduced under another name or in another implementation layer.

## Claim boundary

A successful ablation test may support local necessity only relative to the frozen vocabulary, source contract, alternative construction space, and anti-reintroduction audit. It does not establish global necessity across all possible vocabularies.

## Preregistration requirements

For each tested primitive, register:

- canonical definition;
- operational role;
- semantic commitments;
- known aliases and near-equivalents;
- allowed remaining primitives;
- forbidden derived replacements;
- permitted generic machinery;
- preservation dimensions expected to fail if the primitive is necessary;
- reconstruction procedures;
- evaluator and auditor independence;
- decision rule.

## Ablation procedure

1. Freeze the source-facing observation contract.
2. Freeze the full candidate vocabulary and semantics.
3. Remove the tested primitive from the supplied vocabulary.
4. Prohibit direct aliases and semantic equivalents identified in preregistration.
5. Require at least three isolated reconstruction attempts where feasible.
6. Preserve every attempt, including incomplete and divergent mappings.
7. Evaluate preservation and full representational cost.
8. Run the hidden-reintroduction audit.
9. Adjudicate without changing the frozen rules.
10. classify the result conservatively.

## Reintroduction audit layers

### Vocabulary layer

Inspect remaining primitive definitions for expansion that absorbs the removed function.

### Derived-machinery layer

Inspect helper constructs, macros, relations, state variables, and transition schemas for functional equivalence to the removed primitive.

### Metadata layer

Inspect annotations, identifiers, provenance fields, and configuration for encoded distinctions that should be unavailable after ablation.

### Compiler layer

Inspect parsing, normalization, lowering, code generation, and default behavior for implicit restoration of the removed capability.

### Verifier layer

Inspect validation rules and acceptance assumptions for reliance on the removed commitment.

### Runtime layer

Inspect hidden state, external libraries, interpreter conventions, environment variables, and human procedures.

### Adjudication layer

Inspect manual interpretations and exception policies for case-specific reconstruction of the missing primitive.

## Result classes

- **Necessary within tested space**: all valid reconstructions fail a protected preservation requirement, no hidden reintroduction is found, and the decision rule is met.
- **Not necessary within tested space**: at least one valid reconstruction preserves the contract without prohibited reintroduction and within preregistered cost limits.
- **Tradeoff**: reconstruction succeeds only with increased cost or reduced preservation not sufficient for either categorical result.
- **Reintroduced**: the primitive's function appears in a forbidden layer; the attempt is invalid for necessity testing.
- **Unknown**: evidence, audit coverage, or reconstruction competence is insufficient.

## Competence and independence

Reconstructors must be able to read formal specifications and state-transition systems. They must not see other reconstruction artifacts. Auditors should not be the authors of the mapping under audit where avoidable.

Multiple implementations by one agent establish only isolated implementation-path robustness, not human or organizational independence.

## Decision restrictions

- Failure by one reconstructor does not establish necessity.
- Success by one valid independent reconstruction defeats reproducible local necessity but may leave other questions open.
- Cost explosion must be reported as a tradeoff unless the preregistered rule defines it as failure.
- Unknown must not be converted to Fail.
- A post hoc alias prohibition creates a new protocol version.

## Required artifacts

```text
ablation/
  preregistration.md
  forbidden-equivalents.yaml
  reconstruction-01/
  reconstruction-02/
  reconstruction-03/
  reintroduction-audit.md
  adjudication-log.md
  result.json
```

## Nonclaims

This protocol does not by itself establish global primitive necessity, universal minimality, or uniqueness of FAR's decomposition.