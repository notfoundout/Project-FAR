# PCA-W1 independent-review promotion v1.0

Status: **Accepted on merge**

Program: `POST-CLOSURE-001`

Review target: commit `14105775daf3c5713b134a728db2e1e53673af97`, tree
`68f058199b7c94b707fd5fe978f1ef59d695ab00`, theory
`PROJECT-FAR-CORE-THEORY-1.1`.

Sealed review branch: `research/pca-w1-core-v1.1-independent-review`, head
`0981697546eba68651bddcd22e67ccdeb98decf4`, tree
`3b58ca873c210b62c5ce01f572cb1314b55d95d2`.

## Verification and disposition

The branch adds 18 review artifacts and modifies none of the target tree's files. The target
commit, tree, theory hash, ledger hash, historical-v1 hash, pre-unblinding freeze, terminal
review, and artifact manifest were independently checked. The Stage-A and Stage-E finite
scripts replay deterministically against their committed outputs.

The terminal claim matrix is:

| Verdict | Count |
|---|---:|
| `PROVED` | 14 |
| `REFUTED` | 0 |
| `OPEN` | 0 |
| `UNDERDETERMINED` | 0 |
| `NOT APPLICABLE` | 0 |

The review passes its disclosed independence and integrity tests. It requires no theorem
correction and no software change. It does not establish novelty, priority, a universal
primitive vocabulary, a universal operator basis, or a universal architecture. Every scope
guard and nonclaim remains binding.

The review is therefore accepted as completion of `PCA-W1-INDEPENDENT-REVIEW`. Acceptance
updates an assurance dimension only; it does not rewrite the governing mathematical theory.
`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` becomes the active theoretical workstream.

## FAR-CORE-014 status separation

The independent reviewer assigns `FAR-CORE-014` the truth verdict `PROVED` under only the
stated PR #453 SSS-1/2/3 state, transition-representation, and decoder classes. The governing
v1.1 ledger's `supported_derived` label records the bounded application's historical and
evidence-provenance position. These are different dimensions. Promotion does not relabel the
application as a universal theorem or erase its provenance.

## Immutability

Sixteen terminal/protocol review objects are promoted byte-for-byte as sealed evidence. The
branch's two preparatory machine templates
(`pca-w1-independent-review-evidence-v1.0.json` and
`pca-w1-independent-review-manifest-v1.0.json`) remain only on the sealed review branch:
their embedded pre-run statuses are historical campaign setup, not current Project FAR state.

Future corrections must add a separately versioned adjudication; they must not edit the
protocol, Stage-D freeze, unblinding comparison, terminal review, raw outputs, scripts, or
artifact manifest. Historical v1.0 remains byte
identical at SHA-256
`b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`.

The Stage-A record contains a historical unescaped pipe inside an inline-code Markdown table
cell. The Markdown health check carries a narrow SHA-256-locked exemption for that diagnostic
instead of changing sealed bytes; any byte drift invalidates the exemption and fails CI.

Machine decision:
[`pca-w1-independent-review-promotion-v1.0.json`](../../theory/evaluation/pca-w1-independent-review-promotion-v1.0.json).
