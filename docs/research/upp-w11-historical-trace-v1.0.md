# UPP-W11 Historical-Trace Necessity

## Scope

This workstream establishes the fifth registered RCCD-component necessity lemma relative to the frozen target class `C*`, faithfulness contract `P*`, admissible representation universe `E*`, machinery-closure operator, and commitment-equivalence relation.

The claim is operational and relative. It does not assert a metaphysical theory of time, causation, memory, or identity.

## Theorem

For every `S in C*` and `R in E*`, when `R` is machinery-closed, fully faithful, commitment-equivalence preserving, history-sensitive, and total on registered history queries, there exists an effective historical-trace witness recoverable from `R`.

The witness contains stable event identities, event kinds, represented subjects, temporal indexes, predecessor relations, dependency and reason links, and explicit supersession lineage.

## Why a snapshot is insufficient

A final state can be extensionally identical across systems that reached it through different derivations, defeaters, retractions, or rule changes. The frozen preservation contract already distinguishes those systems. Therefore a fully faithful representation of a history-sensitive case cannot erase the path and retain only the endpoint.

Likewise, a bag of timestamped messages is not yet a faithful trace. It must preserve which event is which, what it changed, what preceded or supported it, what it superseded, and which later transitions depend on that lineage.

## Witness obligations

A positive witness must establish all of the following:

1. A nonempty and nontrivial structurally valid trace.
2. Effective recovery of registered historical facts.
3. Stable event identity.
4. Total temporal ordering for registered events.
5. Complete predecessor links.
6. Complete dependency lineage.
7. Complete revision, retraction, replacement, and supersession lineage.
8. Recoverable reasons where the source system exposes them.
9. Replay or rollback fidelity for the registered case.
10. Invariance under commitment-equivalent representation changes.
11. Complete accounting for logs, clocks, stores, indexes, decoders, replay engines, and external services.
12. Total registered history queries.
13. Separation of failure from `Unknown`.

## Proof architecture

The proof is by extraction and contradiction.

First, full faithfulness requires preservation of operational, dependency, information, and historical distinctions. History-sensitive behavior makes at least one later admissibility, answer, or transition depend on an earlier represented event. The registered query interface must therefore expose the relevant event identities and lineage, or return an explicit unresolved value.

Second, machinery closure charges every required log, clock, event store, decoder, index, replay mechanism, and oracle to the representation package. Hidden audit infrastructure cannot be used to satisfy the theorem.

Third, commitment equivalence prevents event identities and lineage from changing merely because the same commitments are encoded with different names, graph layouts, storage media, or execution schedules.

Denying the existence of a recoverable witness while retaining all antecedents would erase at least one required historical distinction, make a registered query non-total, conceal required machinery, or violate equivalence invariance. Each alternative contradicts a frozen premise.

## Separating countermodels

The following do not satisfy the theorem:

- a final snapshot with no path information;
- timestamps without stable event identity;
- an unordered bag of events;
- a narrative reconstructed after execution;
- revision records without supersession lineage;
- a hidden external audit database;
- rollback that does not reproduce the registered commitment state;
- a query layer that reports absent history when the answer is actually unknown.

## Adjudication

The executable model is three-valued. `proved` requires positive evidence for every antecedent and every witness obligation. Any false item yields `refuted`. If none is false and at least one is unresolved, the result remains `unknown`.

## Result

`historical_trace_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence`

The next registered workstream is PR #293, `UPP-W12-COMPONENT-INDEPENDENCE`. Public evaluation remains unauthorized.
