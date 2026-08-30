# PCA-W5 Native Concept Freeze v1.0

Status: **FROZEN BEFORE CONTROLLED FAR MAPPING**

Query freeze commit: `11a93ba0db812ec849aac9b136be5d5538a0b44e`

Freeze time: `2026-08-30T18:16:49Z`

This document records native concepts recovered from independently motivated literatures. It deliberately does not assign them to Project FAR schema fields.

## 1. Statistical experiments and decision risk

### Native objects

A statistical experiment is a parameter-indexed family of probability distributions. Comparison may allow a randomized transformation/Markov kernel from one experiment to another.

Le Cam deficiency quantifies how closely one experiment can reproduce another under such randomization. Its decision-theoretic meaning is expressed through bounded loss/risk: small deficiency permits procedures in one experiment to be matched by procedures in the other with uniformly small risk increase, subject to normalization conventions.

### Required declarations

A well-defined native comparison requires:
- the two experiments and common parameter indexing;
- the admitted randomization/procedure class;
- a probability-distance convention;
- the decision/loss class and its bound/normalization;
- directionality or symmetrization when a distance is wanted;
- an approximation threshold if a binary adequate/inadequate judgment is desired.

### Exact/zero boundary

Deficiency zero has a specific experiment-comparison meaning tied to exact randomization/information ordering. This is not evidence that an arbitrary zero-valued loss in another domain implies exact sufficiency.

## 2. Rate–distortion and relevance-sensitive compression

### Native objects

Shannon's formulation starts with a source distribution and a supplied nonnegative distortion function. Average distortion is probability-weighted over source/reproduction pairs. A tolerated distortion level is a constraint, and the rate–distortion function depends on the source and the chosen distortion function.

Information bottleneck replaces a fixed external distortion by a relevance-sensitive compression objective determined from a joint distribution involving a relevance variable.

### Required declarations

A well-defined native approximation requires:
- source/reproduction spaces;
- a distortion or relevance criterion;
- the source/joint probability law used for aggregation;
- an aggregation rule, classically expectation;
- a tolerated distortion/relevance level or equivalent tradeoff parameter;
- the admissible encoder/decoder/channel class.

### Exact/zero boundary

A generic nonnegative distortion need not separate distinct outcomes. A degenerate distortion can assign zero to distinct values, so zero expected distortion is not generically equivalent to exact equality. Separation must be established, not inferred from the word “distortion.”

## 3. Approximate behavioral/model relations

### Native objects

Girard and Pappas define approximate language inclusion, simulation, and bisimulation for metric transition systems, using a hierarchy of pseudometrics to quantify approximation quality. The output/observation metric and transition-system structure are part of the formulation.

### Required declarations

A well-defined native comparison requires:
- the system class and transition semantics;
- observation/output spaces;
- an observation metric;
- the chosen approximate relation/pseudometric;
- any tolerance used to turn the quantitative value into an acceptance judgment.

### Exact/zero boundary

Within the stated framework, the developed pseudometrics recover established exact relationships as zero sections. This is a framework-specific theorem, not a generic law of all approximate comparison functions.

## 4. Statistical learning and surrogate-risk calibration

### Native objects

A computationally convenient surrogate loss can differ from the target loss. Bartlett, Jordan, and McAuliffe establish quantitative relationships between surrogate excess risk and target 0–1 excess risk under calibration/Fisher-consistency conditions.

### Required declarations

A well-defined native claim requires:
- the target decision task and target loss;
- the surrogate loss;
- the hypothesis/decision class and probability model;
- the excess-risk notion;
- the calibration/consistency condition or transformation used to relate surrogate and target risks.

### Exact/zero boundary

Low or zero surrogate excess risk does not generically control the target risk absent the required calibration condition. The relationship is loss-specific.

## 5. Multiobjective optimization and preference/order structure

### Native objects

Multiobjective optimization studies several potentially conflicting or incommensurable objectives. Without added preference information, efficient/Pareto solutions form a set rather than a canonical single optimum. Scalarization converts a multiobjective problem into a scalar problem only after adding parameters such as weights, reference points, aspiration levels, or related preference information.

### Required declarations

A well-defined native cost comparison requires:
- the objective vector;
- the direction/order for each objective;
- the induced dominance/preorder/partial order;
- the feasible/candidate set;
- any scalarization and all of its parameters;
- the decision-maker preference information, if a most-preferred point is to be selected.

### Minimality and uniqueness

Pareto minimality is not the same as a least element. Multiple incomparable Pareto-minimal candidates can exist. A scalar optimum is preference/model dependent unless a canonical scalarization is independently justified.

## 6. Computational, statistical, and description-complexity resources

### Native objects

Chandrasekaran and Jordan explicitly study statistical quality under bounded computational resources and derive runtime-versus-data tradeoffs. Hansen and Yu's MDL treatment uses description length as a model-selection complexity criterion.

### Required declarations

A resource/cost statement must identify:
- the resource coordinate(s), such as time, space, data/sample count, communication, description length, or statistical risk;
- the units/model of computation or coding convention where relevant;
- the candidate set;
- the comparison order or tradeoff rule;
- any scalarization/preferences used to combine resource dimensions.

### Non-equivalence

The selected sources do not identify runtime, memory, sample complexity, communication, description length, and statistical risk as one natural scalar. Treating them as interchangeable would be an additional modeling choice.

## Cross-family frozen findings

The following are supported as **native-literature synthesis**, not as Project FAR theorems:

1. There is no source-backed basis in the selected literature for a universal approximation metric, loss, tolerance, aggregation rule, or scalar cost.
2. A metric is a special case; several native families use more general loss/risk/distortion/order structures.
3. Aggregation is substantive. Worst-case/supremum and probability-weighted expectation have different semantics.
4. A tolerance/acceptance threshold is distinct from the achieved discrepancy value.
5. Randomization is native and essential in statistical-experiment comparison; deterministic-only semantics would lose that structure.
6. Cost comparison can be genuinely partial. Pareto-minimal elements need not be unique or mutually comparable.
7. Scalarization imports additional preference parameters.
8. Zero approximation recovers exactness only under family-specific separation/equivalence conditions.
9. Adequacy and implementation/resource cost are separate questions.

## Frozen adversarial obligations for Stage D

Any later operational semantics must survive finite-explicit controls showing:

- **loss-choice dependence:** the same representation can pass under one declared loss and fail under another;
- **aggregation dependence:** the same pointwise losses can pass under an expectation and fail under a supremum;
- **reference-measure dependence:** expected loss can ignore zero-probability cases;
- **tolerance dependence:** changing only the threshold can change the classification;
- **zero-loss nonseparation:** a nonseparating loss can give zero despite distinct required outcomes;
- **randomization necessity:** a randomized decoder/kernel can satisfy a native experiment-comparison obligation where a deterministic class cannot;
- **Pareto incomparability:** two adequate candidates can be mutually incomparable under componentwise cost;
- **nonunique minimality:** multiple Pareto-minimal candidates can coexist;
- **scalarization dependence:** different declared weights/preferences can select different candidates;
- **exact boundary:** zero approximate loss may be promoted to exact only when the declared loss/aggregation supplies the needed separation;
- **missing-declaration failure:** approximate or cost-optimal status must be unavailable when any semantically required declaration is absent.

## What is not frozen as a result

This freeze does not establish:
- one universal operational approximation semantics;
- a single universal cost object;
- a unique minimum representation;
- empirical utility;
- computational tractability;
- external-investigator independence;
- novelty or priority.

Those questions remain downstream.
