# FAR-CORE v1.1 proof-assistant formalization

Status: **Generated W2 assurance view; not governing theory authority**

Sources: [`theory/evaluation/far-core-formalization-ledger-v1.0.json`](../../theory/evaluation/far-core-formalization-ledger-v1.0.json)
and [`artifacts/mechanization/lean-inventory-v1.0.json`](../../artifacts/mechanization/lean-inventory-v1.0.json).
Edit the machine ledger or Lean sources and regenerate this view.

Lean proves machine-checked derivations relative to the encoded premises. It does not establish
novelty, empirical validity, universal architecture, or correctness of an unencoded narrative
application bridge. The W1 truth verdicts and proof-assistant status remain separate dimensions.

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
| `FAR-CORE-007` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.reification_recovers_relation` | — |
| `FAR-CORE-008` | `FORMALIZED` | `PASS` | `Quot.sound` | `FARCoreV11.combine_split_operator_family`<br>`FARCoreV11.split_combine_operator` | — |
| `FAR-CORE-009` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.finite_panel_two_completions` | — |
| `FAR-CORE-010` | `FORMALIZED` | `PASS` | `Quot.sound`<br>`propext` | `FARCoreV11.commonTheory_frame_independent`<br>`FARCoreV11.commonTheory_invariant_under_truth_equivalence`<br>`FARCoreV11.residue_can_change_with_frame` | — |
| `FAR-CORE-011` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.omitted_parameter_refutes_sufficiency` | — |
| `FAR-CORE-012` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.absent_unknown_must_separate` | — |
| `FAR-CORE-013` | `FORMALIZED` | `PASS` | `none` | `FARCoreV11.Omega.omega_elimination`<br>`FARCoreV11.Omega.resolve_is_composition` | — |
| `FAR-CORE-014` | `PARTIAL/OBSTRUCTION` | `PASS` | `propext` | `FARCoreV11.SSS.four_monotone_decoders`<br>`FARCoreV11.SSS.projected_successor_decoder_failure`<br>`FARCoreV11.SSS.hyperedge_factorization`<br>`FARCoreV11.SSS.frontier_factorization` | The decoder enumeration, two Boolean witness profiles, and conditional hyperedge/frontier factorization bridges are kernel-checked. The repository has no Lean encoding of the actual MLL syntax, resource-splitting rules, derivability relation, atom-balance lemma, or the two named sequents. Treating the PR #453 MLL witness facts as axioms or definitions would silently replace their narrative proofs with premises and would not be exact end-to-end formalization. |

## FAR-CORE-014 governed obstruction

- Classification: `encoding_inconvenience`
- Affected surface: Only the application bridge from the Boolean S_or/S_and summaries to actual MLL sequents; FAR-CORE-014 truth and W1 review disposition are not contradicted.
- Reproducible detail: The decoder enumeration, two Boolean witness profiles, and conditional hyperedge/frontier factorization bridges are kernel-checked. The repository has no Lean encoding of the actual MLL syntax, resource-splitting rules, derivability relation, atom-balance lemma, or the two named sequents. Treating the PR #453 MLL witness facts as axioms or definitions would silently replace their narrative proofs with premises and would not be exact end-to-end formalization.
- Allowed resolution: Add a separate application module formalizing the certified MLL presentation, prove balance and both witness profiles, then remove this obstruction without changing v1.1 or PR #453 scope.

This is not a refutation. The decoder enumeration, Boolean witness-profile theorem, conditional
hyperedge factorization, and conditional frontier factorization are kernel-checked. What is absent
is an end-to-end Lean derivation of the actual MLL witness facts.

## W2 module inventory

| File | SHA-256 | Lines | Imports |
|---|---|---:|---|
| `mechanization/lean/FARCoreV11AxiomAudit.lean` | `cba8c9617eded443e34cbf57d444b10fce210e6cfd03f11aed4df0ff790b52b3` | 41 | `FARCoreV11Claims001To012`, `FARCoreV11Omega`, `FARCoreV11SSS` |
| `mechanization/lean/FARCoreV11Claims001To012.lean` | `dbafd344e14fd966a7c3e9b3c4eaa43dfb6de97239dc7e61aabdb627676f2ca7` | 290 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11Mutations.lean` | `ec389d2081c635f336aa2f3cd087f997aeb7ed800e4fa081b76f43130aa23069` | 170 | `FARCoreV11Claims001To012`, `FARCoreV11Omega`, `FARCoreV11SSS` |
| `mechanization/lean/FARCoreV11Omega.lean` | `52570fe1ed0c7a76b850162d584d47e759098b054a8cd147161891d663a7044c` | 51 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11SSS.lean` | `2e3c4e12481ad206587316e34ef6a06736c5872315bc0a02285e2069f8f0b977` | 177 | `FARCoreV11Substrate` |
| `mechanization/lean/FARCoreV11Substrate.lean` | `c10ed7cd9f2bb35018d7312e2f3fa755cb292663a73ed24fb17eeac193c01410` | 240 | `Std` |

The inventory also records every pre-existing Lean file as `LEGACY_OR_OTHER_SCOPE`. Those files
were searched and retained; they do not silently count as coverage of FAR-CORE-001--014.
