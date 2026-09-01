# `far-ir/2.1` Approximation and Cost Contract

Status: **Accepted for PCA-W5 finite-explicit operational semantics**

`far-ir/2.1` is an additive successor. It does not modify or reinterpret `far-ir/2.0` or `far-ir/1.0`. Its checked scope is finite explicit tables with exact nonnegative rational arithmetic.

## Frozen semantics

An approximate record declares all of the following inside the hash-bound contract:

1. a total finite metric table, checked for identity, separation, symmetry, and triangle inequality;
2. a finite probability mass over every source case (the reference semantics);
3. either reference-weighted expected aggregation or worst-case (`maximum`) aggregation;
4. a total decision-loss table over the behavior range and action set, checked here to equal the declared metric on those values;
5. an explicit nonnegative rational tolerance;
6. randomized decoder distributions for each used representation value; and
7. one or more separately named, minimize-only cost coordinates defining a product preorder.

For candidate decoder `d`, case `x`, required behavior `β(x)`, representation `r(x)`, and action `a`, case loss is

`L_d(x) = Σ_a d(a | r(x)) loss(β(x), a)`.

The aggregate is either `Σ_x μ(x)L_d(x)` or `max_x L_d(x)`. A candidate is feasible exactly when its aggregate is at most the frozen tolerance.

## Cost conclusions

Costs are not silently scalarized. Candidate `a` is below `b` exactly when it is no greater on every declared coordinate. A feasible candidate is Pareto-minimal when no other feasible candidate strictly dominates it. A least element must be below every feasible candidate. Consequently, multiple incomparable Pareto minima may exist while no least element exists.

## Exact boundary

Because the checked loss is a separating metric and reference weights are explicit, the verifier reports exact recovery only when every case has zero expected loss. At zero tolerance the fixture's feasible set is recomputed to equal its exact-recovery set. This boundary is finite and operational; it is not a theorem about arbitrary measures, pseudometrics, unrepresented cases, or all representations.

## Boundaries

The verifier does not establish external-domain correspondence, a universally preferred reference distribution, universal scalar cost, unique optimum, open-domain approximation, computational complexity, novelty, empirical utility, or W6 claims. Different metrics, references, aggregators, tolerances, action sets, candidate universes, or cost coordinates define different contracts.
