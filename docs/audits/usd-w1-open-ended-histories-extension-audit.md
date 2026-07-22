# Audit — USD-W1 open-ended-histories extension

## Scope integrity

The source class is frozen independently of the candidate vocabulary. Admission depends on effective event indexing, total finite-prefix access, finite dependency cones, coherent prefix embeddings, and finitely supported revisions. No FARA primitive appears in the admission rule.

## Construction audit

The construction is uniform across `S_hist_eff`. It represents a history by a coherent directed family of finite prefixes with stable event names, one extension interface, and one recovery map. It does not use a source-specific decoder, future-history oracle, or fixed terminal horizon.

## Preservation audit

The proof separately checks:

- prefix coherence;
- stable event identity and order;
- finite dependency-cone recovery;
- separation of commitments, grounds, and dependencies;
- preservation of rejected, revised, and superseded history;
- continued extension availability;
- rejection of fixed-horizon collapse and future-oracle smuggling.

No preservation dimension is promoted from Unknown merely because no counterexample was found.

## Negative-control audit

The fixed-horizon control is rejected because it loses a later revision. The future-oracle control is rejected because it imports unavailable information. Infinite-past dependence and global unbounded rewriting remain explicit scope boundaries rather than being repaired after execution.

## Classification audit

`extension_proved` would be false because major open-ended and infinite-history classes remain excluded. `countermodel` would also be false because all admitted fixtures satisfy the construction. The correct terminal outcome is `proper_subclass_only`.

## Claim-boundary audit

The result advances one feature subclass only. It does not establish all open-ended histories, general `S_IRD` representation, universal structure, necessity, minimality, uniqueness, actual-process correspondence, mechanization, or independent review.
