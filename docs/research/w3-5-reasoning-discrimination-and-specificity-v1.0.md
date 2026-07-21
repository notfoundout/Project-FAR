# W3.5 Reasoning Discrimination and FARA Specificity v1.0

## Status

This artifact records the project-authored execution of the frozen `RCS-CORPUS-001` reasoning/contrast comparison after completion of `W35-GREL-FARA-FACTOR-001`.

The execution is complete at the registered finite-corpus scope. It does **not** resolve all of `W3.5-SDG-001`, authorize W5, establish a universal definition of reasoning, or establish that FARA primitives are necessary.

## Experimental separation

Two questions are kept distinct.

1. **Reasoning discrimination:** can a fixed role-conjunctive predicate separate the eight frozen positive admissions from the eight frozen contrast admissions while leaving the two disputed records unresolved?
2. **FARA specificity:** is that discriminative capacity unique to FARA rather than available on the candidate-neutral source or through `GREL-001`?

A positive answer to the first question does not imply a positive answer to the second.

## Frozen licensing criteria

`W35-REASONING-LICENSING-001` registers seven criteria:

| ID | Criterion |
|---|---|
| R1 | problem-relative objective |
| R2 | live alternative or commitment |
| R3 | grounds-to-outcome dependency |
| R4 | admissibility or entitlement beyond arbitrary transition |
| R5 | consequence-sensitive transformation |
| R6 | interpreted content |
| R7 | auditable entitlement trace |

The decision rule is:

- `reasoning_like` only when all seven criteria pass;
- `nonreasoning_like` when at least two of R2, R3, R4, R5, and R7 fail;
- `borderline` for every other resolved profile;
- `unknown` when any criterion is unknown.

The two disputed records are excluded from the primary sensitivity and specificity calculation.

## Label isolation

Runtime scoring receives only:

- the candidate-neutral authoritative projection;
- the frozen licensing entry.

It does not receive the admission class, family, title, admission rationale, candidate-exposure status, or an expected result. All 18 scores are computed before admission labels are joined for evaluation.

The implementation mutates admission metadata and requires the criterion vector and decision to remain identical.

## Important limitation

The semantic licensing itself is project-authored after the corpus was frozen. It is not an independent, evaluator-blind, or private-holdout evaluation. This protects runtime scoring against direct label leakage but does not eliminate author expectancy or semantic-coding bias.

## Registered result

| Admission class | reasoning-like | nonreasoning-like | borderline | unknown |
|---|---:|---:|---:|---:|
| Positive | 8 | 0 | 0 | 0 |
| Contrast | 0 | 8 | 0 | 0 |
| Disputed | 0 | 0 | 2 | 0 |

At the registered positive/contrast scope:

- positive sensitivity: `1.0`;
- contrast specificity: `1.0`;
- balanced accuracy: `1.0`;
- statistical inference: not authorized.

The perfect registered result is descriptive only. The corpus is finite, synthetic, authored by the project, and not a sample from a defined population.

## Representation transport

The criterion inputs are present in the candidate-neutral source projection. Exact `GREL-001` recovery preserves those inputs and therefore preserves the criterion vector. The FARA-oriented compilation maps the same licensed roles into directly addressable axes.

Consequently:

- bounded role-conjunctive discrimination is established on `RCS-CORPUS-001`;
- FARA role directness is supported;
- FARA's stricter admissibility and audit schema remains supported by the factorization result;
- unique discriminative capacity of FARA is **refuted at the registered scope**;
- FARA primitive necessity and general reasoning specificity remain unestablished.

The terminal registered classification is:

`fara_role_directness_without_unique_discriminative_capacity`

## Preserved disputed cases

`RCS-DIS-001` remains borderline because it compares action values but excludes training, model construction, and online revision.

`RCS-DIS-002` remains borderline because it performs grounded, admissibility-sensitive constraint propagation but lacks explicit hypothesis comparison and an explicit explanation object.

Neither record is coerced into a positive or contrast class.

## Gate effect

This package satisfies, with linked evidence:

- `reasoning-contrast-execution`;
- `fara-specificity-resolved`.

The specificity gate is satisfied by a qualified negative result, not by establishing FARA uniqueness.

`W3.5-SDG-001` advances only to `in_progress_specificity_complete`.

The following remain unexecuted:

- universal-structure candidate scoring;
- candidate ablation and reconstruction;
- complete machinery and cost accounting;
- central claim-impact closure;
- preserved-failure package closure.

W5 remains unauthorized.

## Canonical artifacts

- `theory/evaluation/w3-5-reasoning-licensing-v1.0.json`
- `theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json`
- `theory/evaluation/w3-5-fara-specificity-result-v1.0.json`
- `tools/w3_5_specificity.py`
- `tools/check_w3_5_specificity.py`
- `tests/test_w3_5_specificity.py`

## Nonclaims

This result does not establish:

- a universal or exhaustive definition of reasoning;
- population-level accuracy;
- independent or blind semantic evaluation;
- terminal classifications for the disputed records;
- FARA primitive necessity, minimality, uniqueness, or superiority;
- GREL minimality or universality;
- universal structure;
- W3.5 completion;
- W5 authorization.
