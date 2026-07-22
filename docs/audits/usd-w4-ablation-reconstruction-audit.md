# Audit — USD-W4 ablation and reconstruction

## Scope integrity

The benchmark and commitment-equivalence relation are inherited from USD-W2 and USD-W3. No ablation-specific source cases were added after observing failures.

## Removal integrity

Every registered unit was directly removed and the full preservation vector was recomputed. Unknown was not treated as pass.

## Reconstruction integrity

Alternative reconstructions were canonicalized before comparison. Equivalent reintroductions were counted as machinery rather than evidence that the removed unit was unnecessary.

## Cost integrity

Primitive categories, derived schemas, state, transitions, invariants, semantic declarations, provenance, history, decoders, and adapters were charged. No scalar score was introduced.

## Comparison integrity

FARA and LTS-PROV remain incomparable. The execution does not select a winner.

## Classification integrity

The correct result is `bounded_local_necessity_supported`. Global necessity and minimality remain unresolved because the tested reconstruction space and benchmark are bounded.

## Claim boundary

This audit does not establish universality, uniqueness, actual-process correspondence, formal mechanization, independent review, or independent replication.