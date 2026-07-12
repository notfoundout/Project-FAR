# External System Investigation — Human Expert Reasoning

Status: provisional

## Purpose

Evaluate human expert reasoning because expert judgment often depends on tacit knowledge, perception, experience, and nonverbal pattern recognition that may expose representational limits.

## Independent System Description

Human expert reasoning is skilled judgment and problem solving by people with domain-specific training and experience. It may involve explicit rules, case comparison, pattern recognition, perceptual discrimination, mental simulation, heuristics, and tacit knowledge. Research on expertise emphasizes differences between novice and expert representations, chunking, rapid recognition in familiar situations, and context-sensitive decision making; some processes are reportable, while others are inferred from performance, protocols, or experimental data.

The scope is documented expert reasoning episodes with task, evidence, elicited rationale or protocol, domain standards, and outcome criteria. Unreported neural or experiential processes are not assumed accessible.

## Assumptions

- Verbal reports and explanations are evidence about accessible reasoning but may be incomplete.
- Domain standards can define correctness for some expert tasks, but not all expert judgments have objective ground truth.
- Tacit knowledge pressure must be recorded as unknown or outside scope rather than translated into explicit FAR terms by stipulation.

## Source Evidence

- Primary/empirical source: Chase and Simon, "Perception in Chess" (1973), describing expert chunking and memory effects in chess expertise.
- Primary/empirical source: Ericsson and Simon, *Protocol Analysis* / related verbal-report methodology, for evidence limits of think-aloud protocols.
- Research source: Klein, *Sources of Power* (1998), on recognition-primed decision making in naturalistic expertise.
- Domain-specific primary evidence for concrete future cases: task materials, expert protocol transcript, domain standard, outcome record, and date/version.

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
| Investigation | Expert task or judgment objective. |  |
| Representation | Task materials, observations, cues, hypotheses, rules of thumb, verbal protocol, decision, outcome. |  |
| Representational Structure | Cue-feature relations, domain categories, case analogies, temporal context, evidential dependencies. |  |
| Interpretation | Domain meanings, success standards, expert terminology, cue interpretation. |  |
| Reasoning Calculus | Elicited procedure: rule application, pattern recognition account, case comparison, simulation, or decision heuristic. |  |
| Reasoning State | Current perceived situation, candidate diagnoses/actions, recalled cases, confidence state. |  |
| Transition Signature | Attend to cue, form hypothesis, compare case, simulate action, update confidence, decide. |  |
| Candidate | Candidate diagnosis, move, explanation, action, or recommendation. |  |
| Admissibility Structure (Ω) | Domain constraints, admissible evidence, professional norms, task instructions. |  |
| Resolution Rule | Choose decision under domain or experimental criterion. |  |
| Resolution | Decision, explanation, score, expert/novice comparison, or unresolved judgment. |  |

## Preservation Review

### Representation Fidelity

Target: documented task, cues, explanation, decision, and outcome criteria. Evidence: expertise studies and concrete protocols. Preserving element: Representation. Procedure: compare protocol artifacts with mapped roles. Result: `unknown`. Justification: explicit artifacts preserve, but tacit perceptual and experiential content may be missing

### Semantic Preservation

Target: domain meanings and correctness standards. Evidence: domain standards, task instructions, experimental design. Preserving element: Interpretation. Procedure: check whether each cue/judgment has an explicit interpretation source. Result: `unknown`. Justification: some meanings are explicit; tacit cue salience may not be semantically recoverable

### Structural Preservation

Target: cue relations, case structure, memory chunks, decision dependencies. Evidence: protocols and empirical designs. Preserving element: Representational Structure. Procedure: build cue-decision dependency graph from available evidence. Result: `unknown`. Justification: reported dependencies can be mapped but latent chunks may be inferred only indirectly

### Operational Preservation

Target: expert procedure from cue perception to decision. Evidence: think-aloud/protocol or process-tracing evidence. Preserving element: Reasoning Calculus and Transition Signature. Procedure: attempt step reconstruction and mark gaps. Result: `unknown`. Justification: rapid recognition and tacit processes often lack accessible transition rules

### Dependency Preservation

Target: training history, task context, domain materials, protocols, outcome standards. Evidence: study records or case files. Preserving element: Representational Structure. Procedure: audit listed dependencies for replay. Result: `unknown`. Justification: long-term experiential dependencies are usually unrecoverable

### Information Preservation

Target: information needed to reproduce or audit the expert judgment. Evidence: protocol transcript, stimuli, standards, outcome. Preserving element: all components. Procedure: ask if another investigator can reconstruct the episode without the expert. Result: `unknown`. Justification: visible evidence may be sufficient for outcome audit but insufficient for full process preservation

## Required FAR/FARA Components

Required: all five FAR primitives for documented expert tasks; FARA components for process-trace investigations. Conservative extensions are needed for protocol-evidence quality, tacit-knowledge markers, perceptual cue representation, and domain-standard metadata.

## Unused FAR/FARA Components

No FAR primitive is unused for documented episodes. FARA transition components may be unused only when the report is limited to static judgment classification, but this investigation targets process preservation.

## Alternative Representations Considered

- Treating the expert decision alone as the reasoning representation was rejected because it loses process, dependency, and tacit-knowledge limits.
- Treating retrospective explanation as complete process was rejected due to verbal-report limits.
- Neurobiological representation was rejected as outside this investigation unless direct evidence is included.

## Potential Counterexamples

- Tacit pattern recognition may be inaccessible while still causally central.
- Experts may provide rationalizations rather than process-accurate explanations.
- Domain correctness may be contested or delayed.
- Training history and experience are too large to preserve completely.

## Counterexample Classification

- Tacit causal process: `outside scope` for inaccessible internal details; lower-precedence plausible category `unresolved` for documented behavioral evidence.
- Retrospective rationalization: `unresolved` because process fidelity cannot be established from explanation alone.
- Contested domain standards: `unresolved`.
- Large training history: `conservative extension pressure` for provenance summarization when not required for the scoped decision.

## Classification

`unresolved`

## Justification

Human expert reasoning is partially representable when tasks, cues, protocols, and standards are documented, but faithful operational and information preservation often remains unknown because tacit and perceptual processes are inaccessible. This is not yet a primitive failure because inaccessible or underdocumented process evidence triggers outside-scope/unresolved classifications under the methodology.

## Limitations

Does not evaluate all human cognition, consciousness, affect, motor control, or neural implementation. Expert domains differ substantially, and each concrete domain requires its own evidence standards.

## Methodology Feedback

No methodology defect was discovered. The methodology forced explicit unknown/outside-scope handling rather than rescue reinterpretation.

## Implications

### Universality

Provides significant pressure against overclaiming universality because important human reasoning episodes may not be fully accessible. It does not refute FAR/FARA for explicit documented reasoning.

### Necessity

Supports the need to separate representation, interpretation, calculus, and information preservation; explanation alone is insufficient.

### Minimality

No support for minimality. Tacit cognition may motivate future tests of whether FAR is a theory of explicit reasoning only or can address inaccessible processes via scoped evidence.

## Confidence

Moderate; evidence strongly supports unresolved preservation for tacit expertise, but concrete protocol-rich cases may be more classifiable.

## Remaining Questions

- Can process-tracing methods produce enough evidence for faithful operational preservation?
- What counts as an explicit reasoning process for tacit expert judgment?
- Are there expert domains with stable enough standards for stronger classification?
