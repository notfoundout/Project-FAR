# IKD-W7 Lower-Bound Audit

## Anti-circularity controls

- The universality class C, preservation contract P, and representation family E are explicit and independently stated.
- P names facts that must be preserved; it does not require RCCD terminology, data structures, or implementation form.
- Each lower bound uses a paired countermodel that becomes indistinguishable after one ablation and a registered query or operational consequence that separates the pair.
- A component is classified as necessary only relative to C, P, and E.

## Machinery accounting

Primitive omission is not accepted as reduction when the missing distinction appears in a decoder, scheduler, proof object, adapter, canonicalizer, oracle, lookup table, certificate, or synthesis procedure. All such machinery is charged as equivalent reintroduction.

## Required negative controls

The analysis rejects transition-only commitment recovery, realized-trace admissibility recovery, conclusion-only revision recovery, current-state-only historical recovery, and source-indexed oracle recovery. It also rejects future-information access and unrestricted interpretation.

## Boundary

R5 is a lower bound on admissible effective representation, not an ontological primitive of every reasoning process. The joint result does not establish global necessity, global minimality, actual-process correspondence, or external validation.

## Decision

All five RCCD components have conditional lower bounds on the defined C/P/E scope. W8 must now test bidirectional reconstruction and recompute the non-scalar commitment frontier.
