# USD-W1-APC-001 — Actual-process correspondence boundary

## Status

Complete boundary execution for the final registered `USD-W1-SCOPE-EXT` feature family.

## Frozen question

Can repository-internal formal artifacts establish that a faithful target representation corresponds to an actual external reasoning process?

## Result

No positive correspondence claim follows from the available evidence. The terminal outcome is `new_assumption_required`.

The repository can establish relations among formal objects: source specifications, target representations, transitions, histories, proofs, traces, and provenance records. It cannot, from those artifacts alone, establish that the formal source variables are identical to or track the states of an independently existing process.

## Separation theorem

Formal faithfulness and actual-process correspondence are distinct claims.

A faithful representation theorem has the form: for each admitted formal source object, a target object preserves the declared source commitments.

An actual-process correspondence claim additionally requires a bridge from observations of an external process to the source object. That bridge is not supplied by the representation theorem and cannot be manufactured from target-side labels or generated traces.

## Observational-equivalence control

Distinct internal processes can yield the same admitted observable traces, outputs, and predictions. Therefore behavioral agreement alone does not identify one internal process unless the evidence protocol contains a discriminating measurement or intervention and registers the alternatives it is intended to distinguish.

## Required empirical package

A future positive test must freeze, before observing results:

1. independent process observations;
2. a measurement model with error bounds;
3. identity or tracking criteria across time;
4. a mapping from measurements to source states and transitions;
5. discriminating predictions or interventions where feasible;
6. alternative-process explanations and failure criteria;
7. independent confirmation or replication.

Without this package, correspondence remains unresolved rather than false. Adding the package is a new evidential assumption and a separate empirical execution, not an extension of the current formal proof.

## Fixture results

- `APC-FORMAL-001`: insufficient — formal faithfulness alone does not identify an external process.
- `APC-TRACE-001`: insufficient — implementation-generated traces are not independent observations of the implementation.
- `APC-OBS-EQUIV-001`: blocking — observationally equivalent distinct processes defeat identity inference.
- `APC-MEAS-001`: eligible only as a template for a future empirical test.
- `APC-NEG-REP-001`: rejected — representability does not entail empirical correspondence.
- `APC-NEG-LABEL-001`: rejected — matching labels and self-authored provenance do not establish identity.

## Workstream effect

All seven registered `USD-W1-SCOPE-EXT` feature families now have terminal executions. Six formal feature families retain bounded `proper_subclass_only` results. Actual-process correspondence terminates as `new_assumption_required` because it requires independent empirical access.

The next decisive workstream is `USD-W2-ALT-VOCAB`, not another formal scope-extension claim.

## Nonclaims

This result does not establish that an actual process corresponds to FARA, that no such correspondence is possible, that behavioral equivalence implies internal identity, that repository traces are independent evidence, or that universal structure has been established.