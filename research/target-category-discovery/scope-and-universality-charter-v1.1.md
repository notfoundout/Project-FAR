# Scope and Universality Charter v1.1

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Version: 1.1  
Supersedes within this directory: generated Charter v1.0

## 1. Authority and subordination

This Charter governs only the Research subprogram in this directory. It is not canonical repository governance and does not alter accepted theory.

The controlling authorities remain:

- [`../../docs/governance/research-execution-charter.md`](../../docs/governance/research-execution-charter.md)
- [`../../docs/governance/central-research-program.md`](../../docs/governance/central-research-program.md)
- [`../../docs/governance/anti-self-validation-standard.md`](../../docs/governance/anti-self-validation-standard.md)
- [`../../theory/evaluation/research-gates.json`](../../theory/evaluation/research-gates.json)

Where this Charter conflicts with those artifacts, this Charter fails and must be revised.

## 2. Purpose

The program investigates whether a neutral requirement basis can be derived for a bounded class of explicitly auditable reasoning artifacts and whether RCCD or another architecture is sufficient, necessary, economical, or Pareto-optimal within that class.

It does not test unrestricted metaphysical universality.

## 3. Stable formal boundary

This subprogram may rely on the following narrow results.

### 3.1 Domain declaration

A universal statement must declare the domain over which its quantifier ranges. Changing that domain changes the proposition.

### 3.2 Semantic descent

For a declared semantics map `B : Rep -> Sem`, a representation-level property is semantic only if it is constant on the fibers of `B`, equivalently if it factors through `B`.

This condition validates claims relative to `B`; it does not select `B`.

### 3.3 Bare-carrier projection barrier

On `Set` with all functions, every natural positive-finitary element-valued operation is a coordinate projection, and there is no natural nullary global element.

This excludes bare carriers with unrestricted recodings as a source of nontrivial element-valued operations. It does not exclude nontrivial structure in richer independently justified categories.

## 4. Open theoretical questions

The following remain open in this subprogram:

- whether a broader independently justified structured class supports a common nontrivial invariant;
- whether the explicitly auditable-artifact class is itself independently optimal;
- whether one stable requirement basis exists across the selected cases;
- whether RCCD is necessary, minimal, unique, or Pareto-optimal within the bounded class;
- whether several incomparable bases remain after full-cost accounting;
- whether held-out cases defeat the frozen requirements.

No document may describe these as solved.

## 5. Chosen target for this subprogram

A candidate case is an **explicitly auditable reasoning artifact** when all conditions below hold:

1. a finite or finitely inspectable artifact is presented as support for an identifiable output;
2. an independent reviewer is expected to evaluate at least one declared property of that support;
3. the review task can be expressed through finite registered questions and answer rules;
4. at least some correct answers are determined by disclosed material or a declared environment;
5. at least one possible artifact can fail the review;
6. at least two faithful representational forms are possible in principle;
7. the source can be inspected and used lawfully and ethically.

This is a research choice. It is not derived as the universal domain of reasoning.

## 6. Excluded scope

The primary program excludes:

- inaccessible private mental states;
- unrecorded intuition;
- embodied skill with no inspectable artifact;
- systems evaluated only by task success;
- claims about neural or biological implementation;
- unrestricted live-oracle dependence;
- any case previously used to define the target architecture;
- any source that cannot be frozen and disclosed under the access policy.

A later scope extension requires a new version and cannot retroactively rescue a failed result.

## 7. Neutral review contract

Each case must instantiate a contract

`K = (E, Y, O, A, Q, R, F, C)`

where:

- `E` — disclosed artifact and declared environment;
- `Y` — supported output;
- `O` — reviewer objective;
- `A` — reviewer access policy;
- `Q` — registered audit questions;
- `R_q` — answer space for each question;
- `F` — failure predicates;
- `C` — cost vector for later comparison.

Questions must be justified by a source-native objective or failure mode. A target architecture's native field names are not independent justification.

## 8. Representation and equivalence

For fixed `K`, a representation is admissible only when it:

- is inspectable under `A`;
- preserves the supported output and every registered answer;
- discloses machinery required to produce those answers;
- obeys declared timing, privacy, security, and locality constraints;
- does not rely on undeclared hidden state or unavailable private oracles.

Two representations are equivalent for the program only relative to the frozen contract:

`r ~_K r'` when all registered answers, operational effects, and cost-relevant behavior agree.

Visible field count, module count, file layout, naming, and serialization are not semantic unless independently registered as observables.

## 9. Recoding policy

The following transformations are presumptively admissible when they preserve the frozen contract and all counted costs:

- identifier renaming;
- record reordering;
- lossless serialization changes;
- table/graph conversions;
- bundling and lossless splitting;
- stored/derived substitution;
- equivalent executable compilation;
- normalized versus denormalized storage.

A transformation may be excluded only by a preregistered independent constraint. Resemblance to or divergence from RCCD is not a valid exclusion reason.

## 10. Claim ladder

Every result must be assigned the strongest supported level and no higher.

0. **Compatibility:** one case can be represented.
1. **Bounded coverage:** all registered development questions are answerable.
2. **Held-out adequacy:** the frozen result covers the sealed validation cases under the fixed rules.
3. **Nontrivial constraint:** negative controls are rejected.
4. **Local necessity:** a requirement survives ablation and hidden-reintroduction review in declared cases.
5. **Comparative economy:** a basis is not Pareto-dominated by registered competitors under full-cost accounting.
6. **Bounded universality:** every case in an independently justified bounded class has the property.
7. **Canonicality:** the basis is unique up to declared equivalence.

Levels 6 and 7 require separate arguments beyond successful finite sampling.

## 11. Required outcomes and failure permission

Valid outcomes include:

- one provisional basis;
- multiple incomparable bases;
- no stable basis;
- target leakage invalidating the study;
- held-out failure;
- RCCD dominated by a competitor;
- RCCD useful but nonminimal;
- evidence insufficient.

The protocol is successful when it produces the strongest justified result, including an unfavorable or Unknown result.

## 12. Theory and software gate

This Charter authorizes only preparation required by the registered clean-room program:

- source capture and hashing;
- packet sanitation;
- coverage verification;
- leakage review;
- preregistered clerical randomization;
- deterministic validation of frozen records.

It does not authorize general software development, a new reasoning engine, new benchmarks, or favorable-case expansion.

## 13. Freeze and change rule

The following must be versioned and hashed before execution:

- target definition;
- eligibility rules;
- sampling dimensions;
- source roster;
- source snapshots;
- packet contents;
- prompts;
- role declarations;
- answer formats;
- scoring and stopping rules.

A substantive post-exposure change creates a new program version and preserves the earlier failure or unresolved result.

## 14. Claim-impact policy

This subprogram can affect RCCD claims only after comparison. A clean-room result may:

- support a bounded RCCD mapping;
- narrow RCCD's legitimate scope;
- show one or more obligations are optional or reconstructible;
- identify missing obligations;
- reveal equal or cheaper alternatives;
- leave the existing theorem unchanged because the evidence addresses a different contract.

No exploratory output automatically changes accepted theory.

## 15. Adoption status

Version 1.1 is registered as Research. It may be used to prepare a confirmatory package only after the source and packet defects listed in the audit are closed.
