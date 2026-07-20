# S_core W2 Proof Audit

## Audit target

This audit covers:

- `docs/research/s-core-w2-dynamics-history-proof-v1.0.md`;
- `theory/evaluation/s-core-w2-dynamics-history-proof.json`;
- `tools/s_core_w2_reference.py`;
- `theory/evaluation/s-core-w2-reference-fixtures.json`;
- `tests/test_s_core_w2_reference.py`;
- integration with `SCORE-LEMMA-LEDGER-001`, `THM-TARGET-001`, `FAITHFUL-REP-001`, P8-ROLE-001, governance, planning, and research gates.

## Audit question

Does the package prove the registered finite W2 construction obligations and refute the corresponding finite mismatch hypotheses without silently assuming W3 recovery, semantics, coherence, machinery completeness, composition, theorem assembly, or broader universality?

## Result

**Pass for project-authored W2 proof execution.**

The package proves:

- `LEM-SC-010` deterministic dynamics construction;
- `LEM-SC-011` finite-support probabilistic dynamics construction;
- `LEM-SC-013` historical-and-path construction;
- `LEM-SC-015` nonmonotonic revision and retraction;
- `LEM-SC-016` self-modification and rule-version change.

It refutes:

- `OBS-SC-004` dynamics-bisimulation mismatch;
- `OBS-SC-005` history-and-path collapse.

The refutations are restricted to the finite explicit `S_core` W2 scope.

## Construction audit

`DYN-HISTORY-1.0` is one fixed schema. It:

- reuses W1 source-element images where available;
- allocates one represented target configuration per source configuration;
- copies state snapshots and active rule versions;
- allocates one transition record per source transition record;
- copies admissibility, labels, preconditions, resources, action and observation dependence, rule version, kernel, and weight;
- defines target live transitions from permitted status plus state-indexed active versions;
- copies every material event, order, causal, provenance, revision, modification, ancestry, and path relation;
- adds no FARA primitive.

Source-specific rules, values, histories, labels, and weights enter as finite target data rather than as executable case branches.

## Deterministic dynamics audit

On the represented image, source and target live transitions correspond one-for-one in both directions. The relation is an isomorphism, hence a bisimulation. The target cannot create a live represented-image transition without a copied source record.

## Probabilistic dynamics audit

Each finite source support branch and exact weight is copied. The target distribution is the pushforward of the source distribution under the injective state map. A changed branch, endpoint, kernel, or weight breaks the executable comparison.

## History and path audit

The target copies the material order relation itself rather than inferring order from presentation order. Removed and spurious order pairs fail the reference checker. Revision, rule-version, ancestry, and path facts are linked to represented states and transitions.

## Revision audit

Revision records are checked against before and after state snapshots. A label that says “retracted” while the later target state remains accepted fails. The construction therefore permits genuine nonmonotonic state change.

## Self-modification audit

The target live-transition definition reads the active rule version at the source state. An accepted modification updates the active-version set; a rejected modification preserves it. Removing the newly active version disables the later transition in the executable fixture. The result is operational, not label-only.

## Dependency audit

The proof uses only:

- frozen `S_core` finiteness and explicitness;
- W0 normalization and reduct extraction;
- W1 finite target allocation and direct-axis images;
- frozen P5 and P7 preservation semantics;
- finite graph, finite measure, and exact relational-copy arguments.

It does not use:

- admissible target-only recovery;
- global semantic agreement;
- complete cross-axis coherence;
- a complete machinery ledger;
- distributed composition;
- complete constructor uniformity;
- witness assembly;
- PB-001 completeness;
- actual-process correspondence;
- evaluator agreement.

## Executable corroboration

The reference suite contains 11 tests covering deterministic reflection, probabilistic mass, inactive rule versions, history order, revision snapshots, accepted and rejected modification behavior, path retention, and rule-version retention.

The executable checks are bounded corroboration. They are not proof-assistant verification and not independent proof review.

## Ledger effect

After W2:

- total obligations: 37;
- proved construction lemmas: 16;
- refuted obstruction hypotheses: 4;
- established source-scope boundaries: 1;
- open obligations: 16;
- completed waves: W0, W1, W2;
- active wave: W3.

## Gate audit

The following remain unchanged:

- formal-theorem-target: satisfied;
- premise-ledger-and-semantics: satisfied;
- faithful-representation-definition: satisfied;
- scoped-representation-proof: not satisfied;
- mechanized-proof-verification: not satisfied;
- independent-proof-review: not satisfied.

No central theorem or universality claim is promoted.

## Exact next work

Execute W3 as one integrated package:

- distributed interface construction;
- admissible target-only recovery;
- semantic agreement;
- cross-axis coherence;
- complete machinery accounting;
- uniformity and source-isomorphism equivariance;
- compositional accountability;
- well-formed witness assembly.
