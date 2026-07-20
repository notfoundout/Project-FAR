# S_core Construction and Obstruction Lemma Ledger v1.0

## Status

Frozen proof-dependency ledger for `THM-TARGET-001`; W0 through W3 complete; W4 active.

Ledger identifier: `SCORE-LEMMA-LEDGER-001`.

This artifact preserves the frozen construction, obstruction, and assembly statements while recording their execution state. The accepted proof packages are:

- `SCORE-W0-PROOF-001` — source normalization and reduct extraction;
- `SCORE-W1-PROOF-001` — target allocation and direct-axis construction;
- `SCORE-W2-PROOF-001` — deterministic and probabilistic dynamics, history, revision, and operational rule-version change;
- `SCORE-W3-PROOF-001` — target-only recovery, semantics, coherence, machinery, uniformity, composition, and typed witness assembly.

The ledger records 24 proved construction lemmas, 1 established source-scope boundary, 8 refuted obstruction hypotheses, and 4 open obligations. It does not establish the formal negative-control family, the global `Nontrivial` conjunct, `Faithful_split`, or a scoped representation theorem.

## Governing artifacts

The ledger is subordinate to:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `docs/governance/deduction-first-research-standard.md`.

Accepted execution packages:

- `docs/research/s-core-w0-normalization-proof-v1.0.md` and `theory/evaluation/s-core-w0-normalization-proof.json`;
- `docs/research/s-core-w1-direct-axis-proof-v1.0.md` and `theory/evaluation/s-core-w1-direct-axis-proof.json`;
- `docs/research/s-core-w2-dynamics-history-proof-v1.0.md` and `theory/evaluation/s-core-w2-dynamics-history-proof.json`;
- `docs/research/s-core-w3-global-witness-proof-v1.0.md` and `theory/evaluation/s-core-w3-global-witness-proof.json`.

The machine-readable ledger is `theory/evaluation/s-core-construction-obstruction-ledger.json`.

## Result boundary

Stage D4 requires every material `S_core` feature to receive either a proved uniform construction lemma or a quantified obstruction, refutation, countermodel, or scope-boundary result. Registration is not proof. Failure of one attempted construction does not establish nonexistence.

W0 through W3 now prove every registered construction obligation, including target-only recovery and complete finite witness assembly. The frozen `Faithful_split` definition also requires the registered formal negative-control family and global `Nontrivial` conclusion. Therefore the scoped representation theorem remains unproved until W4 and W5 close.

## Dependency waves and execution

### W0 — Source normalization kernel — **complete**

- `LEM-SC-001` — finite source-contract normalization — **proved**.
- `LEM-SC-002` — canonical reduct extraction — **proved**.
- `LEM-SC-003` — materiality closure and applicability decidability — **proved**.
- `LEM-SC-004` — source-isomorphism transport — **proved**.
- `OBS-SC-001` — non-finite material-closure boundary — **scope boundary established**.

### W1 — Base carriers and direct axes — **complete**

- `LEM-SC-005` — target carrier allocation — **proved**.
- `LEM-SC-006` — configuration construction — **proved**.
- `LEM-SC-007` — commitment construction — **proved**.
- `LEM-SC-008` — stake-and-alternative construction — **proved**.
- `LEM-SC-009` — ground-and-justification construction — **proved**.
- `LEM-SC-012` — consequence construction — **proved**.
- `LEM-SC-014` — internal evidential-status construction — **proved**.
- `OBS-SC-003` — relation-reflection collapse — **refuted**.
- `OBS-SC-006` — evidential-status impossibility — **refuted**.

### W2 — Dynamics, history, and revision — **complete**

- `LEM-SC-010` — deterministic dynamics construction — **proved**.
- `LEM-SC-011` — finite-support probabilistic dynamics construction — **proved**.
- `LEM-SC-013` — historical-and-path construction — **proved**.
- `LEM-SC-015` — nonmonotonic revision and retraction — **proved**.
- `LEM-SC-016` — self-modification and rule-version change — **proved**.
- `OBS-SC-004` — dynamics-bisimulation mismatch — **refuted**.
- `OBS-SC-005` — history-and-path collapse — **refuted**.

### W3 — Global witness obligations — **complete**

- `LEM-SC-017` — distributed decomposition and interface construction — **proved**.
- `LEM-SC-018` — admissible target-only recovery — **proved**.
- `LEM-SC-019` — semantic agreement — **proved**.
- `LEM-SC-020` — cross-axis coherence — **proved**.
- `LEM-SC-021` — complete machinery-ledger construction — **proved**.
- `LEM-SC-022` — uniformity and source-isomorphism equivariance — **proved**.
- `LEM-SC-023` — compositional accountability — **proved**.
- `LEM-SC-024` — well-formed witness assembly — **proved**.
- `OBS-SC-002` — hidden-interpreter necessity — **refuted**.
- `OBS-SC-007` — nonuniform-constructor obstruction — **refuted**.
- `OBS-SC-008` — composition-interface loss — **refuted**.
- `OBS-SC-009` — fixed-target-interface insufficiency — **refuted**.

### W4 — Formal obstruction and negative controls — **active**

- `OBS-SC-010` — formal negative-control family — **registered unproved**.

### W5 — Theorem assembly — **open**

- `ASM-SC-001` — common target-schema assembly — **registered unproved**.
- `ASM-SC-002` — arbitrary-episode faithful-witness assembly — **registered unproved**.
- `ASM-SC-003` — finite-core theorem-or-obstruction closure — **registered unproved**.

No W5 entry may be accepted while `OBS-SC-010` remains open, unknown, or supported only by examples.

## Frozen construction statements

- `LEM-SC-001`: normalize every finite explicit `S_core` source contract without losing theorem-facing materiality, interpretation, applicability, or dependency information.
- `LEM-SC-002`: extract the least finite P1–P7 and P8-I reducts and their closure dependencies.
- `LEM-SC-003`: prove finite materiality closure and decidable applicability.
- `LEM-SC-004`: transport normalized contracts and reducts under source isomorphism.
- `LEM-SC-005`: allocate one finite typed target schema with all helper machinery explicit.
- `LEM-SC-006`: preserve and reflect configuration carriers and incidence.
- `LEM-SC-007`: preserve and reflect commitment identity, content, holder, status, degree, and revision state.
- `LEM-SC-008`: preserve and reflect stakes, questions, live alternatives, relevance, exclusion, rank, and availability.
- `LEM-SC-009`: preserve and reflect grounds and typed justificatory roles.
- `LEM-SC-010`: construct deterministic finite target dynamics satisfying the registered labeled bisimulation.
- `LEM-SC-011`: construct finite-support probabilistic target dynamics preserving exact source weights or source-declared equivalence.
- `LEM-SC-012`: preserve and reflect consequence identity, basis, status, degree, and downstream role.
- `LEM-SC-013`: order-embed and reflect material history, provenance, ancestry, revision, rule versions, and path conditions.
- `LEM-SC-014`: preserve internal evidence status without evidential upgrade.
- `LEM-SC-015`: represent nonmonotonic revision, rejection, retraction, and supersession as actual before/after state change.
- `LEM-SC-016`: make accepted rule-version changes alter later admissible dynamics while rejected changes do not.
- `LEM-SC-017`: construct source-declared distributed components, interfaces, cross-component relations, and composed histories.
- `LEM-SC-018`: define one terminating deterministic target-only recovery family with no source oracle, evaluator, case database, network resource, or undeclared dependency.
- `LEM-SC-019`: prove source-declared semantic agreement without lexical shortcuts or semantic strengthening.
- `LEM-SC-020`: prove one compatible cross-axis representation with shared identities, compatible denotations, and no conflicting status or version data.
- `LEM-SC-021`: construct a complete finite dependency graph for every symbol, procedure, state field, bridge, metadata item, and helper.
- `LEM-SC-022`: prove one finite source-isomorphism-equivariant constructor family with no case-identifier branching.
- `LEM-SC-023`: prove restriction and composition commute for every source-declared decomposition.
- `LEM-SC-024`: assemble a well-formed witness `W=(E,D,M,iota,kappa)` without assuming the theorem conclusion.

## Frozen obstruction statements

- `OBS-SC-001`: determine whether non-finite material closure is admitted by `S_core`; W0 establishes it is outside scope.
- `OBS-SC-002`: determine whether some in-scope source necessarily requires a hidden interpreter, source oracle, or case database; W3 refutes this hypothesis.
- `OBS-SC-003`: determine whether finite direct-axis relations necessarily collapse; W1 refutes this hypothesis.
- `OBS-SC-004`: determine whether finite deterministic or finite-support probabilistic dynamics necessarily fail P5 bisimulation; W2 refutes this hypothesis.
- `OBS-SC-005`: determine whether finite explicit history, revision, path, or rule-version distinctions necessarily collapse; W2 refutes this hypothesis.
- `OBS-SC-006`: determine whether finite internal evidence-status distinctions are impossible to preserve; W1 refutes this hypothesis.
- `OBS-SC-007`: determine whether successful witnesses necessarily require nonuniform case branching or an unbounded helper family; W3 refutes this hypothesis.
- `OBS-SC-008`: determine whether a source-declared composition necessarily loses interface or cross-component structure; W3 refutes this hypothesis.
- `OBS-SC-009`: determine whether the frozen target interface is insufficient after complete witness assembly; W3 refutes this hypothesis.
- `OBS-SC-010`: prove the registered NC-01 through NC-10 family fails for the required formal reasons.

## Assembly statements

- `ASM-SC-001`: assemble one common target schema after recovery, machinery, uniformity, and witness well-formedness are proved.
- `ASM-SC-002`: assemble a faithful witness for an arbitrary admitted source episode from every accepted construction dependency.
- `ASM-SC-003`: derive the strongest justified finite-core theorem, countermodel, proper-subclass result, impossibility result, or explicit unresolved conclusion.

## Current execution summary

| Category | Count |
|---|---:|
| Total obligations | 37 |
| Construction obligations | 24 |
| Obstruction obligations | 10 |
| Assembly obligations | 3 |
| Proved construction obligations | 24 |
| Refuted obstruction hypotheses | 8 |
| Established source-scope boundaries | 1 |
| Open obligations | 4 |

## Exact next work

Execute `OBS-SC-010` as one formal negative-control package covering NC-01 through NC-10. Every negative control must fail for a frozen structural reason, not because of evaluator preference or a case-specific patch. Preserve any valid countermodel or newly exposed hidden commitment. Only after W4 closes may W5 assemble the finite-core result.

## Nonclaims

This ledger does not establish:

- `OBS-SC-010` or the global `Nontrivial` conjunct;
- `Faithful_split` satisfiability;
- any W5 assembly obligation;
- FARA adequacy for `S_core` or `S_IRD`;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- actual-process correspondence;
- a representation, universality, necessity, minimality, equivalence, uniqueness, or impossibility theorem;
- proof-assistant verification or independent proof review.
