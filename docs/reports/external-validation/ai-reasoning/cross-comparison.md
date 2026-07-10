# Cross-Comparison: AI Reasoning External Validation

## Symbolic vs statistical reasoning
Automated theorem proving and ontology reasoning are primarily symbolic: their operations manipulate explicit formulas, terms, triples, rules, and proof states. Large language models are primarily statistical: they infer token distributions from learned parameters and context. Agentic systems may combine both by using statistical controllers with symbolic tools, structured memory, or verifiers. FAR adds structure by keeping representation and reasoning calculus explicit, but it adds no new statistical or symbolic capability.

## Deterministic vs probabilistic inference
Formal proof checking can be deterministic once axioms, rules, and proof objects are fixed. Knowledge-graph traversal can be deterministic for fixed data and query semantics, though graph construction may be uncertain. LLM inference is probabilistic or score-based, and agentic systems often inherit probabilistic controller behavior plus nondeterministic tool and environment effects. FAR represents these differences as operations and uncertainty rather than reducing them to one inference type.

## Explicit vs implicit representations
Knowledge graphs and theorem provers expose many representations explicitly. LLMs encode most knowledge implicitly in parameters and activations while exposing prompts, context, optional reasoning text, and outputs. Agents expose task traces only when their design records plans, tool calls, memory updates, and feedback. FAR clarifies what is observable and what is inferred, but it cannot make hidden activations or proprietary policies transparent.

## Proof vs prediction
Theorem proving seeks derivations that can be checked against a calculus. LLMs predict or sample likely continuations and may produce proof-like text without proof verification. Knowledge graphs answer by query, traversal, entailment, or link prediction depending on configuration. Agentic systems may use prediction to plan and tools to verify. FAR separates proof certificates from predicted explanations.

## Memory
LLMs use learned parameters and context windows, optionally augmented by retrieval. Knowledge graphs store structured assertions and ontology commitments. Theorem provers maintain proof states and libraries. Agentic systems use working state, episodic traces, vector stores, scratchpads, or external files. FAR adds a common memory vocabulary but does not decide which memory is faithful or sufficient.

## Planning
Planning is central in agentic reasoning, incidental or prompt-induced in LLM use, structured as search in theorem proving, and usually absent or query-specific in knowledge graphs. FAR represents planning as operations over goals, dependencies, and intermediate states. It does not guarantee that a plan is optimal, safe, or complete.

## Uncertainty
LLM uncertainty includes probability distributions, calibration limits, hallucination risk, and missing context. Knowledge-graph uncertainty includes incomplete or ambiguous facts. ATP uncertainty often reflects search bounds, undecidability, formalization adequacy, and trust in kernels or certificates. Agentic uncertainty propagates through tools, memory, observations, and revisions. FAR helps preserve uncertainty instead of collapsing it into success/failure.

## Explainability
Proof systems are most explainable when proof certificates are available. Knowledge graphs can explain by paths, rules, or entailments. LLM explanations may be plausible generated text rather than faithful accounts of internal computation. Agent traces can explain action history, but only if logging is complete. FAR distinguishes explanation artifacts from actual causal mechanisms.

## Verification
ATP has the strongest native verification when proof checking is available. Knowledge graphs can verify query results against explicit data and rules. LLM outputs require external verification. Agentic systems may verify through tools or feedback, but verification quality depends on tool reliability and task design. FAR adds dependency tracking, not independent truth verification.

## Failure modes
LLMs hallucinate, miscalibrate, and overfit prompt patterns. Knowledge graphs omit or misclassify entities and relations. ATP systems time out, search the wrong space, or formalize the wrong theorem. Agents compound errors, misuse tools, corrupt memory, or stop incorrectly. FAR maps these failures to assumptions, dependencies, operations, and uncertainty.

## Where FAR adds structure
FAR adds structure by requiring explicit representation, interpretation, investigation, reasoning calculus, operations, evidence, memory, assumptions, dependencies, outputs, and uncertainty across all paradigms. This makes heterogeneous AI reasoning systems comparable without pretending they share the same mechanism.

## Where FAR adds no capability
FAR does not train models, improve retrieval, complete graphs, find proofs, solve undecidable problems, repair tools, align agents, or certify hidden implementations. Its contribution in this campaign is representational clarity.
