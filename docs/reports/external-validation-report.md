# External Validation Report

Status: v0.4.0 external validation batches 1 and 2.

## Purpose

This report applies Project FAR as an instrument to external reasoning systems that were not designed for FAR. The goal is to determine whether the five-primitive architecture can represent their explicit reasoning structure without introducing a sixth primitive.

## Systems Evaluated

| ID | System | Domain | Classification | Report |
|---|---|---|---|---|
| EV-001 | Higher-order logic | Logic | conservative extension | [`higher-order-logic.md`](../../theory/evaluation/external-systems/higher-order-logic.md) |
| EV-002 | Lean | Formal verification | fits FAR | [`lean.md`](../../theory/evaluation/external-systems/lean.md) |
| EV-003 | Coq | Formal verification | fits FAR | [`coq.md`](../../theory/evaluation/external-systems/coq.md) |
| EV-004 | ZFC set theory | Mathematics | fits FAR | [`zfc.md`](../../theory/evaluation/external-systems/zfc.md) |
| EV-005 | Type theory | Logic and foundations | conservative extension | [`type-theory.md`](../../theory/evaluation/external-systems/type-theory.md) |
| EV-006 | Category theory | Mathematics | conservative extension | [`category-theory.md`](../../theory/evaluation/external-systems/category-theory.md) |
| EV-007 | Bayesian inference | Probability and science | conservative extension | [`bayesian-inference.md`](../../theory/evaluation/external-systems/bayesian-inference.md) |
| EV-008 | SAT/CDCL solving | Automated reasoning | fits FAR | [`sat-cdcl.md`](../../theory/evaluation/external-systems/sat-cdcl.md) |
| EV-009 | AGM belief revision | Epistemic logic | conservative extension | [`agm-belief-revision.md`](../../theory/evaluation/external-systems/agm-belief-revision.md) |
| EV-010 | Dynamic logic | Logic and programs | conservative extension | [`dynamic-logic.md`](../../theory/evaluation/external-systems/dynamic-logic.md) |
| EV-011 | SMT solving | Automated reasoning | conservative extension | [`smt-solving.md`](../../theory/evaluation/external-systems/smt-solving.md) |
| EV-012 | Hoare logic | Program verification | conservative extension | [`hoare-logic.md`](../../theory/evaluation/external-systems/hoare-logic.md) |
| EV-013 | Linear logic | Logic | conservative extension | [`linear-logic.md`](../../theory/evaluation/external-systems/linear-logic.md) |
| EV-014 | Relevance logic | Logic | conservative extension | [`relevance-logic.md`](../../theory/evaluation/external-systems/relevance-logic.md) |
| EV-015 | Probabilistic programming | Probabilistic modeling | conservative extension | [`probabilistic-programming.md`](../../theory/evaluation/external-systems/probabilistic-programming.md) |
| EV-016 | Reinforcement-learning planning | AI planning | conservative extension | [`reinforcement-learning-planning.md`](../../theory/evaluation/external-systems/reinforcement-learning-planning.md) |
| EV-017 | Multi-agent reasoning | AI and epistemic logic | conservative extension | [`multi-agent-reasoning.md`](../../theory/evaluation/external-systems/multi-agent-reasoning.md) |
| EV-018 | Argumentation frameworks | Argumentation theory | conservative extension | [`argumentation-frameworks.md`](../../theory/evaluation/external-systems/argumentation-frameworks.md) |
| EV-019 | Constraint solving | Automated reasoning | fits FAR | [`constraint-solving.md`](../../theory/evaluation/external-systems/constraint-solving.md) |
| EV-020 | Scientific hypothesis testing | Science and statistics | conservative extension | [`scientific-hypothesis-testing.md`](../../theory/evaluation/external-systems/scientific-hypothesis-testing.md) |

## Result Counts

| Result | Count |
|---|---:|
| Fits FAR | 5 |
| Conservative extension | 15 |
| Unresolved | 0 |
| Outside scope | 0 |
| Candidate primitive failure | 0 |

## Primitive Pressure Summary

| Pressure Point | Systems | Current Assessment |
|---|---|---|
| Higher-order or dependent interpretation | Higher-order logic, type theory, Lean, Coq | Handled by Interpretation plus Reasoning Calculus; conservative where domain machinery is required. |
| Machine-checked proof validation | Lean, Coq, SAT/CDCL, SMT, constraint solving | Fits FAR directly when proof artifacts, constraints, or certificates are explicit. |
| Structural and diagrammatic reasoning | Category theory, argumentation frameworks | Requires specialized Representational Structure but not a new primitive. |
| Quantitative uncertainty | Bayesian inference, probabilistic programming, reinforcement-learning planning, scientific hypothesis testing | Requires probabilistic, statistical, or decision-theoretic Interpretation and update calculus. |
| State revision and transition | AGM belief revision, dynamic logic, Hoare logic, reinforcement-learning planning | Requires state-transition structure and calculus policy. |
| Resource or relevance-sensitive admissibility | Linear logic, relevance logic | Requires calculus-level admissibility restrictions. |
| Agent-indexed context | Multi-agent reasoning | Requires indexed structure and interpretation. |

## Current Evidence Status

The first two external validation batches do not establish any candidate primitive failure. Five systems map directly to FAR, and fifteen require conservative extensions. The conservative extensions place recurring pressure on Interpretation, Representational Structure, and Reasoning Calculus, but none currently requires a primitive outside the five FAR primitives.

## Limits

This is a finite and provisional external corpus. The current result does not prove universal primitive sufficiency. It shows only that the first twenty external systems evaluated have not produced a sixth-primitive requirement.

## Next Work

Future batches should evaluate graph search, planning systems, model checking, Hoare-style variants, lambda calculus, natural deduction systems, sequent calculi, legal interpretation, common-law reasoning, and informal scientific explanation.