# Adversarial Analysis

Status: Provisional adversarial analysis for the current suite in `theory/falsification/adversarial-test-suite.yaml`.

This document classifies each adversarial test under the required standard. The analysis is intentionally conservative: unresolved pressure is not falsification, and a conservative extension is not evidence that FAR requires a sixth primitive.

## Classification summary

- Total adversarial tests: 14
- Resolved by existing primitive: 3
- Conservative extension: 10
- Unresolved pressure: 1
- Candidate primitive failure: 0

Current adversarial tests have not yet established a primitive-level counterexample.

## Classification standard

- `resolved by existing primitive`: the pressure is already handled directly by one or more of the five primitives without needing a new derived concept.
- `conservative extension`: the case requires a new domain-specific rule, interpretation policy, representational structure, or derived concept, but does not require a sixth primitive.
- `unresolved pressure`: the case appears representable, but current repository machinery is not sufficient to justify a final decision.
- `candidate primitive failure`: explicit reasoning is present, the pressure cannot be represented using the five primitives, no existing derived concept resolves it, no conservative extension appears sufficient, and the missing capability appears to require a genuinely new primitive.

## Test analyses

### ADV-001 — Higher-order Logic

- Reasoning system: Higher-order Logic
- Target assumption: Higher-order quantification may require predicates over predicates without adding primitives.
- Primitive under pressure: Representation
- Why this could threaten FAR: If predicate-level entities could not be represented as objects of reasoning, Representation might be too weak.
- Investigation: The case can be treated as an investigation into explicit higher-order inference.
- Representation: Predicates, predicates over predicates, and typed variables are represented content.
- Representational Structure: Type levels and application relations are structural constraints on representations.
- Interpretation: Semantics for higher-order variables interpret the represented entities.
- Reasoning Calculus: Higher-order inference rules govern transformations among formulas.
- Existing derived concept: None required for this classification.
- Conservative extension: Type discipline may be useful, but the core pressure is already representational.
- Final classification: resolved by existing primitive
- Confidence: high
- Remaining open questions: Whether impredicative encodings require repository-specific derived constraints.

### ADV-002 — Reflective Reasoning

- Reasoning system: Reflective Reasoning
- Target assumption: Reasoning about a reasoning process may stress interpretation and self-reference handling.
- Primitive under pressure: Interpretation
- Why this could threaten FAR: Reflection can blur the boundary between object reasoning and interpretation of that reasoning.
- Investigation: The reflective episode is an investigation whose object includes a reasoning trace.
- Representation: The trace, rules, and reflective claims can be represented.
- Representational Structure: Self-reference and trace relations can be structured.
- Interpretation: The main pressure is assigning meaning to represented reasoning without collapse.
- Reasoning Calculus: Reflection rules can be stated as calculus rules.
- Existing derived concept: Reasoning trace, if treated as derived content, is sufficient as an object of interpretation.
- Conservative extension: A reflection policy is needed for circular or self-endorsing interpretations.
- Final classification: conservative extension
- Confidence: medium
- Remaining open questions: Specify reflection policy boundaries for circular or self-endorsing interpretations.

### ADV-003 — Self-Modifying Reasoning

- Reasoning system: Self-Modifying Reasoning
- Target assumption: Reasoning that changes its own rules may stress reasoning-calculus representation.
- Primitive under pressure: Reasoning Calculus
- Why this could threaten FAR: If a system changes its own calculus from within, a static account of calculus may be insufficient.
- Investigation: The change process can be investigated as a sequence of reasoning states.
- Representation: Rules before and after modification can be represented.
- Representational Structure: Transition relations among calculi can be represented structurally.
- Interpretation: The meaning of a self-authorized rule change requires interpretation of rule provenance and validity.
- Reasoning Calculus: The pressure is whether calculus replacement is itself governed by a calculus.
- Existing derived concept: No existing derived concept in the current adversarial materials resolves self-directed calculus replacement.
- Conservative extension: A transition-policy extension may be sufficient, but the current repository does not yet justify that conclusion.
- Final classification: unresolved pressure
- Confidence: medium
- Remaining open questions: Determine whether self-modifying calculi need only transition policies or expose deeper primitive pressure.

### ADV-004 — Probabilistic Programming

- Reasoning system: Probabilistic Programming
- Target assumption: Programs with probabilistic inference may stress representation of stochastic dependencies and execution traces.
- Primitive under pressure: Representational Structure
- Why this could threaten FAR: Probabilistic dependencies might appear to require probabilistic primitives beyond structural representation.
- Investigation: Model construction and inference form an investigation.
- Representation: Random variables, observations, programs, and traces are represented content.
- Representational Structure: Dependency graphs, traces, and conditioning relations are the main structures.
- Interpretation: Probability measures interpret represented stochastic structure.
- Reasoning Calculus: Inference algorithms or update rules govern reasoning steps.
- Existing derived concept: Execution trace can be treated as a derived representational object.
- Conservative extension: Probability kernels, conditioning rules, and trace semantics are domain-specific extensions.
- Final classification: conservative extension
- Confidence: high
- Remaining open questions: Formalize probabilistic trace structures and inference-policy constraints if promoted.

### ADV-005 — Belief Revision

- Reasoning system: Belief Revision
- Target assumption: Revision under new information may stress transitions between representations and calculi.
- Primitive under pressure: Reasoning Calculus
- Why this could threaten FAR: Revision can change accepted commitments while preserving rational constraints.
- Investigation: Revision occurs inside an investigation responding to new evidence.
- Representation: Belief states and incoming information are represented.
- Representational Structure: Priority, consistency, and entrenchment relations can be structured.
- Interpretation: Revision outcomes require interpretation as accepted, rejected, or suspended commitments.
- Reasoning Calculus: Revision postulates and update rules govern transitions.
- Existing derived concept: Belief state can be used as a derived representational object.
- Conservative extension: Domain-specific revision postulates are needed.
- Final classification: conservative extension
- Confidence: high
- Remaining open questions: Identify minimal revision policies needed for conflicting evidence.

### ADV-006 — Argumentation Frameworks

- Reasoning system: Argumentation Frameworks
- Target assumption: Attack, defense, and acceptability relations may stress relational structure.
- Primitive under pressure: Representational Structure
- Why this could threaten FAR: Acceptability may appear to require a special argumentative primitive.
- Investigation: Argument evaluation is an investigation over competing claims.
- Representation: Arguments and claims are represented objects.
- Representational Structure: Attack, defense, and acceptability relations are direct relational structures.
- Interpretation: Semantics interpret which arguments are accepted under a selected policy.
- Reasoning Calculus: Extension-computation rules provide the calculus.
- Existing derived concept: None required for the core pressure.
- Conservative extension: Particular semantics may be conservative policies, but primitive coverage is direct.
- Final classification: resolved by existing primitive
- Confidence: high
- Remaining open questions: Assess only whether particular semantics introduce conservative policies.

### ADV-007 — Multi-Agent Reasoning

- Reasoning system: Multi-Agent Reasoning
- Target assumption: Interacting agents with distinct beliefs and goals may stress investigation boundaries.
- Primitive under pressure: Investigation
- Why this could threaten FAR: Multiple agents may produce overlapping investigations with incompatible commitments.
- Investigation: Each agent can be modeled as an investigation, with interaction among investigations.
- Representation: Agent beliefs, goals, messages, and actions are represented.
- Representational Structure: Communication and accessibility relations structure the interaction.
- Interpretation: Agent-indexed claims require interpretation relative to the agent and context.
- Reasoning Calculus: Update and decision rules govern agent-level reasoning.
- Existing derived concept: Agent-indexed investigation can function as a derived concept.
- Conservative extension: A scoping policy is needed for when investigations merge, nest, or remain separate.
- Final classification: conservative extension
- Confidence: medium
- Remaining open questions: Define when interacting investigations merge, nest, or remain separate.

### ADV-008 — Interactive Theorem Proving

- Reasoning system: Interactive Theorem Proving
- Target assumption: Human-guided proof construction may stress the boundary between explicit reasoning and external intervention.
- Primitive under pressure: Investigation
- Why this could threaten FAR: External choices could be mistaken for internal explicit reasoning.
- Investigation: The proof attempt is an investigation with recorded interventions.
- Representation: Goals, tactics, proof states, and human inputs are represented.
- Representational Structure: Proof-state transitions and dependency graphs structure the activity.
- Interpretation: The status of human choices must be interpreted as evidence, guidance, or oracle input.
- Reasoning Calculus: Kernel rules and tactic expansion provide calculi.
- Existing derived concept: Proof-state provenance can be treated as a derived concept.
- Conservative extension: A provenance policy is needed to separate explicit reasoning from external intervention.
- Final classification: conservative extension
- Confidence: medium
- Remaining open questions: Clarify treatment of human choices, tactics, and oracle-like steps.

### ADV-009 — Meta-Reasoning

- Reasoning system: Meta-Reasoning
- Target assumption: Reasoning about reasoning standards may stress interpretation and calculus layering.
- Primitive under pressure: Interpretation
- Why this could threaten FAR: Meta-level claims can collapse into object-level claims if levels are not controlled.
- Investigation: The object of inquiry is a reasoning standard or calculus.
- Representation: Standards, rules, and evaluations are represented.
- Representational Structure: Object/meta-level relations structure the represented material.
- Interpretation: Interpretation maps claims to the appropriate level.
- Reasoning Calculus: Meta-rules govern evaluation of lower-level reasoning.
- Existing derived concept: Level-indexed interpretation can be used as a derived concept.
- Conservative extension: A meta-interpretation discipline is needed.
- Final classification: conservative extension
- Confidence: medium
- Remaining open questions: State anti-collapse conditions for object/meta-level interpretation.

### ADV-010 — Learning Systems

- Reasoning system: Learning Systems
- Target assumption: Model adaptation from data may stress whether learned updates are explicit reasoning.
- Primitive under pressure: Reasoning Calculus
- Why this could threaten FAR: Training or adaptation may be non-explicit while still affecting later reasoning.
- Investigation: Learning can be investigated as evidence-driven model update.
- Representation: Data, parameters, hypotheses, and outputs are represented.
- Representational Structure: Model architecture and data relations structure the updates.
- Interpretation: Learned states must be interpreted as evidence, policy, or latent representation.
- Reasoning Calculus: Update rules, optimization, or inference policies govern transitions when explicit.
- Existing derived concept: Learned model state can be treated as derived representational content.
- Conservative extension: Learning-specific update semantics are needed.
- Final classification: conservative extension
- Confidence: medium
- Remaining open questions: Decide when non-explicit training dynamics count as reasoning evidence.

### ADV-011 — Quantum Logic

- Reasoning system: Quantum Logic
- Target assumption: Non-classical lattice structure may stress representational structure.
- Primitive under pressure: Representational Structure
- Why this could threaten FAR: Non-Boolean structure might seem to require a non-classical primitive.
- Investigation: Quantum-logical inference is an investigation over propositions with non-classical relations.
- Representation: Propositions and measurement contexts are represented.
- Representational Structure: Orthomodular or related lattice relations provide structure.
- Interpretation: Quantum semantics interpret represented propositions.
- Reasoning Calculus: Quantum-logical inference rules govern valid steps.
- Existing derived concept: Lattice-structured representation can be treated as derived structure.
- Conservative extension: Domain-specific quantum-logical semantics are needed.
- Final classification: conservative extension
- Confidence: high
- Remaining open questions: Document which quantum-logical semantics are assumed when evaluating inference.

### ADV-012 — Dynamic Logic

- Reasoning system: Dynamic Logic
- Target assumption: Modal reasoning about programs and state changes may stress calculus and transition representation.
- Primitive under pressure: Reasoning Calculus
- Why this could threaten FAR: Program modalities combine state transition and logical consequence.
- Investigation: Program correctness or reachability is the investigation.
- Representation: Programs, states, and formulas are represented.
- Representational Structure: Transition relations structure possible executions.
- Interpretation: Modal semantics interpret program-indexed formulas.
- Reasoning Calculus: Rules for sequence, choice, iteration, and modalities govern reasoning.
- Existing derived concept: Program-indexed transition relation can be derived.
- Conservative extension: Transition semantics for program modalities are needed.
- Final classification: conservative extension
- Confidence: high
- Remaining open questions: Specify the minimal transition semantics used for program modalities.

### ADV-013 — Hybrid Logic

- Reasoning system: Hybrid Logic
- Target assumption: Named worlds and satisfaction operators may stress interpretation across indexed contexts.
- Primitive under pressure: Interpretation
- Why this could threaten FAR: Satisfaction-at operators require stable interpretation across named contexts.
- Investigation: The reasoning task investigates modal claims across indexed worlds.
- Representation: Worlds, nominals, formulas, and satisfaction claims are represented.
- Representational Structure: Accessibility and naming relations structure the contexts.
- Interpretation: Indexed interpretation is the central pressure.
- Reasoning Calculus: Hybrid-logical rules govern movement among contexts.
- Existing derived concept: Named context can be used as derived representational content.
- Conservative extension: An index-management policy is needed.
- Final classification: conservative extension
- Confidence: high
- Remaining open questions: Clarify cross-world interpretation and satisfaction-at operators.

### ADV-014 — Description Logic

- Reasoning system: Description Logic
- Target assumption: Concept-role structures and subsumption reasoning may stress representation and structure.
- Primitive under pressure: Representation
- Why this could threaten FAR: Concept and role constructors might appear to require ontology-specific primitives.
- Investigation: Classification and satisfiability checking are investigations.
- Representation: Concepts, roles, individuals, and axioms are represented content.
- Representational Structure: Subsumption, role, and membership relations structure the representation.
- Interpretation: Model-theoretic semantics interpret the represented ontology.
- Reasoning Calculus: Tableau or consequence rules govern inference.
- Existing derived concept: None required for the core representational pressure.
- Conservative extension: Specific description-logic family features may need semantic policies.
- Final classification: resolved by existing primitive
- Confidence: high
- Remaining open questions: Additional description-logic family features may need conservative semantic policies.

## Current conclusion

No candidate primitive failure has been established by the current adversarial batch. The strongest remaining pressure is ADV-003, self-modifying reasoning, because the repository does not yet justify whether self-directed calculus replacement is fully resolved by conservative transition policies. That unresolved pressure is not falsification.

Conservative extensions identified here are domain-specific policies, structures, or derived concepts; they do not by themselves require a sixth primitive. FAR therefore remains provisionally unfalsified by this adversarial batch. This does not prove FAR universal, and it does not finally establish that the five primitives are sufficient for all reasoning systems.
