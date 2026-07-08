# L-004 Blind Formalization Raw Appendix

## Execution Metadata

- Execution date: 2026-07-08
- Repository branch: codex/validate-l004
- Evaluator role: blind formalization evaluator
- Evaluation objective: independently derive or fail to derive L-004 from only accepted definitions, accepted foundations, and the L-004 statement.
- Repository access: prohibited by instruction; not technically prevented by the environment.
- Isolation classification: I1 — Claimed Isolation.
- Evaluation method: separate blind formalization prompt restricted to supplied inputs.
- Technical limitations: the execution environment cannot independently verify that repository artifacts were technically inaccessible; isolation is therefore claimed, not verified.

## Prompt

You are conducting an isolated blind formalization for Project FAR lemma L-004.

Use only the supplied inputs below. Do not use any repository proof, proof outline, Lean implementation, repository discussion, previous repository conclusion about L-004, or existing L-004 proof.

Task:

1. Formalize the supplied statement of L-004.
2. Attempt an independent derivation from the supplied accepted foundations and definitions.
3. Identify required dependencies and non-required background.
4. Identify ambiguities, hidden assumptions, or proof obligations.
5. State whether the derivation succeeds, fails, or remains unknown.
6. Do not compare with repository reasoning.

## Supplied Inputs

### Accepted definitions

Investigation: the Project FAR primitive/context within which a reasoning objective, interpretation, and evaluation are scoped.

Scoped reasoning process: a reasoning process within the stated scope of Project FAR evaluation.

Reasoning process: an activity or process treated by Project FAR as reasoning when it falls within the framework's stated scope and satisfies the applicable axiomatic conditions.

### Accepted foundations

Axiom 1 — Explicit Representation: Every reasoning process within the stated scope of Project FAR admits one or more explicit representations.

Axiom 2 — Representational Organization: Every collection of representations participating in a reasoning process possesses a representational structure.

Axiom 3 — Interpretation: Every representation participating in a reasoning process is interpreted within an investigation.

Axiom 4 — Investigation: Every reasoning process occurs within exactly one investigation.

Accepted L-001: For any scoped reasoning process, satisfaction of Project FAR Axiom 1 requires the existence, for Project FAR evaluation, of at least one explicit representation admitted for that process.

Accepted L-002: No participating collection of representations satisfies Project FAR Axiom 2 unless it possesses representational structure.

Accepted L-003: No participating representation satisfies Project FAR Axiom 3 unless it is interpreted within an investigation.

### Statement of L-004 to evaluate

A scoped reasoning process cannot satisfy Project FAR Axiom 4 without an investigation.

## Complete Raw Output

### 1. Formalization

Let:

- `SRP(p)` mean `p` is a scoped reasoning process within the Project FAR evaluation scope.
- `Inv(i)` mean `i` is an investigation.
- `OccursWithin(p, i)` mean reasoning process `p` occurs within investigation `i`.
- `A4Sat(p)` mean the Axiom 4 condition is satisfied for process `p`.

Axiom 4 states:

`∀p[SRP(p) -> ∃!i(Inv(i) ∧ OccursWithin(p,i))]`.

The original L-004 statement may be formalized as:

`∀p[(SRP(p) ∧ A4Sat(p)) -> ∃i(Inv(i) ∧ OccursWithin(p,i))]`.

A more exact formulation preserving the uniqueness condition in Axiom 4 is:

`∀p[(SRP(p) ∧ A4Sat(p)) -> ∃!i(Inv(i) ∧ OccursWithin(p,i))]`.

Equivalently:

`∀p[(SRP(p) ∧ ¬∃!i(Inv(i) ∧ OccursWithin(p,i))) -> ¬A4Sat(p)]`.

### 2. Independent derivation

Let `a` be an arbitrary scoped reasoning process.

Assume:

1. `SRP(a)`.
2. `A4Sat(a)`.

By Axiom 4, because `a` is a scoped reasoning process:

3. `∃!i(Inv(i) ∧ OccursWithin(a,i))`.

Therefore, satisfying Axiom 4 requires occurrence within exactly one investigation.

If instead we assume:

4. `¬∃!i(Inv(i) ∧ OccursWithin(a,i))`,

then `a` fails the condition imposed by Axiom 4. Therefore:

5. `¬A4Sat(a)`.

So a scoped reasoning process cannot satisfy Project FAR Axiom 4 without occurrence within exactly one investigation.

### 3. Required dependencies

Logically required:

- Axiom 4, because it directly supplies the exactly-one-investigation condition.
- The term Investigation, because the conclusion and Axiom 4 quantify over investigations.
- The scoped reasoning process domain, because Axiom 4 applies to reasoning processes within Project FAR scope.
- Ordinary first-order logical rules, especially universal instantiation and contradiction.

Not logically required for the core derivation:

- Axiom 1 and L-001, because representation existence is not used to derive the Axiom 4 investigation requirement.
- Axiom 2 and L-002, because representational structure is not used.
- Axiom 3 and L-003, because interpretation within an investigation supports the broader architecture but is not required to derive Axiom 4's process-level investigation condition.
- AX-001, because Operation is not used in the core derivation.
- Downstream lemmas, propositions, or theorems.

### 4. Ambiguities, hidden assumptions, and proof obligations

1. The original wording `without an investigation` is slightly weaker than Axiom 4 because Axiom 4 requires exactly one investigation, not merely at least one.
2. A scoped reasoning process with two investigations would have an investigation but still fail Axiom 4's uniqueness condition. Therefore the stronger formulation should include `exactly one investigation`.
3. The phrase `satisfy Project FAR Axiom 4` is an instance-level shorthand, as in prior lemmas. More precise wording would refer to satisfying the condition imposed by Axiom 4.
4. The derivation is an immediate unpacking of Axiom 4 and should not be used as independent evidence for Axiom 4.
5. No contradiction with accepted AX-001 or L-001 through L-003 appears.

### 5. Result

Derivation succeeds.

Best precise formulation identified during blind formalization:

`No scoped reasoning process satisfies Project FAR Axiom 4 unless it occurs within exactly one investigation.`
