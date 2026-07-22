# USD-W2-ALT-001 — Alternative-vocabulary competition

## Status

Complete bounded comparison under `POST-W5-USD-001`.

## Question

Do FARA, the generic relational baseline, and at least two independently motivated non-FARA vocabularies differ under the same frozen scope, preservation contract, and full machinery ledger?

## Frozen scope

The comparison uses `S_core` plus the six formally represented `USD-W1` subclasses. Actual-process correspondence is excluded because the prior workstream classified it as requiring independent empirical assumptions.

## Candidates

- `FARA-001`: typed reasoning vocabulary.
- `GREL-001`: generic relational baseline.
- `LTS-PROV-001`: labeled transition systems augmented by explicit provenance.
- `ARG-HIST-001`: structured argumentation augmented by versioned history.

No candidate receives free hidden interpreters, metadata, semantic interfaces, decoders, or transition machinery. Every helper required to preserve the frozen commitments is charged to derived machinery, operations, or semantic description length.

## Results

All candidates except `ARG-HIST-001` achieve full bounded coverage and preservation. The argumentation candidate preserves ordinary support, conflict, commitment, and revision structure, but continuous, stochastic, and partial-observation cases require external numeric and transition interfaces; it is therefore Partial rather than Pass.

`GREL-001` can represent the scope, but only by rebuilding reasoning distinctions through typed predicates, constraints, transition conventions, and history schemas. Its genericity therefore produces lower constraint strength and reasoning discrimination plus higher registered machinery cost.

`LTS-PROV-001` preserves the scope with fewer primitive operations than FARA, but requires more derived machinery and longer semantic declarations to recover grounds, commitments, rule status, rejection, and evidential history. Neither candidate is no-worse on every registered dimension.

## Pareto classifications

- FARA dominates GREL on the bounded scope.
- FARA dominates ARG-HIST on coverage and preservation.
- LTS-PROV dominates GREL.
- FARA and LTS-PROV are incomparable.
- LTS-PROV and ARG-HIST are incomparable.

The terminal result is `multiple_incomparable_successful_vocabularies`. There is no scalar winner.

## Scientific effect

This supplies bounded support for reasoning discrimination against `GREL-001`. It does not establish unique superiority, necessity, minimality, representation invariance, exhaustive candidate coverage, or universal structure.

The next decisive workstream is `USD-W3-INVARIANCE`.
