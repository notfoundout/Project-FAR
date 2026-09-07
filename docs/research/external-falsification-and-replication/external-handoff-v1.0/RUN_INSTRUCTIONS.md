# Clean-room execution instructions

1. Copy this directory into the isolated evaluator environment.
2. Run `python verify_packet.py`. On any `INVALID PACKET`, stop; do not repair the packet inside the evaluation environment.
3. Give the evaluator only `packet.json` and the task-specific external-custodian instructions. Do not supply Project FAR proof text, implementations, expected verdicts, prior audits, chats, or repository access.
4. Require a verdict for every governed claim using the externally registered verdict vocabulary. Do not repair, reinterpret, or rescue a failing claim.
5. Save the complete report and its machine-readable ledger before unblinding.
6. Compute SHA-256 of both sealed outputs and record the environment/exposure manifest.
7. Only after sealing may the independent adjudication procedure compare against withheld evidence.

This package does not itself authorize or execute EFR-R1/R2/H1/A1/HD1/U1/C1/N1. The relevant independent custodian must fill and seal the registered input slot before that test begins.
