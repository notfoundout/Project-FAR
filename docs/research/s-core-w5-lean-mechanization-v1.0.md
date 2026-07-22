# S_core W5 Lean Mechanization v1.0

## Status

`SCORE-W5-LEAN-001` machine-checks the bounded theorem assembled in `SCORE-W5-PROOF-001`.

The Lean source is `mechanization/lean/SCoreW5.lean`. It compiles under the repository-pinned Lean toolchain and contains no `axiom`, `sorry`, or `admit` declarations.

## Formalized objects

The mechanization defines:

- an explicit bounded source type carrying the eight internal preservation axes;
- one fixed theorem-facing FARA target structure;
- one uniform constructor from every bounded source into that target structure;
- an explicit witness type connecting source axes to target fields;
- the internal `Faithful_split` predicate.

## Machine-checked results

The Lean kernel checks the following results:

1. `ASM-SC-001`: every bounded source is handled by the same target schema and uniform constructor.
2. `ASM-SC-002`: every bounded source has a target and witness satisfying `Faithful_split`.
3. `ASM-SC-003`: the bounded theorem family is adjudicated.
4. `THM-CORE-REP-001`: bounded faithful representation is constructively proved.
5. The `S_core` impossibility alternative is refuted by the constructed witness.

## Proof boundary

This is a proof-assistant verification of the bounded formal theorem, not verification that the formal source type exhausts reasoning in general. It does not establish:

- representation over `S_IRD`;
- correspondence between actual cognitive processes and formal presentations;
- primitive necessity;
- minimality or uniqueness;
- reasoning specificity;
- universal structure;
- independent proof review.

Mechanization verifies that the theorem follows from the encoded definitions. It does not independently validate the adequacy or completeness of those definitions.

## Verification

The canonical checks are:

```text
lean mechanization/lean/SCoreW5.lean
python tools/check_s_core_w5_mechanization.py
python -m unittest tests.test_s_core_w5_lean_alignment
```
