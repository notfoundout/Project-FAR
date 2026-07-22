# USD-W3 Representation Invariance — v1.0

## Result

The frozen bounded benchmark family was transformed through eight registered admissible presentation changes and re-evaluated under `FARA-001` and `LTS-PROV-001`. All preservation judgments, machinery charges, and registered Pareto relations were stable. Five non-equivalent mutations were rejected.

The terminal result is `bounded_invariance_supported`.

## Equivalence boundary

Source presentations are equivalent only when a bijection preserves admissibility, transitions, commitments, grounds, dependencies, revisions, and history. Target encodings are compared by commitment-equivalence after canonicalization. Shared names, matching outputs, or similar behavior do not establish equivalence when ontology, hidden state, constraints, or history differ.

## Admissible transformations

The execution covers entity renaming, event reindexing, rule-order permutation, history chunking, state factorization, derived-relation materialization, equivalent transition normalization, and insertion of irrelevant annotations.

For every transformation, mapping then canonicalizing produced the same preservation commitments as canonicalizing the original mapping and transporting it through the registered correspondence. Required machinery and the `D/O/L` ledger remained stable up to syntactic normalization.

## Negative controls

Dependency erasure, retroactive revision rewriting, hidden-state collapse, semantic-version merging, and future-history access were rejected. These mutations may preserve some visible outputs but alter registered commitments and therefore are not admissible representation changes.

## Comparison effect

The bounded FARA/LTS-PROV incomparability from USD-W2 survives every registered admissible transformation. FARA and LTS-PROV retain their bounded dominance over GREL. No representation change manufactures a winner.

## Claim boundary

This supports `THM-US-INV-001` only over the frozen benchmark, tested vocabularies, and registered transformations. It does not prove global representation invariance, exhaustive vocabulary coverage, necessity, minimality, uniqueness, universality, or actual-process correspondence.

The next workstream is `USD-W4-ABLATION`.