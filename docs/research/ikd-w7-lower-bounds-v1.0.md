# IKD-W7: Conditional RCCD Lower Bounds

## Decisive question

Can any faithful effective representation of the defined reasoning class avoid encoding RCCD-equivalent commitments?

## Formal scope

Let **C** be effectively describable systems that maintain distinguishable commitments, permit constrained commitment or state change, preserve grounds or dependencies relevant to revision, and support finite recovery queries over their histories.

Let **P** require preservation of commitment content, admissible evolution, dependency-sensitive revision, supersession and historical identity, and uniform finite recovery of those distinctions.

Let **E** contain finite or recursively presented representations with effective construction and one uniform terminating recovery method for every registered finite query. Source-specific hidden decoders, future-information oracles, unrestricted interpreters, and uncharged schedulers or proof machinery are excluded.

The preservation contract is stated in terms of reasoning facts, not RCCD labels. This prevents the lower-bound result from assuming the target vocabulary in advance.

## Component lower bounds

### R1: Recoverable commitments

Construct two systems with the same states and transition graph but different commitment content at a reachable configuration. A transition-only representation identifies them, but the required content query separates them. Therefore every P-faithful representation in E must encode enough information to recover commitment content.

### R2: Constrained evolution

Construct two systems with the same states and realized trace but different permitted next-step sets. State-only and trace-only representations identify them, while the admissibility query separates them. Therefore every P-faithful representation in E must encode constraints equivalent to permitted evolution.

### R3: Dependency-sensitive revision

Construct two systems with the same conclusion but different grounds. Defeat one ground. The required revisions differ. Conclusion-only representations identify the systems before defeat, while the revision query separates them. Therefore every P-faithful representation in E must encode grounds or equivalent dependency structure.

### R4: Historical identity

Construct two systems with the same current visible commitments but different supersession histories that constrain later revision differently. Current-state-only representations identify them, while historical and future-admissibility queries separate them. Therefore every P-faithful representation in E must encode historical identity and supersession information.

### R5: Uniform bounded recovery

Compare a uniformly effective representation family with a source-indexed oracle family that matches sampled behavior. Only the former supplies one terminating representation-independent method for every registered finite query. Finite samples identify the families, but the uniform-recovery obligation separates them. Therefore uniform effective recovery is a necessary admissibility condition for representations counted within E.

## Equivalent reintroduction

A basis may omit an RCCD component from its declared primitive vocabulary. That does not evade the lower bound if the separating query is recovered through a decoder, scheduler, proof object, adapter, canonicalizer, lookup table, or synthesis procedure. Such machinery reintroduces an equivalent distinction and is charged.

## Joint result

For C, P, and E as defined above, every faithful representation requires commitments equivalent to RCCD components R1–R5.

This converts the W6 search result into conditional impossibility arguments. It does not establish unrestricted necessity across every possible definition of reasoning, every preservation standard, or non-effective representations.

## Next step

W8 must recompute the Pareto and commitment frontier. It must determine whether FARA, LTS-PROV, and COALG-DYN are bidirectionally reconstructible realizations of RCCD, whether any contains an additional essential commitment, whether RCCD can be reduced further, or whether an incomparable kernel survives.
