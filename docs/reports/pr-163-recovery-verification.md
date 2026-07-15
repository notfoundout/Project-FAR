# PR 163 Recovery Verification

The recovery branch is based on current `main` and contains only the scoped-status work that was absent after PR 163 became redundant.

Static verification performed during recovery:

- compared `main` with `backup/pr-163-pre-conflict-resolution`;
- confirmed T-001 and T-002 already existed in the theorem catalog but lacked the stronger conditional wording in metadata and summaries;
- confirmed VI-002 retained contradictory `Completed` / `PASS (Provisional)` language despite its canonical `Research` status;
- confirmed VI-003 lacked the explicit relationship to T-002;
- confirmed the open-question register lacked separate conditional and global questions;
- restored the scope-aware status-consistency checker and its regression test.

The pull-request CI remains the authoritative executable verification.
