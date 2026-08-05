# Source Selection and Replacement Protocol v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`

## 1. Preselection freeze

Before any final case is chosen, the custodian freezes for each source class:

- eligible repositories, archives, organizations, or operational record pools;
- inclusion and exclusion rules;
- exact search queries or database filters;
- retrieval start and end timestamps;
- result ordering;
- maximum pages/records inspected;
- deduplication rule;
- candidate identifier format;
- stopping rule;
- dimension-coding rubric;
- replacement rule.

The freeze is committed by the restricted-package format before selectors see final allocations.

## 2. Candidate enumeration

Every result encountered under the frozen procedure receives a candidate ID and immutable log entry before eligibility or coding is finalized. The log records source pointer, retrieval timestamp, query/filter, rank, duplicate relation, and disposition.

Selectors may not omit an encountered candidate from the log.

## 3. Independent functions

- Selector A enumerates candidates and applies objective eligibility rules without seeing row allocation.
- Coder B assigns dimension levels using the frozen rubric without seeing development/validation allocation.
- Matcher C applies the deterministic row-matching rule to eligible coded candidates.
- Custodian D holds the allocation map and performs the final blind assignment.

One person may fill multiple roles only for an explicitly internal pilot. The confirmatory 36-case program requires Selector A and Coder B to be distinct from the theory author and from each other.

## 4. Matching rule

For each row in ascending blind-ID order, select the lowest-ranked unused eligible candidate matching all seven levels. Rank is the frozen source-result order followed by stable candidate ID. No preference, convenience, familiarity, or desired outcome may override the rule.

When multiple pools feed one source class, pool precedence must be frozen.

## 5. Unfilled rows

If no candidate matches, record `unfilled`. Do not relax levels, broaden the pool, or invent a replacement after seeing other selections. A new pool or query requires a new source-selection version and a fresh candidate enumeration.

## 6. Exclusions

Exclude sources used to design Project FAR, RCCD, FARA, FARO, these protocols, the sampling dimensions, the adjudication codebook, or the cost instrument. Exclude sources that cannot be lawfully captured, cannot be frozen, lack a meaningful failure condition, or require unrestricted private mental state.

## 7. Replacement

A selected source may be replaced only for a preregistered reason: access loss, corruption, legal withdrawal, duplicate discovery, eligibility error, or coding error confirmed by independent review. The replacement is the next eligible unused candidate under the original ordering.

The original selection, reason, evidence, and replacement chain remain immutable.

## 8. Audit output

The restricted source-selection package contains:

- preselection freeze;
- complete candidate log;
- eligibility decisions;
- independent dimension codings;
- disagreement records;
- deterministic matching output;
- unfilled rows;
- replacements;
- conflict declarations;
- package commitment.

Only an aggregate commitment is public before reveal.
