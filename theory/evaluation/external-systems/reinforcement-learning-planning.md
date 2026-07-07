# External System Evaluation — Reinforcement-Learning Planning

## Overview

Reinforcement-learning planning evaluates actions by expected future reward under a policy, value function, model, or learned environment interaction.

## FAR Mapping

| FAR Primitive | Mapping |
|---|---|
| Investigation | Select or evaluate actions that optimize expected return. |
| Representation | States, actions, rewards, policies, value estimates, trajectories, and models. |
| Representational Structure | State-transition structure, policy mappings, temporal dependency, and reward accumulation. |
| Interpretation | Decision-theoretic or environment-model semantics for states, actions, and rewards. |
| Reasoning Calculus | Bellman update, policy evaluation, search, planning, and approximation rules. |

## Pressure Point

The pressure is learned or approximate transition evaluation. Some internal learning may be opaque, but explicit planning traces remain representable.

## Classification

`conservative extension`

## Justification

RL planning requires quantitative, temporal, and decision-theoretic calculus machinery. This extends existing primitives but does not require a sixth primitive.

## Confidence

Provisional.
