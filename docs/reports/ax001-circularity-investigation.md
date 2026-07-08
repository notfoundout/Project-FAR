# AX-001 Circularity Investigation

## Executive Summary

This foundational research investigation resolves the immediate open question left by the Foundation Validation Report: whether AX-001's working characterization of Operation survives rigorous circularity review.

Final recommendation: **INCONCLUSIVE**.

The investigation did not establish a successful non-circular reduction of Operation. It also did not establish that every reduction of Operation becomes circular. Instead, both isolated evaluators independently concluded that multiple viable primitive candidates remain, especially Operation and Transition, with State Change, Event, Transformation, and Rule-licensed Transition also retaining limited viability.

The current working characterization — `An operation is an executable act performed within a reasoning process.` — is not explicitly self-referential because it does not use the word `operation` in the definiens. However, the characterization is definitionally unstable. Its central terms, especially `act`, `performed`, `execute`, `executable`, and potentially `reasoning process`, form a mutually dependent operation-adjacent cluster. That cluster cannot function as a successful reduction unless those terms are independently defined without operationality.

This PR does not validate L-001 through T-001. It does not build infrastructure, redesign doctrine, alter tooling, or modify unrelated mathematical artifacts.

AX-001 was not revised. The evidence identifies serious defects in the current working characterization, but it does not justify a clearly superior replacement formulation. Under the revision rule, no AX-001 rewrite is applied merely for improved wording.

Genuine evaluator isolation was approximated through separate sub-agent contexts with repository access prohibited by prompt. The environment cannot provide cryptographic sandbox attestation or prove absence of latent model pretraining knowledge; therefore the appendices record this limitation explicitly.

## Current AX-001

The current AX-001 artifact asks whether Operation can serve as the primitive concept of FARO and whether operation can be treated as irreducible without circularity. Its working characterization is:

```text
An operation is an executable act performed within a reasoning process.
```

AX-001 states that this is not yet a formal definition and is only a provisional characterization used to test whether a non-circular definition is possible.

AX-001's current reduction attempts reject:

1. Operation as state transition, because some operations may preserve state.
2. Operation as representation modification, because some operations inspect, verify, or evaluate without modifying representations.
3. Operation as calculus application, because calculi describe or constrain operations but do not constitute operation itself.

AX-001's provisional result says current evidence supports treating operation as a primitive of FARO, while not proving irreducibility.

## Circularity Analysis

### Question 1 finding

The working characterization is not explicitly circular in the narrow syntactic sense. It does not define Operation using the literal word `operation`.

The characterization is nevertheless definitionally unstable because its major explanatory terms may already presuppose operationality.

### Circular dependencies identified

The following circular dependencies were independently identified or confirmed:

1. **Operation → Act → Action → Operation**
   - This cycle appears if `act` or `action` is treated as an operation-like doing rather than as an independently defined event-token.
   - P1 classifies the act/action loop as linguistic and definitional, not reductive.
   - C1 classifies the same loop as a synonymic or near-synonymic cycle.

2. **Operation → Executable → Execute → Operation**
   - This cycle appears if `execute` means to execute an operation.
   - P1 treats `executable` as unsafe unless `execute` is independently reduced.
   - C1 treats `executable act performed` as one of the strongest direct circularity pressures.

3. **Operation → Performed → Perform → Operation**
   - This cycle appears if `perform` means to carry out an operation.
   - Both blind evaluators identify this as a direct definitional risk.

4. **Perform ↔ Execute**
   - This is a mutual-dependence loop inside the defining vocabulary.
   - It does not by itself prove Operation circular, but it prevents `performed` or `executable` from functioning as independent reducers.

5. **Operation → Reasoning Process → Sequence of Operations → Operation**
   - This cycle appears if `reasoning process` is constituted by operations or reasoning steps that are themselves operations.
   - The cycle can be avoided only if reasoning process is independently characterized, for example through ordered reasoning states, traces, or representational conditions.

6. **Operation → Act Upon → Act → Action → Act**
   - `Act upon` does not escape the act/action cluster.
   - If `act upon` is glossed as `operate on`, the dependency becomes directly circular.

7. **Operation → Rule Application → Application → Perform/Operation**
   - Rule application becomes circular if application means performing or executing a rule-operation.
   - It can be reformulated structurally as rule-licensed transition, but then depends on rule, licensing, transition, and state.

### Linguistic synonymy vs definitional dependence vs logical dependence

The investigation distinguishes three relations:

- **Linguistic synonymy**: ordinary-language overlap among operation, act, action, perform, execute, and move. This alone does not prove logical circularity.
- **Definitional dependence**: a term used in the characterization cannot be explained without invoking Operation or another operation-adjacent term. This defeats reduction.
- **Logical dependence**: Operation cannot be instantiated, individuated, or used unless a prior concept such as state, transition, rule, event, representation, process, or admissibility is already available.

The investigation found extensive linguistic synonymy and several conditional definitional cycles. It did not prove an unconditional logical contradiction in AX-001.

## Reduction Graph

### Core working-characterization graph

```text
Operation
  -> Executable
  -> Act
  -> Performed
  -> Reasoning Process
```

### Expanded cluster graph

```text
Operation
  -> Executable
      -> Execute
          -> Perform
              -> Execute
              -> Act/Action
              -> Operation [if perform = carry out operation]
          -> Operation [if execute = execute operation]
      -> Capability
      -> Admissibility
  -> Act
      -> Action
          -> Act
          -> Event
          -> Agent/Intentionality
          -> Operation [if action = operation]
      -> Event
      -> Occurrence
      -> Agency
      -> Change/Effect
  -> Performed
      -> Perform
          -> Execute
          -> Act/Action
          -> Operation [if perform = carry out operation]
      -> Occurred
      -> Completed
      -> Instantiated
  -> Reasoning Process
      -> Process
          -> Sequence
          -> Events
          -> States
          -> Operations [if process = sequence of operations]
      -> Reasoning
          -> Inference
          -> Representation
          -> Rule/Validity
```

### Act-upon graph

```text
Act upon
  -> Act
      -> Action
      -> Event
      -> Occurrence
  -> Target/Object
  -> Affect
      -> Cause
      -> Change
  -> Operation [if act upon = operate on]
```

### Structural reduction alternatives

```text
Operation
  -> Admissible Transition Between Reasoning States
      -> Transition
      -> Reasoning State
      -> Admissibility
      -> Relation/Ordering
      -> Representation [if states are representational]
```

```text
Operation
  -> Rule-Licensed State Pair
      -> Rule
      -> Licensing
      -> State
      -> Successor Relation
      -> Admissibility
```

```text
Operation
  -> Partial Function/Relation Over Reasoning States
      -> Function/Relation
      -> Domain/Codomain
      -> Reasoning State
      -> Mapping
```

### Cycles

| Cycle | Relation type | Finding |
|---|---|---|
| `Act -> Action -> Act` | linguistic synonymy / definitional dependence | Not reductive. |
| `Perform -> Execute -> Perform` | definitional dependence | Blocks `performed` and `executable` as independent reducers. |
| `Executable -> Execute -> Perform -> Execute` | definitional dependence | Modal executability inherits execution circularity. |
| `Operation -> Executable -> Execute -> Operation` | conditional definitional circularity | Occurs if execute means execute an operation. |
| `Operation -> Performed -> Perform -> Operation` | conditional definitional circularity | Occurs if perform means perform an operation. |
| `Operation -> Act -> Action -> Operation` | conditional definitional circularity | Occurs if act/action are operation-like doings. |
| `Operation -> Reasoning Process -> Sequence of Operations -> Operation` | conditional logical/definitional circularity | Occurs if reasoning process is operationally constituted. |
| `Act upon -> Operate on -> Operation -> Act -> Act upon` | definitional circularity | Occurs if act upon is glossed as operate on. |
| `Operation -> Rule Application -> Apply -> Perform -> Act -> Operation` | conditional definitional circularity | Avoidable only by eliminating application vocabulary. |

## Hidden Assumptions

### Causation

`Performed`, `execute`, `act upon`, transformation, and state-change readings imply that operations produce or determine effects. The evidence does not show that causation is required for Operation. Treating Operation causally risks importing unnecessary causal metaphysics.

### Execution

`Executable` directly presupposes execution. Both blind evaluators found execution to be one of the strongest circularity pressures because execute commonly means perform or carry out an operation.

### Agency

`Act` and `performed` may imply an actor, reasoner, system, mechanism, or intentional agent. Agency may be unnecessary or too narrow for formal, mechanical, automatic, or non-agentive reasoning systems.

### Process

`Within a reasoning process` assumes reasoning is process-like and has stages, order, boundaries, or trace membership. If process is defined by operations, circularity follows.

### Transformation

Many reductions assume an operation transforms an input into an output. This may be too narrow for inspection, verification, comparison, preservation, no-op, identity, or validation cases.

### Manipulation

`Act upon` suggests manipulable operands or representations. Manipulation is action-laden and may reintroduce agency, causation, targethood, and operationality.

### State transition

Transition-based reductions assume identifiable reasoning states, before/after structure, and successor relations. This is the strongest rival primitive path, but it shifts the primitive burden to state, transition, and admissibility.

### Event

Event-based reductions assume operations occur as bounded tokens. Event is relatively independent but too broad unless constrained by reasoning relevance, admissibility, state determination, or rule structure.

### Function

Function or relation reductions assume inputs, outputs, domain, codomain, mapping, and possibly determinacy. They work better for operation-types than operation-tokens and may omit performance or execution.

### Representation

Most reasoning-state and transition reductions assume representational content. If representation is required, Operation depends on a theory of representation. If representation is not required, reasoning process becomes less determinate.

### Reasoning state

State-based reductions assume reasoning states are individuable independently of operations. If reasoning states are defined by available or applied operations, circularity reappears.

## Primitive Candidate Comparison

| Candidate | Necessity | Explanatory power | Circularity | Independence | Simplicity | Expressive power | Compatibility with Project FAR |
|---|---|---|---|---|---|---|---|
| Act | Medium | Medium | High | Low | Medium | Medium | Weak: too close to operation/action and agency-laden. |
| Action | Medium | Medium | High | Low | Medium-low | Medium | Weak: more agency/intentionality burden than Operation. |
| Move | Medium | Medium | Medium | Medium | High | Medium | Limited: useful for proof/game/search models but domain-specific. |
| Transition | High | High | Medium | Medium-high | Medium | High | Strong rival if reasoning states are independently accepted. |
| Transformation | Medium-high | High | Medium | Medium | Medium-low | High | Partial: strong for change but weak for inspection/preservation/no-op. |
| Rule Application | High in formal systems | Very high | High unless `application` is eliminated | Low-medium | Low | Very high | Powerful but likely derivative or too narrow. |
| Constraint Application | Medium-high | High | High unless `application` is eliminated | Low-medium | Low | High | Useful for admissibility/filtering but not broad enough alone. |
| State Change | High | Medium-high | Medium-low | Medium-high | High | Medium-high | Strong but too broad and weak for state-preserving operations. |
| Event | High | Medium | Low-medium | High | High | Medium | Independent but underspecified and overbroad. |
| Operation | High | High | Medium-high under current wording | Medium/unproven | Medium | High | Theory-native but currently contested. |

### Ranking synthesis

Both P1 and C1 rank Transition as the strongest non-operational rival if states and admissibility are independently available. Both preserve Operation as a serious candidate if transition/state/admissibility are not independently available or if transition reductions prove more complex than Operation.

The weakest candidates are Act and Action because they do not escape the synonymic/agency cluster. Rule Application and Constraint Application have high explanatory power but risk circularity through `application` and add more machinery than Operation.

## Primitive Reduction Attempts

### Operation → Act

Result: failed. `Act` cycles with `action`, `perform`, or operation-like doing.

### Operation → Action

Result: failed. `Action` introduces agency/intentionality and cycles with `act`.

### Operation → Performed act

Result: failed. `Performed` depends on `perform`, which cycles with `execute` and potentially Operation.

### Operation → Executable act

Result: failed. `Executable` depends on `execute`, which commonly means perform or carry out an operation.

### Operation → Act upon a reasoning object

Result: failed or too narrow. `Act upon` remains inside the act/action cluster and introduces targethood, causation, and effect.

### Operation → Event in reasoning process

Result: non-circular but incomplete. Event is too broad without additional constraints.

### Operation → State change

Result: partially viable but underspecified. It excludes or strains inspection, validation, comparison, preservation, no-op, and identity cases unless broadened.

### Operation → Transition

Result: strongest non-circular reduction candidate. `Admissible transition between reasoning states` avoids act/perform/execute vocabulary but requires independently accepted reasoning states, transition, and admissibility.

### Operation → Transformation

Result: partially viable but likely too narrow. It presupposes changed objects or states and excludes state-preserving cases.

### Operation → Rule application

Result: failed unless application is eliminated. A structural repair as a rule-licensed state pair is possible but depends on rule, licensing, state, successor, and admissibility.

### Operation → Constraint application

Result: failed or overly specialized. It risks circularity through `application` and does not naturally cover generative or constructive operations.

### Operation → Function/relation over reasoning states

Result: non-circular for operation-types but incomplete for operation-tokens. Abstract functions or relations do not capture performed/executable occurrence unless occurrence or instantiation is added.

### Question 6 conclusion

The justified conclusion is **C — Multiple equally valid primitive candidates remain**.

A is not justified because no successful non-circular reduction satisfies all primitive-identification constraints. B is not justified because transition, state-change, event, function/relation, and rule-licensed state-pair characterizations can be stated without explicit circularity. The evidence therefore supports C.

## Repository Comparison

This comparison occurred only after `docs/reports/appendices/ax001-p1-raw.md` and `docs/reports/appendices/ax001-c1-raw.md` existed.

### Compared materials

- P1 raw appendix: `docs/reports/appendices/ax001-p1-raw.md`
- C1 raw appendix: `docs/reports/appendices/ax001-c1-raw.md`
- Current AX-001: `research/axiomatization/FARO/AX-001-primitive-operation.md`
- Previous reduction attempts: AX-001 and `research/discovery/FARO/FARO-026-reducibility-of-operation.md`
- Foundation Validation Report: `docs/reports/foundation-validation-report.md`

### Independently confirmed findings

- P1 and C1 both find the current working characterization not adequate as a non-circular definition.
- P1 and C1 both identify the act/action/perform/execute/executable cluster as a circularity risk.
- P1 and C1 both identify Transition as the strongest rival candidate if states and admissibility are independently available.
- P1 and C1 both conclude **C — multiple equally valid primitive candidates remain**.
- P1 and C1 both reject Act and Action as superior primitive candidates.
- P1 and C1 both find Rule Application powerful but circular or too complex unless reformulated structurally.

### Independently rediscovered failures

The raw appendices rediscover prior repository failures:

- State-transition reduction is incomplete unless it handles state-preserving, inspection, verification, and evaluation cases.
- Representation modification is incomplete because inspection, verification, and evaluation may not modify representations.
- Rule/calculus application is incomplete because application can be operation-like and rule/calculus structures may describe or constrain operations rather than constitute them.

### Genuinely new findings

Compared to AX-001's current text, this investigation adds:

- An explicit reduction graph over operation, act, action, perform, performed, execute, executable, and act upon.
- A distinction among linguistic synonymy, definitional dependence, and logical dependence.
- A direct finding that the working characterization is definitionally unstable rather than merely provisional.
- A stronger transition-rival analysis: `admissible transition between reasoning states` is not circular in wording and remains a live competitor, though not a completed reduction.
- An explicit conclusion that the primitive status is presently **INCONCLUSIVE** rather than safely retained or rejected.
- A documented isolation limitation for the blind evaluations.

### Repository strengths

- AX-001 correctly marks the working characterization as provisional rather than formal.
- AX-001 correctly asks whether operation can be defined without presupposing operation.
- AX-001 and FARO-026 correctly reject overly narrow reductions by state transition, representation modification, and calculus application.
- The Foundation Validation Report correctly stopped downstream validation when AX-001 failed the Stability Gate.
- The Foundation Validation Report already identified material circularity pressure in `act`, `executable`, `performed`, and `act upon`.

### Repository omissions

- AX-001 does not include an explicit graph of circular dependencies.
- AX-001 does not distinguish linguistic synonymy, definitional dependence, and logical dependence.
- AX-001 does not compare Operation against Act, Action, Move, Transition, Transformation, Rule Application, Constraint Application, State Change, and Event in one table.
- AX-001 does not record that Transition remains a live rival primitive if reasoning states and admissibility are independently accepted.
- AX-001's provisional result is stronger than the evidence generated here warrants.

### Repository contradictions

No direct formal contradiction was established. However, there is evidential tension between:

- AX-001's provisional result that current evidence supports treating operation as a primitive of FARO; and
- this investigation's finding that the evidence currently supports **INCONCLUSIVE** because multiple viable primitive candidates remain.

The raw appendices are authoritative evidence for this investigation. Where this report goes beyond the raw findings, it does so as repository comparison: for example, the report treats C1's conditional `admissible transition` reduction as insufficient to revise AX-001 because the repository has not independently accepted reasoning state, transition, and admissibility as prior primitives in a way that would eliminate Operation.

## Recommended Revision (if any)

No AX-001 revision is applied in this PR.

A revision is not applied because the investigation did not identify a clearly superior characterization. The strongest candidate alternatives are:

1. `Operation := admissible transition between reasoning states.`
2. `Operation := rule-licensed relation between reasoning states.`
3. `Operation := partial function/relation over reasoning states.`
4. `Operation := bounded reasoning-relevant occurrence or formal step by which a reasoning structure proceeds from one admissible condition to another.`

Each candidate avoids some act/perform/execute circularity, but each imports unresolved dependencies such as state, transition, admissibility, rule, relation, function, occurrence, reasoning-state individuation, or representation. Under the revision rule, replacing AX-001's wording with any of these would prematurely promote unresolved research into canonical AX-001 text.

The recommended future revision target, if authorized by subsequent evidence, is not a wording polish. It is an adjudication among Operation, Transition, State Change, Event, Transformation, and Rule-licensed Transition as candidate primitives.

## Remaining Open Questions

1. Can reasoning state be defined independently of Operation?
2. Can transition be defined independently of Operation and without equivalent primitive burden?
3. Can admissibility be defined without rule application, operation, or circular normativity?
4. Are state-preserving inspection, verification, comparison, and validation operations genuine operations or artifacts of current terminology?
5. Does FAR require operation-tokens, operation-types, or both?
6. Is `reasoning process` prior to Operation, constituted by Operation, or jointly dependent with Operation?
7. Can eventhood distinguish operational events from arbitrary events without importing Operation?
8. Does Project FAR require a processual account of reasoning, or can reasoning be represented statically as relations among structures?
9. Should AX-001's provisional result be demoted or annotated in a later PR if no primitive adjudication is available?
10. What accepted doctrine, if any, establishes the prior status of state, transition, relation, representation, and admissibility?

## Final Recommendation

**INCONCLUSIVE**

