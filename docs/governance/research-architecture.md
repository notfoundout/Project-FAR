# Project FAR Research Architecture

## Status

Canonical governance for new research and planning artifacts. Historical and frozen artifacts retain their original terminology and evidential meaning.

## Governing principle

Project FAR is committed to discovering the strongest justified structure of reasoning, not preserving any particular candidate architecture. Every candidate, including FARA, is subject to the same formal tests, counterexample searches, cost accounting, revision controls, and replacement criteria.

## Project FAR

Project FAR is the architecture-neutral research program asking whether any common structure underlies reasoning and, if so, whether that structure is universal and minimal. Project FAR is not itself a candidate architecture and does not presuppose that a universal finite architecture exists.

## Reasoning-domain specification

A reasoning-domain specification defines the class of processes under investigation independently of any candidate architecture. It states observables, admissible transformations, relevant commitments, scope, and exclusion criteria without requiring FARA-native primitives.

The prospective target domain is frozen in `docs/research/reasoning-domain-specification-v1.0.md` and registered in `theory/evaluation/reasoning-domain-registry.json`. This artifact fixes the classes and boundary cases that the next mathematical-definition milestone must address. It is not itself a mathematical definition of reasoning.

## Candidate architecture

A candidate architecture is a versioned proposal concerning the primitive commitments, relations, admissibility rules, or transformation principles required to preserve reasoning structure. A candidate is an object of evaluation, not a protected conclusion.

## FARA

FARA is the current principal candidate architecture derived from the accepted Foundation and theory artifacts in `frameworks/FARA/`, the canonical definitions, and their registered mechanizations. Existing mathematical content is unchanged by this governance distinction.

FARA currently has bounded supporting evidence. Universality, necessity, minimality, comparative economy, and general independent replication remain unestablished.

## FARO

FARO is the operational layer represented by the existing `frameworks/FARO/` artifacts and associated executable machinery. It may encode, lower, execute, verify, compare, replay, or otherwise operationalize candidate representations at declared scopes.

FARO output is evidence only for the contracts actually executed. FARO does not independently establish that FARA is universal, necessary, minimal, or uniquely correct.

## Evaluation system

The evaluation system consists of external observation contracts, preservation commitments, negative controls, anti-reintroduction rules, cost accounting, comparison rules, evaluator controls, evidence standards, and research gates. Candidate-specific success rules are prohibited.

## Discovery system

The discovery system is the planned candidate-neutral machinery for generating or enumerating source systems, candidates, mappings, ablations, counterexamples, dominance relations, equivalence conjectures, and theorem targets. It is not implemented by this reset.

## Mechanization

Mechanization is a formal or executable implementation of a theory, candidate, mapping, evaluator, compiler, verifier, proof, or experiment. Mechanization establishes only the propositions supported by its explicit assumptions, contracts, and proofs.

## Evidence record

An evidence record is an immutable or append-only result that supports, weakens, bounds, rejects, or leaves unresolved one or more registered claims. Failures and unresolved outcomes are evidence records and may not be deleted merely because they are unfavorable.

## Terminology distinctions

- **Project**: the complete research undertaking and repository.
- **Research program**: the governed investigation of the central question.
- **Candidate architecture**: a proposed common structure under evaluation.
- **Candidate vocabulary**: the explicit primitive and derived terms used by a candidate.
- **Formal theory**: axioms, definitions, propositions, and proofs concerning a candidate or domain.
- **Implementation**: executable or mechanized realization of a specification.
- **Evaluator**: a person or system producing judgments under a frozen protocol.
- **Experiment**: a preregistered procedure generating evidence records.
- **Claim**: a proposition tracked by the central claim registry.
- **Result**: the recorded output of a proof, computation, evaluation, or experiment.
- **Scope**: the independently stated domain in which a claim is asserted.
- **Preservation commitment**: an observable distinction or constraint that a faithful representation must retain.

## Backward compatibility

Older repository artifacts may use “FAR” to refer contextually to the project, the existing candidate architecture, its vocabulary, or associated machinery. New central governance, registry, and roadmap artifacts must distinguish Project FAR, FARA, FARO, and candidate architectures explicitly. Historical wording must not be rewritten in a way that alters the original result or claim boundary.

## Outcome space

The research program can legitimately conclude that:

1. a universal finite architecture exists and FARA is justified within the proven scope;
2. a universal finite architecture exists but another candidate replaces FARA;
3. multiple adequate architectures form an unresolved or formally established equivalence class;
4. no finite universal architecture exists under the accepted definition and assumptions;
5. only bounded architectures exist for restricted reasoning classes; or
6. current evidence remains insufficient.

Failure of FARA does not by itself establish that no universal architecture exists. Conversely, failure to find a counterexample does not establish universality.
