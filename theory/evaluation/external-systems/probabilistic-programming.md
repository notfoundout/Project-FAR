# External System Evaluation — Probabilistic Programming

## Overview

Probabilistic programming combines program structure with probabilistic models and inference procedures.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Infer posterior quantities or model predictions from a probabilistic program and observations. |
| Representation | Programs, random variables, observations, priors, likelihoods, traces, and posterior estimates. |
| Representational Structure | Program control flow, dependency graphs, generative structure, and observation constraints. |
| Interpretation | Probabilistic semantics over execution traces. |
| Reasoning Calculus | Sampling, conditioning, inference algorithms, approximation rules, and convergence criteria. |

## Pressure Point

The pressure is hybrid: program semantics plus probabilistic interpretation plus approximate inference.

## Classification

`conservative extension`

## Justification

The required elements fit existing primitives, but FAR needs domain-specific treatment for approximate probabilistic inference and trace semantics. No sixth primitive is currently indicated.

## Confidence

Provisional.
