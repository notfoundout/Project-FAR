# Neutral Case-Selection and Clean-Room Derivation Protocol v1.2

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Version: 1.2  
Supersedes within this program: generated Protocol v1.1

## 1. Research question

What review questions are independently required to evaluate explicitly auditable reasoning artifacts, and—only after those questions are frozen—what information structures can answer them with the least total machinery?

The protocol does not ask derivators to recover RCCD, a fixed factor count, or any named architecture.

## 2. Governing separation

The protocol separates two different discoveries.

### Stage A — Review-contract discovery

Cases and source-native reviewer objectives generate:

- failure modes;
- audit questions;
- answer spaces;
- permitted evidence;
- Unknown rules;
- failure predicates.

Stage A must not ask for primitives, minimal information sets, architecture, modules, recodings, ablation, or alternative bases.

### Stage B — Structural analysis

After Stage A outputs are sealed and adjudicated, separately isolated analysts may derive:

- sufficient information sets;
- necessity or cost witnesses;
- exact derivability relations;
- recoding behavior;
- alternative bases;
- full-cost comparisons.

Stage B may not silently add or rewrite Stage A questions. A missing question is a recorded Stage A failure and triggers a new version if correction is required.

This separation prevents the search for a minimal architecture from shaping the supposedly neutral audit questions.

## 3. Units

### 3.1 Case

A case is

`c = (E, Y, O, A, G)`

where `E` is the artifact/environment, `Y` the supported output, `O` the reviewer objective, `A` the access policy, and `G` any source-native rule or evaluation standard.

### 3.2 Failure mode

A failure mode is a concrete way an artifact can cause an incorrect, unsupported, unauthorized, unreproducible, or unjustifiably confident review conclusion under the source-native objective.

### 3.3 Audit question

An audit question is a function from the disclosed case to a declared answer space. It is admissible only when linked to an accepted failure mode or reviewer objective.

### 3.4 Candidate structural item

A candidate structural item is introduced only in Stage B. It may be stored, derived, distributed, bundled, or replaced. It is not presumed primitive or independent.

## 4. Roles

### 4.1 Governance custodian

Maintains versions, hashes, reveal gates, deviations, and role declarations. May know the project target. Does not derive Stage A questions or adjudicate a preferred architecture.

### 4.2 Case curator

Identifies source records using the frozen eligibility and dimension rules. Source matching is recorded as curator judgment unless an executable selection algorithm is preregistered.

### 4.3 Packet sanitizer

Produces a blind packet from frozen source bytes. Records every removal, renaming, condensation, expansion, and format change. May not add architecture-shaped structure.

### 4.4 Stage A derivator

Receives only a blind packet and the Stage A prompt. Has no repository access, no source identity unless necessary, no comparison labels, and no prior derivations.

### 4.5 Stage A adjudicator

Combines sealed Stage A outputs. May accept, reject, merge, or preserve disagreements. Cannot add unsupported questions.

### 4.6 Stage B structural analyst

Receives only the frozen Stage A ledger and disclosed case facts required for structural testing. Performs sufficiency, ablation, recoding, and alternative-basis analysis.

### 4.7 Comparison team

Receives frozen Stage A and B outputs only after validation rules and costs are fixed. This is the first role allowed to introduce RCCD and named competitors.

## 5. Independence labels

Every run must use exactly one highest justified label.

1. **Context-isolated run:** separate session/workspace, no cross-run outputs.
2. **Implementation/model-family independent:** materially different implementation or model family in addition to context isolation.
3. **Human investigator independent:** a different person not involved in theory design or packet creation.
4. **Organizationally independent:** a separate organization controls execution or adjudication.
5. **Adversarial conceptual review:** an independent or explicitly hostile reviewer can challenge scope, questions, competitors, and scoring.

Three isolated sessions by one operator or one model family establish only repeated context-isolated execution. They do not establish external investigator independence.

The current design uses three Stage A runs per development case as a fixed robustness choice. The count has no automatic statistical interpretation.

## 6. Information barriers

A Stage A workspace must not have access to:

- the Project FAR repository;
- this audit report beyond the Stage A prompt;
- RCCD, FARA, FAR, or FARO terminology;
- the target factor count;
- prior project mappings or examples;
- other Stage A outputs;
- Stage B instructions;
- source identities not required to understand the packet;
- validation or challenge identities.

Each output includes a contamination declaration. Suspected target recognition is flagged and excluded from primary convergence claims, while the record remains immutable.

## 7. Blind identifiers

Public and derivator-facing identifiers use `CR-001` through `CR-036` or separately generated packet IDs with no project acronym.

Internal source-registry identifiers, URLs, titles, and hashes remain in the restricted custodian store. No derivator packet may expose an identifier beginning with `FAR`, `FARA`, `FARO`, or `RCCD`.

## 8. Case eligibility

Each source must pass all eight controls before packet preparation:

1. finitely inspectable artifact;
2. identifiable supported output;
3. independent review objective;
4. at least one objective-linked question is possible;
5. at least one artifact can fail;
6. at least some answers are artifact/environment grounded;
7. at least two faithful representations are possible in principle;
8. lawful and ethical access, capture, and use.

A source is excluded when it was used to define the target architecture, cannot be frozen, lacks a meaningful failure condition, or requires unrestricted private mental state.

## 9. Source instantiation and freeze

The sampling array does not freeze source cases. A source row becomes instantiated only when all required fields exist:

- record-level source identity;
- retrieval date;
- source organization;
- stable URL or accession identifier;
- captured source bytes or archival package;
- SHA-256 digest of every captured file;
- applicable license/access note;
- eligibility record;
- dimension coding rationale;
- replacement chain if any.

A report set, search result, organization page, or unresolved candidate list is not an instantiated case.

Mutable web pages must be captured. A URL alone is not a source lock.

## 10. Synthetic-case freeze

A synthetic case is frozen only when it has:

- a complete generator or complete deterministic manual specification;
- generator/specification version and hash;
- seed when randomness is used;
- generated artifact bytes and hash;
- expected source-native task rules, but no target-architecture labels;
- mutation tests showing the generator can produce both passing and failing artifacts.

A seed plus prose description is not a reproducible synthetic case.

## 11. Sampling design

The public design contains:

- 24 development rows;
- 12 sealed validation rows;
- six later challenge cases;
- seven declared coding dimensions;
- 434/434 pairwise level coverage.

All synthetic rows are currently allocated to development. Therefore validation can support only generalization to the naturally occurring public and de-identified operational source classes represented in the holdout. It cannot establish synthetic-to-natural or full source-class generalization.

Pairwise coverage is a combinatorial property of the declared dimensions. It is not evidence that the dimensions are complete or representative.

## 12. Packet schema

A Stage A packet contains only:

1. blind packet ID;
2. task environment;
3. artifact;
4. supported output;
5. reviewer role;
6. source-native review objective;
7. known source-native failure scenarios when disclosure does not answer the task;
8. permitted external sources and access limits;
9. answer constraints and uncertainty rules.

It does not contain:

- target terminology;
- proposed information fields;
- candidate architecture names;
- suggested recodings;
- requested factor counts;
- a source-to-target mapping;
- the Stage B prompt.

## 13. Packet leakage audit

Every packet receives two reviews: sanitizer self-review and independent leakage review.

### 13.1 Lexical review

Block explicit uses of `Project FAR`, `FAR`, `FARA`, `FARO`, `RCCD`, target factor counts, target architecture names, and prior mapping labels unless a term is unavoidable source-native content. An unavoidable collision must be explained and, where possible, neutralized.

### 13.2 Structural review

Reject packets whose recurring headings, table columns, field order, diagrams, or question groups mirror a compared architecture without source-native necessity.

### 13.3 Inferential review

A reviewer who knows only the packet must not be able to infer that the task is to recover a predetermined architecture rather than evaluate a source-native audit objective.

### 13.4 Unequal-detail review

Do not describe target-relevant facts with greater granularity than equally important non-target facts without source justification.

## 14. Stage A execution

Each development case receives three sealed Stage A runs.

The fixed prompt is in Appendix A. Clarifications may correct source facts only. They may not introduce structural-analysis concepts.

Each run records:

- blind case ID;
- prompt hash;
- packet hash;
- derivator identifier;
- model/tool/version when applicable;
- independence label;
- declared accessible context;
- output hash;
- contamination declaration.

## 15. Stage A acceptance tests

An audit question is accepted only if:

1. it is linked to a source-native reviewer objective or accepted failure mode;
2. the answer space is specified;
3. allowed evidence and access are specified;
4. Unknown handling is specified;
5. a failure predicate is stated;
6. it is not a disguised request for a target field;
7. at least one admissible artifact can receive different correct audit outcomes on the question.

Questions can be convergent, witness-supported, provisional, disputed, or rejected. Disagreement is preserved.

## 16. Stage A freeze

Before Stage B begins, freeze and hash:

- all Stage A outputs;
- failure-mode ledger;
- audit-question ledger;
- answer spaces;
- evidence/access rules;
- Unknown interpretations;
- failure predicates;
- disagreements;
- contamination and deviation records.

Stage B receives this frozen package.

## 17. Stage B execution

For every accepted Stage A question, Stage B may propose one or more sufficient information sets.

### 17.1 Sufficiency

A proposed set must include an explicit reconstruction procedure from disclosed information to the required answer.

### 17.2 Necessity

An item is locally necessary only when removing it yields a paired witness: two admissible cases agree on the remaining disclosed information but require different correct answers.

If an equal-cost replacement succeeds, the original item is not necessary as represented.

### 17.3 Hidden reintroduction

Ablation must inspect renamed fields, metadata, hidden state, interpreter behavior, verifier assumptions, external code, ambiguity policies, and case-specific exceptions.

### 17.4 Recoding

Test renaming, reordering, serialization, table/graph conversion, bundling, splitting, stored/derived substitution, and equivalent compilation where applicable.

A visible distinction that changes under exact recoding is not an invariant requirement.

### 17.5 Alternative bases

Generate at least:

- a coverage basis;
- a cost-aware Pareto set;
- a robustness basis across strata.

Several incomparable bases are an allowed result.

## 18. Full-cost accounting

Count all machinery required for success, including:

- stored primitives;
- derived constructs;
- transformation rules;
- semantic description length;
- hidden/auxiliary state;
- ambiguity and adjudication policies;
- external interpreter or executable machinery;
- exceptions and case-specific patches;
- reviewer reconstruction burden;
- storage and execution costs when material.

A tradeoff is not a victory. Superiority requires Pareto dominance or a separately frozen weighting rule.

## 19. Development synthesis

Cross-case synthesis starts after all development Stage B outputs are sealed.

Build a relation graph whose nodes are accepted questions and structural items and whose edges record:

- exact derivability;
- conditional derivability;
- overlap;
- incompatibility;
- replacement;
- cost tradeoff;
- common witness;
- alternative-basis membership.

No fixed partition or component count is assumed. Frequency is recorded separately from necessity.

## 20. Validation freeze and reveal

Before revealing validation identities, freeze:

- Stage A question ledger;
- Stage B relation graph;
- candidate bases;
- comparison costs;
- scoring rules;
- failure rules;
- claim-impact policy;
- source and packet hashes;
- role and independence declarations.

The validation custodian then releases packets, not source registries, to the authorized validation workspaces.

A new required question or structural item is a validation failure for the frozen version. It is not silently added.

## 21. Challenge set

Six adversarial challenges are revealed only after development synthesis and scoring rules are frozen. They target:

- absent versus negative information;
- same output through materially different paths;
- radical lossless recoding;
- conflicting sources or rules;
- hidden external-oracle dependence;
- a smaller equal-behavior alternative.

Because the challenges are designed after seeing the program, they test resistance but do not count as independent recurrence evidence.

## 22. Comparison phase

Named architectures may be introduced only after the neutral outputs and scores are frozen.

At minimum compare:

- RCCD;
- claim/evidence/inference representations;
- provenance graphs;
- event-sourced records;
- assurance cases;
- argumentation frameworks;
- state-transition-observation models;
- behavioral/observational quotient approaches;
- neutral bases generated by Stage B.

Every candidate maps to the same questions, failures, recodings, access rules, and costs.

## 23. Stopping rule

The registered program stops when:

- 24 development cases complete three Stage A runs;
- Stage A is adjudicated and frozen;
- Stage B and development synthesis are complete;
- scoring rules and candidate bases are frozen;
- 12 validation cases are evaluated;
- six challenges are scored;
- factual corrections and deviations are resolved or explicitly Unknown.

The program does not continue until a preferred architecture wins.

## 24. Current execution gate

At version 1.2, execution is **not authorized** because source instantiation, source snapshots, synthetic generators, packet sanitation, and the corrected restricted workbook are incomplete.

## Appendix A — Fixed Stage A prompt

You are independently reviewing an artifact that is presented as support for an output. Do not fit the artifact into an existing theory, architecture, or component list.

Using only the supplied packet:

1. Restate the supported output, reviewer role, review objective, access limits, and relevant source-native rules.
2. List concrete ways the artifact could mislead the reviewer, conceal a failure, or make a justified review conclusion impossible.
3. Derive only the audit questions needed to detect those failures or satisfy the stated review objective.
4. For each question, define:
   - exact wording;
   - permitted answer space;
   - allowed evidence;
   - access or oracle limits;
   - whether Unknown is valid and what it means;
   - the condition under which the artifact fails the review.
5. Separate source fact, logical consequence, reviewer judgment, methodological choice, and unresolved uncertainty.
6. Do not propose primitives, modules, minimum information sets, architecture, recoding tests, ablations, or alternative representations.
7. State whether you recognized or inferred a hidden preferred theory or architecture.

Return:

- review-task restatement;
- failure-mode ledger;
- audit-question ledger;
- unresolved factual questions;
- disagreements or ambiguities;
- contamination declaration.

## Appendix B — Fixed Stage B prompt

You are analyzing a frozen audit-question ledger. You may not add, remove, or rewrite its questions.

For each accepted question:

1. propose one or more sufficient information sets and an explicit reconstruction procedure;
2. attempt local ablation and construct paired necessity witnesses;
3. inspect hidden reintroduction through metadata, code, assumptions, or external machinery;
4. test the registered exact recodings;
5. generate structurally different alternative bases;
6. count all supporting machinery and reviewer burden;
7. preserve incomparable alternatives and Unknown results.

Return:

- sufficiency ledger;
- necessity/cost witnesses;
- recoding report;
- hidden-reintroduction report;
- alternative bases;
- relation graph updates;
- unresolved issues;
- contamination declaration.
