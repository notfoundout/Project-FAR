# Post-W1 infrastructure and W2 hostile audit v1.0

Status: **Campaign audit complete; W2 remains active at one bounded obstruction**

Audit base: main commit `14105775daf3c5713b134a728db2e1e53673af97`, tree
`68f058199b7c94b707fd5fe978f1ef59d695ab00`.

This audit is repository consistency and proof-alignment evidence. It is not an independent
mathematical review, novelty search, empirical validation, or substitute for Lean's kernel.

## Hostile findings and dispositions

| Threat | Evidence checked | Disposition |
|---|---|---|
| silent theory change | governing v1.1 monograph and all 14 machine claim statements | no statement changed; only assurance, formalization, and next-workstream metadata changed |
| frozen-review contamination | 16 promoted terminal/protocol paths, two pre-run templates retained only on the sealed branch, review head/tree, full SHA-256 seal and source hashes | every promoted path is pinned and byte-identical; stale pre-run templates are not current state; sealed branch untouched |
| historical v1.0 mutation | canonical and exported monograph bytes | unchanged at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5` |
| truth/provenance conflation | W1 verdicts, assurance ledger, v1.1 machine ledger | `FAR-CORE-014` remains truth `PROVED` and provenance/application `supported_derived` |
| novelty overclaim | current status, registries, tool governance, citation relations | novelty and priority remain not established |
| W1-open drift | current status, roadmap, program, repository truth, generated tasks and exports | W1 complete; W2 active; old statements survive only in sealed or historical records |
| hidden W3 semantics | playground, opportunity registry, deferred product surfaces | finite playground is noncanonical; production contract/API/MCP semantics remain deferred |
| duplicated authority | graph, generated views, Zotero map and status generation | generated artifacts carry source hashes and reject drift; GitHub machine sources remain authoritative |
| vacuous or hidden Lean assumptions | exact declarations, mutation controls, forbidden-placeholder/`constant` scan and machine-parsed `#print axioms` output | every declaration's transitive axiom set is enforced exactly; avoidable assumptions were removed; remaining choice/quotient/extensionality dependencies are recorded per claim |
| scope loss | theorem modules, ledger premises, negative controls | identity does not become a universal minimum; finite panels stay finite; decoder/state/application restrictions remain explicit |
| stale PR #452 state | complete diff and five unresolved review findings | stale state not imported; only provider-neutral machinery reimplemented with outbound redaction, lane isolation, exact recorded replay, and durable failures |
| evidence destruction | branch classifier and GitHub comparisons | no branch or evidence deleted; every unknown or unique branch is retained |
| CI gaps | repository health, generated-view drift, Lean workflow, schema and negative tests | all new generators and capsule checks are in health validation; Lean workflow compiles W2 modules, mutation controls, and the axiom audit |

## Formalization conclusion

`FAR-CORE-001`–`013` are `FORMALIZED` relative to the exact encoded premises.
`FAR-CORE-014` is `PARTIAL/OBSTRUCTION`: its decoder enumeration, two projected Boolean
profiles, and conditional factorization bridges compile, but the repository lacks an encoded
MLL syntax, resource-splitting derivability relation, atom-balance lemma, and proofs of both
actual witness sequents. Adding those narrative facts as axioms would be premise laundering.

No contradiction or new counterexample to an exact v1.1 claim was found. New executable
counterexamples target only stronger variants: erased collision information, missing context
closure, reversed invariance inclusion, noninjective encodings, untyped incidence, missing
operator tags, finite-panel universalization, omitted behavior distinctions, extra Ω
information, and unrestricted state-inspecting decoders.

## Validation boundary

The canonical test suite, full validation profile, focused infrastructure suites, Lean build,
W1 replay scripts, schema checks, source-hash checks, generated-view checks, internal links,
and final-newline/Markdown checks are the terminal validation surface. Passing them establishes
repository consistency and the recorded kernel derivations only.
