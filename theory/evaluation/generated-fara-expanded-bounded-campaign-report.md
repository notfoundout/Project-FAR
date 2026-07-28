# Expanded bounded FARA executable campaign

Status: Research

Base: `b05e48f204e273938ef406168b83cafc0958f9a0`. Maximum carrier size: **4**.

## Executed relation axes

- arity 1: 31 concrete interpretations constructed, admitted, and evaluated; rejected=0; execution digest `cb6d9eceb87c305a911cd5c43d07114cca76d637b15d95b725fcbfd787168a14`; result digest `57b73a9bd7055aca025063500bc4fad31d0114b11b138369096fe4bf3f08560a`
  - carrier 0: constructed=1, admissible=1, evaluated=1, rejected=0, paired-reduct=0
  - carrier 1: constructed=2, admissible=2, evaluated=2, rejected=0, paired-reduct=2
  - carrier 2: constructed=4, admissible=4, evaluated=4, rejected=0, paired-reduct=4
  - carrier 3: constructed=8, admissible=8, evaluated=8, rejected=0, paired-reduct=8
  - carrier 4: constructed=16, admissible=16, evaluated=16, rejected=0, paired-reduct=16
- arity 2: 66067 concrete interpretations constructed, admitted, and evaluated; rejected=0; execution digest `fca3ec35910a7008c39e8ccf27e7622e585b13cd11cdfa08478e2b103e6e227e`; result digest `2bd756ac8b4265813635f3f3b53fdf8d3656ae693148d5f798f71372a98e3b0c`
  - carrier 0: constructed=1, admissible=1, evaluated=1, rejected=0, paired-reduct=0
  - carrier 1: constructed=2, admissible=2, evaluated=2, rejected=0, paired-reduct=2
  - carrier 2: constructed=16, admissible=16, evaluated=16, rejected=0, paired-reduct=16
  - carrier 3: constructed=512, admissible=512, evaluated=512, rejected=0, paired-reduct=512
  - carrier 4: constructed=65536, admissible=65536, evaluated=65536, rejected=0, paired-reduct=65536

## Paired-reduct coverage

- Object: supported bounds [1, 2, 3, 4]; unsupported bounds [0]
- Property: supported bounds [1, 2, 3, 4]; unsupported bounds [0]
- Relation: supported bounds [1, 2, 3, 4]; unsupported bounds [0]
- Representation: supported bounds [1, 2, 3, 4]; unsupported bounds [0]
- Interpretation: supported bounds [1, 2, 3, 4]; unsupported bounds [0]
- Investigation: supported bounds [0, 1, 2, 3, 4]; unsupported bounds []
- ReasoningCalculus: supported bounds [0, 1, 2, 3, 4]; unsupported bounds []

The campaign contains 30 independently revalidated witnesses (60 models). It makes no unsupported size-0 claim for Object, Property, Relation, Representation, or Interpretation.

## Upstream reruns

- foundation executions: 57
- ablations: 21 (336 executions)
- round trips: 12
- dominance edges: `[["many-sorted-relational", "algebraic-state-transition"]]`
- terminal result: **multiple foundations remain Pareto-incomparable**

## Historical preservation

All six historical artifacts are pinned to immutable Git blob identities from `b05e48f204e273938ef406168b83cafc0958f9a0`. `--write` refuses to regenerate evidence if any current blob differs.

## Boundary

Oracle, continuous, hybrid, and embodied cases remain Unknown. Results are confined to the declared finite independent axes; full-signature cross-products and carriers above four are untested.

## Nonclaims

- no universality claim
- no uniqueness claim
- no global superiority claim
- no global minimality claim
- no necessity claim
- no completeness claim
- no inference beyond the explicit finite bounds and target-specific support coverage
- no independent-replication claim
