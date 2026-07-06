# Advanced Falsification Tests

## Purpose

This document adds harder falsification tests against Project FAR's representation claims.

These tests focus on cases that stress scope, finiteness, consistency, self-reference, defeasibility, and non-deductive reasoning.

---

# Test A1 — Infinite Reasoning

## Candidate Counterexample

A reasoning process contains infinitely many steps.

## Stress Point

T-009 currently establishes canonical normal form only for finite scoped FAR representations.

## FAR Analysis

If the infinite process is given by an explicit generator, rule, recurrence, or schema, FAR can represent the process schematically. If the claim requires enumerating every transition in an actual infinite trace, current FAR machinery is incomplete.

## Result

Partial boundary.

## Consequence

Future work should develop infinite FAR models, coinductive traces, or schema-level trace representation.

---

# Test A2 — Self-Reference

## Candidate Counterexample

A reasoning process includes a statement about itself, such as `this claim is unsupported`.

## Stress Point

Self-reference may create cycles between representation, interpretation, and evaluation.

## FAR Analysis

FAR can represent the self-reference as a structural loop. The representation is possible. Whether the reasoning is stable, paradoxical, or admissible depends on the supplied calculus.

## Result

Failed falsification for representation. Open issue for stability and resolution.

## Consequence

Future work should classify self-reference cycles and define fixed-point or hierarchy-based handling.

---

# Test A3 — Paradox

## Candidate Counterexample

A reasoning system includes a liar-style sentence or paradox-generating rule.

## Stress Point

Paradox challenges semantic assignment and admissibility.

## FAR Analysis

FAR can represent the sentence, the interpretation attempt, the rule generating contradiction, and the resulting failure state. FAR does not need to solve the paradox in order to represent it.

## Result

Failed falsification for representation. Boundary for resolution.

## Consequence

FAR should distinguish representability from successful resolution.

---

# Test A4 — Inconsistent Calculus

## Candidate Counterexample

A calculus permits both `p` and `not-p` from the same state.

## Stress Point

Consistency is not guaranteed.

## FAR Analysis

FAR can represent the calculus, the permitted transitions, and the contradiction relation. Soundness must be evaluated relative to the supplied calculus, not assumed absolutely.

## Result

Failed falsification.

## Consequence

FAR can represent defective or explosive systems without endorsing them.

---

# Test A5 — Non-Monotonic Reasoning

## Candidate Counterexample

A conclusion is valid given current information but withdrawn after new information appears.

Example:

1. Birds usually fly.
2. Tweety is a bird.
3. Therefore Tweety flies.
4. Tweety is a penguin.
5. Therefore withdraw Tweety flies.

## Stress Point

Admissibility changes with added representations.

## FAR Analysis

FAR can represent the original defeasible inference, the new defeater, and the revised admissibility status. The calculus must allow defeat and revision.

## Result

Failed falsification.

## Consequence

FAR should include explicit support for defeasible calculi in future examples.

---

# Test A6 — Abductive Reasoning

## Candidate Counterexample

A system infers the best explanation rather than a deductive conclusion.

## Stress Point

The conclusion is selected by explanatory ranking, not entailment.

## FAR Analysis

FAR can represent candidate explanations, evidence, explanatory criteria, ranking rules, and the selected resolution. The reasoning calculus is abductive rather than deductive.

## Result

Failed falsification.

## Consequence

Future work should define an abductive calculus example.

---

# Test A7 — Analogical Reasoning

## Candidate Counterexample

A conclusion is drawn from similarity between cases.

## Stress Point

Similarity is not identity and may be context-relative.

## FAR Analysis

FAR can represent source case, target case, shared features, relevant differences, analogy rule, and defeaters. The investigation determines which similarities matter.

## Result

Failed falsification if relevance criteria are explicit. Boundary if relevance is unstated.

## Consequence

FAR should require explicit relevance criteria for analogical arguments.

---

# Test A8 — Moving Goalpost Calculus

## Candidate Counterexample

A reasoner changes admissibility standards whenever a conclusion is challenged.

## Stress Point

The calculus is unstable and potentially strategic rather than rule-governed.

## FAR Analysis

FAR can represent each calculus shift as a transition if the shift is explicit. If the shift is hidden, FAR can represent the visible inconsistency but not the hidden motive.

## Result

Representable as dynamic calculus behavior if explicit. Otherwise partial boundary.

## Consequence

Future dynamic-calculus rules should distinguish explicit rule revision from illicit standard shifting.

---

# Test A9 — Vague Predicate Reasoning

## Candidate Counterexample

A reasoning system depends on vague predicates such as `tall`, `heap`, or `reasonable`.

## Stress Point

Semantic boundaries are unclear.

## FAR Analysis

FAR can represent vagueness by recording open texture, threshold uncertainty, multiple interpretations, or fuzzy membership. The result depends on the supplied interpretation and calculus.

## Result

Failed falsification for representation. Boundary for resolution.

## Consequence

FAR should distinguish semantic representation from semantic sharpening.

---

# Test A10 — Hidden Premise Reasoning

## Candidate Counterexample

An argument appears valid only because it relies on an unstated premise.

## Stress Point

The reasoning process is incomplete as stated.

## FAR Analysis

FAR can represent the stated argument and mark the inferential gap. It can also represent a reconstructed version with the hidden premise added.

## Result

Failed falsification.

## Consequence

FAR should preserve the distinction between original argument and reconstructed argument.

---

# Advanced Audit Conclusion

The hardest cases do not currently falsify FAR's scoped representation thesis.

They expose future work areas:

1. infinite traces;
2. self-reference stability;
3. paradox resolution;
4. dynamic calculi;
5. explicit relevance criteria;
6. vague-predicate semantics;
7. reconstruction standards for hidden premises.
