# External System Investigation — Analogical Reasoning

Status: provisional

## Purpose

Evaluate analogical reasoning because it relies on cross-domain structural mapping and similarity judgments, making it a strong candidate for ambiguity, information-loss, and underdetermination.

## Independent System Description

Analogical reasoning draws inferences about a target domain from similarities or structural correspondences with a source domain. The process may identify objects, relations, higher-order relations, constraints, candidate mappings, transferred inferences, and evaluation criteria for systematicity or relevance. Psychological and AI accounts often emphasize structure mapping, candidate correspondences, mapping constraints, and inference projection, but real analogies can be partial, defeasible, context-sensitive, and creative.

The scope is explicit analogical reasoning where source domain, target domain, proposed correspondences, mapping constraints, and projected inference are documented.

## Assumptions

- The investigation concerns explicit analogies with recorded source/target representations, not unconscious similarity effects.
- Similarity metrics and relevance criteria must be specified or classified as unknown.
- Creative generation of candidate analogies is distinguished from evaluation of a documented analogy.

## Source Evidence

- Primary theory source: Gentner, "Structure-Mapping: A Theoretical Framework for Analogy" (1983), describing source-target correspondences and systematicity.
- Implementation/source: Falkenhainer, Forbus, and Gentner, "The Structure-Mapping Engine" (1989), describing computational mapping operations.
- Cognitive source: Holyoak and Thagard, *Mental Leaps* (1995), for constraint-based analogical reasoning.
- Concrete future-case evidence: source domain description, target domain description, mapping table, projected inference, and evaluation criterion.

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
| Investigation | Question asking whether and what can be inferred from a source-target analogy. |  |
| Representation | Source objects/relations, target objects/relations, correspondences, candidate mappings, projected inference. |  |
| Representational Structure | Source-target mapping graph, relational structure, higher-order constraints, similarity/relevance dependencies. |  |
| Interpretation | Meanings of source/target relations, analogy relevance, systematicity or constraint semantics. |  |
| Reasoning Calculus | Mapping generation/evaluation, constraint satisfaction, inference projection, rejection or acceptance rules. |  |
| Reasoning State | Current candidate mapping set, unmatched elements, constraint scores, projected conclusions. |  |
| Transition Signature | Add correspondence, check consistency, project inference, evaluate relevance, reject mapping. |  |
| Candidate | Candidate correspondence, mapping, projected inference, or analogy. |  |
| Admissibility Structure (Ω) | One-to-one constraints, structural consistency, semantic similarity, pragmatic relevance, domain admissibility. |  |
| Resolution Rule | Accept best/adequate mapping, reject analogy, mark unresolved, or project qualified inference. |  |
| Resolution | Accepted/rejected mapping, projected inference, confidence, or unresolved result. |  |

## Preservation Review

### Representation Fidelity

Target: source, target, correspondences, constraints, and projected inference. Evidence: structure-mapping and concrete analogy evidence. Preserving element: Representation. Procedure: verify all analogy artifacts are explicit before mapping. Result: `pass`. Justification: documented analogies map as explicit artifacts

### Semantic Preservation

Target: relation meanings, similarity, relevance, systematicity criteria. Evidence: theory sources and case-specific criteria. Preserving element: Interpretation. Procedure: check whether each mapping criterion has an explicit semantic/pragmatic source. Result: `unknown`. Justification: formal criteria can pass, but many real analogies rely on underspecified relevance judgments

### Structural Preservation

Target: relational and higher-order structure across source and target. Evidence: Gentner/SME descriptions. Preserving element: Representational Structure. Procedure: reconstruct mapping graph and consistency constraints. Result: `pass`. Justification: structure mapping is naturally graph/constraint structured

### Operational Preservation

Target: candidate generation, mapping evaluation, inference projection. Evidence: SME or explicit analogy protocol. Preserving element: Reasoning Calculus and Transition Signature. Procedure: trace mapping operations or constraint satisfaction steps. Result: `unknown`. Justification: evaluation can pass for SME-like algorithms but human creative analogy generation may lack explicit calculus

### Dependency Preservation

Target: source/target domain assumptions, selected features, constraints, context. Evidence: case record and theory sources. Preserving element: Representational Structure. Procedure: audit whether omitted features could alter mapping. Result: `unknown`. Justification: information selection is central and may be underdocumented

### Information Preservation

Target: information needed to reproduce mapping and assess projected inference. Evidence: domain descriptions, mapping table, criteria. Preserving element: all components. Procedure: attempt independent reconstruction of analogy result. Result: `unknown`. Justification: partial analogies intentionally omit information, and relevance of omissions may be unclear

## Required FAR/FARA Components

Required: all FAR primitives and FARA components for explicit analogy evaluation. Conservative extensions are needed for cross-domain mapping constraints, similarity/relevance metrics, systematicity preferences, and qualified inference projection.

## Unused FAR/FARA Components

No FAR primitive is unused. Generation of novel analogies may leave exact transition signatures unknown if not algorithmically specified.

## Alternative Representations Considered

- Treating analogy as simple predicate matching was rejected because it loses relational/higher-order structure.
- Treating every syntactic correspondence as valid was rejected because it ignores semantic and pragmatic constraints.
- Treating creative analogy generation as fully represented by the accepted mapping was rejected because it confuses outcome with process.

## Potential Counterexamples

- Relevance and similarity criteria may be underspecified or context-dependent.
- Multiple incompatible mappings may satisfy different constraints.
- Creative analogy generation may not have an accessible transition rule.
- Information omitted from the source or target may be decisive for whether the analogy is misleading.

## Counterexample Classification

- Underspecified relevance: `unresolved`; lower-precedence plausible category `conservative extension pressure`.
- Multiple incompatible mappings: `conservative extension pressure` when scoring/admissibility rules exist, otherwise `unresolved`.
- Inaccessible creative generation: `outside scope` for hidden process; explicit accepted mapping remains evaluable.
- Misleading omitted information: `unresolved` unless evidence shows missing information cannot be represented by existing components.

## Classification

`unresolved`

## Justification

Explicit structure-mapping cases are representable, but broad analogical reasoning remains unresolved because semantic relevance, feature selection, and creative candidate generation often lack objective preservation criteria. The pressure does not satisfy candidate primitive failure because source-target mappings, constraints, and projections are expressible through existing primitives plus conservative domain machinery.

## Limitations

Does not evaluate all metaphor, creativity, unconscious priming, or aesthetic similarity. Formal SME-like analogies may deserve separate conservative-extension classification.

## Methodology Feedback

No methodology defect was discovered. The methodology forced explicit unknown/outside-scope handling rather than rescue reinterpretation.

## Implications

### Universality

Provides mixed evidence: explicit analogical mappings support representability, while underdetermined relevance and creative generation weaken claims that all analogical reasoning is faithfully preservable from available evidence.

### Necessity

Supports the need for representational structure and interpretation as separate components because syntax-only matching fails.

### Minimality

No minimality conclusion; analogy is a promising future ablation target for testing whether structure, interpretation, and calculus can be reduced without loss.

## Confidence

Moderate. The unresolved classification is appropriate for broad analogical reasoning; specific computational analogizers could be classified more strongly.

## Remaining Questions

- What objective relevance criteria are sufficient for faithful analogical preservation?
- Should explicit SME-style analogy be split into a separate conservative-extension investigation?
- How can creative generation be evaluated without access to hidden cognitive processes?
