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

## Mechanization-depth calibration

`FORMALIZED` is a mechanization-assurance status. It means the governed statement has a checked Lean counterpart under the recorded premises and kernel dependencies. It is **not** a score of theorem difficulty, independence, originality, or mathematical novelty.

The fourteen claims are intentionally heterogeneous:

- `FAR-CORE-001` is a definition-plus-kernel characterization: exact sufficiency is factorization on the represented image, with kernel inclusion/collision as the substantive equivalent test.
- `FAR-CORE-002` and `FAR-CORE-003` are quotient/universal-property and context-closure/congruence results.
- `FAR-CORE-004`, `005`, and `009` are elementary incompatibility, monotonicity, and finite-extension constructions.
- `FAR-CORE-006` is transport of structure over an injective encoding and its reachable image.
- `FAR-CORE-007` and `008` prove semantic recovery across re-presentation/tagged dispatch and separately compare declared primitive-count profiles. The present formalization does not derive those vocabulary/operator counts from a general typed presentation syntax.
- `FAR-CORE-010` separates a definitional dependency fact—`Gamma` is absent from exact `CommonTheory` when the interpreted truth profile is held fixed—from the substantive companion theorem that the `Gamma`-relative residue can change.
- `FAR-CORE-011` and `012` are direct exact-sufficiency/collision consequences.
- `FAR-CORE-013` is a project-specific definitional elimination of canonical FARA Ω.
- `FAR-CORE-014` is the most application-specific bounded bridge, including the unit-free MLL witness surface and decoder classification.

This classification does not downgrade any theorem or kernel check. It prevents the flat count `14/14 FORMALIZED` from being misread as `14 equally deep or novel mathematical discoveries`.

See [`far-core-epistemic-calibration-v1.0.md`](../audits/far-core-epistemic-calibration-v1.0.md) for the non-authoritative cross-claim calibration and prior-art normalization.

## FAR-CORE-014 closure

The bounded SSS module now encodes the governed unit-free MLL witness surface end to end: formula/sequent syntax, resource-splitting derivability, atom balance, the named `S_or` and `S_and` witness profiles, the exhaustive four monotone successor-set decoders, and the bounded projected-decoder failure. The witness proofs compose with the decoder theorem without changing the governed decoder classes or adding a narrative premise.

This closes the prior encoding/infrastructure obstruction. It does not change FAR-CORE-014's governing `supported_derived` provenance label or its W1 exact-scope truth verdict; truth, provenance, and mechanization assurance remain separate dimensions.

## Disposition

`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is complete. No reproducible contradiction to the governing v1.1 theory was found, so the core remains closed. At W2 completion, the next registered workstream was `PCA-W3-CONTRACT-SCHEMA`. That transition is historical: W3–W6 and `POST-CLOSURE-001` are complete, and the separate current successor is preregistered `EXTERNAL-FALSIFICATION-AND-REPLICATION-001`, not W7.

W2 completion establishes machine-checked derivability relative to the encoded premises. It does not establish novelty, priority, empirical utility, computational efficiency, open-domain universality, or product readiness.

## Validation

```bash
python tools/check_far_core_v11_formalization.py
python -m unittest tests.test_far_core_v11_formalization
```

The Lean workflow compiles every W2 module and its negative controls on pull requests and enforces the exact transitive axiom contract against runtime `#print axioms` output.
