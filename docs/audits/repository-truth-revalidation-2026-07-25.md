# Repository truth revalidation

Tracking issue: #370  
Parent program: #364  
Original audit IDs: 13 and 23–25

## Method

Current `main` was treated as the object of review. Historical audits, generated dashboards, archived files, and frozen research artifacts were treated as evidence about their own bounded context, not automatically as present repository truth.

The review separated:

- package-version authority;
- executable version mirrors;
- current project-status authority;
- historical generated status surfaces;
- repository release navigation;
- claim and readiness boundaries.

## Authoritative inventory

| Declaration | Classification | Authority rule |
|---|---|---|
| `pyproject.toml:[project].version` | canonical package version | sole package-version authority |
| `mechanization/far_mechanization/__init__.py:__version__` | executable mirror | must equal package authority |
| `mechanization/far_mechanization/cli.py:CLI_VERSION` | CLI mirror | must equal package authority |
| `README.md` Central result and Post-terminal phase | canonical current-status surface | defines current repository phase and boundary |
| README generated REP/ADJ/W3.5 block | historical generated surface | may report its bounded program only; cannot claim current status |
| GitHub releases index | release-navigation surface | does not define package metadata version |
| frozen, archived, generated, and research artifacts | bounded evidence | authoritative only for their declared frozen scope |

Machine-readable authority: `governance/repository-truth-authority-v1.json`.

## Confirmed defects and fixes

1. The README release badge linked directly to `v0.4.0` while the package authority and executable mirrors declare `0.6.0`. This created a stale implied release/version relationship. The badge now links to the releases index without claiming equivalence.
2. The historical generated dashboard was preceded by a disclaimer but still used the literal declaration `Current project phase: W3.5`. This contradicted the later canonical post-terminal phase. The block is now explicitly historical throughout.
3. No package-version mismatch existed among the three active declarations. A deterministic checker was added so future drift fails closed.

## Original-ID dispositions

| Original ID | Disposition | Evidence |
|---|---|---|
| 13 | resolved | confirmed status-surface ambiguity corrected; deterministic status authority check added |
| 23 | resolved | version-bearing authorities inventoried and enforced |
| 24 | resolved | stale release-tag implication removed; release and package-version authorities separated |
| 25 | resolved | historical/generated status declarations classified and prevented from overriding current authority |

## Enforcement

`python tools/check_repository_truth.py` verifies:

- the authority-manifest schema;
- equality of package and executable version declarations;
- presence of the canonical post-terminal status language;
- explicit historical labeling of the older W3.5 dashboard;
- absence of the stale `v0.4.0` release pin;
- absence of any historical W3.5 declaration presented as current.

`tests/test_repository_truth.py` includes positive, version-drift, historical-status mutation, and stale-release mutation cases.

## Boundaries

This revalidation does not establish external validation, formal end-to-end completion, certification, commercial readiness, enterprise readiness, or correctness of historical research claims. It establishes only repository authority separation and deterministic detection of the confirmed status/version drift classes.
