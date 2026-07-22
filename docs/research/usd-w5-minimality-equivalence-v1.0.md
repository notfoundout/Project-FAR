# USD-W5 Minimality, Equivalence, and No-Go — v1.0

## Result

The frozen candidate universe contains FARA, LTS-PROV, GREL, and ARG-HIST. The successful set inherited from the bounded competition is FARA and LTS-PROV. GREL and ARG-HIST are not minimal successful candidates because registered dominance or preservation failure removes them from the minimal frontier.

The terminal classification is `multiple_incomparable_minima`.

## Frozen comparison rules

Candidates are grouped only by bidirectional translation equivalence. A valid translation must preserve admissibility, transitions, commitments, grounds, dependencies, revisions, semantic versions, and history. Similar labels, matching outputs, or behavioral agreement on a fixture are insufficient.

Costs are compared componentwise across required primitive commitments, derived machinery, operations, and semantic description length. No scalar score is permitted. A tradeoff is incomparability, not a win.

All helper machinery is charged. Derived relations, canonicalizers, state adapters, provenance bridges, semantic interpreters, decoders, and reconstruction invariants cannot be treated as free.

## Candidate classification

FARA remains successful and locally load-bearing under USD-W4. It is not dominated by any candidate in the frozen universe.

LTS-PROV remains successful and locally load-bearing under USD-W4. It is not dominated by any candidate in the frozen universe.

GREL is removed from the minimal frontier because both FARA and LTS-PROV achieve no-worse preservation with registered strict advantages.

ARG-HIST is removed from the minimal frontier because FARA achieves no-worse preservation with registered strict advantages.

## Translation-equivalence test

The FARA-to-LTS-PROV and LTS-PROV-to-FARA translations are partial but not commitment-equivalent. Each direction requires nontrivial reconstruction of distinctions that are native in the other candidate, and the round trip does not preserve the complete frozen commitment ledger without added machinery.

Therefore FARA and LTS-PROV are not one equivalence class. Neither dominates the other because each retains at least one registered cost advantage. They are distinct incomparable minimal classes in the frozen universe.

## Negative controls

The execution rejects output equality as equivalence, uncharged hidden interpreters, scalarized tradeoffs, exclusion of LTS-PROV to manufacture FARA uniqueness, and promotion of bounded minima to universal structure.

## Scientific effect

`USD-H-MIN` is resolved for this frozen candidate universe. A unique minimum is refuted inside that universe. This is a bounded classification, not a global theorem.

The result does not show that no future vocabulary can dominate both classes, that the candidate universe is exhaustive, that either class is globally minimal, or that multiple minima refute every possible universal kernel.

## Next workstream

The sequential USD-W1 through USD-W5 program is complete. The next registered workstream is `USD-W6-INDEPENDENCE`: independent proof review, technical replication, adversarial conceptual replication, and cross-context replication.
