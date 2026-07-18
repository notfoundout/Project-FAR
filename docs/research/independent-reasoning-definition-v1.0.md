# Independent Mathematical Definition of Reasoning v1.0

## Status

Frozen prospective definition for the second scientific milestone of the Architecture-Neutral Research Roadmap.

This definition is independent of FARA and every other candidate architecture. It fixes a mathematical target for later preservation, representation, lower-bound, equivalence, and impossibility research. It does not establish that FARA represents the target, that the target is universal, or that one finite architecture can preserve every admitted instance.

## Dependencies

This definition is constrained by:

- `docs/research/reasoning-domain-specification-v1.0.md`;
- `theory/evaluation/reasoning-domain-registry.json`;
- `docs/governance/research-architecture.md`;
- the Anti-Self-Validation Standard and current evidence rules.

It does not depend on `frameworks/FARA/`, `frameworks/FARO/`, the FAR interchange format, or any candidate compiler or verifier.

## Design objective

The definition must be broad enough to admit symbolic, probabilistic, causal, analogical, practical, learned, human, collective, embodied, self-modifying, and partially observable reasoning claims, while remaining narrow enough to reject arbitrary state change merely labeled as reasoning.

No substrate, notation, explicit-symbol requirement, centralized controller, fixed rule set, fixed objective, termination condition, or complete introspective trace is required.

## Mathematical setting

A **process presentation** is a tuple

\[
\mathcal{P}=(T,X,\mathcal{H},\mathcal{O},\mathcal{K},\mathcal{Q},\Delta,\Gamma,\Vdash)
\]

with the following components.

### Time or event index `T`

`T` is a nonempty partially ordered set of process locations. It may represent discrete time, continuous time, causal order, asynchronous events, or a finite or unbounded execution history.

A total global clock is not required.

### Process states `X`

For each `t ∈ T`, `X_t` is the state of the process at `t`. A state may include internal, external, environmental, social, embodied, distributed, latent, or instrumented components.

The definition does not require the complete state to be observable or symbolically represented.

### Histories `H`

A history `h ∈ H` is an admissible assignment of states and events over a down-closed subset of `T`. Histories preserve temporal or causal order sufficient to distinguish earlier conditions from later consequences.

### Observations `O`

For each admissible history prefix `h|t`, `O(h,t)` is the evidence available to the investigator under a declared observation contract.

`O` may expose only inputs and outputs, a reported trace, an instrumented trace, a white-box specification, or a formally proved correspondence. Observability is not identical to process ontology.

### Commitments `K`

For each history prefix, `K(h,t)` is a set or structured space of **commitment states**. A commitment is any process-relative stance whose retention, revision, comparison, rejection, weighting, or use can affect what the process subsequently treats as acceptable, preferable, supported, required, possible, intended, explanatory, predictive, or action-guiding.

Commitments need not be sentences, conscious beliefs, explicit symbols, or stable objects. They may be probabilistic, graded, distributed, implicit, action-coupled, temporary, or externally scaffolded.

### Questions or stakes `Q`

`Q(h,t)` records the issue, task, uncertainty, objective, conflict, proof obligation, decision, interpretation, prediction, diagnosis, or other stake relative to which a commitment change can count as reason-sensitive.

`Q` may itself change. The definition does not require one fixed goal or one privileged agent.

### Admissible evolutions `Δ`

`Δ` assigns to each admissible history prefix a nonempty set or distribution of permitted continuations. It may be deterministic, stochastic, nondeterministic, continuous, approximate, learned, self-modifying, or partly environment-controlled.

### Grounds and constraints `Γ`

For each history prefix, `Γ(h,t)` identifies the information, evidence, assumptions, norms, models, similarities, causal hypotheses, goals, resource constraints, environmental feedback, testimony, procedures, or prior commitments that are claimed to make a difference to later commitment or action.

`Γ` is architecture-neutral. It does not require these grounds to be divided into FARA primitives.

### Support relation `⊨`

`g ⊨_{h,t,q} k` means that, under the declared process interpretation and scope, ground configuration `g` counts as supporting, defeating, constraining, selecting, licensing, or otherwise making commitment `k` relevant to stake `q` at `(h,t)`.

This relation may be logical, probabilistic, causal, analogical, normative, practical, institutional, learned, approximate, or contested. It must be externally testable or explicitly marked unresolved at the available observability stratum.

## Core definition

A process presentation `P` contains a **reasoning episode** over interval or event region `J ⊆ T` exactly when all six conditions below are satisfied within a declared scope.

### R1 — Situated stake

There is at least one nontrivial stake `q ∈ Q` for which different commitment or action outcomes are distinguishable.

A process with no identifiable issue, objective, uncertainty, constraint conflict, evaluation target, or inferential stake does not satisfy this condition.

### R2 — Alternative-sensitive commitment space

At some point in `J`, at least two distinguishable commitment states or action-guiding alternatives are admissible, including the possibility of retaining versus revising a prior commitment.

The alternatives need not all be consciously or explicitly represented. They must differ in a way relevant to the declared stake.

### R3 — Ground sensitivity

There exist admissible variations `g` and `g'` in grounds or constraints such that, holding the declared comparison conditions fixed, the process's distribution over later commitment states, evaluations, or actions differs.

This is a difference-making requirement. Mere chronological succession is insufficient.

For stochastic or approximate processes, the difference may be distributional rather than deterministic.

### R4 — Directed evaluation or transformation

The process uses, combines, compares, filters, revises, propagates, weighs, or transforms grounds in a way directed toward resolving, managing, or acting relative to the stake.

Arbitrary state transitions, undirected noise, and purely coincidental correlations do not satisfy this condition.

### R5 — Commitment consequence

The episode produces, maintains, revises, rejects, ranks, suspends, or operationally deploys at least one commitment or action policy in a manner that can affect later behavior, inference, evaluation, communication, or inquiry.

A final output may count only when the declared claim is limited to observable input-output reasoning. It cannot support claims about hidden internal structure without additional evidence.

### R6 — Traceable justificatory dependence

There is a declared relation connecting at least some grounds, transformations, and commitment consequences such that the claimed dependence is:

- directly observed;
- instrumented;
- specified by the process implementation;
- formally proved;
- or explicitly classified as unresolved because available evidence is insufficient.

Invented hidden steps are prohibited. A reasoning classification stronger than the observation contract permits is invalid.

## Definition family by evidential strength

The mathematical definition is one target with three evidential grades, not three different ontologies.

### E0 — Behaviorally supported reasoning claim

R1–R5 are supported at input-output or reported-trace level, but R6 is not established beyond behavioral difference-making.

This permits a bounded claim that behavior is reasoning-compatible. It does not establish faithful internal process structure.

### E1 — Operationally grounded reasoning episode

R1–R6 are supported by an instrumented trace or independently specified operational model.

This supports claims about the captured operational episode within the instrumentation scope.

### E2 — Correspondence-grounded reasoning system

R1–R6 are supported by a white-box specification plus a formal or independently validated correspondence between the specification, trace, and relevant process properties.

This is the strongest current grade. It still does not establish universality or architectural minimality.

## Individuation and composition

### Episode boundaries

A reasoning episode begins at the earliest process location required to establish the relevant grounds or stake and ends when the scoped commitment consequence is produced, suspended, or abandoned.

Boundaries may overlap. One physical execution may contain multiple nested or interacting episodes.

### Agents are optional

The definition does not require a single reasoner. An episode may be distributed across people, tools, institutions, environments, or asynchronous components.

### Composition

A composite process counts as reasoning only when the combined process satisfies R1–R6. The fact that one component reasons does not automatically make every enclosing system a reasoner, and simple aggregation does not automatically create reasoning.

### External scaffolding

External memory, tools, documents, instruments, environmental structures, and other agents may be part of the process state when they are causally and operationally integrated into the episode. Merely being consulted after the fact is not enough.

## Boundary classifications

The definition yields the following prospective treatment.

### Reflexes and fixed stimulus-response loops

Normally fail R2 or R4 when there is no stake-relative alternative evaluation. They remain admissible as counterexamples where internal modulation or learning creates genuine alternative-sensitive commitment consequences.

### Simple feedback controllers

May satisfy R1–R5 under a very broad practical interpretation. They remain a boundary case because R4 and the nontriviality of the commitment space require independent justification. Mere error correction is not automatically reasoning.

### Lookup tables

Normally fail R4 when output selection is entirely extensional and no ground transformation or evaluation occurs in the executing system. A larger system that constructs, chooses, revises, or justifies use of the table may reason.

### Static classifiers

Normally fail R2, R4, or R5 when they only apply a fixed mapping. They may participate in a larger reasoning episode without independently constituting one.

### Optimization

Optimization counts only when the optimization process itself has stake-relative alternatives, ground sensitivity, directed evaluation, and commitment consequences. A final optimized artifact alone is insufficient.

### Evolutionary search

May satisfy the definition at the population-process level if selection, variation, and retained structures instantiate R1–R6 under a justified interpretation. Biological evolution is not automatically reasoning merely because it optimizes.

### Associative recall and perception

May supply grounds or commitments but do not independently count unless they satisfy the full conditions.

### Opaque systems

May receive E0 status when behavioral evidence supports R1–R5. They remain unresolved for internal-preservation claims until R6 is established at a stronger observability level.

### Operator-supplied reasoning

A system does not inherit reasoning status when all stake selection, ground transformation, and commitment evaluation are performed by an external operator and the system merely stores or transmits the result.

## Domain coverage obligations

The definition is prospectively applicable to all D1–D16 classes because it permits:

- formal and nonformal support relations;
- symbolic and subsymbolic state;
- deterministic and stochastic evolution;
- explicit and implicit commitments;
- fixed and changing goals;
- individual and distributed processes;
- passive inference and action-coupled inquiry;
- synchronous and asynchronous histories;
- static and self-modifying transition structures;
- internal, external, and environmental state;
- unresolved classification under limited observability.

Applicability is not evidence of adequacy. Every domain class must later receive positive, negative, and boundary cases under the frozen evaluation protocol.

## Clause-to-domain justification

| Clause | Primary motivation | Principal overbreadth risk | Principal underbreadth risk |
|---|---|---|---|
| R1 | D5, D6, D8, D13 | Any goal-directed control appears to reason | Open-ended inquiry with changing stakes is excluded |
| R2 | D1-D4, D7, D8, D15 | Latent alternatives are invented | Implicit or continuous alternatives are excluded |
| R3 | All classes | Correlation is mistaken for reason sensitivity | Stochastic and opaque systems cannot qualify |
| R4 | D1-D9, D13-D15 | Any computation becomes evaluation | Embodied or learned transformations are excluded |
| R5 | D3, D5, D8-D13 | Any output is called a commitment | Suspended, graded, or distributed commitments are excluded |
| R6 | D10-D16 and all preservation claims | Weak narratives are accepted as traces | Opaque systems are declared non-reasoning rather than unresolved |

## Countermodels and stress tests

The following countermodels are mandatory in later evaluation.

### C1 — Arbitrary labeled transition

A random state machine whose states are renamed “belief,” “evidence,” and “conclusion.” It must fail R3 or R4 despite terminology.

### C2 — Output-equivalent lookup

A lookup table reproduces the same answers as a reasoner on a finite benchmark. It must not inherit the internal reasoning classification without evidence of R4 and R6.

### C3 — Post hoc narrative

A system produces an answer and then generates a plausible explanation unrelated to production. The report may support E0 behavior but must fail stronger R6 claims.

### C4 — Hidden operator

A human performs all evaluation and enters the result into a passive program. The passive program must not be classified as the reasoning process.

### C5 — Pure optimizer

A black-box optimizer improves a scalar objective with no justified commitment interpretation. It remains boundary-unresolved rather than automatically admitted.

### C6 — Trivial universal encoding

Every physical process is encoded as a “reasoning episode” by treating successive states as commitments. It must fail R1, R2, R3, or R4 unless those relations are independently demonstrated.

### C7 — Distributed reasoning

No component individually satisfies all conditions, but the interaction network does. The definition must permit the composite episode when dependencies are evidenced.

### C8 — Self-revision

A process changes the standards by which later commitments are assessed. The definition must preserve the before/after distinction without assuming fixed rules.

### C9 — Continuous embodied control

A robot integrates continuous sensorimotor feedback while replanning. The definition must not require discrete symbolic propositions.

### C10 — Conflicting normative reasons

A legal or ethical process weighs incompatible standards without a unique deductive consequence. The definition must permit contested or defeasible support.

## Candidate-neutrality audit

For every core component and clause:

1. its motivation is traceable to the frozen domain rather than FARA;
2. it can be instantiated using state-transition, probabilistic, categorical, graph, dynamical, institutional, neural, or hybrid formalisms;
3. no clause requires Representation, Representational Structure, Interpretation, Investigation, or Calculus as primitives;
4. no clause requires FARO execution or FAR-IR encoding;
5. a candidate may challenge the decomposition while preserving the same observable commitments;
6. failure of this definition is a permitted result;
7. fragmentation into multiple non-equivalent reasoning classes is a permitted result;
8. no finite universal architecture is a permitted result.

## Failure and revision conditions

Version 1.0 must be revised or rejected if any of the following is established:

- the definition admits arbitrary physical dynamics without nontrivial additional commitments;
- one or more frozen target classes cannot instantiate the definition for reasons unrelated to observability;
- a core clause is shown to be candidate-specific;
- two systems with materially different justificatory dependence are forced into commitment-equivalent presentations;
- the evidential grades permit stronger internal claims than their observation contracts support;
- a clause is redundant under all admissible models;
- the definition cannot distinguish lookup, post hoc narrative, or hidden-operator controls from operational reasoning;
- the definition becomes universal only by making grounds, stakes, commitments, or support relations unconstrained labels.

A revision receives a new version and preserves this document and all results generated under it.

## Formal research obligations created by this definition

The next milestones must determine:

1. whether R1–R6 are jointly sufficient for the frozen domain;
2. whether each clause is independent or derivable;
3. whether additional preservation dimensions are required;
4. whether the definition fragments into multiple mathematical classes;
5. whether FARA faithfully represents the class without hidden reintroduction;
6. whether a simpler or different candidate performs equally or better;
7. whether finite universal representation is impossible under accepted commitments.

## Nonclaims

This definition does not establish:

- that every D1–D16 case is reasoning;
- that R1–R6 are final, necessary, independent, or minimal;
- that one universal reasoning class exists;
- that all reasoning is observable;
- that FARA represents this class;
- that FARA is universal, necessary, minimal, economical, or superior;
- that operational implementation constitutes independent replication.

## Immediate next milestone

Conduct the preservation-basis investigation against this definition and the frozen domain. Test whether the current preservation dimensions are sufficient, independent, redundant, or incomplete before attempting a final representation theorem.