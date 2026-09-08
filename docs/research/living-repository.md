# Living Repository Architecture

Status: **Research infrastructure; no theory promotion**

Research candidate only. Discovery or triage does not establish support, dispute, novelty, priority, external validity, utility, independence, theorem status, EFR result, or any other Project FAR claim/evidence disposition.

Project FAR's living-repository architecture is a set of closed maintenance loops around the
existing canonical repository. It does not replace repository governance.

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
| Change control | Maintain a rolling PR from a persistent inbox branch | No direct write to protected `main` |

## Self-correction

The living repository is designed to remain falsification-responsive. If a candidate ultimately
yields an exact reproducible contradiction, the system can preserve the candidate, identify the
minimal affected claim set, compute downstream claim fallout, and carry a correction packet through
the governed lifecycle. It is forbidden from converting a title, abstract, citation count,
consensus, model vote, or search result directly into a canonical correction.

## Source strategy

Crossref is the primary incremental source because index-date windows detect newly indexed or
updated metadata independent of original publication year. Historical mode instead uses publication
windows.

OpenAlex is used once per scheduled historical slice as a second scholarly index. Its optional
`OPENALEX_API_KEY` may increase free allowance; the engine also operates keyless and preserves
rate-limit failures.

Open Library is sampled only every fourth run for historical books, with small result pages and no
bulk harvesting.

## Reproducibility

Every source request is reconstructable from stored provider, query, mode, window/page, and
parameters. Every returned item receives an explicit acceptance or rejection reason in the run
record. Source failure freezes the affected cursor. Candidate records preserve first/last seen
times and all governed bindings.

## EFR firewall

Nothing in this system executes the preregistered External Falsification and Replication program or
counts as external independence. EFR inputs, freezes, tests, and external execution remain governed
by their own canonical program.
