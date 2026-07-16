# Vocabulary Semantics Baseline 1.0 — Derived Machinery Audit


## Status Vocabulary

- **Supported**: prospectively frozen for CRE-002 and later experiments by explicit baseline definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.

## Chronology and Prospective Authority

- Vocabulary Semantics Baseline 1.0 was formalized after completion of deterministic CRE-001.
- It was informed by lessons learned during CRE-001.
- It is frozen for future experiments beginning with CRE-002.
- It is not independent evidence supporting CRE-001.
- It cannot be used as retrospective validation of CRE-001.
- CRE-001 demonstrates only that compiler-authored declared interpretations successfully compiled, lowered, and verified under the registered deterministic reference.


## Classifications

- `D_boolean_value` — **derived**: explicit truth/status carriers. Introduces two-valued value/status distinction required by CRE-001 model; not primitive-only.

- `D_ordered_history` — **derived**: append-only ordered sequence. Introduces order preservation for history; licensed only with a primitive that supports ordering, history points, or history structure.

- `D_guarded_update` — **derived**: atomic guard/effect records. Introduces guarded transition execution; not arbitrary programming language.

- `D_disjunction` — **derived**: bounded explicit alternative group. Introduces OR guard for halt; limited to registered finite disjunction.

- `D_terminality` — **derived**: halt variable and post-halt blocking. Introduces terminal blocking policy and output treatment under registered ambiguity choices.

- `compiler capability table` — **compiler artifact**: CAPS/CAP_KEYWORDS in tools/cre001_compile_vocabularies.py. Historical compiler-local compatibility heuristic used by CRE-001; not superseded retroactively. Baseline 1.0 may supersede compiler-authored interpretation only for CRE-002 and later preregistered experiments.

- `lowering trace entries` — **representation artifact**: native construct to common-model trace links. Replay evidence for deterministic implementation; not primitive semantics.

- `registered ambiguity policies` — **semantic assumption**: disable/reject repeatability, prohibited transition output, unterminated output. Frozen assumptions for CRE-001 deterministic scope; stronger claims require separate justification.

- `unbounded quantification/concurrency/probability/higher-order modification` — **unresolved**: outside compiler boundary fixtures. No formal semantics frozen here beyond recording non-support in CRE-001 deterministic scope.
