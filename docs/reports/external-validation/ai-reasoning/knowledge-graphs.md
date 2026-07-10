# Target System
Knowledge Graphs

# Source and Scope
Knowledge graphs and ontology-mediated reasoning. Sources: Hogan et al., "Knowledge Graphs", https://doi.org/10.1145/3447772; W3C RDF 1.1 Concepts, https://www.w3.org/TR/rdf11-concepts/; W3C OWL 2 Overview, https://www.w3.org/TR/owl2-overview/; W3C SPARQL 1.1 Query Language, https://www.w3.org/TR/sparql11-query/. Scope is entity representation, relation graphs, ontology, inference, traversal, ambiguity, and incomplete knowledge.

# Architecture
Graph-based information system with nodes/entities, edges/relations, literals, schemas or ontologies, query processors, and optional rule or description-logic reasoners.

# Representation
Entities, identifiers, triples or property graphs, relation types, classes, axioms, constraints, provenance, and query results.

# Reasoning Process
Reasoning proceeds by graph traversal, pattern matching, rule application, ontology entailment, constraint checking, or embedding-based link prediction when statistical extensions are used.

# Hidden Assumptions
Identifiers refer consistently; ontology commitments are accepted; closed-world or open-world treatment is specified; missing edges may mean unknown rather than false; relation semantics are stable enough for inference.

# Failure Modes
Entity ambiguity, duplicate identifiers, incomplete facts, inconsistent ontologies, schema drift, relation misinterpretation, provenance gaps, and computational limits for expressive reasoning.

# Adversarial Analysis
Adversarial cases include same-name entities, contested classifications, missing negative facts, inconsistent taxonomies, and queries that silently assume closed-world completeness. FAR can separate representation from interpretation but cannot supply missing facts.

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
