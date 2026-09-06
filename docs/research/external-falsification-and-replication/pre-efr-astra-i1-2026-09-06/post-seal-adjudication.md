# Project FAR Clean-Room Audit — Post-Seal Adjudication Addendum

Status: FINAL SUPPLEMENTAL ADJUDICATION  
Clean-room run classification: I1  
Clean-room report SHA-256: `9c354031c7b944e89fdb17db50d03b7cc79f659df21cf50fe16df8f75cc10a1d`  
Original clean-room packet SHA-256: `3b99dfc4f7ef220e518d6984c13d00eb10380024f135e53e1360d504e73821e5`  
Uploaded audit bundle SHA-256: `eff1a5a815a10ba73aa41b130a300702ac37dfce48fbcf9da7a019bcffacc2c9`  
Uploaded verdict ledger SHA-256: `54b34cc1c3098cbc79ffd223d99335725f8d908d70d62fa1f9edc963098b7fee`

## Preservation rule

The sealed clean-room result is not rewritten:

- 12 `SURVIVES-ATTACK`
- 0 `FALSIFIED`
- 2 `INDETERMINATE`
- `FAR-CORE-010` and `FAR-CORE-014` were marked `PACKET_DEFECT`.

This addendum is a later adjudication of those packet defects. It is not part of the sealed clean-room run and does not upgrade its isolation class.

## FAR-CORE-010

**Post-seal disposition: SURVIVES-ADJUDICATION.**

The packet combined a fixed-parameter scope clause with a sentence about changing those same parameters, creating a self-conflict in the supplied statement. Canonical v1.1 governance resolves the dependency split:

- exact common theory `T_{L,J,I}` depends directly on `L`, interpreted profiles/models `J`, and target class/index `I`;
- frame-subtracted residue additionally depends on `Γ`;
- changing `Γ` alone while `L,J,I` and interpreted models remain fixed cannot change exact `T`.

The clean-room evaluator therefore correctly identified a packet defect rather than a theorem counterexample.

## FAR-CORE-014

**Post-seal disposition: SURVIVES-ADJUDICATION.**

The packet omitted the exact bounded SSS representation/decoder definitions needed for an independent reproduction. Canonical PR #453 materials define:

- individual-sequent state with the rule-induced projected relation;
- the four uniform monotone successor-set decoders;
- explicit finite MLL witnesses refuting all four decoders for the projected relation;
- resource-labelled hyperedges preserving the joint premise family;
- frontier-multiset state with a binary expansion relation sufficient for finitary rule systems.

These are exactly the bounded representation/decoder classes needed to instantiate the factorization/sufficiency framework. The same source explicitly denies a universal operator-architecture interpretation. Existing W2 formalization separately records the bounded SSS/MLL witness bridge as machine-checked.

The clean-room evaluator's `INDETERMINATE` verdict therefore reflects missing packet inputs, not a surviving contradiction.

## Combined disposition

For theorem-defect triage after adjudication:

- 14/14 claims: no surviving contradiction identified.
- 0/14 claims: falsified.
- 12/14 claims: independently reproduced within the sealed I1 packet run.
- 2/14 claims: resolved only by post-seal canonical-source adjudication.
- The sealed run remains I1 and must not be relabeled as 14/14 clean-room replication, I2, I3, or EFR execution.

## Rerun decision

No rerun is required for Project FAR internal assurance or to determine whether the sealed run exposed a core-theory contradiction.

A rerun is required only if the desired evidence claim is specifically: **one clean-room evaluation independently reproduced all 14 claims from a complete statement-only packet.**
