# S_core Construction and Obstruction Lemma Ledger v1.0

## Status

Frozen proof-dependency ledger for `THM-TARGET-001`; W0 through W4 complete; W5 blocked by `W3.5-SDG-001`.

Ledger identifier: `SCORE-LEMMA-LEDGER-001`.

This artifact preserves the frozen construction, obstruction, and assembly statements while recording their execution state. Accepted proof packages are:

- `SCORE-W0-PROOF-001` — source normalization and reduct extraction;
- `SCORE-W1-PROOF-001` — target allocation and direct-axis construction;
- `SCORE-W2-PROOF-001` — dynamics, history, revision, and operational rule-version change;
- `SCORE-W3-PROOF-001` — target-only recovery, semantics, coherence, machinery, uniformity, composition, and typed witness assembly;
- `SCORE-W4-PROOF-001` — formal incompatibility of the applicable registered NC-01 through NC-10 families with the frozen faithful-representation relation.

The ledger records 24 proved construction lemmas, 1 established source-scope boundary, 8 refuted obstruction hypotheses, 1 established negative-control obstruction, and 3 open assembly obligations.

## Governing artifacts

The ledger is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/governance/deduction-first-research-standard.md`;
- `docs/governance/representation-discovery-separation-standard-v1.0.md`.

The machine-readable authority is `theory/evaluation/s-core-construction-obstruction-ledger.json`.

## Result boundary

W0 through W3 prove every registered construction obligation. W4 proves that each applicable registered negative-control family violates at least one independently frozen `Faithful_split` conjunct for its registered reason.

This closes `OBS-SC-010` at its stated scope. It does not prove that all invalid representations are rejected, that FARA is more constrained than `GREL-001`, or that the complete faithful predicate is satisfiable.

W5 may not begin until `W3.5-SDG-001` has terminal, immutable evidence for the concrete corpus, dimensioned factorization, specificity, ablation, reconstruction, machinery cost, and claim-impact requirements.

## Dependency waves and execution

### W0 — Source normalization kernel — **complete**

- `LEM-SC-001` — finite source-contract normalization — **proved**.
- `LEM-SC-002` — canonical reduct extraction — **proved**.
- `LEM-SC-003` — materiality closure and applicability decidability — **proved**.
- `LEM-SC-004` — source-isomorphism transport — **proved**.
- `OBS-SC-001` — non-finite material-closure boundary — **scope boundary established**.

### W1 — Base carriers and direct axes — **complete**

- `LEM-SC-005` through `LEM-SC-009` — target allocation and P1-P4 construction — **proved**.
- `LEM-SC-012` — consequence construction — **proved**.
- `LEM-SC-014` — internal evidential-status construction — **proved**.
- `OBS-SC-003` and `OBS-SC-006` — **refuted**.

### W2 — Dynamics, history, and revision — **complete**

- `LEM-SC-010`, `LEM-SC-011`, `LEM-SC-013`, `LEM-SC-015`, and `LEM-SC-016` — **proved**.
- `OBS-SC-004` and `OBS-SC-005` — **refuted**.

### W3 — Global witness obligations — **complete**

- `LEM-SC-017` through `LEM-SC-024` — **proved**.
- `OBS-SC-002`, `OBS-SC-007`, `OBS-SC-008`, and `OBS-SC-009` — **refuted**.

### W4 — Formal negative controls — **complete**

- `OBS-SC-010` — formal NC-01 through NC-10 family — **obstruction established**.

`SCORE-W4-PROOF-001` proves the family result only when the protected source distinction is material and applicable. Empty or inapplicable cases are not counted as successful rejections.

### W5 — Theorem assembly — **blocked**

- `ASM-SC-001` — common target-schema assembly — **registered unproved**.
- `ASM-SC-002` — arbitrary-episode faithful-witness assembly — **registered unproved**.
- `ASM-SC-003` — finite-core theorem-or-obstruction closure — **registered unproved**.

External blocker: `W3.5-SDG-001`.

## Frozen construction statements

The 24 frozen construction statements remain unchanged. They cover normalization, canonical reducts, materiality, source transport, target allocation, P1-P7 and P8-I construction, deterministic and finite-support probabilistic dynamics, history, revision, self-modification, decomposition, target-only recovery, semantic agreement, coherence, complete machinery accounting, uniformity, composition, and witness assembly.

## Frozen obstruction statements

- `OBS-SC-001`: non-finite material closure is outside `S_core` — **boundary established**.
- `OBS-SC-002`: hidden interpreter or source oracle is necessary — **refuted**.
- `OBS-SC-003`: finite direct-axis relations necessarily collapse — **refuted**.
- `OBS-SC-004`: finite dynamics necessarily fail P5 — **refuted**.
- `OBS-SC-005`: finite history or revision necessarily collapses — **refuted**.
- `OBS-SC-006`: internal evidential status is impossible to preserve — **refuted**.
- `OBS-SC-007`: witnesses necessarily require nonuniform case branching — **refuted**.
- `OBS-SC-008`: source-declared composition necessarily loses interfaces — **refuted**.
- `OBS-SC-009`: the frozen target interface is necessarily insufficient — **refuted**.
- `OBS-SC-010`: applicable NC-01 through NC-10 controls satisfy the frozen faithful relation — **obstruction established against that possibility**.

## Current execution summary

| Category | Count |
|---|---:|
| Total obligations | 37 |
| Construction obligations | 24 |
| Obstruction obligations | 10 |
| Assembly obligations | 3 |
| Proved construction obligations | 24 |
| Refuted obstruction hypotheses | 8 |
| Established negative-control obstructions | 1 |
| Established source-scope boundaries | 1 |
| Open assembly obligations | 3 |

## Exact next work

Execute `W3.5-SDG-001` with:

- a prospectively frozen, nonempty positive and contrast corpus;
- fixed `S_core → GREL-001`, `GREL-001 → FARA`, and where defined `FARA → GREL-001` translations;
- dimensioned expressiveness, translation, constraint-strength, reasoning-specificity, cost, and overall-interpretation results;
- candidate ablation and alternative reconstruction;
- complete machinery and cost accounting;
- immutable result artifacts with stable identifiers and matching SHA-256 digests;
- preserved failures, counterexamples, and claim-impact output.

Only after that evidence resolves may W5 assembly begin.

## Nonclaims

This ledger does not establish:

- `Faithful_split` satisfiability;
- rejection of every invalid representation;
- any W5 assembly obligation;
- FARA-specificity relative to `GREL-001`;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review.
