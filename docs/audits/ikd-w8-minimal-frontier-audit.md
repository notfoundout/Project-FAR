# IKD-W8 Minimal-Frontier Audit

## Controls

- Comparison is componentwise and commitment-based; no scalar score is permitted.
- Vocabulary cost and reconstruction cost remain separate.
- Bidirectional reconstruction is required before architectures may be grouped.
- Decoders, schedulers, adapters, canonicalizers, proof objects, observation algebras, provenance closure, and history normalization are charged.
- An omitted primitive is not a reduction when equivalent distinctions are reconstructed elsewhere.
- Representation-level Pareto incomparability is not automatically kernel-level incomparability.

## Negative controls

The audit rejects one-way compilation as equivalence, hidden machinery as free, domain-specific features as universal commitments, lower costs as proof of necessity, and failure to find another kernel as global uniqueness.

## Reducibility control

RCCD is treated as irreducible only relative to C/P/E because every R1-R5 ablation has a W7 separating pair. No claim is made about alternative preservation contracts or non-effective representations.

## Decision

FARA, LTS-PROV, COALG-DYN, and RCCD form one commitment-equivalence class on the registered scope. The realization frontier remains non-scalar and Pareto-incomparable, while the kernel frontier contains one nontrivial class. W9 is authorized to perform terminal internal adjudication.
