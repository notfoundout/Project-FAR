# Project FAR knowledge-graph foundation v1.0

Status: **Generated-data foundation; not an independent truth system**

The canonical graph artifact is generated at
[`project-far-knowledge-graph.json`](../../artifacts/knowledge-graph/project-far-knowledge-graph.json)
from the core, assurance, opportunity, research-question, citation, tool, threat, campaign, and
formalization registries. Every input path and SHA-256 is embedded in `generated_from`.

Supported node types are claim, definition, premise, theorem, proof, counterexample,
limitation, open problem, research question, source, evidence artifact, contract, domain,
representation, test/context, tool, version, PR/commit, and workstream. Supported edge types
are `DEPENDS_ON`, `PROVES`, `REFUTES`, `SUPPORTS`, `DERIVES`, `LIMITS`, `SUPERSEDES`,
`IMPLEMENTS`, `FORMALIZES`, `CITES`, `TESTS`, `APPLIES_TO`, `ASSUMES`, `CONFLICTS_WITH`.

The generator rejects unknown identifiers, dangling edges, contradictory node mappings,
duplicate ownership, prohibited dependency cycles, assurance/core/review status or scope
disagreement, and stale output. Claim nodes use the neutral status
`multidimensional_assurance`: their W1 truth disposition, governing-ledger provenance,
narrative-proof, independent-review, Lean, empirical, novelty/prior-art, governance, version,
and exact reviewed scope fields remain separately queryable. Conclusions are not hand-entered in the graph; they are projected from
governed machine data. To change a conclusion, change its authoritative source through the
governed lifecycle and regenerate.

The current graph is a backend truth architecture, not a polished public explorer. It may be
queried or visualized downstream, but a visualization must retain node scope, status dimension,
source, and version.
