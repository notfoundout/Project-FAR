# Frozen merged-PR review findings

Source: `docs/audits/merged-pr-review-audit/raw-review-threads.json`

This report is fail-closed. A resolved GitHub thread is not labeled correctly resolved unless a manual evidence decision proves it.

## Summary

- Total review threads: 450
- `non_actionable`: 0
- `obsolete_after_later_changes`: 45
- `resolved_correctly`: 0
- `resolved_incorrectly`: 405
- `uncertain_manual_review_required`: 0
- `unresolved`: 0

## Findings

### PR12:PRRT_kwDOTH_vCM6OD6bR

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `research/validation/investigations/VI-002-primitive-minimality.md:1349`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891144
- Claim: **P1 Badge Do not mark VI-002 passed before required execution** This file's own methodology requires reconstructing every affected definition/document and verifying that VI-001 remains executable, but the completed result records no suc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR12:PRRT_kwDOTH_vCM6OD6bR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'research/validation/investigations/VI-002-primitive-minimality.md' (SHA-256 46933e607ba37e2ea72e84eefea584f3b7c250dc69437c57809bb35da220bb20).
  - Current repository evidence at 'research/validation/investigations/VI-002-primitive-minimality.md:1349': 'The current reduction study supports a provisional local result under the current Project FAR primitive basis and deletion-only standard. Global minimality remains unresolved.'.

### PR17:PRRT_kwDOTH_vCM6OR8-C

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-completion.md:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/17#discussion_r3521925204
- Claim: **P1 Badge Require completions to add missing limits** Because this obligation only covers sequences whose required limit is already represented by the proposed completion, a candidate can omit any problematic convergent sequence and sti...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR17:PRRT_kwDOTH_vCM6OR8-C found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/mathematics/definitions/evaluation-completion.md' (SHA-256 c16efcbcc604c0875e899a46da7f8d8a10ab9fe1562be133147f0044224fe903).
  - Current repository evidence at 'frameworks/FARE/mathematics/definitions/evaluation-completion.md:45': 'The criterion may be based on convergence, a Cauchy-like condition, refinement behavior, or another formally defined requirement.'.

### PR20:PRRT_kwDOTH_vCM6OTp-R

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `frameworks/FARE/mathematics/theorem-index.md:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/20#discussion_r3522541518
- Claim: **P1 Badge Keep theorem identifiers unique** These new index entries reuse 'MT-001' through 'MT-003' while the existing active proofs 'frameworks/FARE/mathematics/proofs/T001-identity-path-is-geodesic.md', 'T002-path-composition-preserve...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR20:PRRT_kwDOTH_vCM6OTp-R found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/mathematics/theorem-index.md' (SHA-256 03a41522047ece40be0f6f19c370938c9021e14c58e1002052aaab78ff48186f).
  - Current repository evidence at 'frameworks/FARE/mathematics/theorem-index.md:19': '| MT-003 | Path Composition Preserves Reachability | Accepted |'.

### PR22:PRRT_kwDOTH_vCM6OWe3V

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/CANONICAL_MAP.md:295`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/22#discussion_r3523523889
- Claim: **P1 Badge Restore removed canonical theory entries** This rewrite leaves the Theory section ending after 'Propositions', but the parent map also recorded canonical locations for Lemmas, Theorems, Conjectures, Proofs, FARO-specific defin...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR22:PRRT_kwDOTH_vCM6OWe3V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/CANONICAL_MAP.md' (SHA-256 9fae5238b7a853b517252f364f907623ab8729d92dd94b6aaf98194534f1b76e).
  - Current repository evidence at 'docs/CANONICAL_MAP.md:177': '- Comparative experiment registration: 'theory/evaluation/comparative-representation/experiment-registry.json' is the canonical registry for blinded comparative representation experiments. Legacy external-validation reports must not be recl'.

### PR67:PRRT_kwDOTH_vCM6OuqYN

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `examples/far/reasoning-systems/inconsistent-calculus.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162034
- Claim: **P1 Badge Use the accepted inconsistent-calculus classification** When 'tools/evaluate_reasoning_systems.py' evaluates this fixture, 'falsifies FAR' is mapped into 'candidate counterexample', so this line turns the inconsistent-calculus...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR67:PRRT_kwDOTH_vCM6OuqYN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'examples/far/reasoning-systems/inconsistent-calculus.far.yaml' (SHA-256 6408b5a975f69e52f028c3ace16fb42aba2a70e695a763501741673e24f86593).
  - Current repository evidence at 'examples/far/reasoning-systems/inconsistent-calculus.far.yaml:11': 'verdict: falsifies FAR'.

### PR67:PRRT_kwDOTH_vCM6OuqYV

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162043
- Claim: **P1 Badge Do not classify opaque intuition as a FAR falsification** With this verdict, the evaluator records the opaque-oracle fixture as a 'candidate counterexample', but the repository's existing scope test for private intuition with ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR67:PRRT_kwDOTH_vCM6OuqYV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml' (SHA-256 ccbb4980348bcedecc9d05a1bee815dc07073e3b0cb46b9946e4c8f178ac5bb8).
  - Current repository evidence at 'examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml:11': 'verdict: falsifies FAR'.

### PR67:PRRT_kwDOTH_vCM6OuqYa

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `examples/far/reasoning-systems/paradox.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162047
- Claim: **P1 Badge Keep paradox as representable boundary evidence** This verdict causes the paradox fixture to be counted as a 'candidate counterexample', but 'theory/tests/falsification-tests-advanced.md' Test A3 explicitly says FAR can repres...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR67:PRRT_kwDOTH_vCM6OuqYa found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'examples/far/reasoning-systems/paradox.far.yaml' (SHA-256 d0ab59720114860d3b9424d3540d38a6e331d03ce70c4e1e0a805a7cf1c55b8d).
  - Current repository evidence at 'examples/far/reasoning-systems/paradox.far.yaml:11': 'verdict: falsifies FAR'.

### PR70:PRRT_kwDOTH_vCM6OvPip

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/releases/project-far-v0.2.0.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/70#discussion_r3532377341
- Claim: **P1 Badge Declare the release artifact status** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to possess exactly one status ('Accepted', 'Res...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR70:PRRT_kwDOTH_vCM6OvPip found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/releases/project-far-v0.2.0.md' (SHA-256 d8e9483115dec90575b6e2c73a00124b9d79f1bb4e62a1108f5e93309068fc65).
  - Current repository evidence at 'docs/releases/project-far-v0.2.0.md:1': '# Project FAR v0.2.0'.

### PR87:PRRT_kwDOTH_vCM6PG65I

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/update_readme_dashboard.py:86`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/87#discussion_r3541030301
- Claim: **P1 Badge Exclude interpreter caches from generated repository indexes** When a developer has Python bytecode under 'tools/__pycache__', this recursive scan indexes those local cache files; the committed 'docs/planning/repository-index....
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR87:PRRT_kwDOTH_vCM6PG65I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/update_readme_dashboard.py' (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at 'tools/update_readme_dashboard.py:68': "if __name__=='__main__': main()".

### PR95:PRRT_kwDOTH_vCM6PWt_O

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-validation-report.md:131`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/95#discussion_r3546692054
- Claim: **P1 Badge Apply the collective sufficiency criterion** In contexts where normativity, semantics, or validity are supplied by FARA or later artifacts, this marks AX-001 as a sufficiency **FAIL** using a stricter test than the repository ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR95:PRRT_kwDOTH_vCM6PWt_O found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-validation-report.md' (SHA-256 b14995231694ccbf131a10e0d663029db0a79a923752f6bf38a89f31f1a2315f).
  - Current repository evidence at 'docs/reports/foundation-validation-report.md:131': '| Sufficiency | FAIL | Operation alone does not distinguish reasoning from arbitrary manipulation and does not supply normativity, semantic content, inferential relevance, or validity. |'.

### PR96:PRRT_kwDOTH_vCM6PXUsp

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-circularity-investigation.md:394`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/96#discussion_r3546909128
- Claim: **P1 Badge Demote AX-001 when the review concludes inconclusive** This line explicitly decides not to revise AX-001, but the same report records that AX-001's provisional result is stronger than the evidence warrants and is in tension wi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR96:PRRT_kwDOTH_vCM6PXUsp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-circularity-investigation.md' (SHA-256 b968b115ec6e7ca126cb58a682b8c8460e615482d2326eb2bcb6137e6e016689).
  - Current repository evidence at 'docs/reports/ax001-circularity-investigation.md:394': 'No AX-001 revision is applied in this PR.'.

### PR99:PRRT_kwDOTH_vCM6PXsa1

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-stability-review.md:75`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/99#discussion_r3547041586
- Claim: **P1 Badge Do not pass sufficiency via downstream theory** When this gate is used to authorize L-001, resolving AX-001 sufficiency by assigning admissibility, representation, interpretation, structure, calculus, trace, and warrant to sur...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR99:PRRT_kwDOTH_vCM6PXsa1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-stability-review.md' (SHA-256 e5c8ab51daba59132a57296c714c595566d39afb5a4356e00eff50d4a72de42c).
  - Current repository evidence at 'docs/reports/ax001-stability-review.md:75': 'AX-001 now explicitly records that Operation alone does not supply normativity, semantics, validity, or warrant. This resolves the prior sufficiency pressure as a blocking issue because the primitive is no longer presented as sufficient by '.

### PR100:PRRT_kwDOTH_vCM6PX2kN

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/appendices/l001-blind-formalization-raw.md:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/100#discussion_r3547099165
- Claim: **P1 Badge Use the canonical D-REP in the blind inputs** This blind prompt defines 'representation' as an explicit artifact/structure/expression/object made available for Project FAR analysis, but the canonical D-REP in 'theory/definitio...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR100:PRRT_kwDOTH_vCM6PX2kN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/appendices/l001-blind-formalization-raw.md' (SHA-256 b52017245b3a999538795ba944c335a9ca898a3335afd6bda3572d8bd20c5175).
  - Current repository evidence at 'docs/reports/appendices/l001-blind-formalization-raw.md:20': '4. Accepted term: representation means an explicit artifact, structure, expression, or object by which reasoning content, state, or role is made available for analysis in Project FAR.'.

### PR100:PRRT_kwDOTH_vCM6PX2kS

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/appendices/l001-adversarial-review-raw.md:148`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/100#discussion_r3547099172
- Claim: **P1 Badge Restore the omitted adversarial objections** Under the 'Complete output' section, the raw adversarial transcript jumps from Objection 2 to Objection 11, while the final defeat table later lists omitted objections such as categ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR100:PRRT_kwDOTH_vCM6PX2kS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/appendices/l001-adversarial-review-raw.md' (SHA-256 7ec1db88534259985c79799260917d2dd8a76c50d2f1e468689e99cc9c4b30bf).
  - Current repository evidence at 'docs/reports/appendices/l001-adversarial-review-raw.md:148': '## Objection 11: “Operation” is not needed and may introduce dependency confusion'.

### PR107:PRRT_kwDOTH_vCM6Paisx

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/lemmas/core-lemmas.md:85`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/107#discussion_r3548071734
- Claim: **P1 Badge Propagate L-007's new preconditions downstream** The revised L-007 is now only applicable when each step decreases a finite unresolved-item measure and introduces no new unresolved item, but T-009 still declares a dependency o...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR107:PRRT_kwDOTH_vCM6Paisx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/lemmas/core-lemmas.md' (SHA-256 fce9744c6d4efa0b23baacc417eae5eb5b952a3973939be6cf5f698998d138f9).
  - Current repository evidence at 'theory/lemmas/core-lemmas.md:85': 'A normalization procedure over a finite FAR representation terminates if each normalization step strictly decreases a finite unresolved-item measure for ordering, labeling, and redundancy and introduces no new unresolved item.'.

### PR114:PRRT_kwDOTH_vCM6PdHTG

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/t005-validation-report.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/114#discussion_r3549023686
- Claim: **P1 Badge Stop acceptance until dependencies are validated** When this report is used as the acceptance record for T-005, the 'ACCEPT' recommendation skips required upstream validation: the report later lists L-008 and T-003 as logicall...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR114:PRRT_kwDOTH_vCM6PdHTG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/t005-validation-report.md' (SHA-256 5aa97968ca46c6c40e7e6b7df698fd43bfb50372ae582d47a2d2b7021f03b5ed).
  - Current repository evidence at 'docs/reports/t005-validation-report.md:5': 'Final recommendation: ACCEPT.'.

### PR116:PRRT_kwDOTH_vCM6PdVsa

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/t008-validation-report.md:151`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/116#discussion_r3549107828
- Claim: **P1 Badge Resolve the remaining preservation premise** When a shared required-role inventory pairs roles but does not itself define those occupants as preserving structural relation, assigned meaning, admissibility, and trace order, the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR116:PRRT_kwDOTH_vCM6PdVsa found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/t008-validation-report.md' (SHA-256 f0d2806c2376fabd3f8306c1592cf4745ee15b9f354a78fed37c2a0fba05bf24).
  - Current repository evidence at 'docs/reports/t008-validation-report.md:151': 'No open question blocks T-008 after revision.'.

### PR118:PRRT_kwDOTH_vCM6Pd0Mn

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-010.proof.yaml:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283458
- Claim: **P1 Badge Use a supported proof-step rule** With this new 'prior_proposition' rule, the proof object no longer satisfies the repository's proof-object schema: 'tools/verify_theory.py' and 'tools/check_proof_object.py' only allow the rul...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-010.proof.yaml' (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at 'theory/proof-objects/T-010.proof.yaml:46': 'rule: prior_proposition'.

### PR118:PRRT_kwDOTH_vCM6Pd0Mr

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-010.proof.yaml:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283463
- Claim: **P1 Badge Cite the completeness definition by a resolvable ID** This premise source is not resolvable by the strict proof-object checker, which accepts metadata IDs/aliases such as 'DEF-038' or approved base sources, not definition titl...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-010.proof.yaml' (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at 'theory/proof-objects/T-010.proof.yaml:21': 'source: DEF-038'.

### PR118:PRRT_kwDOTH_vCM6Pd0Mv

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-010.proof.yaml:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283467
- Claim: **P1 Badge Make the conclusion match a proved step** The new conclusion text no longer exactly matches any proof step statement after 's7' was removed and 's6' kept a shorter statement. Both 'validate_required_proof_objects()' in 'tools/...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mv found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-010.proof.yaml' (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at 'theory/proof-objects/T-010.proof.yaml:56': 'conclusion: Given a FAR representation that is complete relative to a reconstruction objective, scope, and specified interpretation, the explicitly represented reasoning process can be reconstructed from its represented initial state, struc'.

### PR119:PRRT_kwDOTH_vCM6Pd8Rn

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/proofs/T-011-conservative-extension.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/119#discussion_r3549330195
- Claim: **P1 Badge Preserve proposition and lemma inputs before claiming proof preservation** The revised condition still only freezes axioms and theorem statements/dependencies, but established core proofs also use lemmas and propositions: for ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR119:PRRT_kwDOTH_vCM6Pd8Rn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proofs/T-011-conservative-extension.md' (SHA-256 7c88bcff6ef4166a9482df35eeb03e45a1fc484487aadd9a8ba22f34112f4e0e).
  - Current repository evidence at 'theory/proofs/T-011-conservative-extension.md:11': 'If an extension 'E' of Project FAR introduces no new primitive, adds only terms or machinery definable from existing primitives or established derived concepts, alters no canonical definition, changes no established axiom or theorem stateme'.

### PR124:PRRT_kwDOTH_vCM6Pq9Nm

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-final-consolidation-report.md:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/124#discussion_r3554005850
- Claim: **P1 Badge Keep status inconsistent until backfills avoid downstream use** This status is not supported by the new backfill artifacts: the reports/raw appendices validate earlier artifacts while supplying 'P-001 through P-008' and 'T-001...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR124:PRRT_kwDOTH_vCM6Pq9Nm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-final-consolidation-report.md' (SHA-256 beb28b9078185e1e73f8a7fec2d10ab204763300019242bd8e887d598bed7d21).
  - Current repository evidence at 'docs/reports/foundation-final-consolidation-report.md:9': 'Final status: **FOUNDATION CONSISTENT**.'.

### PR132:PRRT_kwDOTH_vCM6PubMj

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/l008-validation-report.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/132#discussion_r3555277773
- Claim: **P1 Badge Exclude L-008-dependent T-005 from the foundation set** When this report is used as validation evidence for L-008, the stated supplied foundation includes T-001 through T-012; in this repo that includes T-005, whose metadata a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR132:PRRT_kwDOTH_vCM6PubMj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/l008-validation-report.md' (SHA-256 ad66f9b1f4e2d61d4bf18c6eaca8064334e829b3a4064e56117d05f2445a2195).
  - Current repository evidence at 'docs/reports/l008-validation-report.md:11': 'This validation treats the supplied accepted foundation as accepted: AX-001; accepted canonical definitions; L-001 through L-007; P-001 through P-008; T-001 through T-012; Isolation Classification doctrine; Foundation Consistency Audit; Can'.

### PR139:PRRT_kwDOTH_vCM6PvDtm

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/minimality-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/139#discussion_r3555510614
- Claim: **P1 Badge Include A1–A5 in the minimality inventory** This inventory says the audit covers the accepted foundation, but it omits the five established axiom records A1–A5: both 'theory/metadata/generated-axiom-index.md' and the prior can...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR139:PRRT_kwDOTH_vCM6PvDtm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/minimality-audit.md' (SHA-256 724acfe3791c7ea25ac49b02b9853777320996eeedd8ab3a3f224aaa9305e258).
  - Current repository evidence at 'docs/reports/minimality-audit.md:3': 'This Phase 1 Step 9 Minimality Audit is audit-only. It consumes the accepted foundation and prior audits without revalidating theorem proofs or introducing new mathematics. The audit covers 126 accepted artifacts: 5 primitives, 89 canonical'.

### PR150:PRRT_kwDOTH_vCM6PxKNR

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/reports/external-validation/ai-reasoning/campaign-summary.md:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/150#discussion_r3556281887
- Claim: **P1 Badge Record falsification evidence before passing the campaign** When this summary is used as the Phase 2 validation record, the claim that the campaign falsified representability by testing these AI-specific pressures is not repro...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR150:PRRT_kwDOTH_vCM6PxKNR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/external-validation/ai-reasoning/campaign-summary.md' (SHA-256 55f9a4057636a09f3f4856421e670ab5da49fab5f232bc23f242f44f19e1aef6).
  - Current repository evidence at 'docs/reports/external-validation/ai-reasoning/campaign-summary.md:17': 'The campaign attempted to falsify representability by testing hidden neural computation, incomplete graph knowledge, theorem-prover search explosion, proof/formalization mismatch, and agentic error propagation. These did not force Foundatio'.

### PR159:PRRT_kwDOTH_vCM6QQ_JH

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/protocol-v1.0.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821905
- Claim: **P1 Badge Record provenance before accepting CRP** In this new protocol, the artifact is promoted to 'Accepted', but the file does not record the charter-required Question → Execution → Observation → Discovery → Replication → Acceptance...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/protocol-v1.0.md' (SHA-256 1d0411df41d41d4a85792f12b32d5a924ffb9c6911a96123a628bcd096c6cd17).
  - Current repository evidence at 'theory/evaluation/comparative-representation/protocol-v1.0.md:3': 'Status: Accepted methodology for comparative representation evaluation'.

### PR160:PRRT_kwDOTH_vCM6QR-_T

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/validate_cre001_submission.py:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181635
- Claim: **P1 Badge Match provenance checks to the submitted template** For real CRE-001 bundles, the 'provenance' object is supposed to be the completed 'provenance/provenance-record.template.json' referenced by the packet manifests and evaluato...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/validate_cre001_submission.py' (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at 'tools/validate_cre001_submission.py:121': 'require(provenance, "created_at", "provenance")'.

### PR160:PRRT_kwDOTH_vCM6QR-_V

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/validate_cre001_submission.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181637
- Claim: **P1 Badge Allow assigned vocabulary labels through leakage check** Because the validator scans every string in the entire bundle, listing 'Vocabulary A', 'Vocabulary B', and 'Vocabulary C' as leakage terms rejects submissions that follo...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/validate_cre001_submission.py' (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at 'tools/validate_cre001_submission.py:25': '"Vocabulary C",'.

### PR164:PRRT_kwDOTH_vCM6RRYKW

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/metadata/theorems.yaml:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/164#discussion_r3591417084
- Claim: **P1 Badge Use a verifier-supported theorem status** In the reviewed tree, 'tools/verify_theory.py' accepts only 'Draft', 'Proposed', 'Verified', 'Established', or 'Deprecated' for theorem metadata, so introducing 'Established (Condition...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR164:PRRT_kwDOTH_vCM6RRYKW found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/metadata/theorems.yaml' (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at 'theory/metadata/theorems.yaml:4': 'status: Established (Conditional)'.

### PR168:PRRT_kwDOTH_vCM6RSwBn

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/cre001_compile_vocabularies.py:62`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/168#discussion_r3591944859
- Claim: **P1 Badge Verify against the registered reference artifact** In the deterministic comparison path, the verifier uses 'model_from_scenario()' as the reference instead of 'deterministic-verifier/reference-model.json', even though the exis...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR168:PRRT_kwDOTH_vCM6RSwBn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre001_compile_vocabularies.py' (SHA-256 f29f0da5323f68eaaee65e11159af3fce922b17cbad1799d2622298dae058df5).
  - Current repository evidence at 'tools/cre001_compile_vocabularies.py:62': "if (e['output_path'],json.dumps(e['resulting_common_model_value'],sort_keys=True)) not in by: failures.append({'path':e['output_path'],'error':'entry absent from committed trace'})".

### PR171:PRRT_kwDOTH_vCM6RUQL4

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529395
- Claim: **P1 Badge Use real source gaps for strategic tasks** These hard-coded 'GAP-001' through 'GAP-005' values do not describe the new CRE-002 tasks: in the generated gap report they still point to PS-001/PS-003 unresolved/provisional-system ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/generate_next_tasks.py' (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at 'tools/generate_next_tasks.py:21': "if __name__=='__main__': raise SystemExit(main())".

### PR173:PRRT_kwDOTH_vCM6RU20P

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_cre002_preregistration.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755287
- Claim: **P1 Badge Restore the CRE-002 preregistration check** With this value, the new test fails: 'python -m unittest tests.test_cre002_preregistration' invokes 'tools/check_cre002_preregistration.py' and reports 'missing nonclaim: FAR proof',...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre002_preregistration.py' (SHA-256 1dca0309686c2ee316462f60958f09a4a3fe14d3817261deddda1a35bf9bd454).
  - Current repository evidence at 'tools/check_cre002_preregistration.py:26': 'return 1'.

### PR173:PRRT_kwDOTH_vCM6RU20S

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755291
- Claim: **P1 Badge Make the override path reachable before locking the scenario** In this frozen scenario, 'T_override' requires provenance for 'manual_override=true' from the operator, but the initial evidence log is empty and the only evidence...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20S found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json' (SHA-256 f1b355ea5a68526adeb071defc34dcd2260950be2af144d431c51466efb99b0a).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json:70': '"guard_expression": "provenance(manual_override=true,operator,high)",'.

### PR175:PRRT_kwDOTH_vCM6RVFKq

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/175#discussion_r3592838611
- Claim: **P1 Badge Update preregistration validation for the unlock state** In the unlocked state introduced here, the committed CI path still fails: 'tests/test_cre002_preregistration.py' invokes 'tools/check_cre002_preregistration.py', which r...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR175:PRRT_kwDOTH_vCM6RVFKq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json' (SHA-256 b07a78551bb671776c1022ca51b55644a0ed12f5fa28905e16ff55ffcf61cc67).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:38': '}'.

### PR176:PRRT_kwDOTH_vCM6RVX-c

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:34`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/176#discussion_r3592946228
- Claim: **P1 Badge Commit the declared CRE-002 result artifacts** With this line set to 'true', a clean checkout is declared to contain official results, but this commit does not track 'theory/evaluation/comparative-representation/experiments/CR...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR176:PRRT_kwDOTH_vCM6RVX-c found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json' (SHA-256 b07a78551bb671776c1022ca51b55644a0ed12f5fa28905e16ff55ffcf61cc67).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:34': '"official_results_present": true,'.

### PR178:PRRT_kwDOTH_vCM6RV06v

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/178#discussion_r3593108984
- Claim: **P1 Badge Keep the override path reachable** With this scenario as frozen input, 'T_override' can never fire: the initial 'evidence_log' is empty, and the only evidence-producing transitions are 'T_record_a'/'T_record_b', which append o...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR178:PRRT_kwDOTH_vCM6RV06v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json' (SHA-256 3b65fdefc814195d68d6dbc773b8dd598a6029356a17f9a05582fa023faa6239).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json:21': '{"id":"T_override","authorization":"R_override","guard_expression":"provenance(manual_override=true,operator,high)","updates":{"manual_override":true},"defeats_lower_priority_conflict_for_current_state":true,"append_history":true},'.

### PR181:PRRT_kwDOTH_vCM6RWgcF

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:6`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/181#discussion_r3593355089
- Claim: **P1 Badge Update Baseline 1.1 gates before unlocking** In this authorized state, setting these flags to 'true' breaks the existing Baseline 1.1 health gates: 'tools/check_vocabulary_semantics_baseline_1_1.py' still requires both values ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR181:PRRT_kwDOTH_vCM6RWgcF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json' (SHA-256 2253d19c68da78800186089e9b320881c1a70552a02f4c295f05496a40abb6af).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:6': '"compiler_implementation_permitted": true,'.

### PR182:PRRT_kwDOTH_vCM6RXNCP

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/cre002_ext001_model.py:155`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608670
- Claim: **P1 Badge Require every frozen output before passing candidates** In this execution, 'required_outputs_preserved' is the gate used by 'build()' before marking a candidate complete, but this check never consults the frozen scenario's 'ou...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCP found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre002_ext001_model.py' (SHA-256 6ee8e92055c71b1a2679f66a77fc3e5f64a27fded1e3259963254de9e667ba9c).
  - Current repository evidence at 'tools/cre002_ext001_model.py:155': '"required_outputs_preserved": all({"booleans", "evidence_log", "action_history", "active_rules", "nondeterministic_outcomes", "priority_defeat_occurred", "terminal_reason"}.issubset(s.data()) for s in terminals),'.

### PR182:PRRT_kwDOTH_vCM6RXNCU

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/cre002_ext001_native.py:105`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608676
- Claim: **P1 Badge Validate candidate records against derived-field requirements** This audit checks whether the Baseline 1.1 construct definitions themselves have 'required_fields' and 'operational_constraints', but it never checks that the can...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre002_ext001_native.py' (SHA-256 ada1b5cc161684d97c1426b9461a45822d7e4697d57bbb1cee31ee5d4590894e).
  - Current repository evidence at 'tools/cre002_ext001_native.py:105': 'status = "pass" if not (missing or malformed or primitive_mismatch) else "fail"'.

### PR184:PRRT_kwDOTH_vCM6Rc-OK

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/184#discussion_r3595705807
- Claim: **P1 Badge Require all clean counted submissions to pass** When there are multiple eligible uncontaminated submissions and one completes while another fails, these rules can still classify the vocabulary and overall replication as succes...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR184:PRRT_kwDOTH_vCM6Rc-OK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json' (SHA-256 68472ec0c633eddf76f4d38807ae070a76e55aa5af0c23f98bbed2e2255b3437).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json:23': '"overall_replication_success": "Every official vocabulary satisfies vocabulary_replication_success, at least two independent implementation teams contribute counted submissions, and the verifier independence audit passes.",'.

### PR186:PRRT_kwDOTH_vCM6Revz1

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_cre002_ext001_rep001_team_registry.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/186#discussion_r3596346625
- Claim: **P1 Badge Reject shared repositories in registry validation** When eligible registrations have disjoint personnel but reuse the same 'repository_identity', this checker still appends them to the eligible implementation/verifier counts a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR186:PRRT_kwDOTH_vCM6Revz1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre002_ext001_rep001_team_registry.py' (SHA-256 f4ba7a1740930f74f3e3d025eabc17fd2cd039915732a4106d220215c76bcb88).
  - Current repository evidence at 'tools/check_cre002_ext001_rep001_team_registry.py:35': 'personnel.update(members)'.

### PR188:PRRT_kwDOTH_vCM6Rfduh

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/cre002_ext001_robustness.py:93`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/188#discussion_r3596608255
- Claim: **P1 Badge Preserve empty arrays in the third implementation** When the frozen scenario contains empty arrays ('initial_state.evidence_log' and 'initial_state.action_history'), 'json.loads(..., object_pairs_hook=list)' represents those a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR188:PRRT_kwDOTH_vCM6Rfduh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre002_ext001_robustness.py' (SHA-256 d151472585ec34162cd92cd4413ba02fda068ca9256f68105cdb869d2d610c1b).
  - Current repository evidence at 'tools/cre002_ext001_robustness.py:60': 'if __name__=="__main__": raise SystemExit(main())'.

### PR192:PRRT_kwDOTH_vCM6RipTt

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tests/test_t003_adequacy_audit.py:42`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/192#discussion_r3597775989
- Claim: **P1 Badge Align the audit wording checked by the test** Running 'python -m unittest tests.test_t003_adequacy_audit' fails here because the audit document never contains this exact phrase: it says the examples “do not establish universal...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR192:PRRT_kwDOTH_vCM6RipTt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_t003_adequacy_audit.py' (SHA-256 f281bf9f79db14d1ed96dfacfffe884f58e95b3ab8489a04b8c66c48b5a1b689).
  - Current repository evidence at 'tests/test_t003_adequacy_audit.py:42': 'self.assertIn("three examples", text)'.

### PR192:PRRT_kwDOTH_vCM6RipTx

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tests/test_t003_adequacy_audit.py:49`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/192#discussion_r3597775995
- Claim: **P1 Badge Restrict the axiom/admission scan to declarations** This test currently scans the entire Lean source as raw text, so it fails on existing comments rather than new proof admissions: 'FARCore.lean' already contains “as an axiom”...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR192:PRRT_kwDOTH_vCM6RipTx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_t003_adequacy_audit.py' (SHA-256 f281bf9f79db14d1ed96dfacfffe884f58e95b3ab8489a04b8c66c48b5a1b689).
  - Current repository evidence at 'tests/test_t003_adequacy_audit.py:49': 'with self.subTest(word=word):'.

### PR193:PRRT_kwDOTH_vCM6Rj0PR

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `.github/workflows/specification-export.yml:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/193#discussion_r3598208533
- Claim: **P1 Badge Install pytest before running the workflow tests** In the added workflow, the only setup before this command is checkout, 'actions/setup-python', the exporter run, and 'git diff'; neither 'pyproject.toml' nor 'requirements.txt...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR193:PRRT_kwDOTH_vCM6Rj0PR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/specification-export.yml' (SHA-256 2aa19214981ed97c418a375063879cbe20494f215032f7afe5f7d5cd45968b0d).
  - Current repository evidence at '.github/workflows/specification-export.yml:23': '- name: Regenerate Project FAR specification export'.

### PR197:PRRT_kwDOTH_vCM6RpiBK

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/independence/primitive-independence-evaluation.schema.json:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/197#discussion_r3600351085
- Claim: **P1 Badge Separate per-test records from aggregate decisions** This schema validates only a single 'test_type', but 'locally-independent' and 'tested-space-independent' are aggregate outcomes that the framework allows only after every m...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR197:PRRT_kwDOTH_vCM6RpiBK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/independence/primitive-independence-evaluation.schema.json' (SHA-256 2c5923c90c1a8108a16d1e7799dd2d34b18285d765faafdc656493bfeb730c89).
  - Current repository evidence at 'theory/independence/primitive-independence-evaluation.schema.json:95': '},'.

### PR199:PRRT_kwDOTH_vCM6R1VGh

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tests/test_alternative_vocabulary_competition.py:68`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/199#discussion_r3604720523
- Claim: **P1 Badge Fix the self-matching global-minimality assertion** This assertion makes the newly added test suite fail because the report intentionally contains the negated sentence 'AVC-001 does **not** establish that FAR is globally minim...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR199:PRRT_kwDOTH_vCM6R1VGh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_alternative_vocabulary_competition.py' (SHA-256 9aa6f8b7d9acf4b8b5d81b09b5525ecfadb2117bae6083307697e07ea2aaeb4e).
  - Current repository evidence at 'tests/test_alternative_vocabulary_competition.py:68': 'self.assertNotIn("Scientific conclusion: **FAR is globally minimal**", report)'.

### PR200:PRRT_kwDOTH_vCM6R1kcF

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/independence/global-minimality/GMA-001/README.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/200#discussion_r3604808061
- Claim: **P1 Badge Use one charter-approved artifact status** 'AGENTS.md' directs all automated work to 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from 'Accepted', 'R...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR200:PRRT_kwDOTH_vCM6R1kcF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/independence/global-minimality/GMA-001/README.md' (SHA-256 3e070958e4898c8ad375baca08d3563c6a10cdc75fc3d4c33cb9f6a49d6e03bb).
  - Current repository evidence at 'theory/independence/global-minimality/GMA-001/README.md:5': 'Completed evidence synthesis. Scientific conclusion: **global minimality unresolved**.'.

### PR202:PRRT_kwDOTH_vCM6R1vYI

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:32`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871140
- Claim: **P1 Badge Keep CRE-003-I's investigation fixed** When CRE-003-I is used as the interpretation-only case, this changes the investigation objective from determining whether the alarm is permitted to determining whether withdrawal is permi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json' (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:32': '"investigation": "determine whether withdrawal is permitted",'.

### PR202:PRRT_kwDOTH_vCM6R1vYK

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871144
- Claim: **P1 Badge Do not add new facts to the calculus case** When CRE-003-C is evaluated as the reasoning-calculus-only variation, adding 'exception_q' to 'system_b' also changes the represented material and its interpretation, despite both be...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json' (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:72': '"interpretation": {"p": "evidence accepted", "q": "claim supported", "exception_q": "registered defeating exception"},'.

### PR202:PRRT_kwDOTH_vCM6R1vYM

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:96`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871147
- Claim: **P1 Badge Keep the calculus constant in CRE-003-R** When CRE-003-R is used to test representation/structure variation, changing the calculus from 'modus_ponens' to 'support_edge_propagation' conflicts with the case's 'held_constant' dec...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json' (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:96': '"calculus": ["support_edge_propagation"]'.

### PR203:PRRT_kwDOTH_vCM6R12qG

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tests/test_cre003_execution.py:66`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/203#discussion_r3604912577
- Claim: **P1 Badge Fix the assertion string so the test suite passes** When I ran 'python -m unittest tests.test_cre003_preregistration tests.test_cre003_execution', this assertion failed because 'execution.md' contains the phrase "remained unre...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR203:PRRT_kwDOTH_vCM6R12qG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_cre003_execution.py' (SHA-256 81c77ee23ea1d1a3595b84e9894c5d917ac1b37fb119e39a2f6669e45eea866d).
  - Current repository evidence at 'tests/test_cre003_execution.py:66': 'self.assertIn("remain unresolved rather than defeated", self.report)'.

### PR204:PRRT_kwDOTH_vCM6R2SrO

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/204#discussion_r3605073881
- Claim: **P1 Badge Require a registered carrier before passing** When an evaluator selects only 'difference_carriers=["other"]' and answers 'other_function="none"', execution falls through to this 'pass' even though there are no registered funct...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR204:PRRT_kwDOTH_vCM6R2SrO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py' (SHA-256 874bf268cf03dd02744e476d0c34a98c14dfa46107fc0c56f79a3cbea5521f87).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py:72': 'classification = "unknown"'.

### PR206:PRRT_kwDOTH_vCM6R22Dm

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json:10`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278314
- Claim: **P1 Badge Fix the locked evaluator packet hash** This lock entry does not match the checked-in 'evaluator_packet.md': 'verify_protocol_lock()' computes git blob SHA-1 '1ea5043ccb3a10aa0f350237ec1b4b3ce558c7ff' for the file in this commi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Dm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json' (SHA-256 29021338ed94e411a25e5db02ce8c32de90d9646630923db4b45105ab8e6eae9).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json:10': '"evaluator_packet.md": "1ea5043ccb3a10aa0f350237ec1b4b3ce558c7ff"'.

### PR208:PRRT_kwDOTH_vCM6R_ofk

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/208#discussion_r3608557370
- Claim: **P1 Badge Enforce the closed intake gates before scoring** Because this rule is only documented here, it does not actually protect RUN-001: the inspected CRE-004 replay path ('execution_pipeline.replay' → 'validate_manifest') accepts on...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR208:PRRT_kwDOTH_vCM6R_ofk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md' (SHA-256 f4d42154d70f615a5897921272806d43ae0dc656efc885ba9569db0367388577).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md:42': 'The execution pipeline must reject scoring while any gate remains incomplete. No missing evaluator judgment may be inferred, simulated, backfilled, or replaced with an author-generated answer.'.

### PR217:PRRT_kwDOTH_vCM6SCBSx

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_pbts001_replication_package.py:259`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418609
- Claim: **P1 Badge Keep the package validator passing its own frozen protocol** For this commit, running 'python tools/check_pbts001_replication_package.py' fails because the protocol’s nonclaim is written as 'This package does not establish:' f...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBSx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_pbts001_replication_package.py' (SHA-256 5fbe6e175ca382c012f1bdd171f77efc70ce70889f16048e2032845b95c0f6c2).
  - Current repository evidence at 'tools/check_pbts001_replication_package.py:259': '"- FARA compliance;",'.

### PR220:PRRT_kwDOTH_vCM6SIkht

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/update_readme_dashboard.py:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/220#discussion_r3611798075
- Claim: **P1 Badge Close the README dashboard task append call** In the target commit, running 'python -m py_compile tools/update_readme_dashboard.py' fails with 'SyntaxError: '(' was never closed' at this appended task tuple. Any path that invo...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR220:PRRT_kwDOTH_vCM6SIkht found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/update_readme_dashboard.py' (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at 'tools/update_readme_dashboard.py:68': "if __name__=='__main__': main()".

### PR221:PRRT_kwDOTH_vCM6SIzy3

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `README.md:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/221#discussion_r3611882907
- Claim: **P1 Badge Keep research-check aligned with README wording** In this commit the README changes the required wording to “The project is deduction-first,” but 'tools/check_deduction_first_program.py' still asserts the exact old phrase 'The...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR221:PRRT_kwDOTH_vCM6SIzy3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'README.md' (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at 'README.md:20': 'Public evaluation is authorized only when the exact theorem, premises, mechanization status, open-world boundary, Unknown discipline, and nonclaims are disclosed together.'.

### PR221:PRRT_kwDOTH_vCM6SIzy4

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_thm_target_001.py:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/221#discussion_r3611882909
- Claim: **P1 Badge Avoid rejecting the registered nonclaim as a claim** When this new checker is invoked directly, and from the Makefile after the prior gate is fixed, it fails against the committed theorem document because the prohibited substr...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR221:PRRT_kwDOTH_vCM6SIzy4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_thm_target_001.py' (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at 'tools/check_thm_target_001.py:56': "assert family['THM-P8-CORR-001']['status']=='target_frozen_unproved'".

### PR226:PRRT_kwDOTH_vCM6SXowJ

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_s_core_w1.py:112`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/226#discussion_r3617256618
- Claim: **P1 Badge Use the path constant for the W1 registry lookup** When 'python tools/check_s_core_w1.py' runs, this line always raises 'AttributeError' because 'reg' was rebound above to the loaded JSON dict, so it no longer has 'relative_to...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR226:PRRT_kwDOTH_vCM6SXowJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_s_core_w1.py' (SHA-256 0777b463ee186e2a3f5fcf896b007bb95bcf257e200d5af1c76d430293c922a5).
  - Current repository evidence at 'tools/check_s_core_w1.py:18': "if __name__=='__main__': raise SystemExit(main())".

### PR229:PRRT_kwDOTH_vCM6SaGam

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_faithful_representation.py:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/229#discussion_r3618166626
- Claim: **P1 Badge Keep the faithful-representation check aligned with the spec** With this new phrase guard, 'make research-check'/'make health-fast' fails on the committed tree: the faithful spec contains the other checked phrases, but not 'so...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR229:PRRT_kwDOTH_vCM6SaGam found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_faithful_representation.py' (SHA-256 588512b670fc6b3f84911a5bd0c2d695c4185b7b18af79c29a6f070ac8f2033b).
  - Current repository evidence at 'tools/check_faithful_representation.py:12': "d=load(REG); assert d['specification_id']=='FAITHFUL-REP-001' and d['version']=='1.0'; assert d['w3_proof_registry']==W3.relative_to(ROOT).as_posix(); assert d['w4_proof_registry']==W4.relative_to(ROOT).as_posix(); assert d['recovery_contra".

### PR232:PRRT_kwDOTH_vCM6Sd90_

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `far_validation/weakening.py:137`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/232#discussion_r3619656400
- Claim: **P1 Badge Compare the old path when auditing renames** When Git reports a rename such as 'R059 tests/test_old.py tests/test_new.py', this keeps only the new path, so '_show(base, path)' looks for 'tests/test_new.py' in the base commit a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR232:PRRT_kwDOTH_vCM6Sd90_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'far_validation/weakening.py' (SHA-256 aae88e582f096015e5246ffb079ae263b212e66177a5a4e041176253990b0fde).
  - Current repository evidence at 'far_validation/weakening.py:137': 'status, path = fields[0], fields[-1]'.

### PR233:PRRT_kwDOTH_vCM6Sfq25

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_w3_5_corpus_freeze.py:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/233#discussion_r3620279924
- Claim: **P1 Badge Enforce required instance versions before freezing** When 'RCS-001' marks 'version' as a required instance field, this per-record validation never checks for it; all 18 new source/registry records are accepted without a per-in...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR233:PRRT_kwDOTH_vCM6Sfq25 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_w3_5_corpus_freeze.py' (SHA-256 66419a598ad54c35fb458ea35113e85fc6334d8e12d2276792637472147f9cee).
  - Current repository evidence at 'tools/check_w3_5_corpus_freeze.py:77': "for entry in catalog.get('records',[]):".

### PR237:PRRT_kwDOTH_vCM6SwTry

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_w3_5_candidate_tests.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/237#discussion_r3626404989
- Claim: **P1 Badge Load preserved trial records before accepting completion** For the completed candidate package, this regenerates 'trials' from the current Python module and the result only hashes that same module, so updating the generator an...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR237:PRRT_kwDOTH_vCM6SwTry found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_w3_5_candidate_tests.py' (SHA-256 3dbfa3bfd988947fa3a88ea7a4fa7deed530931ce9c0c91f9a0269eeb2751b65).
  - Current repository evidence at 'tools/check_w3_5_candidate_tests.py:26': 'trials=execute()'.

### PR239:PRRT_kwDOTH_vCM6SxUIT

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/s-core-construction-obstruction-ledger.json:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782560
- Claim: **P1 Badge Update the authoritative ledger before marking W5 complete** This promotes the machine-readable ledger to W5-complete, but the same registry still declares 'statement_authority' as 'source_artifact', and 'docs/research/s-core-...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/s-core-construction-obstruction-ledger.json' (SHA-256 46c94d5b4190d74b4c9f7c157b6362a7186cd9b39c13636648348f4d384cd4eb).
  - Current repository evidence at 'theory/evaluation/s-core-construction-obstruction-ledger.json:5': '"status":"w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved",'.

### PR239:PRRT_kwDOTH_vCM6SxUIX

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_thm_target_001.py:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782564
- Claim: **P1 Badge Register W5 as satisfying the scoped proof gate** After this commit marks the bounded S_core theorem proved, this assertion locks 'research-gates.json' in the old pre-W5 state: 'scoped-representation-proof' remains 'not_satisf...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_thm_target_001.py' (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at 'tools/check_thm_target_001.py:111': "assert gates['scoped-representation-proof']['evidence']==[]".

### PR240:PRRT_kwDOTH_vCM6Sxc8r

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `mechanization/lean/SCoreW5.lean:55`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/240#discussion_r3626834839
- Claim: **P1 Badge Make FaithfulSplit enforce the frozen contract** The new registry/doc present this as machine-checking the registered W5 'Faithful_split', but this definition only requires a constructor id and a few list equalities; it omits ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR240:PRRT_kwDOTH_vCM6Sxc8r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/lean/SCoreW5.lean' (SHA-256 e9e5e25b941a0648df13eea91bf19fcaa187d4d7854512ae893afd0a01681703).
  - Current repository evidence at 'mechanization/lean/SCoreW5.lean:55': 'target.investigation = source.stakes ∧'.

### PR244:PRRT_kwDOTH_vCM6SzTq5

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json:24`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/244#discussion_r3627535726
- Claim: **P1 Badge Preserve admitted observations in the obligations** The scope admits 'observations' as part of 'S_inf_eff', but the registered/proved obligations never require observation relations or evidential-status distinctions to be pres...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR244:PRRT_kwDOTH_vCM6SzTq5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json' (SHA-256 5ef9e1730817dbfa6234cd68cca03e4668e38d58ce0a13e3bf8e90d2a52f362d).
  - Current repository evidence at 'theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json:24': '"INF-EXT-005_history_and_revision_prefix_coherence",'.

### PR245:PRRT_kwDOTH_vCM6Szcon

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json:16`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/245#discussion_r3627588070
- Claim: **P1 Badge Require computable guard-crossing certificates** For admitted sources where a guard has isolated crossings but the source does not declare computable brackets, separation/transversality data, or a finite event enumerator, the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR245:PRRT_kwDOTH_vCM6Szcon found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json' (SHA-256 d8f00cd42eaa58262bb6b32e3f4d43c98b9cfc7a5534f4f288811453b7de8ada).
  - Current repository evidence at 'theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json:16': '"inputs": "piecewise-rational controls with finite descriptions and declared switching times",'.

### PR251:PRRT_kwDOTH_vCM6S0zhD

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104186
- Claim: **P1 Badge Add the missing semantic-interface transform** The governing 'POST-W5-USD-001' definition for 'USD-W3-INVARIANCE' requires the semantic-interface replacement class, but this contract's exhaustive 'transformations' list has no ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json' (SHA-256 ca7cc08899fc0b34ba9b3900c9d1b09e5bb013f29a63a9cd4a4b3ec3f0343605).
  - Current repository evidence at 'theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json:19': '"transformations": ['.

### PR252:PRRT_kwDOTH_vCM6S1nVJ

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json:61`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/252#discussion_r3628403071
- Claim: **P1 Badge Do not advance to W5 before W4 controls are run** When this result is consumed to schedule the next USD workstream, it skips part of the registered W4 gate: the frozen program defines Workstream 4 as 'USD-W4-NECESSITY' and req...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR252:PRRT_kwDOTH_vCM6S1nVJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json' (SHA-256 777d215848223d7dbec744916f1a68bb563d3c86dca383ea61dd479c7245abe2).
  - Current repository evidence at 'theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json:61': '"next_workstream": "USD-W5-MIN-EQUIV",'.

### PR254:PRRT_kwDOTH_vCM6S2A_u

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w6-independence-result-v1.0.json:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/254#discussion_r3628552153
- Claim: **P1 Badge Do not mark W6 executed without executable artifacts** This block records a completed three-path execution with artifact isolation, a separate verifier, deterministic comparison, and mutation pass, but the commit only adds JSO...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR254:PRRT_kwDOTH_vCM6S2A_u found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w6-independence-result-v1.0.json' (SHA-256 a90bfb289a42681b1fa5a87e18bdd35436cb16516aa25162cef9b1babe1506bb).
  - Current repository evidence at 'theory/evaluation/usd-w6-independence-result-v1.0.json:17': '"deterministic_comparison": "pass",'.

### PR261:PRRT_kwDOTH_vCM6S-3sQ

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/261#discussion_r3631793680
- Claim: **P1 Badge Fill mandatory candidate declarations before freezing** These objects are admitted as 'admitted_frozen_unscored', but each frozen candidate only has source/primitives/constraint fields and omits the rest of 'admission_rule.req...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR261:PRRT_kwDOTH_vCM6S-3sQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json' (SHA-256 a322b30601057a7f7695f65235ed5b59decf84e0d94a372f213de3c8b5441f61).
  - Current repository evidence at 'theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json:47': '"conceptual_source": "compositional process semantics and categorical structure",'.

### PR277:PRRT_kwDOTH_vCM6TGN_S

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/audits/tue-w1-unknown-boundary-audit.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/277#discussion_r3634548449
- Claim: **P1 Badge Preserve the registered uninstrumented boundary** When this W1 package is used to authorize advancing the queue to PR 278, changing the inherited creative Unknown to 'instrumentable creative generation' means the completed wor...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR277:PRRT_kwDOTH_vCM6TGN_S found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/tue-w1-unknown-boundary-audit.md' (SHA-256 4cd0262ec1394f0fb5c2fbf3401f0eb40e28352f218541dc6146a38fb3202a8c).
  - Current repository evidence at 'docs/audits/tue-w1-unknown-boundary-audit.md:5': 'This audit is limited to the three Unknown boundaries inherited from SC-W6: instrumentable creative generation, tacit moral salience, and systems whose relevant reasoning distinctions remain inaccessible.'.

### PR278:PRRT_kwDOTH_vCM6TGhkw

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_tue_w2_defeating_condition_campaign.py:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/278#discussion_r3634662053
- Claim: **P1 Badge Require every frozen attack family to be exercised** This check only proves that each defeating condition has at least one case, but the protocol freezes specific 'precommitted_attack_families'. In the current artifacts, searc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR278:PRRT_kwDOTH_vCM6TGhkw found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_tue_w2_defeating_condition_campaign.py' (SHA-256 2987e250cd22c0342d462fd7b774d7e8811d4da056b7571fe7abc1476b1e868f).
  - Current repository evidence at 'tools/check_tue_w2_defeating_condition_campaign.py:34': 'require(set(item["condition"] for item in cases) == set(conditions), "not all conditions attacked")'.

### PR290:PRRT_kwDOTH_vCM6TJ7wQ

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/290#discussion_r3635950301
- Claim: **P1 Badge Keep the queue on the registered W10 workstream** For the post-W9 state, this advances PR 291 to 'UPP-W10-SEMANTIC-INTERPRETATION', but the registered universal-proof program still defines target PR 291 as 'UPP-W10-R4' with pu...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR290:PRRT_kwDOTH_vCM6TJ7wQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:17': '{"target_pr":292,"workstream":"UPP-W11-HISTORICAL-TRACE","result":"historical_trace_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"},'.

### PR291:PRRT_kwDOTH_vCM6TKCL7

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:18`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/291#discussion_r3635987842
- Claim: **P1 Badge Keep the UPP queue on the registered workstream** 'theory/evaluation/post-tue-universal-proof-program-v1.0.json' still registers PR 292 as 'UPP-W11-R5' for uniform-effective-recovery, but this queue update sends PR 292 to 'UPP...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR291:PRRT_kwDOTH_vCM6TKCL7 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:18': '{"target_pr":293,"workstream":"UPP-W12-COMPONENT-INDEPENDENCE","result":"five_component_relative_independence_established_by_separating_witnesses_and_anti_reduction_controls"},'.

### PR292:PRRT_kwDOTH_vCM6TKJkz

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/292#discussion_r3636029948
- Claim: **P1 Badge Keep PR #293 aligned with registered sufficiency workstream** The registered UPP plan assigns target PR 293 to 'UPP-W12-SUFFICIENCY' and puts component independence/irreducibility at target PR 294 ('theory/evaluation/post-tue-...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR292:PRRT_kwDOTH_vCM6TKJkz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:19': '{"target_pr":294,"workstream":"UPP-W13-SUFFICIENCY-CONSTRUCTION","result":"relative_rccd_sufficiency_established_by_effective_compositional_construction_and_bidirectional_reconstruction"},'.

### PR294:PRRT_kwDOTH_vCM6TKdMI

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:21`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/294#discussion_r3636143762
- Claim: **P1 Badge Point the queue at the registered PR #295 workstream** When a runner follows this active queue, it is sent to 'UPP-W14-IRREDUCIBILITY-MAXIMALITY', but the registered universal proof program has no such workstream; I checked 't...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR294:PRRT_kwDOTH_vCM6TKdMI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:21': '{"target_pr":296,"workstream":"UPP-W15-TERMINAL-THEOREM","result":"strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary"}'.

### PR296:PRRT_kwDOTH_vCM6TK9sE

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:26`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636341762
- Claim: **P1 Badge Keep historical UPP checkers compatible with terminal closure** With this checkpoint now terminal ('next_action: null' and the public gate open), the existing W1-W11 validation tools still read the same checkpoint as if it wer...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TK9sE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:26': '"public_evaluation_authorized":false,'.

### PR300:PRRT_kwDOTH_vCM6TUJa1

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/adversarial.py:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/300#discussion_r3639747352
- Claim: **P1 Badge Import the existing closure API** In this repo 'closure.py' only defines/exports 'assess_closure'; 'compute_closure' is not present, so importing 'far_release_assurance.adversarial' raises 'ImportError' before any scenario can...
- Rationale: The artifact reviewed by finding PR300:PRRT_kwDOTH_vCM6TUJa1 has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/adversarial.py' does not exist ('test -e' is false).

### PR301:PRRT_kwDOTH_vCM6TU77g

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/cli.py:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039795
- Claim: **P1 Badge Include observed machinery in inventory closure** When a package includes an 'event.machinery_refs' entry for machinery that is not also listed as a root or dependency (for example, a disclosed undeclared tool used by an event...
- Rationale: The artifact reviewed by finding PR301:PRRT_kwDOTH_vCM6TU77g has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/cli.py' does not exist ('test -e' is false).

### PR301:PRRT_kwDOTH_vCM6TU77m

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/io.py:80`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039804
- Claim: **P1 Badge Reject missing declared flags instead of assuming true** When an external package omits 'declared' or sends a non-boolean value such as '"false"', this expression coerces it to 'True', even though the schema makes 'declared' a...
- Rationale: The artifact reviewed by finding PR301:PRRT_kwDOTH_vCM6TU77m has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/io.py' does not exist ('test -e' is false).

### PR302:PRRT_kwDOTH_vCM6TVB6-

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:137`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075291
- Claim: **P1 Badge Review changed required machinery** When a required item changes but remains declared and confirmed, this condition only creates a finding for mutable or unversioned policies; changed model/tool/policy versions otherwise fall ...
- Rationale: The artifact reviewed by finding PR302:PRRT_kwDOTH_vCM6TVB6- has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/compare.py' does not exist ('test -e' is false).

### PR302:PRRT_kwDOTH_vCM6TVB66

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075282
- Claim: **P1 Badge Review declared consequential additions** This added-machinery branch emits findings only for undeclared items and mutable policies, so a candidate that adds a declared/confirmed 'memory', 'external-state', or 'benchmark' depe...
- Rationale: The artifact reviewed by finding PR302:PRRT_kwDOTH_vCM6TVB66 has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/compare.py' does not exist ('test -e' is false).

### PR302:PRRT_kwDOTH_vCM6TVB7E

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:188`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075297
- Claim: **P1 Badge Match withdrawals by event order** Because withdrawals are collapsed into an unordered set by subject, any earlier or unrelated 'commitment_withdrawn' for the same commitment suppresses the invalidated-support finding for a la...
- Rationale: The artifact reviewed by finding PR302:PRRT_kwDOTH_vCM6TVB7E has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/compare.py' does not exist ('test -e' is false).

### PR302:PRRT_kwDOTH_vCM6TVB7N

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:206`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075307
- Claim: **P1 Badge Match identity revalidation by event order** These global counts treat any 'identity_revalidated' event as covering any 'identity_changed' event, even if the revalidation happened before the change or for a different identity ...
- Rationale: The artifact reviewed by finding PR302:PRRT_kwDOTH_vCM6TVB7N has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/compare.py' does not exist ('test -e' is false).

### PR308:PRRT_kwDOTH_vCM6TVyWI

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/docs/refund-authorization-v0.1.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/308#discussion_r3640357185
- Claim: **P1 Badge Add an explicit artifact status** This new reference-domain artifact has no 'Status' or '## Status', so its required single status cannot be audited and readers cannot tell whether it is Accepted, Research, Provisional, Archiv...
- Rationale: The artifact reviewed by finding PR308:PRRT_kwDOTH_vCM6TVyWI has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/docs/refund-authorization-v0.1.md' does not exist ('test -e' is false).

### PR309:PRRT_kwDOTH_vCM6TV50T

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/309#discussion_r3640400953
- Claim: **P1 Badge Keep the legacy audit CLI path working** When existing callers invoke 'far-decision [--output ...]', the new subparser treats the package path as an invalid command before the audit code or invalid-package handling can run. I ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR309:PRRT_kwDOTH_vCM6TV50T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/cli.py' (SHA-256 f58175d95816402404064510efac2c38006e0945119b7b6d924d204588c6f033).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/cli.py:23': 'args = parser.parse_args(argv)'.

### PR310:PRRT_kwDOTH_vCM6TV9Kf

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/policy_impact.py:128`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/310#discussion_r3640420134
- Claim: **P1 Badge Block escalate-to-allow policy changes** When a candidate removes a required evidence check, a request that previously escalated because the fact was unknown can become allowed, but this branch only treats 'BLOCK -> ALLOW' as ...
- Rationale: The artifact reviewed by finding PR310:PRRT_kwDOTH_vCM6TV9Kf has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/policy_impact.py' does not exist ('test -e' is false).

### PR312:PRRT_kwDOTH_vCM6TWZeA

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/trace_ingest.py:58`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/312#discussion_r3640583396
- Claim: **P1 Badge Filter ingestion to the selected trace** This loop normalizes every span in the export after choosing one root, but OTLP exports commonly contain batches with spans from multiple traces. If the file has one FAR root for 'trace...
- Rationale: The artifact reviewed by finding PR312:PRRT_kwDOTH_vCM6TWZeA has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/trace_ingest.py' does not exist ('test -e' is false).

### PR315:PRRT_kwDOTH_vCM6TXCNN

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/store.py:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/315#discussion_r3640823725
- Claim: **P1 Badge Reject path traversal in evidence IDs** Because 'evidence_id' comes directly from the source manifest, 'self.blob_root / evidence_id' allows values like '../escape' or an absolute path to place the canonical blob directory out...
- Rationale: The artifact reviewed by finding PR315:PRRT_kwDOTH_vCM6TXCNN has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/store.py' does not exist ('test -e' is false).

### PR317:PRRT_kwDOTH_vCM6TXS0G

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/317#discussion_r3640920597
- Claim: **P1 Badge Use exact tenant ownership for evidence reads** When one tenant ID is another tenant ID followed by '-' (for example 'tenant' and 'tenant-a'), this prefix check authorizes the shorter tenant to read the longer tenant's evidenc...
- Rationale: The artifact reviewed by finding PR317:PRRT_kwDOTH_vCM6TXS0G has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py' does not exist ('test -e' is false).

### PR318:PRRT_kwDOTH_vCM6TX-ii

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/operations.py:234`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/318#discussion_r3641176869
- Claim: **P1 Badge Reject missing blob roots during backup** When an operator passes a nonexistent '--blob-root' (for example a typo, unmounted volume, or wrong deployment path), this branch silently skips copying evidence blobs and writes a man...
- Rationale: The artifact reviewed by finding PR318:PRRT_kwDOTH_vCM6TX-ii has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/operations.py' does not exist ('test -e' is false).

### PR320:PRRT_kwDOTH_vCM6TYpZx

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/hardening.py:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/320#discussion_r3641428944
- Claim: **P1 Badge Require database files before reporting restore success** For a backup whose manifest omits 'security.db'/'evidence.db', 'verify_backup()' currently returns valid because its SQLite integrity check opens missing paths and crea...
- Rationale: The artifact reviewed by finding PR320:PRRT_kwDOTH_vCM6TYpZx has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/hardening.py' does not exist ('test -e' is false).

### PR322:PRRT_kwDOTH_vCM6TY-OJ

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/oidc.py:110`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552494
- Claim: **P1 Badge Reject unsafe OIDC tenant identifiers** When OIDC mode is enabled and the identity provider can issue a tenant claim containing path separators or '..', this accepts that value unchanged as the 'Principal.tenant_id'. The secur...
- Rationale: The artifact reviewed by finding PR322:PRRT_kwDOTH_vCM6TY-OJ has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/oidc.py' does not exist ('test -e' is false).

### PR323:PRRT_kwDOTH_vCM6TZIq9

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/deploy/kubernetes.yaml:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613886
- Claim: **P1 Badge Preserve image CMD arguments in the manifest** Per the Kubernetes docs, defining 'args' without 'command' keeps the entrypoint but uses “your new arguments”, so this manifest replaces the Dockerfile CMD that sets '--security-d...
- Rationale: The artifact reviewed by finding PR323:PRRT_kwDOTH_vCM6TZIq9 has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/deploy/kubernetes.yaml' does not exist ('test -e' is false).

### PR323:PRRT_kwDOTH_vCM6TZIrB

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/distributed.py:109`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613891
- Claim: **P1 Badge Make evidence inserts idempotent under contention** When two replicas receive the same evidence record before either transaction commits, both 'SELECT ... FOR UPDATE' queries can see no row because PostgreSQL cannot lock a mis...
- Rationale: The artifact reviewed by finding PR323:PRRT_kwDOTH_vCM6TZIrB has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/distributed.py' does not exist ('test -e' is false).

### PR335:PRRT_kwDOTH_vCM6TbKCT

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/335#discussion_r3642378612
- Claim: **P1 Badge Don't count contradictory edges as authorization support** When a producer records a required node's edge to the root as 'contradicts' (or another non-supporting relation), this comprehension still adds the source to 'incoming...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR335:PRRT_kwDOTH_vCM6TbKCT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py' (SHA-256 98cdc768e66c458956e73663258d1def15685818a17147865b7108166115c948).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:29': '}'.

### PR335:PRRT_kwDOTH_vCM6TbKCX

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:124`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/335#discussion_r3642378614
- Claim: **P1 Badge Reject cyclic dependency graphs before adjudication** For packages with two-node or longer cycles, such as 'auth -> root' and 'root -> auth', this validator accepts the graph because it only rejects self-dependencies; adjudica...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR335:PRRT_kwDOTH_vCM6TbKCX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/model.py' (SHA-256 f25f9e8cd0bf1528f65104c2fff166dafcf97cf1d18e484b18dfc824144e9c46).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/model.py:124': 'raise PackageValidationError("self-dependencies are not permitted")'.

### PR355:PRRT_kwDOTH_vCM6Tm8c9

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/validation_app.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/355#discussion_r3646752560
- Claim: **P1 Badge Configure feedback logging before returning recorded** When the Render deployment starts 'uvicorn far_demo.validation_app:app', this custom 'far.validation' logger is never configured in this repo; under Python/uvicorn default...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR355:PRRT_kwDOTH_vCM6Tm8c9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/validation_app.py' (SHA-256 76323b225c44d90c0155deb96e1f08307220b618e999ff9ee84da3e64ff40441).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/validation_app.py:123': 'logger.info("far_validation_feedback %s", canonical)'.

### PR356:PRRT_kwDOTH_vCM6Tm9zN

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:76`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/356#discussion_r3646760091
- Claim: **P1 Badge Reject pre-freeze outcome fields** When a pre-freeze manifest gains an outcome field, for example after execution but before the primary hash freeze someone adds '{"leaked_outcome": {"reward": 1, "grader_output": "..."}}', thi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR356:PRRT_kwDOTH_vCM6Tm9zN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py' (SHA-256 e1f41e94ef45ccb92650ca5eef578a6430e294082fe239a666b5461cf0aca080).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:76': '"same_task", "same_model", "same_model_parameters", "same_agent_configuration",'.

### PR357:PRRT_kwDOTH_vCM6Tnjoh

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml:10`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/357#discussion_r3646978999
- Claim: **P1 Badge Make the frozen SWE-agent config loadable** When the four runs follow 'run_comparison.py'’s instruction to use this file, SWE-agent v1.0 will reject this old-style 'agent.config_file' entry before any run starts: the 1.0 migra...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR357:PRRT_kwDOTH_vCM6Tnjoh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml' (SHA-256 d979eca3fa22afdff57c2894698018649ef94b7c6199ec253f976f2f3f852654).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml:10': 'retry:'.

### PR360:PRRT_kwDOTH_vCM6To5d1

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482119
- Claim: **P1 Badge Use the SWE-bench install_repo_script property** In the pinned SWE-bench harness, 'TestSpec' exposes the repository setup script as 'install_repo_script' (the image builder writes that into 'setup_repo.sh'); there is no 'setup...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py' (SHA-256 cfb53f6d3bc83232efe019eb5967b2f85b494e2db4a600edd04a2267e669b767).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py:73': 'text=True,'.

### PR360:PRRT_kwDOTH_vCM6To5d6

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482128
- Claim: **P1 Badge Verify the local image before accepting the lock** For 'preflight' or 'plan' on a fresh GitHub-hosted runner, comparing the committed JSON 'local_image_id' to the manifest only proves the lock is self-consistent; the Docker da...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py' (SHA-256 eb56a0a73dcdf1b5bae7326f8d00b8d990cb9f2695c75fd9e9d5b460f4948929).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:40': 'if lock.get("local_image_id") != frozen["local_image_id"]:'.

### PR367:PRRT_kwDOTH_vCM6TtX1k

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:183`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152943
- Claim: **P1 Badge Run trajectories through the registered FAR adapter** The comparison reduces each trajectory to scalar, mapping, and list counts, so even a normal completed run produces no decision dependencies, authorization requirements, un...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1k found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py' (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:183': '},'.

### PR367:PRRT_kwDOTH_vCM6TtX1m

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:194`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152946
- Claim: **P1 Badge Block primary regeneration after outcome reveal** If an operator dispatches 'freeze-primary' after 'reveal-outcomes', the workflow restores the latest postprocess artifact—including its 'post-freeze-reveal/outcome-reveal.json'...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py' (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:194': 'paths = compile_primary()'.

### PR367:PRRT_kwDOTH_vCM6TtX1o

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152948
- Claim: **P1 Badge Require the complete primary artifact set** When 'primary-freeze.json' is tampered with or restored from an incompatible artifact, a manifest containing 'artifact_count: 0', 'artifacts: []', and the hash of that empty list pas...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1o found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py' (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:222': 'raise SystemExit("Primary freeze artifact count mismatch")'.

### PR367:PRRT_kwDOTH_vCM6TtX1q

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `.github/workflows/validator-assurance.yml:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152950
- Claim: **P1 Badge Retain independent provenance for the cache bundle** The checksum and the cache bundle are generated by the same producer and uploaded in the same artifact, so a substituted bundle can be accompanied by a matching substituted ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/validator-assurance.yml' (SHA-256 02fd5b0e92615a85e8dc0d68a62ba19c440bc0fd47eb761798f6a16afbf498d1).
  - Current repository evidence at '.github/workflows/validator-assurance.yml:111': 'run: sha256sum -c signed-cache.tar.gz.sha256'.

### PR369:PRRT_kwDOTH_vCM6Ttjrd

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `mechanization/far_mechanization/compare_adjudication.py:357`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223443
- Claim: **P1 Badge Bind findings to referenced package contents** When 'adjudicate' receives a comparison from an untrusted or corrupted producer, these embedded claims are normalized but never checked against the packages identified by 'left_re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/far_mechanization/compare_adjudication.py' (SHA-256 283353eb65da96f80ae88f5299e41436c970f044f13a3d6de6ba09384faa4f2b).
  - Current repository evidence at 'mechanization/far_mechanization/compare_adjudication.py:357': 'right_claim = None if finding["right"] is None else _normalize_claim(finding["right"], f"{path}.right")'.

### PR371:PRRT_kwDOTH_vCM6TuK-l

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_repository_truth.py:36`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/371#discussion_r3649454375
- Claim: **P1 Badge Make the checker enforce the manifest authorities** When an authority or mirror entry in 'repository-truth-authority-v1.json' changes, this checker validates only the schema string and continues checking the three hard-coded p...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR371:PRRT_kwDOTH_vCM6TuK-l found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_repository_truth.py' (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at 'tools/check_repository_truth.py:36': 'fail("unsupported or missing authority schema")'.

### PR373:PRRT_kwDOTH_vCM6TuR8N

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/releases/project-far-v1.0.0.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495818
- Claim: **P1 Badge Assign the release record an allowed status** Assign this newly introduced canonical artifact exactly one of the charter’s permitted statuses—Accepted, Research, Provisional, Archive, or Unknown. The file currently declares it...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8N found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/releases/project-far-v1.0.0.md' (SHA-256 2de11d4186ddf500ba48b9381d9fbdeb545e00be3368a304c1c53be6f19fa7b0).
  - Current repository evidence at 'docs/releases/project-far-v1.0.0.md:3': 'This file records the current published repository release authority.'.

### PR379:PRRT_kwDOTH_vCM6TxgEB

- Disposition: `obsolete_after_later_changes`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/sitecustomize.py:30`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/379#discussion_r3650665592
- Claim: **P1 Badge Import the pathlib constructors from reachable code** In the checked 'far-swe-agent-execution.yml' workflow, Python 3.12 runs the regression suite and controller with this directory merely as the working directory; Python does...
- Rationale: The artifact reviewed by finding PR379:PRRT_kwDOTH_vCM6TxgEB has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/sitecustomize.py' does not exist ('test -e' is false).

### PR380:PRRT_kwDOTH_vCM6Txs_H

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/380#discussion_r3650738324
- Claim: **P1 Badge Exercise SWE-agent before declaring the launch boundary reached** In the added 'full-no-model-execution-rehearsal' job, whenever parsing succeeds but SWE-agent's runtime initialization would fail, this wrapper still reports su...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR380:PRRT_kwDOTH_vCM6Txs_H found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py' (SHA-256 736a0344981d2aad44bea7a07df1b2fffdc7b7ed518f669f151b6e04ece948e8).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py:29': 'import sys'.

### PR381:PRRT_kwDOTH_vCM6TyRNx

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:196`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944620
- Claim: **P1 Badge Revalidate restored completions before selecting the next run** When an execution artifact was produced by the old controller—including the misclassified 'v1.0.0-r1' that motivated this change—its run remains 'complete' even i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRNx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py' (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29': '_core.main()'.

### PR381:PRRT_kwDOTH_vCM6TyRNy

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944621
- Claim: **P1 Badge Block progression when a run fails terminally** When the new classifier emits 'failed_terminal' for an early slot, adding it only to 'ALLOWED_STATES' makes the state loadable but leaves it absent from 'base.RESUMABLE_STATES' a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRNy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py' (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:16': 'from validated_execution_recovery import install as install_recovery'.

### PR384:PRRT_kwDOTH_vCM6Ty6_k

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py:402`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651180908
- Claim: **P1 Badge Align the inherited regression with sequence hardening** The required test command in both '.github/workflows/far-swe-agent-execution.yml' and '.github/workflows/far-swebench-environment-smoke.yml' now fails here: 'make_run(.....
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6Ty6_k found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py' (SHA-256 fbd56ed307203f7dbf84e34bace4df55c6f4041ee9aaa0d58d729ac101b8753e).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py:402': 'self.assertEqual(second["state"], "pending")'.

### PR384:PRRT_kwDOTH_vCM6Ty6_m

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:239`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651180910
- Claim: **P1 Badge Reject malformed noncanonical target predictions** When a noncanonical '.pred' explicitly names the frozen task but omits 'model_patch'—for example '{"instance_id": "", "unexpected": ...}'—'_extract_prediction' returns 'found=...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6Ty6_m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py' (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:239': 'continue'.

### PR384:PRRT_kwDOTH_vCM6TynPj

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:285`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069591
- Claim: **P1 Badge Reconcile before enforcing sequential ordering** When restoring the exact bad state produced by the previous controller—a 'failed_terminal' slot followed by a 'complete' slot—'base.load_state()' rejects the matrix for frozen s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py' (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29': '_core.main()'.

### PR384:PRRT_kwDOTH_vCM6TynPo

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069597
- Claim: **P1 Badge Inspect every prediction file that claims the target** If SWE-agent emits the canonical '.pred' plus another '.pred' whose payload also declares the target instance, this filter ignores the second file solely because its filen...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py' (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:222': 'aggregate_files = sorted(swe_output.rglob("preds.json"))'.

### PR386:PRRT_kwDOTH_vCM6TzCgi

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:107`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/386#discussion_r3651223164
- Claim: **P1 Badge Reject malformed keyed target predictions** When a noncanonical '.pred' or 'preds.json' uses the already-supported '{task_id: prediction}' form, recursion reaches a value without 'instance_id', so this guard never fires. For e...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR386:PRRT_kwDOTH_vCM6TzCgi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py' (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:107': 'return asdict(self)'.

### PR389:PRRT_kwDOTH_vCM6TzgU-

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:324`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388775
- Claim: **P1 Badge Preserve retry classification when output is absent** When SWE-agent reports a genuine 429/5xx before creating 'sweagent-output', this early return marks the attempt 'failed_terminal' before the provider-marker logic can class...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgU- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py' (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:324': ')'.

### PR389:PRRT_kwDOTH_vCM6TzgVA

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:287`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388778
- Claim: **P1 Badge Roll back artifacts moved before an interrupted return** If 'shutil.move' moves an artifact and then raises—for example, a 'KeyboardInterrupt' after the rename/copy but before returning—or an interrupt lands between these two ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgVA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py' (SHA-256 2a6058ab8d4b58209c9f3e0bbfce2cf8cc7c8d9da27f3697aaf43ac49f07eb57).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:287': 'moved.append((path, destination))'.

### PR391:PRRT_kwDOTH_vCM6T0ZLE

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/391#discussion_r3651726623
- Claim: **P1 Badge Require model context for NOT_FOUND signals** When an unsuccessful agent or tool action emits a generic JSON error such as '{"status":"NOT_FOUND"}'—including alongside a genuine HTTP 503—this pattern matches without any model ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR391:PRRT_kwDOTH_vCM6T0ZLE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py' (SHA-256 a049c2ae960747f9295089828e8b0e63c125d52b1d79858fe7071e5783c36730).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:13': 're.compile(r"\\bstatus[\\"\']?\\s*[:=]\\s*[\\"\']?not_found\\b", re.IGNORECASE),'.

### PR391:PRRT_kwDOTH_vCM6T0ZLF

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/391#discussion_r3651726625
- Claim: **P1 Badge Keep standalone provider timeout errors retryable** When a provider reports an actual timeout in forms such as 'Timeout while contacting Gemini' or 'provider request exceeded timeout', the delegate detects the bare 'timeout' m...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR391:PRRT_kwDOTH_vCM6T0ZLF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py' (SHA-256 a049c2ae960747f9295089828e8b0e63c125d52b1d79858fe7071e5783c36730).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:35': 're.compile(r"\\btimeout(?:error|exception)\\b", re.IGNORECASE),'.

### PR392:PRRT_kwDOTH_vCM6T0n2T

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json:139`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812789
- Claim: **P1 Badge Add the required top-level case ID** Every workflow stage stops in the initial 'python case_tools.py validate' step because 'validate_manifest()' requires 'm.get("case_id") == CASE_ID', while this manifest has no top-level 'ca...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json' (SHA-256 3fb0fa29dc3cbc6626c8e0a1e6aa163240acdda4334bc3bff934fd4f5584b65e).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json:139': '"probe_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent",'.

### PR392:PRRT_kwDOTH_vCM6T0n2V

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json:6`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812791
- Claim: **P1 Badge Correct the locked controller blob hash** After the manifest identity is corrected, every validation still fails in 'verify_shared_implementation()': the 'validated_execute_controller.py' blob in the referenced legacy case is ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json' (SHA-256 69d60e95952fcdf84eab559347caba94d44894206b04fc6ae0a63851321ea07e).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json:6': '"validated_execute_controller.py": "ce525ddf6bd3213b80d8d9a01a494c3d9f89f953",'.

### PR392:PRRT_kwDOTH_vCM6T0n2W

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:178`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812793
- Claim: **P1 Badge Extract restored artifacts at the case directory** On the second and subsequent 'execute' dispatches, the uploaded artifact contains both 'execution-output/...' and 'access-freeze/...' relative to their common case-directory r...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/far-swe-agent-execution-v2.yml' (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at '.github/workflows/far-swe-agent-execution-v2.yml:178': 'env:'.

### PR393:PRRT_kwDOTH_vCM6T2FXp

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:112`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/393#discussion_r3652336929
- Claim: **P1 Badge Validate the decoded HTTP error shape before accessing it** When an HTTP error contains valid JSON whose root is not an object, or whose 'error' member is 'null', a string, or a list, this expression raises 'AttributeError' ei...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR393:PRRT_kwDOTH_vCM6T2FXp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py' (SHA-256 7c41039368a85f082d01dc48aa60dd700d08e283dc8d6856ad46174e00e387d5).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:112': 'provider_error = json.loads(raw).get("error", {})'.

### PR393:PRRT_kwDOTH_vCM6T2FXq

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:108`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/393#discussion_r3652336930
- Claim: **P1 Badge Record transport failures that occur while reading the body** When the provider sends response headers but stalls or disconnects while the body is being read, 'response.read()' can raise exceptions such as 'TimeoutError' or 'h...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR393:PRRT_kwDOTH_vCM6T2FXq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py' (SHA-256 7c41039368a85f082d01dc48aa60dd700d08e283dc8d6856ad46174e00e387d5).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:108': 'raw = response.read().decode(errors="replace")'.

### PR395:PRRT_kwDOTH_vCM6T2PsZ

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/395#discussion_r3652395862
- Claim: **P1 Badge Preserve the failed access-probe record** When this freeze is merged, the replacement status records only the successful probe and removes the repository's sole account of attempt 1, including its unsuccessful result, 16-token...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR395:PRRT_kwDOTH_vCM6T2PsZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md' (SHA-256 d81e05527fbe878c22ef9aeef80a43c1b3755bdf832e57878da4d89ada6c43b0).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md:3': 'Authority: the immutable evidence locks, the completed execution artifact from workflow run '30214963069', the outcome-blind primary freeze, and the post-freeze reveal bundle in this directory.'.

### PR396:PRRT_kwDOTH_vCM6T2ibE

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:191`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/396#discussion_r3652500679
- Claim: **P1 Badge Do not let failed restores supersede the last checkpoint** When this new artifact validation rejects a restore, the 'if: always()' upload at the end of this workflow still publishes the freshly generated, plan-only 'execution-...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR396:PRRT_kwDOTH_vCM6T2ibE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/far-swe-agent-execution-v2.yml' (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at '.github/workflows/far-swe-agent-execution-v2.yml:191': ''.

### PR397:PRRT_kwDOTH_vCM6T4r2a

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json:379`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269356
- Claim: **P1 Badge Preserve the source artifact beyond its expiry** The only copy of the 73-file execution source is GitHub artifact '8635674915', and this lock records that it expires on 2026-08-25. Both 'verify-source' and 'evaluate-reveal' do...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json' (SHA-256 0653065cbf8cbcf8f911a5ec9c68a4fea66ce73d3b04ed511dad644387d296b9).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json:379': '"artifact_id": 8635674915,'.

### PR397:PRRT_kwDOTH_vCM6T4r2b

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269359
- Claim: **P1 Badge Bind the reveal to the currently verified freeze** When 'post-freeze-reveal' was generated against an older primary freeze, this verifier accepts it because it checks only the reveal schema and never compares 'primary_freeze_s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2b found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py' (SHA-256 87014ed0fce34411ba57f413414372103094a137a38b9a3e4cccb48d2f1244b4).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466': 'raise SystemExit("Final report reveal binding mismatch")'.

### PR397:PRRT_kwDOTH_vCM6T4r2c

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269360
- Claim: **P1 Badge Recompute the final report from the revealed outcomes** When the derived JSON or Markdown report is accidentally edited, 'verify_reveal' checks only that the final JSON points to the reveal's byte hash; it never verifies that ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2c found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py' (SHA-256 87014ed0fce34411ba57f413414372103094a137a38b9a3e4cccb48d2f1244b4).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466': 'raise SystemExit("Final report reveal binding mismatch")'.

### PR398:PRRT_kwDOTH_vCM6T5D8v

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/398#discussion_r3653404525
- Claim: **P1 Badge Preserve the evaluation evidence behind these hashes** After the workflow artifact's 90-day retention period expires, the committed 'test_output_sha256' and 'run_instance_log_sha256' values cannot be resolved back to the evide...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR398:PRRT_kwDOTH_vCM6T5D8v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json' (SHA-256 0938b41fd28da12af32b586121fff4b105c87fb13a24cee3c4d3685ad0fb3097).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:52': '"test_output_sha256": "d109c9021e37e8bdd69ab4495022c0f59f835cb7975a4f27665f801e91967f84"'.

### PR398:PRRT_kwDOTH_vCM6T5D8w

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:194`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/398#discussion_r3653404528
- Claim: **P1 Badge Declare a status for each new reveal artifact** This new outcome artifact, like the three companion files added by the commit, does not declare whether its status is Accepted, Research, Provisional, Archive, or Unknown. That l...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR398:PRRT_kwDOTH_vCM6T5D8w found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json' (SHA-256 0938b41fd28da12af32b586121fff4b105c87fb13a24cee3c4d3685ad0fb3097).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:194': '"schema": "far-swe-agent-v2-post-freeze-reveal/1.0",'.

### PR399:PRRT_kwDOTH_vCM6T5NRD

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/399#discussion_r3653456877
- Claim: **P1 Badge Enforce the execution freeze independently of the selected ref** When 'workflow_dispatch' selects a branch or tag where 'bundle-sha256.json' is absent, this guard inspects that checked-out ref and passes; unlike 'access-probe'...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR399:PRRT_kwDOTH_vCM6T5NRD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/far-swe-agent-execution-v2.yml' (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at '.github/workflows/far-swe-agent-execution-v2.yml:62': 'if [ -f "$CASE_DIR/post-freeze-reveal/bundle-sha256.json" ]; then'.

### PR400:PRRT_kwDOTH_vCM6T5R2m

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/audits/theory-correction-audit-2026-07-26.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/400#discussion_r3653482542
- Claim: **P1 Badge Keep correction artifacts provisional until replicated** In the reviewed tree, the only new provenance is this single audit and its decision-log entry; no replication record exists, yet this artifact and the newly introduced a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR400:PRRT_kwDOTH_vCM6T5R2m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/theory-correction-audit-2026-07-26.md' (SHA-256 d7f814a44b7ebc3bfca16ec56e2dc54b3db3be0b7e49da9deeab9bb0f8995da6).
  - Current repository evidence at 'docs/audits/theory-correction-audit-2026-07-26.md:3': 'Status: **Accepted repository correction record**'.

### PR400:PRRT_kwDOTH_vCM6T5R2n

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_semantic_consistency.py:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/400#discussion_r3653482543
- Claim: **P1 Badge Scan all active artifacts before reporting semantic consistency** When 'semantic-check' is run on this commit, it reports PASS even though active non-archive artifacts outside this three-file allowlist still use terminology th...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR400:PRRT_kwDOTH_vCM6T5R2n found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_semantic_consistency.py' (SHA-256 a6b65a1b57b23b2d70df62bf6abcc810401b8ba9d4fd0ad65aa97802b1c36513).
  - Current repository evidence at 'tools/check_semantic_consistency.py:54': 'errors.append(f"active canonical document promotes legacy terminology: {path.relative_to(ROOT)}")'.

### PR401:PRRT_kwDOTH_vCM6T5eUS

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_swe_agent_v2_forensics.py:119`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553313
- Claim: **P1 Badge Validate the evidence inventory against its source locks** The validator never loads 'evidence-inventory.json', so deleting an artifact, changing a hash, or mislabeling external evidence still produces the advertised PASS. Thi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_swe_agent_v2_forensics.py' (SHA-256 cbd3324febe7a37a756ca610265ca87ffaa089d51af010dd57872886a647bb93).
  - Current repository evidence at 'tools/check_swe_agent_v2_forensics.py:119': "if {x.get('code') for x in taxonomy}!=expected: errors.append('taxonomy incomplete')".

### PR401:PRRT_kwDOTH_vCM6T5eUU

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_swe_agent_v2_forensics.py:112`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553317
- Claim: **P1 Badge Reconcile timeline facts with the frozen run records** If a timeline's outcome, call budget, termination reason, patch result, or grader result is changed, validation still passes because these checks cover only identity, stag...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_swe_agent_v2_forensics.py' (SHA-256 cbd3324febe7a37a756ca610265ca87ffaa089d51af010dd57872886a647bb93).
  - Current repository evidence at 'tools/check_swe_agent_v2_forensics.py:112': "if any(not required <= set(e) for e in d.get('events',[])): errors.append(f'timeline fields missing: {run}')".

### PR402:PRRT_kwDOTH_vCM6T53x-

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_merged_pr_review_inventory.py:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698273
- Claim: **P1 Badge Reject incomplete per-PR manifests** When 'counts_per_pr' is empty, omits an inventoried PR, or reports endpoint counts that disagree with the raw records, this loop merely finds no failed status and validation can still retur...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_merged_pr_review_inventory.py' (SHA-256 ad69652fd4ed51ac7b975aee9edcee5472fc5ed9834cf758c4923297e3f4cfd7).
  - Current repository evidence at 'tools/check_merged_pr_review_inventory.py:104': 'for status in [endpoint.get("status")]'.

### PR402:PRRT_kwDOTH_vCM6T53x9

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `docs/audits/merged-pr-review-audit/retrieval-manifest.json:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698271
- Claim: **P1 Badge Include standard merge commits in the inventory** At the audited SHA, 'git log --first-parent' contains 138 additional commits with subjects such as 'Merge pull request #395 from ...'; these are explicit, locally available mer...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/merged-pr-review-audit/retrieval-manifest.json' (SHA-256 04098e9daacfb3e35680b3959fa32cc670dbe473885761a32e0aac9b901aecca).
  - Current repository evidence at 'docs/audits/merged-pr-review-audit/retrieval-manifest.json:21': '"pull_requests": {'.

### PR403:PRRT_kwDOTH_vCM6T6IS4

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/check_proof_object.py:207`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792971
- Claim: **P1 Badge Do not weaken final theorem-conclusion alignment** When a proof-object conclusion is much longer than the registered theorem statement, using the shorter vocabulary as the denominator allows the conclusion to add arbitrary uns...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_proof_object.py' (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at 'tools/check_proof_object.py:207': 'return len(summary_words & statement_words) / min(len(summary_words), len(statement_words)) >= 0.35'.

### PR404:PRRT_kwDOTH_vCM6T6taR

- Disposition: `resolved_incorrectly`
- Risk: `high`
- Confidence: `manual_high`
- Location: `tools/export_merged_pr_review_inventory.py:394`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007699
- Claim: **P1 Badge Tie the live API snapshot to the audited SHA** When another PR merges before or during an export, this live 'state=closed' enumeration can include or omit repository state newer than '--audited-sha', yet the manifest still lab...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/export_merged_pr_review_inventory.py' (SHA-256 2d45122793244bc9e461c23061e8ecff8e16a66eb05a137bd84eb45c883aae73).
  - Current repository evidence at 'tools/export_merged_pr_review_inventory.py:394': 'merged = [normalize_pr(pr) for pr in closed_prs if pr.get("merged_at")]'.

### PR12:PRRT_kwDOTH_vCM6OD6bU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `research/validation/investigations/VI-002-primitive-minimality.md:229`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891148
- Claim: **P2 Badge Keep the VI-002 result table in sync** This 'Current Results' table still marks Property as pending, but the same file later adds Reduction Investigation 2 and summarizes Property as 'Independent (Provisional)' in the final re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR12:PRRT_kwDOTH_vCM6OD6bU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'research/validation/investigations/VI-002-primitive-minimality.md' (SHA-256 46933e607ba37e2ea72e84eefea584f3b7c250dc69437c57809bb35da220bb20).
  - Current repository evidence at 'research/validation/investigations/VI-002-primitive-minimality.md:229': '| Property | Pending | — |'.

### PR12:PRRT_kwDOTH_vCM6OD6bV

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `research/proofs/conjectures.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891149
- Claim: **P2 Badge Keep conjectures in one canonical registry** This declares a Project-wide canonical conjecture registry even though 'theory/theorems/conjectures.md' already records Project FAR conjectures, including Primitive Independence, Pr...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR12:PRRT_kwDOTH_vCM6OD6bV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'research/proofs/conjectures.md' (SHA-256 887981ebb396285b379649010d224cf21c819d1b740d0b8bc3f40d353c00af57).
  - Current repository evidence at 'research/proofs/conjectures.md:5': 'This document serves as the canonical registry of conjectures within Project FAR.'.

### PR12:PRRT_kwDOTH_vCM6OD6bY

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `research/README.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891152
- Claim: **P2 Badge Restore the research index or update its users** Deleting this index leaves existing repository navigation and audit evidence stale: 'README.md:31' and 'docs/README.md:24' still point readers to 'research/README.md', and 'docs...
- Rationale: The reviewer concern still reproduces on the audited commit: the research index is absent, but current repository documents still link to or rely on it. The finding is therefore a confirmed defect and must remain in the remediation queue until the index is restored or all dependent references are updated.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 does not contain 'research/README.md', while 'docs/README.md:29' still links to that missing research index.
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/SEMANTIC_AUDIT.md:111', which relies on the missing research index as evidence.

### PR14:PRRT_kwDOTH_vCM6OE6cl

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `research/proofs/theorem-catalog.md:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/14#discussion_r3517251983
- Claim: **P2 Badge Create proof files before cataloging them** This catalog now records L-001 (and the following L/P/T entries) as draft proof artifacts with canonical file paths, but I checked repo-wide with 'rg --files' for these IDs and for '...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR14:PRRT_kwDOTH_vCM6OE6cl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'research/proofs/theorem-catalog.md' (SHA-256 337fadf3f38589aacf01570bbf6a8824d03ad6286f7ce02426304d571d7b0b42).
  - Current repository evidence at 'research/proofs/theorem-catalog.md:46': '| L-001 | Representation/Object Distinction | Draft | Object; Representation; Interpretation | 'lemmas/L-001-representation-object-distinction.md' |'.

### PR15:PRRT_kwDOTH_vCM6OOImd

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARE/definitions/graph-definitions.md:86`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/15#discussion_r3520579015
- Claim: **P2 Badge Define the path used for weak connectivity** When weak connectivity is used by the new dependency-component proof, this definition still relies on a bare 'path' after direction is ignored, but the only path definition introduc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR15:PRRT_kwDOTH_vCM6OOImd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/definitions/graph-definitions.md' (SHA-256 1603803468d08638840962da067cc84d7586c87df20d11dbd8758b4e15d52f9c).
  - Current repository evidence at 'frameworks/FARE/definitions/graph-definitions.md:86': '# Definition 9 — Subgraph'.

### PR15:PRRT_kwDOTH_vCM6OOImg

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARE/proofs/FARE-P012-dependency-components.md:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/15#discussion_r3520579019
- Claim: **P2 Badge Restrict the objective to nodes in the dependency subgraph** For an assessment graph containing an assessment with no dependency edge, or only non-dependency edges, Definition 13 excludes that assessment from the dependency su...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR15:PRRT_kwDOTH_vCM6OOImg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/proofs/FARE-P012-dependency-components.md' (SHA-256 9daf71ff7235bfd0c7832d219b8d21858fe21273c00ce093c25283699c41c298).
  - Current repository evidence at 'frameworks/FARE/proofs/FARE-P012-dependency-components.md:23': 'Demonstrate that every assessment node in a dependency subgraph belongs to exactly one weak dependency component of that dependency subgraph.'.

### PR16:PRRT_kwDOTH_vCM6OPFvc

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARE/meta/README.md:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/16#discussion_r3520915239
- Claim: **P2 Badge Remove unbacked meta-theorem coverage claims** With this commit the only files in 'frameworks/FARE/meta' are M001 and M002, but this sentence says FARE meta-theorems establish traceability, investigation soundness, and proof s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR16:PRRT_kwDOTH_vCM6OPFvc found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/meta/README.md' (SHA-256 bbb669b560a617657744e3e889d3c0867ea5a481808b594a67074398552fdb80).
  - Current repository evidence at 'frameworks/FARE/meta/README.md:9': 'FARE meta-theorems establish properties of the framework, including dependency ordering, definition uniqueness, traceability, consistency, investigation soundness, and proof soundness.'.

### PR19:PRRT_kwDOTH_vCM6OSLhU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-distance.md:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/19#discussion_r3522007433
- Claim: **P2 Badge Make cost models cover every path being measured** This definition allows a transformation cost model to assign costs only to admissible transformations “under consideration,” but the distance definition below still takes the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR19:PRRT_kwDOTH_vCM6OSLhU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/mathematics/definitions/evaluation-distance.md' (SHA-256 ec3dd0e3f0d51ccf2a76e5bd194073b83beb3afa3811572a1ad75c401c9f6493).
  - Current repository evidence at 'frameworks/FARE/mathematics/definitions/evaluation-distance.md:43': 'A **transformation cost model** assigns a non-negative cost to every admissible evaluation transformation under consideration.'.

### PR19:PRRT_kwDOTH_vCM6OSLhV

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/19#discussion_r3522007434
- Claim: **P2 Badge Disambiguate 'N(E)' for chosen neighborhood systems** This introduces 'N(E)' as the collection supplied by a particular neighborhood system, but the existing Neighborhood Family section later defines 'N(E)' as every admissible...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR19:PRRT_kwDOTH_vCM6OSLhV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md' (SHA-256 701618c622e74ac6b85bce90fbd746400f0d7636f89a3f3cabb9349e80da8c77).
  - Current repository evidence at 'frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md:44': 'A **neighborhood system** assigns to each evaluation 'E' a collection 'N(E)' of neighborhoods centered at 'E'.'.

### PR21:PRRT_kwDOTH_vCM6OUG3P

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/21#discussion_r3522698007
- Claim: **P2 Badge Consolidate project status into the existing status file** This adds a second current-status artifact while 'docs/PROJECT_STATUS[.]md' already states that it records the current state and should be updated when a significant m...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR21:PRRT_kwDOTH_vCM6OUG3P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:1': '# Project FAR Status'.

### PR21:PRRT_kwDOTH_vCM6OUG3Q

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:57`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/21#discussion_r3522698008
- Claim: **P2 Badge Align FARE expansion gates with the freeze policy** This development-order rule allows FARE Mathematics to expand when FARO or FARA require it, but the same new status document's governance rules and the new milestone freeze p...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR21:PRRT_kwDOTH_vCM6OUG3Q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:57': 'v0.3.1 packages repository maturity work around the v0.3.0 baseline: README command center, dashboard generation, repository index, dashboard metrics, improved health diagnostics, GitHub Actions, release-readiness reporting, and repository '.

### PR22:PRRT_kwDOTH_vCM6OWe3W

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FAR/README.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/22#discussion_r3523523890
- Claim: **P2 Badge Align FARO status with existing FARO docs** This new status says FARO development should only begin after FAR stabilizes, but the repository already contains an active 'frameworks/FARO/' tree whose README states that FARO cons...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR22:PRRT_kwDOTH_vCM6OWe3W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FAR/README.md' (SHA-256 e01275de69493cc5e2fe23d4d32ece40af7346f921e155688456995be49a77c7).
  - Current repository evidence at 'frameworks/FAR/README.md:25': '## Framework Role'.

### PR23:PRRT_kwDOTH_vCM6OWoT2

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FAR/README.md:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/23#discussion_r3523577639
- Claim: **P2 Badge Advance FAR status past the completed Phase 2 gate** This updated status is now inconsistent with the same commit's audit record, which marks Phase 2 complete and says FAR is ready to proceed to Phase 3 methodology audit; 'met...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR23:PRRT_kwDOTH_vCM6OWoT2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FAR/README.md' (SHA-256 e01275de69493cc5e2fe23d4d32ece40af7346f921e155688456995be49a77c7).
  - Current repository evidence at 'frameworks/FAR/README.md:21': 'Future FAR changes should be driven by concrete downstream requirements, worked examples, or validated methodological deficiencies.'.

### PR23:PRRT_kwDOTH_vCM6OWoTz

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/23#discussion_r3523577636
- Claim: **P2 Badge Define candidate generation in the canonical workflow** This closes the earlier gap by saying candidate generation is explicitly placed in Stage 6, but the commit never updates 'frameworks/FAR/workflow.md', which the FAR docs ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR23:PRRT_kwDOTH_vCM6OWoTz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md' (SHA-256 b62a484b685bea9b0a084c78f72da8f3898bd512bca2d01a997b0bc49625b428).
  - Current repository evidence at 'docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md:135': 'Candidate generation is explicitly placed within Stage 6 — Perform Reasoning.'.

### PR24:PRRT_kwDOTH_vCM6OXXCe

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md:253`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/24#discussion_r3523827593
- Claim: **P2 Badge Do not mark Phase 3 complete while application is stale** The audit lists 'frameworks/FAR/application.md' as reviewed, but that document was not updated for this Phase 3 policy change: its application requirements still end at...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR24:PRRT_kwDOTH_vCM6OXXCe found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md' (SHA-256 fbb051973e105bc6334a4eb6d2f83c2554c03795bdc1e8bb27ee2e4562ade44d).
  - Current repository evidence at 'docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md:253': 'All Phase 3 corrections have been implemented.'.

### PR24:PRRT_kwDOTH_vCM6OXXCg

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FAR/workflow.md:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/24#discussion_r3523827596
- Claim: **P2 Badge Require revision records in the canonical workflow** The new stability criterion says FAR shall require revision records whenever an investigation revisits an earlier stage ('FAR-v1.0-criteria.md' line 67), but the canonical w...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR24:PRRT_kwDOTH_vCM6OXXCg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FAR/workflow.md' (SHA-256 e32e425b80159da92925eb1a103fdc56db21b8166bc0a185dadf5c3b23ae81bb).
  - Current repository evidence at 'frameworks/FAR/workflow.md:121': 'Every return to an earlier stage should record:'.

### PR26:PRRT_kwDOTH_vCM6OXzM2

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md:284`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/26#discussion_r3523976424
- Claim: **P2 Badge Keep FAR status docs synchronized before passing the audit** This pass is used to clear the v1.0 gate, but in the repository context I inspected 'frameworks/FAR/methodology.md' still says the current work is the Phase 3 method...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR26:PRRT_kwDOTH_vCM6OXzM2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md' (SHA-256 4fdfa9127df940fa360d2946506d7201d27e14a516f3a95c2c777b5a146f8ecd).
  - Current repository evidence at 'docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md:284': '| Methodology, workflow, and application synchronized | Pass |'.

### PR27:PRRT_kwDOTH_vCM6OX64p

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/27#discussion_r3524017502
- Claim: **P2 Badge Keep the FARE expansion rule consistent** This broadens the governance rule to allow new FARE definitions when FAR, FARO, or FARA requires them, but the same status document still says FARE Mathematics v0.1 “shall not expand u...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR27:PRRT_kwDOTH_vCM6OX64p found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:104': ''.

### PR27:PRRT_kwDOTH_vCM6OX64q

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md:33`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/27#discussion_r3524017503
- Claim: **P2 Badge Update FAR status before freezing it** This milestone designates 'frameworks/FAR/README.md' as Stable, but that file's Current Status still says FAR is only eligible for a stable freeze after review/merge and that FARO should ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR27:PRRT_kwDOTH_vCM6OX64q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md' (SHA-256 f0004f462711a6722ac915273ad090ee128a4807e4ffa2ade77c8a5596b2455d).
  - Current repository evidence at 'docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md:33': '- 'frameworks/FAR/README.md''.

### PR28:PRRT_kwDOTH_vCM6OYVb4

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARO/architecture.md:84`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/28#discussion_r3524161830
- Claim: **P2 Badge Add the missing FARE dependency field** The architecture checklist says every FARO operation shall specify these dependencies, but it skips the 'FARE Dependency' field that 'operation-interface-standard.md' makes required, inc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR28:PRRT_kwDOTH_vCM6OYVb4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARO/architecture.md' (SHA-256 80e7fa3397249753b7af68b4de8667a2f29da94c1b3c9bf559d65bc1b54d91d3).
  - Current repository evidence at 'frameworks/FARO/architecture.md:84': '- boundary notes.'.

### PR28:PRRT_kwDOTH_vCM6OYVb5

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARO/execution.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/28#discussion_r3524161831
- Claim: **P2 Badge Clarify whether execution may determine admissibility** This exception makes execution operations allowed to determine admissibility when they use a defined FAR reasoning calculus, but the same new document states that “Execut...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR28:PRRT_kwDOTH_vCM6OYVb5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARO/execution.md' (SHA-256 d843f934cf1896a5c4907e02130acc29a670d109aa8ec4287ad70cd29037167b).
  - Current repository evidence at 'frameworks/FARO/execution.md:40': '- determine admissibility unless explicitly acting under a defined FAR reasoning calculus.'.

### PR29:PRRT_kwDOTH_vCM6OYXwk

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/29#discussion_r3524174855
- Claim: **P2 Badge Update FARO README status for Phase 8** When this status document moves active development to Phase 8, 'frameworks/FARO/README.md' still says FARO has entered Phase 7 architecture stabilization and its notes still tell readers...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR29:PRRT_kwDOTH_vCM6OYXwk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:11': 'The frozen comparison is complete: v1.0.0 resolved 0/2 runs and v1.0.1 resolved 0/2 runs on the single preregistered task. The observation is 'no_observed_resolution_difference'; both the outcome-blind integrity decision and bounded case de'.

### PR30:PRRT_kwDOTH_vCM6OYbcS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/30#discussion_r3524194993
- Claim: **P2 Badge Rework the failure-mode pass before advancing Phase 8** This pass result is not supported by the referenced category documents: in 'frameworks/FARO/{execution,reporting,operational-evaluation}.md', there is no category-level f...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR30:PRRT_kwDOTH_vCM6OYbcS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md' (SHA-256 5460573bb377df8df4f1f14f091e3fbbfd689c3500530eaa60a545117d88f6b5).
  - Current repository evidence at 'docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md:77': 'Auditing, reporting, execution, and operational evaluation documents distinguish incomplete, invalid, missing-input, and boundary-related failures at the category level.'.

### PR31:PRRT_kwDOTH_vCM6OYchc

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/31#discussion_r3524200707
- Claim: **P2 Badge Keep the audit-record gate in the criteria** When the stable milestone relies on this Phase 9 finding, it now claims the criteria document records the required audit records, but this same commit replaced the prior 'Audit Reco...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR31:PRRT_kwDOTH_vCM6OYchc found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md' (SHA-256 439282fac9e38bbbe7a4735960faae8068e0556e42cc283d34d6b89c1de0da26).
  - Current repository evidence at 'docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md:135': 'The criteria document records the required architecture, operation categories, interfaces, boundaries, and audit records.'.

### PR32:PRRT_kwDOTH_vCM6OYfSA

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `README.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/32#discussion_r3524214858
- Claim: **P2 Badge Update canonical FARO status before declaring stability** This declaration conflicts with unchanged canonical FARO docs: 'frameworks/FARO/README.md:13-15' still says FARO is only eligible and not formally v1.0 Stable until the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR32:PRRT_kwDOTH_vCM6OYfSA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'README.md' (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at 'README.md:13': ''.

### PR33:PRRT_kwDOTH_vCM6OYgsA

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:64`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/33#discussion_r3524222522
- Claim: **P2 Badge Do not let unproven FARM drive FARE expansion** While the Phase 10 audit still has to decide whether FARM should exist and the milestone says FARM must prove responsibilities before canonical expansion, this effective-immediat...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR33:PRRT_kwDOTH_vCM6OYgsA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:64': ''.

### PR34:PRRT_kwDOTH_vCM6OYk4w

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/FARM-PHASE-10-ARCHITECTURE-AUDIT.md:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/34#discussion_r3524245031
- Claim: **P2 Badge Archive the superseded Phase 10 audit record** By deleting this initiated audit instead of archiving or recording it as superseded, the current tree loses the only in-repository provenance that FARM planning originally opened ...
- Rationale: The artifact reviewed by finding PR34:PRRT_kwDOTH_vCM6OYk4w has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'docs/audits/FARM-PHASE-10-ARCHITECTURE-AUDIT.md' does not exist ('test -e' is false).

### PR35:PRRT_kwDOTH_vCM6OYx2-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `frameworks/FARM/README.md:31`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/35#discussion_r3524315327
- Claim: **P2 Badge Add FARM canonical documents to the canonical map** These new FARM files are now presented as canonical documents, but 'docs/CANONICAL_MAP.md' still has no FARM section or entries (I checked the map and repo-wide FARM referenc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR35:PRRT_kwDOTH_vCM6OYx2- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'frameworks/FARM/README.md' (SHA-256 be455ae44fc227c89317c3dffce2f6cc193d6c0dd8f8148cc426a3939c598f30).
  - Current repository evidence at 'frameworks/FARM/README.md:31': '---'.

### PR36:PRRT_kwDOTH_vCM6OZFPU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/36#discussion_r3524419058
- Claim: **P2 Badge Sync the FARM README before closing Phase 4** With this update, project status says Phase 3 and Phase 4 are complete, but 'frameworks/FARM/README.md' still says the Phase 3 methodology audit is initiated and its next step is t...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR36:PRRT_kwDOTH_vCM6OZFPU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:11': 'The frozen comparison is complete: v1.0.0 resolved 0/2 runs and v1.0.1 resolved 0/2 runs on the single preregistered task. The observation is 'no_observed_resolution_difference'; both the outcome-blind integrity decision and bounded case de'.

### PR37:PRRT_kwDOTH_vCM6OZK28

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/37#discussion_r3524449019
- Claim: **P2 Badge Align the FARM stable component scope** This adds the Phase 1 through Phase 4 audit records to the FARM stable component set, but the new 'docs/milestones/FARM-v1.0-Stable.md' Stable Components section lists only the eight 'fr...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR37:PRRT_kwDOTH_vCM6OZK28 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:53': '### Project FAR v0.3.1 Repository Maturity and Automation'.

### PR38:PRRT_kwDOTH_vCM6ObcXR

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/38#discussion_r3525237179
- Claim: **P2 Badge Recheck placeholder search before recording a pass** The repository already contains matches for this search, so the audit records a false preliminary pass. In the parent tree, 'git grep -n -i -E '\b(dummy|temp|placeholder|TOD...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR38:PRRT_kwDOTH_vCM6ObcXR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md' (SHA-256 0a2ec390012393c0c8a66acd689943bf459b40d259247e78b17faef96ee86a3e).
  - Current repository evidence at 'docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:47': '- FARM v1.0 Stable.'.

### PR39:PRRT_kwDOTH_vCM6ObfIA

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:63`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/39#discussion_r3525252152
- Claim: **P2 Badge Reopen the FARE alignment check** This pass is inaccurate for the post-v1 stack: in this commit, 'README.md''s navigation/reading order lists framework material for FAR/FARA/FARO/FARM but omits FARE, and 'docs/CANONICAL_MAP.md...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR39:PRRT_kwDOTH_vCM6ObfIA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md' (SHA-256 0a2ec390012393c0c8a66acd689943bf459b40d259247e78b17faef96ee86a3e).
  - Current repository evidence at 'docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:63': 'Assessment: pass.'.

### PR40:PRRT_kwDOTH_vCM6OcdQT

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/CANONICAL_MAP.md:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/40#discussion_r3525600994
- Claim: **P2 Badge Restore the missing FARE canonical components** When contributors use this new map as the FARE navigation hub, it drops canonical FARE components that the authoritative FARE spec defines at 'frameworks/FARE/specification.md' l...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR40:PRRT_kwDOTH_vCM6OcdQT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/CANONICAL_MAP.md' (SHA-256 9fae5238b7a853b517252f364f907623ab8729d92dd94b6aaf98194534f1b76e).
  - Current repository evidence at 'docs/CANONICAL_MAP.md:69': '| FAR Dependency Graph | '../frameworks/FAR/dependency-graph.md' | Records FAR dependency order. |'.

### PR48:PRRT_kwDOTH_vCM6Ofq_j

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/roadmap/v0.2.0-next-phase.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/48#discussion_r3526754282
- Claim: **P2 Badge Align the roadmap version with the active milestone** This introduces a new 'v0.2.0' next-phase roadmap even though the repository already records 'docs/releases/project-far-v0.4.md' as the active roadmap milestone and lists t...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR48:PRRT_kwDOTH_vCM6Ofq_j found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/roadmap/v0.2.0-next-phase.md' (SHA-256 326173f01d0461c792cc3e1b6f25926c094a241bf80b9d8f23cbd2abb8e7b117).
  - Current repository evidence at 'docs/roadmap/v0.2.0-next-phase.md:5': 'This document records the next development phase after the initial public release.'.

### PR49:PRRT_kwDOTH_vCM6Of2J_

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/verify_theory.py:201`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/49#discussion_r3526816607
- Claim: **P2 Badge Include non-theorem nodes in the cycle graph** When proposition/lemma metadata is validated, dependencies involving those IDs are accepted as known dependencies but never inserted into the graph passed to 'validate_no_cycles()...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR49:PRRT_kwDOTH_vCM6Of2J_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/verify_theory.py' (SHA-256 884e3d178d04275f2ea97bdf75f5d1c7d1537f083de222c979bc5a3b889cbf63).
  - Current repository evidence at 'tools/verify_theory.py:201': 'aliases.add(str(alias))'.

### PR49:PRRT_kwDOTH_vCM6Of2KD

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/metadata/generated-proposition-index.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/49#discussion_r3526816612
- Claim: **P2 Badge Include P-009 in the generated index** 'theory/metadata/propositions.yaml' adds 'P-009' and the proposition catalog contains it, but the committed generated proposition index stops at 'P-008'. Anyone using this generated index...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR49:PRRT_kwDOTH_vCM6Of2KD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/metadata/generated-proposition-index.md' (SHA-256 75d664a4afd5bc4827f267a2e067d8c69cbabd81c6303d933e88bb9c0cdcc26f).
  - Current repository evidence at 'theory/metadata/generated-proposition-index.md:14': '| P-008 | Resolution Dependence | Established | 'theory/proofs/P-001-first-propositions.md' | resolution execution under a reasoning calculus | n/a | n/a |'.

### PR51:PRRT_kwDOTH_vCM6OgLyL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/verify_theory.py:154`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/51#discussion_r3526938355
- Claim: **P2 Badge Preserve ID checks for existing catalogs** Because this helper is still used for propositions and lemmas, accepting a title match means a metadata entry with a mistyped or stale 'P-*'/'L-*' id now passes as long as the source ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR51:PRRT_kwDOTH_vCM6OgLyL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/verify_theory.py' (SHA-256 884e3d178d04275f2ea97bdf75f5d1c7d1537f083de222c979bc5a3b889cbf63).
  - Current repository evidence at 'tools/verify_theory.py:154': 'raise VerificationError(f"{prefix} entry missing fields {sorted(missing)}: {item}")'.

### PR52:PRRT_kwDOTH_vCM6OgR7W

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-001.proof.yaml:30`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/52#discussion_r3526972612
- Claim: **P2 Badge Add the definition dependency to T-001 metadata** This proof object now makes 'DEF-019' an explicit premise for proving 'T-001', but 'theory/metadata/theorems.yaml' still lists only 'L-001' through 'L-005' as T-001 dependencie...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR52:PRRT_kwDOTH_vCM6OgR7W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-001.proof.yaml' (SHA-256 c592af3b04c3af82dad53d23a354e3c9bc414296f7d2756316a2783a7bb518eb).
  - Current repository evidence at 'theory/proof-objects/T-001.proof.yaml:30': 'source: DEF-019'.

### PR53:PRRT_kwDOTH_vCM6OgVPb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-002.proof.yaml:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/53#discussion_r3526991258
- Claim: **P2 Badge Model the countermodel obligations as inputs** Here 'p2' is only the conditional proof method and 'p4' only states L-001's necessity claim; the proof object never establishes the antecedent that a countermodel with the other f...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR53:PRRT_kwDOTH_vCM6OgVPb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-002.proof.yaml' (SHA-256 32032af6bafeea29b6156a3badf2aa230d96a93bf3d88f677d548cbeb797c87b).
  - Current repository evidence at 'theory/proof-objects/T-002.proof.yaml:42': 'statement: Representation is not eliminable in favor of the other four primitives under the current deletion-only reduction standard.'.

### PR54:PRRT_kwDOTH_vCM6OgbqU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-003.proof.yaml:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/54#discussion_r3527026847
- Claim: **P2 Badge Prove T exists before conjoining it** When 'R' has no specified transition executions, 's6' only establishes a conditional/permission that 'T' may be empty or partial; it does not assert an existing trace component for that ca...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR54:PRRT_kwDOTH_vCM6OgbqU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-003.proof.yaml' (SHA-256 dfd643f02cbbdcec0620ffb475a9bd9fc89e3f43d3ca126190c1f1b1e73c5d4e).
  - Current repository evidence at 'theory/proof-objects/T-003.proof.yaml:77': 'statement: R has C and T.'.

### PR54:PRRT_kwDOTH_vCM6OgbqY

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-003.proof.yaml:97`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/54#discussion_r3527026851
- Claim: **P2 Badge Use universal generalization for arbitrary R** This step derives a universal theorem from the construction for an arbitrary 'R', but labels the inference as 'universal_instantiation', which goes in the opposite direction: from...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR54:PRRT_kwDOTH_vCM6OgbqY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-003.proof.yaml' (SHA-256 dfd643f02cbbdcec0620ffb475a9bd9fc89e3f43d3ca126190c1f1b1e73c5d4e).
  - Current repository evidence at 'theory/proof-objects/T-003.proof.yaml:97': 'statement: Every reasoning process within the stated Project FAR scope admits a FAR representation.'.

### PR55:PRRT_kwDOTH_vCM6OgvoF

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-005.proof.yaml:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/55#discussion_r3527139355
- Claim: **P2 Badge Preserve L-008 in the T-005 proof object** For T-005, 'theory/metadata/theorems.yaml' lists 'L-008' as a dependency, and 'theory/lemmas/core-lemmas.md' uses that lemma to require source state, target state, rule, and admissibi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR55:PRRT_kwDOTH_vCM6OgvoF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-005.proof.yaml' (SHA-256 e37a59886a643d8260b9f094e4c9476d0e16876cf5b77855dca9ef8dc45072d9).
  - Current repository evidence at 'theory/proof-objects/T-005.proof.yaml:53': 'statement: e can be represented in FAR by a transition signature.'.

### PR55:PRRT_kwDOTH_vCM6OgvoG

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-006.proof.yaml:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/55#discussion_r3527139356
- Claim: **P2 Badge Do not add an uncited induction premise** T-006 is registry-relative: its documented dependencies are the derived-concept registry and canonical notation, but this proof object introduces 'induction principle over registry dep...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR55:PRRT_kwDOTH_vCM6OgvoG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-006.proof.yaml' (SHA-256 b7bf4570a43b57da535f9c9e9a1ae32fb06cf9b5a201dc0ed00e2d7ab8052224).
  - Current repository evidence at 'theory/proof-objects/T-006.proof.yaml:19': 'statement: If every concept at registry depth n or lower is constructible from P, then any concept at depth n + 1 deriving from those concepts is constructible from P by substitution.'.

### PR56:PRRT_kwDOTH_vCM6OhRaY

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-008.proof.yaml:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332927
- Claim: **P2 Badge Establish interpretation preservation before concluding semantics** For canonical representations where the role pairing has only been shown to preserve structure/admissibility/trace order, 's3' is still conditional on the pai...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRaY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-008.proof.yaml' (SHA-256 0e6a778db636a6894d498e92e2c8f6e4f3f95f0b436c4daab13b26e3b7c590e4).
  - Current repository evidence at 'theory/proof-objects/T-008.proof.yaml:45': 'rule: definition_unfolding'.

### PR56:PRRT_kwDOTH_vCM6OhRab

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-009.proof.yaml:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332931
- Claim: **P2 Badge Keep L-007's termination precondition explicit** For a finite FAR representation whose supplied ordering/labeling/redundancy rules are not known to strictly reduce unresolved items, L-007 does not by itself prove termination; ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRab found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-009.proof.yaml' (SHA-256 23cb16efa983e035cba420b4795b246594c276fbf2ce20b79446ffed5d924103).
  - Current repository evidence at 'theory/proof-objects/T-009.proof.yaml:28': 'inputs: [s1, s2]'.

### PR56:PRRT_kwDOTH_vCM6OhRac

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-010.proof.yaml:49`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332933
- Claim: **P2 Badge Avoid applying T-009 outside finite normalized cases** T-010's premise is only a complete FAR representation, but T-009 is scoped to finite FAR representations with supplied normalization rules. For complete representations th...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRac found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-010.proof.yaml' (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at 'theory/proof-objects/T-010.proof.yaml:49': 'justification: Applies the trace/process distinction to avoid reconstructing private, hidden, or otherwise unrepresented features.'.

### PR57:PRRT_kwDOTH_vCM6OpqRi

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-012.proof.yaml:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/57#discussion_r3530345511
- Claim: **P2 Badge Attribute Q-equivalence definitions to an existing source** These premises cite 'FAR-model-theory', but the model-theory file only defines equivalence as preservation over a property set ('theory/model-theory/FAR-model-theory....
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR57:PRRT_kwDOTH_vCM6OpqRi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-012.proof.yaml' (SHA-256 db3a7718bb716aa6debde681e63cec929d5c7805a0d86123e3008b82512beeaf).
  - Current repository evidence at 'theory/proof-objects/T-012.proof.yaml:16': 'statement: "A and B are Q-equivalent exactly when every property in Q holds in A exactly when the corresponding property holds in B."'.

### PR58:PRRT_kwDOTH_vCM6Op8yy

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_proof_object.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/58#discussion_r3530450208
- Claim: **P2 Badge Require more than word overlap for conclusions** When a proof object changes the final step and 'conclusion' to a weaker or contradictory phrase that reuses theorem words, this ratio can still pass; for example, a T-003 proof ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR58:PRRT_kwDOTH_vCM6Op8yy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_proof_object.py' (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at 'tools/check_proof_object.py:123': ''.

### PR61:PRRT_kwDOTH_vCM6OrXNb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/language/statement-schema.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/61#discussion_r3530966646
- Claim: **P2 Badge Allow existing artifact statement kinds** When this schema is used to validate current metadata, this allowed set omits the values the repository already stores for statement objects ('theorem', 'proposition', 'lemma', 'defini...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR61:PRRT_kwDOTH_vCM6OrXNb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/language/statement-schema.md' (SHA-256 ec2de2f251a787fb9217d31242792d314f9c386df5d989c7131f2f3acc0f1e61).
  - Current repository evidence at 'theory/language/statement-schema.md:25': 'kind: universal | existential | definitional | conditional | equivalence | preservation | construction | validation | classification | meta'.

### PR64:PRRT_kwDOTH_vCM6OuI1o

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_proof_object.py:329`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/64#discussion_r3531970829
- Claim: **P2 Badge Accept symbolic antecedents for ASCII modus ponens** When a proof object uses the documented modus-ponens shape 'P' plus 'P -> Q' (the same symbolic content added in the new fixture), the new '->' vocabulary check succeeds but...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR64:PRRT_kwDOTH_vCM6OuI1o found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_proof_object.py' (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at 'tools/check_proof_object.py:329': 'errors.append(f"step {step_id} conjunction_intro requires at least two inputs")'.

### PR64:PRRT_kwDOTH_vCM6OuI1r

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_proof_object.py:311`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/64#discussion_r3531970832
- Claim: **P2 Badge Preserve canonical SemanticContent vocabulary matches** For a 'semantic_preservation' step whose inputs express semantic content only in canonical notation such as 'SemanticContent(Int1, r)' and do not also cite 'T-004'/'DEF-0...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR64:PRRT_kwDOTH_vCM6OuI1r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_proof_object.py' (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at 'tools/check_proof_object.py:311': 'if not sources:'.

### PR66:PRRT_kwDOTH_vCM6OuixP

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/evaluate_reasoning_systems.py:195`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/66#discussion_r3532118049
- Claim: **P2 Badge Fail CI when any fixture fails classification** When a reasoning-system fixture is syntactically valid but missing the 'reasoning_system' mapping or using an unsupported verdict, 'classify_fixture()' reports 'fails fixture', b...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR66:PRRT_kwDOTH_vCM6OuixP found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/evaluate_reasoning_systems.py' (SHA-256 64d4fd1e7a3dd1f125b8b3020f7be7f01ed552dff7425e477538b286d92fb0de).
  - Current repository evidence at 'tools/evaluate_reasoning_systems.py:195': 'return 0'.

### PR70:PRRT_kwDOTH_vCM6OvPir

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `README.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/70#discussion_r3532377343
- Claim: **P2 Badge Synchronize the README release pointers** When readers use the README for release navigation, this new section says v0.2.0 is the latest release, but the same README still has a 'Releases' section listing only v0.1.0 and the t...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR70:PRRT_kwDOTH_vCM6OvPir found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'README.md' (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at 'README.md:14': 'The registered Universal Proof Program 'POST-TUE-UPP-001' is complete. Its terminal adjudication is:'.

### PR71:PRRT_kwDOTH_vCM6OvQSt

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/releases/release-publication-instructions-v0.2.0.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/71#discussion_r3532381647
- Claim: **P2 Badge Pin the release target to an exact commit** If publication happens after any later commit lands on 'main', this instruction tells the releaser to create the 'v0.2.0' tag on that newer tree, so the frozen v0.2.0 evidence baseli...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR71:PRRT_kwDOTH_vCM6OvQSt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/releases/release-publication-instructions-v0.2.0.md' (SHA-256 863ca953de9b15fcb8756232c84c124edee014d4fd2808f7d2e3051cd829620d).
  - Current repository evidence at 'docs/releases/release-publication-instructions-v0.2.0.md:13': '- Target: latest 'main' after the finalization PR is merged'.

### PR72:PRRT_kwDOTH_vCM6Ovhp9

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/evaluate_primitive_sufficiency.py:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/72#discussion_r3532480869
- Claim: **P2 Badge Preserve registry validation output for malformed entries** When a registry entry is missing a required field, 'validate_entries()' records the error but 'render_report()' immediately indexes 'entry["classification"]', so the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR72:PRRT_kwDOTH_vCM6Ovhp9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/evaluate_primitive_sufficiency.py' (SHA-256 f320561ebe726bb9f251e61174da5d9293ba9a4f434b5f58a1b4e9e32b0c0eff).
  - Current repository evidence at 'tools/evaluate_primitive_sufficiency.py:73': 'classification_counts = Counter(entry["classification"] for entry in entries)'.

### PR74:PRRT_kwDOTH_vCM6Owd-U

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/evidence-registry.yaml:124`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/74#discussion_r3532823883
- Claim: **P2 Badge Use the fixture classification taxonomy** 'classification' is the fixture/evidence classification consumed by the falsification harness, whose documented valid values are 'fits FAR', 'extends FAR', 'candidate counterexample', ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR74:PRRT_kwDOTH_vCM6Owd-U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/evidence-registry.yaml' (SHA-256 3a27c03b39e73880f21cdde22addb8dd2bd9bb6d52b1077ac2aaca699377e95c).
  - Current repository evidence at 'theory/evaluation/evidence-registry.yaml:124': 'system: Modal logic'.

### PR74:PRRT_kwDOTH_vCM6Owd-X

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/primitive-sufficiency-report.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/74#discussion_r3532823886
- Claim: **P2 Badge Recompute the fits-FAR headline count** The registry now has 7 entries with 'classification: fits FAR' and only 2 entries with 'registry_resolution: fits FAR'; the reported 9 is the sum of those two sets, double-counting PS-02...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR74:PRRT_kwDOTH_vCM6Owd-X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/primitive-sufficiency-report.md' (SHA-256 1ba707a03ad5ef408d82f54353cec258fd1e3ea919d63513505eaad75c9cfd02).
  - Current repository evidence at 'docs/reports/primitive-sufficiency-report.md:14': '- Fits FAR by registry resolution: 2'.

### PR75:PRRT_kwDOTH_vCM6Owjky

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/run_adversarial_suite.py:164`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/75#discussion_r3532856039
- Claim: **P2 Badge Cross-check the pressure registry** This runner only loads and validates '--suite', so the new 'theory/falsification/primitive-pressure-registry.yaml' is never read. Because that registry duplicates the suite’s primitive/syste...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR75:PRRT_kwDOTH_vCM6Owjky found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/run_adversarial_suite.py' (SHA-256 07c4a7fdc6f5314088082f5b657fbfcda69a9d0b3237bec96b89cb339295d4c1).
  - Current repository evidence at 'tools/run_adversarial_suite.py:164': 'errors = validate_suite(data)'.

### PR76:PRRT_kwDOTH_vCM6OwvGp

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/falsification/adversarial-test-suite.yaml:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/76#discussion_r3532924506
- Claim: **P2 Badge Recognize the new adversarial status labels** When the suite is summarized with 'tools/run_adversarial_suite.py', this new label (and the new 'conservative extension'/'unresolved pressure' labels) is not in the runner's 'PASSE...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR76:PRRT_kwDOTH_vCM6OwvGp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/falsification/adversarial-test-suite.yaml' (SHA-256 d45b3463188610731165a4aecda865b713126e6c34ee1afb9407aedfa1f31a93).
  - Current repository evidence at 'theory/falsification/adversarial-test-suite.yaml:12': 'current_status: resolved by existing primitive'.

### PR77:PRRT_kwDOTH_vCM6Ow2uM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/releases/github-release-v0.3.0.md:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/77#discussion_r3532968753
- Claim: **P2 Badge Use release-safe links in GitHub notes** If this file is pasted into a GitHub Release body, these '../reports/...' and same-directory relative links are no longer resolved relative to 'docs/releases'; they resolve from the rel...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR77:PRRT_kwDOTH_vCM6Ow2uM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/releases/github-release-v0.3.0.md' (SHA-256 a7859f9984d5b51a2b3b2d9aef03afaf467c6c2e111371c8f44b93ccf541e7c2).
  - Current repository evidence at 'docs/releases/github-release-v0.3.0.md:7': 'Highlights include:'.

### PR80:PRRT_kwDOTH_vCM6Ox91X

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_internal_links.py:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/80#discussion_r3533389790
- Claim: **P2 Badge Restrict YAML extraction to actual path fields** For YAML files that contain slash-delimited terms in prose or titles, this extracts those terms as repository paths even when they are not links; for example the current repo re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR80:PRRT_kwDOTH_vCM6Ox91X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_internal_links.py' (SHA-256 99a381e80ebf20150db1894d6cd90f909bee3b54e48a8ee00160494896d2625a).
  - Current repository evidence at 'tools/check_internal_links.py:46': 'line_no=int(anchor[1:])'.

### PR80:PRRT_kwDOTH_vCM6Ox91b

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_internal_links.py:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/80#discussion_r3533389794
- Claim: **P2 Badge Resolve YAML repository paths from the root** When a nested YAML file contains a repository-root-relative path, this resolves it relative to the YAML file's directory and reports a false broken link; for example 'theory/metada...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR80:PRRT_kwDOTH_vCM6Ox91b found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_internal_links.py' (SHA-256 99a381e80ebf20150db1894d6cd90f909bee3b54e48a8ee00160494896d2625a).
  - Current repository evidence at 'tools/check_internal_links.py:57': "print('Internal links OK')".

### PR81:PRRT_kwDOTH_vCM6O9Ugn

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-validation-methodology.md:82`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/81#discussion_r3537532171
- Claim: **P2 Badge Require reproducible evidence in external reports** The reporting standard lets an external-system report be complete with only mapping/classification/justification prose, but no source/version, fixture, execution record, obse...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR81:PRRT_kwDOTH_vCM6O9Ugn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-validation-methodology.md' (SHA-256 54f2f30fe0c9ed6c7c68ff5dea10000e32f7ac75378c4edfdb4d2236c19258cb).
  - Current repository evidence at 'theory/evaluation/external-validation-methodology.md:82': '7. Does it require a conservative extension?'.

### PR81:PRRT_kwDOTH_vCM6O9Ugr

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-validation-registry.yaml:24`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/81#discussion_r3537532174
- Claim: **P2 Badge Classify Coq consistently as conservative** Under the new classification rules, 'fits FAR' is for systems that do not need domain-specific extension machinery, while 'conservative extension' is for systems requiring domain-spe...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR81:PRRT_kwDOTH_vCM6O9Ugr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-validation-registry.yaml' (SHA-256 fb34615057c80821d4ff46f7e3586cc15976c4a0056b4cd12c6fb89436b88318).
  - Current repository evidence at 'theory/evaluation/external-validation-registry.yaml:24': 'system: Coq'.

### PR82:PRRT_kwDOTH_vCM6PEMp-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-systems/constraint-solving.md:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/82#discussion_r3540029610
- Claim: **P2 Badge Reclassify constraint solving by the stated rule** The report identifies “domain-specific propagation and search” as pressure and says domain-specific propagators are required, but the v0.4.0 external-validation methodology re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR82:PRRT_kwDOTH_vCM6PEMp- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-systems/constraint-solving.md' (SHA-256 4509bebe11c1bc4b240d17ac25d9db0d157dd61a099c18f71ffba5a6f99e8b27).
  - Current repository evidence at 'theory/evaluation/external-systems/constraint-solving.md:23': ''fits FAR''.

### PR82:PRRT_kwDOTH_vCM6PEMqC

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-systems/linear-logic.md:31`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/82#discussion_r3540029617
- Claim: **P2 Badge Add the required remaining-questions sections** The reporting standard in 'theory/evaluation/external-validation-methodology.md' says every system report must include remaining questions. This new report stops at Confidence, a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR82:PRRT_kwDOTH_vCM6PEMqC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-systems/linear-logic.md' (SHA-256 9d6c92724322281af99406e626a28dc4296d25b716eba574b7f7e9cd9eb0a682).
  - Current repository evidence at 'theory/evaluation/external-systems/linear-logic.md:31': 'Provisional.'.

### PR84:PRRT_kwDOTH_vCM6PEqVg

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_release_consistency.py:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/84#discussion_r3540197240
- Claim: **P2 Badge Anchor release-section detection to the heading** In the current README the first occurrence of “Release” is the badge near the top, so this unanchored regex captures the badge/intro block rather than the '## Latest Release' s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR84:PRRT_kwDOTH_vCM6PEqVg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_release_consistency.py' (SHA-256 8fbb1df37d7d9bae3d75ff91589da316c0d97952b14dac1ca4d4971eb4c61f63).
  - Current repository evidence at 'tools/check_release_consistency.py:14': "latest_section=re.search(r'(?is)(latest release|current release|release)[^\\n]*(?:\\n.{0,200}){0,8}', text)".

### PR84:PRRT_kwDOTH_vCM6PEqVh

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_repository_hygiene.py:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/84#discussion_r3540197241
- Claim: **P2 Badge Validate collected registry IDs before passing** When a non-adversarial registry file contains duplicate 'id' values, they are collected into 'registry_ids' here but that map is never inspected before the script prints success...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR84:PRRT_kwDOTH_vCM6PEqVh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_repository_hygiene.py' (SHA-256 6685979a37a6a30a3ab8a8bda1de8075718b4e992335917f6fbe0d9229ac1a7a).
  - Current repository evidence at 'tools/check_repository_hygiene.py:27': "data=yaml.safe_load(p.read_text(encoding='utf-8'))".

### PR85:PRRT_kwDOTH_vCM6PEvgp

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/generate_next_tasks.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/85#discussion_r3540227276
- Claim: **P2 Badge Resolve gap labels to actual editable files** When the gap row comes from a registry entry or primitive pressure, 'g['loc']' is a logical label such as 'PS-001' or 'Reasoning Calculus', not a repository path. This value is the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR85:PRRT_kwDOTH_vCM6PEvgp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/generate_next_tasks.py' (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at 'tools/generate_next_tasks.py:21': "if __name__=='__main__': raise SystemExit(main())".

### PR85:PRRT_kwDOTH_vCM6PEvgt

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/detect_research_gaps.py:55`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/85#discussion_r3540227280
- Claim: **P2 Badge Sort scanned markdown files before assigning gap IDs** When regenerating the committed reports, this loop emits TODO gaps in the filesystem's 'rglob' traversal order, which is not stable; in this checkout, running the planner ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR85:PRRT_kwDOTH_vCM6PEvgt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/detect_research_gaps.py' (SHA-256 ef103f9a0d426bc67b8b90f8c74e9de4894942c34bfea1d33f64bf4c67283cbd).
  - Current repository evidence at 'tools/detect_research_gaps.py:55': "if p.get('unresolved_pressures'): add(gaps,'unresolved primitive pressure',prim,'high','Analyze unresolved pressure before promoting stronger sufficiency claims.')".

### PR86:PRRT_kwDOTH_vCM6PFwgS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/detect_research_gaps.py:55`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/86#discussion_r3540603299
- Claim: **P2 Badge Sort TODO scans before assigning gap IDs** When the planner is rerun via 'make plan'/'python tools/self_advancement_plan.py', this filesystem-order traversal feeds directly into the 'gaps' list and then into 'enumerate(gaps, 1...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR86:PRRT_kwDOTH_vCM6PFwgS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/detect_research_gaps.py' (SHA-256 ef103f9a0d426bc67b8b90f8c74e9de4894942c34bfea1d33f64bf4c67283cbd).
  - Current repository evidence at 'tools/detect_research_gaps.py:55': "if p.get('unresolved_pressures'): add(gaps,'unresolved primitive pressure',prim,'high','Analyze unresolved pressure before promoting stronger sufficiency claims.')".

### PR87:PRRT_kwDOTH_vCM6PG65K

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/update_readme_dashboard.py:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/87#discussion_r3541030305
- Claim: **P2 Badge Select only completed releases for the current-release link** When a future roadmap document such as 'docs/releases/project-far-v0.4.md' exists, this max-version scan picks it even though that file is marked as an active roadm...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR87:PRRT_kwDOTH_vCM6PG65K found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/update_readme_dashboard.py' (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at 'tools/update_readme_dashboard.py:34': '- Candidate evidence: complete project-authored internal execution; not independent replication.'.

### PR89:PRRT_kwDOTH_vCM6PRccJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/repository-maintenance.yml:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/89#discussion_r3544797401
- Claim: **P2 Badge Preserve failures from piped maintenance commands** When any of these maintenance commands fails in the manual workflow, the failure can be masked because this step does not set 'shell: bash' or 'pipefail'; GitHub's workflow s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR89:PRRT_kwDOTH_vCM6PRccJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/repository-maintenance.yml' (SHA-256 cb5a911b10c43c9b4dba9c668b084030fcb8d4787d98c60556d04c1984eb1234).
  - Current repository evidence at '.github/workflows/repository-maintenance.yml:25': 'make dashboard 2>&1 | tee -a maintenance-summary.md'.

### PR90:PRRT_kwDOTH_vCM6PSOnQ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/update_readme_dashboard.py:36`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/90#discussion_r3545074995
- Claim: **P2 Badge Anchor release filename matching** Because this searches for 'vX.Y.Z' anywhere in every 'docs/releases/project-far-v*.md' file, auxiliary documents such as 'project-far-v0.4.0-theory-freeze.md' or 'project-far-v0.4.0-roadmap.m...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR90:PRRT_kwDOTH_vCM6PSOnQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/update_readme_dashboard.py' (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at 'tools/update_readme_dashboard.py:36': '## Historical Priority Tasks'.

### PR91:PRRT_kwDOTH_vCM6PSncK

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/91#discussion_r3545213004
- Claim: **P2 Badge Synchronize the v0.4 phase label** This changes the status page to say the active target is v0.4 analytical infrastructure, but the canonical README dashboard still says 'v0.4 external validation preparation', and 'tools/updat...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR91:PRRT_kwDOTH_vCM6PSncK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:123': '- FARM defect classification;'.

### PR91:PRRT_kwDOTH_vCM6PSncN

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/project-status.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/91#discussion_r3545213010
- Claim: **P2 Badge Preserve the removed governance rules** This abbreviated development order replaces the former Governance Rules section, including the stable-layer change controls and the rule that draft theorems are not accepted dependencies...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR91:PRRT_kwDOTH_vCM6PSncN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/project-status.md' (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at 'docs/project-status.md:135': 'CRE-002 is complete as a prospective semantic-licensing boundary result under Baseline 1.0, and CRE-002-EXT-001 is complete as a prospective bounded behavioral result under Baseline 1.1. All three official vocabularies completed the extensi'.

### PR92:PRRT_kwDOTH_vCM6PTVW9

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/self_advancement_plan.py:9`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/92#discussion_r3545471390
- Claim: **P2 Badge Stage generated dependency artifacts in dashboard workflow** When 'make dashboard' runs under the regenerate-dashboard action, this new pipeline now writes 'docs/reports/dependency-report.md', 'docs/reports/dependency-graph.js...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR92:PRRT_kwDOTH_vCM6PTVW9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/self_advancement_plan.py' (SHA-256 e7b8e7e3cd75c6b49628936f6c030f2f2f923daa55524a0be64d52526b2fc2b2).
  - Current repository evidence at 'tools/self_advancement_plan.py:9': "GEN=[ROOT/'README.md',ROOT/'docs/planning/dashboard-metrics.md',ROOT/'docs/planning/repository-index.md',ROOT/'docs/reports/project-status-generated.md',ROOT/'docs/reports/research-gap-report.md',ROOT/'docs/planning/next-actions.md',ROOT/'d".

### PR97:PRRT_kwDOTH_vCM6PXYJT

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-primitive-candidate-adjudication.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/97#discussion_r3546928509
- Claim: **P2 Badge Add an explicit artifact status** The root AGENTS instructions require compliance with 'docs/governance/research-execution-charter.md', which states that every artifact must have exactly one status from Accepted/Research/Provi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR97:PRRT_kwDOTH_vCM6PXYJT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-primitive-candidate-adjudication.md' (SHA-256 2489f1a82d48be662bf109070c0ff286e01030e5827a10d7e60eee996ef956f7).
  - Current repository evidence at 'docs/reports/ax001-primitive-candidate-adjudication.md:1': '# AX-001 Primitive Candidate Adjudication'.

### PR97:PRRT_kwDOTH_vCM6PXYJZ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-primitive-candidate-adjudication.md:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/97#discussion_r3546928515
- Claim: **P2 Badge Avoid making AX-001 depend on downstream standards** If this supported wording is used for the later AX-001 edit, it imports admissibility from the surrounding theory even though 'foundation-validation-report.md' stopped downs...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR97:PRRT_kwDOTH_vCM6PXYJZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-primitive-candidate-adjudication.md' (SHA-256 2489f1a82d48be662bf109070c0ff286e01030e5827a10d7e60eee996ef956f7).
  - Current repository evidence at 'docs/reports/ax001-primitive-candidate-adjudication.md:222': '''''.

### PR98:PRRT_kwDOTH_vCM6PXlsJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-wording-revision-report.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/98#discussion_r3547003884
- Claim: **P2 Badge Do not mark pending AX-001 evidence as accepted** This provenance claim says the canonical AX-001 rewrite was authorized by “accepted” prior reports, but the cited foundation report explicitly records Human Adjudication as pen...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR98:PRRT_kwDOTH_vCM6PXlsJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-wording-revision-report.md' (SHA-256 6bddcb44b8a7024843332683d898fa82873cfffa5c67c72d7e78a3f685687721).
  - Current repository evidence at 'docs/reports/ax001-wording-revision-report.md:5': 'This report records the canonical AX-001 wording revision authorized by the accepted prior AX-001 research reports. The revision retains Operation as the AX-001 candidate primitive and changes only the working characterization needed to rem'.

### PR99:PRRT_kwDOTH_vCM6PXsa5

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/ax001-stability-review.md:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/99#discussion_r3547041592
- Claim: **P2 Badge Carry forward unresolved necessity pressure** This Necessity PASS drops the unresolved necessity pressure already recorded in 'docs/reports/foundation-validation-report.md:76' and 'docs/reports/foundation-validation-report.md:...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR99:PRRT_kwDOTH_vCM6PXsa5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/ax001-stability-review.md' (SHA-256 e5c8ab51daba59132a57296c714c595566d39afb5a4356e00eff50d4a72de42c).
  - Current repository evidence at 'docs/reports/ax001-stability-review.md:69': 'Prior evidence found no successful non-circular reduction of Operation. The strongest replacement candidates did not eliminate primitive burden; they shifted it to reasoning states, transitions, rules, licensing, admissibility, or represent'.

### PR101:PRRT_kwDOTH_vCM6PYy6a

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/doctrine/isolation-classification.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/101#discussion_r3547436795
- Claim: **P2 Badge Record provenance before marking doctrine accepted** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', which limits artifact statuses to 'Accepted', 'Research', 'Provisional', 'Arch...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR101:PRRT_kwDOTH_vCM6PYy6a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/doctrine/isolation-classification.md' (SHA-256 7ecc2e234c833dbb6467fc416f68d861a934e2e332c55ff1f5b3704a4c1c4fdf).
  - Current repository evidence at 'docs/doctrine/isolation-classification.md:3': 'Status: Accepted Methodology'.

### PR102:PRRT_kwDOTH_vCM6PZNLb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/lemmas/core-lemmas.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/102#discussion_r3547586005
- Claim: **P2 Badge Define 'participating collection' before canonical use** When downstream users consume 'core-lemmas.md' as the canonical lemma source, this revised statement relies on 'participating collection of representations' as if it wer...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR102:PRRT_kwDOTH_vCM6PZNLb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/lemmas/core-lemmas.md' (SHA-256 fce9744c6d4efa0b23baacc417eae5eb5b952a3973939be6cf5f698998d138f9).
  - Current repository evidence at 'theory/lemmas/core-lemmas.md:25': 'No participating collection of representations satisfies Project FAR Axiom 2 unless it possesses representational structure.'.

### PR103:PRRT_kwDOTH_vCM6PZYQQ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/l003-validation-report.md:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/103#discussion_r3547648976
- Claim: **P2 Badge Track D-INV as a required L-003 dependency** The revised L-003 statement now makes 'within an investigation' part of the condition, and this row itself says that investigation context is necessary to state the clarified result...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR103:PRRT_kwDOTH_vCM6PZYQQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/l003-validation-report.md' (SHA-256 2aa53345742c37a234eb9c3cdce3f0a47db6d701a7469a019ba82c97681f7f90).
  - Current repository evidence at 'docs/reports/l003-validation-report.md:44': '| D-INV | Informative | Axiom 3 requires interpretation within an investigation, so the investigation context is necessary to state the clarified result. Because A3 already carries that contextual condition and the existing declared depende'.

### PR107:PRRT_kwDOTH_vCM6Pais0

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/l007-validation-report.md:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/107#discussion_r3548071738
- Claim: **P2 Badge Register the new L-007 proof obligations** This report states that the core proof now directly depends on finite unresolved-item measure and the no-new-unresolved-item condition, but it also records that no dependency registry...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR107:PRRT_kwDOTH_vCM6Pais0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/l007-validation-report.md' (SHA-256 0e2c5f8f145e91293f1721ea25b266b54da7239277ffd7d7eff05422b0776509).
  - Current repository evidence at 'docs/reports/l007-validation-report.md:60': 'No dependency registry or dependency graph modification was made. The core proof depends directly on finite FAR representation, normalization procedure, finite unresolved-item measure, and a no-new-unresolved-item condition. Candidate infla'.

### PR110:PRRT_kwDOTH_vCM6PcQlI

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-validation-consolidation.md:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/110#discussion_r3548711972
- Claim: **P2 Badge Avoid retroactively labeling earlier validations as I1** When readers use this consolidation as the single status artifact for the AX-001→T-001 chain, this sentence overstates the evidence for the first links: the L-001 report...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR110:PRRT_kwDOTH_vCM6PcQlI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-validation-consolidation.md' (SHA-256 da776b090e643e5efb3efe1db01cf828e1bdb1df4d24eb0331519e828dfd0764).
  - Current repository evidence at 'docs/reports/foundation-validation-consolidation.md:48': 'All independent evaluations were classified as I1 — Claimed Isolation unless otherwise stated in their reports. This means repository access was prohibited by instruction but not technically prevented by the execution environment.'.

### PR111:PRRT_kwDOTH_vCM6PctNL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proofs/T-002-primitive-independence.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/111#discussion_r3548874172
- Claim: **P2 Badge Update theorem catalogs after narrowing T-002** Because this line narrows T-002 from derivability to deletion-only eliminability, the companion catalogs now publish a stronger theorem than the proof establishes: 'theory/theore...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR111:PRRT_kwDOTH_vCM6PctNL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proofs/T-002-primitive-independence.md' (SHA-256 de20ee14b10b1e92137a5836c236130adbeac8533eee26a025dd620c3d9e671b).
  - Current repository evidence at 'theory/proofs/T-002-primitive-independence.md:11': 'Within the current framework and deletion-only reduction standard, none of the five primitives is eliminable in favor of the other four without loss of expressive power:'.

### PR112:PRRT_kwDOTH_vCM6PcwlR

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proofs/P-001-first-propositions.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893237
- Claim: **P2 Badge Align P-002 metadata with the revised proposition** This narrows the canonical P-002 wording, but the machine-readable P-002 entry still records the old scope/claim in 'theory/metadata/propositions.yaml:20-31', so 'theory/meta...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proofs/P-001-first-propositions.md' (SHA-256 6b2ca7972d3478ffd38ba356e35ab712543a24ce779271ce04ba0ce126a4b292).
  - Current repository evidence at 'theory/proofs/P-001-first-propositions.md:25': 'Every scoped reasoning process satisfying Project FAR Axiom 2 and involving a participating collection of more than one representation has, for Project FAR evaluation, a representational structure.'.

### PR112:PRRT_kwDOTH_vCM6PcwlS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/p003-validation-report.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893239
- Claim: **P2 Badge Register the semantic-content dependency for P-003** The audit classifies the semantic content definition as logically required, but the next line leaves metadata unchanged; checked 'theory/metadata/propositions.yaml', and P-0...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/p003-validation-report.md' (SHA-256 fc7988eb46b084b2c32dbd806f10d460a3b45609802eab24bb69ebb7e421d2c8).
  - Current repository evidence at 'docs/reports/p003-validation-report.md:40': 'Dependency modifications: none. Metadata was not modified because no genuine metadata error requiring registry correction was demonstrated.'.

### PR112:PRRT_kwDOTH_vCM6PcwlU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/p004-validation-report.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893242
- Claim: **P2 Badge Reconcile the P-004 D-INT dependency** This audit downgrades 'D-INT' to informative and then says no metadata correction is needed, but 'theory/metadata/propositions.yaml:51-54' still declares 'D-INT' as a P-004 dependency. Un...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/p004-validation-report.md' (SHA-256 076eedafad80156cc330c436ed9846687dc761afff70e0b11d44cef4c5fda879).
  - Current repository evidence at 'docs/reports/p004-validation-report.md:40': 'Dependency modifications: none. Metadata was not modified because no genuine metadata error requiring registry correction was demonstrated.'.

### PR113:PRRT_kwDOTH_vCM6PdBj1

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/metadata/theorems.yaml:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/113#discussion_r3548990147
- Claim: **P2 Badge Keep DEF-033 while the proof object still uses it** With this dependency list reduced to only 'DEF-030', 'DEF-031', and 'DEF-034', T-004's machine proof object still cites 'DEF-033' as premise 'p4' and routes it through 's4' i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR113:PRRT_kwDOTH_vCM6PdBj1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/metadata/theorems.yaml' (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at 'theory/metadata/theorems.yaml:73': 'derived_concepts:'.

### PR115:PRRT_kwDOTH_vCM6PdLxu

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proofs/T-006-primitive-sufficiency.md:32`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/115#discussion_r3549050385
- Claim: **P2 Badge Restore canonical notation dependency** When T-006 is treated as an Established proof under the repo's documented verification gates, this dependency rewrite drops 'theory/notation/canonical-notation.md' even though 'theory/ve...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR115:PRRT_kwDOTH_vCM6PdLxu found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proofs/T-006-primitive-sufficiency.md' (SHA-256 e934b08922bfc8dd6acc844cdd18b05748eb2643c9c69adca52a264db42d7b8f).
  - Current repository evidence at 'theory/proofs/T-006-primitive-sufficiency.md:32': '- D-CALC — Reasoning Calculus'.

### PR116:PRRT_kwDOTH_vCM6PdVsb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/dependencies/dependency-graph.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/116#discussion_r3549107831
- Claim: **P2 Badge Update the stale T-008 circularity audit** After dropping 'T-003' from T-008 here, the current circularity audit still lists 'Dependencies: L-006, T-003, T-004' for T-008 ('theory/audits/circularity-audit-001.md:94') even thou...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR116:PRRT_kwDOTH_vCM6PdVsb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/dependencies/dependency-graph.md' (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at 'theory/dependencies/dependency-graph.md:135': 'Depends on: L-006, T-004.'.

### PR117:PRRT_kwDOTH_vCM6Pdln3

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proofs/T-009-canonical-normal-form.md:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/117#discussion_r3549198406
- Claim: **P2 Badge Require terminal zero-unresolved state for normal form** The revised proof uses L-007 to get termination, but termination only says every performed step decreases the finite unresolved-item measure; it does not establish that ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR117:PRRT_kwDOTH_vCM6Pdln3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proofs/T-009-canonical-normal-form.md' (SHA-256 f128bebccfe23f073beea36f7b6c27dfdb533b748fc4079977fe2212ae4737ef).
  - Current repository evidence at 'theory/proofs/T-009-canonical-normal-form.md:52': 'Therefore every finite scoped FAR representation admits canonical normal form under supplied normalization rules satisfying the stated conditions.'.

### PR117:PRRT_kwDOTH_vCM6Pdln5

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/t009-validation-report.md:5`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/117#discussion_r3549198409
- Claim: **P2 Badge Align T-009 status with the REVISE outcome** This report records the final recommendation as REVISE and later says the stopping rule prevents T-010 from beginning, but the same patch leaves T-009 advertised as 'Established' in...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR117:PRRT_kwDOTH_vCM6Pdln5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/t009-validation-report.md' (SHA-256 3c2f5f1c3cb18dbce97b823b2c19e9a20777a0c72172cce3132f302937f7dcdf).
  - Current repository evidence at 'docs/reports/t009-validation-report.md:5': 'Original validation finding: REVISE.'.

### PR119:PRRT_kwDOTH_vCM6Pd8Rq

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/metadata/theorems.yaml:234`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/119#discussion_r3549330200
- Claim: **P2 Badge Align D-026 with the revised conservative-extension scope** This narrowed T-011 scope is not propagated to the canonical derived concept it still advertises: 'D-026' in 'theory/derivations/derived-concept-registry.md' still de...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR119:PRRT_kwDOTH_vCM6Pd8Rq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/metadata/theorems.yaml' (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at 'theory/metadata/theorems.yaml:234': 'scope: canonical FAR representations'.

### PR120:PRRT_kwDOTH_vCM6Pp34s

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/proof-object-schema.yaml:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/120#discussion_r3553611046
- Claim: **P2 Badge Document prior_proposition in the canonical rule list** Adding 'prior_proposition' here makes the checker accept a rule that still has no entry in 'theory/proof-objects/proof-step-rules.md', even though that document says it d...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR120:PRRT_kwDOTH_vCM6Pp34s found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/proof-object-schema.yaml' (SHA-256 c7a27e3c4f8a23472b65614f4a2f8e490ab922a2fb244d8fbcae6620340695e0).
  - Current repository evidence at 'theory/proof-objects/proof-object-schema.yaml:45': 'description: Apply an established proposition.'.

### PR123:PRRT_kwDOTH_vCM6PqmUy

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-final-consolidation-report.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/123#discussion_r3553876154
- Claim: **P2 Badge Don't clear wording mismatches while P-001 still diverges** This blanket conclusion misses an existing canonical catalog/proof mismatch in the audited P-series scope: 'docs/CANONICAL_MAP.md' identifies 'theory/theorems/proposi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR123:PRRT_kwDOTH_vCM6PqmUy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-final-consolidation-report.md' (SHA-256 beb28b9078185e1e73f8a7fec2d10ab204763300019242bd8e887d598bed7d21).
  - Current repository evidence at 'docs/reports/foundation-final-consolidation-report.md:13': 'This repair pass found no metadata mismatch, dependency graph mismatch, proof object mismatch, theorem/proof wording mismatch, internal link/documentation mismatch, or generated index mismatch. The only demonstrated inconsistency was missin'.

### PR126:PRRT_kwDOTH_vCM6Pr4ri

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-health-verification.md:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/126#discussion_r3554346049
- Claim: **P2 Badge Include the full warning scope** In this commit, the recorded remaining-warning scope is narrower than the checks actually report: 'python tools/check_orphaned_docs.py' emits orphan warnings for 'docs/*', 'docs/reports/appendi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR126:PRRT_kwDOTH_vCM6Pr4ri found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-health-verification.md' (SHA-256 040392476320e7487b1c5ef2e43d9d93bf0af78973387186a983cb6a6c2612ed).
  - Current repository evidence at 'docs/reports/foundation-health-verification.md:72': '- Duplicate-heading-anchor warnings from 'python tools/check_markdown_hygiene.py' in existing foundation documents.'.

### PR127:PRRT_kwDOTH_vCM6Pr_pZ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/foundation-consistency-audit.md:93`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/127#discussion_r3554385195
- Claim: **P2 Badge Link the new audit before calling orphan warnings pre-existing** When 'python tools/validate_docs.py' runs after this commit, 'tools/check_orphaned_docs.py' now reports 'WARN orphaned doc: docs/reports/foundation-consistency-a...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR127:PRRT_kwDOTH_vCM6Pr_pZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/foundation-consistency-audit.md' (SHA-256 db58480f3b2a2001241a016290150ca26e380dde9fb4dee56dd9e5da97a27bf1).
  - Current repository evidence at 'docs/reports/foundation-consistency-audit.md:93': '- 'tools/validate_docs.py' includes orphan-document warnings from the repository orphan-doc check, including many raw appendices and historical research files, then exits successfully.'.

### PR128:PRRT_kwDOTH_vCM6PsH-G

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/canonical-mathematics-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/128#discussion_r3554432485
- Claim: **P2 Badge Include registered derived concepts in the audit** When this report is used as the canonical mathematics inventory, the headline counts and inventory are incomplete: 'theory/derivations/derived-concept-registry.md' registers D...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR128:PRRT_kwDOTH_vCM6PsH-G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/canonical-mathematics-audit.md' (SHA-256 779127a87542df3e6f24c652370b1aa538514648ee34dd8f19abe7fb669e1112).
  - Current repository evidence at 'docs/reports/canonical-mathematics-audit.md:3': 'This Phase 1 Step 4 audit classifies canonical mathematical artifacts without validating new mathematics. The audit found 129 accepted artifacts, 14 experimental artifacts, and 0 deprecated artifacts. Duplicate canonical identifiers found: '.

### PR129:PRRT_kwDOTH_vCM6PsZxY

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/metadata/axioms.yaml:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/129#discussion_r3554535845
- Claim: **P2 Badge Preserve AX-001 draft status in metadata** When consumers use 'theory/metadata/axioms.yaml' or the generated axiom index as the canonical registry, this marks AX-001 as 'Established' even though its canonical source ('research...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR129:PRRT_kwDOTH_vCM6PsZxY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/metadata/axioms.yaml' (SHA-256 ebdaaae3e17c6aeff717eb03c8ea194493d814a11adee326ce2db242936aca8e).
  - Current repository evidence at 'theory/metadata/axioms.yaml:4': 'status: Established'.

### PR131:PRRT_kwDOTH_vCM6PuJ6w

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/dependency-audit.md:130`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/131#discussion_r3555177444
- Claim: **P2 Badge Do not make deferred theorems validation blockers** These steps make T-013–T-015 prerequisites for Phase 1 Step 7, but I checked the existing Phase 1 canonicalization resolution and it explicitly handled the fact that local me...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR131:PRRT_kwDOTH_vCM6PuJ6w found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/dependency-audit.md' (SHA-256 6610c19f446b492bf41cf012bd98fd697f51ff3e17d04b5b7a3882d9426d77fd).
  - Current repository evidence at 'docs/reports/dependency-audit.md:130': '4. Validate T-015.'.

### PR133:PRRT_kwDOTH_vCM6PueMQ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/dependencies/dependency-graph.md:155`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/133#discussion_r3555294440
- Claim: **P2 Badge Update the current circularity audit for T-013** Removing 'T-005' here makes the current dependency sources disagree: 'theory/audits/circularity-audit-001.md' still lists T-013 dependencies as 'D-CALC, T-005' and explains the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR133:PRRT_kwDOTH_vCM6PueMQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/dependencies/dependency-graph.md' (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at 'theory/dependencies/dependency-graph.md:155': 'Depends on: D-CALC.'.

### PR134:PRRT_kwDOTH_vCM6Pujux

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/dependencies/dependency-graph.md:159`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/134#discussion_r3555325304
- Claim: **P2 Badge Synchronize T-014's circularity audit entry** With this dependency graph now declaring T-014 depends only on D-CALC, the current circularity audit still reports 'Dependencies: D-CALC, T-005' and justifies the pass by saying T-...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR134:PRRT_kwDOTH_vCM6Pujux found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/dependencies/dependency-graph.md' (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at 'theory/dependencies/dependency-graph.md:159': 'Depends on: D-CALC.'.

### PR136:PRRT_kwDOTH_vCM6Pus-I

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-014.proof.yaml:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/136#discussion_r3555378849
- Claim: **P2 Badge Use a schema-declared proof-object status** The proof-object schema defines 'status' as an enum with values '[draft, proposed, verified, established, deprecated]' ('theory/proof-objects/proof-object-schema.yaml:17-19'), so set...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR136:PRRT_kwDOTH_vCM6Pus-I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-014.proof.yaml' (SHA-256 7def7aa06fda8cd7fe25e64870076d40aae65c37b6ec41236cd5e0dac279b1db).
  - Current repository evidence at 'theory/proof-objects/T-014.proof.yaml:5': 'status: accepted'.

### PR136:PRRT_kwDOTH_vCM6Pus-M

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/dependency-audit-rerun.md:132`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/136#discussion_r3555378854
- Claim: **P2 Badge Correct the proof-object status audit** This audit conclusion is contradicted by the repository: 'theory/proof-objects/T-001.proof.yaml' through 'T-012.proof.yaml' still have 'status: draft', so T-001 through T-013 were not al...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR136:PRRT_kwDOTH_vCM6Pus-M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/dependency-audit-rerun.md' (SHA-256 c66331f2d7e4f012787f77a60060a40ae4e330d7aa8c9aab98977ec9ed0b372c).
  - Current repository evidence at 'docs/reports/dependency-audit-rerun.md:132': "Proof objects for T-001 through T-013 were already synchronized with accepted status. T-014 and T-015 proof objects still carried 'status: draft' even though theorem metadata lists them as established and this rerun's accepted foundation in".

### PR137:PRRT_kwDOTH_vCM6Pu8t3

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/theorem-coverage-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/137#discussion_r3555471226
- Claim: **P2 Badge Reconcile the canonical inventory with accepted audit** This summary says the audit enumerates all canonical mathematical artifacts, but the accepted foundation includes the Canonical Mathematics Audit ('docs/reports/dependenc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR137:PRRT_kwDOTH_vCM6Pu8t3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/theorem-coverage-audit.md' (SHA-256 294c1e7bdff685529e48f76557aa856f9c23c1291f5abbeca205c91acf663854).
  - Current repository evidence at 'docs/reports/theorem-coverage-audit.md:3': '- Total canonical mathematical artifacts enumerated: 128: 1 primitive record, 89 definitions, 6 axiom records, 8 lemmas, 9 propositions, and 15 theorems.'.

### PR137:PRRT_kwDOTH_vCM6Pu8t7

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/theorem-coverage-audit.md:203`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/137#discussion_r3555471231
- Claim: **P2 Badge Correct the dependency-registry coverage claims** These PASS rows treat 'theory/dependencies/dependency-registry.yaml' as covering every L/P/T artifact, but that registry is explicitly 'scope: repository-structure-only' ('theo...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR137:PRRT_kwDOTH_vCM6Pu8t7 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/theorem-coverage-audit.md' (SHA-256 294c1e7bdff685529e48f76557aa856f9c23c1291f5abbeca205c91acf663854).
  - Current repository evidence at 'docs/reports/theorem-coverage-audit.md:203': '| Theorem dependency metadata | PASS: T-001 through T-015 are recorded in 'theory/metadata/theorems.yaml', 'theory/dependencies/dependency-registry.yaml', and 'theory/dependencies/dependency-graph.md'. |'.

### PR138:PRRT_kwDOTH_vCM6Pu_IE

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/proof-objects/T-001.proof.yaml:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/138#discussion_r3555485237
- Claim: **P2 Badge Use a schema-valid proof-object status** For T-001 through T-012 this change writes 'status: accepted', but 'theory/proof-objects/proof-object-schema.yaml' defines the allowed proof-object statuses as only 'draft', 'proposed',...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR138:PRRT_kwDOTH_vCM6Pu_IE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/proof-objects/T-001.proof.yaml' (SHA-256 c592af3b04c3af82dad53d23a354e3c9bc414296f7d2756316a2783a7bb518eb).
  - Current repository evidence at 'theory/proof-objects/T-001.proof.yaml:5': 'status: accepted'.

### PR148:PRRT_kwDOTH_vCM6Pw5hJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/reports/external-validation/philosophy/campaign-method.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/148#discussion_r3556188197
- Claim: **P2 Badge Add Charter status to the new campaign artifacts** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from Ac...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR148:PRRT_kwDOTH_vCM6Pw5hJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/reports/external-validation/philosophy/campaign-method.md' (SHA-256 5ab002f1821bf39ca628f8a3b9563746c64e11f58c58312b5dcac63d3ecce07f).
  - Current repository evidence at 'docs/reports/external-validation/philosophy/campaign-method.md:1': '# Philosophy External Validation Campaign Method'.

### PR151:PRRT_kwDOTH_vCM6PxMgL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `mechanization/far_mechanization/ir.py:250`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/151#discussion_r3556294779
- Claim: **P2 Badge Include the investigation in duplicate-ID checks** When an IR collection item reuses the 'investigation.identifier', 'FARDocument.validate()' returns no 'DUPLICATE_LOCAL_IDENTIFIER' because the duplicate map starts empty and i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR151:PRRT_kwDOTH_vCM6PxMgL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/far_mechanization/ir.py' (SHA-256 bf54a8e7b96de3c32e46a594e6221af9e44bfd7f80963772dfedaa88f5d64104).
  - Current repository evidence at 'mechanization/far_mechanization/ir.py:250': 'diagnostics.extend(self.graph.validate())'.

### PR151:PRRT_kwDOTH_vCM6PxMgM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `mechanization/far_mechanization/ir.py:178`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/151#discussion_r3556294780
- Claim: **P2 Badge Validate enum fields at runtime** When graph nodes are constructed from untyped parsed data, 'GraphNode(Identifier("N"), "bogus").validate()' reports success because this validator only checks the identifier and source; datacl...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR151:PRRT_kwDOTH_vCM6PxMgM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/far_mechanization/ir.py' (SHA-256 bf54a8e7b96de3c32e46a594e6221af9e44bfd7f80963772dfedaa88f5d64104).
  - Current repository evidence at 'mechanization/far_mechanization/ir.py:178': 'diagnostics.extend(self.source.validate())'.

### PR154:PRRT_kwDOTH_vCM6QJoVS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/governance/repository-certification-standard.md:4`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/154#discussion_r3565194327
- Claim: **P2 Badge Use a Charter-recognized artifact status** Under the root 'AGENTS.md', new work must comply with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from 'A...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR154:PRRT_kwDOTH_vCM6QJoVS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/governance/repository-certification-standard.md' (SHA-256 4141c4ead85e8a4bb10bfc37bbc3ab926775ae9979651fda9d6dedf96e3ac652).
  - Current repository evidence at 'docs/governance/repository-certification-standard.md:4': 'Status: Frozen Canonical Governance Standard'.

### PR154:PRRT_kwDOTH_vCM6QKFHI

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/repository-certification-inventory-audit.md:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/154#discussion_r3565358292
- Claim: **P2 Badge Refresh the inventory against the final tree** In the reviewed tree there are 1000 tracked paths ('git ls-tree -r --name-only cdc9897... | wc -l'), and this inventory also omits certification artifacts added later in the same ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR154:PRRT_kwDOTH_vCM6QKFHI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/repository-certification-inventory-audit.md' (SHA-256 6ad4783e8e996d8cf54d0715000bb606a2fc67b40f5820fdbefd3fa771d6901c).
  - Current repository evidence at 'docs/audits/repository-certification-inventory-audit.md:34': '| Total tracked artifacts | 989 |'.

### PR155:PRRT_kwDOTH_vCM6QMr9J

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `README.md:99`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/155#discussion_r3566291247
- Claim: **P2 Badge Restore generated TASK-004 metadata** In this generated dashboard block, 'tools/update_readme_dashboard.py::parse_tasks' takes the branch and title from 'docs/planning/next-actions.md', which still records TASK-004 as 'mainten...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR155:PRRT_kwDOTH_vCM6QMr9J found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'README.md' (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at 'README.md:99': '## Certification and Architecture Navigation'.

### PR156:PRRT_kwDOTH_vCM6QMZtL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-validation-methodology.md:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/156#discussion_r3566189890
- Claim: **P2 Badge Scope the new requirements before applying them globally** Because this says every external-system investigation must now record the new fields, the 20 already-registered investigations in 'theory/evaluation/external-systems/*...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR156:PRRT_kwDOTH_vCM6QMZtL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-validation-methodology.md' (SHA-256 54f2f30fe0c9ed6c7c68ff5dea10000e32f7ac75378c4edfdb4d2236c19258cb).
  - Current repository evidence at 'theory/evaluation/external-validation-methodology.md:43': '- the reasoning process is inaccessible or purely opaque;'.

### PR157:PRRT_kwDOTH_vCM6QMn8d

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-system-investigations/legal-reasoning.md:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/157#discussion_r3566269404
- Claim: **P2 Badge Reclassify legal reasoning when preservation is unknown** Here the report classifies legal reasoning as 'conservative extension', but its own preservation review leaves semantic, operational, and information preservation as 'u...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR157:PRRT_kwDOTH_vCM6QMn8d found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-system-investigations/legal-reasoning.md' (SHA-256 9c4231e8a3ea073a8020ccb6c872f04ed8bc0879cd0fdd1dfb3e717c7125b364).
  - Current repository evidence at 'theory/evaluation/external-system-investigations/legal-reasoning.md:111': ''conservative extension''.

### PR157:PRRT_kwDOTH_vCM6QMn8f

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/157#discussion_r3566269407
- Claim: **P2 Badge Recompute synthesis over all nine investigations** The scope lists nine investigations, including the five adversarial reports, but this aggregate still says 'All four' and summarizes only the original formal/Bayesian/science ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR157:PRRT_kwDOTH_vCM6QMn8f found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md' (SHA-256 9ebb5a68dd908d74d6a8251e8cb6d4a6455e6223d32490ac956916a9ede43838).
  - Current repository evidence at 'theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md:23': 'All nine scoped EV-021 through EV-029 investigations required Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus for their target mappings. FARA operational components were used when procedure,'.

### PR158:PRRT_kwDOTH_vCM6QQUuU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/158#discussion_r3567578096
- Claim: **P2 Badge Reclassify EV-028 before aggregating counts** When this table counts EV-021 through EV-029 as 3 'conservative extension' and 4 'unresolved', it preserves EV-028's conservative label even though 'legal-reasoning.md' records sem...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR158:PRRT_kwDOTH_vCM6QQUuU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/external-system-investigations/current-evidence-assessment-001.md' (SHA-256 fb686f15f9b48318d224e41c4a34ab4252748e00f12cb8a183930ea73f020376).
  - Current repository evidence at 'theory/evaluation/external-system-investigations/current-evidence-assessment-001.md:27': '| EV-021 through EV-029 | 9 | 2 'fits FAR'; 3 'conservative extension'; 4 'unresolved'; 0 'candidate primitive failure' | Stronger within stated scopes because the reports explicitly separate preservation dimensions, limitations, and univer'.

### PR159:PRRT_kwDOTH_vCM6QQ_JJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiment-registry.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821907
- Claim: **P2 Badge Register only immutable experiment artifacts** The registry pins a concrete scenario/vocabulary/instruction version for CRE-001, but the CRE-001 directory currently contains only a README and a repo-wide search finds no artifa...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiment-registry.json' (SHA-256 7ee62a82595c68c5d9afd1257bbb8ecc42515d4555191878151be997b00d4bcb).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiment-registry.json:12': '"instruction_version": "CRE-001-INSTRUCTIONS-1.0",'.

### PR159:PRRT_kwDOTH_vCM6QQ_JM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821910
- Claim: **P2 Badge Inline the provenance schema reference** When an evaluator submission includes its required 'provenance' object, validation through the repository's bundled JSON Schema implementation fails before checking the instance because...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json' (SHA-256 ffe7d9da8ad47b2c1d742909f52b3f5fdabf912c2364d722d05ff287cce014db).
  - Current repository evidence at 'theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json:1': '{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"CRP v1.0 Evaluator Mapping Submission","type":"object","required":["protocol_version","experiment","evaluator","assignment","date","vocabulary_label","mapping","derived_cons'.

### PR160:PRRT_kwDOTH_vCM6QR-_Y

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/validate_cre001_submission.py:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181639
- Claim: **P2 Badge Check mapping provenance against the bundle record** This only verifies the CIR provenance identifier, so a bundle where 'mapping_submission.provenance' points at a different or nonexistent record is still accepted as long as ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_Y found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/validate_cre001_submission.py' (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at 'tools/validate_cre001_submission.py:135': 'raise ValidationError("cir: provenance mismatch")'.

### PR161:PRRT_kwDOTH_vCM6RQoEE

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/repo_health_check.py:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/161#discussion_r3591137832
- Claim: **P2 Badge Run the documented pytest mechanization suite** When 'repo_health_check.py --fast' or '--full' runs in this repository, this 'unittest discover' command exercises only the 51 'unittest.TestCase' cases; the documented mechaniza...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR161:PRRT_kwDOTH_vCM6RQoEE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/repo_health_check.py' (SHA-256 2e93d1abcbc1c8a467308efb98368be4c9559b4d5a818f53968854152f0be0a5).
  - Current repository evidence at 'tools/repo_health_check.py:11': 'def main()->int:'.

### PR161:PRRT_kwDOTH_vCM6RQoEG

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_status_consistency.py:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/161#discussion_r3591137834
- Claim: **P2 Badge Preserve negative status before matching supported** For any parsed source whose status is 'Not supported', this loop matches the substring 'supported' first and normalizes the value to 'supported', so the consistency report i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR161:PRRT_kwDOTH_vCM6RQoEG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_status_consistency.py' (SHA-256 cc238d6cc8f1dc73e77cedbc3ebe7a2e836896846c0989fc1a4f051e3718eea8).
  - Current repository evidence at 'tools/check_status_consistency.py:45': 'return status'.

### PR164:PRRT_kwDOTH_vCM6RRYKa

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_status_consistency.py:177`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/164#discussion_r3591417087
- Claim: **P2 Badge Update tests for scoped fallback matching** This new scope gate changes the checker so conditional theorem titles no longer fallback-match the broad investigation titles, but 'tests/test_status_consistency.py::test_similarity_...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR164:PRRT_kwDOTH_vCM6RRYKa found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_status_consistency.py' (SHA-256 cc238d6cc8f1dc73e77cedbc3ebe7a2e836896846c0989fc1a4f051e3718eea8).
  - Current repository evidence at 'tools/check_status_consistency.py:177': 'if score >= SIMILARITY_THRESHOLD and scope_compatible_for_fallback(a, b):'.

### PR165:PRRT_kwDOTH_vCM6RRgpO

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/165#discussion_r3591465879
- Claim: **P2 Badge Record pilot exposure in CRE-001 status** When this pilot artifact is kept under CRE-001, this line records that calibration and experimental materials were exposed to an evaluator, but the existing status sources still say no...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR165:PRRT_kwDOTH_vCM6RRgpO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md' (SHA-256 1160ddca740e70d001a8361450f6d76389bdcc14653ed6c06323422a863ebdc8).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md:27': '- Calibration and experimental materials were exposed in one prompt.'.

### PR165:PRRT_kwDOTH_vCM6RRgpS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json:2`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/165#discussion_r3591465884
- Claim: **P2 Badge Add required provenance to pilot metadata** For this new CRE-001 artifact, the metadata omits several immutable provenance identifiers required by CRP v1.0's Provenance rule for every dataset and artifact, including protocol/s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR165:PRRT_kwDOTH_vCM6RRgpS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json' (SHA-256 d79ab5d9e6bd2119e050b472446a1dd5c8820b4dd53a9d6277d9da56828198c9).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json:2': '"artifact_id": "CRE-001-E01-CLAUDE-SONNET-MEDIUM-PILOT-V1-REVIEW-METADATA",'.

### PR169:PRRT_kwDOTH_vCM6RUGku

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/169#discussion_r3592472967
- Claim: **P2 Badge Use distinct provenance for strategic tasks** When the current gap report contains GAP-001 through GAP-005, these hard-coded tasks reuse both the same task IDs and the same source-gap IDs as the generated gap-derived tasks, so...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR169:PRRT_kwDOTH_vCM6RUGku found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/generate_next_tasks.py' (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at 'tools/generate_next_tasks.py:21': "if __name__=='__main__': raise SystemExit(main())".

### PR170:PRRT_kwDOTH_vCM6RUPh-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/170#discussion_r3592525583
- Claim: **P2 Badge Use noncolliding source gaps for strategic tasks** In this repo 'docs/reports/research-gap-report.md' already defines 'GAP-001' through 'GAP-005' as unrelated PS-001/PS-003 maintenance gaps; these hard-coded CRE-002 tasks reus...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR170:PRRT_kwDOTH_vCM6RUPh- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/generate_next_tasks.py' (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at 'tools/generate_next_tasks.py:21': "if __name__=='__main__': raise SystemExit(main())".

### PR170:PRRT_kwDOTH_vCM6RUPh8

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_cre001_semantics.py:54`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/170#discussion_r3592525581
- Claim: **P2 Badge Compare semantic docs against the frozen specification** This loop only checks that each semantic doc contains the five status words; it never hashes the docs or compares their primitive definitions/licensing tables to 'semant...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR170:PRRT_kwDOTH_vCM6RUPh8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre001_semantics.py' (SHA-256 42c8c66386e2c0764fd901699f14306586d3371d2d84bd43dfa84b304fe5edd7).
  - Current repository evidence at 'tools/check_cre001_semantics.py:54': 'for prim in prims:'.

### PR171:PRRT_kwDOTH_vCM6RUQL5

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/generate_next_tasks.py:73`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529397
- Claim: **P2 Badge Keep generated task identifiers unique** Because 'task_from_gap()' also derives IDs as 'TASK-', prepending strategic tasks named 'TASK-001' through 'TASK-005' makes the generated 'docs/planning/next-actions.md' contain two dif...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/generate_next_tasks.py' (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at 'tools/generate_next_tasks.py:21': "if __name__=='__main__': raise SystemExit(main())".

### PR171:PRRT_kwDOTH_vCM6RUQL6

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_cre001_semantics.py:44`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529398
- Claim: **P2 Badge Guard the FAR-proof non-claim in semantic checks** 'NONCLAIMS' includes 'FAR proof', but this condition explicitly exempts that claim, so 'tools/check_cre001_semantics.py' passes even if the frozen primitive semantics omit the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre001_semantics.py' (SHA-256 42c8c66386e2c0764fd901699f14306586d3371d2d84bd43dfa84b304fe5edd7).
  - Current repository evidence at 'tools/check_cre001_semantics.py:44': "chronology=spec.get('chronology',{})".

### PR172:PRRT_kwDOTH_vCM6RUxxM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/repository-health.yml:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/172#discussion_r3592726443
- Claim: **P2 Badge Defer PR trigger until full health passes** This new 'pull_request' trigger makes the workflow run the unchanged 'python tools/repo_health_check.py --full' step for every PR targeting 'main'; in this checkout that exact comman...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR172:PRRT_kwDOTH_vCM6RUxxM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/repository-health.yml' (SHA-256 a7efc79586d873fbdfd3b626610290f2098001b190688d672901aeee28a90a70).
  - Current repository evidence at '.github/workflows/repository-health.yml:9': '- main'.

### PR172:PRRT_kwDOTH_vCM6RUxxO

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/update_readme_dashboard.py:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/172#discussion_r3592726445
- Claim: **P2 Badge Parse strategic tasks in the planner summary too** Now that this parser promotes 'STRATEGIC-*' entries into the README top tasks, the canonical 'make dashboard' workflow becomes inconsistent because 'tools/self_advancement_pla...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR172:PRRT_kwDOTH_vCM6RUxxO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/update_readme_dashboard.py' (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at 'tools/update_readme_dashboard.py:60': 'make plan'.

### PR173:PRRT_kwDOTH_vCM6RU20U

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/README.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755293
- Claim: **P2 Badge Register CRE-002 in the canonical experiment registry** This commit introduces CRE-002 as a preregistered experiment package, but 'theory/evaluation/comparative-representation/experiment-registry.json' still contains only CRE-...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002/README.md' (SHA-256 a8695bb976ca5a19072f809374054cfb1ff8ee9cc2cfe4e77955daa4c241ba02).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002/README.md:1': '# CRE-002: Prospective Multi-Pressure Reasoning System'.

### PR174:PRRT_kwDOTH_vCM6RVB21

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_cre002_lock.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/174#discussion_r3592819589
- Claim: **P2 Badge Verify the manifest's recorded checksums** When this gate builds 'actual', it uses 'package-manifest.json' only as a path list and ignores each entry's recorded 'sha256' and 'byte_count', so CI still passes if the manifest is ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR174:PRRT_kwDOTH_vCM6RVB21 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre002_lock.py' (SHA-256 08ecb63c76d5eb0e43698f03aaa13509487431f059f0bd355cbc91bd69152209).
  - Current repository evidence at 'tools/check_cre002_lock.py:25': '}'.

### PR174:PRRT_kwDOTH_vCM6RVB22

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_cre002_lock.py:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/174#discussion_r3592819591
- Claim: **P2 Badge Use a reachable checksum source commit** In the reviewed commit, this hard-coded 'source_commit' is not an ancestor of '2692d8cbd329ff68bb63f2e5dfb1e9c6bf73453b' ('git merge-base --is-ancestor 003f0fda... 2692d8c...' returns n...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR174:PRRT_kwDOTH_vCM6RVB22 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre002_lock.py' (SHA-256 08ecb63c76d5eb0e43698f03aaa13509487431f059f0bd355cbc91bd69152209).
  - Current repository evidence at 'tools/check_cre002_lock.py:16': 'EXECUTION_LOCK = PACKAGE / "execution-lock.json"'.

### PR176:PRRT_kwDOTH_vCM6RVX-h

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/cre002_execute.py:358`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/176#discussion_r3592946238
- Claim: **P2 Badge Emit the preregistered boundary reports** CRE-002 preregistration requires each vocabulary to emit both a compiler-boundary report and a limitation/unsupported-element report, but this artifact map never writes either artifact...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR176:PRRT_kwDOTH_vCM6RVX-h found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre002_execute.py' (SHA-256 a772507579200e564f24e3d7cb04e152e442ac1819f56e4f1a5acf2a5c36b6e1).
  - Current repository evidence at 'tools/cre002_execute.py:221': 'raise SystemExit(main())'.

### PR177:PRRT_kwDOTH_vCM6RVqC_

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_vocabulary_semantics_baseline_1_1.py:100`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/177#discussion_r3593046970
- Claim: **P2 Badge Restore byte-for-byte CRE-002 result validation** When the original CRE-002 result changes outside the sampled fields, this checker still passes even though the new baseline's freeze requirement says the result must remain byt...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR177:PRRT_kwDOTH_vCM6RVqC_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_vocabulary_semantics_baseline_1_1.py' (SHA-256 f6a379ab8da564755aa7b010d5017415d75101873c7bf15d4388857b558dcde8).
  - Current repository evidence at 'tools/check_vocabulary_semantics_baseline_1_1.py:87': 'raise SystemExit(main())'.

### PR178:PRRT_kwDOTH_vCM6RV06x

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/178#discussion_r3593108987
- Claim: **P2 Badge Require the Baseline 1.1 checksum lock before execution** This unlock prerequisite now only requires Baseline 1.1 to be merged, but the Baseline 1.1 freeze boundary says it becomes usable only after merge and checksum lock ('t...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR178:PRRT_kwDOTH_vCM6RV06x found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json' (SHA-256 2253d19c68da78800186089e9b320881c1a70552a02f4c295f05496a40abb6af).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:8': '"semantic_authority": "VOCABULARY-SEMANTICS-BASELINE-1.1",'.

### PR182:PRRT_kwDOTH_vCM6RXNCb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/cre002_ext001_execute.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608682
- Claim: **P2 Badge Hash the official vocabulary source packages** The preregistration makes the official Vocabulary A/B/C source definitions frozen inputs and each candidate is supposed to emit source checksums, but this shared 'source_checksums...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/cre002_ext001_execute.py' (SHA-256 9ae28e0320901e1fcb68abfac166ed99aef66da6f3b957fb8c8623496e6cbf38).
  - Current repository evidence at 'tools/cre002_ext001_execute.py:74': 'source_checksums = {'.

### PR183:PRRT_kwDOTH_vCM6RXZ9j

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/integrate-cre002-ext001-evidence.yml:59`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/183#discussion_r3593681934
- Claim: **P2 Badge Commit the dashboard index after regeneration** When this workflow runs, 'tools/update_readme_dashboard.py' also rewrites 'docs/planning/repository-index.md' via 'generate_index()'. I verified the workflow command sequence on ...
- Rationale: The artifact reviewed by finding PR183:PRRT_kwDOTH_vCM6RXZ9j has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path '.github/workflows/integrate-cre002-ext001-evidence.yml' does not exist ('test -e' is false).

### PR183:PRRT_kwDOTH_vCM6RXZ9l

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/integrate-cre002-ext001-evidence.yml:55`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/183#discussion_r3593681939
- Claim: **P2 Badge Keep the regenerated README phase current** When this integration workflow reaches the README step, 'tools/update_readme_dashboard.py' still renders the old post-CRE-001 / CRE-002-preparation phase and roadmap lines. Because t...
- Rationale: The artifact reviewed by finding PR183:PRRT_kwDOTH_vCM6RXZ9l has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path '.github/workflows/integrate-cre002-ext001-evidence.yml' does not exist ('test -e' is false).

### PR185:PRRT_kwDOTH_vCM6RefEA

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_cre002_ext001_rep001_preregistration.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/185#discussion_r3596251334
- Claim: **P2 Badge Require the checksum-locked phase** After this commit promotes the package to 'checksum_state: locked', the preregistration checker still accepts 'pending'. If a bad merge or later edit reverts the manifest to 'pending', this ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR185:PRRT_kwDOTH_vCM6RefEA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_cre002_ext001_rep001_preregistration.py' (SHA-256 6dc61420004ed64be76510276503bf647b101117792b621b801942fddcd5b5c1).
  - Current repository evidence at 'tools/check_cre002_ext001_rep001_preregistration.py:40': 'fail("an independent verifier team is required")'.

### PR188:PRRT_kwDOTH_vCM6Rfdum

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/188#discussion_r3596608260
- Claim: **P2 Badge Keep the superseded manifest state accepted by checks** Changing the package checksum state to this new value leaves the existing preregistration gate out of sync: 'tools/check_cre002_ext001_rep001_preregistration.py' still re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR188:PRRT_kwDOTH_vCM6Rfdum found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json' (SHA-256 aaa00f8fd67a7c0dcf8d574b249750d15b00b2341b3e00854cad0b0b843e2e8f).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json:23': '"checksum_state": "locked",'.

### PR189:PRRT_kwDOTH_vCM6RgFpD

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/parse_far.py:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833875
- Claim: **P2 Badge Reject non-string scalars instead of coercing them** In files that use non-string YAML scalars for 'string+' fields, such as 'id: 1' or 'kind: true', this coerces them to strings before validation, so 'python tools/parse_far.p...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/parse_far.py' (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at 'tools/parse_far.py:48': 'return text'.

### PR189:PRRT_kwDOTH_vCM6RgFpI

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/parse_far.py:85`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833882
- Claim: **P2 Badge Validate unknown keys inside statement mappings** When a representation uses a mapped 'statement', this delegates to 'Statement.from_value' without checking the grammar's statement allow-list, so 'statement: {kind: claim, clai...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/parse_far.py' (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at 'tools/parse_far.py:85': 'statement = Statement.from_value(item["statement"], f"representation {rep_id}") if "statement" in item else None'.

### PR189:PRRT_kwDOTH_vCM6RgFpM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/parse_far.py:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833889
- Claim: **P2 Badge Remove lowercase aliases from primitive key allow-list** With these lowercase keys allowed, a 'reasoning_system.far_primitives' block containing only 'investigation', 'representation', 'structure', 'interpretation', and 'calcu...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/parse_far.py' (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at 'tools/parse_far.py:22': 'PRIMITIVE_KEYS = {"Investigation", "Representation", "Representational Structure", "Interpretation", "Reasoning Calculus", "investigation", "representation", "structure", "interpretation", "calculus"}'.

### PR191:PRRT_kwDOTH_vCM6Rg6qO

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `mechanization/lean/FARCore.lean:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/191#discussion_r3597138599
- Claim: **P2 Badge Carry the required transition-signature fields** When a scoped process has specified transition executions, this type treats a bare label as a complete transition signature. The accepted definitions say a transition signature ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR191:PRRT_kwDOTH_vCM6Rg6qO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/lean/FARCore.lean' (SHA-256 7b004e58006ee9f5f767308f896284c4dfbaef2c37d1a56b06605e6dfc2978ab).
  - Current repository evidence at 'mechanization/lean/FARCore.lean:28': 'deriving Repr, DecidableEq'.

### PR191:PRRT_kwDOTH_vCM6Rg6qW

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `mechanization/lean/FARCore.lean:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/191#discussion_r3597138611
- Claim: **P2 Badge Tie trace transitions to the governing calculus** For a process whose 'specifiedTransitions' includes a signature that 'premises.calculus R hScope' rejects, the construction still succeeds because the representation only store...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR191:PRRT_kwDOTH_vCM6Rg6qW found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/lean/FARCore.lean' (SHA-256 7b004e58006ee9f5f767308f896284c4dfbaef2c37d1a56b06605e6dfc2978ab).
  - Current repository evidence at 'mechanization/lean/FARCore.lean:70': 'traceMatchesProcess : T.transitions = R.specifiedTransitions'.

### PR193:PRRT_kwDOTH_vCM6Rj0PX

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/export_specification.py:118`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/193#discussion_r3598208540
- Claim: **P2 Badge Recompute VCS metadata instead of preserving it** When the exporter runs over the committed export directory, 'existing_vcs_metadata()' returns the old manifest values and this early return keeps them, so the exact CI regenera...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR193:PRRT_kwDOTH_vCM6Rj0PX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/export_specification.py' (SHA-256 f1d9622b27169a9033e6ad2f45aa734b5a9578c62fce039d3bf8a0de3b0a623c).
  - Current repository evidence at 'tools/export_specification.py:118': 'return preserved'.

### PR197:PRRT_kwDOTH_vCM6RpiBO

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/README.md:15`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/197#discussion_r3600351090
- Claim: **P2 Badge Register the new theory child domain** Adding 'theory/independence/' here creates a new canonical theory area, but the frozen Repository Domain Registry remains the authoritative list of 'theory/' child domains and still omits...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR197:PRRT_kwDOTH_vCM6RpiBO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/README.md' (SHA-256 0aad43903cd38647857f274d6add9559a24c510074baaa1f6a3c8e6b5bab5b9a).
  - Current repository evidence at 'theory/README.md:15': '- 'independence/' — falsifiable primitive-independence criteria, schemas, and future execution artifacts.'.

### PR198:PRRT_kwDOTH_vCM6R1HgZ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/independence/executions/PIE-001/attempts.csv:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/198#discussion_r3604642189
- Claim: **P2 Badge Record required preservation and complexity judgments** For PIE-001 rows, the protocol requires each attempted reduction to record per-dimension preservation judgments and complexity accounting before success/failure can be ad...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR198:PRRT_kwDOTH_vCM6R1HgZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/independence/executions/PIE-001/attempts.csv' (SHA-256 6b156d3ee3f7cb7f6d3c23a2ef2f8edeed955644c8135aa265cff94ad2f9c1b0).
  - Current repository evidence at 'theory/independence/executions/PIE-001/attempts.csv:1': 'execution_id,primitive,test_type,attempt_outcome,hidden_reintroduction,decision,reason'.

### PR200:PRRT_kwDOTH_vCM6R1kcJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/independence/global-minimality/GMA-001/README.md:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/200#discussion_r3604808065
- Claim: **P2 Badge Do not label unresolved counts as demonstrated** I checked the referenced AVC-001 results: only the FAR control is all-'Pass', while every three-primitive candidate is either 'unresolved' or 'not-admissible'. Calling the minim...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR200:PRRT_kwDOTH_vCM6R1kcJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/independence/global-minimality/GMA-001/README.md' (SHA-256 3e070958e4898c8ad375baca08d3563c6a10cdc75fc3d4c33cb9f6a49d6e03bb).
  - Current repository evidence at 'theory/independence/global-minimality/GMA-001/README.md:45': '> The minimum demonstrated sufficient primitive count is at most five and may be as low as three within the tested families.'.

### PR201:PRRT_kwDOTH_vCM6R1r2E

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/scope/ISD-001/scope-registry.json:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/201#discussion_r3604850584
- Claim: **P2 Badge Preserve frozen-benchmark gate in the registry rule** If future scope-expansion tooling or reviewers use this machine-readable 'inclusion_rule', a class can be marked demonstrated from any single explicit instance, even when n...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR201:PRRT_kwDOTH_vCM6R1r2E found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/scope/ISD-001/scope-registry.json' (SHA-256 72f851af52ed016c75f382f3dcf08a352d20df3d337450b6691a203874c9dbec).
  - Current repository evidence at 'theory/scope/ISD-001/scope-registry.json:5': '"inclusion_rule": "A class is in current demonstrated scope only when at least one explicit instance has a preserved mapping or deterministic execution artifact covering structural, semantic, operational, dependency, information, and histor'.

### PR201:PRRT_kwDOTH_vCM6R1r2G

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/scope/ISD-001/scope-registry.json:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/201#discussion_r3604850587
- Claim: **P2 Badge Include standalone universality in registry exclusions** If downstream checks consume 'excluded_from_current_claims' as the machine-readable claim boundary, this list still does not exclude the standalone universality claim ('...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR201:PRRT_kwDOTH_vCM6R1r2G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/scope/ISD-001/scope-registry.json' (SHA-256 72f851af52ed016c75f382f3dcf08a352d20df3d337450b6691a203874c9dbec).
  - Current repository evidence at 'theory/scope/ISD-001/scope-registry.json:43': '"universal necessity, global minimality, or unique optimality"'.

### PR204:PRRT_kwDOTH_vCM6R2SrT

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json:38`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/204#discussion_r3605073887
- Claim: **P2 Badge Make 'cannot_determine' exclusive in the schema** For translated systems marked distinguishable, the schema currently accepts 'difference_carriers' such as '["cannot_determine", "assigns_meaning"]' because 'cannot_determine' i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR204:PRRT_kwDOTH_vCM6R2SrT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json' (SHA-256 9c75d5c5ffdb68103b5994ec4d307de44099fc56f7885828cd00635173d2ac50).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json:38': '"defines_objective",'.

### PR205:PRRT_kwDOTH_vCM6R2llN

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/205#discussion_r3605183243
- Claim: **P2 Badge Use the schema field in the decision tree** For implementations following this frozen tree, 'translated_distinction' is not a response field: 'response.schema.json', 'preregistration.json', and 'scoring.py' all use 'translated...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR205:PRRT_kwDOTH_vCM6R2llN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md' (SHA-256 8414e3f277208dd0fd36705cf71540350897a0e8f06546d011270979ee950a6f).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md:8': '4. If 'source_difference = yes' and 'translated_difference = cannot_determine', classify it as 'unknown'.'.

### PR205:PRRT_kwDOTH_vCM6R2llV

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/205#discussion_r3605183253
- Claim: **P2 Badge Align hidden-reintroduction outcomes with scorer** When 'other' is selected with 'other_function = cannot_determine', this frozen rule says to output 'hidden_reintroduction = unknown', but the normative implementation in 'scor...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR205:PRRT_kwDOTH_vCM6R2llV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md' (SHA-256 1756f03bbbb70a96efebadb7b8fa0c8338827cc45dcad0c46288f0c51787eeb6).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md:25': '- 'cannot_determine': 'unknown'.'.

### PR206:PRRT_kwDOTH_vCM6R22Dp

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:86`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278317
- Claim: **P2 Badge Validate responses against the frozen schema** This only checks labels and 'submitted_at' are non-empty strings, so a manifest and response using values such as 'case_label: "CASE 001"' or 'submitted_at: "not-a-date"' are acce...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Dp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py' (SHA-256 00bb336e72569ed231258ca9b8aba71b2065567f5c9b180c9b27134a9bc0cba6).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:86': 'def validate_response_shape(response: Mapping[str, Any]) -> None:'.

### PR206:PRRT_kwDOTH_vCM6R22Ds

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:179`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278320
- Claim: **P2 Badge Report the required per-evaluator and per-case aggregates** The frozen automatic-scoring spec requires results at response, evaluator, case, candidate, and overall levels, but this summary only emits the overall counts and 'by...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Ds found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py' (SHA-256 00bb336e72569ed231258ca9b8aba71b2065567f5c9b180c9b27134a9bc0cba6).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:179': 'record_id = raw["record_id"]'.

### PR209:PRRT_kwDOTH_vCM6SASkl

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/209#discussion_r3608793206
- Claim: **P2 Badge Use non-predictable candidate labels** The frozen key preserves the source numbering ('CANDIDATE_001' maps to 'AV-001', and so on), even though CRE-004’s blinding rules require randomized opaque candidate identities and AVC-00...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR209:PRRT_kwDOTH_vCM6SASkl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json' (SHA-256 880f1be62af3340ea6f49f5201c044fb3cccd2857ea016684ccca83c032c3be6).
  - Current repository evidence at 'theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json:7': '"CANDIDATE_001": "AV-001",'.

### PR211:PRRT_kwDOTH_vCM6SAc_1

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/candidate-architecture-registry.json:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/211#discussion_r3608851714
- Claim: **P2 Badge Allow equivalence-conjectured in the registry** The standard introduced in this same change says valid bidirectional translations let two candidates be marked 'equivalence-conjectured', but this machine-readable status list om...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR211:PRRT_kwDOTH_vCM6SAc_1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/candidate-architecture-registry.json' (SHA-256 10f35de3758570c30aba04c837c6ee020e04cfccabb8f25222a1d82be518744b).
  - Current repository evidence at 'theory/evaluation/candidate-architecture-registry.json:9': '"allowed_statuses": ['.

### PR217:PRRT_kwDOTH_vCM6SCBS0

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/pbts001-independent-replication-registry.json:71`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418612
- Claim: **P2 Badge Rename the calibration metadata key to preserve the path** This second 'calibration' member duplicates the path-valued 'calibration' key at line 7. Standard JSON parsers keep only one value, and Python's loader used by the new...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBS0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/pbts001-independent-replication-registry.json' (SHA-256 cb15ce75a041f4863268c5be628dc09c1b18360feaebcc9309826cf953c39329).
  - Current repository evidence at 'theory/evaluation/pbts001-independent-replication-registry.json:71': '"calibration": {'.

### PR217:PRRT_kwDOTH_vCM6SCBS4

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/pbts001-independent-replication-response-schema.json:89`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418616
- Claim: **P2 Badge Require distinct coverage entries in the response schema** The schema's exact item counts only limit array length; they do not require the eight entries to cover PA-01 through PA-08. A schema-valid submission can repeat 'PA-01...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBS4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/pbts001-independent-replication-response-schema.json' (SHA-256 1ba27c70158ec6602d3966d56af76ba4ccdc9285c69f4304ca97be1804d98eba).
  - Current repository evidence at 'theory/evaluation/pbts001-independent-replication-response-schema.json:89': '"maxItems": 8,'.

### PR218:PRRT_kwDOTH_vCM6SG4vx

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/research/pbts001-replication-run-001-coordinator-controls.md:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/218#discussion_r3611191513
- Claim: **P2 Badge Use the slot-specific seed in the frozen controls** This seed text does not match the run registry's frozen 'seed_template' ('PBTS-001-REP-001-RUN-001|{slot_id}|order-v1'). If the coordinator follows this human-facing control ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR218:PRRT_kwDOTH_vCM6SG4vx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/research/pbts001-replication-run-001-coordinator-controls.md' (SHA-256 f861716dbdea7c9a3ad2f57add94f9c5222d76e16dd974c0ff33490b1732e1e7).
  - Current repository evidence at 'docs/research/pbts001-replication-run-001-coordinator-controls.md:123': '3. seed material is 'PBTS-001-REP-001-RUN-001|slot-id|order-v1';'.

### PR224:PRRT_kwDOTH_vCM6SWc46

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/faithful-representation-specification-v1.0.json:156`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/224#discussion_r3616820802
- Claim: **P2 Badge Sync the faithful source artifact before advancing W0** This registry now advances FAITHFUL-REP-001 to the W0 proof package, but its declared 'source_artifact' ('docs/research/faithful-representation-specification-v1.0.md') st...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR224:PRRT_kwDOTH_vCM6SWc46 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/faithful-representation-specification-v1.0.json' (SHA-256 c6d4f1fd3f69bfca62fe91a2df38807bdf1c5bddbd9b67c7d3c24a1e5b5c8a11).
  - Current repository evidence at 'theory/evaluation/faithful-representation-specification-v1.0.json:45': '}'.

### PR225:PRRT_kwDOTH_vCM6SXDn-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/s_core_w0_reference.py:171`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/225#discussion_r3617043351
- Claim: **P2 Badge Do not infer sort preservation from labels** For a valid sort-preserving renaming whose fresh target name happens to start with another fixture prefix, 'renamed()' raises before constructing the renamed contract, even though l...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR225:PRRT_kwDOTH_vCM6SXDn- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/s_core_w0_reference.py' (SHA-256 6d21aaa7a70103a31185821763c3f45ba0301f6416c559e804af431a2c6f244e).
  - Current repository evidence at 'tools/s_core_w0_reference.py:171': 'raise ValueError("renaming must preserve sorts")'.

### PR225:PRRT_kwDOTH_vCM6SXDn8

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/s_core_w0_reference.py:186`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/225#discussion_r3617043347
- Claim: **P2 Badge Restrict canonical codes to the material closure** When a finite contract contains declared nodes outside 'Cl(material_seed)', this loop canonicalizes every 'self.nodes' entry rather than the theorem-facing material restrictio...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR225:PRRT_kwDOTH_vCM6SXDn8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/s_core_w0_reference.py' (SHA-256 6d21aaa7a70103a31185821763c3f45ba0301f6416c559e804af431a2c6f244e).
  - Current repository evidence at 'tools/s_core_w0_reference.py:186': 'groups.setdefault(sort_map[node], []).append(node)'.

### PR226:PRRT_kwDOTH_vCM6SXowM

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/s_core_w1_reference.py:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/226#discussion_r3617256620
- Claim: **P2 Badge Reject shared elements with conflicting denotations** For the case where the same source element id appears in multiple direct axes with a different 'denotation', this validation only enforces sort consistency. 'construct_targ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR226:PRRT_kwDOTH_vCM6SXowM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/s_core_w1_reference.py' (SHA-256 42472f9725f10240bbe9892a62c84cc65735f1de17a37a7699b1b8c7e567922f).
  - Current repository evidence at 'tools/s_core_w1_reference.py:72': 'raise W1Error(f"shared element {element_id} changes sort: {old} -> {sort}")'.

### PR229:PRRT_kwDOTH_vCM6SaGao

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `README.md:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/229#discussion_r3618166629
- Claim: **P2 Badge Regenerate the README dashboard from the updated generator** This section is inside the 'BEGIN GENERATED PROJECT FAR DASHBOARD' block, but it was not regenerated from the updated 'tools/update_readme_dashboard.py': running tha...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR229:PRRT_kwDOTH_vCM6SaGao found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'README.md' (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at 'README.md:68': ''.

### PR231:PRRT_kwDOTH_vCM6ScNF3

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `far_validation/engine.py:565`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/231#discussion_r3618991940
- Claim: **P2 Badge Decode timeout output before serializing results** When a checker times out after emitting output, 'subprocess.TimeoutExpired.stdout' and 'stderr' are 'bytes' even though 'text=True' was passed, so storing them directly here m...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR231:PRRT_kwDOTH_vCM6ScNF3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'far_validation/engine.py' (SHA-256 1b3008a73f39dbe21a8179f6c371f04c9cc7f1f4e867d015f651f9620c82beaf).
  - Current repository evidence at 'far_validation/engine.py:565': 'stderr=exc.stderr or "",'.

### PR231:PRRT_kwDOTH_vCM6ScNF9

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `far_validation/engine.py:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/231#discussion_r3618991947
- Claim: **P2 Badge Treat globstar inputs as covering direct files** In changed-file mode, 'fnmatch'/'Path.match' both return false for direct-file cases such as 'README.md' vs '**/*.md' and 'tools/run_tests.py' vs 'tools/**/*.py', even though th...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR231:PRRT_kwDOTH_vCM6ScNF9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'far_validation/engine.py' (SHA-256 1b3008a73f39dbe21a8179f6c371f04c9cc7f1f4e867d015f651f9620c82beaf).
  - Current repository evidence at 'far_validation/engine.py:95': 'if fnmatch.fnmatch(normalized, pattern) or Path(normalized).match(pattern):'.

### PR232:PRRT_kwDOTH_vCM6Sd91A

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `far_validation/tracing.py:145`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/232#discussion_r3619656401
- Claim: **P2 Badge Account for dirfd-relative traced file accesses** When a traced syscall is 'openat'/'newfstatat' against a directory fd, for example 'openat(3, "secret.txt", ...)', this branch returns 'None' and drops the access entirely. A c...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR232:PRRT_kwDOTH_vCM6Sd91A found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'far_validation/tracing.py' (SHA-256 3cd16ac267cc450d93db7a0939621b2ba71473fac42ca3507613c59153423830).
  - Current repository evidence at 'far_validation/tracing.py:145': 'return None'.

### PR234:PRRT_kwDOTH_vCM6Srbte

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/w3_5_grel.py:79`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/234#discussion_r3624592982
- Claim: **P2 Badge Reject unreachable carriers in GREL validation** When validating externally supplied GREL packages, this only checks that the declared root exists; it never verifies that all entities, values, attributes, and relations are rea...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR234:PRRT_kwDOTH_vCM6Srbte found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/w3_5_grel.py' (SHA-256 91a303bd87b05db2231f5d57d0eabf4a52307c987d88e1c3d42d30dd7102613c).
  - Current repository evidence at 'tools/w3_5_grel.py:79': 'raise FactorizationError("GREL root entity is missing")'.

### PR234:PRRT_kwDOTH_vCM6Srbti

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_w3_5_factorization.py:117`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/234#discussion_r3624592986
- Claim: **P2 Badge Require every frozen runtime check to be present** If a future change drops a required runtime check such as 'no_hidden_interpreter' but leaves the remaining checks as 'pass', this condition still accepts the record because it...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR234:PRRT_kwDOTH_vCM6Srbti found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_w3_5_factorization.py' (SHA-256 233ea87dd07aaa24a4db7fa89761f3a1bc1ee160cbe62a992b977e9fe1778511).
  - Current repository evidence at 'tools/check_w3_5_factorization.py:82': "if __name__=='__main__': raise SystemExit(main())".

### PR236:PRRT_kwDOTH_vCM6Sv2G6

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_w3_5_corpus_freeze.py:58`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/236#discussion_r3626232359
- Claim: **P2 Badge Don't hard-code the withdrawn candidate outcome** When 'W3.5' later moves to 'in_progress_candidate_complete', this checker will only accept 'current_results.candidate_invariants == "complete_no_indispensable_candidate"'. The ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR236:PRRT_kwDOTH_vCM6Sv2G6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_w3_5_corpus_freeze.py' (SHA-256 66419a598ad54c35fb458ea35113e85fc6334d8e12d2276792637472147f9cee).
  - Current repository evidence at 'tools/check_w3_5_corpus_freeze.py:58': "current=w35.get('current_results',{}); req(current.get('reasoning_contrast_corpus')=='frozen','W3.5 current corpus result must be frozen',e); expected_disc='bounded_role_conjunctive_discrimination_established' if stage in {'in_progress_spec".

### PR237:PRRT_kwDOTH_vCM6SwTr0

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/w3_5_candidate_execution.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/237#discussion_r3626404991
- Claim: **P2 Badge Score information in equivalence comparisons** For reconstructable trials, the equivalence vector can declare 'commitment_equivalent' without scoring the 'information' dimension, even though the preservation dimensions used fo...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR237:PRRT_kwDOTH_vCM6SwTr0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/w3_5_candidate_execution.py' (SHA-256 6a1ad3c7eb596e5f28f16b5f5c87fb8215e7673176f10caffa62b6e3bce87f01).
  - Current repository evidence at 'tools/w3_5_candidate_execution.py:74': '"equivalence_comparison":{"structural":"pass" if reconstruct else ("not_applicable" if not present else "fail"),"semantic":"pass" if reconstruct else ("not_applicable" if not present else "fail"),"operational":"pass" if reconstruct else ("n'.

### PR238:PRRT_kwDOTH_vCM6Swy90

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/w3-5-claim-impact-result-v1.0.json:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/238#discussion_r3626587380
- Claim: **P2 Badge Synchronize the central claim registry during claim-impact closure** This new claim-impact artifact completes the 'central_claim_impact_audit' and authorizes W5, but the canonical 'theory/evaluation/central-claim-registry.json...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR238:PRRT_kwDOTH_vCM6Swy90 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/w3-5-claim-impact-result-v1.0.json' (SHA-256 434765b0a73a221cc889f5fbd1eed5ffba4f3dd63a0a157e21ff3d81e7ae3093).
  - Current repository evidence at 'theory/evaluation/w3-5-claim-impact-result-v1.0.json:1': '{"artifact_id":"W35-CLAIM-RESULT-001","gate_effect":{"W3_5_resolved":true,"W5_authorized":true,"W5_theorem_proved":false},"nonclaims":["W5 is complete","Faithful_split is proved","a universal kernel exists","FARA primitives are universally '.

### PR238:PRRT_kwDOTH_vCM6Swy9x

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/project_status_report.py:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/238#discussion_r3626587376
- Claim: **P2 Badge Update the dashboard generators with W5 authorization** When this status report starts declaring W3.5 resolved and W5 authorized, the canonical planner path still rewrites the repository back to the old state: 'make dashboard'...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR238:PRRT_kwDOTH_vCM6Swy9x found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/project_status_report.py' (SHA-256 9eb604bb78c3b4a56100a43995212c30d6a3b07d8e549328b6a4030184406a44).
  - Current repository evidence at 'tools/project_status_report.py:53': '"- W5 theorem assembly is authorized to begin.",'.

### PR239:PRRT_kwDOTH_vCM6SxUIb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_thm_target_001.py:122`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782568
- Claim: **P2 Badge Align central claims with the bounded W5 theorem** With W5 now proving 'THM-CORE-COMMON-001' and 'THM-CORE-REP-001', the central claim registry is left contradictory: 'CLM-EXISTENCE', 'CLM-SUFFICIENCY', and 'CLM-REP-CAPACITY' ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_thm_target_001.py' (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at 'tools/check_thm_target_001.py:122': "assert claim['current_status'] not in {'supported','supported_at_registered_control_scope'}".

### PR240:PRRT_kwDOTH_vCM6Sxc8v

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/s-core-w5-lean-mechanization.json:30`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/240#discussion_r3626834843
- Claim: **P2 Badge Reconcile the canonical W5 gate with this claim** When this new artifact marks 'bounded_faithful_representation' as 'machine_checked', the canonical theorem target it names is left inconsistent: 'theory/evaluation/thm-target-0...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR240:PRRT_kwDOTH_vCM6Sxc8v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/s-core-w5-lean-mechanization.json' (SHA-256 1e9c93921189e72a5d0725baf17aeb17ab50769e2027e0038c8d5db978ba80a7).
  - Current repository evidence at 'theory/evaluation/s-core-w5-lean-mechanization.json:30': '"bounded_faithful_representation": "machine_checked",'.

### PR241:PRRT_kwDOTH_vCM6Sx4fi

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/s-core-w5-independent-review-package-v1.0.json:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/241#discussion_r3626998461
- Claim: **P2 Badge Register all mandatory proof dependencies** The frozen source list jumps directly from the construction-obstruction ledger to the W5 assembly, but the review package’s own artifact map requires reviewers to inspect W0-W4 and W...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR241:PRRT_kwDOTH_vCM6Sx4fi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/s-core-w5-independent-review-package-v1.0.json' (SHA-256 9be5efc8f46802f5b225ae526ad1c52cc4f13512667b04ef3b706549b9cb618c).
  - Current repository evidence at 'theory/evaluation/s-core-w5-independent-review-package-v1.0.json:27': '{"path": "docs/research/s-core-w5-theorem-assembly-proof-v1.0.md"},'.

### PR241:PRRT_kwDOTH_vCM6Sx4fk

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_s_core_w5_review_package.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/241#discussion_r3626998465
- Claim: **P2 Badge Compare frozen hashes to file contents** This check only compares the JSON-declared 'git_blob_sha' to another hard-coded string, so if the protected artifact changes while the registry still carries the old hash, the validator...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR241:PRRT_kwDOTH_vCM6Sx4fk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_s_core_w5_review_package.py' (SHA-256 42e29a81e41b3dab9c26f7836e87e9bc7eb10d26a21473dcfb0794d01a9c9469).
  - Current repository evidence at 'tools/check_s_core_w5_review_package.py:74': '"W5 assembly registry binding changed",'.

### PR242:PRRT_kwDOTH_vCM6Sy_r1

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/planning/architecture-neutral-research-roadmap.md:119`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/242#discussion_r3627420080
- Claim: **P2 Badge Align the generated task queue with USD W1** This roadmap now makes 'USD-W1-SCOPE-EXT' the immediate next action, but the generated planning pipeline still contradicts it: 'make plan' runs 'tools/self_advancement_plan.py', whi...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR242:PRRT_kwDOTH_vCM6Sy_r1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/planning/architecture-neutral-research-roadmap.md' (SHA-256 8e9eb2796d08b826c73313ed2b79c256f2a3822e0b4c792918dc0b62fd6eb11f).
  - Current repository evidence at 'docs/planning/architecture-neutral-research-roadmap.md:119': 'Freeze and execute one 'USD-W1-SCOPE-EXT' feature family. The recommended first unit is partial observability because it directly tests whether the explicit-state construction survives restricted access without hidden-state smuggling.'.

### PR243:PRRT_kwDOTH_vCM6SzFwm

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/243#discussion_r3627455024
- Claim: **P2 Badge Make positive fixtures satisfy S_po_fin** When this history-sensitive fixture is used to support the registered 'pass', it is not an admitted 'S_po_fin' source presentation: the scope contract added in this commit requires an ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR243:PRRT_kwDOTH_vCM6SzFwm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json' (SHA-256 7ad27dba3937160c4e34b4c56614ac143f472cb30d36dca2bd167b99c5e2b54d).
  - Current repository evidence at 'theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json:27': '"expected": "distinct_observation_histories_preserved_even_when_current_observation_matches"'.

### PR243:PRRT_kwDOTH_vCM6SzFwo

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/243#discussion_r3627455026
- Claim: **P2 Badge Use canonical USD theorem IDs** These theorem-effect keys do not match the frozen target registry: 'theory/evaluation/universal-structure-discovery-target-v1.0.json' defines the parameterized IDs as 'THM-US-INV-001[K]' and 'TH...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR243:PRRT_kwDOTH_vCM6SzFwo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json' (SHA-256 8b2ee652e026fb5498dd3c107a6609e44c1ec3f5cb78e876f07817ab642ca8ea).
  - Current repository evidence at 'theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json:43': '"THM-US-NEC-001": "unresolved",'.

### PR245:PRRT_kwDOTH_vCM6Szcoo

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tests/test_usd_w1_continuous_dynamics.py:19`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/245#discussion_r3627588072
- Claim: **P2 Badge Put these tests on the canonical unittest path** When the project’s canonical 'tools/run_tests.py'/'make test' path is used, 'unittest.TestLoader.loadTestsFromModule' only collects 'unittest.TestCase' tests, so these top-level...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR245:PRRT_kwDOTH_vCM6Szcoo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_usd_w1_continuous_dynamics.py' (SHA-256 70abbe1d309438c7ca620314cfa0201448c627286f77f281350e97a3e65fa8e4).
  - Current repository evidence at 'tests/test_usd_w1_continuous_dynamics.py:19': ''.

### PR246:PRRT_kwDOTH_vCM6SzrWU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/246#discussion_r3627674001
- Claim: **P2 Badge Exclude completed finite histories from the scope** When the admitted history domain includes 'a finite ... sequence', a completed finite trace with a fixed terminal event count is in scope, but the same contract/proof claims ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR246:PRRT_kwDOTH_vCM6SzrWU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json' (SHA-256 8441a4e81b7fb4d47c4359cd0b50a66b857bd0ec1aaae32f75336cd4d1b12987).
  - Current repository evidence at 'theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json:12': '"history_domain": "a finite or countably unbounded sequence of effectively indexed events with no frozen terminal length",'.

### PR249:PRRT_kwDOTH_vCM6S0g9r

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/249#discussion_r3627993773
- Claim: **P2 Badge Add the measurement-to-source mapping to the scope** The report freezes a future positive APC package that includes “a mapping from measurements to source states and transitions” (docs/research/usd-w1-actual-process-correspond...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR249:PRRT_kwDOTH_vCM6S0g9r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json' (SHA-256 f15d6bf77bbde44907d900f05c0d3126c7fd4d2242ab6f228767257f51d8369e).
  - Current repository evidence at 'theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json:22': '"replication or independent confirmation"'.

### PR249:PRRT_kwDOTH_vCM6S0g9v

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/249#discussion_r3627993780
- Claim: **P2 Badge Sync the program registry before routing to W2** This result routes the next decisive workstream to 'USD-W2-ALT-VOCAB', but the governing program registry still records 'USD-W1-SCOPE-EXT' as 'registered_unexecuted' and 'next_d...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR249:PRRT_kwDOTH_vCM6S0g9v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json' (SHA-256 efcfc6ba6064891d24b59ba6c5a70426dc1909a5ccbcc77986715313ad2782b7).
  - Current repository evidence at 'theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json:54': '"next_decisive_workstream": "USD-W2-ALT-VOCAB",'.

### PR250:PRRT_kwDOTH_vCM6S0qkt

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:63`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/250#discussion_r3628051855
- Claim: **P2 Badge Record the missing GREL/ARG-HIST comparison** With four candidates, the completed pairwise ledger needs six unordered comparisons, but this array records only five and omits 'GREL-001' vs 'ARG-HIST-001'. Any downstream audit o...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR250:PRRT_kwDOTH_vCM6S0qkt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json' (SHA-256 dac279da465a183bcf40c23497a9ac07988227ddaa0e648a415117fca7dad209).
  - Current repository evidence at 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:63': '"pairwise_results": ['.

### PR250:PRRT_kwDOTH_vCM6S0qkx

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/250#discussion_r3628051860
- Claim: **P2 Badge Reclassify LTS-PROV versus ARG-HIST consistently** Under the dominance rule recorded in the audit, 'LTS-PROV-001' is no worse on coverage/preservation ('pass' vs 'partial') and has lower registered costs on every numeric cost ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR250:PRRT_kwDOTH_vCM6S0qkx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json' (SHA-256 dac279da465a183bcf40c23497a9ac07988227ddaa0e648a415117fca7dad209).
  - Current repository evidence at 'theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:68': '{"left": "LTS-PROV-001", "right": "ARG-HIST-001", "classification": "incomparable_tradeoff"}'.

### PR251:PRRT_kwDOTH_vCM6S0zhH

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:38`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104192
- Claim: **P2 Badge Test GREL before preserving its dominance relations** These '*_vs_GREL' outcomes are published even though 'GREL-001' is omitted from both contract and result 'tested_vocabularies', and the checker asserts exactly that two-voc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w3-representation-invariance-result-v1.0.json' (SHA-256 6389334c3e1ec1dedc26ea1ad5ffb5d8032fce0e11aed95fd31961fe58a9ef0a).
  - Current repository evidence at 'theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:38': '"LTS_PROV_vs_GREL": "bounded_dominance_preserved"'.

### PR251:PRRT_kwDOTH_vCM6S0zhL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:50`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104195
- Claim: **P2 Badge Use the registered USD-W4-NECESSITY workstream id** Repo-wide search finds 'USD-W4-ABLATION' only in this new W3 package, while the governing POST-W5 program registers the next W4 id as 'USD-W4-NECESSITY'. Emitting the unregis...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w3-representation-invariance-result-v1.0.json' (SHA-256 6389334c3e1ec1dedc26ea1ad5ffb5d8032fce0e11aed95fd31961fe58a9ef0a).
  - Current repository evidence at 'theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:50': '"next_workstream": "USD-W4-ABLATION",'.

### PR253:PRRT_kwDOTH_vCM6S12uq

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/253#discussion_r3628492372
- Claim: **P2 Badge Include GREL in the successful set** When downstream W5 consumers use this contract as the frozen success set, 'GREL-001' is incorrectly dropped even though the W2 bounded competition records that all candidates except 'ARG-HI...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR253:PRRT_kwDOTH_vCM6S12uq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json' (SHA-256 33406af9a859c33774f46087b3a3645a4f99f71cdfa153b31b672be2bf4d92d3).
  - Current repository evidence at 'theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json:8': '"successful_candidates": ["FARA-001", "LTS-PROV-001"],'.

### PR255:PRRT_kwDOTH_vCM6S611M

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/255#discussion_r3630313815
- Claim: **P2 Badge Keep USD-H-DISC within the registered GREL support** This terminal disposition broadens reasoning-discrimination support to 'ARG-HIST', but the USD-W2 source only records 'USD-H-DISC' as 'supported_boundedly_against_GREL_001' ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR255:PRRT_kwDOTH_vCM6S611M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json' (SHA-256 641f9946dcf29bfdd40eaf88d32974ec3dc6d448fc529e0d26da84001445d48a).
  - Current repository evidence at 'theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:29': '"USD-H-DISC": "supported_for_FARA_against_GREL_and_ARG-HIST_but_not_unique_against_LTS-PROV",'.

### PR255:PRRT_kwDOTH_vCM6S611P

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/255#discussion_r3630313820
- Claim: **P2 Badge Synchronize terminal outcome with status registry** Declaring this synthesis as the 'incomparable_kernels' program outcome adds a completed USD result, but the repository status surfaces still report the old state: 'theory/eva...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR255:PRRT_kwDOTH_vCM6S611P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json' (SHA-256 641f9946dcf29bfdd40eaf88d32974ec3dc6d448fc529e0d26da84001445d48a).
  - Current repository evidence at 'theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:47': '"valid_program_outcome_mapping": "incomparable_kernels",'.

### PR256:PRRT_kwDOTH_vCM6S7HDC

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json:15`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/256#discussion_r3630412997
- Claim: **P2 Badge Include the EVC parent program in the manifest** This 'program_and_synthesis' group lists the pre-W5 USD program but omits 'theory/evaluation/post-w5-usd-next-program-v1.0.json', even though the new protocol declares 'parent_p...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR256:PRRT_kwDOTH_vCM6S7HDC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json' (SHA-256 35028a27954124d2c532d2f0e5ed1ddd707fa859fb72901d19034a452150bfcb).
  - Current repository evidence at 'theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json:15': '"docs/research/post-w5-usd-terminal-synthesis-v1.0.md",'.

### PR258:PRRT_kwDOTH_vCM6S8A12

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json:39`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/258#discussion_r3630743615
- Claim: **P2 Badge Gate all twelve adversarial challenges** The protocol’s terminal rules are keyed to 'mandatory_attack_domains', but this list stops before the two corpus domains added as R4-C11 and R4-C12 ('candidate_universe' and 'correspond...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR258:PRRT_kwDOTH_vCM6S8A12 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json' (SHA-256 89f788be840341f3ab6583f1615d1049a5ffcc69f13b06bda3f1ddd432f83585).
  - Current repository evidence at 'theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json:39': '"independence labels and universal-structure claim boundaries"'.

### PR260:PRRT_kwDOTH_vCM6S-n2N

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/260#discussion_r3631702770
- Claim: **P2 Badge Wire the IKD queue into canonical planning** In the current repo, 'tools/generate_next_tasks.py' is still the command behind 'make plan'/'docs/planning/next-actions.md', and I checked it still hard-codes the old W3.5 STRATEGIC...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR260:PRRT_kwDOTH_vCM6S-n2N found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json' (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:12': '{"target_pr":264,"workstream":"IKD-W4-CROSS-FEATURE-COMPOSITION","result":"bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions"},'.

### PR260:PRRT_kwDOTH_vCM6S-n2U

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:37`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/260#discussion_r3631702779
- Claim: **P2 Badge Block candidate scoring in the queue** The prose registration says PR #261 must freeze admission controls and “must not execute candidate scoring” ('docs/research/post-usd-internal-discovery-continuation-v1.0.md:63'), but the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR260:PRRT_kwDOTH_vCM6S-n2U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json' (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28': '}'.

### PR266:PRRT_kwDOTH_vCM6TBUHR

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_post_usd_internal_discovery_continuation.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/266#discussion_r3632706842
- Claim: **P2 Badge Restore validation for the IKD-W6 queue state** Since 'next_pr' still allows 266 above, making the only exact queue-shape check 'if next_pr==267' means the standalone validator no longer rejects an IKD-W6-active queue with the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR266:PRRT_kwDOTH_vCM6TBUHR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_post_usd_internal_discovery_continuation.py' (SHA-256 cccd7d1c158aa5d38566fd1e4bdf424c3f1155bc5a751eec1dcf60e681d00eaf).
  - Current repository evidence at 'tools/check_post_usd_internal_discovery_continuation.py:35': "assert queue['ordered_followups']==[]".

### PR267:PRRT_kwDOTH_vCM6TBxUH

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/ikd-w7-lower-bounds-v1.0.json:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/267#discussion_r3632877103
- Claim: **P2 Badge Leave W7 unresolved until all countermodels are closed** Because this result is used to move the queue to IKD-W8, marking W7 complete here skips part of the registered W6 handoff: docs/audits/ikd-w6-global-reconstruction-audit...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR267:PRRT_kwDOTH_vCM6TBxUH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/ikd-w7-lower-bounds-v1.0.json' (SHA-256 3557e505d617553defbda22549aa1cb5460b7fafd0d6d682ec8c973676054c0d).
  - Current repository evidence at 'theory/evaluation/ikd-w7-lower-bounds-v1.0.json:70': '"terminal_result": "all_five_rccd_components_have_conditional_lower_bounds_on_defined_class",'.

### PR268:PRRT_kwDOTH_vCM6TDpuf

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/268#discussion_r3633577183
- Claim: **P2 Badge Record the componentwise frontier evidence** For the W8 frontier result, this records only the final kernel and realization sets, but not the componentwise cost ledger, dominance/incomparability matrix, or a precise reference ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR268:PRRT_kwDOTH_vCM6TDpuf found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/ikd-w8-minimal-frontier-v1.0.json' (SHA-256 e65eb916b413f80df46a8a7b476dc3f8d13e957fff42b5d368c8da2b1ce5413c).
  - Current repository evidence at 'theory/evaluation/ikd-w8-minimal-frontier-v1.0.json:69': '"interpretation": "the three formerly incomparable architectures are incomparable implementations inside one commitment-equivalence class, not distinct necessary kernels"'.

### PR268:PRRT_kwDOTH_vCM6TDpum

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:39`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/268#discussion_r3633577187
- Claim: **P2 Badge Keep pre-W9 bounded kernel claims blocked** With 'next_action' now pointing at W9, narrowing the blocked claim to only unrestricted universality leaves a bounded universal/common-kernel claim unblocked before terminal adjudica...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR268:PRRT_kwDOTH_vCM6TDpum found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json' (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at 'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28': '}'.

### PR270:PRRT_kwDOTH_vCM6TEQDL

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/research/post-w9-internal-scope-challenge-v1.0.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/270#discussion_r3633800226
- Claim: **P2 Badge Add an explicit status to the challenge document** When this new 'docs/research' artifact is audited directly, it has no '## Status' section, so the document itself does not state whether it is accepted, research, provisional,...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR270:PRRT_kwDOTH_vCM6TEQDL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/research/post-w9-internal-scope-challenge-v1.0.md' (SHA-256 9f35f2235676fcb2b68068a453c14e216f7b26cdbccf3c65295ec1f905b33f2f).
  - Current repository evidence at 'docs/research/post-w9-internal-scope-challenge-v1.0.md:1': '# Post-W9 Internal Scope Challenge'.

### PR279:PRRT_kwDOTH_vCM6TGrkv

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_tue_w3_deeper_kernel.py:41`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/279#discussion_r3634720987
- Claim: **P2 Badge Handle the terminal queue state in W3 checks** When PR #280 completes, the repository’s own terminal-queue contract requires 'status == "complete"', 'next_action is None', and completed workstreams '[276, 277, 278, 279, 280]' ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR279:PRRT_kwDOTH_vCM6TGrkv found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_tue_w3_deeper_kernel.py' (SHA-256 40fc44cc11d1f8d82c7914e768abc9740e39469e89dbadaa22abc421a8992724).
  - Current repository evidence at 'tools/check_tue_w3_deeper_kernel.py:41': 'require([x["target_pr"] for x in queue["completed_workstreams"]] == [276, 277, 278, 279], "completed sequence incorrect")'.

### PR279:PRRT_kwDOTH_vCM6TGrkz

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_tue_w2_defeating_condition_campaign.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/279#discussion_r3634720991
- Claim: **P2 Badge Accept completed queues in the W2 live check** After PR #280, the authorized queue state has 'next_action' set to 'None', but this W2 regression check still dereferences 'queue["next_action"]' and only allows the in-progress P...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR279:PRRT_kwDOTH_vCM6TGrkz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_tue_w2_defeating_condition_campaign.py' (SHA-256 2987e250cd22c0342d462fd7b774d7e8811d4da056b7571fe7abc1476b1e868f).
  - Current repository evidence at 'tools/check_tue_w2_defeating_condition_campaign.py:47': 'require(queue["next_action"]["workstream"] in ("TUE-W3-DEEPER-KERNEL", "TUE-W4-FINAL-QUESTION-ANSWER"), "live queue has unauthorized workstream")'.

### PR280:PRRT_kwDOTH_vCM6THCUb

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/280#discussion_r3634855220
- Claim: **P2 Badge Clear the live TUE queue when declaring no next action** This declares the terminal program closed, but the unchanged 'theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json' still has 'status: "frozen"' wit...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR280:PRRT_kwDOTH_vCM6THCUb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json' (SHA-256 594dfec3e11248a292f3784f906dddd9a2c577d37f8cf04c2d0985e4ad3b9ca1).
  - Current repository evidence at 'theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json:13': '"next_action":null,'.

### PR281:PRRT_kwDOTH_vCM6THZ2F

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/research/upp-theorem-target-v1.0.md:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/281#discussion_r3634995151
- Claim: **P2 Badge Bind S in the sufficiency target** When later workstreams mechanize UPP-W12/W15, this sufficiency obligation leaves 'S' free: unlike the necessity target above, it never says 'forall S in C*' or otherwise fixes the domain. Tha...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR281:PRRT_kwDOTH_vCM6THZ2F found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/research/upp-theorem-target-v1.0.md' (SHA-256 6a9691918e2fd575db70275dd3b8a679bb2b8cc8b78d334ec69bb4b094860b35).
  - Current repository evidence at 'docs/research/upp-theorem-target-v1.0.md:22': '''''.

### PR281:PRRT_kwDOTH_vCM6THZ2G

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_post_tue_universal_proof_program.py:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/281#discussion_r3634995152
- Claim: **P2 Badge Validate the active queue checkpoint** This checker only defines and loads the program artifact, so the new active queue checkpoint can drift undetected. If 'post-tue-universal-proof-queue-checkpoint-v1.0.json' skips W1, adver...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR281:PRRT_kwDOTH_vCM6THZ2G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_post_tue_universal_proof_program.py' (SHA-256 e8895754a871e2d7a0dece3ace97090e2216bf15aaa61b9848f4ef40cac3aa8c).
  - Current repository evidence at 'tools/check_post_tue_universal_proof_program.py:7': 'PROGRAM = ROOT / "theory/evaluation/post-tue-universal-proof-program-v1.0.json"'.

### PR282:PRRT_kwDOTH_vCM6THfYY

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/foundation/upp_foundation_v1.py:218`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027651
- Claim: **P2 Badge Validate grounds references before accepting a system** When a transition carries a typo or missing id in 'grounds', 'ReasoningSystem.validate()' still returns success because this loop only resolves the source and target stat...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/foundation/upp_foundation_v1.py' (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at 'theory/foundation/upp_foundation_v1.py:218': 'errors.append(f"transition {transition.id} references missing state")'.

### PR282:PRRT_kwDOTH_vCM6THfYZ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/foundation/upp_foundation_v1.py:185`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027652
- Claim: **P2 Badge Add recovery witnesses to system validation** When downstream workstreams attach recovery evidence to a reasoning system, this aggregate model has no 'RecoveryWitness' collection, so the system validator cannot enforce that ea...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/foundation/upp_foundation_v1.py' (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at 'theory/foundation/upp_foundation_v1.py:185': 'observations: Tuple[Observation, ...]'.

### PR282:PRRT_kwDOTH_vCM6THfYd

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/foundation/upp_foundation_v1.py:171`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027656
- Claim: **P2 Badge Validate parsed recovery statuses by value** If a witness is hydrated from the machine-readable artifacts, 'status' will commonly be the string '"recovered"' rather than a 'RecoveryStatus' instance; because this uses identity ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/foundation/upp_foundation_v1.py' (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at 'theory/foundation/upp_foundation_v1.py:171': 'if self.status is RecoveryStatus.RECOVERED and self.output_key is None:'.

### PR283:PRRT_kwDOTH_vCM6TIDhg

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/class/upp_target_class_v1.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/283#discussion_r3635243050
- Claim: **P2 Badge Reject the actual RCCD obligation names** UPP-W1's W2 handoff says the class-neutrality audit must reject RCCD, R1-R5, their named formulations, and semantic construct loading (docs/research/upp-w1-foundation-v1.0.md:36), and ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR283:PRRT_kwDOTH_vCM6TIDhg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/class/upp_target_class_v1.py' (SHA-256 4bc562afd914018d488e9ab6ad347fe754785557e02d9fe8c97dcee1ab395c7c).
  - Current repository evidence at 'theory/class/upp_target_class_v1.py:42': '"historical identity", "uniform recovery", "rccd", "r1", "r2", "r3", "r4", "r5",'.

### PR284:PRRT_kwDOTH_vCM6TIXCy

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/contract/upp_faithfulness_contract_v1.py:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/284#discussion_r3635359587
- Claim: **P2 Badge Coerce verdict values before validation** When assessments are built from JSON/CLI data, 'verdict' will be a plain string such as '"pass"' or '"unknown"'. These 'is' checks then skip the evidence/reason requirements, while enu...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR284:PRRT_kwDOTH_vCM6TIXCy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/contract/upp_faithfulness_contract_v1.py' (SHA-256 6a6f4fbda19b7eeef6ab3086267bd85d401d06efc7f0ed14681ea6dbb087700d).
  - Current repository evidence at 'theory/contract/upp_faithfulness_contract_v1.py:44': 'if self.verdict is Verdict.UNKNOWN and not self.reason:'.

### PR284:PRRT_kwDOTH_vCM6TIXCz

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tests/test_upp_w3_contract.py:10`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/284#discussion_r3635359589
- Claim: **P2 Badge Run the W3 checker from regression tests** The new deterministic checker is never invoked by this test module, unlike the W1/W2 test suites, and it is not included in the Makefile health targets. CI can therefore pass if the W...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR284:PRRT_kwDOTH_vCM6TIXCz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_upp_w3_contract.py' (SHA-256 109b657ec1987a36d3f966952232eec998a1f6125a056e7ff934125a172b3c86).
  - Current repository evidence at 'tests/test_upp_w3_contract.py:10': 'class ContractTests(unittest.TestCase):'.

### PR285:PRRT_kwDOTH_vCM6TIa4M

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/representations/upp_representation_universe_v1.py:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/285#discussion_r3635382804
- Claim: **P2 Badge Allow effectively realized oracle support** For candidates that include an inventoried oracle claim, the new universe spec lists 'oracle' as a support kind and excludes only oracle use without an effective realization ('theory...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR285:PRRT_kwDOTH_vCM6TIa4M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/representations/upp_representation_universe_v1.py' (SHA-256 52db7f81287f38faeb279a80593b5d03111ba25b737ba5b57d851436c41d01ff).
  - Current repository evidence at 'theory/representations/upp_representation_universe_v1.py:52': 'raise ValueError("an oracle cannot be treated as effective without a separately effective realization")'.

### PR286:PRRT_kwDOTH_vCM6TIf5H

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/machinery/upp_machinery_closure_v1.py:41`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/286#discussion_r3635412254
- Claim: **P2 Badge Limit effectiveness failures to required support** Because 'validate()' runs on every declared node before reachability, this check makes an otherwise closed package open whenever it declares optional present-but-ineffective s...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR286:PRRT_kwDOTH_vCM6TIf5H found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/machinery/upp_machinery_closure_v1.py' (SHA-256 ac2d7516ba1a41dcdbbb82fbeafb6b45667123b5dd8f4b0b85cf0bb15244f15d).
  - Current repository evidence at 'theory/machinery/upp_machinery_closure_v1.py:41': 'errors.append(f"{self.node_id}: present support must be effectively usable")'.

### PR286:PRRT_kwDOTH_vCM6TIf5I

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/machinery/upp_machinery_closure_v1.py:122`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/286#discussion_r3635412255
- Claim: **P2 Badge Continue through unresolved required targets** When a required disclosed edge has 'evidence=UNKNOWN', this 'continue' prevents traversal into the declared target. If that target has its own required missing or concealed depend...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR286:PRRT_kwDOTH_vCM6TIf5I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/machinery/upp_machinery_closure_v1.py' (SHA-256 ac2d7516ba1a41dcdbbb82fbeafb6b45667123b5dd8f4b0b85cf0bb15244f15d).
  - Current repository evidence at 'theory/machinery/upp_machinery_closure_v1.py:122': 'continue'.

### PR287:PRRT_kwDOTH_vCM6TImCR

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/equivalence/upp_representation_equivalence_v1.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/287#discussion_r3635447837
- Claim: **P2 Badge Reject undeclared dependency facts** For a closed package where a dependency tuple mentions a fact that is absent from 'facts', this validation returns no error; if the correspondence adds extra 'fact_map' entries for that und...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR287:PRRT_kwDOTH_vCM6TImCR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/equivalence/upp_representation_equivalence_v1.py' (SHA-256 a39e929d7f4ce9b120b2b49e14c22adcc4ca0ac49a549b11a3e9fd98206d3089).
  - Current repository evidence at 'theory/equivalence/upp_representation_equivalence_v1.py:47': 'errors.append("empty_fact")'.

### PR287:PRRT_kwDOTH_vCM6TImCU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/287#discussion_r3635447841
- Claim: **P2 Badge Keep prior W5 validation reproducible** Advancing 'next_action' to PR 288 here leaves 'tools/check_upp_w5_machinery_closure.py' still requiring the queue to equal '{'target_pr': 287, 'workstream': 'UPP-W6-EQUIVALENCE'}'; after...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR287:PRRT_kwDOTH_vCM6TImCU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json' (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at 'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:14': '{"target_pr":289,"workstream":"UPP-W8-CONSTRAINED-EVOLUTION","result":"constrained_evolution_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"},'.

### PR288:PRRT_kwDOTH_vCM6TJvkl

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/necessity/upp_recoverable_commitment_v1.py:65`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/288#discussion_r3635879012
- Claim: **P2 Badge Require queries to actually recover commitments** When 'query_to_commitment' is empty, or when it omits a listed commitment, this 'all(...)' check is vacuously true as long as 'total_on_registered_queries' is true. That lets '...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR288:PRRT_kwDOTH_vCM6TJvkl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/necessity/upp_recoverable_commitment_v1.py' (SHA-256 518ec9f77a8be98889daca5f78d05bdcb032239d562f8829cddc7e911aa42222).
  - Current repository evidence at 'theory/necessity/upp_recoverable_commitment_v1.py:65': '),'.

### PR289:PRRT_kwDOTH_vCM6TJ0hQ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/necessity/upp_w8_constrained_evolution_v1.py:90`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/289#discussion_r3635907650
- Claim: **P2 Badge Validate transition context before returning Unknown** When a commitment-changing transition has 'admissible=Truth.UNKNOWN', these lines return 'UNKNOWN' before the checks that reject empty IDs, erased 'history_prefix', or mis...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR289:PRRT_kwDOTH_vCM6TJ0hQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/necessity/upp_w8_constrained_evolution_v1.py' (SHA-256 57fe6cc0c5c6ca61c7b10672bf46acdde94a8f213fea608b845e9568f4401674).
  - Current repository evidence at 'theory/necessity/upp_w8_constrained_evolution_v1.py:90': 'return Verdict.UNKNOWN'.

### PR290:PRRT_kwDOTH_vCM6TJ7wS

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/foundation/upp_dependency_structure_v1.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/290#discussion_r3635950306
- Claim: **P2 Badge Reject duplicate relations before proving the witness** When an assessment contains two edges with different 'edge_id's but the same source, target, kind, and temporal scope, this validation passes and 'assess_dependency_struc...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR290:PRRT_kwDOTH_vCM6TJ7wS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/foundation/upp_dependency_structure_v1.py' (SHA-256 f258c9dd5f5a7c1d097137ea3e31a87bd3004a4d34c9b6e72d4fd85cf2c7bb25).
  - Current repository evidence at 'theory/foundation/upp_dependency_structure_v1.py:74': 'edge_ids.add(edge.edge_id)'.

### PR291:PRRT_kwDOTH_vCM6TKCL8

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/foundation/upp_semantic_interpretation_v1.py:126`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/291#discussion_r3635987843
- Claim: **P2 Badge Require coverage of registered semantic items** When all premises are yes, this returns 'PROVED' for any non-empty consistent mapping, but 'SemanticAssessment' only contains the supplied interpretations and no registered item/...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR291:PRRT_kwDOTH_vCM6TKCL8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/foundation/upp_semantic_interpretation_v1.py' (SHA-256 0b5ce68c2a374d0c0efe5bd47e8a6dd0b6e28bacef958c63f9724643eecf7adb).
  - Current repository evidence at 'theory/foundation/upp_semantic_interpretation_v1.py:126': 'return Verdict.PROVED if function else Verdict.UNKNOWN'.

### PR292:PRRT_kwDOTH_vCM6TKJk3

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/history/upp_historical_trace_v1.py:94`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/292#discussion_r3636029955
- Claim: **P2 Badge Validate dependency and reason links chronologically** When a trace uses 'dependency_ids' or 'reason_ids' that point to later events, this loop ignores those references, so 'obligations()' can still mark the structural obligat...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR292:PRRT_kwDOTH_vCM6TKJk3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/history/upp_historical_trace_v1.py' (SHA-256 c0a5f3977476d40c25a9f16a43b8ccb9ed725cee66b04211223e2bf97f4f0672).
  - Current repository evidence at 'theory/history/upp_historical_trace_v1.py:94': 'for predecessor in event.predecessor_ids | event.supersedes_ids:'.

### PR293:PRRT_kwDOTH_vCM6TKVUC

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/independence/upp_component_independence_v1.py:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/293#discussion_r3636098309
- Claim: **P2 Badge Reject unregistered reduction sources** When a proposed reduction names a source outside the five registered components, this guard still allows it through; for example 'ReductionAttempt("recoverable_commitment", frozenset({"h...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR293:PRRT_kwDOTH_vCM6TKVUC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/independence/upp_component_independence_v1.py' (SHA-256 40ed8fb5cf5ee9e1c37b2559694393cb7c642d1de99e0c2ab6f67723901b0c57).
  - Current repository evidence at 'theory/independence/upp_component_independence_v1.py:53': 'return Verdict.REFUTED'.

### PR293:PRRT_kwDOTH_vCM6TKVUH

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_upp_w11_historical_trace.py:94`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/293#discussion_r3636098314
- Claim: **P2 Badge Handle terminal queues in the W11 checker** This checker is still invoked by 'tests/test_upp_w11_historical_trace.py', but the new forward-progress logic assumes 'next_action' is always an object. When the UPP queue reaches a ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR293:PRRT_kwDOTH_vCM6TKVUH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_upp_w11_historical_trace.py' (SHA-256 ea2a822f85141863f26765c52710fca3338198ab1a50be1c11bb8b045c55e62c).
  - Current repository evidence at 'tools/check_upp_w11_historical_trace.py:94': 'next_pr = next_action.get("target_pr")'.

### PR295:PRRT_kwDOTH_vCM6TLOM-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/irreducibility/upp-irreducibility-maximality-v1.0.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440071
- Claim: **P2 Badge Point to an accepted irreducibility result** This metadata names 'UPP-W13-IRREDUCIBILITY' as the supporting prior result, but the completed PR #294 artifact is 'UPP-W13-SUFFICIENCY-CONSTRUCTION' and it explicitly lists 'does_n...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLOM- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/irreducibility/upp-irreducibility-maximality-v1.0.json' (SHA-256 26d408754095692101f404fb1c1b2cff4f5a9bf9c640583f6e3c4c628f01e578).
  - Current repository evidence at 'theory/irreducibility/upp-irreducibility-maximality-v1.0.json:8': '"supporting_prior_result":"UPP-W13-IRREDUCIBILITY",'.

### PR295:PRRT_kwDOTH_vCM6TLONF

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440081
- Claim: **P2 Badge Keep the W13 audit in sync with the successor** Changing the W13 successor here to 'UPP-W14-MAXIMALITY' leaves the W13 audit saying completion advances to 'UPP-W14-IRREDUCIBILITY-MAXIMALITY' ('docs/audits/upp-w13-sufficiency-c...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLONF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json' (SHA-256 be187c6ef8bbdc30b15a0b8a09d35849a2b355cc07034dad635fa15d86ba1d95).
  - Current repository evidence at 'theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json:28': '"next_workstream": {"target_pr": 295, "workstream": "UPP-W14-MAXIMALITY"},'.

### PR295:PRRT_kwDOTH_vCM6TLONJ

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/irreducibility/upp_irreducibility_maximality_v1.py:117`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440085
- Claim: **P2 Badge Classify excluded challenges before checking embeddings** When a registered challenge is already excluded from the target class and records 'embeds_in_rccd=None' as not applicable, this check returns 'UNKNOWN' before line 118 ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLONJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/irreducibility/upp_irreducibility_maximality_v1.py' (SHA-256 4dde1eb64f04525fafc1c633fa0ca44f7b5552969e656da50e3ff86e2ad858aa).
  - Current repository evidence at 'theory/irreducibility/upp_irreducibility_maximality_v1.py:117': 'return Verdict.UNKNOWN'.

### PR296:PRRT_kwDOTH_vCM6TK9sG

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/terminal/upp_terminal_theorem_v1.py:75`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636341765
- Claim: **P2 Badge Honor blocked-dependency precedence before defeating overclaims** For evidence that both contains an unresolved or absent required property and sets an overclaim flag, this branch returns 'REFUTED/DEFEATED' before the unresolv...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TK9sG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/terminal/upp_terminal_theorem_v1.py' (SHA-256 94f1909a48aa55452ac813832f1699b90f0e9e9fdfe92b3c7ea2ac47057e5a17).
  - Current repository evidence at 'theory/terminal/upp_terminal_theorem_v1.py:75': 'return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, ("proof_standard_not_satisfied",), False)'.

### PR296:PRRT_kwDOTH_vCM6TLCCD

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/terminal/upp_terminal_theorem_v1.py:87`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636367923
- Claim: **P2 Badge Block full proof when terminal composition is absent** When evidence has 'central_semantic_theorem_kernel_checked=True' but 'executable_composition_verified=False', this early return selects 'FULL/PROVED' before the later miss...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TLCCD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/terminal/upp_terminal_theorem_v1.py' (SHA-256 94f1909a48aa55452ac813832f1699b90f0e9e9fdfe92b3c7ea2ac47057e5a17).
  - Current repository evidence at 'theory/terminal/upp_terminal_theorem_v1.py:87': 'return Adjudication(Verdict.PROVED, Outcome.FULL, ("all_registered_properties_and_kernel_checked_terminal_theorem",), True)'.

### PR297:PRRT_kwDOTH_vCM6TRTNk

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post_terminal_public_evaluation_v1.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/297#discussion_r3638690913
- Claim: **P2 Badge Use registry prohibited-promotion tokens** When a submission uses the identifiers published by 'theory/evaluation/post-terminal-public-evaluation-program-v1.0.json', several banned overclaims bypass the executable check becaus...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR297:PRRT_kwDOTH_vCM6TRTNk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post_terminal_public_evaluation_v1.py' (SHA-256 3ff34a0a540ac1174de609a609d22837b4d7bf45a8612f8cb9f412fc104e9d77).
  - Current repository evidence at 'theory/evaluation/post_terminal_public_evaluation_v1.py:40': '"internal_as_independent_replication",'.

### PR297:PRRT_kwDOTH_vCM6TRTNr

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `theory/evaluation/post_terminal_public_evaluation_v1.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/297#discussion_r3638690922
- Claim: **P2 Badge Reject unsupported evidence types** The adjudicator stores 'evidence_type' but never checks it against the registered evidence-type vocabulary, so a submission with 'evidence_type="not_a_type"' and otherwise-confirming flags i...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR297:PRRT_kwDOTH_vCM6TRTNr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'theory/evaluation/post_terminal_public_evaluation_v1.py' (SHA-256 3ff34a0a540ac1174de609a609d22837b4d7bf45a8612f8cb9f412fc104e9d77).
  - Current repository evidence at 'theory/evaluation/post_terminal_public_evaluation_v1.py:47': 'evidence_type: str'.

### PR299:PRRT_kwDOTH_vCM6TUCdN

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/decision.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/299#discussion_r3639707213
- Claim: **P2 Badge Check open closure before returning review** When 'candidate_closure' is 'OPEN' and any confirmed-medium or inferred high/critical finding is active, this early return prevents the later open-closure check from running. That c...
- Rationale: The artifact reviewed by finding PR299:PRRT_kwDOTH_vCM6TUCdN has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/decision.py' does not exist ('test -e' is false).

### PR301:PRRT_kwDOTH_vCM6TU77t

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/io.py:211`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039813
- Claim: **P2 Badge Reject non-standard JSON constants** For package files containing Python's accepted 'NaN'/'Infinity' constants inside attributes or metrics, 'json.loads' succeeds even though the input is not valid JSON; 'validate' then exits ...
- Rationale: The artifact reviewed by finding PR301:PRRT_kwDOTH_vCM6TU77t has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/io.py' does not exist ('test -e' is false).

### PR303:PRRT_kwDOTH_vCM6TVMqb

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/cli.py:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/303#discussion_r3640138711
- Claim: **P2 Badge Return the documented gate exit codes** The commercial CLI contract still defines exact gate codes as 2/3/4 for review-required/blocked/unknown (commercial/far-release-assurance/ARCHITECTURE.md:258-263), but this table makes t...
- Rationale: The artifact reviewed by finding PR303:PRRT_kwDOTH_vCM6TVMqb has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/cli.py' does not exist ('test -e' is false).

### PR303:PRRT_kwDOTH_vCM6TVMqf

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/report.py:98`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/303#discussion_r3640138717
- Claim: **P2 Badge Escape package strings before rendering Markdown** For packages whose 'release_id' or 'source_commit' contains Markdown control characters such as backticks or newlines, this raw interpolation can break out of the inline code ...
- Rationale: The artifact reviewed by finding PR303:PRRT_kwDOTH_vCM6TVMqf has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-release-assurance/src/far_release_assurance/report.py' does not exist ('test -e' is false).

### PR305:PRRT_kwDOTH_vCM6TVbST

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/far-release-assurance-e2e-gate.yml:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/305#discussion_r3640224198
- Claim: **P2 Badge Fetch full history for evidence checkout** The release-assurance CI design I checked requires this job to check out full history before producing evidence ('commercial/far-release-assurance/ARCHITECTURE.md:321-334'), but this ...
- Rationale: The artifact reviewed by finding PR305:PRRT_kwDOTH_vCM6TVbST has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path '.github/workflows/far-release-assurance-e2e-gate.yml' does not exist ('test -e' is false).

### PR306:PRRT_kwDOTH_vCM6TVtkK

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:96`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/306#discussion_r3640330535
- Claim: **P2 Badge Require explicit unknown and authorization fields** When a package omits 'authorization_requirements' or 'unknowns', these defaults silently coerce the absence to an empty tuple, so a payload that never declared “no requiremen...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR306:PRRT_kwDOTH_vCM6TVtkK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/model.py' (SHA-256 f25f9e8cd0bf1528f65104c2fff166dafcf97cf1d18e484b18dfc824144e9c46).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/model.py:96': 'trace_completeness=_bounded_number('.

### PR307:PRRT_kwDOTH_vCM6TVt_a

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/307#discussion_r3640332959
- Claim: **P2 Badge Require an authorizing edge for authorization requirements** When a required authorization node has any edge into the decision root, this treats the requirement as satisfied without checking 'dependency.relation'; because the ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR307:PRRT_kwDOTH_vCM6TVt_a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py' (SHA-256 98cdc768e66c458956e73663258d1def15685818a17147865b7108166115c948).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:28': 'if dependency.target_id == package.decision_root'.

### PR308:PRRT_kwDOTH_vCM6TVyWK

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/refund.py:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/308#discussion_r3640357187
- Claim: **P2 Badge Reject pre-purchase refund windows** When 'days_since_purchase' is negative, this check still marks the 30-day window requirement as satisfied, so an otherwise complete request with 'days_since_purchase=-1' adjudicates as 'jus...
- Rationale: The artifact reviewed by finding PR308:PRRT_kwDOTH_vCM6TVyWK has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/refund.py' does not exist ('test -e' is false).

### PR309:PRRT_kwDOTH_vCM6TV50X

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/authorization.py:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/309#discussion_r3640400960
- Claim: **P2 Badge Reject boolean values for refund amounts** For inputs that serialize 'amount' as JSON 'true' or 'false', this coercion treats the boolean as '1.0' or '0.0' instead of invalid input, and a request with all other requirements tr...
- Rationale: The artifact reviewed by finding PR309:PRRT_kwDOTH_vCM6TV50X has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/authorization.py' does not exist ('test -e' is false).

### PR310:PRRT_kwDOTH_vCM6TV9Ki

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/policy_cli.py:33`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/310#discussion_r3640420138
- Claim: **P2 Badge Validate case JSON before building refund requests** When cases are loaded from JSON, constructing 'RefundRequest' directly bypasses the validation used by the runtime loader, so malformed fixture types can be evaluated as rea...
- Rationale: The artifact reviewed by finding PR310:PRRT_kwDOTH_vCM6TV9Ki has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/policy_cli.py' does not exist ('test -e' is false).

### PR311:PRRT_kwDOTH_vCM6TWLBi

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/311#discussion_r3640500302
- Claim: **P2 Badge Restore legacy audit path for console invocations** When 'far-decision' is invoked through the installed console script, 'main()' is called with 'argv=None', so 'arguments' stays 'None' and this compatibility branch is skipped...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR311:PRRT_kwDOTH_vCM6TWLBi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/cli.py' (SHA-256 f58175d95816402404064510efac2c38006e0945119b7b6d924d204588c6f033).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/cli.py:35': 'if __name__ == "__main__":'.

### PR311:PRRT_kwDOTH_vCM6TWLBm

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/regression.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/311#discussion_r3640500307
- Claim: **P2 Badge Reject non-object run entries as invalid input** If a supplied regression suite contains a non-object entry inside 'baseline' or 'candidate' (for example 'null'), this subscript raises 'TypeError' before 'regression_cli.main()...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR311:PRRT_kwDOTH_vCM6TWLBm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/regression.py' (SHA-256 fda240cf1a245b3b51f6f5795ee59ab8e57517fdb474244d38d601a7ac7ce5b7).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/regression.py:26': 'raise ValueError("run result must be an object")'.

### PR313:PRRT_kwDOTH_vCM6TWucb

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/instrumentation.py:179`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/313#discussion_r3640708680
- Claim: **P2 Badge Reserve provenance keys before emitting node attributes** When callers record a node attribute named '_far_source', this flattening emits it as 'far.node.attribute._far_source', but the existing ingester unconditionally replac...
- Rationale: The artifact reviewed by finding PR313:PRRT_kwDOTH_vCM6TWucb has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/instrumentation.py' does not exist ('test -e' is false).

### PR314:PRRT_kwDOTH_vCM6TW6hD

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:75`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777758
- Claim: **P2 Badge Serialize evidence writes before hashing** When two identical '/v1/authorize' POSTs are handled concurrently, they intentionally resolve to the same 'evidence_id', and 'serve()' runs them in a 'ThreadingHTTPServer'; these dige...
- Rationale: The artifact reviewed by finding PR314:PRRT_kwDOTH_vCM6TW6hD has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/service.py' does not exist ('test -e' is false).

### PR314:PRRT_kwDOTH_vCM6TW6hF

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:168`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777761
- Claim: **P2 Badge Bound the decision-id path component** For an otherwise valid package with a long 'decision_id', this unbounded sanitized value becomes a single directory-name component, so common filesystems raise 'OSError: File name too lon...
- Rationale: The artifact reviewed by finding PR314:PRRT_kwDOTH_vCM6TW6hF has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/service.py' does not exist ('test -e' is false).

### PR314:PRRT_kwDOTH_vCM6TW6hJ

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:126`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777766
- Claim: **P2 Badge Reject non-standard JSON constants** When a client sends 'NaN', 'Infinity', or '-Infinity' inside payload fields that are not validated as bounded numbers, such as 'proposed_action' or 'metadata', Python's default 'json.loads'...
- Rationale: The artifact reviewed by finding PR314:PRRT_kwDOTH_vCM6TW6hJ has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/service.py' does not exist ('test -e' is false).

### PR315:PRRT_kwDOTH_vCM6TXCNX

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/store.py:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/315#discussion_r3640823736
- Claim: **P2 Badge Support the advertised runtime evidence format** At this point 'put_directory()' rejects manifests that do not contain 'evidence_id' and 'input_type'. The FAR runtime path advertised in 'EVIDENCE_STORE.md' still writes 'far-au...
- Rationale: The artifact reviewed by finding PR315:PRRT_kwDOTH_vCM6TXCNX has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/store.py' does not exist ('test -e' is false).

### PR316:PRRT_kwDOTH_vCM6TXIZT

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/security.py:190`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/316#discussion_r3640859442
- Claim: **P2 Badge Sanitize tenant evidence identifiers before returning** When tenant IDs or evidence IDs contain path separators or absolute-path prefixes, this helper returns them unchanged around the digest. The new contract recommends using...
- Rationale: The artifact reviewed by finding PR316:PRRT_kwDOTH_vCM6TXIZT has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/security.py' does not exist ('test -e' is false).

### PR316:PRRT_kwDOTH_vCM6TXIZX

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/security.py:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/316#discussion_r3640859449
- Claim: **P2 Badge Reject dots in key IDs before storing credentials** A key registered with a 'key_id' containing '.' is accepted here, but 'authenticate()' parses bearer tokens with 'token.split('.', 1)', so 'key.with.dot.secret' is looked up ...
- Rationale: The artifact reviewed by finding PR316:PRRT_kwDOTH_vCM6TXIZX has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/security.py' does not exist ('test -e' is false).

### PR317:PRRT_kwDOTH_vCM6TXS0N

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/317#discussion_r3640920604
- Claim: **P2 Badge Include the policy binding in secured evidence IDs** For the same tenant and decision payload, 'raw_evidence_id' is deterministic only from the FAR input, so changing the active 'policy_id'/version produces the same 'secured_i...
- Rationale: The artifact reviewed by finding PR317:PRRT_kwDOTH_vCM6TXS0N has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py' does not exist ('test -e' is false).

### PR319:PRRT_kwDOTH_vCM6TYhUh

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:82`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/319#discussion_r3641382514
- Claim: **P2 Badge Preserve idempotent evidence manifests across upgrade** Deployments with evidence already written by secured-service 0.1 can no longer retry the same authorization after this change: the secured evidence id is still derived on...
- Rationale: The artifact reviewed by finding PR319:PRRT_kwDOTH_vCM6TYhUh has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py' does not exist ('test -e' is false).

### PR319:PRRT_kwDOTH_vCM6TYhUi

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:118`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/319#discussion_r3641382515
- Claim: **P2 Badge Validate admin JSON field types before mutation** The new admin HTTP adapter lets malformed JSON change behavior before 'OperationsStore' validation: 'tuple(...)' raises an uncaught 'TypeError' for '"scopes": null', while 'boo...
- Rationale: The artifact reviewed by finding PR319:PRRT_kwDOTH_vCM6TYhUi has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py' does not exist ('test -e' is false).

### PR320:PRRT_kwDOTH_vCM6TYpZy

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/hardening.py:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/320#discussion_r3641428946
- Claim: **P2 Badge Report retention failure when blob deletion fails** When an expired blob directory cannot be removed, for example because of permissions or filesystem errors, 'ignore_errors=True' suppresses the failure after the database rows...
- Rationale: The artifact reviewed by finding PR320:PRRT_kwDOTH_vCM6TYpZy has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/hardening.py' does not exist ('test -e' is false).

### PR321:PRRT_kwDOTH_vCM6TYtSh

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/EXTERNAL_IDENTITY.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/321#discussion_r3641451725
- Claim: **P2 Badge Add required provenance before promoting the adapter contract** Because this new document promotes the external identity/observability adapter as a package contract without a status/provenance record or link to the execution/o...
- Rationale: The artifact reviewed by finding PR321:PRRT_kwDOTH_vCM6TYtSh has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/EXTERNAL_IDENTITY.md' does not exist ('test -e' is false).

### PR321:PRRT_kwDOTH_vCM6TYtSp

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/external_identity.py:127`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/321#discussion_r3641451733
- Claim: **P2 Badge Reject malformed temporal claims without crashing** When a token is correctly signed but omits or uses a non-integer 'iat'/'exp', these conversions run outside the parsing error path, so 'verify()' raises raw 'TypeError'/'Valu...
- Rationale: The artifact reviewed by finding PR321:PRRT_kwDOTH_vCM6TYtSp has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/external_identity.py' does not exist ('test -e' is false).

### PR322:PRRT_kwDOTH_vCM6TY-OL

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552499
- Claim: **P2 Badge Avoid revalidating assertions with the default clock** When an OIDC deployment configures 'clock_skew_seconds' above the default 30 seconds, 'verify()' first validates the token with that configured skew, but this call to 'pri...
- Rationale: The artifact reviewed by finding PR322:PRRT_kwDOTH_vCM6TY-OL has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py' does not exist ('test -e' is false).

### PR322:PRRT_kwDOTH_vCM6TY-OR

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/oidc.py:97`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552505
- Claim: **P2 Badge Convert missing time claims into auth failures** When a correctly signed OIDC JWT omits 'iat' or 'exp' or provides a non-integer object for either claim, these 'int(payload.get(...))' calls raise 'TypeError' outside any OIDC e...
- Rationale: The artifact reviewed by finding PR322:PRRT_kwDOTH_vCM6TY-OR has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/oidc.py' does not exist ('test -e' is false).

### PR323:PRRT_kwDOTH_vCM6TZIrD

- Disposition: `obsolete_after_later_changes`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/distributed.py:181`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613892
- Claim: **P2 Badge Convert probe exceptions into failed checks** When a real metadata, object-storage, or counter probe raises on a timeout/auth failure, this eager construction aborts before returning a readiness payload, so callers do not get ...
- Rationale: The artifact reviewed by finding PR323:PRRT_kwDOTH_vCM6TZIrD has been removed by later repository changes, so the path-specific condition cannot reproduce on current main. This does not claim that a differently located concern was repaired.
- Evidence:
  - At current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760, repository path 'commercial/far-decision-integrity/src/far_decision_integrity/distributed.py' does not exist ('test -e' is false).

### PR324:PRRT_kwDOTH_vCM6TZUi3

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_universality_remainder_theorem.py:107`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/324#discussion_r3641683971
- Claim: **P2 Badge Validate the completed-work ledger exactly** When a frozen completed-work item is removed or renamed but the list is padded back to 15 entries, 'validate_registry' still returns no errors because this check only enforces list ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR324:PRRT_kwDOTH_vCM6TZUi3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_universality_remainder_theorem.py' (SHA-256 ecf3cbabda707a62dc06811b97158c19f388b150d8f3a6c69fb3188bd0e46b43).
  - Current repository evidence at 'tools/check_universality_remainder_theorem.py:107': 'errors.append("completed-work nonredundancy ledger is incomplete")'.

### PR333:PRRT_kwDOTH_vCM6TbDy4

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/architecture/repository-convergence-2026-07-23.md:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/333#discussion_r3642340123
- Claim: **P2 Badge Use charter-defined artifact statuses** This new audit is introduced with 'Status: execution baseline', and the companion convergence documents use similarly descriptive statuses ('canonical convergence guidance', 'active exec...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR333:PRRT_kwDOTH_vCM6TbDy4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/architecture/repository-convergence-2026-07-23.md' (SHA-256 dff4315d49cc32bd3853bc46ed4dd070d8bc73c1e1bc68f81493e75ed282914e).
  - Current repository evidence at 'docs/architecture/repository-convergence-2026-07-23.md:4': 'Status: execution baseline'.

### PR336:PRRT_kwDOTH_vCM6TbQvA

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/336#discussion_r3642422084
- Claim: **P2 Badge Verify hashed evidence sources before accepting bundles** When a generated bundle is verified after the referenced regression suite is edited or removed, this still returns true as long as the report file is unchanged, because...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR336:PRRT_kwDOTH_vCM6TbQvA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/evidence.py' (SHA-256 04aceb87bdd17e94524cc6ae5a996ee575ad7220d580f3ce65ad6e22e830925e).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/evidence.py:74': 'return sha256_bytes(report_path.read_bytes()) == report.get("sha256")'.

### PR337:PRRT_kwDOTH_vCM6TbmOr

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/337#discussion_r3642550453
- Claim: **P2 Badge Preserve observation records from SWE-agent trajectories** When the input is a current SWE-agent trajectory that stores tool output as '{"message_type":"observation","content":...}' (as shown in the official trajectory docs: h...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR337:PRRT_kwDOTH_vCM6TbmOr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py' (SHA-256 0d604804905a7dab36e904906027445040906a548ff90e176e6dd486a7836c8d).
  - Current repository evidence at 'commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py:25': 'observation = record.get("observation") or record.get("result") or record.get("output")'.

### PR340:PRRT_kwDOTH_vCM6Tb8P_

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `research/external-validation/trace-candidate-002/protocol.json:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/340#discussion_r3642681741
- Claim: **P2 Badge Add a charter status to the frozen protocol** This 'status' records the execution phase, but the new protocol still lacks one of the charter artifact statuses (Accepted, Research, Provisional, Archive, or Unknown). Because Can...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR340:PRRT_kwDOTH_vCM6Tb8P_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'research/external-validation/trace-candidate-002/protocol.json' (SHA-256 607e35f12bd36270dd143fb188f9d3ae2264c7a6ac0f9a3e7f407b62698ae0ec).
  - Current repository evidence at 'research/external-validation/trace-candidate-002/protocol.json:4': '"status": "frozen-before-outcome-inspection",'.

### PR344:PRRT_kwDOTH_vCM6TcTFp

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/1-0-golden-clean-install.yml:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/344#discussion_r3642814795
- Claim: **P2 Badge Run the golden tests against the installed wheel** This step uses the checkout's default 'python', and the package tests prepend 'commercial/far-decision-integrity/src' to 'sys.path', so the behavioral tests exercise the worki...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR344:PRRT_kwDOTH_vCM6TcTFp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/1-0-golden-clean-install.yml' (SHA-256 11d4de2470c4e96c1f2fda0ad365763198fc46e5da2436360991ae282cc41e7e).
  - Current repository evidence at '.github/workflows/1-0-golden-clean-install.yml:54': 'run: python -m unittest discover -s commercial/far-decision-integrity/tests -p "test_*.py"'.

### PR344:PRRT_kwDOTH_vCM6TcTFr

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/releases/1.0.0-draft.md:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/344#discussion_r3642814797
- Claim: **P2 Badge Attach provenance to the cumulative release narrative** This new draft immediately summarizes a long 0.4.0→1.0.0 development path and the following sections list research, governance, and validation claims, but the artifact co...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR344:PRRT_kwDOTH_vCM6TcTFr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/releases/1.0.0-draft.md' (SHA-256 15891cfb5e1d22ff9547080564979cccd904795652c85393e4da440c067ce9fd).
  - Current repository evidence at 'docs/releases/1.0.0-draft.md:7': 'Project FAR moved from an early formal-vocabulary research repository into a consolidated research and verification system with explicit claim boundaries, mechanized validation, deterministic decision adjudication, external-trace ingestion,'.

### PR347:PRRT_kwDOTH_vCM6TcnkK

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:197`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/347#discussion_r3642936015
- Claim: **P2 Badge Escape uploaded values before rendering findings** When a user analyzes an uploaded trace whose 'action' contains HTML, that value is copied into finding descriptions and then interpolated into 'innerHTML' here, so opening the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR347:PRRT_kwDOTH_vCM6TcnkK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:197': 'baseline_adjudication.status.value,'.

### PR347:PRRT_kwDOTH_vCM6TcnkO

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/347#discussion_r3642936021
- Claim: **P2 Badge Validate event objects before parsing fields** If an uploaded JSON file has an 'events' array containing any non-object value, '_parse' passes it into '_event' and this '.get' call raises 'AttributeError', which is not caught ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR347:PRRT_kwDOTH_vCM6TcnkO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:27': ''.

### PR348:PRRT_kwDOTH_vCM6Tc-2A

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:210`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/348#discussion_r3643074604
- Claim: **P2 Badge Download the analyzed artifact instead of the sample** When a user verifies custom packages through 'runUpload()', the rendered status/changes come from '/api/analyze', but this CTA always requests '/api/example/report'. In th...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR348:PRRT_kwDOTH_vCM6Tc-2A found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:210': '"candidate": {'.

### PR348:PRRT_kwDOTH_vCM6Tc-2B

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:210`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/348#discussion_r3643074607
- Claim: **P2 Badge Render uploaded evidence in the comparison panel** For custom uploads, 'runUpload()' updates only the verdict card from '/api/analyze', while this side-by-side “Execution comparison” remains the hard-coded refund sequence. Any...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR348:PRRT_kwDOTH_vCM6Tc-2B found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:210': '"candidate": {'.

### PR350:PRRT_kwDOTH_vCM6Tdsan

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:130`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/350#discussion_r3643345247
- Claim: **P2 Badge Keep upload summaries evidence-bound** When '/api/analyze' is used for any package other than the bundled refund sample—e.g. a justified package or an unsupported non-refund decision—'_present()' still returns these refund/app...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR350:PRRT_kwDOTH_vCM6Tdsan found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:130': 'structural_changes.append('.

### PR350:PRRT_kwDOTH_vCM6Tdsas

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:251`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/350#discussion_r3643345252
- Claim: **P2 Badge Render the actual returned status** When the upload flow analyzes a package whose returned 'status' is 'justified', 'unverifiable', or 'underdetermined', this hard-coded label remains 'Result: unsupported' because 'render()' o...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR350:PRRT_kwDOTH_vCM6Tdsas found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:251': '"unknowns": [],'.

### PR351:PRRT_kwDOTH_vCM6TeaVq

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:130`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/351#discussion_r3643608853
- Claim: **P2 Badge Keep upload summaries evidence-bound** Because '_present()' also builds the response for '/api/analyze', these hard-coded refund-specific fields are returned after users upload arbitrary FAR packages; an unsupported access-con...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR351:PRRT_kwDOTH_vCM6TeaVq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:130': 'structural_changes.append('.

### PR353:PRRT_kwDOTH_vCM6TfYV2

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/formats.py:129`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/353#discussion_r3643957046
- Claim: **P2 Badge Reject XML packages that omit trace completeness** For an XML upload that omits 'trace_completeness', this line silently inserts '0' before the package reaches 'DecisionPackage.from_dict'. The same missing required field is re...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR353:PRRT_kwDOTH_vCM6TfYV2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/formats.py' (SHA-256 245cfde121dbdd9d9e78fd0841ddaa862948912a22d9f7b84f3c75f60fe50726).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/formats.py:129': 'payload["trace_completeness"] = float(payload.get("trace_completeness", 0))'.

### PR353:PRRT_kwDOTH_vCM6TfYVy

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:297`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/353#discussion_r3643957042
- Claim: **P2 Badge Wrap parser errors for supported uploads** When either upload is a malformed newly supported format, 'parse_package_file()' can now raise parser-specific exceptions such as 'yaml.YAMLError', XML parse errors, or zip/package er...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR353:PRRT_kwDOTH_vCM6TfYVy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:297': 'def example_report() -> Response:'.

### PR354:PRRT_kwDOTH_vCM6Tfu7K

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-demo/src/far_demo/app.py:170`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/354#discussion_r3644086806
- Claim: **P2 Badge Don't pass releases that remove recorded support** When a candidate removes a baseline decision-root dependency that is not in 'authorization_requirements', '_present()' still emits a high-severity 'decision_dependency_removed...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR354:PRRT_kwDOTH_vCM6Tfu7K found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-demo/src/far_demo/app.py' (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at 'commercial/far-demo/src/far_demo/app.py:170': '}[status]'.

### PR357:PRRT_kwDOTH_vCM6Tnjol

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:68`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/357#discussion_r3646979006
- Claim: **P2 Badge Validate every frozen model parameter** With the validator only checking 'temperature' and 'reasoning_effort', later edits can change or remove frozen fields like 'top_p', 'per_instance_cost_limit_usd', or 'total_cost_limit_us...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR357:PRRT_kwDOTH_vCM6Tnjol found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py' (SHA-256 e1f41e94ef45ccb92650ca5eef578a6430e294082fe239a666b5461cf0aca080).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:68': '"baseline_commit": "8ed382c",'.

### PR359:PRRT_kwDOTH_vCM6Too8m

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/359#discussion_r3647386256
- Claim: **P2 Badge Parse the verbose manifest digest** When the fallback is used for a normal single-image manifest, Docker's verbose output exposes the registry digest as a top-level 'Digest' field (see the Docker CLI docs' 'docker manifest ins...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR359:PRRT_kwDOTH_vCM6Too8m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py' (SHA-256 eb56a0a73dcdf1b5bae7326f8d00b8d990cb9f2695c75fd9e9d5b460f4948929).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:68': ')'.

### PR360:PRRT_kwDOTH_vCM6To5d8

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/far-swe-agent-execution.yml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482130
- Claim: **P2 Badge Update the documented stage name with the workflow rename** After this dispatch option is renamed, the setup guide still describes the available stages as 'resolve-image', 'preflight', and 'plan' and tells operators to run 're...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/far-swe-agent-execution.yml' (SHA-256 59e8d37483ac0eaa48dcdb1acfd7b8017906e9e7818210a123f869fa5d10092a).
  - Current repository evidence at '.github/workflows/far-swe-agent-execution.yml:11': '- prepare-environment'.

### PR369:PRRT_kwDOTH_vCM6Ttjrh

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `mechanization/far_mechanization/compare_adjudication.py:160`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223447
- Claim: **P2 Badge Reject non-finite metadata values** When package or adjudication metadata contains 'NaN', 'Infinity', or '-Infinity', Python's permissive 'json.loads' produces a 'float' and this check accepts it. 'canonical_json_bytes' then e...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'mechanization/far_mechanization/compare_adjudication.py' (SHA-256 283353eb65da96f80ae88f5299e41436c970f044f13a3d6de6ba09384faa4f2b).
  - Current repository evidence at 'mechanization/far_mechanization/compare_adjudication.py:160': 'raise InterfaceError(f"{path}.{key} must be a JSON scalar")'.

### PR369:PRRT_kwDOTH_vCM6Ttjrj

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `schemas/far-evidence-comparison-v1.schema.json:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223449
- Claim: **P2 Badge Validate embedded claims in the comparison schema** When consumers validate comparison artifacts using the published JSON Schema rather than the Python CLI, 'left' and 'right' accept any object, including '{}' or arbitrary fie...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'schemas/far-evidence-comparison-v1.schema.json' (SHA-256 95243bfa7e5514f96d38afc777d5ac562afaa506217321995da4f548a746cd44).
  - Current repository evidence at 'schemas/far-evidence-comparison-v1.schema.json:26': '"right": {"type": ["object", "null"]},'.

### PR371:PRRT_kwDOTH_vCM6TuK-m

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/governance/repository-truth-revalidation-scope.md:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/371#discussion_r3649454378
- Claim: **P2 Badge Complete the authority inventory before resolving the audit** These required categories are absent from both the machine-readable manifest and the audit's authoritative inventory, which cover only package/CLI versions, README ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR371:PRRT_kwDOTH_vCM6TuK-m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/governance/repository-truth-revalidation-scope.md' (SHA-256 9c489414865bbf61006f78edb0e6c94780f01d3295f30116ef1f4d286e75f27a).
  - Current repository evidence at 'docs/governance/repository-truth-revalidation-scope.md:28': '- generated or frozen artifacts that embed versions or status;'.

### PR373:PRRT_kwDOTH_vCM6TuR8O

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_repository_truth.py:66`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495821
- Claim: **P2 Badge Validate the README release target** Validate the anchor target as well as its displayed label. If the README link is changed back to '/releases/tag/v0.4.0' while its text remains 'v1.0.0', this phrase still matches and the se...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8O found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_repository_truth.py' (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at 'tools/check_repository_truth.py:66': 'f"The latest published GitHub repository release is [{latest_release}]",'.

### PR373:PRRT_kwDOTH_vCM6TuR8P

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_repository_truth.py:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495822
- Claim: **P2 Badge Require the authoritative repository in the record URL** Require the complete canonical GitHub release URL here. The current suffix-only test also accepts a link on another domain or in a fork, such as 'https://github.com/othe...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_repository_truth.py' (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at 'tools/check_repository_truth.py:95': 'fail("release record does not link to the authoritative GitHub release")'.

### PR381:PRRT_kwDOTH_vCM6TyRN1

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:190`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944624
- Claim: **P2 Badge Do not let transient provider logs override validated success** When SWE-agent or LiteLLM logs a transient timeout, 429, or 5xx during one of the configured provider retries and then successfully submits a non-empty patch, the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRN1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py' (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:190': 'value["predictions"], task_id, allow_implicit_instance=False'.

### PR384:PRRT_kwDOTH_vCM6TynPq

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:105`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069599
- Claim: **P2 Badge Validate the copied trajectory during restoration** When a restored artifact is missing 'trajectories/' or that file no longer matches 'run["trajectory_sha256"]', this required-evidence set still allows the run to remain 'comp...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py' (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29': '_core.main()'.

### PR389:PRRT_kwDOTH_vCM6TzgVD

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:272`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388783
- Claim: **P2 Badge Reject broken symlinks before archiving** When a prior attempt leaves a broken symlink under an artifact name such as 'instance.json', 'stdout.log', or 'sweagent-output', the preceding '.exists()' filter omits it because that ...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgVD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py' (SHA-256 2a6058ab8d4b58209c9f3e0bbfce2cf8cc7c8d9da27f3697aaf43ac49f07eb57).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:272': 'raise SystemExit(f"Attempt artifact is not a local regular path: {path}")'.

### PR392:PRRT_kwDOTH_vCM6T0n2X

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py:216`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812794
- Claim: **P2 Badge Record connection-level access-probe failures** When the provider request fails before receiving an HTTP response—for example on DNS, TLS, connection-refusal, or timeout errors—'urlopen()' raises 'urllib.error.URLError', not '...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py' (SHA-256 fa5bb3be3dbdf745d091a4e3863010dd4f4540799397fb7939aa7e9804d50971).
  - Current repository evidence at 'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py:216': 'except urllib.error.HTTPError as exc:'.

### PR399:PRRT_kwDOTH_vCM6T5NRG

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/far-swe-agent-v2-postprocess.yml:64`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/399#discussion_r3653456881
- Claim: **P2 Badge Refuse reveal evaluation after the final bundle exists** On the current completed 'main', a dispatch with 'stage=evaluate-reveal' and the confirmation phrase passes this new existence check and continues into the still-enabled...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR399:PRRT_kwDOTH_vCM6T5NRG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/far-swe-agent-v2-postprocess.yml' (SHA-256 872880280b0831e6d35081ae23a695878645a843c80986916f7b55180eccf259).
  - Current repository evidence at '.github/workflows/far-swe-agent-v2-postprocess.yml:64': '--output-dir post-freeze-reveal'.

### PR401:PRRT_kwDOTH_vCM6T5eUV

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json:84`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553318
- Claim: **P2 Badge Keep patch-design failure classified as unknown** The reveal proves only that each applied patch did not pass the target; it cannot distinguish a design error from implementation, environment, or oracle causes without the unav...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'docs/audits/swe-agent-v2-forensics/failure-taxonomy.json' (SHA-256 12d311ac7b7c9adadd50c2ced37f57b515abbf38cd0fbce14043751efb02fa53).
  - Current repository evidence at 'docs/audits/swe-agent-v2-forensics/failure-taxonomy.json:84': '"residual_risk": "A failed patch outcome must not be relabeled as a patch-design cause without direct distinguishing evidence.",'.

### PR402:PRRT_kwDOTH_vCM6T53x_

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_merged_pr_review_inventory.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698274
- Claim: **P2 Badge Reject repeated source and thread IDs** If pagination replay or overlapping retrieval produces the same record twice, the equality condition allows both copies because only conflicting duplicates are rejected. Incrementing the...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_merged_pr_review_inventory.py' (SHA-256 ad69652fd4ed51ac7b975aee9edcee5472fc5ed9834cf758c4923297e3f4cfd7).
  - Current repository evidence at 'tools/check_merged_pr_review_inventory.py:29': 'elif value in seen and seen[value] != record:'.

### PR402:PRRT_kwDOTH_vCM6T53yB

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tests/test_merged_pr_review_inventory.py:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698276
- Claim: **P2 Badge Validate the checked-in inventory in canonical tests** The canonical test path discovers this test, but every assertion validates 'self.root', which is a synthetic temporary directory; repository-wide inspection of the validat...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53yB found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tests/test_merged_pr_review_inventory.py' (SHA-256 73d91818500d917c7ebcfcd7f6efd996693ff10b2be9b8f5cec4bdfb29393933).
  - Current repository evidence at 'tests/test_merged_pr_review_inventory.py:46': 'def test_positive(self): self.assertEqual([], validate(self.root, self.sha))'.

### PR403:PRRT_kwDOTH_vCM6T6IS5

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_orphaned_docs.py:72`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792972
- Claim: **P2 Badge Preserve the documented orphan-ok exemption** When an intentionally standalone document contains the documented 'orphan-ok' marker, it is now included in 'all_docs' and therefore fails '--strict' unless linked. The repository'...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_orphaned_docs.py' (SHA-256 d833f93de7a104ccab735bc2bd74119c18c678a16ad9c6c00fda55766efb47ea).
  - Current repository evidence at 'tools/check_orphaned_docs.py:72': 'if "archive" not in path.relative_to(root).parts'.

### PR403:PRRT_kwDOTH_vCM6T6IS6

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `tools/check_proof_object.py:117`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792973
- Claim: **P2 Badge Count distinct metadata sources before suppressing warnings** When two inputs inherit the same lemma, theorem, or axiom through separate lineage paths, 'source_items' returns the same source tuple twice, so 'len(sources) != 1'...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains 'tools/check_proof_object.py' (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at 'tools/check_proof_object.py:117': 'return'.

### PR404:PRRT_kwDOTH_vCM6T6taT

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007701
- Claim: **P2 Badge Pin manual inventory runs to main** For a 'workflow_dispatch' run launched against a non-main ref, 'actions/checkout' checks out that selected ref because no 'ref' is specified. The resulting 'audit/authenticated-review-data-*...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/export-merged-pr-review-inventory.yml' (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at '.github/workflows/export-merged-pr-review-inventory.yml:29': 'fetch-depth: 1'.

### PR404:PRRT_kwDOTH_vCM6T6taU

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:78`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007702
- Claim: **P2 Badge Give reruns a new export branch** When a failed or incomplete workflow is re-run, GitHub's 'run_id' does not change (GitHub context documentation), so this reuses the branch created by the first attempt. Because the exporter e...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/export-merged-pr-review-inventory.yml' (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at '.github/workflows/export-merged-pr-review-inventory.yml:78': 'run: |'.

### PR405:PRRT_kwDOTH_vCM6T7G3-

- Disposition: `resolved_incorrectly`
- Risk: `medium`
- Confidence: `manual_high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:67`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/405#discussion_r3654155071
- Claim: **P2 Badge Report the actual number of export attempts** When all four attempts return '2', this unconditional increment changes 'attempt' from 4 to 5 before the loop exits, so the fail-closed step reports that five attempts ran even tho...
- Rationale: Inspection of the current repository evidence against the complete reviewer claim in finding PR405:PRRT_kwDOTH_vCM6T7G3- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains '.github/workflows/export-merged-pr-review-inventory.yml' (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at '.github/workflows/export-merged-pr-review-inventory.yml:67': 'attempt=$((attempt + 1))'.

