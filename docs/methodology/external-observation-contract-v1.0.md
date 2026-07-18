# External Observation Contract v1.0

## Purpose

This standard defines the source-facing contract against which every candidate vocabulary is evaluated in a confirmatory comparative-representation experiment.

The contract must describe the investigated system independently of FAR, FARO, FARA, any competing vocabulary, and any compiler or verifier implementation. It exists to prevent a candidate vocabulary from defining success by construction.

## Governing rule

No confirmatory mapping may begin until the external observation contract is frozen.

The contract must be written from source evidence and observable commitments. Candidate-native terminology may appear only in later mappings.

## Required contents

Each contract must register:

1. source identity and version;
2. admissible source evidence;
3. entities and externally distinguishable types;
4. relations and dependency distinctions;
5. state variables and permitted values;
6. transition schemas;
7. admissibility conditions;
8. ordinary inference events;
9. rule, policy, or interpretation modification events;
10. historical and provenance constraints;
11. termination or continuation conditions;
12. uncertainty and unresolved source interpretation;
13. observables that must survive representation;
14. forbidden mergers or omissions;
15. permitted abstractions;
16. failure effects for each omitted distinction.

## Preservation dimensions

Every mapping is evaluated on:

- structural preservation;
- semantic preservation;
- operational preservation;
- dependency preservation;
- information preservation;
- historical preservation.

Allowed values are Pass, Partial, Fail, and Unknown. Unknown is unresolved and must not be ranked between Partial and Fail.

## Behavioral and commitment equivalence

Behavioral equivalence means two representations reproduce the same registered observable outputs under the tested inputs.

Commitment equivalence additionally requires preservation of registered ontology, dependency, state, admissibility, provenance, and historical commitments.

Behavioral equivalence alone is insufficient when the contract protects internal distinctions. A lookup table, hidden interpreter, or output-equivalent substitute may therefore reproduce outputs while failing commitment equivalence.

## Canonical comparison boundary

Canonicalization may normalize formatting, names, ordering, and mechanically equivalent syntax. It must not erase differences in:

- entity or relation types;
- hidden state;
- transition authority;
- admissibility conditions;
- historical dependencies;
- semantic commitments;
- external interpreter requirements;
- exception policies.

Two mappings may be merged as equivalent only when both behavioral and commitment-equivalence criteria are met.

## Freeze and amendment policy

The frozen contract receives a version identifier, commit SHA, and content digest before candidate construction.

A material amendment after candidate exposure creates a new experiment version. The prior experiment remains recorded and is not silently repaired.

Nonmaterial corrections must be listed in an amendment log and justified as incapable of changing scoring or candidate construction.

## Independence declaration

The contract package must identify:

- contract authors;
- source-system experts consulted;
- candidate-vocabulary affiliations;
- prior access to candidate mappings;
- conflicts of interest;
- whether an independent source reviewer approved the contract.

## Required failure conditions

The experiment must fail or remain unresolved when:

- the contract uses candidate-native categories to define the source;
- material source evidence is unavailable;
- protected distinctions are changed after mappings are visible;
- candidate mappings are scored against different contracts;
- unresolved source interpretations are forced into favorable conclusions;
- output equivalence is substituted for commitment equivalence without preregistered justification.

## Required artifact layout

Each confirmatory experiment should contain:

```text
observation-contract/
  contract.md
  contract.json
  source-manifest.yaml
  protected-distinctions.yaml
  amendment-log.md
  freeze-record.json
```

## Permitted conclusions

Passing this contract supports only preservation within the frozen system and tested scope. It does not by itself establish universality, necessity, minimality, superiority, or independent replication.