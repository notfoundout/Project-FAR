# Validation and Challenge Protocol v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Execution: **blocked**

## 1. Pre-exposure freeze

Before the first development A1 run, the validation custodian must freeze and commit, in the restricted package:

- exactly 12 validation packet identities, bytes, hashes, allocation map, answer constraints, and scoring keys;
- exactly six challenge packet identities, bytes, hashes, class labels, answer constraints, and scoring keys;
- the exact A1, A2, and B1 prompt identities from `execution-prompts-v1.0.json`;
- the adjudication codebook, cost instrument, validation procedure, challenge procedure, stopping rules, and claim-impact rules.

Validation or challenge material constructed or altered after development exposure invalidates the version.

## 2. Validation set

The validation set is exactly the 12 rows labeled `Validation—sealed` in the frozen public covering array: six naturally occurring public cases and six de-identified operational cases. Allocation profiles are public; source identities and packet contents are sealed. The holdout is therefore profile-known and source-identity-hidden, not profile-blind.

Each validation case receives:

1. three context-isolated A1 runs using `TCD-A1-PROMPT-001`;
2. one A2 completeness arm using `TCD-A2-PROMPT-001` after A1 outputs are frozen;
3. adjudication under the frozen Stage A codebook;
4. B1 analysis using `TCD-B1-PROMPT-001` and the frozen cost instrument;
5. scoring against the development-frozen question ledger, relation graph, candidate bases, costs, and failure rules.

No validation result may add or repair a development question, structural item, cost rule, or scoring rule in place.

## 3. Validation scoring

A validation case is `PASS` only when all are true:

- every source-native objective-linked question required by the case is already represented in the frozen development ledger or is exactly derivable under a frozen equivalence rule;
- the frozen candidate basis reconstructs every required answer under the case access policy;
- no required machinery is hidden, unavailable, or excluded from cost;
- the case introduces no new failure predicate, required structural item, or decisive cost coordinate;
- adjudication contains no unresolved issue that could reverse the result.

A case is `FAIL` when any condition is false. It is `UNKNOWN` when required evidence or adjudication is insufficient. `UNKNOWN` is not a pass.

`held_out_adequacy_supported` may be reported only at 12/12 `PASS`. Any `FAIL` defeats that claim for the frozen version. Any `UNKNOWN` yields `held_out_adequacy_unresolved`. Results must also be reported separately for the six public and six operational cases.

Validation cannot establish population representativeness, synthetic-class transfer, undisclosed-profile transfer, external independence, universality, necessity, minimality, or canonicality.

## 4. Challenge set

The six frozen challenge classes are:

1. absent information versus an explicit negative assertion;
2. identical final output reached through materially different authorized paths;
3. radical lossless bundling, splitting, renaming, or serialization;
4. conflicting sources or rules with a valid `Unknown` outcome;
5. hidden dependence on an unavailable external oracle or environment;
6. a smaller alternative basis with equal registered behavior and no hidden machinery.

Each class has one sealed packet and scoring key frozen before development exposure. Challenge packets are revealed only after development synthesis, validation rules, candidate bases, costs, and scoring are frozen.

A challenge is `PASS` only when the frozen method preserves the required distinction, rejects the invalid construction, or retains the valid smaller/equivalent alternative exactly as required by its key. A missed distinction, false rejection, hidden repair, or post-reveal rule change is `FAIL`; insufficient evidence is `UNKNOWN`.

`challenge_resistance_supported` requires 6/6 `PASS`. Challenge success is adversarial resistance evidence only, not independent recurrence evidence.

## 5. Stopping and invalidation

Stop the program when all 24 development cases, 12 validation cases, and six challenges have completed under frozen rules, or immediately when a material contamination, access-control breach, source-freeze defect, prompt mismatch, adjudication departure, cost-rule change, or post-exposure packet change occurs.

A correction after exposure creates a new version and preserves the earlier failed or unresolved record.

## 6. Claim impact

Validation and challenge outcomes may support only the strongest registered bounded claim reached under the claim ladder. Named architecture comparison occurs after neutral outputs are frozen. No result automatically changes accepted theory.
