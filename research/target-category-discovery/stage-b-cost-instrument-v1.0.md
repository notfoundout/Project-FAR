# Stage B Full-Cost Instrument v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`

## 1. Rule

A candidate may be compared only through the registered vector below. No scalar score, hidden weight, or informal “simplicity” judgment is permitted.

## 2. Cost vector

For a fixed frozen contract and implementation package:

- `P_count`: number of non-derivable primitive declarations.
- `P_bits`: UTF-8 byte length of canonical primitive declarations after fixed formatting.
- `D_count`: number of derived constructs used by the reconstruction.
- `D_bits`: UTF-8 byte length of canonical definitions of those constructs.
- `O_count`: number of distinct transformation or inference rules invoked.
- `O_bits`: UTF-8 byte length of canonical rule definitions.
- `H_bytes`: serialized bytes of hidden or auxiliary persistent state required at evaluation time.
- `I_bytes`: serialized bytes of external interpreter, executable, query, or lookup machinery not already counted.
- `E_count`: number of case-specific exceptions or escape hatches.
- `E_bits`: UTF-8 byte length of their canonical descriptions.
- `A_count`: number of ambiguity/adjudication policies needed for deterministic answers.
- `A_bits`: UTF-8 byte length of those policies.
- `R_steps`: median number of atomic reconstruction steps across registered questions.
- `R_minutes`: median blinded reviewer time in minutes, measured by monotonic clock.
- `S_bytes`: total canonical stored bytes required by the representation.
- `X_ms`: median execution time in milliseconds over 30 warm runs on the registered environment when execution is material.
- `M_bytes`: median peak resident memory over the same runs when execution is material.

A non-applicable coordinate is `NA`, not zero. Unknown measurement is `Unknown`.

## 3. Canonicalization

Text is UTF-8, LF line endings, Unicode NFC, no trailing whitespace, one terminal newline, and sorted declarations by stable identifier. JSON uses UTF-8, sorted keys, separators `(',', ':')`, and no insignificant whitespace. Executables are counted as exact distributed bytes.

Shared machinery is counted once per candidate package and separately amortized per case. Both totals are reported.

## 4. Measurement

Two blinded measurers independently produce every non-executable count. Disagreement is resolved only by locating the differing bytes or declarations; unresolved disagreement is `Unknown`.

Timing uses the same pinned environment, input corpus, warm-up count, run count, and measurement script for every candidate. Environment metadata and raw observations are retained.

Reviewer burden is measured on the same question order randomized from a frozen seed. Reviewers cannot know candidate identity where blinding is feasible.

## 5. Dominance

Candidate A Pareto-dominates B only when:

1. preservation and access constraints are equal or better;
2. every jointly applicable known cost coordinate for A is no worse than B;
3. at least one coordinate is strictly better;
4. neither candidate has an `Unknown` on a coordinate decisive to the claim.

`NA` coordinates are compared only when applicability matches. Tradeoffs yield `incomparable`, not victory.

## 6. Necessity and replacement

Removing an item establishes local necessity only with a paired witness: same remaining disclosed information, different correct frozen answer. An equal-or-lower-cost replacement defeats necessity of the original representation.

## 7. Prohibited scoring

Prohibited:

- unregistered composite scores;
- after-the-fact weights;
- excluding derived or executable machinery;
- calling metadata free;
- ignoring reviewer burden;
- treating visible field count as total cost;
- selecting only favorable coordinates.

A new cost coordinate or weighting rule requires a new version before validation reveal.
