# Target System
Agentic Reasoning

# Source and Scope
Agentic AI systems using planning, tools, memory, and iterative feedback. Sources: Russell and Norvig, "Artificial Intelligence: A Modern Approach", http://aima.cs.berkeley.edu/; Yao et al., "ReAct: Synergizing Reasoning and Acting", https://arxiv.org/abs/2210.03629; Schick et al., "Toolformer", https://arxiv.org/abs/2302.04761; Park et al., "Generative Agents", https://arxiv.org/abs/2304.03442; Mialon et al., "Augmented Language Models", https://arxiv.org/abs/2302.07842. Scope is planning, decomposition, tool usage, memory, iterative refinement, feedback loops, and uncertainty propagation.

# Architecture
Controller model or policy connected to task state, planner, tools, memory stores, feedback channels, and stopping criteria. Implementations may be LLM-centered, symbolic, reinforcement-learning based, or hybrid.

# Representation
Goals, subtasks, plans, observations, tool schemas, memory records, intermediate traces, environment state, feedback, and final outputs.

# Reasoning Process
Reasoning decomposes goals, selects actions, calls tools, observes results, updates state or memory, revises plans, and iterates until termination or failure.

# Hidden Assumptions
Tools are callable and reliable within declared limits; observations are interpreted correctly; memory retrieval is relevant; plans decompose the task adequately; feedback reflects progress; uncertainty is not erased across iterations.

# Failure Modes
Tool errors, compounding mistakes, stale memory, circular planning, ungrounded subgoals, hidden state loss, over-decomposition, unsafe actions, and false confidence after feedback.

# Adversarial Analysis
Adversarial tasks can poison memory, return misleading tool outputs, induce loops, or exploit planner assumptions. FAR can represent the loop and dependency chain but cannot guarantee agent success or safety.

# FAR Mapping
- Representation: target system behavior and documented AI methodology.
- Representational Structure: architecture, inputs, internal representation, inference mechanism, memory, evidence, output, and uncertainty.
- Interpretation: domain-specific interpretation of symbols, tokens, graph edges, proof terms, or agent observations.
- Investigation: reconstruct how the system transforms input and dependencies into output.
- Reasoning Calculus: system-specific calculus, including probabilistic token inference, graph entailment, formal proof rules, or planning/action loops.
- Operations: encode, retrieve, attend, traverse, infer, search, verify, plan, call tools, update memory, and emit outputs as applicable.
- Evidence: cited methodology, official documentation, formal standards, prompts, retrieved material, graph assertions, proof certificates, tool results, or observations.
- Memory: context window, graph store, proof state, learned parameters, external memory, or execution history as applicable.
- Assumptions: explicit architecture, source, semantic, inference, reliability, and scope assumptions.
- Dependencies: training data or ontology commitments; inference rules; retrieval sources; solvers; tools; memory policy; decoding or search parameters.
- Outputs: generated text, query result, entailment, proof, countermodel, plan, action trace, or final answer.
- Uncertainty: probabilistic uncertainty, incompleteness, ambiguity, search bounds, hidden implementation details, and source limitations.

# What FAR Clarifies
FAR clarifies the separation between representation, interpretation, operations, evidence, assumptions, dependencies, outputs, and uncertainty. It allows the system to be reconstructed without treating the system's output as automatically true.

# What FAR Does Not Decide
FAR does not decide whether a generated answer is true, whether a graph is complete, whether a theorem search will terminate, whether a plan is safe, or whether a proprietary implementation actually matches an abstract reconstruction beyond documented evidence.

# Outcome
CONDITIONAL PASS
