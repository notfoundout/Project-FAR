# Public Sampling Design v1.2

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Design version: 1.2  
Design seed: `20260805`  
Supersedes: v1.1

## 1. Exact freeze

The exact bytes of `covering-array-v1.0.csv` and `pairwise-coverage-report-v1.0.csv` are frozen by SHA-256 in `freeze-manifest-v1.0.json` and enforced by `verify_sampling_design.py`. Semantic equivalence is not sufficient: a different array that preserves counts and pairwise coverage is a different design version.

## 2. Allocation and coverage

The design contains 24 development rows and 12 sealed validation rows. Validation is exactly six naturally occurring public and six de-identified operational cases. All 12 synthetic rows are development rows. The 36 objective-by-medium cells occur exactly once. All 434 declared cross-dimension level pairs are covered.

This is combinatorial coverage only. It is not statistical power, population representativeness, independence, dimension completeness, or universality.

## 3. Holdout boundary

Validation is profile-known and source-identity-hidden. Dimension profiles and allocation labels are public; exact source identities, bytes, packets, and mappings remain sealed. Validation cannot establish generalization to synthetic cases as a holdout class or to undisclosed dimension combinations.

## 4. Source selection

Source selection follows `source-selection-and-replacement-protocol-v1.0.md`. Curator discretion is replaced by a pre-frozen universe/query/order/stopping procedure, complete candidate logging, independent coding, deterministic matching, and immutable replacement chains.

## 5. Freeze conditions

A row remains uninstantiated until record-level identity, exact bytes, SHA-256, access note, eligibility, independent coding, candidate-log pointer, and replacement history exist. Synthetic rows additionally require complete generators/specifications and generated-byte hashes.

## 6. Execution state

The public array is exactly frozen. Cases are not instantiated. Source selection and Stage A remain blocked until the sacrificial operational pilot passes and the role/access package is operational.
