# Comparative Representation Cost Model v1.0

## Purpose

This standard measures the full burden required for a vocabulary to preserve a frozen source system. It prevents a candidate from appearing simple by relocating commitments into derived constructs, metadata, compilers, verifiers, hidden state, or external interpreters.

## Separation of costs

Vocabulary cost and representation cost must remain distinct.

### Vocabulary cost

- `A_used`: supplied primitive categories actually used;
- `A_required`: supplied primitive categories judged necessary for the mapping;
- primitive semantics and admissibility assumptions.

### Representation cost

- `D`: derived machinery;
- `O`: explicit operations and transition rules;
- `L`: semantic description length;
- `H`: hidden or auxiliary state;
- `I`: external interpreter machinery;
- `E`: exceptions and case-specific patches;
- `J`: adjudication and ambiguity policies;
- `T`: trace and provenance burden.

No single scalar total is authoritative by default.

## Metric definitions

### Derived machinery (`D`)

Count distinct derived entity types, relation types, state constructs, transition schemas, helper predicates, macros, and compilation-only constructs required for preservation.

### Operations (`O`)

Count distinct operational clauses required to produce, modify, validate, or terminate system states. Repeated instances of one schema are reported separately from schema count.

### Semantic description length (`L`)

Count normalized declarations, constraints, transition clauses, preservation conditions, and interpretation rules. Formatting, comments, and arbitrary naming do not count.

### Hidden state (`H`)

Count state required for correct behavior that is not visible in the declared candidate representation. Hidden state is presumptively disallowed unless preregistered and charged.

### External interpreter (`I`)

Record all external code, runtime conventions, semantic libraries, or human interpretation required to make the representation operational. General-purpose capability does not make this cost zero.

### Exceptions (`E`)

Count domain-specific patches, one-off rules, special cases, and source-specific repairs.

### Adjudication (`J`)

Record policies and human judgments needed to resolve ambiguity, canonicalization, equivalence, or scoring.

### Trace burden (`T`)

Measure the size and structure of provenance, lowering traces, proof objects, and history artifacts needed to verify preservation.

## Canonicalization

Before counting, mappings must be normalized over:

- entity types;
- relation types;
- state variables;
- transition schemas;
- admissibility conditions;
- historical constraints;
- termination rules;
- interpretation clauses;
- external assumptions.

Canonicalization may remove syntactic duplication but may not merge distinct commitments.

## Pareto comparison

Candidate X dominates candidate Y only when:

1. preservation for X is no worse than Y on every registered dimension;
2. vocabulary cost for X is no greater than Y;
3. each of `D`, `O`, `L`, `H`, `I`, `E`, `J`, and `T` is no greater for X;
4. at least one comparison is strictly better.

Otherwise the result is a tradeoff or incomparability, not a win.

## Tolerances

Any tolerance for measurement noise must be preregistered by metric. Tolerances may not be introduced after candidate values are known.

## Required reporting

For every evaluator mapping, report:

- preservation vector;
- `A_used` and `A_required`;
- `D`, `O`, `L`, `H`, `I`, `E`, `J`, and `T`;
- unresolved counting disputes;
- canonicalization decisions;
- sensitivity to alternate reasonable counts.

Report the full mapping distribution. The least favorable resolved preservation value remains the primary conservative value; Unknown remains unresolved.

## Prohibited shortcuts

- primitive count alone must not be called simplicity;
- generated code must not be excluded merely because it is automated;
- shared libraries must not be treated as free when candidate behavior depends on them;
- hidden state must not be renamed provenance or metadata to avoid counting;
- human interpretation must not be omitted from cost;
- tradeoffs must not be reported as dominance.

## Permitted conclusions

The model supports bounded comparative economy and Pareto claims only within the frozen contract, mappings, canonicalization rules, and tested alternatives. It does not establish global minimality without a broader alternative-vocabulary search.