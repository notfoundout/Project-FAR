# Native contract: formal logic

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

For a fixed propositional language and a fixed consequence query, does a summary of a theory determine the answer to that query? Feitosa and D'Ottaviano model logics using consequence relations and translations using consequence preservation; conservative translation strengthens the preservation requirement [feitosa2001conservative]. The bounded contract here tests a consequence observation directly. It does not purport to instantiate or refute their general translation results.

## Finite fragment

Let valuations assign Boolean values to `p` and `q`. Let `T1 = {p}` and `T2 = {p, q}`. The declared behavior is the Boolean answer to `T |= q` under ordinary propositional semantics.

The deliberately lossy summary is only `satisfiable(T)`. Both theories are satisfiable, but `T1` does not entail `q` and `T2` does. The summary therefore does not determine the declared consequence behavior.

The repaired carrier is the explicit model set of each theory over `{p,q}`. The decoder returns true exactly when every listed model makes `q` true. This repair is sufficient for these two theories and this one query.

## Scope boundary

The case universe contains exactly `T1` and `T2`; the only observation is entailment of `q`; syntax, proof identity, other formulas, nonclassical semantics, and arbitrary translations are outside scope. No minimality or universality is claimed.
