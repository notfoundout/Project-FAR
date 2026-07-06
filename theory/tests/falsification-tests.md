# Falsification Tests

## Purpose

This document tries to construct reasoning systems that Project FAR cannot represent.

A failed falsification strengthens the scoped theory. A successful falsification identifies either a boundary condition or a required revision.

---

# Test 1 — Pure Unstructured Marks

## Candidate Counterexample

A page contains random marks with no interpretation, no structure, and no rule of transition.

## FAR Analysis

The marks may be representations only in the weakest physical sense, but they do not supply an investigation, interpretation, or calculus.

## Result

Not in FAR scope.

## Effect

This is not a falsification. FAR claims scoped explicit reasoning, not arbitrary marks.

---

# Test 2 — Private Intuition with No Articulation

## Candidate Counterexample

A person has an intuition but cannot state the object, meaning, reason, or transition rule.

## FAR Analysis

The intuition lacks explicit representations and an explicit calculus.

## Result

Not in FAR scope unless reconstructed into explicit representations.

## Effect

This is a boundary condition, not a falsification.

---

# Test 3 — Contradictory Reasoning System

## Candidate Counterexample

A system permits both a claim and its negation.

## FAR Analysis

FAR can represent inconsistent systems by encoding the claims, contradiction relation, interpretation, and permissive calculus.

## Result

Representable.

## Effect

Failed falsification. Consistency is not required for representation.

---

# Test 4 — Circular Reasoning

## Candidate Counterexample

A conclusion depends on a premise that depends on the conclusion.

## FAR Analysis

FAR can represent circularity as a dependency cycle in representational structure.

## Result

Representable.

## Effect

Failed falsification. A reasoning defect can be represented without being endorsed.

---

# Test 5 — Probabilistic Reasoning

## Candidate Counterexample

A system updates beliefs by probability rather than deduction.

## FAR Analysis

The probability calculus supplies the reasoning calculus. Hypotheses and evidence supply representations. Conditional dependencies supply structure.

## Result

Representable.

## Effect

Failed falsification. FAR is not limited to deductive logic.

---

# Test 6 — Ambiguous Natural Language

## Candidate Counterexample

A sentence has multiple possible meanings.

## FAR Analysis

FAR can represent each interpretation separately or represent ambiguity as multiple candidate interpretations.

## Result

Representable if the ambiguity is made explicit.

## Effect

Partial boundary. Unarticulated ambiguity must be reconstructed before representation.

---

# Test 7 — Infinite Reasoning Process

## Candidate Counterexample

A reasoning process has infinitely many steps.

## FAR Analysis

The current finite normal form theorem does not cover infinite traces. However, the core representation theorem may still represent the process schematically if the infinite rule or generator is explicit.

## Result

Partially representable. Full trace representation requires additional infinite-model machinery.

## Effect

Open boundary. This motivates future work on infinite FAR models.

---

# Test 8 — Non-Rule-Governed Association

## Candidate Counterexample

A person jumps from one thought to another with no rule, standard, association, or reconstructible transition.

## FAR Analysis

If no calculus or transition standard is available, the process fails FAR scope. If an association rule is supplied, it becomes representable.

## Result

Not in FAR scope unless reconstructed.

## Effect

Boundary condition, not falsification.

---

# Test 9 — Self-Modifying Reasoning System

## Candidate Counterexample

A system changes its own rules while reasoning.

## FAR Analysis

FAR can represent rule-change by treating the calculus at each state as part of the reasoning state and representing transitions between calculi.

## Result

Representable if rule-change is explicit.

## Effect

Failed falsification. This requires dynamic calculus representation but not a new primitive.

---

# Test 10 — Reasoning with Undefined Terms

## Candidate Counterexample

A proof uses a term that has no definition or interpretation.

## FAR Analysis

FAR can represent the token, but not its semantic content. The gap is marked as undefined interpretation.

## Result

Partially representable as defective reasoning.

## Effect

Not a falsification. FAR can represent semantic failure as a failure.

---

# Audit Conclusion

No tested case defeats FAR within its stated scope.

The strongest boundary cases are:

1. infinite reasoning traces;
2. private unreconstructed intuition;
3. non-rule-governed association;
4. undefined or uninterpreted terms.

These should become future research targets rather than be hidden.
