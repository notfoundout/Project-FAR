# EFR external handoff v1.0

Status: **frozen handoff package; EFR not executed**.

This directory is the self-contained Project FAR → external-custodian handoff for independent falsification/replication work. It does not execute any registered EFR test and does not establish I3, novelty, priority, human utility, field utility, or product value.

The scientific evidence baseline is commit `195fc079d0a8993e4db3e063e09cf45d0bcd78c2`, tree `a01517ed65f45e62b3d47ffba9dc955fff2bae9b`.

Before any derivation, run:

```bash
python verify_packet.py
```

Proceed only if the first line begins `VALID PACKET`. During derivation, use only `packet.json`. Do not access Project FAR's repository, chats, prior audits, proof sources, implementations, expected outputs, external copies, or withheld material. If the environment does not technically enforce isolation, the run cannot be promoted above I1 merely because the evaluator followed an instruction.

The packet fixes the two defects found by the 2026-09-06 pre-EFR I1 exercise: FAR-CORE-010 now separates exact `T_{L,J,I}` from the `Γ`-relative residue without contradictory fixed/varying wording; FAR-CORE-014 now carries the complete bounded state/transition/decoder/witness surface from the frozen authoritative source rather than relying on PR #453.

After evaluation, save the complete report and compute its SHA-256 **before** viewing or releasing withheld material. External custodians must separately satisfy the registered EFR intake, identity/exposure, sealing, timing, and adjudication rules. This package is necessary handoff material, not proof that those conditions have been met.
