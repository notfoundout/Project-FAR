# Expanded bounded FARA campaign

Status: Research

## Question

Do the bounded core-formalization and foundation-comparison observations persist when the carrier ceiling is expanded beyond two?

## Execution and observation

`python tools/check_fara_expanded_campaign.py --write` materially constructs every unary and binary relation interpretation on carriers of size 0 through 4, validates tuple arity and carrier membership, and performs a relation-content-dependent paired-reduct evaluation. The independent axes contain 31 unary and 66,067 binary interpretations, for 66,098 concrete executions. Full-signature cross-products were deliberately not enumerated and remain outside the evidence.

The target-level paired-reduct search independently revalidates model admissibility, actual carrier cardinality, typing, references, reduct equality, and target difference. It retains 30 witnesses comprising 60 models. Object, Property, Relation, Representation, and Interpretation have witnesses only at support bounds 1 through 4. Investigation and Reasoning Calculus have witnesses at support bounds 0 through 4. The earlier claim that every target had a valid witness at every tested size was false and has been removed.

The frozen foundation campaign was independently rerun: 57 mappings, 21 ablations comprising 336 executions, 12 round trips, six-dimensional preservation accounting, and the direction-aware Pareto comparison. Its bounded terminal result remains that multiple foundations are Pareto-incomparable, with the edge many-sorted relational → algebraic/state-transition and typed hypergraph incomparable with many-sorted relational.

Oracle, continuous, hybrid, and embodied cases remain Unknown because this campaign supplies no executable semantics for them.

## Discovery and acceptance boundary

This is reproducible Research evidence, not accepted theory. The six prior size-at-most-two specification, proof, and report artifacts are pinned to immutable Git blob identities from base commit `b05e48f204e273938ef406168b83cafc0958f9a0`. The writer refuses to regenerate campaign evidence when any historical artifact differs, so `--write` cannot bless a mutation.

No universality, uniqueness, global superiority, minimality, necessity, completeness, or independent-replication claim is made. No workstream label is introduced. Conclusions are limited to the declared independent relation axes and the target-specific support bounds recorded in the proof object.
