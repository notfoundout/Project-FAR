# UPP Successor Semantic Repair Program v1.0

## Identity

Program: `UPP-SR-001`

Status: **Registered. Implementation not yet begun.** This document authorizes the repair program's scope and gates; it implements no repair.

Predecessors: completed Universal Proof Program `POST-TUE-UPP-001` (terminal PR #296) and the bounded-v1 three-lane internal closure campaign adjudicated in [`../audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md`](../audits/bounded-v1-three-lane-cross-audit-adjudication-v1.0.md).

Governing standards: [`../governance/research-execution-charter.md`](../governance/research-execution-charter.md) and [`../governance/evidence-replication-and-freeze-standard-v1.0.md`](../governance/evidence-replication-and-freeze-standard-v1.0.md).

This program does not reopen the closed UPP deductive queue (there is no `UPP-W16`), does not amend the `POST-TERM-EVAL-001` evaluation program, and does not alter the frozen `f6645a77` evidence. It is the separately registered program that a successor deductive claim requires.

## Objective

Produce the strongest defensible successor bounded-v1 theorem that repairs the confirmed defects `XA-001` through `XA-005` without inventing phenomena, silently shrinking scope, or retroactively validating the frozen theorem.

The frozen conclusion is permanent: `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED` for `f6645a77f3b0af0b12897fa9bc2c329cdb345261`. Every successor artifact must carry a new version identity; a repaired candidate cannot inherit the `f6645a77` freeze, and the successor source freeze is created only after implementation, regression, and validation complete (see "Materiality and successor freeze" below).

## Repair hypotheses to be tested

Do not force a positive repair outcome. Each hypothesis must be tested against the exact frozen semantics and may be falsified. `NONE`/obstruction is a valid result.

### H1 — Local/typed-degenerate repair

- W9 permits an explicitly established empty typed dependency relation when the underlying system has no registered dependency facts.
- Nonempty/support-defeat obligations become conditional on the existence of relevant dependency phenomena.
- Static systems receive a valid degenerate constrained-evolution representation rather than fabricated transitions.
- History-insensitive systems receive a valid degenerate/trivial historical representation rather than fabricated history.
- W13/W15 perform explicit per-instance case analysis.

### H2 — Applicability-indexed component repair

- Preserve three-valued epistemic status unchanged.
- Separate theorem applicability / phenomenon presence from epistemic Pass/Fail/Unknown.
- W8/W9/W11 produce typed results indexed by whether the relevant phenomenon is present.
- Terminal package obligations are conditional on applicability.

### H3 — Explicit terminal scope reduction

- Preserve existing nondegenerate component definitions.
- Restrict the terminal theorem to systems with commitment-changing transitions, required dependency phenomena, and history sensitivity, as necessary.
- Logically available but strictly weakens the theorem; selectable only if H1/H2 cannot be justified, and only as an explicit, recorded scope reduction — never a silent one.

### H4 — New global status value

- Introduce a distinct global status such as `EstablishedAbsent`.
- **Not preferred by default.** Selectable only on a recorded proof that local witness/applicability semantics (H1/H2) cannot faithfully express the required distinction.

### H5 — No coherent repair preserving full domain

- If none of H1–H4 survives falsification, record the obstruction and derive the strongest narrower theorem that actually follows.

H1 and H2 are competing candidate mechanisms for the same requirement; the program must adjudicate between them (or a justified combination) by smallest sufficient change, not preference.

## Determinate-absence requirement (XA-005, corrected)

The registered requirement is exactly:

> Known/determinate absence must be representable distinctly from epistemic Unknown wherever required by the repaired theorem.

The representation mechanism is not predetermined. Lawful representations include, non-exhaustively: an explicitly established empty typed witness; a theorem-applicability predicate; a local result/witness type; or, only if independently proven necessary, a new status value. Choose the smallest representation justified by the existing semantics and repair requirements, and record the justification.

## Forbidden repairs

The following moves are prohibited in every workstream of this program:

- redefining every appraisal standard as a support/defeat edge;
- fabricating dependencies where the source has none;
- fabricating commitment-changing transitions for static systems;
- fabricating meaningful history for history-insensitive systems;
- promoting determinate absence to Unknown (or Unknown to any positive result);
- treating repository/workstream completion as proof that a per-instance semantic premise holds;
- adding a premise solely because it saves the theorem, without independent justification;
- silently narrowing `C*`, `E*`, or `P*`;
- silently changing the W6 equivalence relation;
- claiming the frozen `f6645a77` theorem is now vindicated;
- beginning OP-06 formalization before the semantic repair stabilizes.

## Workstreams

| Workstream | Deliverable | Boundary |
|---|---|---|
| `SR-W0-REGISTRATION` | This registration plus the adjudication record and register synchronization — complete on merge of the registration change set. | Registration only; no theory, test, or Lean change. |
| `SR-W1-ABSENCE-REPRESENTATION` | Adjudicated selection of the determinate-absence representation (H1/H2/H4 mechanism question), with falsification attempts recorded. | Smallest justified representation; H4 requires proof of necessity. |
| `SR-W2-W9-REPAIR` | The exact weakest true W9 successor theorem over the frozen `C*`/`E*`/`P*`/closure/equivalence domain (questions A–D below), as versioned successor artifacts. | No forbidden repair; K-matrix corners must be derivable. |
| `SR-W3-W8-DEGENERATE` | The weakest true theorem covering both transition-bearing and static systems (question structure below), or a recorded rejection plus scope-reduction test. | Degenerate objects must be derived from component semantics, not assumed. |
| `SR-W4-W11-DEGENERATE` | Same for history-sensitive and history-insensitive systems. | Same. |
| `SR-W5-RECOMPOSITION` | Successor W13/W15 composition consuming per-instance semantic propositions with explicit case structure and a fully visible antecedent graph. | May not consume queue/PR completion as semantic entailment. |
| `SR-W6-REGRESSION` | Implementation of the preregistered K1–K8 regression matrix. | Tests follow the derived repair; expected outcomes below remain hypotheses until derived. |
| `SR-W7-VALIDATION-AND-FREEZE` | Full validation of the repaired candidate; then, and only then, the successor source freeze under the freeze standard. | Freeze gates below. |
| `SR-W8-STATUS-RECONCILIATION` | XA-006 governance reconciliation and XA-008 mechanization hygiene. | Status surfaces only; OP-06 is not closed by this workstream. |

OP-06/PTE-W2 kernel reconstruction is **not** a workstream of this program; it is sequenced strictly after `SR-W7` (see "OP-06 sequencing").

## Required W9 repair question (`SR-W2`)

Settle: **what is the exact weakest true W9 theorem over the original frozen `C*`/`E*`/`P*`/closure/equivalence domain?**

Test at minimum, deriving each from existing semantics rather than assuming it:

- **A.** Every qualified system has a recoverable typed dependency relation, possibly empty.
- **B.** If a qualified system has at least one registered dependency fact, the relation is nonempty.
- **C.** If a qualified system has at least one support/defeat dependency fact, at least one support/defeat edge exists.
- **D.** Correctly established empty dependency answers count as successful faithful recovery, not Unknown.

Determine whether A–D follow from the existing semantics. Do not assume them. Record which are theorems, which require the new representation from `SR-W1`, and which fail.

## Required W8 repair question (`SR-W3`)

Determine the weakest true theorem covering **both** transition-bearing systems **and** static systems. Candidate structure:

- If commitment-changing transitions exist: prove the original W8 nondegenerate witness.
- Else: prove an explicitly static/empty-domain constrained-evolution representation that correctly states that there are no commitment-changing transitions to classify.

Test whether such an object genuinely satisfies the intended RCCD component semantics. If it does not, report that and test scope reduction (H3) instead.

## Required W11 repair question (`SR-W4`)

Determine the weakest true theorem covering **both** history-sensitive systems **and** history-insensitive systems. Candidate structure:

- If registered path-sensitive distinctions exist: prove the original W11 nontrivial trace witness.
- Else: prove an explicit history-insensitive/trivial trace representation sufficient to preserve all registered historical commitments.

Do not assume a trivial trace qualifies. Derive it from the intended component semantics or reject it.

## Required W13/W15 recomposition (`SR-W5`)

The repaired composition must consume semantic propositions for the exact S,R instance. It may not use "workstream W8 complete", "PR #289 complete", or "all workstreams registered complete" as a substitute for "W8's relevant proposition holds for this S,R". Explicit case structure or typed theorem dependencies are required, and the successor W13/W15 dependency graph must make every antecedent visible — including every specialized side condition and every degenerate branch.

## Preregistered regression matrix (`SR-W6`)

The expected outcomes below are **hypotheses until the repair is formally derived**; the derived successor semantics adjudicates them. No test is implemented at registration time (governance requires no executable registration fixture at this stage).

| Case | Construction | Key expectations to adjudicate |
|---|---|---|
| K1 | Rich case: transitions > 0; dependencies > 0; support/defeat present; history sensitive | All lemmas nondegenerate; successor W15 positive. |
| K2 | C-D1: transitions = 0; dependencies = 0; history insensitive; dependency queries total; all absences determinate | `C*` in; `E*` admissible; `P*` Pass; W9 established-empty (not Unknown); W8/W11 degenerate branches; successor W15 positive under the revised statement. Frozen-chain behavior (Unknown / underived) is the defect reproducer. |
| K3 | Transitions > 0; dependencies = 0; history sensitive | W9 established-empty; remainder nondegenerate. |
| K4 | Dependencies exist but no support/defeat edges (e.g. provenance/admissibility-only relation, if permitted) | The support/defeat sub-claim's antecedent is absent; the negative verdict on the positive-witness sub-lemma must survive the weakening. |
| K5 | Static system; dependencies present; history insensitive | W8/W11 degenerate; W9 nonempty. |
| K6 | History sensitive; required history query unavailable/unregistered | W11 inapplicable by antecedent, recorded as such; not promoted to Unknown or to success. |
| K7 | Fabricated-edge representation of an actually dependency-free source | Must fail `P*` information/dependency fidelity; out of the terminal antecedent. |
| K8 | Genuinely inaccessible/unresolved dependency evidence | Must remain Unknown and must be distinguished from K2/K3 determinate emptiness. K2 vs K8 is the decisive discrimination pair. |

For each case, preregistered evaluation dimensions: `C*`; `E*`; `P*`; W7; W8 applicability/result; W9 applicability/result; W10; W11 applicability/result; W12 relevance; W13 result; W15 result.

## Success gates (`SR-W7` entry criteria)

Implementation may not be declared complete merely because tests pass. All of the following semantic gates must hold, each with recorded evidence:

- C-D1 no longer contradicts the successor W9.
- Determinate absence is distinct from epistemic Unknown (K2/K8 discrimination demonstrated).
- Static `C*` systems are handled lawfully or explicitly excluded by a recorded revised scope.
- History-insensitive `C*` systems are handled lawfully or explicitly excluded by a recorded revised scope.
- Every W13 component dependency is valid for the exact S,R instance.
- W15 no longer consumes queue completion as semantic entailment.
- No fabricated edge/transition/history can satisfy `P*` (K7 negative control).
- Rich nondegenerate systems preserve the original stronger component obligations (K1).
- W14 maximality remains frozen-ledger-relative; no unrestricted universality language is introduced anywhere.
- ADR-002 remains untouched unless a new dependency on it is actually proven.
- The conclusion-loading classification remains `INFORMATIONAL_CONCLUSION_LOADING_BUT_NO_LOGICAL_CIRCULARITY` unless separately reopened with new evidence.
- Every theorem change is explicitly identified as a successor-theory change; no artifact claims the frozen theorem was vindicated.

## Validation requirements (predefined for the implementation phase)

The implementation change set must pass, at minimum (commands are the repository's actual canonical targets):

- all new K1–K8 regression cases and all existing W7–W15 test suites (`make test` / `make test-fast` as applicable);
- `make semantic-check`;
- `make research-check`;
- `make docs-check`;
- `make links-check`;
- `make health-fast` (and `make health` when the change set touches surfaces it covers);
- `make validate-changed` (and `make validate-full` before the successor freeze);
- relevant Lean checks (`make validate-formal`) once the semantic repair reaches the mechanization stage — not before;
- explicit negative tests for fabricated dependency/history/transition evidence (K7 family);
- explicit K2/K8 determinate-absence vs Unknown discrimination tests.

## Materiality and successor freeze

The semantic repair is expected to be **material** under the freeze standard, because it changes W9 witness semantics, W8/W11 applicability, the determinate-absence representation, the W13/W15 composition, the component-nontriviality interpretation, and the theorem statement/antecedent structure. Therefore:

- the repaired candidate cannot inherit the `f6645a77` freeze;
- successor artifacts must carry new version identities; frozen v1.0 result records remain immutable evidence on their original terms;
- **the successor source freeze is not created by this registration.** It occurs only after: (1) implementation complete; (2) registered regression tests pass; (3) repository validation passes; (4) semantic surfaces are internally synchronized; (5) no known repair defect remains;
- fresh closure audits then run against that successor freeze, per the freeze record's material-change rule.

## OP-06 sequencing

OP-06/PTE-W2 kernel reconstruction is downstream of semantic repair. The current Lean layer must not be upgraded first: a faithful kernel proof of the frozen chain would either formalize a defective dependency composition, or silently repair semantics inside Lean and cause source/proof drift. After successor semantic repair and validation, OP-06 must target the repaired theorem. The minimum faithful target remains: formal `C*`; formal `E*`; formal `P*`; formal machinery closure; formal W6; exact repaired W7–W11 theorem schemas; W12; the repaired W13 construction; W14; the exact repaired W15; `∀ S`; `∀ R`; an existential RCCD package; the exact preservation dimensions; the exact case/applicability semantics; and no name-only placeholders standing in for canonical propositions.

## Status reconciliation (`SR-W8`)

Until OP-06 is genuinely closed, the current Lean G1 wrapper is a **partial formalization / conditional composition layer**, not full G1 semantic reconstruction. Surfaces requiring eventual reconciliation (not changed by this registration beyond the register/status updates in the registration change set): `mechanization/lean/UPPSemanticKernel.lean` header comment; `docs/research/g1-end-to-end-semantic-kernel-v1.0.md`; `theory/evaluation/far-canonical-universality-decision-v1.0.json` (`g1_relative_semantic_composition`); `theory/terminal/g1-semantic-kernel-v1.0.json`; OP-06, UQ-T3, LIM-007; the theorem-proof status register; and project status. OP-06 must not be marked closed by any workstream of this program.

## Implementation authorization boundary

The next implementation pass (SR-W1 through SR-W6), once separately authorized to begin, **may** change:

- successor-version theory artifacts for W9, the W8/W11 degenerate cases, and the W13/W15 composition (new version identifiers; frozen v1.0 records untouched);
- successor-version executable models and checkers implementing the derived repair semantics;
- new regression tests implementing the preregistered K1–K8 matrix;
- research/audit documents recording the hypothesis adjudications;
- registers and status surfaces, only to record the program's own governed progress.

It **may not** change:

- the frozen `f6645a77` history or any historical evidence record, including the campaign evidence files;
- `C*`, `E*`, `P*`, W5 closure, or W6 equivalence semantics, except through an explicitly registered, justified material change (none is currently authorized);
- ADR-002 (no A/B selection; no reopening);
- any Lean/mechanization artifact toward OP-06 closure before `SR-W7` completes (XA-008 naming/comment hygiene under `SR-W8` is exempt);
- the terminal result recorded for the frozen source, on any surface;
- W14's ledger-relative maximality boundary or any nonclaim;
- and it may not create the successor source freeze before the `SR-W7` gates are met.

## Operating principle

Do not optimize for preserving the old theorem. Optimize for discovering and registering the strongest theorem actually supported by the evidence. Do not silently weaken, silently strengthen, or silently redesign. Search before building; test before shipping; preserve failed evidence; make every repair falsifiable.
