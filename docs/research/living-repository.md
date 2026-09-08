# Living Repository Architecture

Status: **Research infrastructure; no theory promotion**

Research candidate only. Discovery or triage does not establish support, dispute, novelty, priority, external validity, utility, independence, theorem status, EFR result, or any other Project FAR claim/evidence disposition.

Project FAR's living-repository architecture is a set of closed maintenance loops around the existing canonical repository. It does not replace repository governance.

## Loops

| Loop | Automatic action | Hard boundary |
|---|---|---|
| Discovery | Search current scholarly metadata every 30 minutes | Discovery is not evidence |
| Historical backfill | Walk backward through publication history and low-volume book metadata | Search absence is not novelty |
| Philosophy/metaphysics | Admit only candidates with a formal/mathematical bridge | No unconstrained worldview import |
| Identity/provenance | Deduplicate DOI/provider identities and retain query/rejection/failure records | Provider agreement is not proof |
| Claim watch | Route candidate signals to exact governed RQs and explicit FAR-CORE references | Metadata cannot falsify a theorem |
| Dependency impact | Derive reverse FAR-CORE fallout from canonical assurance dependencies | No invented dependency edges |
| Canonical drift | Hash governed theory/status/limitations/open-problem/research surfaces | Drift report is not adjudication |
| Validation | Re-run living invariants, research gates, and repository fast health | CI is assurance, not theorem proof |
| State generation | Regenerate research and repository dashboards | Generated pages are non-authoritative |
| Change control | Refresh one permanent noncanonical inbox PR from a persistent branch | No direct write to protected `main`; never merge the rolling inbox |

## Permanent inbox PR

`automation/living-research-inbox` has one deliberately permanent draft pull request. The unattended workflow rebuilds that branch as one Research-only commit on current protected `main`, carries forward only accumulated living-research data, and refreshes the already-open PR.

The branch contains `research/living/inbox/.rolling-pr-anchor.json`. The anchor exists only to keep the permanent PR non-empty immediately after a canonical snapshot promotion. It is not a candidate, evidence item, claim, or canonical research artifact and its merge policy is `NEVER_MERGE_THIS_ANCHOR`.

This architecture removes the steady-state need for GitHub Actions to create pull requests. `GITHUB_TOKEN` may update the existing PR, maintain the review-queue issue, and dispatch bounded validation, but does not need repository-wide permission to create/approve PRs and does not need an administrator token or branch-protection bypass.

If the permanent inbox PR is accidentally closed or deleted, discovery data must still be preserved on the branch and the unattended run must remain fail-closed until a human bootstraps one replacement permanent PR. The correct recovery is to recreate the permanent review surface, not to broaden automation authority.

## Canonical snapshot promotion

The permanent inbox PR is never the promotion vehicle. When Research-only state is ready to enter canonical `main`, create a separate snapshot branch from current protected `main` and copy only the reviewed living-research state intended for promotion. The snapshot must explicitly exclude `.rolling-pr-anchor.json`.

The snapshot PR then follows the ordinary protected path: normal PR-triggered checks, Exact Head Assurance, Validator Assurance / `merge-authority`, review resolution, and merge only if the exact final head is accepted. Promotion of Research-only metadata still does not change theory/evidence status merely by being merged.

After a snapshot merges, the permanent inbox remains open and the next unattended cycle rebuilds it on the new `main`, carries forward the anchor plus any unpromoted/new Research state, and continues discovery.

## Self-correction

The living repository is designed to remain falsification-responsive. If a candidate ultimately yields an exact reproducible contradiction, the system can preserve the candidate, identify the minimal affected claim set, compute downstream claim fallout, and carry a correction packet through the governed lifecycle. It is forbidden from converting a title, abstract, citation count, consensus, model vote, or search result directly into a canonical correction.

## Source strategy

Crossref is the primary incremental source because index-date windows detect newly indexed or updated metadata independent of original publication year. Historical mode instead uses publication windows.

OpenAlex is used once per scheduled historical slice as a second scholarly index. Its optional `OPENALEX_API_KEY` may increase free allowance; the engine also operates keyless and preserves rate-limit failures.

Open Library is sampled only every fourth run for historical books, with small result pages and no bulk harvesting.

## Reproducibility

Every source request is reconstructable from stored provider, query, mode, window/page, and parameters. Every returned item receives an explicit acceptance or rejection reason in the run record. Source failure freezes the affected cursor. Candidate records preserve first/last seen times and all governed bindings.

## EFR firewall

Nothing in this system executes the preregistered External Falsification and Replication program or counts as external independence. EFR inputs, freezes, tests, and external execution remain governed by their own canonical program.
