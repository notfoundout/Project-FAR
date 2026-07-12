# External System Investigation — Large Language Model Reasoning

Status: provisional

## Purpose

Evaluate transformer-based large language model reasoning as a high-risk case for FAR/FARA because the system combines explicit textual inputs/outputs with largely opaque learned internal computation.

## Independent System Description

Large language models are neural language models trained to predict or generate text from large corpora. Transformer language models use attention mechanisms over token sequences, learned parameters, embeddings, and feed-forward layers to produce probability distributions over next tokens; deployed systems may generate answers by decoding those distributions. Reasoning-like behavior appears in generated chains of thought, tool-use traces, mathematical answers, plans, and explanations, but internal learned representations are high-dimensional statistical states rather than human-legible proof objects unless exposed by instrumentation.

The scope of this investigation is inference-time textual reasoning behavior of transformer-based LLMs when prompts, outputs, decoding parameters, and any visible intermediate traces are documented. It does not claim access to inaccessible internal activations, training-data causal provenance, or hidden provider-side system components.

## Assumptions

- The evaluated target is an LLM reasoning episode with documented prompt, model/version, decoding settings when available, output, and any visible intermediate trace.
- Transformer architecture and probabilistic token generation are treated as source-described mechanisms; specific proprietary internals are unknown unless published.
- Generated explanations are treated as output evidence, not automatically as faithful internal process evidence.

## Source Evidence

- Primary source: Vaswani et al., "Attention Is All You Need" (2017), describing transformer attention, sequence transduction, and model architecture.
- Primary/implementation source: OpenAI API/model documentation or provider model card for the specific model/version when an investigation uses one; record retrieval date and model identifier.
- Research source: Brown et al., "Language Models are Few-Shot Learners" (2020), describing autoregressive language-model prompting and task behavior.
- Methodological caution source: Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022), treated as evidence about visible rationale prompting rather than proof of hidden cognition.

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
| Investigation | Question or task posed to the model. |  |
| Representation | Prompt tokens, generated tokens, visible rationale, tool calls, probabilities/logprobs if available. |  |
| Representational Structure | Token order, attention-context window, prompt-message roles, output segmentation, trace dependencies. |  |
| Interpretation | Tokenizer/model semantics, prompt interpretation, probability distribution over next tokens, task success criteria. |  |
| Reasoning Calculus | Forward-pass token prediction plus decoding policy; optional visible tool or reasoning trace rules. |  |
| Reasoning State | Prompt prefix, context window, generated prefix, external tool state if any. |  |
| Transition Signature | Append token, sample/select token, call tool, incorporate tool result, stop. |  |
| Candidate | Candidate next token, candidate answer, candidate tool call, candidate plan step. |  |
| Admissibility Structure (Ω) | Context-window constraints, decoding parameters, safety/tool policies, task validity criteria. |  |
| Resolution Rule | Select next token/answer/tool call; accept answer under external grader or human task criterion. |  |
| Resolution | Generated answer, trace, score, or failure classification. |  |

## Preservation Review

### Representation Fidelity

Target: documented prompts, outputs, model identifiers, and visible traces. Evidence: transformer and LLM task sources. Preserving element: Representation and Representational Structure. Procedure: check whether all externally accessible artifacts are recorded before mapping. Result: `pass`. Justification: accessible artifacts map without reshaping, but inaccessible activations are explicitly scoped out

### Semantic Preservation

Target: task meaning, prompt roles, token probabilities, and answer correctness criteria. Evidence: provider documentation and task specification. Preserving element: Interpretation. Procedure: compare target semantics with explicit interpretation policies and mark hidden semantics unknown. Result: `unknown`. Justification: visible prompt semantics can be preserved, but internal learned meaning and causal rationale are not fully accessible

### Structural Preservation

Target: sequence order, context dependence, message structure, and trace links. Evidence: transformer sequence model description. Preserving element: Representational Structure and Reasoning State. Procedure: reconstruct token/trace dependencies from prompt-output records. Result: `pass`. Justification: externally visible sequential and contextual structure is preservable

### Operational Preservation

Target: forward generation, decoding, tool-call transitions when documented. Evidence: architecture papers and provider settings. Preserving element: Reasoning Calculus and Transition Signature. Procedure: trace visible generation/tool transitions; require logprobs/settings for stronger equivalence. Result: `unknown`. Justification: operational replay is incomplete for proprietary or nondeterministic systems without weights, random seed, and decoding details

### Dependency Preservation

Target: prompt, model version, decoding settings, tool dependencies, and evidence used by answer. Evidence: provider docs and recorded run metadata. Preserving element: Representational Structure. Procedure: audit whether report lists every needed dependency. Result: `unknown`. Justification: many deployments omit hidden system prompts, filters, weights, or retrieval context

### Information Preservation

Target: information needed to reproduce the reasoning episode and judge correctness. Evidence: run metadata, output trace, task sources. Preserving element: all components. Procedure: attempt replay from prompt/model/settings and compare output/task result. Result: `unknown`. Justification: outputs can be recorded, but hidden weights/training provenance and nondeterminism prevent full information preservation

## Required FAR/FARA Components

Required for accessible episodes: Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus, Reasoning State, Transition Signature, Candidate, Admissibility Structure, Resolution Rule, and Resolution. Conservative machinery is required for probabilistic decoding, model-version metadata, uncertainty over hidden state, and tool-use policies.

## Unused FAR/FARA Components

No FAR primitive is unused for the scoped episode. Some internal-neural details are outside accessible representation rather than unused components.

## Alternative Representations Considered

- Treating the output text alone as the representation was rejected because it confuses answer encoding with reasoning-process preservation.
- Treating chain-of-thought as the actual internal process was rejected unless source evidence establishes that role.
- A mechanistic-neural mapping of every activation was retained as possible only for open models with weights and instrumentation; otherwise unresolved/outside scope.

## Potential Counterexamples

- Proprietary LLMs with hidden prompts, weights, filters, retrieval, and sampling seeds may not permit operational or information preservation.
- Plausible but false generated explanations may satisfy output format while failing faithful process representation.
- Stochastic decoding may prevent exact replay even when prompt and model are known.
- Emergent behavior might depend on training-data regularities not recorded in the episode.

## Counterexample Classification

- Hidden proprietary episode: `outside scope` for internal process evidence; lower-precedence plausible category is `unresolved` for visible input-output behavior.
- False chain-of-thought as process evidence: `not a counterexample` to FAR/FARA, but a failed representation choice because it does not preserve the target process.
- Stochastic non-replay: `conservative extension pressure` when model/settings are known, because probabilistic transition policy can be represented but exact replay may not be expected.
- Training-provenance dependence: `unresolved` unless evidence shows the dependence is required and inaccessible.

## Classification

`unresolved`

## Justification

The system is in scope only for documented visible episodes. Preservation of semantic, operational, dependency, and information dimensions remains unknown for ordinary proprietary or under-instrumented LLM reasoning. The pressure is not yet a candidate primitive failure because the missing material is accessibility, probabilistic machinery, and model-specific metadata rather than a demonstrated sixth primitive.

## Limitations

Applies only to documented inference episodes. It does not evaluate training, mechanistic interpretability, hidden safety systems, multimodal reasoning, or all LLM architectures. It cannot distinguish genuine internal reasoning from post-hoc explanation without additional evidence.

## Methodology Feedback

No methodology defect was discovered. The methodology forced explicit unknown/outside-scope handling rather than rescue reinterpretation.

## Implications

### Universality

This investigation weakens any premature universality claim because an important modern reasoning-like system often cannot be fully preserved from public evidence. It does not refute FAR/FARA for explicit reasoning because visible episodes remain partially representable and hidden processes may be outside scope.

### Necessity

The case supports the practical need for structure, interpretation, calculus, state, and dependency tracking in opaque computational reasoning episodes. It does not prove necessity globally.

### Minimality

No minimality support is generated. The need for probabilistic/model metadata creates pressure to test whether some FARA machinery is derived or whether reusable AI-specific derived concepts are needed.

## Confidence

Moderate for the unresolved classification; high that public/proprietary LLM episodes create operational and information preservation pressure.

## Remaining Questions

- What minimum model metadata is sufficient for operational equivalence?
- Can open-weight instrumented models convert this classification from unresolved to conservative extension?
- How should reports distinguish faithful process traces from generated rationales?
