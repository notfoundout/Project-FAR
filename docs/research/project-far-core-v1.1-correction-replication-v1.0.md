# Project FAR Core v1.1 Correction Replication v1.0

Status: **Research — internal replication complete**

Date: 2026-08-27

Target: `PROJECT-FAR-CORE-THEORY-1.0`

Successor candidate: `PROJECT-FAR-CORE-THEORY-1.1`

This record exists to make the Research Execution Charter lifecycle explicit. It is not independent review and must not be cited as satisfying `PCA-W1-INDEPENDENT-REVIEW`.

## Question

Are the W1 objections to `FAR-CORE-004`, `FAR-CORE-010`, and the Blackwell prior-art paragraph reproducible from the frozen v1.0 artifact and external primary literature without treating the W1 conclusion itself as a premise?

## Execution

### R1 — FAR-CORE-004

Use a two-element set `X={x0,x1}` and the identity representation `rho(x0)=r0`, `rho(x1)=r1`.

Evaluate two exact behavior maps:

- `beta_const(x0)=beta_const(x1)=v`;
- `beta_inj(x0)=v0`, `beta_inj(x1)=v1`, with `v0 != v1`.

For each behavior map, test the factorization criterion `beta = delta o rho`. Then compare the identity representation with the observational quotient induced by each behavior map.

### R2 — FAR-CORE-010

Hold `L`, `J`, `I`, and all interpreted models `M_i` fixed. Let `phi` be a non-logically-valid sentence in the exact common theory

`T_{L,J,I}=intersection_i Th_L(M_i)`.

Compare frames `Gamma0=emptyset` and `Gamma1={phi}`. Evaluate exact `T` and the frame-subtracted residues `T \ Cn_L(Gamma0)` and `T \ Cn_L(Gamma1)`.

### R3 — Blackwell prior art

Query scholarly sources independently of the Project FAR prose for the classical comparison-of-experiments result. Check whether Blackwell comparison is tied to one selected loss function or quantifies uniformly over a class of decision problems.

Research channels used during replication:

- Consensus scholarly search;
- Scite literature/full-text/citation-context search;
- Acumen/Talarion freshness check for later developments;
- direct inspection of the cited theorem statement and Project FAR wording.

Primary source anchor: David Blackwell, “Equivalent Comparisons of Experiments,” *The Annals of Mathematical Statistics* 24(2), 1953, DOI `10.1214/aoms/1177729032`.

Corroborating sources used: DOI `10.3390/e19100527` and DOI `10.48550/arxiv.2005.06673`.

## Observations

### O1

The identity representation admits a decoder for both the constant and injective behavior maps. Therefore it is sufficient for both contracts.

For the constant observer, the observational quotient has one class and is strictly less informative than identity. For the injective observer, the quotient is identity up to isomorphism.

### O2

Changing `Gamma0` to `Gamma1` leaves `T_{L,J,I}` unchanged because the frame is absent from the definition and the interpreted models were held fixed. The residue changes because `phi` is removed by `Cn_L(Gamma1)` but not by `Cn_L(Gamma0)`.

### O3

The classical Blackwell order compares experiments uniformly over decision problems in its stated setup and is characterized by garbling in the standard finite formulation. The v1.0 generic phrase that there is “no loss-independent ranking of information structures” therefore overstates the relativity result.

The freshness check located no 2025–2026 development requiring a different correction.

## Discovery replicated

1. `FAR-CORE-004` must distinguish universal sufficiency from simultaneous universal least-informativeness/minimality.
2. `FAR-CORE-010` must distinguish the direct indices of exact common theory (`L,J,I`/models) from the additional frame index of the frame-subtracted residue.
3. The Blackwell paragraph must acknowledge the classical decision-problem-uniform partial order and limit Project FAR's prior-art/novelty language accordingly.
4. None of these replicated defects refutes the surviving terminal kernel or `FAR-CORE-014`.

## Reproduction artifacts

Machine-readable permanent fixtures:

- `theory/evaluation/project-far-core-theory-v1.1-regressions.json`

Executable validator/tests:

- `tools/check_project_far_theory_closure.py`
- `tests/test_project_far_theory_closure.py`

These artifacts independently recompute the elementary countermodels instead of accepting prose labels.

## Replication disposition

`REPLICATED_INTERNAL`.

The correction findings are reproducible and therefore eligible for Acceptance/Promotion under the Charter. The replication is internal and does **not** improve evaluator-independence assurance.
