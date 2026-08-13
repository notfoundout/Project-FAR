# Bounded-v1 Three-Lane Cross-Audit Adjudication v1.0

Status: **Accepted adjudication record of the bounded-v1 internal closure campaign.** This record registers what the campaign established and did not establish. It changes no theory artifact, implements no repair, selects no ADR-002 alternative, and creates no successor freeze.

## Identity

| Field | Value |
|---|---|
| Program / campaign | Bounded-v1 three-lane internal closure audit (per [`../governance/bounded-v1-closure-source-freeze-f6645a77.md`](../governance/bounded-v1-closure-source-freeze-f6645a77.md)) |
| Frozen analytical source | `f6645a77f3b0af0b12897fa9bc2c329cdb345261` |
| Frozen root tree | `a870c1213873158d288ba40bad3952c465e5acab` |
| Method | Three blind first-pass lanes (Lane A semantic closure, Lane B OP-06/proof assurance, Lane C adversarial countermodels) followed by a source-grounded cross-audit that adjudicated every material disagreement against the frozen Git objects |
| Adjudication date | 2026-08-13 |
| Evidence classification | Internal, model-assisted, non-independent. Not R3/R4/R5 replication and not independent validation, per the freeze record's evidence qualifier. |

Primary evidence classes under [`../governance/evidence-replication-and-freeze-standard-v1.0.md`](../governance/evidence-replication-and-freeze-standard-v1.0.md), assigned per finding: the C-D1 finding (XA-001) is **Counterexample** (protected failure within justified scope); the composition findings (XA-002, XA-003, XA-004) and the representation finding (XA-005) are **Boundary**; the status/assurance findings (XA-006, XA-007, XA-008) are **Implementation**. The lane reports themselves remain **Exploratory** claim sources; only cross-audit findings verified against the frozen source are registered here. The more conservative classification controls if disputed.

## Preserved evidence

The verbatim first-pass reports and the full cross-audit adjudication are preserved byte-for-byte as immutable campaign evidence (`.txt` deliberately, following the repository's superseded-snapshot convention — historical text, not live documentation):

- [`bounded-v1-closure-campaign/lane-a-first-pass.txt`](bounded-v1-closure-campaign/lane-a-first-pass.txt)
- [`bounded-v1-closure-campaign/lane-b-first-pass.txt`](bounded-v1-closure-campaign/lane-b-first-pass.txt)
- [`bounded-v1-closure-campaign/lane-c-first-pass.txt`](bounded-v1-closure-campaign/lane-c-first-pass.txt)
- [`bounded-v1-closure-campaign/cross-audit-adjudication-full.txt`](bounded-v1-closure-campaign/cross-audit-adjudication-full.txt)

These files are historical evidence. Per the freeze record's errata rule, findings recorded against `f6645a77` remain attributable to that source permanently; later repairs do not retroactively repair, reclassify, or overwrite them.

## Overall result

`FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED`

Exact interpretation — these clauses must travel together:

- The terminal proposition of the frozen bounded-v1 theorem was **not refuted**. No S,R satisfying the literal W15 antecedent was exhibited for which no RCCD-equivalent operational package exists.
- The **registered derivation is not sound as frozen**: it does not establish the terminal claim over its stated quantifier domain (defects XA-001 through XA-005 below).
- Lane A's closure verdict (`V1_SEMANTICALLY_CLOSED_ON_FROZEN_SCOPE`) is **overturned**.
- Lane B's OP-06 finding is **confirmed**: `OP06_FORMAL_SEMANTIC_BRIDGES_REQUIRED`; the current Lean artifact is partial, name-level formalization (`PTE_W2_PARTIAL`).
- Lane C's W9/W8/W11 challenges are **materially sustained** (with the corrections recorded under "Rejected and adjusted claims" below).
- **No independent validation is claimed.** All three lanes and the cross-audit are internal model-assisted work.

The historical conclusion for the frozen source is permanent: `f6645a77` remains immutable failed-closure evidence. Later successor repairs, however successful, do not vindicate the frozen derivation.

## Confirmed defects

### Semantic / on-graph (bounded-v1 derivation)

| ID | Defect | Frozen source | Severity |
|---|---|---|---|
| XA-001 | W9's universal positive dependency witness is false over part of the frozen terminal domain. The seven frozen W9 antecedents do not imply a nonempty typed dependency edge set, nor at least one support/defeat edge. The antecedent-satisfying empty-dependency system C-D1 survives the frozen C*/E*/P*/closure/equivalence conditions; P* `information_fidelity` forbids fabricating the missing edge; the frozen executable model itself never returns `proved` on the empty-edge corner (`test_empty_edges_are_unknown_not_proved`). | `theory/foundation/upp-dependency-structure-v1.0.json` witness requirements; `docs/research/upp-w9-dependency-structure-v1.0.md`; `theory/foundation/upp_dependency_structure_v1.py`; `tests/test_upp_dependency_structure.py` | High |
| XA-002 | W8 requires `at_least_one_commitment_changing_transition`. W13/W15 do not propagate that side condition, and no frozen degenerate/static bridge exists anywhere in the frozen tree. The terminal derivation is defective on the static corner. | `theory/necessity/upp-w8-constrained-evolution-v1.0.json`; `theory/necessity/upp_w8_constrained_evolution_v1.py` (no-transition branch → `unknown`); W13/W15 statements | High |
| XA-003 | W11 requires `history_sensitive_behavior` and `registered_history_query_totality`. W13/W15 do not propagate those side conditions, and no frozen history-insensitive degenerate bridge exists. The terminal derivation is defective on the memoryless corner. | `theory/history/upp-historical-trace-v1.0.json`; W13/W15 statements | High |
| XA-004 | W13/W15 consume `five_component_necessity` effectively as completed-workstream/status information (queue completion of PRs 281–296), not as establishment of the five component obligations for each exact S,R instance. No case split or per-instance consumption exists. | `theory/sufficiency/upp-sufficiency-construction-v1.0.json` antecedents; `theory/sufficiency/upp_sufficiency_construction_v1.py`; `tools/check_upp_w15_terminal_theorem.py` | High |
| XA-005 | Representation deficiency around determinate absence — see the corrected statement below. | `theory/foundation/upp_dependency_structure_v1.py` empty-edge branch; `theory/necessity/upp_w8_constrained_evolution_v1.py` no-transition branch; P* `error_and_unknown_separation` | Moderate |

**XA-005 — corrected registered requirement.** Known/determinate absence must be representable distinctly from epistemic Unknown wherever required by the repaired theorem. This is the whole registered requirement. It is **not** registered that a new global fourth truth/status value is required; lawful representations include (non-exhaustively) an explicitly established empty typed witness, a theorem-applicability predicate, a local result/witness type, or — only if independently proven necessary — a new status value. The representation mechanism is not predetermined by this record; the successor repair program must select the smallest representation justified by the existing semantics and repair requirements, and `H4` (global status value) may be selected only on a recorded proof that local witness/applicability semantics cannot faithfully express the distinction.

### Assurance / status

| ID | Defect | Frozen source | Severity |
|---|---|---|---|
| XA-006 | G1/OP-06 status surfaces are inconsistent: the Lean header ("closes remainder obligation G1"), `docs/research/g1-end-to-end-semantic-kernel-v1.0.md`, and `theory/evaluation/far-canonical-universality-decision-v1.0.json` (`"g1_relative_semantic_composition": "established"`) conflict with OP-06 (open), UQ-T3 (Unresolved), LIM-007 (Open), the theorem-proof register, and `theory/terminal/g1-semantic-kernel-v1.0.json` (`implemented_pending_validation`). The registers are the conservative, correct surfaces; the closure claims are the overstatement. | Listed surfaces | Moderate |
| XA-007 | `mechanization/lean/UPPSemanticKernel.lean` is partial, name-level formalization only and does not close OP-06: all substantive content is opaque structure fields; canonical `∀S, ∀R` quantification and the existential RCCD package are absent; alignment tests are textual/regex-level. G1's text forbids replacing semantic premises with repository-status assertions. | `mechanization/lean/UPPSemanticKernel.lean`; `tests/test_upp_semantic_kernel_alignment.py`; `docs/research/universality-remainder-theorem-v1.0.md` §G1 | High (for OP-06/PTE-W2 only; the bounded theorem's own declared assurance already disclaims kernel composition) |

### Minor post-terminal hygiene

| ID | Defect | Frozen source | Severity |
|---|---|---|---|
| XA-008 | Several post-terminal Lean names/comments/proofs overstate their evidential content: `MaximalKnowability.no_embedding_no_registered_scope_dominance` proves `¬X` from `¬X`; `g2_open_world_structural_lower_bound` leaves stated hypotheses unused; `FARCanonicalUniversalityDecision` "independence" wording is proved only as Boolean `decide` bookkeeping. Off the bounded-v1 semantic graph. | `mechanization/lean/MaximalKnowability.lean`; `G2OpenWorldLowerBound.lean`; `FARCanonicalUniversalityDecision.lean` | Minor |

## Adjudications that did not become defects

- **ADR-002:** `ADR002_OFF_GRAPH_NONBLOCKING`, including under the newly confirmed defects. The UPP chain contains zero references to FARA, Ω, or FARA `unresolved status`; the XA-005 issue concerns the UPP models' own three-valued vocabulary, not FARA's `:111`. ADR-002 remains untouched and unselected.
- **P*/W6 conclusion-loading:** `INFORMATIONAL_CONCLUSION_LOADING_BUT_NO_LOGICAL_CIRCULARITY`. The necessity lemmas' informational content is largely premise-supplied and they must not be described as neutral discoveries; but no frozen surface claims neutral discovery, no premise literally asserts the conclusion, and C-D1 itself proves the premises do not logically contain the lemma conclusions. This classification is not to be reopened as a confirmed semantic defect absent new evidence from a separately authorized investigation.
- **W8 and W11 as lemmas:** sound conditionals on their own antecedents; the confirmed defect is compositional (XA-002/XA-003), not lemma falsity.
- **W14 maximality, W5 closure, W6 equivalence, W12 as stated, C\* neutrality, Unknown→Pass paths:** all attacked and all survived; see the preserved lane and cross-audit reports.

## Rejected and adjusted claims

- Lane A's closure verdict: rejected (missed propagation of the W8/W11 side conditions and the W9 empty-relation corner). Lane A's ADR-002, UQ-T8/T16/T17, Lean-fidelity, and G1-status findings survive.
- Lane C's classification of the P*/W6 finding as a `LOGICAL_DEFECT`: adjusted to informational loading without circularity (above).
- Lane C's C-T1/C-H1: sustained as composition defects only, exactly as Lane C itself scoped them.

## Mandated sequencing consequence

OP-06 / PTE-W2 kernel reconstruction is downstream of semantic repair. The current Lean layer must not be upgraded first: a faithful kernel proof of the frozen chain would either formalize a defective dependency composition or silently repair semantics inside Lean, causing source/proof drift. See the successor repair program registration: [`../research/upp-successor-repair-program-v1.0.md`](../research/upp-successor-repair-program-v1.0.md).

## Claim boundary

This record establishes only what is stated above. It does not establish that the terminal proposition is false, that any repair will succeed, that the successor theorem will retain the full frozen domain, independent validation, any replication layer, or any change to FARA, ADR-002, or the frameworks' status.
