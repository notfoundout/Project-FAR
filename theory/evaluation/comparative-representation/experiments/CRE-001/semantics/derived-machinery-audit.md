# CRE-001 Derived Machinery Audit


## Status Vocabulary

- **Supported**: established for frozen CRE-001 vocabulary-semantics scope by explicit source definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.


## Classifications

- `D_boolean_value` — **derived**: explicit truth/status carriers. Introduces two-valued value/status distinction required by CRE-001 model; not primitive-only.

- `D_ordered_history` — **derived**: append-only ordered sequence. Introduces order preservation for history; licensed only with a primitive that supports ordering, history points, or history structure.

- `D_guarded_update` — **derived**: atomic guard/effect records. Introduces guarded transition execution; not arbitrary programming language.

- `D_disjunction` — **derived**: bounded explicit alternative group. Introduces OR guard for halt; limited to registered finite disjunction.

- `D_terminality` — **derived**: halt variable and post-halt blocking. Introduces terminal blocking policy and output treatment under registered ambiguity choices.

- `compiler capability table` — **compiler artifact**: CAPS/CAP_KEYWORDS in tools/cre001_compile_vocabularies.py. Historical compiler-local compatibility heuristic; superseded for semantic licensing by these frozen semantics.

- `lowering trace entries` — **representation artifact**: native construct to common-model trace links. Replay evidence for deterministic implementation; not primitive semantics.

- `registered ambiguity policies` — **semantic assumption**: disable/reject repeatability, prohibited transition output, unterminated output. Frozen assumptions for CRE-001 deterministic scope; stronger claims require separate justification.

- `unbounded quantification/concurrency/probability/higher-order modification` — **unresolved**: outside compiler boundary fixtures. No formal semantics frozen here beyond recording non-support in CRE-001 deterministic scope.
