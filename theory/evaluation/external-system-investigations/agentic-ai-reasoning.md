# External System Investigation — Agentic AI Reasoning

Status: provisional

## Purpose

Evaluate agentic AI reasoning because it combines planning, tool use, memory, environment interaction, and possible hidden model reasoning, making it a strong candidate for representation and dependency failures.

## Independent System Description

Agentic AI systems pursue goals through iterative perception, planning, action selection, tool invocation, environment feedback, memory updates, and stopping criteria. A typical agent loop represents a task state, selects an action or tool call, observes a result, updates context or memory, and repeats until success, failure, or interruption. In contemporary LLM-based agents, part of the policy may be produced by a language model, while the surrounding scaffold may include explicit prompts, tools, planners, memories, evaluators, and orchestration code.

The scope is a documented agent run whose objective, tools, observations, actions, memory changes, and termination criteria are available. Undocumented internal model computation or hidden orchestration is not assumed accessible.

## Assumptions

- The evaluated target is an agent run, not merely the final answer.
- Tool APIs, environment observations, memory updates, and stop conditions must be captured to evaluate the reasoning process.
- If the agent uses an LLM, hidden LLM internals inherit the limitations of the LLM investigation.

## Source Evidence

- Primary/framework source: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022/2023), describing interleaved reasoning/action/observation traces.
- Primary/framework source: Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023), describing memory/reflection updates for agents.
- Implementation evidence for any concrete agent: orchestration code, tool schemas, logs, run identifier, prompt/version, and environment transcript.
- Planning background source: Russell and Norvig, *Artificial Intelligence: A Modern Approach*, agent and planning chapters, for standard agent/environment/action terminology.

## Claim Separation

- Syntactic encoding: recording external-system artifacts as text, tokens, states, rules, cases, examples, or traces.
- Representability: mapping objects, structures, interpretation policies, and transformations to FAR/FARA roles.
- Faithful representation: preserving the scoped source-described properties required for the investigation objective.
- Operational equivalence: replaying or comparing target procedures and FAR/FARA transitions under the same stated inputs, rules, and success criteria where the procedure is accessible.
- Explanatory adequacy: explaining the target reasoning at the abstraction level claimed by this investigation, without asserting internal details not evidenced by sources.
- Universality: not claimed; this report evaluates only the scoped system.
- Necessity: component use is reported only for this investigation.
- Minimality: not claimed; no primitive ablation or primitive-independence proof is performed.

## FAR/FARA Representation

| FAR/FARA Component | Target-System Mapping | Notes |
|---|---|---|
| Investigation | Goal-directed task or environment objective. |  |
| Representation | Goals, observations, actions, tool calls, tool results, memories, plans, critiques, final outputs. |  |
| Representational Structure | Temporal action-observation graph, tool schemas, memory links, subgoal hierarchy, environment state dependencies. |  |
| Interpretation | Task success semantics, tool-result meanings, environment state interpretation, policy/evaluator meanings. |  |
| Reasoning Calculus | Agent loop policy: plan/select action, execute tool, observe, update memory/context, evaluate stop condition. |  |
| Reasoning State | Current goal, context, memory, available tools, environment observation, intermediate plan. |  |
| Transition Signature | Choose action/tool, call tool, receive observation, update memory/context, revise plan, terminate. |  |
| Candidate | Candidate action, tool call, plan step, memory write, final answer. |  |
| Admissibility Structure (Ω) | Tool preconditions, safety rules, environment constraints, memory policy, success criteria. |  |
| Resolution Rule | Policy/evaluator selection of next action or termination. |  |
| Resolution | Completed run, failure, partial result, or revised state. |  |

## Preservation Review

### Representation Fidelity

Target: complete run transcript including objective, tools, actions, observations, memory, and stopping. Evidence: agent framework sources and concrete logs. Preserving element: Representation. Procedure: check transcript completeness against target run components. Result: `unknown`. Justification: many real agents have incomplete logs or hidden prompts; documented toy/open runs can pass

### Semantic Preservation

Target: goal, observation, action, tool, memory, and success semantics. Evidence: tool schemas, environment docs, task spec. Preserving element: Interpretation. Procedure: compare each logged artifact to explicit semantics. Result: `unknown`. Justification: semantics are preserved only when tool/environment specifications are available

### Structural Preservation

Target: temporal loop, subgoals, tool dependencies, memory links. Evidence: agent logs and orchestration code. Preserving element: Representational Structure and Reasoning State. Procedure: reconstruct action-observation dependency graph. Result: `pass`. Justification: documented agent loops have explicit temporal/dependency structure

### Operational Preservation

Target: action selection, tool execution, observation update, reflection/planning. Evidence: ReAct/Reflexion/framework code. Preserving element: Reasoning Calculus and Transition Signature. Procedure: replay transitions from logged state when policy and tool outputs are available. Result: `unknown`. Justification: LLM policy and external environments often prevent deterministic replay

### Dependency Preservation

Target: tools, prompts, model versions, environment state, memory stores, external APIs. Evidence: run metadata and code. Preserving element: Representational Structure. Procedure: audit dependency manifest. Result: `unknown`. Justification: external APIs and hidden provider state may be missing or mutable

### Information Preservation

Target: information required to reproduce and audit the run. Evidence: logs, code, versions, API snapshots. Preserving element: all components. Procedure: attempt reconstruction from report and artifacts. Result: `unknown`. Justification: mutable tools/environments and hidden model state can lose decisive information

## Required FAR/FARA Components

Required: all FAR primitives and FARA state-transition components. Conservative extensions are required for tool schemas, environment models, memory policy, nondeterministic policy execution, and run provenance.

## Unused FAR/FARA Components

No primitive is categorically unused. Some hidden model internals are outside accessible evidence for a given run.

## Alternative Representations Considered

- Final-answer-only mapping was rejected because it discards action and dependency information.
- Treating agent framework diagrams as the run was rejected unless concrete logs instantiate them.
- Full mechanistic mapping was retained only for agents with open code, fixed tools, captured environment, and accessible policy internals.

## Potential Counterexamples

- Dynamic external tools may change behavior between original run and replay.
- Hidden LLM/system prompts may drive actions not visible in logs.
- Memory retrieval may depend on embeddings or stores not recorded in the report.
- Multi-step autonomous behavior may create unbounded environment dependencies.

## Counterexample Classification

- Mutable tool/environment behavior: `unresolved`; lower-precedence plausible category is `conservative extension pressure`.
- Hidden policy state: `outside scope` for internal process; visible trace remains unresolved.
- Unbounded environment dependencies: `unresolved` unless bounded by run artifact capture.
- Final-answer-only success: `not a counterexample` to FAR/FARA but fails operational preservation.

## Classification

`unresolved`

## Justification

Documented agent traces are structurally representable, but ordinary agentic AI runs do not reliably satisfy semantic, operational, dependency, and information preservation without strong artifact capture. The limitation is not a demonstrated sixth primitive because the pressure concerns conservative machinery for tools/environments/provenance and inaccessible internals.

## Limitations

Does not cover all autonomous systems, robotics, continuous-control agents, or proprietary orchestrators. It evaluates reasoning process preservation only where run artifacts are available.

## Methodology Feedback

No methodology defect was discovered. The methodology forced explicit unknown/outside-scope handling rather than rescue reinterpretation.

## Implications

### Universality

Adds evidence against premature universal claims for real-world opaque/dynamic systems, while not refuting explicit-reasoning representability where agent runs are fully logged.

### Necessity

Supports necessity pressure for state, transitions, admissibility, dependency, and resolution components in interactive reasoning.

### Minimality

No minimality conclusion; agentic systems may be valuable future ablation targets because they require nearly every FARA component.

## Confidence

Moderate; the unresolved classification follows from common dependency and replay gaps, but fully captured open agents may classify as conservative extensions.

## Remaining Questions

- What artifact bundle is sufficient for agent replay years later?
- Should tool/environment snapshotting become a reusable derived evidence standard?
- Can open benchmark agents be investigated as conservative-extension cases?
