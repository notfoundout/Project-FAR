# Claude blind hostile-review protocol

Status: **PRE-EFR MODEL ASSURANCE ONLY — NOT EFR EXECUTION — NOT I2 — NOT I3**

Input: only `r1-statement-only.json` after `verify_packet.py` passes.

Claude must not access Project FAR's repository, chats, prior audits, proofs, Lean proof bodies,
implementations, expected outputs, or external copies, and must not browse during derivation.
For every `FAR-CORE-001` through `FAR-CORE-014`, bind the exact supplied scope and claim,
then return exactly one of `SURVIVES-ATTACK`, `FALSIFIED`, or `INDETERMINATE` with a
self-contained derivation or reproducible counterexample/countermodel. Do not repair a claim.

Before any unblinding, save the complete report and record its SHA-256. A Project-FAR-controlled
Claude run is internal model assurance only. If technical isolation is not enforced it is at most
I1-style claimed isolation. It is never independent external replication.
