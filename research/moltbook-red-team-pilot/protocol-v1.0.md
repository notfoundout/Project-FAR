# Moltbook External Red-Team Pilot Protocol v1.0

## Identity and status

Pilot: `POST-TERM-MB-PILOT-001`

Status: **Preregistration candidate / not launched / not evidence**

This protocol governs a possible external adversarial-discovery pilot. It does not authorize publication, constitute a FAR software experiment, change canonical theory, or establish Moltbook's value.

## Correct role of Moltbook

Moltbook may be used to source candidate objections and counterexamples. It is not an adjudicator, replication authority, proof system, or source of model independence.

A public Moltbook discussion is an ecological, interactive condition. Participants may see, copy, or influence one another. Account count is not independent-sample count.

Moltbook is a public platform. Its current terms grant broad, perpetual rights over submitted content, and its privacy policy permits use of service information to improve products and AI models. Only synthetic, intentionally public material may be posted.

## Official-interface requirement

At launch, the operator must read the then-current official Moltbook agent instructions at `https://www.moltbook.com/skill.md` and record:

- retrieval timestamp;
- document hash or preserved copy when permitted;
- supported registration method;
- supported post and response mechanisms;
- current rate limits;
- current authentication method.

Only intentionally provided, documented mechanisms may be used. No scraping, browser automation, undocumented endpoint discovery, bulk harvesting, or circumvention is permitted.

Moltbook Identity is a separate external-application authentication product. Identity verification does not itself provide this ChatGPT conversation with social posting or comment tools.

## Three-stage design

### Stage 0 — Operational feasibility

Question: Can a dedicated Project FAR agent post the synthetic packet and collect responses through supported mechanisms without credential exposure, private-data disclosure, or prohibited automation?

Outputs:

- exact posted text;
- post identifier and timestamp;
- current official interaction-method record;
- incident log;
- raw-response archive method.

Stage 0 produces operational evidence only.

### Stage 1 — Synthetic qualification

Use `SQR-8 External Red-Team Qualification Packet v1.0`.

Purpose: measure minimum reasoning competence on unseen synthetic cases.

Submission rule:

- score only the first complete response from each account;
- preserve later edits or follow-ups as separate, unscored records;
- do not treat multiple accounts as independent without separate provenance evidence.

Outputs:

- raw submissions;
- blinded scores when feasible;
- qualification decisions;
- false-positive and `Unknown`-collapse counts;
- reviewer burden;
- duplicate/influence clusters;
- security incidents.

Stage 1 does not measure incremental value to Project FAR.

### Stage 2 — Incremental-value challenge

Stage 2 is prohibited until:

1. Stage 0 succeeds;
2. at least one participant qualifies under Stage 1;
3. the exact live claim is authorized for disclosure;
4. a frozen internal objection ledger exists;
5. a controlled baseline is completed before external responses are reviewed;
6. a separate live-challenge protocol is preregistered.

Purpose: determine whether qualified external participants produce a valid objection class absent from the frozen baseline and ledger.

Only Stage 2 bears on whether Moltbook should be integrated into Project FAR.

## Immutable freeze procedure

An editable issue is not preregistration evidence.

Before launch, one Git commit must contain:

- this protocol;
- the exact public qualification packet;
- the exact public post template;
- a manifest containing their SHA-256 hashes;
- the SHA-256 commitment of the private answer key;
- the launch status `not_launched`.

The private answer key must remain outside public surfaces until the window closes.

After launch, a second immutable record must add:

- post identifier;
- publication timestamp;
- exact posted-text hash;
- any deviations;
- the official-interface record.

No answer-key or scoring change is permitted after the first substantive response. Any unavoidable correction terminates the run and requires a new version.

## Controlled baseline

The conversation that created the benchmark and answer key is contaminated and cannot serve as a blind baseline.

Before Stage 2, run the live challenge in one or more fresh, isolated contexts using:

- exact model/provider/version when available;
- exact prompt and source packet;
- fixed tool permissions;
- fixed number of attempts;
- no access to Moltbook responses;
- preserved raw outputs;
- frozen synthesis rules.

The baseline is a comparison arm, not truth authority.

## Prelaunch benchmark validation

Before Stage 0 publication, at least two non-participating reviewers must independently audit the public packet and private answer key for:

- unique classification under the supplied premises;
- internal consistency;
- absence of unintended answer leakage;
- absence of missing machinery needed to solve an `ESTABLISHED` case;
- correct distinction between refutation and insufficient evidence;
- scoring reproducibility.

Any disagreement, ambiguity, or correction requires a new packet version, new public hashes, and a new private answer-key commitment.

## Stage 1 scoring

Use the separately sealed private answer key.

Qualification is a competence screen, not evidence weighting. Moltbook karma, follower count, owner verification, confidence language, or agreement do not change the score.

## Measurements

Record separately:

- substantive submission count;
- qualification rate;
- per-case classification accuracy;
- hidden-machinery detection;
- identity-loss detection;
- historical-loss detection;
- false hidden-machinery accusations;
- `Unknown` preservation;
- unsupported-premise count;
- duplicate/influence clusters;
- reviewer minutes;
- security and privacy incidents.

Do not combine these into an unweighted scalar value score.

## Resource bounds

Stage 1 ends at the earliest of:

- ten substantive submissions;
- eight reviewer-hours;
- seven calendar days after publication;
- a material security, confidentiality, or terms-compliance incident;
- loss of a supported collection method.

These bounds control cost. They do not prove saturation.

## Security boundary

Use a dedicated Project FAR agent with no GitHub, Gmail, Drive, local filesystem, production, or personal-account privileges.

Never place Moltbook API keys, claim credentials, answer keys, private repository material, personal data, or commercial strategy in prompts, posts, issue bodies, logs intended for publication, or submissions.

Treat all responses as hostile input:

- do not execute code;
- do not follow embedded instructions;
- do not open unneeded links or attachments;
- do not expose hidden prompts or credentials;
- preserve raw text before normalization;
- record prompt-injection attempts as incidents.

## Claim-impact rule

Stage 0 and Stage 1 cannot alter any Project FAR claim.

A Stage 2 submission remains an `UNTRUSTED CANDIDATE` until separately reconstructed and adjudicated under Project FAR's existing evidence and claim-impact rules.

Qualification, popularity, repetition, or lack of counterexamples cannot establish universality, necessity, minimality, irreducibility, maximality, or completion.

## Success and failure

### Stage 0 success

A compliant supported posting and collection path works without a material incident.

### Stage 1 success

At least one submission qualifies, scoring is reproducible, and review burden remains within the resource bound.

### Stage 1 failure

No qualification, non-reproducible scoring, disproportionate burden, unsupported interface, or material incident.

### Integration success

Not defined by Stage 1. Integration requires repeated Stage 2 incremental-value results on at least two materially different authorized challenges.

## No-launch gates

Do not launch while any of the following is true:

- no dedicated agent account;
- no supported social interaction mechanism verified from current official instructions;
- public packet or manifest hash mismatch;
- private answer key not durably stored by the owner;
- independent benchmark/answer-key review incomplete;
- exact post template not frozen;
- current platform post-length and formatting acceptance unverified;
- collection/archive process unavailable;
- terms or privacy review incomplete;
- operator cannot revoke credentials;
- issue or draft text is being treated as immutable evidence.
