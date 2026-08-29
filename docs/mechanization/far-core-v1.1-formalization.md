# FAR-CORE v1.1 proof-assistant formalization

Status: **Generated W2 assurance view; not governing theory authority**

Sources: [`theory/evaluation/far-core-formalization-ledger-v1.0.json`](../../theory/evaluation/far-core-formalization-ledger-v1.0.json)
and [`artifacts/mechanization/lean-inventory-v1.0.json`](../../artifacts/mechanization/lean-inventory-v1.0.json).
Edit the machine ledger or Lean sources and regenerate this view.

Lean proves machine-checked derivations relative to the encoded premises. It does not establish
novelty, empirical validity, or universal architecture. The W1 truth verdicts, historical
provenance labels, and proof-assistant status remain separate dimensions.

The W2 workflow captures every `#print axioms` result and rejects missing declarations,
unexpected transitive assumptions, or any mismatch with the declaration-level and claim-level
assumption contracts. Merely printing the audit is not accepted as assurance.

## Outcome matrix

| Claim | W2 outcome | Kernel | Kernel assumptions | Declarations | Obstruction |
|---|---|---|---|---|---|
| `FAR-CORE-001` | `FORMALIZED` | `PASS` | `Classical.choice` | `FARCoreV11.exact_factorization_criterion`<br>`FARCoreV11.collision_refutes_sufficiency` | — |
| `FAR-CORE-002` | `FORMALIZED` | `PASS` | `Classical.choice`<br>`Quot.sound` | `FARCoreV11.quotient_is_sufficient`<br>`FARCoreV11.observational_quotient_universal`<br>`FARCoreV11.factorToQuotient_surjective`<br>`FARCoreV11.leastInformativeImageEquiv` | — |
| `FAR-CORE-003` | `FORMALIZED` | `PASS` | `Quot.sound` | `FARCoreV11.action_preserves_observational_equivalence`<br>`FARCoreV11.descendAction` | — |
| `FAR-CORE-004` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.no_contract_free_simultaneous_minimum`<br>`FARCoreV11.identity_is_universally_sufficient` | — |
| `FAR-CORE-005` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.invariants_antitone` | — |
| `FAR-CORE-006` | `FORMALIZED` | `PASS` | `Classical.choice`<br>`Quot.sound`<br>`propext` | `FARCoreV11.embeddingRangeEquiv`<br>`FARCoreV11.transport_operation_commutes`<br>`FARCoreV11.transport_relation_commutes` | — |
| `FAR-CORE-007` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.reification_recovers_relation`<br>`FARCoreV11.primitive_vocabulary_count_noninvariant` | — |
| `FAR-CORE-008` | `FORMALIZED` | `PASS` | `Quot.sound` | `FARCoreV11.combine_split_operator_family`<br>`FARCoreV11.split_combine_operator` | — |
| `FAR-CORE-009` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.finite_panel_two_completions` | — |
| `FAR-CORE-010` | `FORMALIZED` | `PASS` | `Quot.sound`<br>`propext` | `FARCoreV11.commonTheory_frame_independent`<br>`FARCoreV11.commonTheory_invariant_under_truth_equivalence`<br>`FARCoreV11.residue_can_change_with_frame` | — |
| `FAR-CORE-011` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.omitted_parameter_refutes_sufficiency` | — |
| `FAR-CORE-012` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.absent_unknown_must_separate` | — |
| `FAR-CORE-013` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.Omega.omega_elimination`<br>`FARCoreV11.Omega.resolve_is_composition` | — |
| `FAR-CORE-014` | `FORMALIZED` | `PASS` | `Quot.sound`<br>`propext` | `FARCoreV11.SSS.four_monotone_decoders`<br>`FARCoreV11.SSS.projected_successor_decoder_failure`<br>`FARCoreV11.SSS.hyperedge_factorization`<br>`FARCoreV11.SSS.frontier_factorization`<br>`FARCoreV11.SSS.MLL.derivable_atom_balance`<br>`FARCoreV11.SSS.MLL.sOr_witness_certified`<br>`FARCoreV11.SSS.MLL.sAnd_witness_certified`<br>`FARCoreV11.SSS.MLL.bounded_projected_decoder_failure` | — |

## FAR-CORE-014 bounded application bridge

The governed MLL syntax, cut-free unit-free derivability rules, atom-balance invariant, both named
witness sequents, their mixed projected-successor truth profiles, and the uniform-decoder failure
are now kernel-checked in `FARCoreV11SSS.lean`. The positive hyperedge and frontier statements
remain explicitly conditional on their stated rule-characterization/recursion premises. This
formalization does not enlarge FAR-CORE-014 into a universal architecture claim.

## W2 module inventory

| File | SHA-256 | Lines | Imports |
|---|---|---:|---|
| `mechanization/lean/FARCoreV11AxiomAudit.lean` | `3a5f71c40a06336f6d08ebe877bdcf6c9aa8782b8760e7de5885fd757f6e5736` | 38 | `FARCoreV11Claims001To012`, `FARCoreV11Omega`, `FARCoreV11SSS` |
| `mechanization/lean/FARCoreV11Claims001To012.lean` | `9171f9a6598bfdaf2eaf37cf8994438c0095ff4a8e39081c8887ce5ea90f746e` | 318 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11Mutations.lean` | `ec389d2081c635f336aa2f3cd087f997aeb7ed800e4fa081b76f43130aa23069` | 170 | `FARCoreV11Claims001To012`, `FARCoreV11Omega`, `FARCoreV11SSS` |
| `mechanization/lean/FARCoreV11Omega.lean` | `52570fe1ed0c7a76b850162d584d47e759098b054a8cd147161891d663a7044c` | 51 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11SSS.lean` | `15fdf821d878cedcf205891fc2d29822a0cc49c3dcedc8610eb4609169060465` | 375 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11Substrate.lean` | `c10ed7cd9f2bb35018d7312e2f3fa755cb292663a73ed24fb17eeac193c01410` | 240 | `Std` |

The inventory also records every pre-existing Lean file as `LEGACY_OR_OTHER_SCOPE`. Those files
were searched and retained; they do not silently count as coverage of FAR-CORE-001--014.
