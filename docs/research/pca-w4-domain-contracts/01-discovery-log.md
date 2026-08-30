# W4 discovery and verification log

Protocol commit: `9638185b2f92913b3ce13ee2aaae5289e93945b1`

Execution date: `2026-08-30`

This log records the staged research invocations made after the native queries were frozen. Search-system summaries, citation classifications, and citation counts were treated as discovery metadata only. The admitted claims below were checked against publisher or author-hosted primary records before use.

## Invocation receipt

| Lane | Invocations | Result |
|---|---:|---|
| GitHub | repository, branch, governance, Git-data writes | Pre-search protocol committed before the first external query. |
| Consensus | six domain-bundle searches plus fetches of selected records | Candidate identities and abstracts; selected records fetched before citation. |
| SciSpace | six domain-bundle semantic searches | Candidate identities and related work; no platform summary was used as evidence. |
| Acumen/Talarion | six domain-bundle research briefs | Returned mostly recent or adjacent material; no item met the primary-source contract criterion. Retained as a negative selection result. |
| ordinary web | all 18 frozen queries `W4-Q-*-01..03`, in five batches | Publisher/author records and PDFs used for primary-source verification; noisy and secondary hits rejected. |
| Scite | eight DOI-targeted literature calls | DOI identity, abstracts/full-text passages where indexed, access state, and retraction/correction fields checked. No selected record carried a retraction notice. |
| Zotero | two local status probes | `BLOCKED`: no profile, preferences, API, or connector; `127.0.0.1:23119` refused connection. Repository bibliography used as the fallback, explicitly not represented as Zotero-managed. |
| Wolfram | one context call and two evaluator calls | First evaluator run exposed a malformed argumentation decoder and returned `factorizes = false`; corrected run returned all six collisions and all six repairs `True`. |

## Frozen-query execution

Every query in `research/campaigns/pca-w4-domain-contracts-v1.0.json` was submitted verbatim to ordinary web search. Consensus, SciSpace, and Acumen/Talarion received one bundle per domain made only from that domain's three frozen queries. Scite was used after discovery for targeted source checking, not to change the native questions.

| Domain | Frozen query IDs | Primary records carried forward |
|---|---|---|
| formal logic | `W4-Q-FL-01..03` | Feitosa & D'Ottaviano (2001) |
| Bayesian/causal | `W4-Q-BC-01..03` | Blackwell (1953); Beckers & Halpern (2019) |
| argumentation | `W4-Q-AR-01..03` | Prakken (2010); Modgil & Prakken (2014) |
| model-based reasoning | `W4-Q-MB-01..03` | van der Schaft (2004) |
| type theory | `W4-Q-TT-01..03` | Pientka (2020); Angiuli & Gratzer (2026 pre-publication version) |
| proof theory | `W4-Q-PT-01..03` | Došen (2003) |

## Targeted verification receipt

| Source | Scite query | Verification outcome |
|---|---|---|
| `10.1016/S0168-0072(00)00046-4` | `conservative translation consequence preserve reflect` | Exact DOI/title matched; indexed text describes translations as consequence-preserving and conservative translations as strongly preserving consequence. |
| `10.1214/aoms/1177729032` | `comparison experiment decision problems sufficient garbling` | Exact DOI/title matched; Project Euclid open record found. Used only as decision-relative Bayesian comparison background. |
| `10.1609/aaai.v33i01.33012678` | `intervention exact transformation abstraction` | Exact DOI/title matched; AAAI full text states comparison across allowed interventions and induced distributions. |
| `10.1080/19462160903564592` | `preference attack defeat rebut undercut` | Exact DOI/title matched; indexed text distinguishes attack from preference-sensitive defeat. |
| `10.1080/19462166.2013.869766` | `preferences defeat relation structured argumentation` | Exact DOI/title matched; indexed text states that preferences determine successful attacks/defeats and accepted arguments are evaluated on the defeat graph. |
| `10.1109/TAC.2004.838497` | `bisimulation external behavior equivalence` | Exact DOI/title matched; indexed text relates deterministic bisimulation to external trace behavior and distinguishes nondeterministic cases. |
| `10.1145/3373718.3394735` | `contextual types context judgments equality` | Exact DOI/title matched; full text was not indexed by Scite. ACM proceedings metadata and the authors' type-theory text were used for verification. |
| `10.2178/BSL/1067620091` | `identity proofs normalization cut elimination` | Exact DOI/title matched; Cambridge abstract identifies normalization/cut-free-form criteria and limits their coincidence with generality criteria. |

Consensus records fetched before citation included `d10650f4e2515ddda98fc02b006fd047` (Feitosa & D'Ottaviano), `5ed9e57841195aa1afc5cb517aaf9159` (Blackwell), `cd077264c5b05e1eb1bc9278aab58598` (Otsuka & Saigo, later not needed), `5c1e2361eb0253918e8d27a65aacd1cf` (Prakken), `bd90d717108058f8ac14ae0fae57a3a7` (Amgoud & Cayrol, later not needed), `c6b97571b5835c5aac0541a9e7af3e52` (van der Schaft), `b5af18cd149a5886a0555454f2dae467` (Petković, later not needed), and `0f24a28c68ba577b864b8131a8b69b1e` (Došen).

## Rejections and negative selection results

| Candidate/category | Decision | Reason |
|---|---|---|
| Otsuka & Saigo, category-theoretic causal-model equivalence | not used in the bounded witness | Useful adjacent framing, but Beckers & Halpern gives the direct intervention/distribution contract used here. |
| Rischel & Weichwald, compositional abstraction error | not used in the bounded witness | Valuable for later approximation work; W4 is exact and W5 owns approximation/loss. |
| Goguen & Burstall, institutions | not used in the bounded witness | Broader satisfaction-condition framework than the selected finite consequence query requires. |
| Amgoud & Cayrol; Dung; strong-equivalence papers | not used in the bounded witness | Background or a different contextual-equivalence question; Prakken and Modgil–Prakken directly define the preference-to-defeat step. |
| Petković equality-checking algorithm | not used in the bounded witness | Concerns equality-checker extensibility rather than the selected context-sensitive typing judgment. |
| Proof-system translation papers | not used in the bounded witness | The selected witness concerns proof structure versus end-sequent, not translation between calculi. |
| Acumen/Talarion returned items | rejected as a set | Mostly recent, application-level, or terminologically adjacent; none supplied a better primary definition for a frozen contract. |
| Search snippets, surveys, citation-count rankings, and platform support labels | rejected as evidence | Discovery metadata cannot establish a native definition or the finite witness. |
| Results about approximate preservation, empirical utility, or computational cost | deferred | These belong to W5/W6 and cannot be promoted by W4. |

No absence of a search result is used as novelty or priority evidence.
