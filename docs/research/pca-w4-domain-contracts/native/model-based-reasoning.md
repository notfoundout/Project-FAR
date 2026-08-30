# Native contract: model-based reasoning

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

Does agreement at the initial observation determine a model's declared external behavior after an action? Van der Schaft relates deterministic bisimulation to equality of external behavior while distinguishing finer behavior for nondeterministic systems [vanderschaft2004equivalence]. The bounded contract uses deterministic labelled transition systems and a single trace observation.

## Finite models

Each model has initial state `s0`, action `a`, transition `s0 -a-> s1`, and output `out(s0)=0`. In `M0`, `out(s1)=0`; in `M1`, `out(s1)=1`. Both therefore have the same initial output, while their declared output traces for action sequence `[a]` are `[0,0]` and `[0,1]`.

The deliberately lossy carrier is the initial output only. The repaired carrier is the explicit initial state, transition table, and output table. The decoder follows `[a]` and emits the two-state output trace.

## Scope boundary

Only these two deterministic finite models and the action sequence `[a]` are covered. This is not a general bisimulation checker, a scientific-model adequacy claim, or an empirical validation result.
