# PCA-W1 Independent Review Protocol v1.0

Status: **PREPARED — REVIEW NOT STARTED**

Program: `POST-CLOSURE-001`

Workstream: `PCA-W1-INDEPENDENT-REVIEW`

## Immutable review target

The object under review is the merged Project FAR v1.1 successor state, not the mutable review branch.

- Repository: `notfoundout/Project-FAR`
- Target commit: `14105775daf3c5713b134a728db2e1e53673af97`
- Target tree: `68f058199b7c94b707fd5fe978f1ef59d695ab00`
- Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`
- Governing monograph: `theory/theorems/Project-FAR-Theory-Closure-v1.1.md`
- Governing monograph SHA-256: `91513dce21273364ef8ad24ebd1102e3b5957b513bbd5bc429f2b10917fa8239`
- Machine ledger: `theory/terminal/project-far-core-theory-v1.1.json`
- Machine ledger SHA-256: `66372644e5a2fe65c93f7e893e41eae74211934f92827cadcfe28dd81290ab40`
- Preserved historical v1.0 SHA-256: `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`
- Specification export version: `1.2.0`

The target tree is exactly the content tree of the final PR #457 head that passed Specification Export, Formal Artifact Validation, Lean Mechanization, both Repository Health workflows, Unified Validation Shadow, and Validator Assurance. Those checks establish repository consistency only; they are not evidence that the theory is true.

## Independence requirement

The reviewer must be genuinely isolated from prior Project FAR reasoning. A reviewer with material prior exposure must disclose that exposure and cannot be classified as the independent reviewer merely because it starts a new execution.

Before reading the target, the reviewer must record:

1. reviewer/model identity;
2. prior exposure to Project FAR, if any;
3. conflicts or incentives;
4. tools available;
5. external-data access available;
6. date/time and environment;
7. any unavoidable contamination.

If material prior exposure exists, output `INDEPENDENCE FAILED` and do not relabel the work independent.

## Staged-access rule

### Stage A — blind reconstruction

Allowed initially:

- `theory/theorems/Project-FAR-Theory-Closure-v1.1.md` at the pinned target commit;
- the assurance rules in `docs/governance/post-closure-assurance-and-application-program-v1.0.md` only as review procedure;
- independently chosen formal, mathematical, or computational tools.

Do not inspect during Stage A:

- PR #457 discussion, diff, or commit history;
- `docs/audits/project-far-core-theory-v1.1-correction-audit.md`;
- `docs/research/project-far-core-v1.1-correction-replication-v1.0.md`;
- `docs/governance/project-far-theory-closure-acceptance-v1.1.md`;
- v1.0 theory or ledger;
- previous Project FAR chat/session history or project memory;
- prior internal source lists or prior-art conclusions;
- repository tests as evidence for a theorem.

The reviewer must independently reconstruct every proposition, premise, quantifier, proof step, dependency, and falsifier in the v1.1 monograph.

### Stage B — claim reconciliation

Only after the independent reconstruction is recorded, inspect `theory/terminal/project-far-core-theory-v1.1.json` to reconcile exact claim IDs and scopes, including the stated scope of `FAR-CORE-014`.

Any mismatch between the independently reconstructed proposition and the machine ledger must be recorded rather than silently harmonized.

### Stage C — independent prior-art and countermodel search

Begin with an empty external evidence corpus. Do not seed searches from Project FAR's prior source lists.

For each material claim:

- derive search terms from the claim itself;
- search for stronger predecessors, equivalent formulations, counterexamples, impossibility results, boundary conditions, and simpler competing architectures;
- record every material query, database/tool, result accepted, result rejected, and reason;
- prefer primary sources where available;
- distinguish bibliographic discovery from logical validation.

Available research tools may include Acumen/Talarion for current-state reconnaissance, Consensus and SciSpace for scholarly discovery, Scite for citation context/full-text evidence when access permits, web search for uncovered literature, and Wolfram for computational checks where the proposition is representable. Tool agreement is not proof and shared-source dependence must be considered.

### Stage D — provisional verdict

Before reading any internal correction audit or prior Project FAR review, freeze a provisional claim-by-claim verdict and terminal verdict.

Required statuses are drawn from:

`PROVED`, `REFUTED`, `OPEN`, `BLOCKED`, `UNDERDETERMINED`, `NOT APPLICABLE`, `HISTORICAL/SUPERSEDED`.

For every claim, record:

- exact proposition reviewed;
- scope and quantifiers;
- premises used;
- proof reconstruction;
- strongest countermodel attempt;
- prior-art result;
- unresolved objections;
- dependency impact;
- provisional status;
- falsifier or reopening condition.

### Stage E — controlled unblinding

Only after Stage D is frozen may the reviewer inspect internal historical material, including the v1.1 correction audit, acceptance record, PR #457, v1.0, regression fixtures, and prior internal research.

The reviewer must then report:

- which independent findings matched prior internal findings;
- which findings were genuinely new;
- which prior internal conclusions were not independently reproduced;
- whether unblinding changes any verdict and why.

Unblinding must not erase the Stage D record.

## Required hostile tests

The review must, where applicable:

- negate premises one at a time;
- attack universal and existential quantifiers;
- search finite and infinite countermodels;
- test degenerate/identity/constant/injective cases;
- test boundary and empty cases;
- search type/domain mismatches;
- trace hidden dependence on representations, contracts, languages, frames, semantics, or invariance assumptions;
- distinguish necessity from sufficiency;
- distinguish existence from minimality and uniqueness;
- distinguish host capacity from native structure;
- distinguish finite-panel evidence from open-domain universality;
- test whether purportedly independent parameters actually occur in definitions;
- search for stronger prior frameworks and simpler equivalent bases.

## Evidence rules

- CI, tests, schemas, and successful encoding are consistency evidence only.
- Previous acceptance, repository status, or internal agreement are not proof.
- A citation establishes only what the cited source actually supports.
- A computational check establishes only the represented finite/symbolic case unless a valid general derivation follows.
- Failure to find a counterexample is not a proof.
- Failure to find prior art is not a novelty proof.

## Required outputs

The reviewer must produce, before any promotion decision:

1. exposure/conflict statement;
2. tool and environment record;
3. blind reconstruction ledger;
4. premise/dependency graph;
5. countermodel ledger;
6. prior-art search log and source corpus;
7. claim-by-claim verdict for `FAR-CORE-001` through `FAR-CORE-014`;
8. unresolved-objection register;
9. provisional terminal verdict frozen before unblinding;
10. controlled-unblinding comparison;
11. exact final terminal verdict;
12. minimum repository consequences, if any.

## Repository-write rule

The review target is immutable. Work may be committed only to `research/pca-w1-core-v1.1-independent-review` or another dedicated review branch. Do not modify `main` during the audit. Any discovered contradiction must first be recorded as review evidence; correction requires a separate governed reopening after review adjudication.

## Current state

This protocol prepares the environment only. `PCA-W1-INDEPENDENT-REVIEW` has **not started** and remains `OPEN` until a genuinely isolated reviewer executes the protocol.