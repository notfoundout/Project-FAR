# External System Investigation — Bayesian Reasoning

Status: provisional

## Purpose

Evaluate whether Bayesian reasoning can be represented by FAR/FARA without reducing probabilistic update to deductive proof or treating successful representation as universality or minimality evidence.

## Independent System Description

Bayesian reasoning represents uncertainty with probabilities over hypotheses, parameters, or models and updates those probabilities using evidence. Its primary objects include hypotheses, prior probability distributions, likelihood functions, evidence or observations, posterior distributions, conditional probabilities, models, and decision or comparison criteria. Bayes' rule relates posterior probability to prior probability and likelihood. In practical Bayesian inference, exact or approximate procedures compute, sample, or compare posterior quantities.

The scope is explicit Bayesian inference in which hypotheses, evidence, probabilities, and update rules are specified. Opaque learned heuristics that merely approximate Bayesian behavior without accessible probability model or update procedure are outside this scope.

## Assumptions

- Probability assignments are part of the target representation and interpretation, not optional annotations.
- Approximate inference can be evaluated operationally only when its approximation target and procedure are stated.
- The investigation does not evaluate whether Bayesian priors are epistemically justified.

## Source Evidence

- Primary historical evidence: Bayes and Price, "An Essay towards Solving a Problem in the Doctrine of Chances" (1763), for inverse probability motivation.
- Standard reference: Jaynes, *Probability Theory: The Logic of Science*, for probability as extended logic and Bayesian updating.
- Standard reference: Gelman et al., *Bayesian Data Analysis*, for modern model, prior, likelihood, posterior, and computation practices.
- Existing Project FAR contextual evidence: `theory/evaluation/external-systems/bayesian-inference.md`, used only after the independent description.

## Claim Separation

- Syntactic encoding: probability formulas and model definitions can be written in FAR/FARA artifacts.
- Representability: hypotheses, distributions, evidence, likelihoods, updates, and posterior results can be mapped to FAR/FARA roles.
- Faithful representation: probability semantics and update criteria are preserved for the scoped model.
- Operational equivalence: exact or approximate inference procedures produce corresponding posterior or decision outputs under stated conditions.
- Explanatory adequacy: the mapping explains probabilistic reasoning as structured uncertainty update, not as categorical proof.
- Universality: not claimed.
- Necessity: limited to this investigation.
- Minimality: not claimed.

## FAR/FARA Representation

| FAR/FARA Component | Target-System Mapping | Notes |
|---|---|---|
| Investigation | Determine how evidence changes support for hypotheses or model parameters. | |
| Representation | Hypotheses, variables, priors, likelihoods, observations, posteriors, models. | Quantitative values are required content. |
| Representational Structure | Conditional dependencies, model graph, parameter-observation relations, sample space. | |
| Interpretation | Probabilistic semantics of variables, events, parameters, and evidence. | Includes measure/normalization assumptions where needed. |
| Reasoning Calculus | Bayes' rule, conditioning, marginalization, model comparison, sampling or approximation algorithms. | |
| Reasoning State | Current prior/posterior state, observed evidence set, sampler state, or approximation state. | |
| Transition Signature | Condition on evidence, update posterior, marginalize, sample, compare models. | |
| Candidate | Candidate hypothesis, parameter value, posterior estimate, model, or sample. | |
| Admissibility Structure (Ω) | Probability axioms, normalization, model assumptions, convergence/diagnostic criteria. | |
| Resolution Rule | Accept posterior calculation, reject invalid update, report approximation uncertainty, choose model by criterion. | |
| Resolution | Posterior distribution, decision, comparison result, or unresolved inference. | |

## Preservation Review

### Representation Fidelity

Target: model, priors, likelihoods, evidence, posteriors, and computation method. Evidence: Bayesian references. Preserving element: Representation and Structure. Procedure: verify that quantitative probability content is mapped rather than replaced by labels. Result: `pass`. Justification: the mapping requires numeric/distributional content.

### Semantic Preservation

Target: probability semantics and conditionalization. Evidence: Bayes' rule and standard Bayesian model semantics. Preserving element: Interpretation. Procedure: correspondence between target probability model and FAR interpretation policy. Result: `pass`. Justification: probabilistic meaning is preserved as interpretation, not collapsed into truth values.

### Structural Preservation

Target: dependency relations among hypotheses, parameters, data, and conditional distributions. Evidence: model descriptions in Bayesian sources. Preserving element: Representational Structure. Procedure: reconstruct conditional-dependency graph or factorization from the mapping. Result: `pass`. Justification: dependency structure is explicit when the model is specified.

### Operational Preservation

Target: exact updating or declared approximate inference. Evidence: Bayesian update and computation procedures. Preserving element: Reasoning Calculus and FARA transition components. Procedure: compare target update equation or algorithmic trace with transition output. Result: `pass` for exact or fully specified approximate procedures; `unknown` for opaque approximation. Justification: the scoped system requires explicit procedures; opaque approximations are excluded or unresolved.

### Dependency Preservation

Target: dependence on priors, likelihoods, evidence, model assumptions, and approximation diagnostics. Evidence: Bayesian modeling practice. Preserving element: Structure, State, and Ω. Procedure: list all dependencies needed to reproduce a posterior. Result: `pass`. Justification: Bayesian conclusions are explicitly dependent on these inputs.

### Information Preservation

Target: information needed to recompute or audit the posterior. Evidence: source update rules and model descriptions. Preserving element: all five primitives plus state and resolution. Procedure: determine whether omission of priors, likelihoods, data, or algorithm would change the result. Result: `pass` when all are recorded; `fail` for reports omitting them. Justification: this report's mapping treats those items as mandatory.

## Required FAR/FARA Components

Required: all five FAR primitives and FARA state-transition components for update traces.

## Unused FAR/FARA Components

No component is unused for explicit Bayesian update. Resolution may be a distribution rather than a categorical truth judgment.

## Alternative Representations Considered

- Encoding Bayes' rule as a formula only was rejected because it loses model and evidence dependencies.
- Treating posterior probability as an interpretation-free score was rejected because it loses probability semantics.
- Representing Bayesian reasoning as deductive proof was rejected as explanatory distortion for uncertain inference.

## Potential Counterexamples

- Subjective prior choice may be underdetermined by evidence.
- Improper priors or non-identifiability can prevent a well-defined posterior.
- Black-box systems that claim Bayesian behavior without explicit model/update access cannot be faithfully investigated.

## Counterexample Classification

- Subjective prior choice: `conservative extension pressure`; it requires evidence-quality and prior-selection policy, not a new primitive.
- Improper priors/non-identifiability: `unresolved` when posterior existence cannot be established from available evidence.
- Black-box Bayesian claims: `outside scope` if the reasoning process is inaccessible.

## Classification

`conservative extension`

## Justification

Bayesian reasoning requires quantitative probability semantics, model assumptions, and sometimes approximation diagnostics. These are domain-specific interpretation, structure, calculus, and admissibility machinery over the existing primitives, not a candidate sixth primitive.

## Limitations

This investigation does not settle prior justification, convergence diagnostics, causal interpretation, or all approximate-inference validity questions.

## Implications

### Universality

Supports representability for an uncertain quantitative reasoning system when the model and update process are explicit. It does not prove universality.

### Necessity

Supports the need for interpretation, structure, and calculus in probabilistic reasoning. Necessity is not generalized beyond the scope.

### Minimality

Provides no direct minimality proof. Quantitative interpretation pressure could motivate future ablation tests of whether interpretation or calculus can be reduced without loss.

## Confidence

Moderate to high for explicit Bayesian models; lower for approximate or underspecified implementations.

## Remaining Questions

- Should prior-selection policy be a reusable derived concept?
- What minimum approximation diagnostics are required for operational preservation?
