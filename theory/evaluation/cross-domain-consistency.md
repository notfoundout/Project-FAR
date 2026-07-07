# Cross-Domain Consistency Audit

Status: Provisional v0.3.0 evaluation artifact.

## Purpose

This audit checks whether Project FAR's current reasoning-system classifications are internally consistent across similar domains. It does not change primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, or metadata schemas. It records whether the current v0.3.0 evidence classifies similar pressures similarly and identifies borderline cases for future falsification.

## Audit Method

The audit uses repository-grounded evidence from:

- `theory/evaluation/evidence-registry.yaml`;
- `theory/evaluation/expanded-fixture-analysis.md`;
- `theory/falsification/adversarial-analysis.md`;
- `theory/falsification/adversarial-test-suite.yaml`;
- `theory/falsification/primitive-pressure-registry.yaml`;
- fixture files in `examples/far/reasoning-systems/`.

The method is comparative rather than proof-theoretic:

1. group systems with similar primitive pressures;
2. compare recorded classifications, analysis statuses, and registry resolutions;
3. identify pressure points shared by systems in the group;
4. distinguish genuine inconsistency from different evidence status;
5. preserve unresolved or borderline cases instead of smoothing them away.

## Classification Consistency Rules

- Systems with explicit representations, structures, interpretations, and calculus rules may be classified as `fits FAR` when the current fixture and registry evidence indicate no domain-specific conservative extension is needed.
- Systems requiring domain-specific semantics, policies, admissibility standards, or structural constraints may be classified as `conservative extension` or `extends FAR` without implying a sixth primitive.
- Candidate counterexamples remain candidates until analysis classifies them as `real counterexample`, `conservative extension`, or `outside scope` under the falsification standard.
- Unanalyzed carried-forward fixtures remain unresolved even when they resemble analyzed systems.
- Opaque processes without inspectable explicit reasoning remain outside current FAR scope rather than primitive failures.

## Comparison Across Reasoning Systems

### Modal, Temporal, Dynamic, and Hybrid Logic

Modal and temporal logic are consistently treated as conservative extensions because their pressure comes from indexed interpretation plus accessibility, ordering, or path structure. Dynamic logic and hybrid logic appear in the adversarial suite and receive conservative-extension treatment for program-transition semantics and index-management policy. The classification pattern is consistent: additional semantics and index or transition discipline are treated as conservative extensions, not primitive additions.

### SAT Solving and Theorem Provers

SAT solving and theorem provers are both analyzed as `fits FAR`. Both provide explicit machine-checkable artifacts: formulas, assignments, proof states, kernels, certificates, and calculus-governed steps. Their similar classification is consistent because neither current analysis requires an extra semantic policy beyond explicit representation, structure, interpretation, and calculus.

### Type Theory and Intuitionistic Logic

Type theory and intuitionistic logic are both classified as conservative extensions in the evidence registry. The shared pressure is proof or judgment admissibility: constructive proof standards, typing contexts, judgments, and derivations require specialized calculus discipline but do not currently require a new primitive. This is internally consistent.

### Paradox, Self-Reference, Reflective Reasoning, and Meta-Reasoning

Paradoxical reasoning is a candidate counterexample resolved as a conservative extension. Self-reference remains an unresolved carried-forward reasoning-system fixture. Reflective reasoning and meta-reasoning are adversarial conservative extensions because they require policies preventing level or interpretation collapse. The borderline result is self-reference: it resembles the analyzed reflection/paradox cluster but remains unresolved because its carried-forward registry entry lacks targeted v0.3.0 analysis.

### Fuzzy Logic, Bayesian Reasoning, and Probabilistic Programming

Fuzzy logic is an analyzed conservative extension because degree-valued truth requires interpretation and calculus policies. Probabilistic programming is an adversarial conservative extension because stochastic traces and conditioning rules require domain-specific structures and policies. Bayesian reasoning remains `fits FAR` at fixture-classification level but unresolved in the evidence registry because probabilistic update sufficiency has not been targeted. This is a documented borderline classification rather than a hidden inconsistency: similar probabilistic pressures are not yet analyzed at the same depth.

### Legal, Deontic, and Normative Reasoning

Deontic logic is an analyzed conservative extension because obligation, permission, and conflict handling require normative interpretation and conflict calculus. Legal reasoning remains `extends FAR` and unresolved because authority and precedent handling have not received targeted v0.3.0 sufficiency analysis. These are consistent at the pressure level: normative systems are not recorded as requiring a sixth primitive, but the broader legal fixture remains unresolved.

## Recurring Pressure Points

- Indexed contexts, worlds, times, and named states.
- Domain-specific interpretation policies for truth, obligation, probability, construction, or satisfaction.
- Specialized calculus policies for revision, conflict, transition, proof construction, typing, learning, and self-modification.
- Boundary and provenance discipline for multi-agent or interactive reasoning.
- Object/meta-level discipline for reflection, self-reference, and meta-reasoning.
- Opaque reasoning processes that cannot yet count as explicit FAR evidence.

## Inconsistent or Borderline Classifications

No direct contradiction is established by this audit. The strongest borderline cases are:

- Bayesian reasoning versus fuzzy logic and probabilistic programming: related uncertainty-oriented systems have different current statuses because Bayesian reasoning is a carried-forward fixture without targeted v0.3.0 sufficiency analysis.
- Self-reference versus paradox, reflective reasoning, and meta-reasoning: related self-referential systems are not all analyzed at the same depth.
- Legal reasoning versus deontic logic: deontic logic has targeted analysis, while legal reasoning remains unresolved because it includes authority and precedent pressures beyond basic normative modalities.
- Scientific, abductive, analogical, non-monotonic, and infinite reasoning remain carried-forward unresolved cases and should not be over-aligned with analyzed neighboring systems.

## Current Conclusion

The current classifications are broadly consistent across analyzed domains. Similar analyzed pressures are classified similarly: indexed semantics and transition policies are conservative extensions; explicit proof and SAT artifacts fit FAR; opaque oracle reasoning is outside current scope. Remaining differences are primarily differences in analysis depth, not established contradictions. The audit therefore supports v0.3.0 release readiness as a provisional internal evaluation baseline, while preserving unresolved and borderline cases for future falsification.
