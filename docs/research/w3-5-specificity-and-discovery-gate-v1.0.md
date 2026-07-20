# W3.5 Specificity and Universal-Discovery Gate v1.0

## Status

Frozen mandatory bridge after W3 and before W5 theorem assembly.

Identifier: `W3.5-SDG-001`.

## Purpose

W0–W3 record project-authored finite representation constructions. W3.5 determines how those constructions should be classified before the repository assembles the finite-core theorem.

W4 formal negative controls may proceed in parallel. W5 remains blocked until W3.5 is resolved with linked immutable result artifacts.

## Required investigations

### A. Generic-baseline factorization

Attempt to construct fixed translations:

\[
S_{core}\xrightarrow{E_G}GREL\text{-}001\xrightarrow{T_{GF}}FARA\text{-}WITNESS\text{-}1.0
\]

and, where defined,

\[
FARA\text{-}WITNESS\text{-}1.0\xrightarrow{T_{FG}}GREL\text{-}001.
\]

Record exact failures, extra constraints, helper machinery, and costs.

The result must be reported as a vector rather than a single scalar classification.

### B. Dimensioned FARA comparison

Report independently:

- expressiveness;
- translation direction;
- admissible-representation constraint strength;
- reasoning specificity;
- machinery and cost relation;
- overall interpretation.

Expressive equivalence may coexist with stronger FARA constraints, a cost tradeoff, and no demonstrated reasoning specificity.

### C. Concrete reasoning and contrast corpus

`RCS-001` currently freezes only the admission framework.

Before discrimination testing, W3.5 must freeze concrete positive and contrast instance registries with:

- stable instance identifiers and versions;
- independent admission decisions and rationales;
- source or observation contracts;
- formalization boundaries;
- candidate-exposure status;
- immutable corpus records.

Execution remains blocked while either corpus is empty.

### D. Reasoning discrimination

Execute the frozen concrete positive and contrast corpus against the candidate-invariant registry. Separate:

- general structured-system properties;
- representation properties;
- reasoning-relevant but nonuniversal properties;
- candidate universal invariants;
- unresolved cases.

### E. Ablation and reconstruction

For each candidate invariant:

1. remove or collapse it;
2. search for alternative reconstructions;
3. count equivalent reintroductions;
4. preserve failures and successful reductions;
5. classify the candidate.

Allowed classifications are:

- `indispensable_within_frozen_class`;
- `derivable`;
- `replaceable`;
- `architecture_dependent`;
- `scope_dependent`;
- `generic_system_property`;
- `unnecessary`;
- `unresolved`.

### F. Claim-impact audit

Update every central claim independently. Representation counts may not change universal-structure, necessity, minimality, or uniqueness status.

## Immutable result contract

Every required W3.5 result must have:

- a stable result identifier;
- a repository path;
- status `complete`;
- a SHA-256 content digest;
- explicit assumptions and scope;
- preserved failures and countermodels;
- explicit nonclaims.

A status string without linked evidence does not resolve W3.5.

## Exit criteria

W3.5 is resolved only when:

- every factorization dimension has a non-`unresolved` terminal value or an explicit failed-translation record;
- FARA-specificity has a terminal classification;
- the concrete positive and contrast corpora are frozen;
- positive/contrast execution is complete;
- the candidate-invariant distribution is recorded;
- machinery and cost accounting is complete;
- central-claim impact is recorded;
- every required result artifact satisfies the immutable result contract;
- countermodels and failures are preserved.

## W5 authorization

W5 may begin only when:

- `OBS-SC-010` has a terminal ledger status;
- `W3.5-SDG-001` has status `resolved`;
- the concrete reasoning and contrast corpus is frozen;
- all required W3.5 result artifacts exist and satisfy the immutable result contract;
- the factorization, specificity, corpus, and execution research gates are satisfied with evidence;
- `THM-TARGET-001` records no remaining W4 or W3.5 blocker;
- any change to the frozen representation theorem is versioned.

The separation checker must reject any attempt to set `w5_authorized` to true without these conditions.

## Nonclaims

Freezing W3.5 does not establish any factorization, specificity, discrimination, necessity, universal structure result, concrete corpus freeze, or W5 authorization.
