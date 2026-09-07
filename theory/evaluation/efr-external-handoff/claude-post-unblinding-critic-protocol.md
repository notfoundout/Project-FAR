# Claude post-unblinding critic protocol

Status: **PRE-EFR MODEL ASSURANCE ONLY — NOT EFR EXECUTION — NOT I2 — NOT I3**

Prerequisites:
1. the blind report is sealed and SHA-256 recorded;
2. `verify_packet.py` passed before the blind run;
3. the blind report hash cannot be changed during adjudication.

Only after sealing may Claude receive the withheld Project FAR proof/review material. Compare each
blind derivation with the governed source and classify discrepancies as:
`REVIEWER_ERROR`, `PACKET_DEFECT`, `GOVERNING_DEFECT`, or `UNRESOLVED`.
Do not overwrite the blind verdict. Record dependency fallout separately. A packet defect triggers
packet repair and a new separately identified blind run; it never converts a failed blind result
into external validation.
