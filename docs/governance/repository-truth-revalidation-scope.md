# Repository hygiene and status/version truth revalidation

Tracking issue: #370
Parent program: #364
Original audit IDs: 13 and 23–25

## Objective

Revalidate the current repository rather than repeating historic audit assertions. Establish which version and status declarations are authoritative, identify contradictions or stale declarations, and add deterministic checks only where a current defect is confirmed.

## Evidence rules

- Treat current `main` content as the object under test, not as automatically correct.
- Preserve every original audit ID and record one evidence-backed disposition for each.
- Distinguish current defects from stale audit findings, duplicates, and historic snapshots.
- Do not rewrite broad documentation merely to create superficial consistency.
- Every correction must identify its authority, affected files, and failure mode.

## Required inventory

The PR must inventory and classify at least:

- package and CLI versions;
- schema and interchange-format versions;
- framework/foundation/theory version declarations;
- project status, roadmap, release, and readiness declarations;
- canonical architecture and dependency declarations;
- generated or frozen artifacts that embed versions or status;
- archived material that could be mistaken for current authority.

## Required implementation

Before merge:

1. produce a machine-readable authority inventory;
2. produce an evidence-backed disposition for IDs 13 and 23–25;
3. identify confirmed contradictions, stale declarations, duplicates, or orphaned authorities;
4. correct only confirmed defects;
5. add deterministic tests for the frozen authority rules;
6. preserve explicit claim boundaries and historical context;
7. pass the complete observable repository CI surface.

## Non-goals

This PR does not alter FAR theory, execute the frozen SWE-agent case, establish external validation, or claim commercial, enterprise, security, or formal readiness.
