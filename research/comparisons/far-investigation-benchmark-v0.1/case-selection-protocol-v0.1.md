# FAR Investigation Benchmark — Case Selection Protocol v0.1

Status: PREPARED / must be frozen before case discovery  
Parent: `research/comparisons/far-investigation-benchmark-v0.1.md`

## Purpose

Construct the 60-case corpus without selecting cases because they are favorable to FAR, without treating syndicated copies of one proposition as independent cases, and without creating gold conclusions during selection.

## Sampling frame

The six canonical `stratum_id` values are:

1. `public_policy_law` (display code S1);
2. `health_biomedical` (S2);
3. `economics_quant_social` (S3);
4. `science_technology` (S4);
5. `historical` (S5);
6. `media_viral_public_factual` (S6).

Each stratum contributes exactly 10 final cases and at least 10 ordered reserves before S1.

For every stratum, the selectors construct a retrieval-ordered candidate frame from public sources satisfying the frozen discovery cutoff. Candidate discovery uses the same frozen query templates, source classes, tool/provider configuration, pagination rule, and result-count rule for the whole stratum. Every candidate encountered before eligibility screening is recorded, including rejected candidates and non-representative members of duplicate claim families.

The selectors may not search for examples described as "bad reasoning", "misinformation", "fallacy", "debunked", "false", "hoax", "fact check", or equivalent outcome-bearing terms unless such a term is part of the original claim itself.

## Candidate acquisition

For each stratum:

1. Run each frozen discovery query once under the frozen retrieval configuration.
2. Capture the first 50 source-level candidate records in provider-returned retrieval order after only exact mechanical duplicate-record removal under the frozen source-record rule.
3. Record candidate ID, raw provider-returned source identity, retrieval rank, publication/version metadata, verbatim claim text, and discovery-query ID for every captured record.
4. Apply the eligibility and contamination screens without researching the truth of the claim.
5. Independently cluster all provisionally eligible records by substantive proposition identity under the claim-family protocol below.
6. Resolve clustering disagreements before deterministic selection and mark exactly one canonical representative per resolved claim family.
7. Compute the deterministic selection key for each eligible uncontaminated canonical representative.
8. Sort eligible canonical representatives lexicographically by selection key.
9. Provisionally accept the first 10 representatives.
10. Retain the remaining eligible representatives in selection-key order as the reserve frame, with at least 10 reserves per stratum.
11. If the frame cannot supply 10 final cases plus 10 reserves after claim-family deduplication, execute the next preregistered discovery-query batch; never hand-pick replacements.

`corpus_seed = 20260922`.

## Claim-family deduplication

Source-level deduplication is not sufficient. Before selection, substantively identical propositions are clustered even when they appear at different URLs, publications, reposts, speakers, or platforms.

For clustering only, normalize claim text as follows: Unicode NFKC; lowercase; replace CRLF and CR with LF; trim leading/trailing Unicode whitespace; collapse each maximal internal Unicode-whitespace run to one ASCII space. Preserve punctuation after NFKC/lowercasing.

Two candidate records belong to the same claim family when they assert the same material proposition after accounting for subject, predicate, object, and any material time, geography, population, quantity, comparison class, or other scope qualifier. Source identity, publication, later evidence, and eventual truth value are ignored when deciding family identity.

Two distinct independent selectors assign provisional family memberships without access to condition outputs or benchmark results. A distinct `clustering_adjudicator` resolves every disagreement before selection. `case-selection-declarations.json` identifies all three people, their roles, affiliations/providers, independence declarations, conflicts, and prior Project FAR/protocol exposure. The three IDs and identities must be distinct.

For each resolved family, the canonical representative is the member with the minimum tuple `(retrieval_rank, normalized_source_identity, candidate_id)`. Let `cluster_normalized_claim` be that representative's clustering-normalized claim text. `claim_cluster_id` is lowercase hexadecimal `SHA256(UTF8(cluster_normalized_claim))`. Every family member records the same `claim_cluster_id`, and exactly one member records `cluster_representative = true`.

Only eligible, uncontaminated canonical cluster representatives may enter the final corpus or reserve frame. Final and reserve records must therefore have unique `claim_cluster_id` values across the entire selected-plus-reserve set.

## Source identity

`source_identity` is the provider-returned canonical URL string when a URL is available. If the provider exposes no URL, use its stable provider source/document ID prefixed with the frozen provider name, for example `provider_name:source_id`. Do not manually shorten, expand, resolve, strip parameters from, or otherwise canonicalize a URL unless `case-selection-config.json` freezes an exact mechanical canonicalizer before discovery.

The raw source identity is retained separately. The normalized source identity used for deterministic keys follows the selection-key normalization below.

## Selection-key encoding

For deterministic selection-key construction only, normalize the canonical representative's `claim_text` and `source_identity` identically: Unicode NFC; replace CRLF and CR with LF; trim leading/trailing Unicode whitespace; collapse every maximal internal Unicode-whitespace run to one ASCII space; preserve case and punctuation. Encode every field as UTF-8.

The ASCII stratum code used in the key is S1 through S6 according to the fixed mapping above.

Construct the byte string by length-prefixing each field in decimal ASCII:

`len(seed):seed|len(stratum):stratum|len(claim):claim|len(source):source`

Each `len` is the number of UTF-8 bytes and `|` is literal byte `0x7C`. The selection key is the lowercase hexadecimal SHA-256 digest of that byte string.

The required pre-discovery test vector is:

- seed: `20260922`
- stratum: `S1`
- claim: `Example claim`
- source: `https://example.com/a`
- exact serialized UTF-8 text: `8:20260922|2:S1|13:Example claim|21:https://example.com/a`
- SHA-256: `20ef7ac636da4318d3a80d713735cd3cf5554d1ac16042625664c515574af18b`

`case-selection-config.json` must reproduce this vector before discovery begins. A mismatch is `BLOCKED`.

## Eligibility screen

A candidate is provisionally eligible only when all are YES:

- contains an externally checkable factual proposition;
- resolution requires synthesis beyond a single trivial lookup;
- public evidence accessible to every condition appears likely to exist;
- there is a plausible opportunity for evidence omission, interpretation error, or inference error;
- primary adjudication does not require private evidence;
- claim is not a prediction whose truth depends on future events;
- claim is not pure normative preference;
- claim is not merely arithmetic, spelling, dictionary meaning, or direct quotation verification;
- claim was not used in Project FAR development, protocol tuning, demonstrations, or prior benchmark design.

The eligibility screen records only YES/NO plus a short procedural reason. It must not record an expected verdict.

A provisional case becomes final only after the firewalled reference-evidence procedure establishes at least one valid material evidence item. A zero-denominator provisional case is replaced before S1 by the next eligible uncontaminated reserve representative in the same stratum under `reference-evidence-protocol-v0.1.md`.

## Contamination screen

Before provisional acceptance, search the Project FAR repository for distinctive claim phrases and named-case identifiers. Any substantive prior use excludes the candidate. A mechanical name collision without substantive use is recorded but does not automatically exclude.

The selectors declare prior exposure to every provisionally accepted and reserve candidate as one of: NONE KNOWN, INCIDENTAL, SUBSTANTIVE. SUBSTANTIVE exposure excludes the candidate. All contamination decisions and any pre-S1 reserve replacements are frozen before the first condition output exists.

After S1 begins, no leakage discovery may cause replacement. A later-discovered contamination issue is an integrity deviation handled under the frozen disposition/missingness rules or by starting a new campaign version.

## Prompt construction

The case prompt contains only:

- the canonical representative's claim text after only the frozen selection-key Unicode/line-ending/whitespace normalization defined above; no semantic rewrite, paraphrase, grammar repair, or case/punctuation change is permitted;
- source context necessary to disambiguate who/what/time/place the claim refers to, stored separately from the claim text;
- investigation question: `Assess this claim using publicly accessible evidence available by the source cutoff. Distinguish what is established, contradicted, and unresolved.`

No expected answer, evidence hint, source list, argument map, or FAR-specific language enters the case prompt. The exact rendered prompt and SHA-256 are stored in the final case record.

## Deterministic IDs

After final selection and any pre-S1 reserve replacements, sort each stratum's 10 final cases by selection key and assign display IDs `S1-C01` through `S6-C10` using the fixed stratum-code mapping above. Reserve records remain sorted by selection key and receive `S1-R01`, `S1-R02`, etc. IDs are assigned only from this rule and are never manually reused.

The machine-readable `stratum_id` remains the canonical textual ID, not the S1-S6 display code.

## Required candidate and case records

Each candidate-frame record contains at least:

- `candidate_id`;
- canonical textual `stratum_id`;
- `retrieval_rank`;
- raw `claim_text` and clustering/selection normalized forms;
- raw and normalized source identity;
- discovery provenance;
- eligibility and contamination dispositions;
- `claim_cluster_id`;
- `cluster_representative`.

Each final `cases.jsonl` record contains at least:

- `case_id`;
- `candidate_id`;
- canonical textual `stratum_id`;
- `claim_cluster_id`;
- raw and normalized claim text;
- raw and normalized source identity;
- source context;
- discovery provenance and retrieval rank;
- eligibility/contamination disposition;
- selection key;
- exact rendered case prompt;
- SHA-256 of the UTF-8 case-prompt bytes.

## Freeze artifacts

Before S1, the freeze bundle contains and hashes:

- `candidate-frame.jsonl`: all discovered candidates, family memberships, representatives, and screening outcomes;
- `cases.jsonl`: exactly 60 final cases, exactly 10 per canonical stratum, with 60 unique claim-cluster IDs;
- `replacement-frame.jsonl`: at least 10 ordered unused canonical cluster representatives per stratum, disjoint by candidate ID and claim-cluster ID from the final corpus and from one another;
- `case-selection-config.json`: query templates, source classes, cutoff, seed, retrieval configuration, pagination/result rules, source-identity rule, both normalization rules, claim-clustering rule, and selection-key test vector;
- `case-selection-declarations.json`: two selector identities, one clustering-adjudicator identity, independence/exposure/conflict declarations, and contamination-search record;
- the reference-evidence artifacts required by `reference-evidence-protocol-v0.1.md`.

After S1 begins, the confirmatory corpus cannot be replaced or reordered. A later case defect is an integrity deviation handled by the preregistered missingness/disposition rule.
