# Protocol Amendment 002 — Exact Prompts and Confirmatory Scoring

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Applies to: clean-room protocol v1.3

This amendment is normative and closes exact-head review defects.

1. `execution-prompts-v1.0.json` is the sole A1, A2, and B1 prompt authority. `verify_program_freeze.py` deterministically computes each normalized prompt SHA-256. Every run must record prompt ID, computed prompt digest, packet/input digest, output digest, model/provider/version, tools, accessible context, operator, timing, and independence label. A mismatch invalidates the run.
2. `validation-and-challenge-protocol-v1.0.md` is the sole authority for construction, pre-exposure freeze, reveal, execution, scoring, stopping, failure, and claim impact for the 12 validation cases and six challenge classes.
3. `verify_program_freeze.py` rejects symlinks in every governed path component before hashing and checks exact Git blob identities for the non-self-referential control core.
4. The original `audit-manifest-v1.0.json` payload is immutable historical evidence. `audit-manifest-v1.1.json` is the current audit authority.

Where v1.3 or another same-program artifact is silent or inconsistent on these points, this amendment controls. Execution remains blocked.
