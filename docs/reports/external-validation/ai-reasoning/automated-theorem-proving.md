# Target System
Automated Theorem Proving

# Source and Scope
Automated theorem proving and proof assistants. Sources: Robinson, "A Machine-Oriented Logic Based on the Resolution Principle", https://doi.org/10.1145/321250.321253; Harrison, Urban, and Wiedijk, "History of Interactive Theorem Proving", https://doi.org/10.1016/B978-0-444-51624-4.50004-6; Coq reference documentation, https://coq.inria.fr/doc/; Isabelle documentation, https://isabelle.in.tum.de/documentation.html; SMT-LIB standard, https://smt-lib.org/. Scope is formal proof, search, verification, theorem representation, completeness limits, search explosion, and proof certificates.

# Architecture
Formal logic engine, proof assistant, SAT/SMT solver, or ATP system combining theorem representation, calculus rules, search heuristics, decision procedures, and proof checking where available.

# Representation
Formal languages, terms, formulas, types, axioms, definitions, inference rules, goals, proof states, proof objects, models, countermodels, and certificates.

# Reasoning Process
Reasoning applies sound inference rules, search strategies, unification, rewriting, decision procedures, induction tactics, or model finding. Verification checks whether a proof object or certificate follows accepted rules.

# Hidden Assumptions
The formalization captures the intended claim; axioms are accepted; the calculus is sound for the target semantics; tactics and solvers are trusted or independently checked; resource bounds do not imply semantic failure.

# Failure Modes
Search explosion, undecidability, incomplete heuristics, malformed formalization, unsound trusted kernels, missing proof certificates, and mismatch between informal theorem and formal encoding.

# Adversarial Analysis
Adversarial cases include false axioms, hidden inconsistent assumptions, statements outside decidable fragments, proof search timeout, and certificates accepted by an unsound checker. FAR can expose dependencies but cannot create a proof if the ATP search fails.

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
