# Project FAR Core Theory v1.1 — Governed Correction Audit

Date: 2026-08-27

Status: **Correction audit complete; independent review still open**

Base repository head: `ef2daad0f805ffe1386d8310875456df824c0e0d`

Base theory: `PROJECT-FAR-CORE-THEORY-1.0`

Preserved v1.0 SHA-256: `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`

Successor: `PROJECT-FAR-CORE-THEORY-1.1`

## Audit question

Do the W1 findings require rejection of the terminal theory, or a narrower versioned correction?

## Finding 1 — FAR-CORE-004 wording was overbroad/ambiguous

The v1.0 proof itself establishes incompatible minima across a constant and an injective observation contract. The machine ledger wording could instead be read as saying no representation is sufficient for every contract.

Countermodel to that reading: on fixed `X`, the identity representation is sufficient for every observation contract because it creates no collisions. It is not minimal for a constant observer.

Disposition: **clarify, do not refute**. The surviving theorem is impossibility of one representation being least-informative sufficient for every observation contract on a nontrivial domain.

## Finding 2 — FAR-CORE-010 contained an invalid direct dependency

The v1.0 definition is

`T_{L,J,I} = intersection_i Th_L(M_i)`.

`Γ` is absent. Therefore, holding `L,J,I` and the interpreted models fixed, changing `Γ` cannot change exact `T`.

The subsequent residue

`T_{L,J,I} \ Cn_L(Γ)`

does depend on `Γ`.

Disposition: **correct the dependency statement, preserve the theorem's substantive profile-relative result**.

Permanent countermodel: choose `φ` in `T` that is not logically valid, use `Γ0=∅` and `Γ1={φ}`. `T` is unchanged; the residue loses `φ` under `Γ1`.

## Finding 3 — Blackwell prior-art wording overstated relativity

Research channels used:

- Consensus scholarly search;
- Scite literature/full-text and citation-context search;
- Acumen/Talarion freshness check for recent developments;
- direct logical comparison against the canonical Project FAR claim.

Primary anchor: David Blackwell, “Equivalent Comparisons of Experiments,” *The Annals of Mathematical Statistics* 24(2), 1953, DOI `10.1214/aoms/1177729032`.

Modern corroboration located during the audit includes:

- Rauh, Banerjee, Olbrich, “Coarse-Graining and the Blackwell Order,” *Entropy* 19(10), 2017, DOI `10.3390/e19100527`;
- Hogeboom-Burr and Yüksel, “Comparison of Information Structures for Zero-Sum Games and a Partial Converse to Blackwell Ordering in Standard Borel Spaces,” DOI `10.48550/arxiv.2005.06673`.

The classical Blackwell result provides a decision-problem-uniform partial order under its stated experiment model and garbling relation. Therefore the v1.0 phrase “there is no loss-independent ranking of information structures” is not an accurate generic description of Blackwell comparison.

Disposition: **correct the prior-art characterization and make no novelty claim for the underlying comparison pattern**.

## Finding 4 — FAR-CORE-014 survives

No W1 objection refutes the bounded classification of Search-State Sufficiency as an instance of factorization under the PR #453 representation and decoder classes.

Disposition: **preserve `SUPPORTED/DERIVED`**.

## Finding 5 — terminal kernel survives

No W1 finding refutes:

- exact sufficiency iff factorization;
- existence/universality of the contract-relative observational quotient;
- incompatibility of contract-relative minima across unrestricted observation contracts;
- invariance antitonicity;
- transport triviality;
- primitive/operator count noninvariance;
- finite-panel boundary;
- omitted-parameter collision logic;
- determinate-absence/Unknown separation;
- Ω elimination under the canonical definition.

The terminal verdict therefore survives.

## Independence record

The W1 audit is not accepted as independent validation. It had prior exposure to Project FAR and the repository. The correction uses its objections as adversarial internal evidence only.

This distinction is material: a reviewer can find a real defect without satisfying the independence conditions required to upgrade assurance.

## Exact claim impact

| Claim/surface | v1.0 | v1.1 | Action |
|---|---|---|---|
| `FAR-CORE-004` | proved, ambiguous machine wording | proved, clarified | versioned correction |
| `FAR-CORE-010` | proved, incorrect direct Γ dependency sentence | proved with exact theory/residue dependency split | versioned correction |
| Blackwell prior art | understated classical uniform partial order | corrected | versioned correction |
| `FAR-CORE-014` | supported/derived | supported/derived | unchanged |
| terminal verdict | closed | closed | unchanged |
| assurance | internal, not independent | internal corrected, not independent | no upgrade |

## Next workstream

`PCA-W1-INDEPENDENT-REVIEW` remains the next workstream, now against `PROJECT-FAR-CORE-THEORY-1.1`.
