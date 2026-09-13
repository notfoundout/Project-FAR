# Living-research protected implementation path

Status: **Repository implementation infrastructure; not scientific authority**

This path exists for one case: governed review has already concluded that a `PROJECT_CHANGE_REQUIRED` study requires Project FAR to change, and the required change includes executable or control-plane repository surfaces that the scientific promotion path is intentionally forbidden to write.

## Dual-PR rule

A project-changing study always uses the scientific correction path. If `implementation_required` is `false`, the review sets `implementation_proposal_id` to `null` and no implementation PR is created. If `implementation_required` is `true`, the review must bind one exact `IMPLEMENTATION_PROPOSED` package and one protected authorization in `implementation-authorizations-v1.0.json`.

The resulting flow is:

`accepted study → scientific correction PR +, when required, separate implementation PR → protected review/validation → main`

The implementation PR never substitutes for the scientific correction PR and never changes scientific status by itself.

## Trust boundary

PR #490 may contain implementation proposal and payload bytes, but those bytes have no write authority. Protected `main` must first bind the exact candidate SHA-256, exact implementation proposal SHA-256, exact operation-set SHA-256, and exact canonical review-row SHA-256.

`Living Research Implementation` executes its runner and contract only from protected `main`. It freezes the exact PR #490 head and exact `main` base, reads the authorized source bytes as data, validates every target/preimage/payload hash, and materializes only the exact authorized operations into a new one-commit branch. The write-scoped job never executes the inbox payloads.

Allowed automatic implementation targets are defined in `implementation-policy-v1.0.json`. Scientific/canonical targets remain in the separate promotion policy. This keeps research intake from becoming an unreviewed software supply chain.

## Self-validation rule

If an implementation proposal changes merge-authority's own assurance surface, the implementation PR is still created automatically, but automation does not dispatch that modified assurance workflow to certify itself. The PR remains subject to independent protected review and validation of the self-change.

For implementation proposals that do not touch the declared assurance-sensitive paths, the runner may dispatch the existing protected validator-assurance workflow for the exact implementation head. It never merges the PR.

## Failure behavior

The path fails closed on missing implementation declarations, missing or malformed protected authorization, source/proposal/candidate hash drift, stale `main` preimages, payload hash drift, duplicate/colliding targets, path traversal or symlink targets, source movement, `main` movement, unsealed changed paths, or a previously closed implementation PR for the same frozen source/base.

A scheduled run is only a recovery mechanism. Acceptance/authorization changes and successful living-inbox validation are the primary triggers.

## Files

- `implementation-policy-v1.0.json` — target, source, branch, assurance-sensitive, and trust rules.
- `implementation-authorizations-v1.0.json` — protected exact-byte authority for implementation proposals.
- `tools/living_implementation_contract.py` — pure deterministic plan validator; no network/Git operations.
- `tools/materialize_living_implementation.py` — exact-byte materializer; never executes payloads.
- `tools/run_living_research_implementation.py` — protected-main transaction/orchestration runner.
- `.github/workflows/living-research-implementation.yml` — automatic implementation-PR workflow.
- `tests/test_living_implementation_contract.py` — negative controls and materialization regression coverage.

## Nonclaims

Automatic creation of an implementation PR does not establish that the underlying study is correct, that the proposed implementation is scientifically valid, that the PR should merge, or that any FAR claim has changed. Those conclusions remain governed by the scientific acceptance record and protected merge path.
