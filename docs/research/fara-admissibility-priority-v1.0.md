# FARA admissibility-priority deductive investigation v1.0

Status: **Research result — alleged circularity dissolved under a stipulative reading (Provisional); one bounded expressive-loss counterexample retained; global priority question unresolved**
Investigation target: `OP-04` / `UQ-T8`
Kind: deductive text-and-definition analysis. No execution, no software, no experiment.

## Authority recovery and discrepancy

`OP-04` asks whether admissibility or valid transition is prior "without circular definition"; `UQ-T8` asks whether admissibility is logically prior to valid transition or both are jointly specified by a calculus. Both record the blocking evidence as "Both depend on a declared calculus/context in current specifications."

This investigation was selected because `OP-04` was the only open problem with no recorded execution artifact. It is confined to canonical definitional text. It does not consume, reinterpret, or weaken any bounded campaign result, and it does not touch the terminal UPP theorem: that theorem's admissibility premise `E*` is independently frozen and is not the FARA `Ω` architecture examined here.

## Canonical definitions under examination

- `D1` — reasoning calculus: "a specification of the rules governing admissible reasoning within an investigation", specifying admissible transformations, admissible inference rules, admissibility criteria, and resolution procedures (`theory/definitions/definitions.md:475-482`).
- `D2` — admissibility: "the property of satisfying the criteria established by the applicable reasoning calculus within an investigation"; "determined by the reasoning calculus"; "not determined by the admissibility structure" (`theory/definitions/definitions.md:596-600`).
- `D3` — valid state transition: "a transition permitted by the governing calculus and declared admissibility conditions" (`docs/glossary/canonical-terminology.md:20`).
- `D4` — `Ω`: "the representation of the admissibility classifications of candidates within an investigation" (`theory/definitions/definitions.md:614`); each candidate carries "either an explicit admissibility classification or an explicitly represented unresolved status" (`frameworks/FARA/admissibility-structure.md:111`).
- `D5` — `Ω` "represents and records those classifications without determining them" (`frameworks/FARA/admissibility-structure.md:43`).

## Findings

### F1 — The alleged circularity is lexical and dissolves only under an unstated reading

`D1` defines the reasoning calculus using "admissible"; `D2` defines admissibility by reference to the reasoning calculus. Substituting `D2` into `D1` yields "a specification of the rules governing reasoning that satisfies the criteria established by that specification", which is self-referential.

Two readings are available. Under a **characterizing** reading, the calculus is picked out by the property of governing admissible reasoning, and the circle is vicious. Under a **stipulative** reading, the calculus is an arbitrary declared tuple and "governing admissible reasoning" is a role gloss, so admissibility is well defined relative to a given calculus and no circle arises.

Canonical text supports the stipulative reading — "Project FAR remains independent of any particular reasoning calculus" (`theory/definitions/definitions.md:484`) treats the calculus as a parameter rather than a characterized object — but **no canonical text states the reading**. The non-circularity of FARA's admissibility architecture therefore rests on an unstated interpretive choice.

Status: **Provisional.** This is a finding about definitional text, not a discovery about reasoning. Minimum sufficient revision, if later authorized, is to state the stipulative reading explicitly. No revision is applied here.

### F2 — Determinant-set asymmetry (weak priority only)

`D3` is ambiguous among three readings of "the governing calculus": the whole calculus, or its rule components alone. Under the reading that takes "governing calculus" as the transformation and inference components and "declared admissibility conditions" as the criteria component, both conjuncts are calculus-internal, and:

- admissibility is determined by the criteria together with the investigation and reasoning-state context;
- valid transition is determined by those same items **together with** the transformation and inference rules.

The determinants of admissibility are then a proper subset of the determinants of valid transition. This yields priority only in the weak sense of **dependency-set inclusion**, and it is a consequence of how `D1` partitions the calculus — a definitional choice, not a derived result about reasoning.

Status: **Provisional.** Blocking condition: canonical text does not fix which of the three readings of `D3` applies. Under a different reading the asymmetry does not follow.

### F3 — The non-circularity guard is one clause, and it does not cover trace reference

`D5` is the clause that prevents `Ω`-referential admissibility criteria from making admissibility self-determining. It blocks reference to `Ω`. It does not block reference to the **reasoning trace**, which is a distinct artifact and which records prior admissibility classifications through transition signatures (`theory/definitions/definitions.md:564`; `frameworks/FARA/admissibility-structure.md:166`).

History-sensitive admissibility is in active use downstream: `docs/research/upp-w8-constrained-evolution-audit.md:9` records the constrained-evolution witness as "a time-indexed, history-sensitive admissibility relation over commitment-state transitions." Canonical FARA states no well-foundedness or strict-past condition on such criteria. `UPP-W8` handles non-resolution by preserving explicit `Unknown` outcomes, which is a downstream convention rather than an upstream structural constraint.

Status: **Provisional.** Observation recorded: a downstream workstream relies on a constraint the upstream architecture does not state. No claim is made that this affects the `UPP-W8` result or the terminal theorem; `E*` is independently frozen.

### F4 — `CE-ADM-001`: bounded expressive-loss counterexample to `Ω`'s per-candidate form

`D4` fixes `Ω` as a per-candidate classification map. Abstract argumentation frameworks (Dung, "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning", 1995) predicate admissibility of **sets** of arguments: a set is admissible when it is conflict-free and defends each of its members.

Two minimal finite witnesses, both hand-checkable:

| Witness | Framework | Result | Loss under a per-candidate `Ω` |
|---|---|---|---|
| `CE-ADM-001a` | `A={a,b}`, attacks `{(a,b),(b,a)}` | preferred extensions `{a}` and `{b}`; grounded `∅` | A per-candidate map cannot encode that `a` and `b` are each admissible but not jointly admissible. |
| `CE-ADM-001b` | `A={a}`, attacks `{(a,a)}` | no stable extension; grounded `∅` | Nonexistence of an extension and multiplicity of extensions both collapse to the same recorded status. |

The characteristic function is monotone, so the grounded extension exists and is unique by Knaster–Tarski; stable extensions need not exist. Under grounded semantics the mapping succeeds and no counterexample arises. The loss appears only under multi-extension semantics.

Status: **Accepted with restricted scope.** Scope: multi-extension admissibility semantics, witnessed by Dung preferred and stable semantics. The counterexample:

- does **not** refute "admissibility is determined solely by the applicable reasoning calculus";
- does **not** indicate a sixth candidate primitive — extension indexing is expressible over existing primitives;
- does **not** bear on the terminal UPP theorem;
- does establish that a single-valued per-candidate `Ω` cannot represent set-valued admissibility without loss, at the stated scope.

### F5 — Rejected constructions (preserved)

Three constructions were attempted and rejected during this investigation. They are recorded to prevent silent return.

| Rejected construction | Reason for rejection |
|---|---|
| Reading Dung's attack relation as a FARA valid state transition, thereby answering `UQ-T8` | Terminology stretch. The attack relation relates arguments, which map to candidates, not to reasoning states. Argumentation does not reach the transition layer of `UQ-T8`. |
| A dilemma that `D3` is either redundant or contradicts `D2` | Defeated by a third reading in which both conjuncts are calculus-internal components. The dilemma had no third horn only because the reading was overlooked. |
| That FARA requires admissibility **criteria** to be candidate-local | False. FARA constrains how classifications are recorded, not how criteria quantify. Criteria may quantify over other candidates. |

### F6 — Documentation defects observed, not repaired

- `theory/evaluation/external-system-investigations/legal-reasoning.md:51` maps `Ω` to jurisdiction, hierarchy, admissible sources, evidentiary standard, and precedent rules. Those are admissibility **criteria**, which `frameworks/FARA/admissibility-structure.md:27-35` states `Ω` is distinct from. A downstream evaluation record redefines an upstream concept.
- `theory/evaluation/external-systems/argumentation-frameworks.md` names its pressure point as "graph-governed admissibility" and classifies the system as `conservative extension` with "No sixth primitive is indicated." The conclusion survives `CE-ADM-001`; the supporting analysis does not, because multi-extension semantics were never tested and "calculus-governed extension selection" conceals that selection must occur upstream of `Ω`.

Neither record is modified. Both are recorded evaluation evidence; the findings are registered in the governance registers instead.

### F7 — Unregistered prior investigation

`docs/reports/ax001-circularity-investigation.md` records remaining open questions 3 ("Can admissibility be defined without rule application, operation, or circular normativity?") and 10 (what establishes the prior status of state, transition, relation, representation, and admissibility). These restate `OP-04`/`UQ-T8` from the FARO side. The report is cited by `AX-001`, the repository index, and audit inventories, but by no governance register.

## Adjudication

`OP-04`/`UQ-T8` is **not resolved**. The alleged circularity is dissolved only provisionally and only by an unstated reading; the priority result obtained is weak, reading-dependent, and definitional rather than discovered. One bounded counterexample is retained against a different target — `Ω`'s per-candidate form — and it raises a discriminating successor question about whether `Ω` can faithfully represent set-valued admissibility.

## Nonclaims

This investigation does not establish or affect: the terminal UPP theorem or any of its frozen premises; global admissibility priority; any primitive necessity, minimality, independence, or sufficiency result; universality; the `FARA-FORMAL-KERNEL-001` acceptance or its scope; any empirical result. No frozen evidence was altered.
