# IKD-W8: Minimal-Frontier Recalculation

## Question

After the W7 lower bounds are incorporated, do FARA, LTS-PROV, COALG-DYN, and RCCD represent distinct necessary kernels or different realizations of one kernel?

## Method

The comparison is bidirectional and commitment-based. For each successful architecture, the analysis asks:

1. whether RCCD plus declared domain parameters reconstructs the architecture;
2. whether the architecture recovers all five lower-bounded RCCD distinctions;
3. whether either direction relies on hidden decoders, schedulers, canonicalizers, proof objects, or interpretation machinery;
4. whether any architecture carries an additional commitment required across the entire class C;
5. whether any RCCD component can be removed while retaining preservation contract P within effective representation family E.

No scalar score or winner is used. Representation costs and commitments remain separate.

## Bidirectional result

FARA, LTS-PROV, and COALG-DYN are each reconstructible from RCCD plus domain-specific parameters. In the reverse direction, each recovers:

- recoverable commitment content;
- constrained admissible evolution;
- dependency-sensitive revision;
- historical identity and supersession;
- one effective bounded recovery interface.

The reconstruction directions require explicit machinery, and that machinery is charged. None introduces a sixth commitment that is necessary across every successful architecture.

## Equivalence class

The four structures form one commitment-equivalence class:

`CEC-RCCD-001 = {RCCD-001, FARA-001, LTS-PROV-001, COALG-DYN-001}`

The architectures remain different representations and may have different implementation costs. Their differences do not establish different necessary kernels on the registered scope.

## Reducibility

RCCD cannot be reduced below R1-R5 while preserving P on C within E. W7 supplies a separating pair for each attempted ablation. Any successful omission reconstructs the missing distinction through charged machinery and is therefore commitment-equivalent rather than strictly weaker.

## Additional commitments

Global proof objects, primitive causality, primitive probability, primitive temporal continuity, primitive agency, and primitive modality were tested as possible additional essentials. None is required across all successful architectures. Each is domain-specific, derivable, or absent from at least one faithful realization.

## Frontier result

At the kernel level, the frontier contains one nontrivial class: `CEC-RCCD-001`.

At the realization level, FARA, LTS-PROV, and COALG-DYN remain Pareto-incomparable implementations. This no longer implies multiple incomparable kernels because their required commitments are bidirectionally equivalent.

## Boundary

The result is restricted to C, P, and E. It does not establish unrestricted universality, actual-process correspondence, held-out cross-context success, or independent external validation.

## Next step

W9 must issue the internal terminal adjudication. It must either state the bounded RCCD universality theorem supported by W1-W8 or downgrade the result if a remaining blocking contradiction is found.
