# External System Investigation — Legal Reasoning

Status: provisional

## Purpose

Evaluate legal reasoning because it combines rule interpretation, precedent, factual classification, defeasible argument, institutional authority, and contested norms.

## Independent System Description

Legal reasoning applies legal sources to facts to justify decisions, arguments, or advice. Common objects include statutes, regulations, constitutional provisions, cases, holdings, dicta, facts, issues, rules, standards, burdens of proof, remedies, and precedential relationships. Procedures include rule application, analogical reasoning from precedent, distinguishing cases, statutory interpretation, weighing factors, resolving conflicts of authority, and applying standards of review. Legal validity depends on jurisdiction, institutional hierarchy, procedural posture, and accepted interpretive canons.

The scope is documented common-law/statutory legal analysis in a specified jurisdiction with cited authorities, facts, issue, and decision standard. It does not assume one globally uniform legal calculus.

## Assumptions

- Jurisdiction and time are necessary because legal authority and interpretation change.
- Legal reasoning can be represented only relative to cited authorities and procedural posture.
- Normative disagreement is not treated as a FAR failure unless it blocks explicit representation of the legal reasoning process.

## Source Evidence

- Primary legal evidence for concrete cases: statutes/regulations/cases from official reporters or jurisdictional sources with citation, court, date, and relevant passages.
- Methodological source: legal doctrine of precedent/stare decisis as expressed in jurisdictional court practice and legal methods texts.
- Research source: Ashley, *Artificial Intelligence and Legal Analytics* (2017), for computational descriptions of case-based and analogical legal reasoning.
- Argumentation background: Dung, "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning" (1995), for abstract attack/acceptability structures relevant to defeasible legal arguments.

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
| Investigation | Legal question, issue, or dispute to resolve. |  |
| Representation | Facts, claims, legal authorities, rules, precedents, arguments, burdens, conclusions. |  |
| Representational Structure | Authority hierarchy, precedent relations, fact-rule mappings, argument attack/support graph, temporal/jurisdictional scope. |  |
| Interpretation | Legal meanings, holdings, statutory interpretation, jurisdictional validity, burden and standard semantics. |  |
| Reasoning Calculus | Rule application, analogical comparison, distinguishing, balancing tests, conflict resolution, defeasible argument evaluation. |  |
| Reasoning State | Current issue posture, authority set, fact findings, candidate arguments, procedural status. |  |
| Transition Signature | Cite authority, classify fact, apply rule, compare precedent, distinguish, weigh factor, resolve conflict. |  |
| Candidate | Candidate holding, argument, interpretation, precedent analogy, outcome. |  |
| Admissibility Structure (Ω) | Jurisdiction, hierarchy, admissible sources, procedural posture, evidentiary standard, precedent rules. |  |
| Resolution Rule | Select legally justified conclusion under authority and standard of review. |  |
| Resolution | Judgment, legal advice, argument set, or unresolved conflict. |  |

## Preservation Review

### Representation Fidelity

Target: facts, authorities, issue, arguments, and conclusion. Evidence: official legal sources and case file. Preserving element: Representation. Procedure: verify each legal artifact has citation and mapped role. Result: `pass`. Justification: for documented legal analysis, artifacts are explicit and citable

### Semantic Preservation

Target: legal meanings, authority, jurisdiction, standards, and interpretive policies. Evidence: official sources and legal methods evidence. Preserving element: Interpretation. Procedure: check interpretation against cited authority rather than evaluator preference. Result: `unknown`. Justification: semantics are preservable when sources are explicit, but contested interpretive theories may remain unresolved

### Structural Preservation

Target: precedent hierarchy, factual analogies, issue-rule-application structure, attack/support relations. Evidence: case citations and legal argument record. Preserving element: Representational Structure. Procedure: reconstruct authority and argument graph. Result: `pass`. Justification: legal reasoning is highly structured when citations and posture are recorded

### Operational Preservation

Target: application, analogy, distinguishing, balancing, and conflict resolution. Evidence: judicial opinions and legal method sources. Preserving element: Reasoning Calculus and Transition Signature. Procedure: trace each inference step to an authority/canon/standard. Result: `unknown`. Justification: some standards are discretionary or underdetermined, so exact operational equivalence may fail

### Dependency Preservation

Target: source authority, jurisdiction, dates, procedural posture, evidentiary record. Evidence: official citations and docket/case materials. Preserving element: Representational Structure. Procedure: audit whether all dependencies are cited with dates and hierarchy. Result: `pass`. Justification: dependency preservation is strong when legal citation practice is followed

### Information Preservation

Target: information needed to reproduce the analysis at the same legal date. Evidence: facts, authorities, dates, quoted passages, procedural posture. Preserving element: all components. Procedure: attempt re-analysis from cited record. Result: `unknown`. Justification: information can be sufficient for doctrinal reconstruction, but discretionary judgment and omitted record facts can remain underdetermined

## Required FAR/FARA Components

Required: all FAR primitives and FARA components for procedural legal analysis. Conservative extensions are needed for jurisdiction/time indexing, authority hierarchy, defeasible argument status, burdens of proof, and standards of review.

## Unused FAR/FARA Components

No FAR primitive is unused. Some FARA components may be implicit in written opinions but are required for replaying the reasoning.

## Alternative Representations Considered

- Pure rule-deduction mapping was rejected because legal reasoning uses precedent, interpretation, defeasibility, and institutional authority.
- Pure argument-graph mapping was rejected because it can omit legal source hierarchy and procedural posture.
- Outcome-only mapping was rejected as encoding rather than reasoning preservation.

## Potential Counterexamples

- Hard cases may have multiple legally plausible outcomes under the same sources.
- Open-textured standards may resist deterministic operational equivalence.
- Changing law makes conclusions time-indexed.
- Moral or policy reasoning embedded in legal interpretation may introduce contested semantics.

## Counterexample Classification

- Multiple plausible outcomes: `conservative extension pressure`; lower-precedence plausible category `unresolved` when criteria are underspecified.
- Open-textured standards: `conservative extension pressure` if represented as discretionary interpretive policy; `unresolved` if no source controls the discretion.
- Changing law: `not a counterexample` if time-indexed; it is dependency pressure.
- Moral-policy embedded reasoning: `unresolved` when legal sources do not specify interpretation criteria.

## Classification

`conservative extension`

## Justification

Legal reasoning is explicitly representable but requires domain-specific machinery for jurisdiction, authority hierarchy, defeasible conflict, standards, and time-indexed sources. No sixth primitive is indicated because these pressures extend structure, interpretation, calculus, admissibility, and resolution rules.

## Limitations

Scope excludes undocumented jury deliberations, purely political decision making, and nonlegal moral justification except where legal sources incorporate it. Classification may vary by legal tradition and jurisdiction.

## Methodology Feedback

No methodology defect was discovered. The methodology forced explicit unknown/outside-scope handling rather than rescue reinterpretation.

## Implications

### Universality

Supports representability for a complex normative-institutional explicit reasoning system, but only as a conservative extension and only when legal sources are documented.

### Necessity

Strongly supports distinct structure, interpretation, calculus, admissibility, and dependency tracking for this domain.

### Minimality

Does not support minimality. Legal reasoning creates pressure for derived concepts but not for primitive reduction or proof of minimality.

## Confidence

Moderate to high for the conservative-extension classification for documented legal analysis; lower for broad legal practice as a whole.

## Remaining Questions

- Which legal subdomains have sufficiently deterministic standards for operational equivalence?
- Should authority hierarchy and defeasible precedent be reusable derived concepts?
- How should discretionary judicial balancing be preserved without pretending determinism?
