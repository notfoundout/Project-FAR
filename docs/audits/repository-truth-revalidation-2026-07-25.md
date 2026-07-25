# Repository truth revalidation

Tracking issue: #370  
Parent program: #364  
Original audit IDs: 13 and 23–25

## Method

Current `main` was treated as the object of review. Historical audits, generated dashboards, archived files, and frozen research artifacts were treated as evidence about their own bounded context, not automatically as present repository truth.

The review separated package-version authority, executable mirrors, current project status, historical generated status, GitHub release authority, and claim boundaries.

## Authoritative inventory

| Declaration | Classification | Authority rule |
|---|---|---|
| `pyproject.toml:[project].version` | canonical package version | sole installable-package version authority |
| `mechanization/far_mechanization/__init__.py:__version__` | executable mirror | must equal package authority |
| `mechanization/far_mechanization/cli.py:CLI_VERSION` | CLI mirror | must equal package authority |
| GitHub latest release | canonical repository release | currently `v1.0.0`; distinct from package version |
| `docs/releases/project-far-v1.0.0.md` | repository release record | must identify and link the canonical GitHub release |
| `README.md` Central result and Post-terminal phase | canonical current-status surface | defines current repository phase and boundary |
| README generated REP/ADJ/W3.5 block | historical generated surface | cannot claim current status |

Machine-readable authority: `governance/repository-truth-authority-v1.json`.

## Correction to the original revalidation

The initial PR #371 incorrectly inferred that `v0.4.0` was the latest GitHub release from the newest local file under `docs/releases/`. That inference was invalid: a local release-document inventory is not the GitHub release authority. The latest published repository release is `v1.0.0`.

The hotfix corrects the README, authority manifest, release record, checker, tests, and audit language. The package version remains `0.6.0`; repository release and package version are intentionally separate version surfaces.

## Confirmed defects and fixes

1. The README and audit falsely identified `v0.4.0` as the latest repository release. They now identify `v1.0.0`.
2. The authority manifest now records an explicit latest-release value and release record instead of inferring release state from local filenames.
3. The checker now fails closed when the README badge, heading, release link, manifest, or release record disagree.
4. The historical W3.5 dashboard remains explicitly historical and cannot override the canonical post-terminal phase.
5. Package-version mirrors remain required to equal `pyproject.toml`.

## Original-ID dispositions

| Original ID | Disposition | Evidence |
|---|---|---|
| 13 | resolved | status-surface ambiguity corrected and generator constrained |
| 23 | resolved | package-version authorities inventoried and enforced |
| 24 | resolved after hotfix | latest release corrected to `v1.0.0`; release authority now explicit and tested |
| 25 | resolved | historical/generated status declarations classified and prevented from overriding current authority |

## Enforcement

`python tools/check_repository_truth.py` verifies package-version equality, canonical post-terminal language, historical dashboard labeling, exact release authority `v1.0.0`, the latest-release route, and the canonical release record.

`tests/test_repository_truth.py` includes positive, package-version drift, historical-status mutation, release-badge drift, and release-record drift cases.

## Boundaries

This revalidation does not establish external validation, formal end-to-end completion, certification, commercial readiness, enterprise readiness, or correctness of historical research claims. It establishes repository authority separation and deterministic detection of the listed drift classes.
