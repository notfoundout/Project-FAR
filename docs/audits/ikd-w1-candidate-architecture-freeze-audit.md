# IKD-W1 Candidate Architecture Freeze Audit

## Prospective integrity

- Candidate families are frozen before scoring.
- Current winners do not determine admission.
- The bounded source and preservation contract remain unchanged.
- No candidate result or frontier position is asserted.

## Novelty integrity

- Six independently motivated architecture families are included.
- Renaming, recompilation, wrappers, serialization changes, and implementation-language changes are insufficient.
- Direct or hidden commitment-equivalent reconstruction of FARA or LTS-PROV fails admission.
- Each candidate declares a distinctive constraint or failure mode from its own conceptual source.

## Machinery integrity

- Helpers, interpreters, decoders, adapters, invariants, bridges, metadata, and history mechanisms are charged.
- Equivalent reintroduction is not elimination.
- Source-specific decoders and unrestricted interpreters are prohibited.
- Candidate-specific repair after scoring requires a new version and cannot rewrite the frozen candidate.

## Comparison integrity

- Preservation remains six-dimensional.
- Costs remain componentwise.
- Pareto comparison is the only aggregate relation.
- Unknown is not Pass.
- Tradeoffs remain incomparable.

## Claim integrity

- Candidate admission is not candidate success.
- Six families are not an exhaustive global universe.
- Failure of all new candidates would not prove FARA or LTS-PROV universal.
- Success of one candidate would not by itself prove a universal kernel.

## Terminal classification

`candidate_architecture_universe_frozen_unexecuted`
