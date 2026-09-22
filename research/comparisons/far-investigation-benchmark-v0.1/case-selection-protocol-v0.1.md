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

Each stratum contributes exactly 10 accepted cases.

For every stratum, the selector constructs a chronological candidate frame from public sources published before the frozen source cutoff. Candidate discovery must use the same frozen query templates and source classes for the whole stratum. The selector records every candidate encountered before eligibility screening, including rejected candidates.

The selector may not search for examples described as "bad reasoning", "misinformation", "fallacy", "debunked", "false", "hoax", "fact check", or equivalent outcome-bearing terms unless such a term is part of the original claim itself.

## Candidate acquisition

For each stratum:

1. Run each frozen discovery query once under the frozen retrieval configuration.
2. Capture the first 50 unique candidate claims in retrieval order after mechanical deduplication.
3. Record discovery URL/source identity, retrieval rank, publication date, verbatim claim text, and discovery-query ID.
4. Apply eligibility rules without researching the truth of the claim.
5. Assign each eligible candidate a deterministic selection key using the exact encoding below.
6. Sort eligible candidates lexicographically by selection key.
7. Accept the first 10.
8. Retain the next 10 eligible candidates as ordered replacements.
9. If fewer than 20 are eligible, execute the next preregistered discovery-query batch; never hand-pick replacements.

`corpus_seed = 20260922`.

### Selection-key encoding

Normalize \`claim_text\` and \`source_identity\` identically: Unicode NFC; replace CRLF and CR with LF; trim leading/trailing Unicode whitespace; collapse every maximal internal Unicode-whitespace run to one ASCII space; preserve case and punctuation. \`stratum_id\` is the fixed ASCII identifier \`S1\` through \`S6\`. Encode every field as UTF-8.

Construct the byte string by length-prefixing each field in decimal ASCII: \`len(seed):seed|len(stratum):stratum|len(claim):claim|len(source):source\`, where each \`len\` is the number of UTF-8 bytes and \`|\` is literal byte 0x7C. The selection key is the lowercase hexadecimal SHA-256 digest of that byte string. Mechanical deduplication uses the pair \`(normalized_claim, normalized_source_identity)\` exactly. The freeze configuration must contain a test vector generated from this rule before discovery begins.

## Eligibility screen

A case is eligible only when all are YES:

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

## Contamination screen

Before acceptance, search the Project FAR repository for distinctive claim phrases and named-case identifiers. Any substantive prior use excludes the case. A mechanical name collision without substantive use is recorded but does not automatically exclude.

The selector must declare prior exposure to each accepted case as one of: NONE KNOWN, INCIDENTAL, SUBSTANTIVE. SUBSTANTIVE exposure excludes the case.

## Prompt construction

The case prompt contains only:

- verbatim or minimally normalized claim;
- source context necessary to disambiguate who/what/time/place the claim refers to;
- investigation question: "Assess this claim using publicly accessible evidence available by the source cutoff. Distinguish what is established, contradicted, and unresolved."

No expected answer, evidence hints, source list, argument map, or FAR-specific language enters the case prompt.

## Freeze artifacts

Before any condition run:

- `candidate-frame.jsonl`: all discovered candidates and screening outcomes;
- `cases.jsonl`: 60 selected cases;
- `replacement-frame.jsonl`: ordered reserve cases;
- `case-selection-config.json`: query templates, source classes, cutoff, seed, retrieval configuration;
- `case-selection-declarations.json`: selector exposure/conflict declarations;
- hashes for all five artifacts.

After freeze, a selected case can be replaced only for a preregistered integrity reason. Replacement uses the next eligible reserve in the same stratum and is logged before condition identity is inspected.
