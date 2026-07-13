# CRE-001 Scenario v1.0: Reflective Discrete Rule-Transition System

Status: Frozen input; not executed
Experiment: CRE-001
Scenario identifier: CRE-001-SCENARIO-1.0
Protocol: CRP-1.0

## Scenario Description

The target system is a finite, reflective, discrete rule-transition system. It contains explicit propositions, explicit rules, explicit transitions, a rule-modification mechanism, historical dependency preservation, observable outputs, and explicit stopping conditions.

The system evolves through numbered discrete states. Each state records proposition truth values, active rule statuses, transition history, and termination status. A transition is permitted only when an active rule authorizes it and no prohibited-transition condition blocks it. One rule can modify the active status of another rule, so the system is reflective but remains explicitly governed by state-transition rules.

## Initial State

State `S0` contains:

| Identifier | Content | Initial value |
| --- | --- | --- |
| `p_ready` | the system is ready to begin | `true` |
| `p_token` | a token is available | `true` |
| `p_checked` | the token has been checked | `false` |
| `p_accepted` | the token has been accepted | `false` |
| `p_rejected` | the token has been rejected | `false` |
| `p_rule_modified` | the modification rule has changed another rule status | `false` |
| `p_halted` | the system has halted | `false` |

Active rules at `S0`: `R_check`, `R_accept`, `R_reject`, `R_modify`, and `R_halt`. Inactive rules at `S0`: none. Transition history at `S0`: empty.

## Propositions

- `p_ready`: the system may begin a checking sequence.
- `p_token`: the token exists as the object of the transition sequence.
- `p_checked`: the token has passed through the checking transition.
- `p_accepted`: the token has entered accepted status.
- `p_rejected`: the token has entered rejected status.
- `p_rule_modified`: the modification transition has changed the active status of `R_reject`.
- `p_halted`: the system has reached a terminal state.

## Rules

- `R_check`: if `p_ready=true`, `p_token=true`, and `p_checked=false`, then transition `T_check` may set `p_checked=true` and append `T_check` to history.
- `R_accept`: if `p_checked=true`, `p_rejected=false`, and `R_accept` is active, then transition `T_accept` may set `p_accepted=true` and append `T_accept` to history.
- `R_reject`: if `p_checked=true`, `p_accepted=false`, and `R_reject` is active, then transition `T_reject` may set `p_rejected=true` and append `T_reject` to history.
- `R_modify`: if `p_checked=true`, `p_accepted=false`, `p_rejected=false`, and `R_modify` is active, then transition `T_disable_reject` may set `R_reject` to inactive, set `p_rule_modified=true`, and append `T_disable_reject` to history.
- `R_halt`: if `p_accepted=true` or `p_rejected=true`, then transition `T_halt` may set `p_halted=true` and append `T_halt` to history.

## Permitted Transitions

- `T_check`: authorized only by active `R_check` under its preconditions.
- `T_accept`: authorized only by active `R_accept` under its preconditions.
- `T_reject`: authorized only by active `R_reject` under its preconditions.
- `T_disable_reject`: authorized only by active `R_modify` under its preconditions.
- `T_halt`: authorized only by active `R_halt` under its preconditions.

## Prohibited Transitions

- No transition may set both `p_accepted=true` and `p_rejected=true`.
- No transition other than `T_disable_reject` may change the active status of any rule.
- No transition may remove or rewrite prior transition-history entries.
- No transition may occur after `p_halted=true`.
- `T_reject` is prohibited after `R_reject` is inactive.
- `T_accept`, `T_reject`, and `T_disable_reject` are prohibited before `p_checked=true`.

## Rule-Modification Behavior

`T_disable_reject` is the only rule-modification transition. When it occurs, it changes `R_reject` from active to inactive, sets `p_rule_modified=true`, and records the transition in history. The historical record must preserve that `R_reject` was active before the transition and inactive after it.

## Stopping Conditions

The system stops when `p_halted=true`. `T_halt` may occur only after either acceptance or rejection. A terminal state has no permitted outgoing transitions.

## Observable Outputs

The observable output of any completed run is:

- final status: `accepted`, `rejected`, or `unterminated`;
- final active/inactive status of each rule;
- ordered transition history;
- whether rule modification occurred;
- whether any prohibited transition occurred.

## Success Criteria

A representation succeeds for this scenario only if it preserves the propositions, rule statuses, permitted transitions, prohibited transitions, rule-modification behavior, historical dependency record, stopping condition, and observable outputs without adding unstated domain rules.

## Failure Criteria

A representation fails if it permits an expressly prohibited transition, omits rule-modification history, collapses acceptance and rejection into an indistinguishable status, cannot represent rule activation status, cannot express the stopping condition, changes the scenario dynamics, or leaves a required preservation dimension unknown.
