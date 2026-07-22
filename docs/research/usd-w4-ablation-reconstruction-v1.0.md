# USD-W4 Ablation and Reconstruction — v1.0

## Result

The frozen bounded benchmark was evaluated under direct primitive removal, alternative reconstruction, and equivalent reintroduction for `FARA-001` and `LTS-PROV-001`.

Every tested unit was locally load-bearing or could preserve the contract only by reintroducing commitment-equivalent machinery. No strictly cheaper non-equivalent reconstruction preserved all obligations.

The terminal result is `bounded_local_necessity_supported`.

## Method

Each unit was removed while all other frozen commitments remained fixed. The resulting mapping was re-evaluated for commitments, admissibility, dependencies, revision effects, historical distinctions, semantic versions, hidden-state boundaries, and uniform recovery.

Where a reconstruction restored preservation, its complete machinery was canonicalized and charged. A renamed relation, typed carrier, interpretation function, provenance table, event log, supersession relation, decoder, or invariant was not treated as free merely because it was described as derived.

## FARA result

Structure, calculus, and provenance/history are directly load-bearing on the benchmark. Removing representation or interpretation also breaks preservation; successful repairs reconstruct typed identity or semantic-version machinery commitment-equivalent to the removed category.

## LTS-PROV result

State, transition, and provenance are directly load-bearing. Label semantics and history/revision can be reconstructed, but only through typed interpretation and explicit event/supersession machinery that is commitment-equivalent and fully charged.

## Comparison effect

The bounded FARA/LTS-PROV incomparability survives. Ablation does not manufacture a winner.

## Boundary

This establishes local load-bearing status only over the frozen benchmark, tested units, reconstruction class, and cost ledger. It does not prove global necessity across all vocabularies or `S_IRD`, nor minimality, uniqueness, universality, actual-process correspondence, formal mechanization, or independent verification.

The next workstream is `USD-W5-MIN-EQUIV`.