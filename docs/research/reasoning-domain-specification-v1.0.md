# Reasoning Domain Specification v1.0

## Status

Frozen prospective research-domain specification for Milestone 1 of the Architecture-Neutral Research Roadmap.

This document determines what classes of systems Project FAR intends to investigate before any architecture-neutral mathematical definition of reasoning is proposed. It does not define reasoning mathematically, endorse FARA, establish a preservation basis, or classify any candidate architecture as universal or minimal.

## Purpose

The purpose of this specification is to prevent the later definition of reasoning from silently selecting only systems that already resemble FARA or another favored candidate. It fixes a broad target domain, known boundary cases, exclusion rules, and an admission process against which later formal definitions must be evaluated.

## Governing constraints

1. Domain membership may not depend on whether a system is easy to encode in FARA.
2. No FARA primitive is a required domain criterion.
3. A system may remain unresolved without being excluded.
4. Lack of internal-state access does not by itself make a system non-reasoning; it may limit the claims that can be tested.
5. Human, machine, individual, collective, symbolic, probabilistic, embodied, and hybrid systems are not privileged or excluded by substrate alone.
6. Historical failures, disputed cases, and systems unfavorable to FARA must remain in the research record.
7. A scope restriction adopted after exposure to a difficult case must be treated as a revision and justified independently.

## Domain-level inclusion question

A process is eligible for study when there is a serious, independently motivated claim that its behavior involves one or more of the following:

- forming, revising, maintaining, comparing, or rejecting commitments;
- drawing conclusions from information, assumptions, constraints, rules, models, evidence, or prior states;
- selecting among alternatives through reasons, evidence, inference, evaluation, or structured transformation;
- constructing or modifying representations in a way relevant to a question, objective, decision, explanation, prediction, proof, diagnosis, or interpretation;
- coordinating multiple partial processes whose combined activity is plausibly described as reasoning.

These are admission indicators, not a mathematical definition and not individually necessary or jointly sufficient conditions.

## Target classes

### D1 — Deductive and formal proof systems

Includes natural-deduction systems, sequent calculi, theorem provers, model checkers, proof assistants, and mathematical proof practices.

Required variation coverage:

- monotonic and nonmonotonic rules;
- classical, intuitionistic, paraconsistent, modal, temporal, and other logics;
- proof search, proof checking, and proof revision;
- explicit and compressed proof objects.

### D2 — Rule-based and symbolic inference systems

Includes expert systems, production systems, logic programs, planning systems, constraint solvers, and symbolic agents.

Required variation coverage:

- fixed and self-modifying rule sets;
- defeasible and priority-sensitive rules;
- forward, backward, and mixed inference;
- hidden and explicit control policies.

### D3 — Probabilistic and statistical reasoning

Includes Bayesian inference, probabilistic programming, statistical model comparison, uncertainty revision, forecasting, and decision under uncertainty.

Required variation coverage:

- precise and imprecise probabilities;
- updating, conditioning, approximation, and model revision;
- uncertainty over hypotheses, rules, observations, and utilities;
- cases where numerical equivalence hides different dependency or causal commitments.

### D4 — Causal, explanatory, and diagnostic reasoning

Includes causal-model construction, diagnosis, abduction, explanation selection, counterfactual reasoning, and mechanistic inference.

Required variation coverage:

- multiple competing explanations;
- intervention and counterfactual distinctions;
- causal discovery and causal revision;
- explanatory adequacy not reducible to prediction alone.

### D5 — Scientific and empirical investigation

Includes hypothesis formation, experimental design, measurement interpretation, evidence integration, theory revision, and replication reasoning.

Required variation coverage:

- incomplete and noisy observation;
- changing instruments or measurement models;
- underdetermination and competing theories;
- social and institutional components of scientific reasoning.

### D6 — Legal, normative, and policy reasoning

Includes statutory interpretation, case-law reasoning, defeasible authority, standards of proof, ethical deliberation, policy analysis, and practical justification.

Required variation coverage:

- authority hierarchies;
- jurisdiction and time-indexed sources;
- conflicting norms and exceptions;
- descriptive, interpretive, and normative conclusions.

### D7 — Analogical, case-based, and similarity-driven reasoning

Includes analogy, precedent transfer, case-based reasoning, metaphor-supported inference, and structural comparison.

Required variation coverage:

- relevance selection;
- source-target alignment;
- feature construction rather than only feature matching;
- creative or contested analogies.

### D8 — Planning, decision, and practical reasoning

Includes means-end planning, scheduling, game reasoning, action selection, resource-sensitive deliberation, and multiobjective decision processes.

Required variation coverage:

- changing goals;
- conflicting objectives;
- bounded resources;
- partial observability;
- policies, plans, and replanning.

### D9 — Learning and model-revision systems

Includes systems that revise hypotheses, rules, representations, parameters, abstractions, or policies using data or feedback.

Required variation coverage:

- online and offline learning;
- representation change;
- catastrophic revision and gradual update;
- learned internal structures whose interpretation is uncertain.

Learning alone is not presumed to be reasoning; the relevant question is whether and how learning participates in a process plausibly claimed to reason.

### D10 — Language-model and neural reasoning claims

Includes chain-of-thought-like traces, hidden-state computation, tool-using language models, neural theorem provers, multimodal systems, and systems whose claimed reasoning may not be fully observable.

Required variation coverage:

- visible trace versus hidden computation;
- faithful versus post hoc explanation;
- stochastic outputs;
- prompt, context, memory, and tool dependence;
- systems for which only input-output behavior is available.

This class must permit the outcome that available evidence is insufficient to determine whether a particular run instantiates the later formal definition.

### D11 — Agentic and tool-mediated systems

Includes autonomous or semi-autonomous agents that plan, call tools, inspect environments, maintain memory, delegate tasks, and revise behavior.

Required variation coverage:

- asynchronous actions;
- external memory;
- environmental feedback;
- changing tools and capabilities;
- partial trace capture;
- failure recovery and self-modification.

### D12 — Human individual reasoning

Includes explicit and tacit human reasoning in mathematics, science, diagnosis, law, everyday choice, creativity, and interpretation.

Required variation coverage:

- verbalizable and nonverbal processes;
- perceptual and embodied contributions;
- memory limitations;
- emotion and motivation where causally relevant;
- confabulation and incomplete introspective access.

The project must distinguish a model of documented reasoning from a claim about all underlying cognition.

### D13 — Collective and distributed reasoning

Includes committees, scientific communities, courts, markets where inferential claims are made, multi-agent systems, debate, deliberation, and organizational decision procedures.

Required variation coverage:

- disagreement;
- distributed evidence;
- communication constraints;
- authority and role structure;
- emergent conclusions not attributable to one participant;
- asynchronous and adversarial interaction.

### D14 — Embodied and situated reasoning

Includes reasoning claims in robotics, active perception, navigation, sensorimotor planning, and systems whose environment participates materially in the process.

Required variation coverage:

- externalized state;
- continuous dynamics;
- action-dependent observation;
- environmental scaffolding;
- representations that may be implicit or disputed.

### D15 — Self-modifying and reflective reasoning

Includes systems that inspect or change their own rules, objectives, representations, proof procedures, evaluation standards, or architecture.

Required variation coverage:

- meta-reasoning;
- reflective consistency problems;
- rule replacement and versioned history;
- changes to admissible future transitions;
- self-reference and circular support.

### D16 — Adversarial, deceptive, and strategically opaque reasoning

Includes argumentation under incentives, adversarial planning, deception, security reasoning, and systems that conceal or manipulate evidence about their internal process.

Required variation coverage:

- public versus private commitments;
- strategic reporting;
- misleading traces;
- adversarially selected observations;
- evaluator uncertainty.

## Cross-cutting variation requirements

The later mathematical definition must be tested against systems varying along at least these axes:

- discrete versus continuous state;
- deterministic versus stochastic transition;
- static versus changing representational types;
- monotonic versus retractable commitments;
- centralized versus distributed control;
- explicit versus partially observable state;
- terminating versus open-ended operation;
- fixed versus changing goals;
- synchronous versus asynchronous activity;
- finite versus potentially unbounded history;
- exact versus approximate inference;
- symbolic versus subsymbolic implementation;
- individual versus collective agency;
- passive inference versus action-coupled inquiry.

## Boundary and unresolved classes

The following must not be automatically classified either as reasoning or non-reasoning:

- reflexes and fixed stimulus-response loops;
- simple feedback controllers;
- lookup tables;
- static classifiers;
- optimization without interpretable intermediate commitments;
- evolutionary search;
- associative recall;
- perception-only pipelines;
- dream-like or unconstrained generation;
- social aggregation without identifiable inferential function;
- opaque systems with reasoning-like outputs but insufficient evidence;
- systems whose apparent reasoning is entirely supplied by an external operator.

Each such case requires classification under an independently justified later definition. Until then its status is `boundary_unresolved`.

## Provisional exclusions

The following are outside the active domain unless a future revision supplies a serious reasoning claim and testable observables:

1. purely physical evolution described with no claim of information-sensitive inference, evaluation, deliberation, or commitment change;
2. arbitrary state transitions labeled as reasoning solely to obtain universal coverage;
3. artifacts containing only a final answer with no accessible basis for testing anything beyond input-output adequacy, where the research claim requires internal preservation;
4. fictional or metaphorical uses of “reasoning” with no proposed operational interpretation;
5. systems admitted only because their structure matches a candidate architecture.

Exclusion from the active domain is not a claim that the process cannot reason in principle. It states that the current research package lacks an independently justified and testable reasoning claim.

## Observability strata

Every admitted case must be assigned one of these strata:

- **O0 — Input/output only:** only stimuli, prompts, actions, or final outputs are available.
- **O1 — Reported trace:** an explanation or trace is available but fidelity to the producing process is unestablished.
- **O2 — Instrumented operational trace:** state changes, dependencies, actions, or updates are captured under a defined instrumentation contract.
- **O3 — White-box specification:** the transition rules or complete formal implementation are available.
- **O4 — Proven correspondence:** a formal result links the recorded trace or model to the process properties relevant to the claim.

A lower stratum limits the strength of conclusions. It must not be repaired by inventing hidden structure.

## Evidence-source classes

Cases should be drawn from independently motivated sources, including:

- established formal systems;
- published empirical or computational systems;
- real documented human or institutional practices;
- independently authored benchmarks;
- adversarially proposed cases;
- synthetic controls designed before candidate exposure;
- privately held boundary cases.

Candidate-authored examples may be used for implementation testing but cannot alone establish domain adequacy.

## Sampling obligations

A future domain corpus must not be treated as representative merely because it is large. It must document:

- the target classes covered;
- variation axes covered;
- observability strata;
- source provenance;
- known omissions;
- duplicate or near-duplicate families;
- candidate-author involvement;
- why each case is evidentially useful.

At least one difficult or unfavorable case must be retained for every target class where such a case is known.

## Domain admission procedure

A new domain class or case may be admitted only with:

1. a plain-language reasoning claim independent of FARA;
2. source provenance;
3. intended scope;
4. observable or inferable features relevant to testing that claim;
5. observability stratum;
6. known ambiguity and alternative non-reasoning explanations;
7. expected pressure on at least one current assumption or candidate;
8. a declaration of candidate-author involvement;
9. a permanent identifier and version;
10. a pre-exposure decision on whether the case is exploratory, confirmatory, control, boundary, or holdout material.

## Revision and freeze policy

This version is frozen for use in constructing the independent mathematical definition.

A revision must:

- receive a new version;
- preserve the prior version;
- state whether it adds, removes, splits, or merges a target class;
- state which observed case motivated the revision;
- disclose whether candidate or benchmark exposure occurred;
- identify any theorem, experiment, or claim whose scope changes;
- avoid retroactively reclassifying unfavorable evidence without an explicit supersession record.

## Candidate-neutrality audit

This specification passes the following prospective checks:

- no target class is defined by the presence of Representation, Structure, Interpretation, Investigation, or Calculus;
- FARA is not referenced as an admission criterion;
- target classes include systems that may pressure explicit-state, symbolic, centralized, fixed-rule, and fully observable assumptions;
- systems may be unresolved rather than repaired into candidate-compatible form;
- alternative architectures may use this same domain without adopting FARA terminology;
- failure to define one common mathematical class is an allowed outcome;
- a future result may support multiple incompatible reasoning classes or no finite universal architecture.

## Required output of the next milestone

The next milestone must propose one or more mathematical definitions and show, case by case, how they address this frozen domain.

For every clause in a proposed definition, it must state:

1. which domain classes or boundary problems motivate the clause;
2. whether the clause excludes any admitted cases;
3. whether the clause privileges a known candidate;
4. what counterexample would show the clause is too weak or too strong;
5. whether multiple definitions are required.

## Current conclusion

Project FAR now has a frozen architecture-neutral target domain, not a final definition of reasoning. The principal unresolved question is whether one mathematical class can cover the admitted target without triviality, candidate bias, or loss of relevant distinctions.