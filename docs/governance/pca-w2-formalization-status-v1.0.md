# PCA-W2 proof-assistant formalization status v1.0

Status: **Active — reproducible partial obstruction**

Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`

Machine authority: [`far-core-formalization-ledger-v1.0.json`](../../theory/evaluation/far-core-formalization-ledger-v1.0.json)

Generated view: [`far-core-v1.1-formalization.md`](../mechanization/far-core-v1.1-formalization.md)

## Current outcome

- `FORMALIZED`: 13 (`FAR-CORE-001`–`FAR-CORE-013`)
- `PARTIAL/OBSTRUCTION`: 1 (`FAR-CORE-014`)
- `CONTRADICTION/REOPEN REQUIRED`: 0
- pinned Lean toolchain: `leanprover/lean4:v4.19.0`
- kernel check: pass for the substrate, claims, Ω, bounded SSS, and mutation modules

The formalization changes no governing v1.1 statement and adds no axiom, `sorry`, `admit`, or
unsafe declaration. Classical choice is exposed where an image representative is selected;
function/proposition extensionality and quotient soundness are used only where recorded in the
ledger.

## Exact obstruction

The bounded SSS module proves the four uniform monotone successor-set decoders are exhaustive,
proves that one of the two Boolean witness profiles defeats each decoder, and proves conditional
hyperedge/frontier factorization bridges. The repository does not contain a Lean presentation of
the actual MLL formula/sequent syntax, resource-splitting rules, derivability judgment,
atom-balance lemma, or proofs of the two named `S_or` and `S_and` sequents.

Promoting the narrative witness facts to Lean axioms or definitions would silently add premises
and would not be end-to-end formalization. This is an encoding/infrastructure obstruction, not a
counterexample or contradiction to FAR-CORE-014. Its W1 truth verdict remains `PROVED` under the
exact PR #453 scope; its v1.1 `supported_derived` provenance label remains unchanged.

## Closure criterion

W2 may complete only when a separate application module:

1. fixes the certified MLL presentation used by PR #453;
2. encodes its syntax, contexts, rule instances, resource splits, and derivability;
3. proves atom balance;
4. proves both named witness profiles; and
5. composes those proofs with the existing decoder theorem without changing the decoder or state
   classes.

Until then, `PCA-W2-PROOF-ASSISTANT-FORMALIZATION` remains the canonical active theoretical
workstream. W3 contract semantics are not authorized by this partial result.

## Validation

```bash
python tools/check_far_core_v11_formalization.py
python -m unittest tests.test_far_core_v11_formalization
```

The Lean workflow compiles every W2 module and its negative controls on pull requests. A green
build establishes only machine-checked derivability relative to the encoded premises.
