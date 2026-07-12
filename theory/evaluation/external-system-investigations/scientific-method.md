# External System Investigation — Scientific Method

Status: provisional

## Purpose

Evaluate whether explicit scientific inquiry can be represented by FAR/FARA while preserving the distinction between empirical evidence, methodological procedure, and proof-like derivation.

## Independent System Description

Scientific inquiry formulates questions, constructs hypotheses or models, derives predictions, designs observations or experiments, collects evidence, analyzes results, and revises or rejects claims. Its primary objects include research questions, hypotheses, models, measurements, experimental designs, protocols, data, statistical analyses, background assumptions, predictions, and publication or replication records. Reasoning procedures include deduction from models to predictions, measurement, statistical inference, causal or mechanistic interpretation, error analysis, peer criticism, and revision in light of evidence.

The scope is explicit, documented scientific reasoning in which hypotheses, procedures, evidence, and inference standards are accessible. Tacit laboratory skill, institutional trust, and inaccessible proprietary data are included only when documented sufficiently for audit.

## Assumptions

- Scientific method is not a single algorithm; this investigation evaluates a family of documented inquiry practices.
- Empirical measurement and statistical analysis must be represented as evidence-producing and evidence-interpreting procedures, not as proof rules alone.
- Social review and replication are treated as methodological structures when they bear on claim acceptance.

## Source Evidence

- Standard source: Popper, *The Logic of Scientific Discovery*, for falsifiability and severe testing as methodological pressure.
- Standard source: Fisher, *The Design of Experiments*, for experiment design and statistical inference practice.
- Standard source: National Academies reports on reproducibility and replicability in science, for documentation and replication norms.
- Existing Project FAR contextual evidence: `theory/evaluation/external-systems/scientific-hypothesis-testing.md` and `theory/applications/empirical-inquiry.md`, used only after the independent description.

## Claim Separation

- Syntactic encoding: hypotheses, protocols, and data can be stored as documents.
- Representability: research questions, models, evidence, procedures, and revisions can be mapped to FAR/FARA roles.
- Faithful representation: the mapping preserves evidential relations, methodological constraints, and revision criteria for a stated inquiry.
- Operational equivalence: a documented inquiry trace corresponds to state transitions from question and hypothesis through evidence and resolution.
- Explanatory adequacy: the mapping explains explicit inquiry structure but not every sociological or tacit factor.
- Universality: not claimed.
- Necessity: limited to explicit scientific investigations.
- Minimality: not claimed.

## FAR/FARA Representation

| FAR/FARA Component | Target-System Mapping | Notes |
|---|---|---|
| Investigation | Scientific question or test of a hypothesis/model. | |
| Representation | Hypotheses, models, predictions, protocols, observations, data, analyses, reports. | |
| Representational Structure | Model-variable relations, experimental design, causal diagrams, data schemas, dependency between evidence and claims. | |
| Interpretation | Measurement semantics, statistical interpretation, operational definitions, error models, causal or mechanistic meaning. | |
| Reasoning Calculus | Experimental protocol, statistical test/model comparison, prediction derivation, revision/rejection rules, replication policy. | Domain-specific. |
| Reasoning State | Current hypothesis set, evidence state, analysis state, review/replication state. | |
| Transition Signature | Generate prediction, collect measurement, update evidence, run analysis, accept/reject/revise claim. | |
| Candidate | Candidate hypothesis, model, explanation, measurement, analysis, or replication result. | |
| Admissibility Structure (Ω) | Protocol constraints, inclusion/exclusion criteria, measurement validity, statistical assumptions, preregistration, peer-review checks. | |
| Resolution Rule | Accept provisionally, reject, revise, replicate, or mark unresolved. | |
| Resolution | Provisional conclusion with confidence, limitation, and replication status. | |

## Preservation Review

### Representation Fidelity

Target: hypotheses, evidence, methods, analysis, and revision history. Evidence: scientific-method and reproducibility sources. Preserving element: Representation and Reasoning State. Procedure: verify that evidence and method are recorded separately from conclusions. Result: `pass` for documented investigations; `unknown` for undocumented tacit practice. Justification: explicit reports can preserve the needed objects, but inaccessible practice cannot.

### Semantic Preservation

Target: operational definitions, measurement meaning, statistical interpretation, and claim scope. Evidence: experimental design and reproducibility sources. Preserving element: Interpretation. Procedure: compare target measurement and analysis semantics with mapped interpretation policy. Result: `pass` when protocols and measurement models are specified; `unknown` otherwise. Justification: semantics depend on domain-specific documentation.

### Structural Preservation

Target: relations among hypotheses, variables, interventions, measurements, data, assumptions, and conclusions. Evidence: design and analysis records. Preserving element: Representational Structure. Procedure: reconstruct the dependency chain from hypothesis to evidence to conclusion. Result: `pass` for sufficiently documented studies. Justification: study design and data schemas can be represented structurally.

### Operational Preservation

Target: actual inquiry procedure from design to evidence to analysis to revision. Evidence: protocols, analyses, and replication records. Preserving element: Reasoning Calculus and transition components. Procedure: trace an inquiry as ordered transitions and compare to recorded procedure. Result: `unknown` in the general case; `pass` only for fully documented individual studies. Justification: scientific method is not one universal algorithm, and many reports omit operational details.

### Dependency Preservation

Target: dependence on instruments, background theory, data processing, statistical assumptions, and replication. Evidence: reproducibility standards. Preserving element: Structure, Ω, and State. Procedure: list claim dependencies and check retrievability. Result: `unknown` in the general case. Justification: documentation quality varies materially.

### Information Preservation

Target: information required to reproduce or audit an inquiry. Evidence: reproducibility sources. Preserving element: all primitives plus evidence records. Procedure: determine whether data, code, protocol, materials, and assumptions are available. Result: `unknown` in the general case; `fail` for inaccessible data/procedure; `pass` for fully open and documented cases. Justification: scientific reasoning often depends on information not present in summary reports.

## Required FAR/FARA Components

Required: all five FAR primitives and FARA state-transition components. Ω and Resolution Rule are especially important because scientific conclusions are provisional and method-dependent.

## Unused FAR/FARA Components

None are categorically unused for explicit scientific inquiry.

## Alternative Representations Considered

- Treating science as Bayesian update only was rejected because it omits design, measurement, replication, and model construction.
- Treating science as falsification only was rejected because it omits estimation, confirmation, exploratory modeling, and revision.
- Treating publications as outputs only was rejected because it fails to represent reasoning process.

## Potential Counterexamples

- Tacit expert practice and undocumented laboratory decisions may be inaccessible.
- Exploratory research can revise hypotheses after observing data, creating post-hoc bias risk.
- Irreproducible or proprietary studies may not preserve information needed for audit.

## Counterexample Classification

- Tacit or inaccessible reasoning: `outside scope` where the reasoning process cannot be accessed.
- Exploratory post-hoc revision: `conservative extension pressure`; requires explicit revision/admissibility policy, not a new primitive.
- Irreproducible/proprietary studies: `unresolved` or `outside scope` depending on whether enough evidence remains to classify the reasoning.

## Classification

`unresolved`

## Justification

The explicit components of scientific inquiry appear representable, but the general family of scientific method cannot be classified as fitting FAR or conservative extension without selecting a documented inquiry subtype and evidence standard. Preservation of operational, dependency, and information dimensions is often unknown. Under the deterministic precedence rule, unresolved status outranks conservative extension when required evidence or criteria cannot be decided.

## Limitations

This report does not investigate a specific experiment, field science, simulation science, qualitative method, or causal-inference framework. It evaluates only the general methodology family.

## Implications

### Universality

Provides mixed evidence: explicit documented inquiry appears representable, while inaccessible or underdocumented inquiry remains unresolved or outside scope.

### Necessity

Suggests that state, admissibility, interpretation, and resolution policies are important for empirical reasoning, but does not generalize necessity.

### Minimality

Does not support minimality. Scientific inquiry may pressure additional derived concepts for evidence quality, replication, and revision, though no new primitive is identified.

## Confidence

Moderate for the unresolved classification; lower for any stronger classification because scientific practice is heterogeneous.

## Remaining Questions

- Should future investigations evaluate specific scientific subtypes separately, such as randomized controlled trials, mechanistic modeling, simulation science, and qualitative inference?
- What documentation threshold makes operational preservation pass rather than unknown?

## Methodology Feedback

No methodology defect was discovered. The methodology forced an unresolved classification rather than allowing the investigation to overclaim from partially explicit practices.
