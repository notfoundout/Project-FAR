# PCA-W2 proof-assistant formalization status v1.0

Status: **Complete**

Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`

Machine authority: [`far-core-formalization-ledger-v1.0.json`](../../theory/evaluation/far-core-formalization-ledger-v1.0.json)

Generated view: [`far-core-v1.1-formalization.md`](../mechanization/far-core-v1.1-formalization.md)

## Terminal outcome

- `FORMALIZED`: 14 (`FAR-CORE-001`–`FAR-CORE-014`)
- `PARTIAL/OBSTRUCTION`: 0
- `CONTRADICTION/REOPEN REQUIRED`: 0
- pinned Lean toolchain: `leanprover/lean4:v4.19.0`
- kernel check: pass for the substrate, claims, Ω, bounded SSS/MLL witness bridge, and mutation modules

The formalization changes no governing v1.1 statement and adds no FAR axiom, `sorry`, `admit`, or unsafe declaration. Transitive Lean kernel dependencies are recorded exactly by declaration in the formalization ledger and enforced by the generated `#print axioms` audit; they include `Classical.choice`, `propext`, and `Quot.sound` only where observed and declared.

## FAR-CORE-014 closure

The bounded SSS module now encodes the governed unit-free MLL witness surface end to end: formula/sequent syntax, resource-splitting derivability, atom balance, the named `S_or` and `S_and` witness profiles, the exhaustive four monotone successor-set decoders, and the bounded projected-decoder failure. The witness proofs compose with the decoder theorem without changing the governed decoder classes or adding a narrative premise.

This closes the prior encoding/infrastructure obstruction. It does not change FAR-CORE-014's governing `supported_derived` provenance label or its W1 exact-scope truth verdict; truth, provenance, and mechanization assurance remain separate dimensions.

## Disposition

`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is complete. No reproducible contradiction to the governing v1.1 theory was found, so the core remains closed. The next registered workstream is `PCA-W3-CONTRACT-SCHEMA`.

W2 completion establishes machine-checked derivability relative to the encoded premises. It does not establish novelty, priority, empirical utility, computational efficiency, open-domain universality, or product readiness.

## Validation

```bash
python tools/check_far_core_v11_formalization.py
python -m unittest tests.test_far_core_v11_formalization
```

The Lean workflow compiles every W2 module and its negative controls on pull requests and enforces the exact transitive axiom contract against runtime `#print axioms` output.
