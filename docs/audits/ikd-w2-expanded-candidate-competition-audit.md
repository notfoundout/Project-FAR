# IKD-W2 Expanded Candidate Competition Audit

## Freeze integrity

- The six IKD-W1 candidates were admitted before evaluation.
- No candidate primitives, scope exceptions, or helper permissions were added after results were known.
- The prior FARA and LTS-PROV results were imported without favorable reinterpretation.

## Comparison integrity

- Every candidate faced the same bounded cases and six preservation dimensions.
- Costs include supplied primitives, derived machinery, operations, semantic description length, and equivalent reintroduction.
- Partial preservation is not treated as success.
- Unknown is not treated as Pass.
- No scalar score or preferred-vocabulary tie breaker is used.

## Negative-control integrity

The execution rejects hidden provenance, unrestricted interpreters, source-specific decoding, finite truncation presented as exact coverage, future-state access, post-result repair, and scalar winner construction.

## Result integrity

- FARA, LTS-PROV, and COALG-DYN satisfy the bounded contract.
- They are pairwise incomparable under the componentwise preorder.
- Five candidates remain scope-limited with explicit failed dimensions and charged repairs.
- The new three-candidate frontier does not imply global minimality or candidate exhaustiveness.

## Next-dependency integrity

The result freezes exactly the successful set required by `IKD-W3-COMMON-FACTOR`. Common-factor search must not count label intersection, generic graph structure, unrestricted interpretation, or hidden equivalent reintroduction as a kernel.

## Terminal classification

`expanded_competition_complete_three_incomparable_successful_architectures`
