# S_core W5 Independent Proof Review Package v1.0

## Status

Frozen review package, effective on merge. Review has not been executed. This artifact prepares independent checking; it does not satisfy the independent-proof-review gate.

## Review target

**Theorem:** `THM-CORE-REP-001`

**Quantified statement:**

> For every `(P,J)` in the frozen class `S_core`, there exists a target object `A` in the fixed theorem-facing class `A_FARA` and a witness `W` such that `Faithful_split(P,J,A,W)`.

The accompanying W5 assembly also establishes `THM-CORE-COMMON-001` for `S_core` and refutes only the bounded `S_core` branch of `THM-IMP-001` under the frozen target.

## Frozen scope

`S_core` consists only of candidate-neutral IRD-001 presentations satisfying the registered finite-explicit requirements: finite event region, finite material carriers, explicit finite or finite-support dynamics, explicit grounds, material history and revision distinctions, declared source interpretation, and independent admission into scope.

The review must not silently widen this quantifier to all reasoning, all IRD systems, actual cognitive processes, or `S_IRD`.

## Artifact map

The reviewer must inspect the following as one dependency-ordered package:

1. theorem target and premise ledger;
2. faithful-representation and P8 split definitions;
3. construction-obstruction ledger;
4. W0 normalization;
5. W1 direct-axis preservation;
6. W2 dynamics, history, and revision preservation;
7. W3 uniform global witness;
8. W4 formal negative controls;
9. W3.5 corpus, factorization, specificity, machinery, claim-impact, and preserved-failure results;
10. W5 theorem assembly;
11. Lean mechanization and alignment checks.

The machine-readable registry lists the canonical paths and binds the two decisive W5 result registries by Git blob SHA.

## Questions the review must answer

### A. Scope and definitions

- Is `S_core` independently specified rather than selected because FARA can encode it?
- Does `A_FARA` remain fixed across all source objects?
- Are definitions, assumptions, and substantive axioms distinguishable?
- Is `Faithful_split` independent enough to test the target rather than restate the construction?

### B. Construction and preservation

- Is the constructor uniform and total over the declared source class?
- Are P1 configuration, P2 commitment, P3 stake/alternative, P4 ground/justification, P5 admissibility/dynamics, P6 consequence, P7 history/path, and P8I internal evidential status each preserved and reflected as claimed?
- Are cross-axis coherence and dependency identity preserved?
- Does the proof avoid unrestricted interpreters, lookup-table encodings, metadata smuggling, evaluator repair, or hidden source-specific decoders?

### C. Assembly

- Do the cited W0-W4 lemmas entail `ASM-SC-001` and `ASM-SC-002`?
- Does `ASM-SC-003` adjudicate the bounded theorem family without importing stronger conclusions?
- Are all premise and dependency references accurate?
- Is any material lemma used but not registered?

### D. Mechanization

- Does `mechanization/lean/SCoreW5.lean` formalize the same bounded theorem rather than a materially weaker surrogate?
- Are its source and target types faithful to the frozen paper definitions?
- Are theorem names and quantifiers aligned with the W5 registry?
- Are there `sorry`, new axioms, opaque admissions, or assumptions hidden by definitional construction?

Mechanization validates derivation inside the encoded definitions. It does not establish that those definitions completely capture the intended human theorem.

### E. Adversarial review

The reviewer must attempt, not merely consider:

1. an in-scope counterexample;
2. an unstated-axiom diagnosis;
3. a circularity attack on source admission or preservation;
4. a source-specific-decoder attack on uniformity;
5. a history, dependency, or evidential-status collapse;
6. a mismatch between the prose proof and Lean theorem;
7. a strictly simpler equivalent target construction.

A failed attack is recorded as failed, not omitted. A successful attack must include the smallest reproducible witness available.

## Reviewer eligibility

An eligible independent reviewer must:

- be able to read formal specifications and state-transition or reasoning-system models;
- have no authorship role in W0-W5 or the Lean mechanization;
- have no access to unpublished repair guidance;
- declare conflicts, prior Project FAR involvement, and communication with the project author;
- preserve all substantive objections, including objections later resolved.

Project-authored reruns, multiple assistant agents, isolated implementations, and CI do not satisfy this independence condition.

## Decision rule

The final review classification must be exactly one of:

- `verified`;
- `verified_with_errata`;
- `not_verified`;
- `inconclusive`.

`RG-15` remains `not_satisfied` until an eligible reviewer submits the complete review form, identifies the exact frozen package revision, and all blocking objections are resolved without changing the reviewed theorem package. A material theorem repair creates a new version; the original review result remains immutable.

## Claim boundary

Freezing this package supports only these claims:

- the bounded theorem is presented in a self-contained reviewable form;
- the human and mechanized artifacts can be independently inspected;
- adversarial review requirements and decision rules are fixed in advance.

It does not establish independent verification, independent replication, `S_IRD` representation, actual-process correspondence, necessity, minimality, uniqueness, reasoning specificity, or universal structure.
