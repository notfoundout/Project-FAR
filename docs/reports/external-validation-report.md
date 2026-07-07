# External Validation Report

Status: v0.4.0 initial hard-system batch.

## Purpose

This report applies Project FAR as an instrument to ten external reasoning systems that were not designed for FAR. The goal is to determine whether the five-primitive architecture can represent their explicit reasoning structure without introducing a sixth primitive.

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

## Result Counts

| Result | Count |
|---|---:|
| Fits FAR | 4 |
| Conservative extension | 6 |
| Unresolved | 0 |
| Outside scope | 0 |
| Candidate primitive failure | 0 |

## Primitive Pressure Summary

| Pressure Point | Systems | Current Assessment |
|---|---|---|
| Higher-order or dependent interpretation | Higher-order logic, type theory, Lean, Coq | Handled by Interpretation plus Reasoning Calculus; conservative where domain machinery is required. |
| Machine-checked proof validation | Lean, Coq, SAT/CDCL | Fits FAR directly when proof artifacts or certificates are explicit. |
| Structural and diagrammatic reasoning | Category theory | Requires specialized Representational Structure but not a new primitive. |
| Quantitative uncertainty | Bayesian inference | Requires probabilistic Interpretation and update calculus. |
| State revision and transition | AGM belief revision, dynamic logic | Requires state-transition structure and calculus policy. |

## Current Evidence Status

The initial hard-system batch did not establish any candidate primitive failure. Four systems map directly to FAR, and six require conservative extensions. The conservative extensions place pressure on Interpretation, Representational Structure, and Reasoning Calculus, but none currently requires a primitive outside the five FAR primitives.

## Limits

This is a finite and provisional external corpus. The current result does not prove universal primitive sufficiency. It does show that this first hard external batch has not produced a sixth-primitive requirement.

## Next Work

Future batches should evaluate additional external systems, including SMT solving, Hoare logic, linear logic, relevance logic, planning systems, multi-agent reasoning, graph search, probabilistic programming, and scientific hypothesis testing.