# CRE-002-SCENARIO-1.0

## System

A bounded emergency-response controller coordinates two agents, Alpha and Beta, using provenance-sensitive facts, defeasible rules, interleaved actions, and rule modification.

## State

Boolean facts:

- `alarm_confirmed=false`
- `sensor_a_positive=false`
- `sensor_b_positive=false`
- `manual_override=false`
- `route_alpha_open=true`
- `route_beta_open=true`
- `alpha_dispatched=false`
- `beta_dispatched=false`
- `incident_contained=false`
- `system_halted=false`

Structured state:

- `evidence_log=[]`, an ordered append-only list of evidence records.
- `action_history=[]`, an ordered append-only list of transition records.
- `active_rules={R_confirm,R_dispatch_alpha,R_dispatch_beta,R_override,R_contain,R_modify,R_halt}`.
- `priority(R_override)=100`, `priority(R_modify)=80`, `priority(R_dispatch_alpha)=50`, `priority(R_dispatch_beta)=50`.
- `modification_count=0`, bounded to at most 1.

Each evidence record is `(claim, source, reliability)` where source is one of `sensor_a`, `sensor_b`, or `operator`, and reliability is `high` or `low`.

## Transitions

### T_record_a

May nondeterministically append exactly one of:

- `(sensor_a_positive=true, sensor_a, high)`; or
- `(sensor_a_positive=false, sensor_a, high)`.

It sets `sensor_a_positive` to the recorded value and appends itself to `action_history`.

### T_record_b

May nondeterministically append exactly one of:

- `(sensor_b_positive=true, sensor_b, high)`; or
- `(sensor_b_positive=false, sensor_b, low)`.

It sets `sensor_b_positive` to the recorded value and appends itself to `action_history`.

`T_record_a` and `T_record_b` are independent and may occur in either order. Their individual updates are atomic; simultaneous execution is not permitted.

### T_confirm

Authorized by `R_confirm` when:

`((sensor_a_positive=true AND high-reliability provenance exists for sensor_a_positive=true) AND (sensor_b_positive=true OR manual_override=true))`

It sets `alarm_confirmed=true` and appends itself to `action_history`.

### T_override

Authorized by `R_override` when an operator evidence record with `claim=manual_override=true` and `reliability=high` exists.

It sets `manual_override=true`. When its conclusion conflicts with a lower-priority dispatch prohibition, `R_override` defeats that prohibition for the current state only. It does not delete or rewrite the defeated rule.

### T_dispatch_alpha

Authorized by `R_dispatch_alpha` when:

- `alarm_confirmed=true`;
- `route_alpha_open=true`;
- `alpha_dispatched=false`;
- `system_halted=false`.

It sets `alpha_dispatched=true`.

### T_dispatch_beta

Authorized by `R_dispatch_beta` when:

- `alarm_confirmed=true`;
- `route_beta_open=true`;
- `beta_dispatched=false`;
- `system_halted=false`.

It sets `beta_dispatched=true`.

When both dispatch transitions are admissible, either may occur first. The second remains admissible unless another transition changes its guard.

### T_modify

Authorized by `R_modify` when:

- `alarm_confirmed=true`;
- `modification_count=0`;
- exactly one of `alpha_dispatched` or `beta_dispatched` is true.

It deactivates the dispatch rule for the not-yet-dispatched agent, increments `modification_count` to 1, and appends a rule-modification record identifying the before and after rule status.

### T_contain

Authorized by `R_contain` when:

`(alpha_dispatched=true OR beta_dispatched=true) AND alarm_confirmed=true`.

It sets `incident_contained=true`.

### T_halt

Authorized by `R_halt` when either:

- `incident_contained=true`; or
- no non-halt transition is admissible and both dispatch rules are inactive or blocked.

It sets `system_halted=true`.

## Invariants and prohibitions

1. Evidence and action histories are append-only and preserve order.
2. A claim requiring provenance is not satisfied by the same Boolean value without the required source and reliability record.
3. No transition may fire after `system_halted=true`.
4. `modification_count` may never exceed 1.
5. Only `T_modify` may change rule activation status.
6. A defeated defeasible rule remains represented and historically recoverable.
7. Interleaving may change history order but may not change the atomic effect of an individual transition.

## Observable outputs

For every terminal run preserve:

- final Boolean and structured state;
- ordered evidence log;
- ordered action history;
- final active/inactive rule statuses;
- which nondeterministic outcomes occurred;
- whether a priority defeat occurred;
- whether rule modification occurred;
- terminal reason: `contained` or `deadlock`;
- whether any invariant was violated.

## Bounds

A run contains at most one firing of each recording transition, one override, one rule modification, one dispatch per agent, one containment, and one halt. The bounded state space is intentional and part of the frozen scenario.
