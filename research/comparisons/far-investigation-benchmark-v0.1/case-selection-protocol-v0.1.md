# FAR Investigation Benchmark — Case Selection Protocol v0.1

Status: PREPARED / must be frozen before case collection  
Parent: `research/comparisons/far-investigation-benchmark-v0.1.md`

## Purpose

Construct the 60-case corpus without selecting cases because they are favorable to FAR and without creating gold conclusions during selection.

## Sampling frame

Six strata are fixed:

1. public policy / law;
2. health / biomedical;
3. economics / quantitative social claims;
4. science / technology;
5. historical claims;
6. media / viral or public factual claims.

Each stratum contributes exactly 10 final cases.

For every stratum, the selector constructs a **retrieval-ordered** candidate frame from public sources that satisfy the frozen discovery cutoff. Candidate discovery uses the same frozen query templates, source classes, tool/provider configuration, pagination rule, and result-count rule for the whole stratum. Every candidate encountered before eligibility screening is recorded, including rejected candidates.

The selector may not search for examples described as "bad reasoning", "misinformation", "fallacy", "debunked", "false", "hoax", "fact check", or equivalent outcome-bearing terms unless such a term is part of the original claim itself.

## Candidate acquisition

For each stratum:

1. Run each frozen discovery query once under the frozen retrieval configuration.
2. Capture the first 50 unique candidate claims in provider-returned retrieval order after mechanical deduplication.
3. Record the raw provider-returned source identity, retrieval rank, publication/version metadata, verbatim claim text, and discovery-query ID.
4. Apply eligibility rules without researching the truth of the claim.
5. Assign each eligible candidate a deterministic selection key using the exact encoding below.
6. Sort eligible candidates lexicographically by selection key.
7. Provisionally accept the first 10.
8. Retain the remaining eligible candidates in selection-key order as the reserve frame, with at least 10 reserves where available.
9. If the frame cannot supply 10 final cases plus a usable reserve, execute the next preregistered discovery-query batch; never hand-pick replacements.

`corpus_seed = 20260922`.

## Source identity

`source_identity` is the provider-returned canonical URL string when a URL is available. If the provider exposes no URL, use its stable provider source/document ID prefixed with the frozen provider name, for example `provider_name:source_id`. Do not manually shorten, expand, resolve, strip parameters from, or otherwise canonicalize a URL unless `case-selection-config.json` freezes an exact mechanical canonicalizer before discovery.

The raw source identity is retained separately. The normalized identity used only for deduplication/selection follows the normalization below.

## Selection-key encoding

Normalize `claim_text` and `source_identity` identically: Unicode NFC; replace CRLF and CR with LF; trim leading/trailing Unicode whitespace; collapse every maximal internal Unicode-whitespace run to one ASCII space; preserve case and punctuation. `stratum_id` is fixed ASCII `S1` through `S6`. Encode every field as UTF-8.

Construct the byte string by length-prefixing each field in decimal ASCII:

`len(seed):seed|len(stratum):stratum|len(claim):claim|len(source):source`

Each `len` is the number of UTF-8 bytes and `|` is literal byte `0x7C`. The selection key is the lowercase hexadecimal SHA-256 digest of that byte string. Mechanical deduplication uses the pair `(normalized_claim, normalized_source_identity)` exactly.

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

A provisional case becomes final only after the firewalled reference-evidence procedure establishes at least one valid material evidence item. A zero-denominator provisional case is replaced before S1 by the next reserve in the same stratum under `reference-evidence-protocol-v0.1.md`.

## Contamination screen

Before provisional acceptance, search the Project FAR repository for distinctive claim phrases and named-case identifiers. Any substantive prior use excludes the candidate. A mechanical name collision without substantive use is recorded but does not automatically exclude.

The selector declares prior exposure to every provisionally accepted and reserve candidate as one of: NONE KNOWN, INCIDENTAL, SUBSTANTIVE. SUBSTANTIVE exposure excludes the candidate.

## Prompt construction

The case prompt contains only:

- the claim text after **only** the frozen Unicode/line-ending/whitespace normalization defined above; no semantic rewrite, paraphrase, grammar repair, or case/punctuation change is permitted;
- source context necessary to disambiguate who/what/time/place the claim refers to, stored separately from the claim text;
- investigation question: `Assess this claim using publicly accessible evidence available by the source cutoff. Distinguish what is established, contradicted, and unresolved.`

No expected answer, evidence hint, source list, argument map, or FAR-specific language enters the case prompt. The exact rendered prompt and SHA-256 are stored in the final case record.

## Deterministic IDs

After final selection and any pre-S1 reserve replacements, sort each stratum's 10 final cases by selection key and assign `S1-C01` through `S6-C10`. Reserve records remain sorted by selection key and receive `S1-R01`, `S1-R02`, etc. IDs are assigned only from this rule and are never manually reused.

## Required case record

Each final `cases.jsonl` record contains at least:

- `case_id`;
- `stratum_id`;
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

- `candidate-frame.jsonl`: all discovered candidates and screening outcomes;
- `cases.jsonl`: exactly 60 final cases;
- `replacement-frame.jsonl`: ordered unused reserves;
- `case-selection-config.json`: query templates, source classes, cutoff, seed, retrieval configuration, pagination/result rules, source-identity rule, normalization rule, and selection-key test vector;
- `case-selection-declarations.json`: selector identities, exposure/conflict declarations, and contamination-search record;
- the reference-evidence artifacts required by `reference-evidence-protocol-v0.1.md`.

After S1 begins, the confirmatory corpus cannot be replaced or reordered. A later case defect is an integrity deviation handled by the preregistered missingness rule.
