# Worked FAR Encodings

## Purpose

This document gives full FAR encodings of five reasoning examples.

Each example uses:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

---

# Example 1 — Syllogism

## Source Reasoning

1. All humans are mortal.
2. Socrates is human.
3. Therefore Socrates is mortal.

## FAR Encoding

### I — Investigation

Determine whether the conclusion `Socrates is mortal` follows from the two premises.

### Rep — Representations

- `r1`: All humans are mortal.
- `r2`: Socrates is human.
- `r3`: Socrates is mortal.

### S — Representational Structure

- `r1` supports `r3`.
- `r2` supports `r3`.
- `r3` depends on `{r1, r2}`.

### Int — Interpretation

- Domain: persons or beings under discussion.
- `Human(x)`: x is human.
- `Mortal(x)`: x is mortal.
- `Socrates`: named individual.
- `r1`: For every x, if Human(x), then Mortal(x).
- `r2`: Human(Socrates).
- `r3`: Mortal(Socrates).

### C — Reasoning Calculus

Classical first-order inference using universal instantiation and modus ponens.

### T — Reasoning Trace

- `t1`: instantiate `r1` for Socrates: Human(Socrates) -> Mortal(Socrates).
- `t2`: apply modus ponens using `r2` and `t1`.
- `t3`: derive `r3`.

## Result

The conclusion is admissible under the supplied calculus.

---

# Example 2 — Bayesian Update

## Source Reasoning

A hypothesis `H` has prior probability `P(H) = 0.2`. Evidence `E` is observed. Suppose `P(E|H) = 0.9` and `P(E|not-H) = 0.3`. Update the probability of `H`.

## FAR Encoding

### I — Investigation

Determine the posterior probability of `H` after observing `E`.

### Rep — Representations

- `r1`: `P(H) = 0.2`.
- `r2`: `P(E|H) = 0.9`.
- `r3`: `P(E|not-H) = 0.3`.
- `r4`: `E` is observed.
- `r5`: `P(H|E)`.

### S — Representational Structure

- `r1`, `r2`, `r3`, and `r4` jointly determine `r5`.
- `r5` depends on Bayes' rule.

### Int — Interpretation

- `H`: target hypothesis.
- `E`: observed evidence.
- probabilities are real values in `[0,1]`.

### C — Reasoning Calculus

Bayesian conditionalization:

```text
P(H|E) = [P(E|H)P(H)] / [P(E|H)P(H) + P(E|not-H)P(not-H)]
```

### T — Reasoning Trace

- `t1`: compute `P(not-H) = 0.8`.
- `t2`: compute numerator: `0.9 * 0.2 = 0.18`.
- `t3`: compute denominator: `(0.9 * 0.2) + (0.3 * 0.8) = 0.42`.
- `t4`: compute posterior: `0.18 / 0.42 = 0.428571...`.
- `t5`: set `r5 = P(H|E) ≈ 0.429`.

## Result

The posterior probability is approximately `0.429` under the supplied probability assignments.

---

# Example 3 — Legal Argument

## Source Reasoning

A law prohibits parking in a marked fire lane. A car was parked in a marked fire lane. Therefore the car violated the rule.

## FAR Encoding

### I — Investigation

Determine whether the car violated the stated parking rule.

### Rep — Representations

- `r1`: Parking in a marked fire lane is prohibited.
- `r2`: The car was parked in a marked fire lane.
- `r3`: The car violated the parking rule.

### S — Representational Structure

- `r1` supplies the rule.
- `r2` supplies the fact.
- `r3` depends on applying `r1` to `r2`.

### Int — Interpretation

- `marked fire lane`: a designated restricted zone.
- `prohibited`: not permitted by the rule.
- `violated`: conduct satisfies the prohibited condition.

### C — Reasoning Calculus

Rule application:

```text
If rule prohibits action A under condition X,
and actor performed A under condition X,
then violation follows unless an exception applies.
```

No exception is represented.

### T — Reasoning Trace

- `t1`: identify prohibited condition from `r1`.
- `t2`: match fact `r2` to prohibited condition.
- `t3`: check represented exceptions: none.
- `t4`: derive `r3`.

## Result

The conclusion is admissible under the supplied legal-rule calculus.

---

# Example 4 — Scientific Claim

## Source Reasoning

A metal rod is heated. It expands. Repeated trials show the same pattern. Infer that heating this rod type tends to cause expansion under the tested conditions.

## FAR Encoding

### I — Investigation

Determine whether the observed pattern supports the claim that heating this rod type tends to cause expansion under the tested conditions.

### Rep — Representations

- `r1`: Rod type `M` is heated under condition set `K`.
- `r2`: Rod type `M` expands after heating under `K`.
- `r3`: Repeated trials show the same pattern.
- `r4`: Heating rod type `M` under `K` tends to cause expansion.

### S — Representational Structure

- `r1` and `r2` form an observation pair.
- `r3` aggregates repeated observation pairs.
- `r4` depends on `r1`, `r2`, `r3`, and the causal-inference standard supplied by `C`.

### Int — Interpretation

- `heated`: temperature is increased by the procedure.
- `expands`: measured length increases beyond the measurement threshold.
- `condition set K`: controlled test conditions.
- `tends to cause`: supports a defeasible causal generalization under `K`.

### C — Reasoning Calculus

Empirical causal-support rule:

```text
If intervention-like condition X is repeatedly followed by outcome Y under controlled conditions K,
and no represented defeater explains Y better,
then X supports Y as a defeasible causal generalization under K.
```

### T — Reasoning Trace

- `t1`: record heating condition.
- `t2`: record expansion outcome.
- `t3`: aggregate repeated trials.
- `t4`: check represented defeaters: none supplied.
- `t5`: infer defeasible causal support for `r4`.

## Result

The claim is supported defeasibly under the supplied empirical calculus. FAR does not convert it into absolute certainty.

---

# Example 5 — Everyday Argument

## Source Reasoning

Someone says: `You did not text me all day, so I think you did not care.`

## FAR Encoding

### I — Investigation

Determine whether the conclusion `you did not care` follows from the premise `you did not text me all day`.

### Rep — Representations

- `r1`: You did not text me all day.
- `r2`: People who care usually communicate.
- `r3`: You did not care.
- `r4`: You may have had another reason for not texting.

### S — Representational Structure

- `r1` supports `r3` only if combined with `r2`.
- `r2` is an unstated generalization.
- `r4` is a defeater for the move from `r1` to `r3`.

### Int — Interpretation

- `text`: send a message during the relevant day.
- `care`: have concern or emotional investment.
- `usually communicate`: probabilistic or normative expectation, not a strict rule.

### C — Reasoning Calculus

Defeasible ordinary-language reasoning:

```text
If behavior B is normally evidence for state S,
then B can support S unless alternative explanations are represented.
```

### T — Reasoning Trace

- `t1`: state observed behavior `r1`.
- `t2`: supply hidden generalization `r2`.
- `t3`: infer `r3` defeasibly.
- `t4`: introduce alternative explanation `r4`.
- `t5`: weaken the inference from `r1` to `r3`.

## Result

The conclusion does not strictly follow. It is a defeasible interpretation that depends on an unstated generalization and is weakened by plausible alternatives.
