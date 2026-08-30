# Native contract: Bayesian/causal reasoning

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

Do two finite causal models that induce the same observational joint distribution also agree under a declared intervention? Blackwell's comparison of experiments is retained as background for decision-relative comparison [blackwell1953equivalent]. The operative causal source is Beckers and Halpern: their abstraction relations explicitly range over allowed interventions and compare the induced distributions [beckers2019abstracting].

## Finite models

Let `U ~ Bernoulli(1/2)` and `X,Y` be Boolean.

- `MXtoY`: `X := U`, `Y := X`.
- `MYtoX`: `Y := U`, `X := Y`.

Both observational distributions place probability `1/2` on `(X,Y)=(0,0)` and `1/2` on `(1,1)`. The declared behavior is `P(Y=1 | do(X=0))`. It is `0` in `MXtoY` and `1/2` in `MYtoX`.

The deliberately lossy carrier is the observational joint distribution alone. The repaired carrier adds the response distribution for the single allowed intervention `do(X=0)`. A decoder reads the probability mass with `Y=1` from that response distribution.

## Scope boundary

The case universe is these two recursive Boolean structural models with the stated exogenous distribution. Only one intervention and one scalar behavior are declared. The repair is not a complete causal abstraction, identifiability result, or minimal intervention set.
