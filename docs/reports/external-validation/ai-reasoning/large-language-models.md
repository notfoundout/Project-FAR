# Target System
Large Language Models

# Source and Scope
Transformer-based large language models trained by next-token prediction. Sources: Vaswani et al., "Attention Is All You Need", https://arxiv.org/abs/1706.03762; Brown et al., "Language Models are Few-Shot Learners", https://arxiv.org/abs/2005.14165; Lewis et al., "Retrieval-Augmented Generation", https://arxiv.org/abs/2005.11401; OpenAI documentation on text generation and prompt engineering, https://platform.openai.com/docs/. Scope is methodological: token prediction, context window use, attention, probabilistic inference, hallucination risk, optional chain-of-thought representation, retrieval augmentation, and limits.

# Architecture
Layered neural sequence model, usually transformer attention over token embeddings, trained to estimate conditional token distributions and then decoded into text.

# Representation
Tokens, embeddings, positional/context information, learned parameters, optional retrieved passages, prompt instructions, and generated output sequences.

# Reasoning Process
Inference samples or selects tokens conditioned on context. Apparent reasoning can be represented as latent computation, explicit intermediate text, retrieved evidence use, or tool-mediated augmentation, but token prediction remains the core mechanism.

# Hidden Assumptions
Training corpora are adequate for learned regularities; context contains sufficient task information; decoding policy preserves intended constraints; retrieved documents are relevant when retrieval is used; chain-of-thought text, when exposed or requested, is an optional representation and not guaranteed to mirror hidden computation.

# Failure Modes
Hallucination, prompt sensitivity, stale or missing knowledge, context overflow, spurious correlations, brittle multi-step reasoning, retrieval contamination, and overconfident output.

# Adversarial Analysis
Adversarial prompts can exploit instruction conflicts, ambiguous references, false premises, or missing evidence. FAR can expose dependencies and uncertainty, but it cannot inspect hidden activations or prove output truth.

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
