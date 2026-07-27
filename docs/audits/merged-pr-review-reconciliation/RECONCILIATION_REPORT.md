# Merged-PR finding reconciliation

Audited main: `5ca27d5c40281771cf74aa29704c2a06868a16ae`
Frozen input disposition: `resolved_incorrectly`

## Result

- Original findings reconciled: 402
- Residual findings: 400
- `fixed_on_current_main`: 2
- `still_reproducible`: 400

## Residual counts

- By risk: `{"high": 124, "medium": 276}`
- By subsystem: `{"canonical-theory": 111, "ci-and-automation": 13, "commercial-validation": 20, "comparative-experiments": 26, "documentation-and-governance": 69, "external-validation": 35, "frameworks": 13, "mechanization": 7, "repository-metadata": 6, "research-records": 4, "test-infrastructure": 7, "validation-engine": 4, "validators-and-tooling": 85}`
- By experiment-blocking status: `{"false": 219, "true": 181}`

## Unresolved P1 findings

**124 unresolved P1 findings require remediation.**

- `PR100:PRRT_kwDOTH_vCM6PX2kN` — `docs/reports/appendices/l001-blind-formalization-raw.md` — P1 Badge Use the canonical D-REP in the blind inputs This blind prompt defines representation as an explicit artifact/structure/expression/object made available for Project FAR ana
- `PR100:PRRT_kwDOTH_vCM6PX2kS` — `docs/reports/appendices/l001-adversarial-review-raw.md` — P1 Badge Restore the omitted adversarial objections Under the Complete output section, the raw adversarial transcript jumps from Objection 2 to Objection 11, while the final defeat
- `PR107:PRRT_kwDOTH_vCM6Paisx` — `theory/lemmas/core-lemmas.md` — P1 Badge Propagate L-007's new preconditions downstream The revised L-007 is now only applicable when each step decreases a finite unresolved-item measure and introduces no new unr
- `PR114:PRRT_kwDOTH_vCM6PdHTG` — `docs/reports/t005-validation-report.md` — P1 Badge Stop acceptance until dependencies are validated When this report is used as the acceptance record for T-005, the ACCEPT recommendation skips required upstream validation:
- `PR116:PRRT_kwDOTH_vCM6PdVsa` — `docs/reports/t008-validation-report.md` — P1 Badge Resolve the remaining preservation premise When a shared required-role inventory pairs roles but does not itself define those occupants as preserving structural relation, 
- `PR118:PRRT_kwDOTH_vCM6Pd0Mn` — `theory/proof-objects/T-010.proof.yaml` — P1 Badge Use a supported proof-step rule With this new priorproposition rule, the proof object no longer satisfies the repository's proof-object schema: tools/verifytheory.py and t
- `PR118:PRRT_kwDOTH_vCM6Pd0Mr` — `theory/proof-objects/T-010.proof.yaml` — P1 Badge Cite the completeness definition by a resolvable ID This premise source is not resolvable by the strict proof-object checker, which accepts metadata IDs/aliases such as DE
- `PR118:PRRT_kwDOTH_vCM6Pd0Mv` — `theory/proof-objects/T-010.proof.yaml` — P1 Badge Make the conclusion match a proved step The new conclusion text no longer exactly matches any proof step statement after s7 was removed and s6 kept a shorter statement. Bo
- `PR119:PRRT_kwDOTH_vCM6Pd8Rn` — `theory/proofs/T-011-conservative-extension.md` — P1 Badge Preserve proposition and lemma inputs before claiming proof preservation The revised condition still only freezes axioms and theorem statements/dependencies, but establish
- `PR124:PRRT_kwDOTH_vCM6Pq9Nm` — `docs/reports/foundation-final-consolidation-report.md` — P1 Badge Keep status inconsistent until backfills avoid downstream use This status is not supported by the new backfill artifacts: the reports/raw appendices validate earlier artif
- `PR132:PRRT_kwDOTH_vCM6PubMj` — `docs/reports/l008-validation-report.md` — P1 Badge Exclude L-008-dependent T-005 from the foundation set When this report is used as validation evidence for L-008, the stated supplied foundation includes T-001 through T-01
- `PR139:PRRT_kwDOTH_vCM6PvDtm` — `docs/reports/minimality-audit.md` — P1 Badge Include A1–A5 in the minimality inventory This inventory says the audit covers the accepted foundation, but it omits the five established axiom records A1–A5: both theory/
- `PR150:PRRT_kwDOTH_vCM6PxKNR` — `docs/reports/external-validation/ai-reasoning/campaign-summary.md` — P1 Badge Record falsification evidence before passing the campaign When this summary is used as the Phase 2 validation record, the claim that the campaign falsified representabilit
- `PR159:PRRT_kwDOTH_vCM6QQ_JH` — `theory/evaluation/comparative-representation/protocol-v1.0.md` — P1 Badge Record provenance before accepting CRP In this new protocol, the artifact is promoted to Accepted, but the file does not record the charter-required Question → Execution →
- `PR160:PRRT_kwDOTH_vCM6QR-_T` — `tools/validate_cre001_submission.py` — P1 Badge Match provenance checks to the submitted template For real CRE-001 bundles, the provenance object is supposed to be the completed provenance/provenance-record.template.jso
- `PR160:PRRT_kwDOTH_vCM6QR-_V` — `tools/validate_cre001_submission.py` — P1 Badge Allow assigned vocabulary labels through leakage check Because the validator scans every string in the entire bundle, listing Vocabulary A, Vocabulary B, and Vocabulary C 
- `PR164:PRRT_kwDOTH_vCM6RRYKW` — `theory/metadata/theorems.yaml` — P1 Badge Use a verifier-supported theorem status In the reviewed tree, tools/verifytheory.py accepts only Draft, Proposed, Verified, Established, or Deprecated for theorem metadata
- `PR168:PRRT_kwDOTH_vCM6RSwBn` — `tools/cre001_compile_vocabularies.py` — P1 Badge Verify against the registered reference artifact In the deterministic comparison path, the verifier uses modelfromscenario() as the reference instead of deterministic-veri
- `PR171:PRRT_kwDOTH_vCM6RUQL4` — `tools/generate_next_tasks.py` — P1 Badge Use real source gaps for strategic tasks These hard-coded GAP-001 through GAP-005 values do not describe the new CRE-002 tasks: in the generated gap report they still poin
- `PR173:PRRT_kwDOTH_vCM6RU20P` — `tools/check_cre002_preregistration.py` — P1 Badge Restore the CRE-002 preregistration check With this value, the new test fails: python -m unittest tests.testcre002preregistration invokes tools/checkcre002preregistration.
- `PR173:PRRT_kwDOTH_vCM6RU20S` — `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json` — P1 Badge Make the override path reachable before locking the scenario In this frozen scenario, Toverride requires provenance for manualoverride=true from the operator, but the init
- `PR175:PRRT_kwDOTH_vCM6RVFKq` — `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` — P1 Badge Update preregistration validation for the unlock state In the unlocked state introduced here, the committed CI path still fails: tests/testcre002preregistration.py invokes
- `PR176:PRRT_kwDOTH_vCM6RVX-c` — `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` — P1 Badge Commit the declared CRE-002 result artifacts With this line set to true, a clean checkout is declared to contain official results, but this commit does not track theory/ev
- `PR178:PRRT_kwDOTH_vCM6RV06v` — `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json` — P1 Badge Keep the override path reachable With this scenario as frozen input, Toverride can never fire: the initial evidencelog is empty, and the only evidence-producing transition
- `PR17:PRRT_kwDOTH_vCM6OR8-C` — `frameworks/FARE/mathematics/definitions/evaluation-completion.md` — P1 Badge Require completions to add missing limits Because this obligation only covers sequences whose required limit is already represented by the proposed completion, a candidate
- `PR181:PRRT_kwDOTH_vCM6RWgcF` — `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json` — P1 Badge Update Baseline 1.1 gates before unlocking In this authorized state, setting these flags to true breaks the existing Baseline 1.1 health gates: tools/checkvocabularysemant
- `PR182:PRRT_kwDOTH_vCM6RXNCP` — `tools/cre002_ext001_model.py` — P1 Badge Require every frozen output before passing candidates In this execution, requiredoutputspreserved is the gate used by build() before marking a candidate complete, but this
- `PR182:PRRT_kwDOTH_vCM6RXNCU` — `tools/cre002_ext001_native.py` — P1 Badge Validate candidate records against derived-field requirements This audit checks whether the Baseline 1.1 construct definitions themselves have requiredfields and operation
- `PR184:PRRT_kwDOTH_vCM6Rc-OK` — `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json` — P1 Badge Require all clean counted submissions to pass When there are multiple eligible uncontaminated submissions and one completes while another fails, these rules can still clas
- `PR186:PRRT_kwDOTH_vCM6Revz1` — `tools/check_cre002_ext001_rep001_team_registry.py` — P1 Badge Reject shared repositories in registry validation When eligible registrations have disjoint personnel but reuse the same repositoryidentity, this checker still appends the
- `PR188:PRRT_kwDOTH_vCM6Rfduh` — `tools/cre002_ext001_robustness.py` — P1 Badge Preserve empty arrays in the third implementation When the frozen scenario contains empty arrays (initialstate.evidencelog and initialstate.actionhistory), json.loads(...,
- `PR192:PRRT_kwDOTH_vCM6RipTt` — `tests/test_t003_adequacy_audit.py` — P1 Badge Align the audit wording checked by the test Running python -m unittest tests.testt003adequacyaudit fails here because the audit document never contains this exact phrase: 
- `PR192:PRRT_kwDOTH_vCM6RipTx` — `tests/test_t003_adequacy_audit.py` — P1 Badge Restrict the axiom/admission scan to declarations This test currently scans the entire Lean source as raw text, so it fails on existing comments rather than new proof admi
- `PR193:PRRT_kwDOTH_vCM6Rj0PR` — `.github/workflows/specification-export.yml` — P1 Badge Install pytest before running the workflow tests In the added workflow, the only setup before this command is checkout, actions/setup-python, the exporter run, and git dif
- `PR197:PRRT_kwDOTH_vCM6RpiBK` — `theory/independence/primitive-independence-evaluation.schema.json` — P1 Badge Separate per-test records from aggregate decisions This schema validates only a single testtype, but locally-independent and tested-space-independent are aggregate outcome
- `PR199:PRRT_kwDOTH_vCM6R1VGh` — `tests/test_alternative_vocabulary_competition.py` — P1 Badge Fix the self-matching global-minimality assertion This assertion makes the newly added test suite fail because the report intentionally contains the negated sentence AVC-0
- `PR200:PRRT_kwDOTH_vCM6R1kcF` — `theory/independence/global-minimality/GMA-001/README.md` — P1 Badge Use one charter-approved artifact status AGENTS.md directs all automated work to docs/governance/research-execution-charter.md, whose Repository Rules require every artifa
- `PR202:PRRT_kwDOTH_vCM6R1vYI` — `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` — P1 Badge Keep CRE-003-I's investigation fixed When CRE-003-I is used as the interpretation-only case, this changes the investigation objective from determining whether the alarm is
- `PR202:PRRT_kwDOTH_vCM6R1vYK` — `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` — P1 Badge Do not add new facts to the calculus case When CRE-003-C is evaluated as the reasoning-calculus-only variation, adding exceptionq to systemb also changes the represented m
- `PR202:PRRT_kwDOTH_vCM6R1vYM` — `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` — P1 Badge Keep the calculus constant in CRE-003-R When CRE-003-R is used to test representation/structure variation, changing the calculus from modusponens to supportedgepropagation
- `PR203:PRRT_kwDOTH_vCM6R12qG` — `tests/test_cre003_execution.py` — P1 Badge Fix the assertion string so the test suite passes When I ran python -m unittest tests.testcre003preregistration tests.testcre003execution, this assertion failed because ex
- `PR204:PRRT_kwDOTH_vCM6R2SrO` — `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py` — P1 Badge Require a registered carrier before passing When an evaluator selects only differencecarriers=["other"] and answers otherfunction="none", execution falls through to this p
- `PR206:PRRT_kwDOTH_vCM6R22Dm` — `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json` — P1 Badge Fix the locked evaluator packet hash This lock entry does not match the checked-in evaluatorpacket.md: verifyprotocollock() computes git blob SHA-1 1ea5043ccb3a10aa0f35023
- `PR208:PRRT_kwDOTH_vCM6R_ofk` — `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md` — P1 Badge Enforce the closed intake gates before scoring Because this rule is only documented here, it does not actually protect RUN-001: the inspected CRE-004 replay path (executio
- `PR20:PRRT_kwDOTH_vCM6OTp-R` — `frameworks/FARE/mathematics/theorem-index.md` — P1 Badge Keep theorem identifiers unique These new index entries reuse MT-001 through MT-003 while the existing active proofs frameworks/FARE/mathematics/proofs/T001-identity-path-
- `PR217:PRRT_kwDOTH_vCM6SCBSx` — `tools/check_pbts001_replication_package.py` — P1 Badge Keep the package validator passing its own frozen protocol For this commit, running python tools/checkpbts001replicationpackage.py fails because the protocol’s nonclaim is
- `PR220:PRRT_kwDOTH_vCM6SIkht` — `tools/update_readme_dashboard.py` — P1 Badge Close the README dashboard task append call In the target commit, running python -m pycompile tools/updatereadmedashboard.py fails with SyntaxError: '(' was never closed a
- `PR221:PRRT_kwDOTH_vCM6SIzy3` — `README.md` — P1 Badge Keep research-check aligned with README wording In this commit the README changes the required wording to “The project is deduction-first,” but tools/checkdeductionfirstpr
- `PR221:PRRT_kwDOTH_vCM6SIzy4` — `tools/check_thm_target_001.py` — P1 Badge Avoid rejecting the registered nonclaim as a claim When this new checker is invoked directly, and from the Makefile after the prior gate is fixed, it fails against the com
- `PR226:PRRT_kwDOTH_vCM6SXowJ` — `tools/check_s_core_w1.py` — P1 Badge Use the path constant for the W1 registry lookup When python tools/checkscorew1.py runs, this line always raises AttributeError because reg was rebound above to the loaded
- `PR229:PRRT_kwDOTH_vCM6SaGam` — `tools/check_faithful_representation.py` — P1 Badge Keep the faithful-representation check aligned with the spec With this new phrase guard, make research-check/make health-fast fails on the committed tree: the faithful spe
- `PR22:PRRT_kwDOTH_vCM6OWe3V` — `docs/CANONICAL_MAP.md` — P1 Badge Restore removed canonical theory entries This rewrite leaves the Theory section ending after Propositions, but the parent map also recorded canonical locations for Lemmas,
- `PR232:PRRT_kwDOTH_vCM6Sd90_` — `far_validation/weakening.py` — P1 Badge Compare the old path when auditing renames When Git reports a rename such as R059 tests/testold.py tests/testnew.py, this keeps only the new path, so show(base, path) look
- `PR233:PRRT_kwDOTH_vCM6Sfq25` — `tools/check_w3_5_corpus_freeze.py` — P1 Badge Enforce required instance versions before freezing When RCS-001 marks version as a required instance field, this per-record validation never checks for it; all 18 new sour
- `PR237:PRRT_kwDOTH_vCM6SwTry` — `tools/check_w3_5_candidate_tests.py` — P1 Badge Load preserved trial records before accepting completion For the completed candidate package, this regenerates trials from the current Python module and the result only ha
- `PR239:PRRT_kwDOTH_vCM6SxUIT` — `theory/evaluation/s-core-construction-obstruction-ledger.json` — P1 Badge Update the authoritative ledger before marking W5 complete This promotes the machine-readable ledger to W5-complete, but the same registry still declares statementauthorit
- `PR239:PRRT_kwDOTH_vCM6SxUIX` — `tools/check_thm_target_001.py` — P1 Badge Register W5 as satisfying the scoped proof gate After this commit marks the bounded Score theorem proved, this assertion locks research-gates.json in the old pre-W5 state:
- `PR240:PRRT_kwDOTH_vCM6Sxc8r` — `mechanization/lean/SCoreW5.lean` — P1 Badge Make FaithfulSplit enforce the frozen contract The new registry/doc present this as machine-checking the registered W5 Faithfulsplit, but this definition only requires a c
- `PR244:PRRT_kwDOTH_vCM6SzTq5` — `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json` — P1 Badge Preserve admitted observations in the obligations The scope admits observations as part of Sinfeff, but the registered/proved obligations never require observation relatio
- `PR245:PRRT_kwDOTH_vCM6Szcon` — `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json` — P1 Badge Require computable guard-crossing certificates For admitted sources where a guard has isolated crossings but the source does not declare computable brackets, separation/tr
- `PR251:PRRT_kwDOTH_vCM6S0zhD` — `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json` — P1 Badge Add the missing semantic-interface transform The governing POST-W5-USD-001 definition for USD-W3-INVARIANCE requires the semantic-interface replacement class, but this con
- `PR252:PRRT_kwDOTH_vCM6S1nVJ` — `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json` — P1 Badge Do not advance to W5 before W4 controls are run When this result is consumed to schedule the next USD workstream, it skips part of the registered W4 gate: the frozen progr
- `PR254:PRRT_kwDOTH_vCM6S2A_u` — `theory/evaluation/usd-w6-independence-result-v1.0.json` — P1 Badge Do not mark W6 executed without executable artifacts This block records a completed three-path execution with artifact isolation, a separate verifier, deterministic compar
- `PR261:PRRT_kwDOTH_vCM6S-3sQ` — `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json` — P1 Badge Fill mandatory candidate declarations before freezing These objects are admitted as admittedfrozenunscored, but each frozen candidate only has source/primitives/constraint
- `PR277:PRRT_kwDOTH_vCM6TGN_S` — `docs/audits/tue-w1-unknown-boundary-audit.md` — P1 Badge Preserve the registered uninstrumented boundary When this W1 package is used to authorize advancing the queue to PR 278, changing the inherited creative Unknown to instrum
- `PR278:PRRT_kwDOTH_vCM6TGhkw` — `tools/check_tue_w2_defeating_condition_campaign.py` — P1 Badge Require every frozen attack family to be exercised This check only proves that each defeating condition has at least one case, but the protocol freezes specific precommitt
- `PR290:PRRT_kwDOTH_vCM6TJ7wQ` — `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` — P1 Badge Keep the queue on the registered W10 workstream For the post-W9 state, this advances PR 291 to UPP-W10-SEMANTIC-INTERPRETATION, but the registered universal-proof program 
- `PR291:PRRT_kwDOTH_vCM6TKCL7` — `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` — P1 Badge Keep the UPP queue on the registered workstream theory/evaluation/post-tue-universal-proof-program-v1.0.json still registers PR 292 as UPP-W11-R5 for uniform-effective-rec
- `PR292:PRRT_kwDOTH_vCM6TKJkz` — `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` — P1 Badge Keep PR #293 aligned with registered sufficiency workstream The registered UPP plan assigns target PR 293 to UPP-W12-SUFFICIENCY and puts component independence/irreducibi
- `PR294:PRRT_kwDOTH_vCM6TKdMI` — `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` — P1 Badge Point the queue at the registered PR #295 workstream When a runner follows this active queue, it is sent to UPP-W14-IRREDUCIBILITY-MAXIMALITY, but the registered universal
- `PR296:PRRT_kwDOTH_vCM6TK9sE` — `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` — P1 Badge Keep historical UPP checkers compatible with terminal closure With this checkpoint now terminal (nextaction: null and the public gate open), the existing W1-W11 validation
- `PR309:PRRT_kwDOTH_vCM6TV50T` — `commercial/far-decision-integrity/src/far_decision_integrity/cli.py` — P1 Badge Keep the legacy audit CLI path working When existing callers invoke far-decision [--output ...], the new subparser treats the package path as an invalid command before the
- `PR335:PRRT_kwDOTH_vCM6TbKCT` — `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py` — P1 Badge Don't count contradictory edges as authorization support When a producer records a required node's edge to the root as contradicts (or another non-supporting relation), th
- `PR335:PRRT_kwDOTH_vCM6TbKCX` — `commercial/far-decision-integrity/src/far_decision_integrity/model.py` — P1 Badge Reject cyclic dependency graphs before adjudication For packages with two-node or longer cycles, such as auth -> root and root -> auth, this validator accepts the graph be
- `PR355:PRRT_kwDOTH_vCM6Tm8c9` — `commercial/far-demo/src/far_demo/validation_app.py` — P1 Badge Configure feedback logging before returning recorded When the Render deployment starts uvicorn fardemo.validationapp:app, this custom far.validation logger is never config
- `PR356:PRRT_kwDOTH_vCM6Tm9zN` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py` — P1 Badge Reject pre-freeze outcome fields When a pre-freeze manifest gains an outcome field, for example after execution but before the primary hash freeze someone adds {"leakedout
- `PR357:PRRT_kwDOTH_vCM6Tnjoh` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml` — P1 Badge Make the frozen SWE-agent config loadable When the four runs follow runcomparison.py’s instruction to use this file, SWE-agent v1.0 will reject this old-style agent.config
- `PR360:PRRT_kwDOTH_vCM6To5d1` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py` — P1 Badge Use the SWE-bench installreposcript property In the pinned SWE-bench harness, TestSpec exposes the repository setup script as installreposcript (the image builder writes t
- `PR360:PRRT_kwDOTH_vCM6To5d6` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py` — P1 Badge Verify the local image before accepting the lock For preflight or plan on a fresh GitHub-hosted runner, comparing the committed JSON localimageid to the manifest only prov
- `PR367:PRRT_kwDOTH_vCM6TtX1k` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` — P1 Badge Run trajectories through the registered FAR adapter The comparison reduces each trajectory to scalar, mapping, and list counts, so even a normal completed run produces no 
- `PR367:PRRT_kwDOTH_vCM6TtX1m` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` — P1 Badge Block primary regeneration after outcome reveal If an operator dispatches freeze-primary after reveal-outcomes, the workflow restores the latest postprocess artifact—inclu
- `PR367:PRRT_kwDOTH_vCM6TtX1o` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` — P1 Badge Require the complete primary artifact set When primary-freeze.json is tampered with or restored from an incompatible artifact, a manifest containing artifactcount: 0, arti
- `PR367:PRRT_kwDOTH_vCM6TtX1q` — `.github/workflows/validator-assurance.yml` — P1 Badge Retain independent provenance for the cache bundle The checksum and the cache bundle are generated by the same producer and uploaded in the same artifact, so a substituted
- `PR369:PRRT_kwDOTH_vCM6Ttjrd` — `mechanization/far_mechanization/compare_adjudication.py` — P1 Badge Bind findings to referenced package contents When adjudicate receives a comparison from an untrusted or corrupted producer, these embedded claims are normalized but never 
- `PR371:PRRT_kwDOTH_vCM6TuK-l` — `tools/check_repository_truth.py` — P1 Badge Make the checker enforce the manifest authorities When an authority or mirror entry in repository-truth-authority-v1.json changes, this checker validates only the schema s
- `PR373:PRRT_kwDOTH_vCM6TuR8N` — `docs/releases/project-far-v1.0.0.md` — P1 Badge Assign the release record an allowed status Assign this newly introduced canonical artifact exactly one of the charter’s permitted statuses—Accepted, Research, Provisional
- `PR380:PRRT_kwDOTH_vCM6Txs_H` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py` — P1 Badge Exercise SWE-agent before declaring the launch boundary reached In the added full-no-model-execution-rehearsal job, whenever parsing succeeds but SWE-agent's runtime initi
- `PR381:PRRT_kwDOTH_vCM6TyRNx` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` — P1 Badge Revalidate restored completions before selecting the next run When an execution artifact was produced by the old controller—including the misclassified v1.0.0-r1 that moti
- `PR381:PRRT_kwDOTH_vCM6TyRNy` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` — P1 Badge Block progression when a run fails terminally When the new classifier emits failedterminal for an early slot, adding it only to ALLOWEDSTATES makes the state loadable but 
- `PR384:PRRT_kwDOTH_vCM6Ty6_k` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py` — P1 Badge Align the inherited regression with sequence hardening The required test command in both .github/workflows/far-swe-agent-execution.yml and .github/workflows/far-swebench-e
- `PR384:PRRT_kwDOTH_vCM6Ty6_m` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` — P1 Badge Reject malformed noncanonical target predictions When a noncanonical .pred explicitly names the frozen task but omits modelpatch—for example {"instanceid": "", "unexpected
- `PR384:PRRT_kwDOTH_vCM6TynPj` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` — P1 Badge Reconcile before enforcing sequential ordering When restoring the exact bad state produced by the previous controller—a failedterminal slot followed by a complete slot—bas
- `PR384:PRRT_kwDOTH_vCM6TynPo` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` — P1 Badge Inspect every prediction file that claims the target If SWE-agent emits the canonical .pred plus another .pred whose payload also declares the target instance, this filter
- `PR386:PRRT_kwDOTH_vCM6TzCgi` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` — P1 Badge Reject malformed keyed target predictions When a noncanonical .pred or preds.json uses the already-supported {taskid: prediction} form, recursion reaches a value without i
- `PR389:PRRT_kwDOTH_vCM6TzgU-` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` — P1 Badge Preserve retry classification when output is absent When SWE-agent reports a genuine 429/5xx before creating sweagent-output, this early return marks the attempt failedter
- `PR389:PRRT_kwDOTH_vCM6TzgVA` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py` — P1 Badge Roll back artifacts moved before an interrupted return If shutil.move moves an artifact and then raises—for example, a KeyboardInterrupt after the rename/copy but before r
- `PR391:PRRT_kwDOTH_vCM6T0ZLE` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` — P1 Badge Require model context for NOTFOUND signals When an unsuccessful agent or tool action emits a generic JSON error such as {"status":"NOTFOUND"}—including alongside a genuine
- `PR391:PRRT_kwDOTH_vCM6T0ZLF` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` — P1 Badge Keep standalone provider timeout errors retryable When a provider reports an actual timeout in forms such as Timeout while contacting Gemini or provider request exceeded t
- `PR392:PRRT_kwDOTH_vCM6T0n2T` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json` — P1 Badge Add the required top-level case ID Every workflow stage stops in the initial python casetools.py validate step because validatemanifest() requires m.get("caseid") == CASEI
- `PR392:PRRT_kwDOTH_vCM6T0n2V` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json` — P1 Badge Correct the locked controller blob hash After the manifest identity is corrected, every validation still fails in verifysharedimplementation(): the validatedexecutecontrol
- `PR392:PRRT_kwDOTH_vCM6T0n2W` — `.github/workflows/far-swe-agent-execution-v2.yml` — P1 Badge Extract restored artifacts at the case directory On the second and subsequent execute dispatches, the uploaded artifact contains both execution-output/... and access-freez
- `PR393:PRRT_kwDOTH_vCM6T2FXp` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` — P1 Badge Validate the decoded HTTP error shape before accessing it When an HTTP error contains valid JSON whose root is not an object, or whose error member is null, a string, or a
- `PR393:PRRT_kwDOTH_vCM6T2FXq` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` — P1 Badge Record transport failures that occur while reading the body When the provider sends response headers but stalls or disconnects while the body is being read, response.read(
- `PR395:PRRT_kwDOTH_vCM6T2PsZ` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md` — P1 Badge Preserve the failed access-probe record When this freeze is merged, the replacement status records only the successful probe and removes the repository's sole account of a
- `PR396:PRRT_kwDOTH_vCM6T2ibE` — `.github/workflows/far-swe-agent-execution-v2.yml` — P1 Badge Do not let failed restores supersede the last checkpoint When this new artifact validation rejects a restore, the if: always() upload at the end of this workflow still pub
- `PR397:PRRT_kwDOTH_vCM6T4r2a` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json` — P1 Badge Preserve the source artifact beyond its expiry The only copy of the 73-file execution source is GitHub artifact 8635674915, and this lock records that it expires on 2026-0
- `PR397:PRRT_kwDOTH_vCM6T4r2b` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` — P1 Badge Bind the reveal to the currently verified freeze When post-freeze-reveal was generated against an older primary freeze, this verifier accepts it because it checks only the
- `PR397:PRRT_kwDOTH_vCM6T4r2c` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` — P1 Badge Recompute the final report from the revealed outcomes When the derived JSON or Markdown report is accidentally edited, verifyreveal checks only that the final JSON points 
- `PR398:PRRT_kwDOTH_vCM6T5D8v` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` — P1 Badge Preserve the evaluation evidence behind these hashes After the workflow artifact's 90-day retention period expires, the committed testoutputsha256 and runinstancelogsha256
- `PR398:PRRT_kwDOTH_vCM6T5D8w` — `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` — P1 Badge Declare a status for each new reveal artifact This new outcome artifact, like the three companion files added by the commit, does not declare whether its status is Accepte
- `PR399:PRRT_kwDOTH_vCM6T5NRD` — `.github/workflows/far-swe-agent-execution-v2.yml` — P1 Badge Enforce the execution freeze independently of the selected ref When workflowdispatch selects a branch or tag where bundle-sha256.json is absent, this guard inspects that c
- `PR400:PRRT_kwDOTH_vCM6T5R2m` — `docs/audits/theory-correction-audit-2026-07-26.md` — P1 Badge Keep correction artifacts provisional until replicated In the reviewed tree, the only new provenance is this single audit and its decision-log entry; no replication record
- `PR400:PRRT_kwDOTH_vCM6T5R2n` — `tools/check_semantic_consistency.py` — P1 Badge Scan all active artifacts before reporting semantic consistency When semantic-check is run on this commit, it reports PASS even though active non-archive artifacts outside
- `PR401:PRRT_kwDOTH_vCM6T5eUS` — `tools/check_swe_agent_v2_forensics.py` — P1 Badge Validate the evidence inventory against its source locks The validator never loads evidence-inventory.json, so deleting an artifact, changing a hash, or mislabeling extern
- `PR401:PRRT_kwDOTH_vCM6T5eUU` — `tools/check_swe_agent_v2_forensics.py` — P1 Badge Reconcile timeline facts with the frozen run records If a timeline's outcome, call budget, termination reason, patch result, or grader result is changed, validation still 
- `PR402:PRRT_kwDOTH_vCM6T53x-` — `tools/check_merged_pr_review_inventory.py` — P1 Badge Reject incomplete per-PR manifests When countsperpr is empty, omits an inventoried PR, or reports endpoint counts that disagree with the raw records, this loop merely find
- `PR402:PRRT_kwDOTH_vCM6T53x9` — `docs/audits/merged-pr-review-audit/retrieval-manifest.json` — P1 Badge Include standard merge commits in the inventory At the audited SHA, git log --first-parent contains 138 additional commits with subjects such as Merge pull request #395 fr
- `PR403:PRRT_kwDOTH_vCM6T6IS4` — `tools/check_proof_object.py` — P1 Badge Do not weaken final theorem-conclusion alignment When a proof-object conclusion is much longer than the registered theorem statement, using the shorter vocabulary as the d
- `PR404:PRRT_kwDOTH_vCM6T6taR` — `tools/export_merged_pr_review_inventory.py` — P1 Badge Tie the live API snapshot to the audited SHA When another PR merges before or during an export, this live state=closed enumeration can include or omit repository state new
- `PR70:PRRT_kwDOTH_vCM6OvPip` — `docs/releases/project-far-v0.2.0.md` — P1 Badge Declare the release artifact status The root AGENTS.md requires compliance with docs/governance/research-execution-charter.md, whose Repository Rules require every artifac
- `PR87:PRRT_kwDOTH_vCM6PG65I` — `tools/update_readme_dashboard.py` — P1 Badge Exclude interpreter caches from generated repository indexes When a developer has Python bytecode under tools/pycache, this recursive scan indexes those local cache files;
- `PR95:PRRT_kwDOTH_vCM6PWt_O` — `docs/reports/foundation-validation-report.md` — P1 Badge Apply the collective sufficiency criterion In contexts where normativity, semantics, or validity are supplied by FARA or later artifacts, this marks AX-001 as a sufficienc
- `PR96:PRRT_kwDOTH_vCM6PXUsp` — `docs/reports/ax001-circularity-investigation.md` — P1 Badge Demote AX-001 when the review concludes inconclusive This line explicitly decides not to revise AX-001, but the same report records that AX-001's provisional result is str
- `PR99:PRRT_kwDOTH_vCM6PXsa1` — `docs/reports/ax001-stability-review.md` — P1 Badge Do not pass sufficiency via downstream theory When this gate is used to authorize L-001, resolving AX-001 sufficiency by assigning admissibility, representation, interpret

## Complete dispositions

### PR100:PRRT_kwDOTH_vCM6PX2kN

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/appendices/l001-blind-formalization-raw.md:20`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/appendices/l001-blind-formalization-raw.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR100:PRRT_kwDOTH_vCM6PX2kN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use the canonical D-REP in the blind inputs This blind prompt defines representation as an explicit artifact/structure/expression/object made available for Project FAR ana' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/appendices/l001-blind-formalization-raw.md` (SHA-256 b52017245b3a999538795ba944c335a9ca898a3335afd6bda3572d8bd20c5175).
  - Current repository evidence at `docs/reports/appendices/l001-blind-formalization-raw.md:20`: '4. Accepted term: representation means an explicit artifact, structure, expression, or object by which reasoning content, state, or role is made available for analysis in Project FAR.'.
  - The later-change audit compared `docs/reports/appendices/l001-blind-formalization-raw.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR100:PRRT_kwDOTH_vCM6PX2kS

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/appendices/l001-adversarial-review-raw.md:148`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/appendices/l001-adversarial-review-raw.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR100:PRRT_kwDOTH_vCM6PX2kS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Restore the omitted adversarial objections Under the Complete output section, the raw adversarial transcript jumps from Objection 2 to Objection 11, while the final defeat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/appendices/l001-adversarial-review-raw.md` (SHA-256 7ec1db88534259985c79799260917d2dd8a76c50d2f1e468689e99cc9c4b30bf).
  - Current repository evidence at `docs/reports/appendices/l001-adversarial-review-raw.md:148`: '## Objection 11: “Operation” is not needed and may introduce dependency confusion'.
  - The later-change audit compared `docs/reports/appendices/l001-adversarial-review-raw.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR101:PRRT_kwDOTH_vCM6PYy6a

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/doctrine/isolation-classification.md:3`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/doctrine/isolation-classification.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR101:PRRT_kwDOTH_vCM6PYy6a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record provenance before marking doctrine accepted The root AGENTS.md requires compliance with docs/governance/research-execution-charter.md, which limits artifact statuse' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/doctrine/isolation-classification.md` (SHA-256 7ecc2e234c833dbb6467fc416f68d861a934e2e332c55ff1f5b3704a4c1c4fdf).
  - Current repository evidence at `docs/doctrine/isolation-classification.md:3`: 'Status: Accepted Methodology'.
  - The later-change audit compared `docs/doctrine/isolation-classification.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR102:PRRT_kwDOTH_vCM6PZNLb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/lemmas/core-lemmas.md:25`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/lemmas/core-lemmas.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR102:PRRT_kwDOTH_vCM6PZNLb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Define participating collection before canonical use When downstream users consume core-lemmas.md as the canonical lemma source, this revised statement relies on participa' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/lemmas/core-lemmas.md` (SHA-256 fce9744c6d4efa0b23baacc417eae5eb5b952a3973939be6cf5f698998d138f9).
  - Current repository evidence at `theory/lemmas/core-lemmas.md:25`: 'No participating collection of representations satisfies Project FAR Axiom 2 unless it possesses representational structure.'.
  - The later-change audit compared `theory/lemmas/core-lemmas.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR103:PRRT_kwDOTH_vCM6PZYQQ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/l003-validation-report.md:44`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/l003-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR103:PRRT_kwDOTH_vCM6PZYQQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Track D-INV as a required L-003 dependency The revised L-003 statement now makes within an investigation part of the condition, and this row itself says that investigation' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/l003-validation-report.md` (SHA-256 2aa53345742c37a234eb9c3cdce3f0a47db6d701a7469a019ba82c97681f7f90).
  - Current repository evidence at `docs/reports/l003-validation-report.md:44`: '| D-INV | Informative | Axiom 3 requires interpretation within an investigation, so the investigation context is necessary to state the clarified result. Because A3 already carries that contextual condition and the existing declared depende'.
  - The later-change audit compared `docs/reports/l003-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR107:PRRT_kwDOTH_vCM6Pais0

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/l007-validation-report.md:60`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/l007-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR107:PRRT_kwDOTH_vCM6Pais0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register the new L-007 proof obligations This report states that the core proof now directly depends on finite unresolved-item measure and the no-new-unresolved-item condi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/l007-validation-report.md` (SHA-256 0e2c5f8f145e91293f1721ea25b266b54da7239277ffd7d7eff05422b0776509).
  - Current repository evidence at `docs/reports/l007-validation-report.md:60`: 'No dependency registry or dependency graph modification was made. The core proof depends directly on finite FAR representation, normalization procedure, finite unresolved-item measure, and a no-new-unresolved-item condition. Candidate infla'.
  - The later-change audit compared `docs/reports/l007-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR107:PRRT_kwDOTH_vCM6Paisx

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/lemmas/core-lemmas.md:85`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/lemmas/core-lemmas.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR107:PRRT_kwDOTH_vCM6Paisx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Propagate L-007's new preconditions downstream The revised L-007 is now only applicable when each step decreases a finite unresolved-item measure and introduces no new unr" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/lemmas/core-lemmas.md` (SHA-256 fce9744c6d4efa0b23baacc417eae5eb5b952a3973939be6cf5f698998d138f9).
  - Current repository evidence at `theory/lemmas/core-lemmas.md:85`: 'A normalization procedure over a finite FAR representation terminates if each normalization step strictly decreases a finite unresolved-item measure for ordering, labeling, and redundancy and introduces no new unresolved item.'.
  - The later-change audit compared `theory/lemmas/core-lemmas.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR110:PRRT_kwDOTH_vCM6PcQlI

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/foundation-validation-consolidation.md:48`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/foundation-validation-consolidation.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR110:PRRT_kwDOTH_vCM6PcQlI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Avoid retroactively labeling earlier validations as I1 When readers use this consolidation as the single status artifact for the AX-001→T-001 chain, this sentence overstat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-validation-consolidation.md` (SHA-256 da776b090e643e5efb3efe1db01cf828e1bdb1df4d24eb0331519e828dfd0764).
  - Current repository evidence at `docs/reports/foundation-validation-consolidation.md:48`: 'All independent evaluations were classified as I1 — Claimed Isolation unless otherwise stated in their reports. This means repository access was prohibited by instruction but not technically prevented by the execution environment.'.
  - The later-change audit compared `docs/reports/foundation-validation-consolidation.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR111:PRRT_kwDOTH_vCM6PctNL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proofs/T-002-primitive-independence.md:11`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proofs/T-002-primitive-independence.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR111:PRRT_kwDOTH_vCM6PctNL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update theorem catalogs after narrowing T-002 Because this line narrows T-002 from derivability to deletion-only eliminability, the companion catalogs now publish a strong' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proofs/T-002-primitive-independence.md` (SHA-256 de20ee14b10b1e92137a5836c236130adbeac8533eee26a025dd620c3d9e671b).
  - Current repository evidence at `theory/proofs/T-002-primitive-independence.md:11`: 'Within the current framework and deletion-only reduction standard, none of the five primitives is eliminable in favor of the other four without loss of expressive power:'.
  - The later-change audit compared `theory/proofs/T-002-primitive-independence.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR112:PRRT_kwDOTH_vCM6PcwlR

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proofs/P-001-first-propositions.md:25`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proofs/P-001-first-propositions.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align P-002 metadata with the revised proposition This narrows the canonical P-002 wording, but the machine-readable P-002 entry still records the old scope/claim in theor' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proofs/P-001-first-propositions.md` (SHA-256 6b2ca7972d3478ffd38ba356e35ab712543a24ce779271ce04ba0ce126a4b292).
  - Current repository evidence at `theory/proofs/P-001-first-propositions.md:25`: 'Every scoped reasoning process satisfying Project FAR Axiom 2 and involving a participating collection of more than one representation has, for Project FAR evaluation, a representational structure.'.
  - The later-change audit compared `theory/proofs/P-001-first-propositions.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR112:PRRT_kwDOTH_vCM6PcwlS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/p003-validation-report.md:40`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/p003-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register the semantic-content dependency for P-003 The audit classifies the semantic content definition as logically required, but the next line leaves metadata unchanged;' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/p003-validation-report.md` (SHA-256 fc7988eb46b084b2c32dbd806f10d460a3b45609802eab24bb69ebb7e421d2c8).
  - Current repository evidence at `docs/reports/p003-validation-report.md:40`: 'Dependency modifications: none. Metadata was not modified because no genuine metadata error requiring registry correction was demonstrated.'.
  - The later-change audit compared `docs/reports/p003-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR112:PRRT_kwDOTH_vCM6PcwlU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/p004-validation-report.md:40`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/p004-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR112:PRRT_kwDOTH_vCM6PcwlU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reconcile the P-004 D-INT dependency This audit downgrades D-INT to informative and then says no metadata correction is needed, but theory/metadata/propositions.yaml:51-54' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/p004-validation-report.md` (SHA-256 076eedafad80156cc330c436ed9846687dc761afff70e0b11d44cef4c5fda879).
  - Current repository evidence at `docs/reports/p004-validation-report.md:40`: 'Dependency modifications: none. Metadata was not modified because no genuine metadata error requiring registry correction was demonstrated.'.
  - The later-change audit compared `docs/reports/p004-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR113:PRRT_kwDOTH_vCM6PdBj1

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/metadata/theorems.yaml:73`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/metadata/theorems.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR113:PRRT_kwDOTH_vCM6PdBj1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Keep DEF-033 while the proof object still uses it With this dependency list reduced to only DEF-030, DEF-031, and DEF-034, T-004's machine proof object still cites DEF-033" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/metadata/theorems.yaml` (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at `theory/metadata/theorems.yaml:73`: 'derived_concepts:'.
  - The later-change audit compared `theory/metadata/theorems.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR114:PRRT_kwDOTH_vCM6PdHTG

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/t005-validation-report.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/t005-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR114:PRRT_kwDOTH_vCM6PdHTG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Stop acceptance until dependencies are validated When this report is used as the acceptance record for T-005, the ACCEPT recommendation skips required upstream validation:' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/t005-validation-report.md` (SHA-256 5aa97968ca46c6c40e7e6b7df698fd43bfb50372ae582d47a2d2b7021f03b5ed).
  - Current repository evidence at `docs/reports/t005-validation-report.md:5`: 'Final recommendation: ACCEPT.'.
  - The later-change audit compared `docs/reports/t005-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR115:PRRT_kwDOTH_vCM6PdLxu

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proofs/T-006-primitive-sufficiency.md:32`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proofs/T-006-primitive-sufficiency.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR115:PRRT_kwDOTH_vCM6PdLxu found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Restore canonical notation dependency When T-006 is treated as an Established proof under the repo's documented verification gates, this dependency rewrite drops theory/no" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proofs/T-006-primitive-sufficiency.md` (SHA-256 e934b08922bfc8dd6acc844cdd18b05748eb2643c9c69adca52a264db42d7b8f).
  - Current repository evidence at `theory/proofs/T-006-primitive-sufficiency.md:32`: '- D-CALC — Reasoning Calculus'.
  - The later-change audit compared `theory/proofs/T-006-primitive-sufficiency.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR116:PRRT_kwDOTH_vCM6PdVsa

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/t008-validation-report.md:151`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/t008-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR116:PRRT_kwDOTH_vCM6PdVsa found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Resolve the remaining preservation premise When a shared required-role inventory pairs roles but does not itself define those occupants as preserving structural relation, ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/t008-validation-report.md` (SHA-256 f0d2806c2376fabd3f8306c1592cf4745ee15b9f354a78fed37c2a0fba05bf24).
  - Current repository evidence at `docs/reports/t008-validation-report.md:151`: 'No open question blocks T-008 after revision.'.
  - The later-change audit compared `docs/reports/t008-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR116:PRRT_kwDOTH_vCM6PdVsb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/dependencies/dependency-graph.md:135`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/dependencies/dependency-graph.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR116:PRRT_kwDOTH_vCM6PdVsb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update the stale T-008 circularity audit After dropping T-003 from T-008 here, the current circularity audit still lists Dependencies: L-006, T-003, T-004 for T-008 (theor' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/dependencies/dependency-graph.md` (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at `theory/dependencies/dependency-graph.md:135`: 'Depends on: L-006, T-004.'.
  - The later-change audit compared `theory/dependencies/dependency-graph.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR117:PRRT_kwDOTH_vCM6Pdln3

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proofs/T-009-canonical-normal-form.md:52`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proofs/T-009-canonical-normal-form.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR117:PRRT_kwDOTH_vCM6Pdln3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require terminal zero-unresolved state for normal form The revised proof uses L-007 to get termination, but termination only says every performed step decreases the finite' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proofs/T-009-canonical-normal-form.md` (SHA-256 f128bebccfe23f073beea36f7b6c27dfdb533b748fc4079977fe2212ae4737ef).
  - Current repository evidence at `theory/proofs/T-009-canonical-normal-form.md:52`: 'Therefore every finite scoped FAR representation admits canonical normal form under supplied normalization rules satisfying the stated conditions.'.
  - The later-change audit compared `theory/proofs/T-009-canonical-normal-form.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR117:PRRT_kwDOTH_vCM6Pdln5

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/t009-validation-report.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/t009-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR117:PRRT_kwDOTH_vCM6Pdln5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align T-009 status with the REVISE outcome This report records the final recommendation as REVISE and later says the stopping rule prevents T-010 from beginning, but the s' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/t009-validation-report.md` (SHA-256 3c2f5f1c3cb18dbce97b823b2c19e9a20777a0c72172cce3132f302937f7dcdf).
  - Current repository evidence at `docs/reports/t009-validation-report.md:5`: 'Original validation finding: REVISE.'.
  - The later-change audit compared `docs/reports/t009-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR118:PRRT_kwDOTH_vCM6Pd0Mn

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/proof-objects/T-010.proof.yaml:46`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-010.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Use a supported proof-step rule With this new priorproposition rule, the proof object no longer satisfies the repository's proof-object schema: tools/verifytheory.py and t" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-010.proof.yaml` (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at `theory/proof-objects/T-010.proof.yaml:46`: 'rule: prior_proposition'.
  - The later-change audit compared `theory/proof-objects/T-010.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR118:PRRT_kwDOTH_vCM6Pd0Mr

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/proof-objects/T-010.proof.yaml:21`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-010.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Cite the completeness definition by a resolvable ID This premise source is not resolvable by the strict proof-object checker, which accepts metadata IDs/aliases such as DE' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-010.proof.yaml` (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at `theory/proof-objects/T-010.proof.yaml:21`: 'source: DEF-038'.
  - The later-change audit compared `theory/proof-objects/T-010.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR118:PRRT_kwDOTH_vCM6Pd0Mv

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/proof-objects/T-010.proof.yaml:56`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-010.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR118:PRRT_kwDOTH_vCM6Pd0Mv found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Make the conclusion match a proved step The new conclusion text no longer exactly matches any proof step statement after s7 was removed and s6 kept a shorter statement. Bo' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-010.proof.yaml` (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at `theory/proof-objects/T-010.proof.yaml:56`: 'conclusion: Given a FAR representation that is complete relative to a reconstruction objective, scope, and specified interpretation, the explicitly represented reasoning process can be reconstructed from its represented initial state, struc'.
  - The later-change audit compared `theory/proof-objects/T-010.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR119:PRRT_kwDOTH_vCM6Pd8Rn

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/proofs/T-011-conservative-extension.md:11`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proofs/T-011-conservative-extension.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR119:PRRT_kwDOTH_vCM6Pd8Rn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve proposition and lemma inputs before claiming proof preservation The revised condition still only freezes axioms and theorem statements/dependencies, but establish' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proofs/T-011-conservative-extension.md` (SHA-256 7c88bcff6ef4166a9482df35eeb03e45a1fc484487aadd9a8ba22f34112f4e0e).
  - Current repository evidence at `theory/proofs/T-011-conservative-extension.md:11`: 'If an extension `E` of Project FAR introduces no new primitive, adds only terms or machinery definable from existing primitives or established derived concepts, alters no canonical definition, changes no established axiom or theorem stateme'.
  - The later-change audit compared `theory/proofs/T-011-conservative-extension.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR119:PRRT_kwDOTH_vCM6Pd8Rq

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/metadata/theorems.yaml:234`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/metadata/theorems.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR119:PRRT_kwDOTH_vCM6Pd8Rq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align D-026 with the revised conservative-extension scope This narrowed T-011 scope is not propagated to the canonical derived concept it still advertises: D-026 in theory' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/metadata/theorems.yaml` (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at `theory/metadata/theorems.yaml:234`: 'scope: canonical FAR representations'.
  - The later-change audit compared `theory/metadata/theorems.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR120:PRRT_kwDOTH_vCM6Pp34s

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/proof-object-schema.yaml:45`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/proof-object-schema.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR120:PRRT_kwDOTH_vCM6Pp34s found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Document priorproposition in the canonical rule list Adding priorproposition here makes the checker accept a rule that still has no entry in theory/proof-objects/proof-ste' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/proof-object-schema.yaml` (SHA-256 c7a27e3c4f8a23472b65614f4a2f8e490ab922a2fb244d8fbcae6620340695e0).
  - Current repository evidence at `theory/proof-objects/proof-object-schema.yaml:45`: 'description: Apply an established proposition.'.
  - The later-change audit compared `theory/proof-objects/proof-object-schema.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR123:PRRT_kwDOTH_vCM6PqmUy

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/foundation-final-consolidation-report.md:13`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/foundation-final-consolidation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR123:PRRT_kwDOTH_vCM6PqmUy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Don't clear wording mismatches while P-001 still diverges This blanket conclusion misses an existing canonical catalog/proof mismatch in the audited P-series scope: docs/C" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-final-consolidation-report.md` (SHA-256 beb28b9078185e1e73f8a7fec2d10ab204763300019242bd8e887d598bed7d21).
  - Current repository evidence at `docs/reports/foundation-final-consolidation-report.md:13`: 'This repair pass found no metadata mismatch, dependency graph mismatch, proof object mismatch, theorem/proof wording mismatch, internal link/documentation mismatch, or generated index mismatch. The only demonstrated inconsistency was missin'.
  - The later-change audit compared `docs/reports/foundation-final-consolidation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR124:PRRT_kwDOTH_vCM6Pq9Nm

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/foundation-final-consolidation-report.md:9`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/foundation-final-consolidation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR124:PRRT_kwDOTH_vCM6Pq9Nm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep status inconsistent until backfills avoid downstream use This status is not supported by the new backfill artifacts: the reports/raw appendices validate earlier artif' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-final-consolidation-report.md` (SHA-256 beb28b9078185e1e73f8a7fec2d10ab204763300019242bd8e887d598bed7d21).
  - Current repository evidence at `docs/reports/foundation-final-consolidation-report.md:9`: 'Final status: **FOUNDATION CONSISTENT**.'.
  - The later-change audit compared `docs/reports/foundation-final-consolidation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR126:PRRT_kwDOTH_vCM6Pr4ri

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/foundation-health-verification.md:72`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/foundation-health-verification.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR126:PRRT_kwDOTH_vCM6Pr4ri found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include the full warning scope In this commit, the recorded remaining-warning scope is narrower than the checks actually report: python tools/checkorphaneddocs.py emits or' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-health-verification.md` (SHA-256 040392476320e7487b1c5ef2e43d9d93bf0af78973387186a983cb6a6c2612ed).
  - Current repository evidence at `docs/reports/foundation-health-verification.md:72`: '- Duplicate-heading-anchor warnings from `python tools/check_markdown_hygiene.py` in existing foundation documents.'.
  - The later-change audit compared `docs/reports/foundation-health-verification.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR127:PRRT_kwDOTH_vCM6Pr_pZ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/foundation-consistency-audit.md:93`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/foundation-consistency-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR127:PRRT_kwDOTH_vCM6Pr_pZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Link the new audit before calling orphan warnings pre-existing When python tools/validatedocs.py runs after this commit, tools/checkorphaneddocs.py now reports WARN orphan' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-consistency-audit.md` (SHA-256 db58480f3b2a2001241a016290150ca26e380dde9fb4dee56dd9e5da97a27bf1).
  - Current repository evidence at `docs/reports/foundation-consistency-audit.md:93`: '- `tools/validate_docs.py` includes orphan-document warnings from the repository orphan-doc check, including many raw appendices and historical research files, then exits successfully.'.
  - The later-change audit compared `docs/reports/foundation-consistency-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR128:PRRT_kwDOTH_vCM6PsH-G

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/canonical-mathematics-audit.md:3`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/canonical-mathematics-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR128:PRRT_kwDOTH_vCM6PsH-G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include registered derived concepts in the audit When this report is used as the canonical mathematics inventory, the headline counts and inventory are incomplete: theory/' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/canonical-mathematics-audit.md` (SHA-256 779127a87542df3e6f24c652370b1aa538514648ee34dd8f19abe7fb669e1112).
  - Current repository evidence at `docs/reports/canonical-mathematics-audit.md:3`: 'This Phase 1 Step 4 audit classifies canonical mathematical artifacts without validating new mathematics. The audit found 129 accepted artifacts, 14 experimental artifacts, and 0 deprecated artifacts. Duplicate canonical identifiers found: '.
  - The later-change audit compared `docs/reports/canonical-mathematics-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR129:PRRT_kwDOTH_vCM6PsZxY

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/metadata/axioms.yaml:4`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/metadata/axioms.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR129:PRRT_kwDOTH_vCM6PsZxY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve AX-001 draft status in metadata When consumers use theory/metadata/axioms.yaml or the generated axiom index as the canonical registry, this marks AX-001 as Establ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/metadata/axioms.yaml` (SHA-256 ebdaaae3e17c6aeff717eb03c8ea194493d814a11adee326ce2db242936aca8e).
  - Current repository evidence at `theory/metadata/axioms.yaml:4`: 'status: Established'.
  - The later-change audit compared `theory/metadata/axioms.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR12:PRRT_kwDOTH_vCM6OD6bR

- Disposition: `fixed_on_current_main`
- Risk/subsystem: `high` / `research-records`
- Current location: `research/validation/investigations/VI-002-primitive-minimality.md:1303-1340`
- Blocks experiment reconstruction: `true`
- Root cause: `vi-002:unsupported-pass`
- Failure mechanism: The former PASS classification could be consumed despite missing reconstruction and VI-001 re-execution evidence; the current manifest and validator now prohibit that state.
- Remediation boundary: Complete: the investigation, execution manifest, status surfaces, validator, and focused fail-closed tests now agree that VI-002 is non-passing.
- Evidence:
  - Commit 1f3b086a88c541bfdb56ea2a26762129101e9008 replaces the unsupported pass claim with an explicit INCOMPLETE — NON-PASSING execution audit.
  - research/validation/executions/VI-002.execution.yaml records only 3 of 7 required steps complete and tools/check_investigation_execution.py validates the fail-closed manifest.
  - tests/test_investigation_execution_gates.py exercises incomplete evidence, dependency, step identity, and status propagation failures.

### PR12:PRRT_kwDOTH_vCM6OD6bU

- Disposition: `fixed_on_current_main`
- Risk/subsystem: `medium` / `research-records`
- Current location: `research/validation/investigations/VI-002-primitive-minimality.md:1226-1236`
- Blocks experiment reconstruction: `false`
- Root cause: `vi-002:divergent-result-surfaces`
- Failure mechanism: The stale interim Property row contradicted the final investigation summary; the interim table is no longer a live result surface and the current audited table is synchronized.
- Remediation boundary: Complete: retain the supersession marker, synchronized final summary, and execution-manifest validator.
- Evidence:
  - Commit 1f3b086a88c541bfdb56ea2a26762129101e9008 labels the earlier partial table superseded and retains one audited seven-primitive summary.
  - research/validation/investigations/VI-002-primitive-minimality.md:1230 records Property as Independent (Provisional), consistent with the audited final summary.
  - research/validation/executions/VI-002.execution.yaml is the machine-readable status authority validated by tools/check_investigation_execution.py.

### PR12:PRRT_kwDOTH_vCM6OD6bV

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `research-records`
- Current location: `research/proofs/conjectures.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `research-records:research/proofs/conjectures.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR12:PRRT_kwDOTH_vCM6OD6bV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep conjectures in one canonical registry This declares a Project-wide canonical conjecture registry even though theory/theorems/conjectures.md already records Project FA' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `research/proofs/conjectures.md` (SHA-256 887981ebb396285b379649010d224cf21c819d1b740d0b8bc3f40d353c00af57).
  - Current repository evidence at `research/proofs/conjectures.md:5`: 'This document serves as the canonical registry of conjectures within Project FAR.'.
  - The later-change audit compared `research/proofs/conjectures.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR12:PRRT_kwDOTH_vCM6OD6bY

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `research-records`
- Current location: `research/README.md`
- Blocks experiment reconstruction: `false`
- Root cause: `research-records:research/README.md`
- Failure mechanism: The reviewer concern still reproduces on the audited commit: the research index is absent, but current repository documents still link to or rely on it. The finding is therefore a confirmed defect and must remain in the remediation queue until the index is restored or all dependent references are updated.
- Remediation boundary: Correct 'P2 Badge Restore the research index or update its users Deleting this index leaves existing repository navigation and audit evidence stale: README.md:31 and docs/README.md:24 still' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 does not contain `research/README.md`, while `docs/README.md:29` still links to that missing research index.
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/SEMANTIC_AUDIT.md:111`, which relies on the missing research index as evidence.
  - The later-change audit compared `research/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR131:PRRT_kwDOTH_vCM6PuJ6w

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/dependency-audit.md:130`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/dependency-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR131:PRRT_kwDOTH_vCM6PuJ6w found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not make deferred theorems validation blockers These steps make T-013–T-015 prerequisites for Phase 1 Step 7, but I checked the existing Phase 1 canonicalization resolu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/dependency-audit.md` (SHA-256 6610c19f446b492bf41cf012bd98fd697f51ff3e17d04b5b7a3882d9426d77fd).
  - Current repository evidence at `docs/reports/dependency-audit.md:130`: '4. Validate T-015.'.
  - The later-change audit compared `docs/reports/dependency-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR132:PRRT_kwDOTH_vCM6PubMj

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/l008-validation-report.md:11`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/l008-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR132:PRRT_kwDOTH_vCM6PubMj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Exclude L-008-dependent T-005 from the foundation set When this report is used as validation evidence for L-008, the stated supplied foundation includes T-001 through T-01' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/l008-validation-report.md` (SHA-256 ad66f9b1f4e2d61d4bf18c6eaca8064334e829b3a4064e56117d05f2445a2195).
  - Current repository evidence at `docs/reports/l008-validation-report.md:11`: 'This validation treats the supplied accepted foundation as accepted: AX-001; accepted canonical definitions; L-001 through L-007; P-001 through P-008; T-001 through T-012; Isolation Classification doctrine; Foundation Consistency Audit; Can'.
  - The later-change audit compared `docs/reports/l008-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR133:PRRT_kwDOTH_vCM6PueMQ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/dependencies/dependency-graph.md:155`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/dependencies/dependency-graph.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR133:PRRT_kwDOTH_vCM6PueMQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update the current circularity audit for T-013 Removing T-005 here makes the current dependency sources disagree: theory/audits/circularity-audit-001.md still lists T-013 ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/dependencies/dependency-graph.md` (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at `theory/dependencies/dependency-graph.md:155`: 'Depends on: D-CALC.'.
  - The later-change audit compared `theory/dependencies/dependency-graph.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR134:PRRT_kwDOTH_vCM6Pujux

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/dependencies/dependency-graph.md:159`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/dependencies/dependency-graph.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR134:PRRT_kwDOTH_vCM6Pujux found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Synchronize T-014's circularity audit entry With this dependency graph now declaring T-014 depends only on D-CALC, the current circularity audit still reports Dependencies" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/dependencies/dependency-graph.md` (SHA-256 64060a228b4aa8b7a70e8f94cdcbb3edb9e8a7650fd06941a6c7a176f8526d71).
  - Current repository evidence at `theory/dependencies/dependency-graph.md:159`: 'Depends on: D-CALC.'.
  - The later-change audit compared `theory/dependencies/dependency-graph.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR136:PRRT_kwDOTH_vCM6Pus-I

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-014.proof.yaml:5`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-014.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR136:PRRT_kwDOTH_vCM6Pus-I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use a schema-declared proof-object status The proof-object schema defines status as an enum with values [draft, proposed, verified, established, deprecated] (theory/proof-' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-014.proof.yaml` (SHA-256 7def7aa06fda8cd7fe25e64870076d40aae65c37b6ec41236cd5e0dac279b1db).
  - Current repository evidence at `theory/proof-objects/T-014.proof.yaml:5`: 'status: accepted'.
  - The later-change audit compared `theory/proof-objects/T-014.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR136:PRRT_kwDOTH_vCM6Pus-M

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/dependency-audit-rerun.md:132`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/dependency-audit-rerun.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR136:PRRT_kwDOTH_vCM6Pus-M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Correct the proof-object status audit This audit conclusion is contradicted by the repository: theory/proof-objects/T-001.proof.yaml through T-012.proof.yaml still have st' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/dependency-audit-rerun.md` (SHA-256 c66331f2d7e4f012787f77a60060a40ae4e330d7aa8c9aab98977ec9ed0b372c).
  - Current repository evidence at `docs/reports/dependency-audit-rerun.md:132`: "Proof objects for T-001 through T-013 were already synchronized with accepted status. T-014 and T-015 proof objects still carried `status: draft` even though theorem metadata lists them as established and this rerun's accepted foundation in".
  - The later-change audit compared `docs/reports/dependency-audit-rerun.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR137:PRRT_kwDOTH_vCM6Pu8t3

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/theorem-coverage-audit.md:3`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/theorem-coverage-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR137:PRRT_kwDOTH_vCM6Pu8t3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reconcile the canonical inventory with accepted audit This summary says the audit enumerates all canonical mathematical artifacts, but the accepted foundation includes the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/theorem-coverage-audit.md` (SHA-256 294c1e7bdff685529e48f76557aa856f9c23c1291f5abbeca205c91acf663854).
  - Current repository evidence at `docs/reports/theorem-coverage-audit.md:3`: '- Total canonical mathematical artifacts enumerated: 128: 1 primitive record, 89 definitions, 6 axiom records, 8 lemmas, 9 propositions, and 15 theorems.'.
  - The later-change audit compared `docs/reports/theorem-coverage-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR137:PRRT_kwDOTH_vCM6Pu8t7

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/theorem-coverage-audit.md:203`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/theorem-coverage-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR137:PRRT_kwDOTH_vCM6Pu8t7 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Correct the dependency-registry coverage claims These PASS rows treat theory/dependencies/dependency-registry.yaml as covering every L/P/T artifact, but that registry is e' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/theorem-coverage-audit.md` (SHA-256 294c1e7bdff685529e48f76557aa856f9c23c1291f5abbeca205c91acf663854).
  - Current repository evidence at `docs/reports/theorem-coverage-audit.md:203`: '| Theorem dependency metadata | PASS: T-001 through T-015 are recorded in `theory/metadata/theorems.yaml`, `theory/dependencies/dependency-registry.yaml`, and `theory/dependencies/dependency-graph.md`. |'.
  - The later-change audit compared `docs/reports/theorem-coverage-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR138:PRRT_kwDOTH_vCM6Pu_IE

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-001.proof.yaml:5`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-001.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR138:PRRT_kwDOTH_vCM6Pu_IE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use a schema-valid proof-object status For T-001 through T-012 this change writes status: accepted, but theory/proof-objects/proof-object-schema.yaml defines the allowed p' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-001.proof.yaml` (SHA-256 c592af3b04c3af82dad53d23a354e3c9bc414296f7d2756316a2783a7bb518eb).
  - Current repository evidence at `theory/proof-objects/T-001.proof.yaml:5`: 'status: accepted'.
  - The later-change audit compared `theory/proof-objects/T-001.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR139:PRRT_kwDOTH_vCM6PvDtm

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/minimality-audit.md:3`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/minimality-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR139:PRRT_kwDOTH_vCM6PvDtm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Include A1–A5 in the minimality inventory This inventory says the audit covers the accepted foundation, but it omits the five established axiom records A1–A5: both theory/' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/minimality-audit.md` (SHA-256 724acfe3791c7ea25ac49b02b9853777320996eeedd8ab3a3f224aaa9305e258).
  - Current repository evidence at `docs/reports/minimality-audit.md:3`: 'This Phase 1 Step 9 Minimality Audit is audit-only. It consumes the accepted foundation and prior audits without revalidating theorem proofs or introducing new mathematics. The audit covers 126 accepted artifacts: 5 primitives, 89 canonical'.
  - The later-change audit compared `docs/reports/minimality-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR148:PRRT_kwDOTH_vCM6Pw5hJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/external-validation/philosophy/campaign-method.md:1`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/external-validation/philosophy/campaign-method.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR148:PRRT_kwDOTH_vCM6Pw5hJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add Charter status to the new campaign artifacts The root AGENTS.md requires compliance with docs/governance/research-execution-charter.md, whose Repository Rules require ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/external-validation/philosophy/campaign-method.md` (SHA-256 5ab002f1821bf39ca628f8a3b9563746c64e11f58c58312b5dcac63d3ecce07f).
  - Current repository evidence at `docs/reports/external-validation/philosophy/campaign-method.md:1`: '# Philosophy External Validation Campaign Method'.
  - The later-change audit compared `docs/reports/external-validation/philosophy/campaign-method.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR14:PRRT_kwDOTH_vCM6OE6cl

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `research-records`
- Current location: `research/proofs/theorem-catalog.md:46`
- Blocks experiment reconstruction: `false`
- Root cause: `research-records:research/proofs/theorem-catalog.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR14:PRRT_kwDOTH_vCM6OE6cl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Create proof files before cataloging them This catalog now records L-001 (and the following L/P/T entries) as draft proof artifacts with canonical file paths, but I checke' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `research/proofs/theorem-catalog.md` (SHA-256 337fadf3f38589aacf01570bbf6a8824d03ad6286f7ce02426304d571d7b0b42).
  - Current repository evidence at `research/proofs/theorem-catalog.md:46`: '| L-001 | Representation/Object Distinction | Draft | Object; Representation; Interpretation | `lemmas/L-001-representation-object-distinction.md` |'.
  - The later-change audit compared `research/proofs/theorem-catalog.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR150:PRRT_kwDOTH_vCM6PxKNR

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/external-validation/ai-reasoning/campaign-summary.md:17`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/external-validation/ai-reasoning/campaign-summary.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR150:PRRT_kwDOTH_vCM6PxKNR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Record falsification evidence before passing the campaign When this summary is used as the Phase 2 validation record, the claim that the campaign falsified representabilit' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/external-validation/ai-reasoning/campaign-summary.md` (SHA-256 55f9a4057636a09f3f4856421e670ab5da49fab5f232bc23f242f44f19e1aef6).
  - Current repository evidence at `docs/reports/external-validation/ai-reasoning/campaign-summary.md:17`: 'The campaign attempted to falsify representability by testing hidden neural computation, incomplete graph knowledge, theorem-prover search explosion, proof/formalization mismatch, and agentic error propagation. These did not force Foundatio'.
  - The later-change audit compared `docs/reports/external-validation/ai-reasoning/campaign-summary.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR151:PRRT_kwDOTH_vCM6PxMgL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `mechanization`
- Current location: `mechanization/far_mechanization/ir.py:250`
- Blocks experiment reconstruction: `false`
- Root cause: `mechanization:mechanization/far_mechanization/ir.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR151:PRRT_kwDOTH_vCM6PxMgL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include the investigation in duplicate-ID checks When an IR collection item reuses the investigation.identifier, FARDocument.validate() returns no DUPLICATELOCALIDENTIFIER' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/far_mechanization/ir.py` (SHA-256 bf54a8e7b96de3c32e46a594e6221af9e44bfd7f80963772dfedaa88f5d64104).
  - Current repository evidence at `mechanization/far_mechanization/ir.py:250`: 'diagnostics.extend(self.graph.validate())'.
  - The later-change audit compared `mechanization/far_mechanization/ir.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR151:PRRT_kwDOTH_vCM6PxMgM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `mechanization`
- Current location: `mechanization/far_mechanization/ir.py:178`
- Blocks experiment reconstruction: `false`
- Root cause: `mechanization:mechanization/far_mechanization/ir.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR151:PRRT_kwDOTH_vCM6PxMgM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate enum fields at runtime When graph nodes are constructed from untyped parsed data, GraphNode(Identifier("N"), "bogus").validate() reports success because this vali' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/far_mechanization/ir.py` (SHA-256 bf54a8e7b96de3c32e46a594e6221af9e44bfd7f80963772dfedaa88f5d64104).
  - Current repository evidence at `mechanization/far_mechanization/ir.py:178`: 'diagnostics.extend(self.source.validate())'.
  - The later-change audit compared `mechanization/far_mechanization/ir.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR154:PRRT_kwDOTH_vCM6QJoVS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/governance/repository-certification-standard.md:4`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/governance/repository-certification-standard.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR154:PRRT_kwDOTH_vCM6QJoVS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use a Charter-recognized artifact status Under the root AGENTS.md, new work must comply with docs/governance/research-execution-charter.md, whose Repository Rules require ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/governance/repository-certification-standard.md` (SHA-256 4141c4ead85e8a4bb10bfc37bbc3ab926775ae9979651fda9d6dedf96e3ac652).
  - Current repository evidence at `docs/governance/repository-certification-standard.md:4`: 'Status: Frozen Canonical Governance Standard'.
  - The later-change audit compared `docs/governance/repository-certification-standard.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR154:PRRT_kwDOTH_vCM6QKFHI

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/repository-certification-inventory-audit.md:34`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/repository-certification-inventory-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR154:PRRT_kwDOTH_vCM6QKFHI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Refresh the inventory against the final tree In the reviewed tree there are 1000 tracked paths (git ls-tree -r --name-only cdc9897... | wc -l), and this inventory also omi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/repository-certification-inventory-audit.md` (SHA-256 6ad4783e8e996d8cf54d0715000bb606a2fc67b40f5820fdbefd3fa771d6901c).
  - Current repository evidence at `docs/audits/repository-certification-inventory-audit.md:34`: '| Total tracked artifacts | 989 |'.
  - The later-change audit compared `docs/audits/repository-certification-inventory-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR155:PRRT_kwDOTH_vCM6QMr9J

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `repository-metadata`
- Current location: `README.md:99`
- Blocks experiment reconstruction: `false`
- Root cause: `repository-metadata:README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR155:PRRT_kwDOTH_vCM6QMr9J found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restore generated TASK-004 metadata In this generated dashboard block, tools/updatereadmedashboard.py::parsetasks takes the branch and title from docs/planning/next-action' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `README.md` (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at `README.md:99`: '## Certification and Architecture Navigation'.
  - The later-change audit compared `README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR156:PRRT_kwDOTH_vCM6QMZtL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-validation-methodology.md:43`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-validation-methodology.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR156:PRRT_kwDOTH_vCM6QMZtL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Scope the new requirements before applying them globally Because this says every external-system investigation must now record the new fields, the 20 already-registered in' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-validation-methodology.md` (SHA-256 54f2f30fe0c9ed6c7c68ff5dea10000e32f7ac75378c4edfdb4d2236c19258cb).
  - Current repository evidence at `theory/evaluation/external-validation-methodology.md:43`: '- the reasoning process is inaccessible or purely opaque;'.
  - The later-change audit compared `theory/evaluation/external-validation-methodology.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR157:PRRT_kwDOTH_vCM6QMn8d

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-system-investigations/legal-reasoning.md:111`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-system-investigations/legal-reasoning.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR157:PRRT_kwDOTH_vCM6QMn8d found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reclassify legal reasoning when preservation is unknown Here the report classifies legal reasoning as conservative extension, but its own preservation review leaves semant' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-system-investigations/legal-reasoning.md` (SHA-256 9c4231e8a3ea073a8020ccb6c872f04ed8bc0879cd0fdd1dfb3e717c7125b364).
  - Current repository evidence at `theory/evaluation/external-system-investigations/legal-reasoning.md:111`: '`conservative extension`'.
  - The later-change audit compared `theory/evaluation/external-system-investigations/legal-reasoning.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR157:PRRT_kwDOTH_vCM6QMn8f

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md:23`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR157:PRRT_kwDOTH_vCM6QMn8f found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Recompute synthesis over all nine investigations The scope lists nine investigations, including the five adversarial reports, but this aggregate still says All four and su' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md` (SHA-256 9ebb5a68dd908d74d6a8251e8cb6d4a6455e6223d32490ac956916a9ede43838).
  - Current repository evidence at `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md:23`: 'All nine scoped EV-021 through EV-029 investigations required Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus for their target mappings. FARA operational components were used when procedure,'.
  - The later-change audit compared `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR158:PRRT_kwDOTH_vCM6QQUuU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md:27`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-system-investigations/current-evidence-assessment-001.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR158:PRRT_kwDOTH_vCM6QQUuU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Reclassify EV-028 before aggregating counts When this table counts EV-021 through EV-029 as 3 conservative extension and 4 unresolved, it preserves EV-028's conservative l" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md` (SHA-256 fb686f15f9b48318d224e41c4a34ab4252748e00f12cb8a183930ea73f020376).
  - Current repository evidence at `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md:27`: '| EV-021 through EV-029 | 9 | 2 `fits FAR`; 3 `conservative extension`; 4 `unresolved`; 0 `candidate primitive failure` | Stronger within stated scopes because the reports explicitly separate preservation dimensions, limitations, and univer'.
  - The later-change audit compared `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR159:PRRT_kwDOTH_vCM6QQ_JH

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/protocol-v1.0.md:3`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/protocol-v1.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Record provenance before accepting CRP In this new protocol, the artifact is promoted to Accepted, but the file does not record the charter-required Question → Execution →' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/protocol-v1.0.md` (SHA-256 1d0411df41d41d4a85792f12b32d5a924ffb9c6911a96123a628bcd096c6cd17).
  - Current repository evidence at `theory/evaluation/comparative-representation/protocol-v1.0.md:3`: 'Status: Accepted methodology for comparative representation evaluation'.
  - The later-change audit compared `theory/evaluation/comparative-representation/protocol-v1.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR159:PRRT_kwDOTH_vCM6QQ_JJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiment-registry.json:12`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiment-registry.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register only immutable experiment artifacts The registry pins a concrete scenario/vocabulary/instruction version for CRE-001, but the CRE-001 directory currently contains' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiment-registry.json` (SHA-256 7ee62a82595c68c5d9afd1257bbb8ecc42515d4555191878151be997b00d4bcb).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiment-registry.json:12`: '"instruction_version": "CRE-001-INSTRUCTIONS-1.0",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiment-registry.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR159:PRRT_kwDOTH_vCM6QQ_JM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json:1`
- Blocks experiment reconstruction: `false`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR159:PRRT_kwDOTH_vCM6QQ_JM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Inline the provenance schema reference When an evaluator submission includes its required provenance object, validation through the repository's bundled JSON Schema implem" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json` (SHA-256 ffe7d9da8ad47b2c1d742909f52b3f5fdabf912c2364d722d05ff287cce014db).
  - Current repository evidence at `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json:1`: '{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"CRP v1.0 Evaluator Mapping Submission","type":"object","required":["protocol_version","experiment","evaluator","assignment","date","vocabulary_label","mapping","derived_cons'.
  - The later-change audit compared `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR15:PRRT_kwDOTH_vCM6OOImd

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARE/definitions/graph-definitions.md:86`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/definitions/graph-definitions.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR15:PRRT_kwDOTH_vCM6OOImd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Define the path used for weak connectivity When weak connectivity is used by the new dependency-component proof, this definition still relies on a bare path after directio' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/definitions/graph-definitions.md` (SHA-256 1603803468d08638840962da067cc84d7586c87df20d11dbd8758b4e15d52f9c).
  - Current repository evidence at `frameworks/FARE/definitions/graph-definitions.md:86`: '# Definition 9 — Subgraph'.
  - The later-change audit compared `frameworks/FARE/definitions/graph-definitions.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR15:PRRT_kwDOTH_vCM6OOImg

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARE/proofs/FARE-P012-dependency-components.md:23`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/proofs/FARE-P012-dependency-components.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR15:PRRT_kwDOTH_vCM6OOImg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restrict the objective to nodes in the dependency subgraph For an assessment graph containing an assessment with no dependency edge, or only non-dependency edges, Definiti' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/proofs/FARE-P012-dependency-components.md` (SHA-256 9daf71ff7235bfd0c7832d219b8d21858fe21273c00ce093c25283699c41c298).
  - Current repository evidence at `frameworks/FARE/proofs/FARE-P012-dependency-components.md:23`: 'Demonstrate that every assessment node in a dependency subgraph belongs to exactly one weak dependency component of that dependency subgraph.'.
  - The later-change audit compared `frameworks/FARE/proofs/FARE-P012-dependency-components.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR160:PRRT_kwDOTH_vCM6QR-_T

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/validate_cre001_submission.py:121`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/validate_cre001_submission.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Match provenance checks to the submitted template For real CRE-001 bundles, the provenance object is supposed to be the completed provenance/provenance-record.template.jso' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/validate_cre001_submission.py` (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at `tools/validate_cre001_submission.py:121`: 'require(provenance, "created_at", "provenance")'.
  - The later-change audit compared `tools/validate_cre001_submission.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR160:PRRT_kwDOTH_vCM6QR-_V

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/validate_cre001_submission.py:25`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/validate_cre001_submission.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Allow assigned vocabulary labels through leakage check Because the validator scans every string in the entire bundle, listing Vocabulary A, Vocabulary B, and Vocabulary C ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/validate_cre001_submission.py` (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at `tools/validate_cre001_submission.py:25`: '"Vocabulary C",'.
  - The later-change audit compared `tools/validate_cre001_submission.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR160:PRRT_kwDOTH_vCM6QR-_Y

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/validate_cre001_submission.py:135`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/validate_cre001_submission.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR160:PRRT_kwDOTH_vCM6QR-_Y found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Check mapping provenance against the bundle record This only verifies the CIR provenance identifier, so a bundle where mappingsubmission.provenance points at a different o' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/validate_cre001_submission.py` (SHA-256 959e85b7ac14094dfbf7e48a518e5f6c5c6cb7f1ffded2770b6fd6a6c8e597d4).
  - Current repository evidence at `tools/validate_cre001_submission.py:135`: 'raise ValidationError("cir: provenance mismatch")'.
  - The later-change audit compared `tools/validate_cre001_submission.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR161:PRRT_kwDOTH_vCM6RQoEE

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/repo_health_check.py:11`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/repo_health_check.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR161:PRRT_kwDOTH_vCM6RQoEE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Run the documented pytest mechanization suite When repohealthcheck.py --fast or --full runs in this repository, this unittest discover command exercises only the 51 unitte' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/repo_health_check.py` (SHA-256 2e93d1abcbc1c8a467308efb98368be4c9559b4d5a818f53968854152f0be0a5).
  - Current repository evidence at `tools/repo_health_check.py:11`: 'def main()->int:'.
  - The later-change audit compared `tools/repo_health_check.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR161:PRRT_kwDOTH_vCM6RQoEG

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_status_consistency.py:45`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_status_consistency.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR161:PRRT_kwDOTH_vCM6RQoEG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve negative status before matching supported For any parsed source whose status is Not supported, this loop matches the substring supported first and normalizes the ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_status_consistency.py` (SHA-256 cc238d6cc8f1dc73e77cedbc3ebe7a2e836896846c0989fc1a4f051e3718eea8).
  - Current repository evidence at `tools/check_status_consistency.py:45`: 'return status'.
  - The later-change audit compared `tools/check_status_consistency.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR164:PRRT_kwDOTH_vCM6RRYKW

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/metadata/theorems.yaml:4`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/metadata/theorems.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR164:PRRT_kwDOTH_vCM6RRYKW found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use a verifier-supported theorem status In the reviewed tree, tools/verifytheory.py accepts only Draft, Proposed, Verified, Established, or Deprecated for theorem metadata' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/metadata/theorems.yaml` (SHA-256 f44985b32233297816c4daa2b5e4ef879cabe1124b93d02dcd8a912261b5d245).
  - Current repository evidence at `theory/metadata/theorems.yaml:4`: 'status: Established (Conditional)'.
  - The later-change audit compared `theory/metadata/theorems.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR164:PRRT_kwDOTH_vCM6RRYKa

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_status_consistency.py:177`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_status_consistency.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR164:PRRT_kwDOTH_vCM6RRYKa found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update tests for scoped fallback matching This new scope gate changes the checker so conditional theorem titles no longer fallback-match the broad investigation titles, bu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_status_consistency.py` (SHA-256 cc238d6cc8f1dc73e77cedbc3ebe7a2e836896846c0989fc1a4f051e3718eea8).
  - Current repository evidence at `tools/check_status_consistency.py:177`: 'if score >= SIMILARITY_THRESHOLD and scope_compatible_for_fallback(a, b):'.
  - The later-change audit compared `tools/check_status_consistency.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR165:PRRT_kwDOTH_vCM6RRgpO

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md:27`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR165:PRRT_kwDOTH_vCM6RRgpO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record pilot exposure in CRE-001 status When this pilot artifact is kept under CRE-001, this line records that calibration and experimental materials were exposed to an ev' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md` (SHA-256 1160ddca740e70d001a8361450f6d76389bdcc14653ed6c06323422a863ebdc8).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md:27`: '- Calibration and experimental materials were exposed in one prompt.'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR165:PRRT_kwDOTH_vCM6RRgpS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json:2`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR165:PRRT_kwDOTH_vCM6RRgpS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Add required provenance to pilot metadata For this new CRE-001 artifact, the metadata omits several immutable provenance identifiers required by CRP v1.0's Provenance rule" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json` (SHA-256 d79ab5d9e6bd2119e050b472446a1dd5c8820b4dd53a9d6277d9da56828198c9).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json:2`: '"artifact_id": "CRE-001-E01-CLAUDE-SONNET-MEDIUM-PILOT-V1-REVIEW-METADATA",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR168:PRRT_kwDOTH_vCM6RSwBn

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/cre001_compile_vocabularies.py:62`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/cre001_compile_vocabularies.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR168:PRRT_kwDOTH_vCM6RSwBn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Verify against the registered reference artifact In the deterministic comparison path, the verifier uses modelfromscenario() as the reference instead of deterministic-veri' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre001_compile_vocabularies.py` (SHA-256 f29f0da5323f68eaaee65e11159af3fce922b17cbad1799d2622298dae058df5).
  - Current repository evidence at `tools/cre001_compile_vocabularies.py:62`: "if (e['output_path'],json.dumps(e['resulting_common_model_value'],sort_keys=True)) not in by: failures.append({'path':e['output_path'],'error':'entry absent from committed trace'})".
  - The later-change audit compared `tools/cre001_compile_vocabularies.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR169:PRRT_kwDOTH_vCM6RUGku

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/generate_next_tasks.py:21`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/generate_next_tasks.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR169:PRRT_kwDOTH_vCM6RUGku found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use distinct provenance for strategic tasks When the current gap report contains GAP-001 through GAP-005, these hard-coded tasks reuse both the same task IDs and the same ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/generate_next_tasks.py` (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at `tools/generate_next_tasks.py:21`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/generate_next_tasks.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR16:PRRT_kwDOTH_vCM6OPFvc

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARE/meta/README.md:9`
- Blocks experiment reconstruction: `true`
- Root cause: `frameworks:frameworks/FARE/meta/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR16:PRRT_kwDOTH_vCM6OPFvc found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Remove unbacked meta-theorem coverage claims With this commit the only files in frameworks/FARE/meta are M001 and M002, but this sentence says FARE meta-theorems establish' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/meta/README.md` (SHA-256 bbb669b560a617657744e3e889d3c0867ea5a481808b594a67074398552fdb80).
  - Current repository evidence at `frameworks/FARE/meta/README.md:9`: 'FARE meta-theorems establish properties of the framework, including dependency ordering, definition uniqueness, traceability, consistency, investigation soundness, and proof soundness.'.
  - The later-change audit compared `frameworks/FARE/meta/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR170:PRRT_kwDOTH_vCM6RUPh-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/generate_next_tasks.py:21`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/generate_next_tasks.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR170:PRRT_kwDOTH_vCM6RUPh- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use noncolliding source gaps for strategic tasks In this repo docs/reports/research-gap-report.md already defines GAP-001 through GAP-005 as unrelated PS-001/PS-003 mainte' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/generate_next_tasks.py` (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at `tools/generate_next_tasks.py:21`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/generate_next_tasks.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR170:PRRT_kwDOTH_vCM6RUPh8

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_cre001_semantics.py:54`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre001_semantics.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR170:PRRT_kwDOTH_vCM6RUPh8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Compare semantic docs against the frozen specification This loop only checks that each semantic doc contains the five status words; it never hashes the docs or compares th' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre001_semantics.py` (SHA-256 42c8c66386e2c0764fd901699f14306586d3371d2d84bd43dfa84b304fe5edd7).
  - Current repository evidence at `tools/check_cre001_semantics.py:54`: 'for prim in prims:'.
  - The later-change audit compared `tools/check_cre001_semantics.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR171:PRRT_kwDOTH_vCM6RUQL4

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/generate_next_tasks.py:21`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/generate_next_tasks.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use real source gaps for strategic tasks These hard-coded GAP-001 through GAP-005 values do not describe the new CRE-002 tasks: in the generated gap report they still poin' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/generate_next_tasks.py` (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at `tools/generate_next_tasks.py:21`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/generate_next_tasks.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR171:PRRT_kwDOTH_vCM6RUQL5

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/generate_next_tasks.py:21`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/generate_next_tasks.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep generated task identifiers unique Because taskfromgap() also derives IDs as TASK-, prepending strategic tasks named TASK-001 through TASK-005 makes the generated docs' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/generate_next_tasks.py` (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at `tools/generate_next_tasks.py:21`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/generate_next_tasks.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR171:PRRT_kwDOTH_vCM6RUQL6

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_cre001_semantics.py:44`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre001_semantics.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR171:PRRT_kwDOTH_vCM6RUQL6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Guard the FAR-proof non-claim in semantic checks NONCLAIMS includes FAR proof, but this condition explicitly exempts that claim, so tools/checkcre001semantics.py passes ev' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre001_semantics.py` (SHA-256 42c8c66386e2c0764fd901699f14306586d3371d2d84bd43dfa84b304fe5edd7).
  - Current repository evidence at `tools/check_cre001_semantics.py:44`: "chronology=spec.get('chronology',{})".
  - The later-change audit compared `tools/check_cre001_semantics.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR172:PRRT_kwDOTH_vCM6RUxxM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/repository-health.yml:9`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/repository-health.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR172:PRRT_kwDOTH_vCM6RUxxM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Defer PR trigger until full health passes This new pullrequest trigger makes the workflow run the unchanged python tools/repohealthcheck.py --full step for every PR target' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/repository-health.yml` (SHA-256 a7efc79586d873fbdfd3b626610290f2098001b190688d672901aeee28a90a70).
  - Current repository evidence at `.github/workflows/repository-health.yml:9`: '- main'.
  - The later-change audit compared `.github/workflows/repository-health.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR172:PRRT_kwDOTH_vCM6RUxxO

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/update_readme_dashboard.py:60`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/update_readme_dashboard.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR172:PRRT_kwDOTH_vCM6RUxxO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Parse strategic tasks in the planner summary too Now that this parser promotes STRATEGIC- entries into the README top tasks, the canonical make dashboard workflow becomes ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/update_readme_dashboard.py` (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at `tools/update_readme_dashboard.py:60`: 'make plan'.
  - The later-change audit compared `tools/update_readme_dashboard.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR173:PRRT_kwDOTH_vCM6RU20P

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_cre002_preregistration.py:26`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre002_preregistration.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Restore the CRE-002 preregistration check With this value, the new test fails: python -m unittest tests.testcre002preregistration invokes tools/checkcre002preregistration.' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre002_preregistration.py` (SHA-256 1dca0309686c2ee316462f60958f09a4a3fe14d3817261deddda1a35bf9bd454).
  - Current repository evidence at `tools/check_cre002_preregistration.py:26`: 'return 1'.
  - The later-change audit compared `tools/check_cre002_preregistration.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR173:PRRT_kwDOTH_vCM6RU20S

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json:70`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20S found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Make the override path reachable before locking the scenario In this frozen scenario, Toverride requires provenance for manualoverride=true from the operator, but the init' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json` (SHA-256 f1b355ea5a68526adeb071defc34dcd2260950be2af144d431c51466efb99b0a).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json:70`: '"guard_expression": "provenance(manual_override=true,operator,high)",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR173:PRRT_kwDOTH_vCM6RU20U

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002/README.md:1`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR173:PRRT_kwDOTH_vCM6RU20U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register CRE-002 in the canonical experiment registry This commit introduces CRE-002 as a preregistered experiment package, but theory/evaluation/comparative-representatio' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002/README.md` (SHA-256 a8695bb976ca5a19072f809374054cfb1ff8ee9cc2cfe4e77955daa4c241ba02).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002/README.md:1`: '# CRE-002: Prospective Multi-Pressure Reasoning System'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR174:PRRT_kwDOTH_vCM6RVB21

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_cre002_lock.py:25`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre002_lock.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR174:PRRT_kwDOTH_vCM6RVB21 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Verify the manifest's recorded checksums When this gate builds actual, it uses package-manifest.json only as a path list and ignores each entry's recorded sha256 and bytec" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre002_lock.py` (SHA-256 08ecb63c76d5eb0e43698f03aaa13509487431f059f0bd355cbc91bd69152209).
  - Current repository evidence at `tools/check_cre002_lock.py:25`: '}'.
  - The later-change audit compared `tools/check_cre002_lock.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR174:PRRT_kwDOTH_vCM6RVB22

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_cre002_lock.py:16`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre002_lock.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR174:PRRT_kwDOTH_vCM6RVB22 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use a reachable checksum source commit In the reviewed commit, this hard-coded sourcecommit is not an ancestor of 2692d8cbd329ff68bb63f2e5dfb1e9c6bf73453b (git merge-base ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre002_lock.py` (SHA-256 08ecb63c76d5eb0e43698f03aaa13509487431f059f0bd355cbc91bd69152209).
  - Current repository evidence at `tools/check_cre002_lock.py:16`: 'EXECUTION_LOCK = PACKAGE / "execution-lock.json"'.
  - The later-change audit compared `tools/check_cre002_lock.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR175:PRRT_kwDOTH_vCM6RVFKq

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:38`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR175:PRRT_kwDOTH_vCM6RVFKq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Update preregistration validation for the unlock state In the unlocked state introduced here, the committed CI path still fails: tests/testcre002preregistration.py invokes' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` (SHA-256 b07a78551bb671776c1022ca51b55644a0ed12f5fa28905e16ff55ffcf61cc67).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:38`: '}'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR176:PRRT_kwDOTH_vCM6RVX-c

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:34`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR176:PRRT_kwDOTH_vCM6RVX-c found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Commit the declared CRE-002 result artifacts With this line set to true, a clean checkout is declared to contain official results, but this commit does not track theory/ev' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` (SHA-256 b07a78551bb671776c1022ca51b55644a0ed12f5fa28905e16ff55ffcf61cc67).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:34`: '"official_results_present": true,'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR176:PRRT_kwDOTH_vCM6RVX-h

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/cre002_execute.py:221`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/cre002_execute.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR176:PRRT_kwDOTH_vCM6RVX-h found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Emit the preregistered boundary reports CRE-002 preregistration requires each vocabulary to emit both a compiler-boundary report and a limitation/unsupported-element repor' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre002_execute.py` (SHA-256 a772507579200e564f24e3d7cb04e152e442ac1819f56e4f1a5acf2a5c36b6e1).
  - Current repository evidence at `tools/cre002_execute.py:221`: 'raise SystemExit(main())'.
  - The later-change audit compared `tools/cre002_execute.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR177:PRRT_kwDOTH_vCM6RVqC_

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_vocabulary_semantics_baseline_1_1.py:87`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_vocabulary_semantics_baseline_1_1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR177:PRRT_kwDOTH_vCM6RVqC_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restore byte-for-byte CRE-002 result validation When the original CRE-002 result changes outside the sampled fields, this checker still passes even though the new baseline' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_vocabulary_semantics_baseline_1_1.py` (SHA-256 f6a379ab8da564755aa7b010d5017415d75101873c7bf15d4388857b558dcde8).
  - Current repository evidence at `tools/check_vocabulary_semantics_baseline_1_1.py:87`: 'raise SystemExit(main())'.
  - The later-change audit compared `tools/check_vocabulary_semantics_baseline_1_1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR178:PRRT_kwDOTH_vCM6RV06v

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json:21`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR178:PRRT_kwDOTH_vCM6RV06v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the override path reachable With this scenario as frozen input, Toverride can never fire: the initial evidencelog is empty, and the only evidence-producing transition' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json` (SHA-256 3b65fdefc814195d68d6dbc773b8dd598a6029356a17f9a05582fa023faa6239).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json:21`: '{"id":"T_override","authorization":"R_override","guard_expression":"provenance(manual_override=true,operator,high)","updates":{"manual_override":true},"defeats_lower_priority_conflict_for_current_state":true,"append_history":true},'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR178:PRRT_kwDOTH_vCM6RV06x

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:8`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR178:PRRT_kwDOTH_vCM6RV06x found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require the Baseline 1.1 checksum lock before execution This unlock prerequisite now only requires Baseline 1.1 to be merged, but the Baseline 1.1 freeze boundary says it ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json` (SHA-256 2253d19c68da78800186089e9b320881c1a70552a02f4c295f05496a40abb6af).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:8`: '"semantic_authority": "VOCABULARY-SEMANTICS-BASELINE-1.1",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR17:PRRT_kwDOTH_vCM6OR8-C

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `frameworks`
- Current location: `frameworks/FARE/mathematics/definitions/evaluation-completion.md:45`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/mathematics/definitions/evaluation-completion.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR17:PRRT_kwDOTH_vCM6OR8-C found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require completions to add missing limits Because this obligation only covers sequences whose required limit is already represented by the proposed completion, a candidate' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/mathematics/definitions/evaluation-completion.md` (SHA-256 c16efcbcc604c0875e899a46da7f8d8a10ab9fe1562be133147f0044224fe903).
  - Current repository evidence at `frameworks/FARE/mathematics/definitions/evaluation-completion.md:45`: 'The criterion may be based on convergence, a Cauchy-like condition, refinement behavior, or another formally defined requirement.'.
  - The later-change audit compared `frameworks/FARE/mathematics/definitions/evaluation-completion.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR181:PRRT_kwDOTH_vCM6RWgcF

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:6`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR181:PRRT_kwDOTH_vCM6RWgcF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Update Baseline 1.1 gates before unlocking In this authorized state, setting these flags to true breaks the existing Baseline 1.1 health gates: tools/checkvocabularysemant' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json` (SHA-256 2253d19c68da78800186089e9b320881c1a70552a02f4c295f05496a40abb6af).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:6`: '"compiler_implementation_permitted": true,'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR182:PRRT_kwDOTH_vCM6RXNCP

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/cre002_ext001_model.py:155`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/cre002_ext001_model.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCP found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require every frozen output before passing candidates In this execution, requiredoutputspreserved is the gate used by build() before marking a candidate complete, but this' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre002_ext001_model.py` (SHA-256 6ee8e92055c71b1a2679f66a77fc3e5f64a27fded1e3259963254de9e667ba9c).
  - Current repository evidence at `tools/cre002_ext001_model.py:155`: '"required_outputs_preserved": all({"booleans", "evidence_log", "action_history", "active_rules", "nondeterministic_outcomes", "priority_defeat_occurred", "terminal_reason"}.issubset(s.data()) for s in terminals),'.
  - The later-change audit compared `tools/cre002_ext001_model.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR182:PRRT_kwDOTH_vCM6RXNCU

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/cre002_ext001_native.py:105`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/cre002_ext001_native.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Validate candidate records against derived-field requirements This audit checks whether the Baseline 1.1 construct definitions themselves have requiredfields and operation' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre002_ext001_native.py` (SHA-256 ada1b5cc161684d97c1426b9461a45822d7e4697d57bbb1cee31ee5d4590894e).
  - Current repository evidence at `tools/cre002_ext001_native.py:105`: 'status = "pass" if not (missing or malformed or primitive_mismatch) else "fail"'.
  - The later-change audit compared `tools/cre002_ext001_native.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR182:PRRT_kwDOTH_vCM6RXNCb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/cre002_ext001_execute.py:74`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/cre002_ext001_execute.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR182:PRRT_kwDOTH_vCM6RXNCb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Hash the official vocabulary source packages The preregistration makes the official Vocabulary A/B/C source definitions frozen inputs and each candidate is supposed to emi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre002_ext001_execute.py` (SHA-256 9ae28e0320901e1fcb68abfac166ed99aef66da6f3b957fb8c8623496e6cbf38).
  - Current repository evidence at `tools/cre002_ext001_execute.py:74`: 'source_checksums = {'.
  - The later-change audit compared `tools/cre002_ext001_execute.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR184:PRRT_kwDOTH_vCM6Rc-OK

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json:23`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR184:PRRT_kwDOTH_vCM6Rc-OK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require all clean counted submissions to pass When there are multiple eligible uncontaminated submissions and one completes while another fails, these rules can still clas' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json` (SHA-256 68472ec0c633eddf76f4d38807ae070a76e55aa5af0c23f98bbed2e2255b3437).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json:23`: '"overall_replication_success": "Every official vocabulary satisfies vocabulary_replication_success, at least two independent implementation teams contribute counted submissions, and the verifier independence audit passes.",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR185:PRRT_kwDOTH_vCM6RefEA

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_cre002_ext001_rep001_preregistration.py:40`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre002_ext001_rep001_preregistration.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR185:PRRT_kwDOTH_vCM6RefEA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require the checksum-locked phase After this commit promotes the package to checksumstate: locked, the preregistration checker still accepts pending. If a bad merge or lat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre002_ext001_rep001_preregistration.py` (SHA-256 6dc61420004ed64be76510276503bf647b101117792b621b801942fddcd5b5c1).
  - Current repository evidence at `tools/check_cre002_ext001_rep001_preregistration.py:40`: 'fail("an independent verifier team is required")'.
  - The later-change audit compared `tools/check_cre002_ext001_rep001_preregistration.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR186:PRRT_kwDOTH_vCM6Revz1

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_cre002_ext001_rep001_team_registry.py:35`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_cre002_ext001_rep001_team_registry.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR186:PRRT_kwDOTH_vCM6Revz1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject shared repositories in registry validation When eligible registrations have disjoint personnel but reuse the same repositoryidentity, this checker still appends the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_cre002_ext001_rep001_team_registry.py` (SHA-256 f4ba7a1740930f74f3e3d025eabc17fd2cd039915732a4106d220215c76bcb88).
  - Current repository evidence at `tools/check_cre002_ext001_rep001_team_registry.py:35`: 'personnel.update(members)'.
  - The later-change audit compared `tools/check_cre002_ext001_rep001_team_registry.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR188:PRRT_kwDOTH_vCM6Rfduh

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/cre002_ext001_robustness.py:60`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/cre002_ext001_robustness.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR188:PRRT_kwDOTH_vCM6Rfduh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve empty arrays in the third implementation When the frozen scenario contains empty arrays (initialstate.evidencelog and initialstate.actionhistory), json.loads(...,' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/cre002_ext001_robustness.py` (SHA-256 d151472585ec34162cd92cd4413ba02fda068ca9256f68105cdb869d2d610c1b).
  - Current repository evidence at `tools/cre002_ext001_robustness.py:60`: 'if __name__=="__main__": raise SystemExit(main())'.
  - The later-change audit compared `tools/cre002_ext001_robustness.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR188:PRRT_kwDOTH_vCM6Rfdum

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json:23`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR188:PRRT_kwDOTH_vCM6Rfdum found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep the superseded manifest state accepted by checks Changing the package checksum state to this new value leaves the existing preregistration gate out of sync: tools/che' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json` (SHA-256 aaa00f8fd67a7c0dcf8d574b249750d15b00b2341b3e00854cad0b0b843e2e8f).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json:23`: '"checksum_state": "locked",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR189:PRRT_kwDOTH_vCM6RgFpD

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/parse_far.py:48`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/parse_far.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject non-string scalars instead of coercing them In files that use non-string YAML scalars for string+ fields, such as id: 1 or kind: true, this coerces them to strings ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/parse_far.py` (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at `tools/parse_far.py:48`: 'return text'.
  - The later-change audit compared `tools/parse_far.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR189:PRRT_kwDOTH_vCM6RgFpI

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/parse_far.py:85`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/parse_far.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Validate unknown keys inside statement mappings When a representation uses a mapped statement, this delegates to Statement.fromvalue without checking the grammar's stateme" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/parse_far.py` (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at `tools/parse_far.py:85`: 'statement = Statement.from_value(item["statement"], f"representation {rep_id}") if "statement" in item else None'.
  - The later-change audit compared `tools/parse_far.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR189:PRRT_kwDOTH_vCM6RgFpM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/parse_far.py:22`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/parse_far.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR189:PRRT_kwDOTH_vCM6RgFpM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Remove lowercase aliases from primitive key allow-list With these lowercase keys allowed, a reasoningsystem.farprimitives block containing only investigation, representati' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/parse_far.py` (SHA-256 041b6a7d7b7bc741e7d39ac7ba463ca426fde26e583062a7a2554acb37be14cf).
  - Current repository evidence at `tools/parse_far.py:22`: 'PRIMITIVE_KEYS = {"Investigation", "Representation", "Representational Structure", "Interpretation", "Reasoning Calculus", "investigation", "representation", "structure", "interpretation", "calculus"}'.
  - The later-change audit compared `tools/parse_far.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR191:PRRT_kwDOTH_vCM6Rg6qO

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `mechanization`
- Current location: `mechanization/lean/FARCore.lean:28`
- Blocks experiment reconstruction: `true`
- Root cause: `mechanization:mechanization/lean/FARCore.lean`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR191:PRRT_kwDOTH_vCM6Rg6qO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Carry the required transition-signature fields When a scoped process has specified transition executions, this type treats a bare label as a complete transition signature.' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/lean/FARCore.lean` (SHA-256 7b004e58006ee9f5f767308f896284c4dfbaef2c37d1a56b06605e6dfc2978ab).
  - Current repository evidence at `mechanization/lean/FARCore.lean:28`: 'deriving Repr, DecidableEq'.
  - The later-change audit compared `mechanization/lean/FARCore.lean` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR191:PRRT_kwDOTH_vCM6Rg6qW

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `mechanization`
- Current location: `mechanization/lean/FARCore.lean:70`
- Blocks experiment reconstruction: `true`
- Root cause: `mechanization:mechanization/lean/FARCore.lean`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR191:PRRT_kwDOTH_vCM6Rg6qW found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Tie trace transitions to the governing calculus For a process whose specifiedTransitions includes a signature that premises.calculus R hScope rejects, the construction sti' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/lean/FARCore.lean` (SHA-256 7b004e58006ee9f5f767308f896284c4dfbaef2c37d1a56b06605e6dfc2978ab).
  - Current repository evidence at `mechanization/lean/FARCore.lean:70`: 'traceMatchesProcess : T.transitions = R.specifiedTransitions'.
  - The later-change audit compared `mechanization/lean/FARCore.lean` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR192:PRRT_kwDOTH_vCM6RipTt

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `test-infrastructure`
- Current location: `tests/test_t003_adequacy_audit.py:42`
- Blocks experiment reconstruction: `false`
- Root cause: `test-infrastructure:tests/test_t003_adequacy_audit.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR192:PRRT_kwDOTH_vCM6RipTt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Align the audit wording checked by the test Running python -m unittest tests.testt003adequacyaudit fails here because the audit document never contains this exact phrase: ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_t003_adequacy_audit.py` (SHA-256 f281bf9f79db14d1ed96dfacfffe884f58e95b3ab8489a04b8c66c48b5a1b689).
  - Current repository evidence at `tests/test_t003_adequacy_audit.py:42`: 'self.assertIn("three examples", text)'.
  - The later-change audit compared `tests/test_t003_adequacy_audit.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR192:PRRT_kwDOTH_vCM6RipTx

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `test-infrastructure`
- Current location: `tests/test_t003_adequacy_audit.py:49`
- Blocks experiment reconstruction: `false`
- Root cause: `test-infrastructure:tests/test_t003_adequacy_audit.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR192:PRRT_kwDOTH_vCM6RipTx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Restrict the axiom/admission scan to declarations This test currently scans the entire Lean source as raw text, so it fails on existing comments rather than new proof admi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_t003_adequacy_audit.py` (SHA-256 f281bf9f79db14d1ed96dfacfffe884f58e95b3ab8489a04b8c66c48b5a1b689).
  - Current repository evidence at `tests/test_t003_adequacy_audit.py:49`: 'with self.subTest(word=word):'.
  - The later-change audit compared `tests/test_t003_adequacy_audit.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR193:PRRT_kwDOTH_vCM6Rj0PR

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `ci-and-automation`
- Current location: `.github/workflows/specification-export.yml:23`
- Blocks experiment reconstruction: `false`
- Root cause: `ci-and-automation:.github/workflows/specification-export.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR193:PRRT_kwDOTH_vCM6Rj0PR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Install pytest before running the workflow tests In the added workflow, the only setup before this command is checkout, actions/setup-python, the exporter run, and git dif' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/specification-export.yml` (SHA-256 2aa19214981ed97c418a375063879cbe20494f215032f7afe5f7d5cd45968b0d).
  - Current repository evidence at `.github/workflows/specification-export.yml:23`: '- name: Regenerate Project FAR specification export'.
  - The later-change audit compared `.github/workflows/specification-export.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR193:PRRT_kwDOTH_vCM6Rj0PX

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/export_specification.py:118`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/export_specification.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR193:PRRT_kwDOTH_vCM6Rj0PX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Recompute VCS metadata instead of preserving it When the exporter runs over the committed export directory, existingvcsmetadata() returns the old manifest values and this ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/export_specification.py` (SHA-256 f1d9622b27169a9033e6ad2f45aa734b5a9578c62fce039d3bf8a0de3b0a623c).
  - Current repository evidence at `tools/export_specification.py:118`: 'return preserved'.
  - The later-change audit compared `tools/export_specification.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR197:PRRT_kwDOTH_vCM6RpiBK

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/independence/primitive-independence-evaluation.schema.json:95`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/independence/primitive-independence-evaluation.schema.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR197:PRRT_kwDOTH_vCM6RpiBK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Separate per-test records from aggregate decisions This schema validates only a single testtype, but locally-independent and tested-space-independent are aggregate outcome' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/independence/primitive-independence-evaluation.schema.json` (SHA-256 2c5923c90c1a8108a16d1e7799dd2d34b18285d765faafdc656493bfeb730c89).
  - Current repository evidence at `theory/independence/primitive-independence-evaluation.schema.json:95`: '},'.
  - The later-change audit compared `theory/independence/primitive-independence-evaluation.schema.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR197:PRRT_kwDOTH_vCM6RpiBO

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/README.md:15`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR197:PRRT_kwDOTH_vCM6RpiBO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register the new theory child domain Adding theory/independence/ here creates a new canonical theory area, but the frozen Repository Domain Registry remains the authoritat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/README.md` (SHA-256 0aad43903cd38647857f274d6add9559a24c510074baaa1f6a3c8e6b5bab5b9a).
  - Current repository evidence at `theory/README.md:15`: '- `independence/` — falsifiable primitive-independence criteria, schemas, and future execution artifacts.'.
  - The later-change audit compared `theory/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR198:PRRT_kwDOTH_vCM6R1HgZ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/independence/executions/PIE-001/attempts.csv:1`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/independence/executions/PIE-001/attempts.csv`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR198:PRRT_kwDOTH_vCM6R1HgZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record required preservation and complexity judgments For PIE-001 rows, the protocol requires each attempted reduction to record per-dimension preservation judgments and c' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/independence/executions/PIE-001/attempts.csv` (SHA-256 6b156d3ee3f7cb7f6d3c23a2ef2f8edeed955644c8135aa265cff94ad2f9c1b0).
  - Current repository evidence at `theory/independence/executions/PIE-001/attempts.csv:1`: 'execution_id,primitive,test_type,attempt_outcome,hidden_reintroduction,decision,reason'.
  - The later-change audit compared `theory/independence/executions/PIE-001/attempts.csv` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR199:PRRT_kwDOTH_vCM6R1VGh

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `test-infrastructure`
- Current location: `tests/test_alternative_vocabulary_competition.py:68`
- Blocks experiment reconstruction: `false`
- Root cause: `test-infrastructure:tests/test_alternative_vocabulary_competition.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR199:PRRT_kwDOTH_vCM6R1VGh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Fix the self-matching global-minimality assertion This assertion makes the newly added test suite fail because the report intentionally contains the negated sentence AVC-0' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_alternative_vocabulary_competition.py` (SHA-256 9aa6f8b7d9acf4b8b5d81b09b5525ecfadb2117bae6083307697e07ea2aaeb4e).
  - Current repository evidence at `tests/test_alternative_vocabulary_competition.py:68`: 'self.assertNotIn("Scientific conclusion: **FAR is globally minimal**", report)'.
  - The later-change audit compared `tests/test_alternative_vocabulary_competition.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR19:PRRT_kwDOTH_vCM6OSLhU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARE/mathematics/definitions/evaluation-distance.md:43`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/mathematics/definitions/evaluation-distance.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR19:PRRT_kwDOTH_vCM6OSLhU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Make cost models cover every path being measured This definition allows a transformation cost model to assign costs only to admissible transformations “under consideration' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/mathematics/definitions/evaluation-distance.md` (SHA-256 ec3dd0e3f0d51ccf2a76e5bd194073b83beb3afa3811572a1ad75c401c9f6493).
  - Current repository evidence at `frameworks/FARE/mathematics/definitions/evaluation-distance.md:43`: 'A **transformation cost model** assigns a non-negative cost to every admissible evaluation transformation under consideration.'.
  - The later-change audit compared `frameworks/FARE/mathematics/definitions/evaluation-distance.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR19:PRRT_kwDOTH_vCM6OSLhV

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md:44`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR19:PRRT_kwDOTH_vCM6OSLhV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Disambiguate N(E) for chosen neighborhood systems This introduces N(E) as the collection supplied by a particular neighborhood system, but the existing Neighborhood Family' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md` (SHA-256 701618c622e74ac6b85bce90fbd746400f0d7636f89a3f3cabb9349e80da8c77).
  - Current repository evidence at `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md:44`: 'A **neighborhood system** assigns to each evaluation `E` a collection `N(E)` of neighborhoods centered at `E`.'.
  - The later-change audit compared `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR200:PRRT_kwDOTH_vCM6R1kcF

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/independence/global-minimality/GMA-001/README.md:5`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/independence/global-minimality/GMA-001/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR200:PRRT_kwDOTH_vCM6R1kcF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use one charter-approved artifact status AGENTS.md directs all automated work to docs/governance/research-execution-charter.md, whose Repository Rules require every artifa' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/independence/global-minimality/GMA-001/README.md` (SHA-256 3e070958e4898c8ad375baca08d3563c6a10cdc75fc3d4c33cb9f6a49d6e03bb).
  - Current repository evidence at `theory/independence/global-minimality/GMA-001/README.md:5`: 'Completed evidence synthesis. Scientific conclusion: **global minimality unresolved**.'.
  - The later-change audit compared `theory/independence/global-minimality/GMA-001/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR200:PRRT_kwDOTH_vCM6R1kcJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/independence/global-minimality/GMA-001/README.md:45`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/independence/global-minimality/GMA-001/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR200:PRRT_kwDOTH_vCM6R1kcJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not label unresolved counts as demonstrated I checked the referenced AVC-001 results: only the FAR control is all-Pass, while every three-primitive candidate is either ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/independence/global-minimality/GMA-001/README.md` (SHA-256 3e070958e4898c8ad375baca08d3563c6a10cdc75fc3d4c33cb9f6a49d6e03bb).
  - Current repository evidence at `theory/independence/global-minimality/GMA-001/README.md:45`: '> The minimum demonstrated sufficient primitive count is at most five and may be as low as three within the tested families.'.
  - The later-change audit compared `theory/independence/global-minimality/GMA-001/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR201:PRRT_kwDOTH_vCM6R1r2E

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/scope/ISD-001/scope-registry.json:5`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/scope/ISD-001/scope-registry.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR201:PRRT_kwDOTH_vCM6R1r2E found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve frozen-benchmark gate in the registry rule If future scope-expansion tooling or reviewers use this machine-readable inclusionrule, a class can be marked demonstra' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/scope/ISD-001/scope-registry.json` (SHA-256 72f851af52ed016c75f382f3dcf08a352d20df3d337450b6691a203874c9dbec).
  - Current repository evidence at `theory/scope/ISD-001/scope-registry.json:5`: '"inclusion_rule": "A class is in current demonstrated scope only when at least one explicit instance has a preserved mapping or deterministic execution artifact covering structural, semantic, operational, dependency, information, and histor'.
  - The later-change audit compared `theory/scope/ISD-001/scope-registry.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR201:PRRT_kwDOTH_vCM6R1r2G

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/scope/ISD-001/scope-registry.json:43`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/scope/ISD-001/scope-registry.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR201:PRRT_kwDOTH_vCM6R1r2G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include standalone universality in registry exclusions If downstream checks consume excludedfromcurrentclaims as the machine-readable claim boundary, this list still does ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/scope/ISD-001/scope-registry.json` (SHA-256 72f851af52ed016c75f382f3dcf08a352d20df3d337450b6691a203874c9dbec).
  - Current repository evidence at `theory/scope/ISD-001/scope-registry.json:43`: '"universal necessity, global minimality, or unique optimality"'.
  - The later-change audit compared `theory/scope/ISD-001/scope-registry.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR202:PRRT_kwDOTH_vCM6R1vYI

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:32`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Keep CRE-003-I's investigation fixed When CRE-003-I is used as the interpretation-only case, this changes the investigation objective from determining whether the alarm is" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:32`: '"investigation": "determine whether withdrawal is permitted",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR202:PRRT_kwDOTH_vCM6R1vYK

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:72`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not add new facts to the calculus case When CRE-003-C is evaluated as the reasoning-calculus-only variation, adding exceptionq to systemb also changes the represented m' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:72`: '"interpretation": {"p": "evidence accepted", "q": "claim supported", "exception_q": "registered defeating exception"},'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR202:PRRT_kwDOTH_vCM6R1vYM

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:96`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR202:PRRT_kwDOTH_vCM6R1vYM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the calculus constant in CRE-003-R When CRE-003-R is used to test representation/structure variation, changing the calculus from modusponens to supportedgepropagation' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` (SHA-256 7500aecfec0d81d2f3d6a2b5dc637a185e7ca0dedac9bb9026877c066ce2019c).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:96`: '"calculus": ["support_edge_propagation"]'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR203:PRRT_kwDOTH_vCM6R12qG

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `test-infrastructure`
- Current location: `tests/test_cre003_execution.py:66`
- Blocks experiment reconstruction: `true`
- Root cause: `test-infrastructure:tests/test_cre003_execution.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR203:PRRT_kwDOTH_vCM6R12qG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Fix the assertion string so the test suite passes When I ran python -m unittest tests.testcre003preregistration tests.testcre003execution, this assertion failed because ex' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_cre003_execution.py` (SHA-256 81c77ee23ea1d1a3595b84e9894c5d917ac1b37fb119e39a2f6669e45eea866d).
  - Current repository evidence at `tests/test_cre003_execution.py:66`: 'self.assertIn("remain unresolved rather than defeated", self.report)'.
  - The later-change audit compared `tests/test_cre003_execution.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR204:PRRT_kwDOTH_vCM6R2SrO

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py:72`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR204:PRRT_kwDOTH_vCM6R2SrO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require a registered carrier before passing When an evaluator selects only differencecarriers=["other"] and answers otherfunction="none", execution falls through to this p' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py` (SHA-256 874bf268cf03dd02744e476d0c34a98c14dfa46107fc0c56f79a3cbea5521f87).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py:72`: 'classification = "unknown"'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR204:PRRT_kwDOTH_vCM6R2SrT

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json:38`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR204:PRRT_kwDOTH_vCM6R2SrT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Make cannotdetermine exclusive in the schema For translated systems marked distinguishable, the schema currently accepts differencecarriers such as ["cannotdetermine", "as' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json` (SHA-256 9c75d5c5ffdb68103b5994ec4d307de44099fc56f7885828cd00635173d2ac50).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json:38`: '"defines_objective",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR205:PRRT_kwDOTH_vCM6R2llN

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md:8`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR205:PRRT_kwDOTH_vCM6R2llN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use the schema field in the decision tree For implementations following this frozen tree, translateddistinction is not a response field: response.schema.json, preregistrat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md` (SHA-256 8414e3f277208dd0fd36705cf71540350897a0e8f06546d011270979ee950a6f).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md:8`: '4. If `source_difference = yes` and `translated_difference = cannot_determine`, classify it as `unknown`.'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR205:PRRT_kwDOTH_vCM6R2llV

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md:25`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR205:PRRT_kwDOTH_vCM6R2llV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align hidden-reintroduction outcomes with scorer When other is selected with otherfunction = cannotdetermine, this frozen rule says to output hiddenreintroduction = unknow' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md` (SHA-256 1756f03bbbb70a96efebadb7b8fa0c8338827cc45dcad0c46288f0c51787eeb6).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md:25`: '- `cannot_determine`: `unknown`.'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR206:PRRT_kwDOTH_vCM6R22Dm

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json:10`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Dm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Fix the locked evaluator packet hash This lock entry does not match the checked-in evaluatorpacket.md: verifyprotocollock() computes git blob SHA-1 1ea5043ccb3a10aa0f35023' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json` (SHA-256 29021338ed94e411a25e5db02ce8c32de90d9646630923db4b45105ab8e6eae9).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json:10`: '"evaluator_packet.md": "1ea5043ccb3a10aa0f350237ec1b4b3ce558c7ff"'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR206:PRRT_kwDOTH_vCM6R22Dp

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:86`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Dp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate responses against the frozen schema This only checks labels and submittedat are non-empty strings, so a manifest and response using values such as caselabel: "CAS' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py` (SHA-256 00bb336e72569ed231258ca9b8aba71b2065567f5c9b180c9b27134a9bc0cba6).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:86`: 'def validate_response_shape(response: Mapping[str, Any]) -> None:'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR206:PRRT_kwDOTH_vCM6R22Ds

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:179`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR206:PRRT_kwDOTH_vCM6R22Ds found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Report the required per-evaluator and per-case aggregates The frozen automatic-scoring spec requires results at response, evaluator, case, candidate, and overall levels, b' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py` (SHA-256 00bb336e72569ed231258ca9b8aba71b2065567f5c9b180c9b27134a9bc0cba6).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:179`: 'record_id = raw["record_id"]'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR208:PRRT_kwDOTH_vCM6R_ofk

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md:42`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR208:PRRT_kwDOTH_vCM6R_ofk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Enforce the closed intake gates before scoring Because this rule is only documented here, it does not actually protect RUN-001: the inspected CRE-004 replay path (executio' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md` (SHA-256 f4d42154d70f615a5897921272806d43ae0dc656efc885ba9569db0367388577).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md:42`: 'The execution pipeline must reject scoring while any gate remains incomplete. No missing evaluator judgment may be inferred, simulated, backfilled, or replaced with an author-generated answer.'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR209:PRRT_kwDOTH_vCM6SASkl

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `comparative-experiments`
- Current location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json:7`
- Blocks experiment reconstruction: `true`
- Root cause: `comparative-experiments:theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR209:PRRT_kwDOTH_vCM6SASkl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use non-predictable candidate labels The frozen key preserves the source numbering (CANDIDATE001 maps to AV-001, and so on), even though CRE-004’s blinding rules require r' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json` (SHA-256 880f1be62af3340ea6f49f5201c044fb3cccd2857ea016684ccca83c032c3be6).
  - Current repository evidence at `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json:7`: '"CANDIDATE_001": "AV-001",'.
  - The later-change audit compared `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR20:PRRT_kwDOTH_vCM6OTp-R

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `frameworks`
- Current location: `frameworks/FARE/mathematics/theorem-index.md:19`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARE/mathematics/theorem-index.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR20:PRRT_kwDOTH_vCM6OTp-R found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep theorem identifiers unique These new index entries reuse MT-001 through MT-003 while the existing active proofs frameworks/FARE/mathematics/proofs/T001-identity-path-' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARE/mathematics/theorem-index.md` (SHA-256 03a41522047ece40be0f6f19c370938c9021e14c58e1002052aaab78ff48186f).
  - Current repository evidence at `frameworks/FARE/mathematics/theorem-index.md:19`: '| MT-003 | Path Composition Preserves Reachability | Accepted |'.
  - The later-change audit compared `frameworks/FARE/mathematics/theorem-index.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR211:PRRT_kwDOTH_vCM6SAc_1

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/candidate-architecture-registry.json:9`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/candidate-architecture-registry.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR211:PRRT_kwDOTH_vCM6SAc_1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Allow equivalence-conjectured in the registry The standard introduced in this same change says valid bidirectional translations let two candidates be marked equivalence-co' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/candidate-architecture-registry.json` (SHA-256 10f35de3758570c30aba04c837c6ee020e04cfccabb8f25222a1d82be518744b).
  - Current repository evidence at `theory/evaluation/candidate-architecture-registry.json:9`: '"allowed_statuses": ['.
  - The later-change audit compared `theory/evaluation/candidate-architecture-registry.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR217:PRRT_kwDOTH_vCM6SCBS0

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/pbts001-independent-replication-registry.json:71`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/pbts001-independent-replication-registry.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBS0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Rename the calibration metadata key to preserve the path This second calibration member duplicates the path-valued calibration key at line 7. Standard JSON parsers keep on' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/pbts001-independent-replication-registry.json` (SHA-256 cb15ce75a041f4863268c5be628dc09c1b18360feaebcc9309826cf953c39329).
  - Current repository evidence at `theory/evaluation/pbts001-independent-replication-registry.json:71`: '"calibration": {'.
  - The later-change audit compared `theory/evaluation/pbts001-independent-replication-registry.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR217:PRRT_kwDOTH_vCM6SCBS4

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/pbts001-independent-replication-response-schema.json:89`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/pbts001-independent-replication-response-schema.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBS4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Require distinct coverage entries in the response schema The schema's exact item counts only limit array length; they do not require the eight entries to cover PA-01 throu" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/pbts001-independent-replication-response-schema.json` (SHA-256 1ba27c70158ec6602d3966d56af76ba4ccdc9285c69f4304ca97be1804d98eba).
  - Current repository evidence at `theory/evaluation/pbts001-independent-replication-response-schema.json:89`: '"maxItems": 8,'.
  - The later-change audit compared `theory/evaluation/pbts001-independent-replication-response-schema.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR217:PRRT_kwDOTH_vCM6SCBSx

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_pbts001_replication_package.py:259`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_pbts001_replication_package.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR217:PRRT_kwDOTH_vCM6SCBSx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the package validator passing its own frozen protocol For this commit, running python tools/checkpbts001replicationpackage.py fails because the protocol’s nonclaim is' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_pbts001_replication_package.py` (SHA-256 5fbe6e175ca382c012f1bdd171f77efc70ce70889f16048e2032845b95c0f6c2).
  - Current repository evidence at `tools/check_pbts001_replication_package.py:259`: '"- FARA compliance;",'.
  - The later-change audit compared `tools/check_pbts001_replication_package.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR218:PRRT_kwDOTH_vCM6SG4vx

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/research/pbts001-replication-run-001-coordinator-controls.md:123`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/research/pbts001-replication-run-001-coordinator-controls.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR218:PRRT_kwDOTH_vCM6SG4vx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Use the slot-specific seed in the frozen controls This seed text does not match the run registry's frozen seedtemplate (PBTS-001-REP-001-RUN-001|{slotid}|order-v1). If the" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/research/pbts001-replication-run-001-coordinator-controls.md` (SHA-256 f861716dbdea7c9a3ad2f57add94f9c5222d76e16dd974c0ff33490b1732e1e7).
  - Current repository evidence at `docs/research/pbts001-replication-run-001-coordinator-controls.md:123`: '3. seed material is `PBTS-001-REP-001-RUN-001|slot-id|order-v1`;'.
  - The later-change audit compared `docs/research/pbts001-replication-run-001-coordinator-controls.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR21:PRRT_kwDOTH_vCM6OUG3P

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:1`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR21:PRRT_kwDOTH_vCM6OUG3P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Consolidate project status into the existing status file This adds a second current-status artifact while docs/PROJECTSTATUS.md already states that it records the current ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:1`: '# Project FAR Status'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR21:PRRT_kwDOTH_vCM6OUG3Q

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:57`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR21:PRRT_kwDOTH_vCM6OUG3Q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align FARE expansion gates with the freeze policy This development-order rule allows FARE Mathematics to expand when FARO or FARA require it, but the same new status docum' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:57`: 'v0.3.1 packages repository maturity work around the v0.3.0 baseline: README command center, dashboard generation, repository index, dashboard metrics, improved health diagnostics, GitHub Actions, release-readiness reporting, and repository '.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR220:PRRT_kwDOTH_vCM6SIkht

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/update_readme_dashboard.py:68`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/update_readme_dashboard.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR220:PRRT_kwDOTH_vCM6SIkht found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Close the README dashboard task append call In the target commit, running python -m pycompile tools/updatereadmedashboard.py fails with SyntaxError: '(' was never closed a" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/update_readme_dashboard.py` (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at `tools/update_readme_dashboard.py:68`: "if __name__=='__main__': main()".
  - The later-change audit compared `tools/update_readme_dashboard.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR221:PRRT_kwDOTH_vCM6SIzy3

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `repository-metadata`
- Current location: `README.md:20`
- Blocks experiment reconstruction: `false`
- Root cause: `repository-metadata:README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR221:PRRT_kwDOTH_vCM6SIzy3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep research-check aligned with README wording In this commit the README changes the required wording to “The project is deduction-first,” but tools/checkdeductionfirstpr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `README.md` (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at `README.md:20`: 'Public evaluation is authorized only when the exact theorem, premises, mechanization status, open-world boundary, Unknown discipline, and nonclaims are disclosed together.'.
  - The later-change audit compared `README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR221:PRRT_kwDOTH_vCM6SIzy4

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_thm_target_001.py:56`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_thm_target_001.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR221:PRRT_kwDOTH_vCM6SIzy4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Avoid rejecting the registered nonclaim as a claim When this new checker is invoked directly, and from the Makefile after the prior gate is fixed, it fails against the com' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_thm_target_001.py` (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at `tools/check_thm_target_001.py:56`: "assert family['THM-P8-CORR-001']['status']=='target_frozen_unproved'".
  - The later-change audit compared `tools/check_thm_target_001.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR224:PRRT_kwDOTH_vCM6SWc46

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/faithful-representation-specification-v1.0.json:45`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/faithful-representation-specification-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR224:PRRT_kwDOTH_vCM6SWc46 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Sync the faithful source artifact before advancing W0 This registry now advances FAITHFUL-REP-001 to the W0 proof package, but its declared sourceartifact (docs/research/f' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/faithful-representation-specification-v1.0.json` (SHA-256 c6d4f1fd3f69bfca62fe91a2df38807bdf1c5bddbd9b67c7d3c24a1e5b5c8a11).
  - Current repository evidence at `theory/evaluation/faithful-representation-specification-v1.0.json:45`: '}'.
  - The later-change audit compared `theory/evaluation/faithful-representation-specification-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR225:PRRT_kwDOTH_vCM6SXDn-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/s_core_w0_reference.py:171`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/s_core_w0_reference.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR225:PRRT_kwDOTH_vCM6SXDn- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not infer sort preservation from labels For a valid sort-preserving renaming whose fresh target name happens to start with another fixture prefix, renamed() raises befo' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/s_core_w0_reference.py` (SHA-256 6d21aaa7a70103a31185821763c3f45ba0301f6416c559e804af431a2c6f244e).
  - Current repository evidence at `tools/s_core_w0_reference.py:171`: 'raise ValueError("renaming must preserve sorts")'.
  - The later-change audit compared `tools/s_core_w0_reference.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR225:PRRT_kwDOTH_vCM6SXDn8

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/s_core_w0_reference.py:186`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/s_core_w0_reference.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR225:PRRT_kwDOTH_vCM6SXDn8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restrict canonical codes to the material closure When a finite contract contains declared nodes outside Cl(materialseed), this loop canonicalizes every self.nodes entry ra' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/s_core_w0_reference.py` (SHA-256 6d21aaa7a70103a31185821763c3f45ba0301f6416c559e804af431a2c6f244e).
  - Current repository evidence at `tools/s_core_w0_reference.py:186`: 'groups.setdefault(sort_map[node], []).append(node)'.
  - The later-change audit compared `tools/s_core_w0_reference.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR226:PRRT_kwDOTH_vCM6SXowJ

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_s_core_w1.py:18`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_s_core_w1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR226:PRRT_kwDOTH_vCM6SXowJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use the path constant for the W1 registry lookup When python tools/checkscorew1.py runs, this line always raises AttributeError because reg was rebound above to the loaded' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_s_core_w1.py` (SHA-256 0777b463ee186e2a3f5fcf896b007bb95bcf257e200d5af1c76d430293c922a5).
  - Current repository evidence at `tools/check_s_core_w1.py:18`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/check_s_core_w1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR226:PRRT_kwDOTH_vCM6SXowM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/s_core_w1_reference.py:72`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/s_core_w1_reference.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR226:PRRT_kwDOTH_vCM6SXowM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject shared elements with conflicting denotations For the case where the same source element id appears in multiple direct axes with a different denotation, this validat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/s_core_w1_reference.py` (SHA-256 42472f9725f10240bbe9892a62c84cc65735f1de17a37a7699b1b8c7e567922f).
  - Current repository evidence at `tools/s_core_w1_reference.py:72`: 'raise W1Error(f"shared element {element_id} changes sort: {old} -> {sort}")'.
  - The later-change audit compared `tools/s_core_w1_reference.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR229:PRRT_kwDOTH_vCM6SaGam

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_faithful_representation.py:12`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_faithful_representation.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR229:PRRT_kwDOTH_vCM6SaGam found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the faithful-representation check aligned with the spec With this new phrase guard, make research-check/make health-fast fails on the committed tree: the faithful spe' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_faithful_representation.py` (SHA-256 588512b670fc6b3f84911a5bd0c2d695c4185b7b18af79c29a6f070ac8f2033b).
  - Current repository evidence at `tools/check_faithful_representation.py:12`: "d=load(REG); assert d['specification_id']=='FAITHFUL-REP-001' and d['version']=='1.0'; assert d['w3_proof_registry']==W3.relative_to(ROOT).as_posix(); assert d['w4_proof_registry']==W4.relative_to(ROOT).as_posix(); assert d['recovery_contra".
  - The later-change audit compared `tools/check_faithful_representation.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR229:PRRT_kwDOTH_vCM6SaGao

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `repository-metadata`
- Current location: `README.md:68`
- Blocks experiment reconstruction: `true`
- Root cause: `repository-metadata:README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR229:PRRT_kwDOTH_vCM6SaGao found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Regenerate the README dashboard from the updated generator This section is inside the BEGIN GENERATED PROJECT FAR DASHBOARD block, but it was not regenerated from the upda' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `README.md` (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at `README.md:68`: ''.
  - The later-change audit compared `README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR22:PRRT_kwDOTH_vCM6OWe3V

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/CANONICAL_MAP.md:177`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/CANONICAL_MAP.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR22:PRRT_kwDOTH_vCM6OWe3V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Restore removed canonical theory entries This rewrite leaves the Theory section ending after Propositions, but the parent map also recorded canonical locations for Lemmas,' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/CANONICAL_MAP.md` (SHA-256 9fae5238b7a853b517252f364f907623ab8729d92dd94b6aaf98194534f1b76e).
  - Current repository evidence at `docs/CANONICAL_MAP.md:177`: '- Comparative experiment registration: `theory/evaluation/comparative-representation/experiment-registry.json` is the canonical registry for blinded comparative representation experiments. Legacy external-validation reports must not be recl'.
  - The later-change audit compared `docs/CANONICAL_MAP.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR22:PRRT_kwDOTH_vCM6OWe3W

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FAR/README.md:25`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FAR/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR22:PRRT_kwDOTH_vCM6OWe3W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align FARO status with existing FARO docs This new status says FARO development should only begin after FAR stabilizes, but the repository already contains an active frame' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FAR/README.md` (SHA-256 e01275de69493cc5e2fe23d4d32ece40af7346f921e155688456995be49a77c7).
  - Current repository evidence at `frameworks/FAR/README.md:25`: '## Framework Role'.
  - The later-change audit compared `frameworks/FAR/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR231:PRRT_kwDOTH_vCM6ScNF3

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validation-engine`
- Current location: `far_validation/engine.py:565`
- Blocks experiment reconstruction: `false`
- Root cause: `validation-engine:far_validation/engine.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR231:PRRT_kwDOTH_vCM6ScNF3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Decode timeout output before serializing results When a checker times out after emitting output, subprocess.TimeoutExpired.stdout and stderr are bytes even though text=Tru' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `far_validation/engine.py` (SHA-256 1b3008a73f39dbe21a8179f6c371f04c9cc7f1f4e867d015f651f9620c82beaf).
  - Current repository evidence at `far_validation/engine.py:565`: 'stderr=exc.stderr or "",'.
  - The later-change audit compared `far_validation/engine.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR231:PRRT_kwDOTH_vCM6ScNF9

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validation-engine`
- Current location: `far_validation/engine.py:95`
- Blocks experiment reconstruction: `false`
- Root cause: `validation-engine:far_validation/engine.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR231:PRRT_kwDOTH_vCM6ScNF9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Treat globstar inputs as covering direct files In changed-file mode, fnmatch/Path.match both return false for direct-file cases such as README.md vs /.md and tools/runtest' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `far_validation/engine.py` (SHA-256 1b3008a73f39dbe21a8179f6c371f04c9cc7f1f4e867d015f651f9620c82beaf).
  - Current repository evidence at `far_validation/engine.py:95`: 'if fnmatch.fnmatch(normalized, pattern) or Path(normalized).match(pattern):'.
  - The later-change audit compared `far_validation/engine.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR232:PRRT_kwDOTH_vCM6Sd90_

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validation-engine`
- Current location: `far_validation/weakening.py:137`
- Blocks experiment reconstruction: `false`
- Root cause: `validation-engine:far_validation/weakening.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR232:PRRT_kwDOTH_vCM6Sd90_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Compare the old path when auditing renames When Git reports a rename such as R059 tests/testold.py tests/testnew.py, this keeps only the new path, so show(base, path) look' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `far_validation/weakening.py` (SHA-256 aae88e582f096015e5246ffb079ae263b212e66177a5a4e041176253990b0fde).
  - Current repository evidence at `far_validation/weakening.py:137`: 'status, path = fields[0], fields[-1]'.
  - The later-change audit compared `far_validation/weakening.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR232:PRRT_kwDOTH_vCM6Sd91A

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validation-engine`
- Current location: `far_validation/tracing.py:145`
- Blocks experiment reconstruction: `true`
- Root cause: `validation-engine:far_validation/tracing.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR232:PRRT_kwDOTH_vCM6Sd91A found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Account for dirfd-relative traced file accesses When a traced syscall is openat/newfstatat against a directory fd, for example openat(3, "secret.txt", ...), this branch re' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `far_validation/tracing.py` (SHA-256 3cd16ac267cc450d93db7a0939621b2ba71473fac42ca3507613c59153423830).
  - Current repository evidence at `far_validation/tracing.py:145`: 'return None'.
  - The later-change audit compared `far_validation/tracing.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR233:PRRT_kwDOTH_vCM6Sfq25

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_w3_5_corpus_freeze.py:77`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_w3_5_corpus_freeze.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR233:PRRT_kwDOTH_vCM6Sfq25 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Enforce required instance versions before freezing When RCS-001 marks version as a required instance field, this per-record validation never checks for it; all 18 new sour' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_w3_5_corpus_freeze.py` (SHA-256 66419a598ad54c35fb458ea35113e85fc6334d8e12d2276792637472147f9cee).
  - Current repository evidence at `tools/check_w3_5_corpus_freeze.py:77`: "for entry in catalog.get('records',[]):".
  - The later-change audit compared `tools/check_w3_5_corpus_freeze.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR234:PRRT_kwDOTH_vCM6Srbte

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/w3_5_grel.py:79`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/w3_5_grel.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR234:PRRT_kwDOTH_vCM6Srbte found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject unreachable carriers in GREL validation When validating externally supplied GREL packages, this only checks that the declared root exists; it never verifies that al' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/w3_5_grel.py` (SHA-256 91a303bd87b05db2231f5d57d0eabf4a52307c987d88e1c3d42d30dd7102613c).
  - Current repository evidence at `tools/w3_5_grel.py:79`: 'raise FactorizationError("GREL root entity is missing")'.
  - The later-change audit compared `tools/w3_5_grel.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR234:PRRT_kwDOTH_vCM6Srbti

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_w3_5_factorization.py:82`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_w3_5_factorization.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR234:PRRT_kwDOTH_vCM6Srbti found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require every frozen runtime check to be present If a future change drops a required runtime check such as nohiddeninterpreter but leaves the remaining checks as pass, thi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_w3_5_factorization.py` (SHA-256 233ea87dd07aaa24a4db7fa89761f3a1bc1ee160cbe62a992b977e9fe1778511).
  - Current repository evidence at `tools/check_w3_5_factorization.py:82`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/check_w3_5_factorization.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR236:PRRT_kwDOTH_vCM6Sv2G6

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_w3_5_corpus_freeze.py:58`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_w3_5_corpus_freeze.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR236:PRRT_kwDOTH_vCM6Sv2G6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Don\'t hard-code the withdrawn candidate outcome When W3.5 later moves to inprogresscandidatecomplete, this checker will only accept currentresults.candidateinvariants == "' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_w3_5_corpus_freeze.py` (SHA-256 66419a598ad54c35fb458ea35113e85fc6334d8e12d2276792637472147f9cee).
  - Current repository evidence at `tools/check_w3_5_corpus_freeze.py:58`: "current=w35.get('current_results',{}); req(current.get('reasoning_contrast_corpus')=='frozen','W3.5 current corpus result must be frozen',e); expected_disc='bounded_role_conjunctive_discrimination_established' if stage in {'in_progress_spec".
  - The later-change audit compared `tools/check_w3_5_corpus_freeze.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR237:PRRT_kwDOTH_vCM6SwTr0

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/w3_5_candidate_execution.py:74`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/w3_5_candidate_execution.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR237:PRRT_kwDOTH_vCM6SwTr0 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Score information in equivalence comparisons For reconstructable trials, the equivalence vector can declare commitmentequivalent without scoring the information dimension,' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/w3_5_candidate_execution.py` (SHA-256 6a1ad3c7eb596e5f28f16b5f5c87fb8215e7673176f10caffa62b6e3bce87f01).
  - Current repository evidence at `tools/w3_5_candidate_execution.py:74`: '"equivalence_comparison":{"structural":"pass" if reconstruct else ("not_applicable" if not present else "fail"),"semantic":"pass" if reconstruct else ("not_applicable" if not present else "fail"),"operational":"pass" if reconstruct else ("n'.
  - The later-change audit compared `tools/w3_5_candidate_execution.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR237:PRRT_kwDOTH_vCM6SwTry

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_w3_5_candidate_tests.py:26`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_w3_5_candidate_tests.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR237:PRRT_kwDOTH_vCM6SwTry found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Load preserved trial records before accepting completion For the completed candidate package, this regenerates trials from the current Python module and the result only ha' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_w3_5_candidate_tests.py` (SHA-256 3dbfa3bfd988947fa3a88ea7a4fa7deed530931ce9c0c91f9a0269eeb2751b65).
  - Current repository evidence at `tools/check_w3_5_candidate_tests.py:26`: 'trials=execute()'.
  - The later-change audit compared `tools/check_w3_5_candidate_tests.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR238:PRRT_kwDOTH_vCM6Swy90

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/w3-5-claim-impact-result-v1.0.json:1`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/w3-5-claim-impact-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR238:PRRT_kwDOTH_vCM6Swy90 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Synchronize the central claim registry during claim-impact closure This new claim-impact artifact completes the centralclaimimpactaudit and authorizes W5, but the canonica' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/w3-5-claim-impact-result-v1.0.json` (SHA-256 434765b0a73a221cc889f5fbd1eed5ffba4f3dd63a0a157e21ff3d81e7ae3093).
  - Current repository evidence at `theory/evaluation/w3-5-claim-impact-result-v1.0.json:1`: '{"artifact_id":"W35-CLAIM-RESULT-001","gate_effect":{"W3_5_resolved":true,"W5_authorized":true,"W5_theorem_proved":false},"nonclaims":["W5 is complete","Faithful_split is proved","a universal kernel exists","FARA primitives are universally '.
  - The later-change audit compared `theory/evaluation/w3-5-claim-impact-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR238:PRRT_kwDOTH_vCM6Swy9x

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/project_status_report.py:53`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/project_status_report.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR238:PRRT_kwDOTH_vCM6Swy9x found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update the dashboard generators with W5 authorization When this status report starts declaring W3.5 resolved and W5 authorized, the canonical planner path still rewrites t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/project_status_report.py` (SHA-256 9eb604bb78c3b4a56100a43995212c30d6a3b07d8e549328b6a4030184406a44).
  - Current repository evidence at `tools/project_status_report.py:53`: '"- W5 theorem assembly is authorized to begin.",'.
  - The later-change audit compared `tools/project_status_report.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR239:PRRT_kwDOTH_vCM6SxUIT

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/s-core-construction-obstruction-ledger.json:5`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/s-core-construction-obstruction-ledger.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Update the authoritative ledger before marking W5 complete This promotes the machine-readable ledger to W5-complete, but the same registry still declares statementauthorit' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/s-core-construction-obstruction-ledger.json` (SHA-256 46c94d5b4190d74b4c9f7c157b6362a7186cd9b39c13636648348f4d384cd4eb).
  - Current repository evidence at `theory/evaluation/s-core-construction-obstruction-ledger.json:5`: '"status":"w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved",'.
  - The later-change audit compared `theory/evaluation/s-core-construction-obstruction-ledger.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR239:PRRT_kwDOTH_vCM6SxUIX

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_thm_target_001.py:111`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_thm_target_001.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Register W5 as satisfying the scoped proof gate After this commit marks the bounded Score theorem proved, this assertion locks research-gates.json in the old pre-W5 state:' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_thm_target_001.py` (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at `tools/check_thm_target_001.py:111`: "assert gates['scoped-representation-proof']['evidence']==[]".
  - The later-change audit compared `tools/check_thm_target_001.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR239:PRRT_kwDOTH_vCM6SxUIb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_thm_target_001.py:122`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_thm_target_001.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR239:PRRT_kwDOTH_vCM6SxUIb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align central claims with the bounded W5 theorem With W5 now proving THM-CORE-COMMON-001 and THM-CORE-REP-001, the central claim registry is left contradictory: CLM-EXISTE' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_thm_target_001.py` (SHA-256 fe4e72bf62f55118f0ede618f21f4b51946f091ec719a67f38c379028ca938cb).
  - Current repository evidence at `tools/check_thm_target_001.py:122`: "assert claim['current_status'] not in {'supported','supported_at_registered_control_scope'}".
  - The later-change audit compared `tools/check_thm_target_001.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR23:PRRT_kwDOTH_vCM6OWoT2

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FAR/README.md:21`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FAR/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR23:PRRT_kwDOTH_vCM6OWoT2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Advance FAR status past the completed Phase 2 gate This updated status is now inconsistent with the same commit's audit record, which marks Phase 2 complete and says FAR i" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FAR/README.md` (SHA-256 e01275de69493cc5e2fe23d4d32ece40af7346f921e155688456995be49a77c7).
  - Current repository evidence at `frameworks/FAR/README.md:21`: 'Future FAR changes should be driven by concrete downstream requirements, worked examples, or validated methodological deficiencies.'.
  - The later-change audit compared `frameworks/FAR/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR23:PRRT_kwDOTH_vCM6OWoTz

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md:135`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR23:PRRT_kwDOTH_vCM6OWoTz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Define candidate generation in the canonical workflow This closes the earlier gap by saying candidate generation is explicitly placed in Stage 6, but the commit never upda' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md` (SHA-256 b62a484b685bea9b0a084c78f72da8f3898bd512bca2d01a997b0bc49625b428).
  - Current repository evidence at `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md:135`: 'Candidate generation is explicitly placed within Stage 6 — Perform Reasoning.'.
  - The later-change audit compared `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR240:PRRT_kwDOTH_vCM6Sxc8r

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `mechanization`
- Current location: `mechanization/lean/SCoreW5.lean:55`
- Blocks experiment reconstruction: `true`
- Root cause: `mechanization:mechanization/lean/SCoreW5.lean`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR240:PRRT_kwDOTH_vCM6Sxc8r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Make FaithfulSplit enforce the frozen contract The new registry/doc present this as machine-checking the registered W5 Faithfulsplit, but this definition only requires a c' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/lean/SCoreW5.lean` (SHA-256 e9e5e25b941a0648df13eea91bf19fcaa187d4d7854512ae893afd0a01681703).
  - Current repository evidence at `mechanization/lean/SCoreW5.lean:55`: 'target.investigation = source.stakes ∧'.
  - The later-change audit compared `mechanization/lean/SCoreW5.lean` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR240:PRRT_kwDOTH_vCM6Sxc8v

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/s-core-w5-lean-mechanization.json:30`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/s-core-w5-lean-mechanization.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR240:PRRT_kwDOTH_vCM6Sxc8v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reconcile the canonical W5 gate with this claim When this new artifact marks boundedfaithfulrepresentation as machinechecked, the canonical theorem target it names is left' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/s-core-w5-lean-mechanization.json` (SHA-256 1e9c93921189e72a5d0725baf17aeb17ab50769e2027e0038c8d5db978ba80a7).
  - Current repository evidence at `theory/evaluation/s-core-w5-lean-mechanization.json:30`: '"bounded_faithful_representation": "machine_checked",'.
  - The later-change audit compared `theory/evaluation/s-core-w5-lean-mechanization.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR241:PRRT_kwDOTH_vCM6Sx4fi

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/s-core-w5-independent-review-package-v1.0.json:27`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/s-core-w5-independent-review-package-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR241:PRRT_kwDOTH_vCM6Sx4fi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Register all mandatory proof dependencies The frozen source list jumps directly from the construction-obstruction ledger to the W5 assembly, but the review package’s own a' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/s-core-w5-independent-review-package-v1.0.json` (SHA-256 9be5efc8f46802f5b225ae526ad1c52cc4f13512667b04ef3b706549b9cb618c).
  - Current repository evidence at `theory/evaluation/s-core-w5-independent-review-package-v1.0.json:27`: '{"path": "docs/research/s-core-w5-theorem-assembly-proof-v1.0.md"},'.
  - The later-change audit compared `theory/evaluation/s-core-w5-independent-review-package-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR241:PRRT_kwDOTH_vCM6Sx4fk

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_s_core_w5_review_package.py:74`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_s_core_w5_review_package.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR241:PRRT_kwDOTH_vCM6Sx4fk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Compare frozen hashes to file contents This check only compares the JSON-declared gitblobsha to another hard-coded string, so if the protected artifact changes while the r' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_s_core_w5_review_package.py` (SHA-256 42e29a81e41b3dab9c26f7836e87e9bc7eb10d26a21473dcfb0794d01a9c9469).
  - Current repository evidence at `tools/check_s_core_w5_review_package.py:74`: '"W5 assembly registry binding changed",'.
  - The later-change audit compared `tools/check_s_core_w5_review_package.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR242:PRRT_kwDOTH_vCM6Sy_r1

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/planning/architecture-neutral-research-roadmap.md:119`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/planning/architecture-neutral-research-roadmap.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR242:PRRT_kwDOTH_vCM6Sy_r1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align the generated task queue with USD W1 This roadmap now makes USD-W1-SCOPE-EXT the immediate next action, but the generated planning pipeline still contradicts it: mak' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/planning/architecture-neutral-research-roadmap.md` (SHA-256 8e9eb2796d08b826c73313ed2b79c256f2a3822e0b4c792918dc0b62fd6eb11f).
  - Current repository evidence at `docs/planning/architecture-neutral-research-roadmap.md:119`: 'Freeze and execute one `USD-W1-SCOPE-EXT` feature family. The recommended first unit is partial observability because it directly tests whether the explicit-state construction survives restricted access without hidden-state smuggling.'.
  - The later-change audit compared `docs/planning/architecture-neutral-research-roadmap.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR243:PRRT_kwDOTH_vCM6SzFwm

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json:27`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR243:PRRT_kwDOTH_vCM6SzFwm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Make positive fixtures satisfy Spofin When this history-sensitive fixture is used to support the registered pass, it is not an admitted Spofin source presentation: the sco' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json` (SHA-256 7ad27dba3937160c4e34b4c56614ac143f472cb30d36dca2bd167b99c5e2b54d).
  - Current repository evidence at `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json:27`: '"expected": "distinct_observation_histories_preserved_even_when_current_observation_matches"'.
  - The later-change audit compared `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR243:PRRT_kwDOTH_vCM6SzFwo

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json:43`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR243:PRRT_kwDOTH_vCM6SzFwo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use canonical USD theorem IDs These theorem-effect keys do not match the frozen target registry: theory/evaluation/universal-structure-discovery-target-v1.0.json defines t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json` (SHA-256 8b2ee652e026fb5498dd3c107a6609e44c1ec3f5cb78e876f07817ab642ca8ea).
  - Current repository evidence at `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json:43`: '"THM-US-NEC-001": "unresolved",'.
  - The later-change audit compared `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR244:PRRT_kwDOTH_vCM6SzTq5

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json:24`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR244:PRRT_kwDOTH_vCM6SzTq5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve admitted observations in the obligations The scope admits observations as part of Sinfeff, but the registered/proved obligations never require observation relatio' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json` (SHA-256 5ef9e1730817dbfa6234cd68cca03e4668e38d58ce0a13e3bf8e90d2a52f362d).
  - Current repository evidence at `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json:24`: '"INF-EXT-005_history_and_revision_prefix_coherence",'.
  - The later-change audit compared `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR245:PRRT_kwDOTH_vCM6Szcon

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json:16`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR245:PRRT_kwDOTH_vCM6Szcon found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require computable guard-crossing certificates For admitted sources where a guard has isolated crossings but the source does not declare computable brackets, separation/tr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json` (SHA-256 d8f00cd42eaa58262bb6b32e3f4d43c98b9cfc7a5534f4f288811453b7de8ada).
  - Current repository evidence at `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json:16`: '"inputs": "piecewise-rational controls with finite descriptions and declared switching times",'.
  - The later-change audit compared `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR245:PRRT_kwDOTH_vCM6Szcoo

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `test-infrastructure`
- Current location: `tests/test_usd_w1_continuous_dynamics.py:19`
- Blocks experiment reconstruction: `false`
- Root cause: `test-infrastructure:tests/test_usd_w1_continuous_dynamics.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR245:PRRT_kwDOTH_vCM6Szcoo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Put these tests on the canonical unittest path When the project’s canonical tools/runtests.py/make test path is used, unittest.TestLoader.loadTestsFromModule only collects' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_usd_w1_continuous_dynamics.py` (SHA-256 70abbe1d309438c7ca620314cfa0201448c627286f77f281350e97a3e65fa8e4).
  - Current repository evidence at `tests/test_usd_w1_continuous_dynamics.py:19`: ''.
  - The later-change audit compared `tests/test_usd_w1_continuous_dynamics.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR246:PRRT_kwDOTH_vCM6SzrWU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json:12`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR246:PRRT_kwDOTH_vCM6SzrWU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Exclude completed finite histories from the scope When the admitted history domain includes a finite ... sequence, a completed finite trace with a fixed terminal event cou' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json` (SHA-256 8441a4e81b7fb4d47c4359cd0b50a66b857bd0ec1aaae32f75336cd4d1b12987).
  - Current repository evidence at `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json:12`: '"history_domain": "a finite or countably unbounded sequence of effectively indexed events with no frozen terminal length",'.
  - The later-change audit compared `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR249:PRRT_kwDOTH_vCM6S0g9r

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json:22`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR249:PRRT_kwDOTH_vCM6S0g9r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add the measurement-to-source mapping to the scope The report freezes a future positive APC package that includes “a mapping from measurements to source states and transit' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json` (SHA-256 f15d6bf77bbde44907d900f05c0d3126c7fd4d2242ab6f228767257f51d8369e).
  - Current repository evidence at `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json:22`: '"replication or independent confirmation"'.
  - The later-change audit compared `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR249:PRRT_kwDOTH_vCM6S0g9v

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json:54`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR249:PRRT_kwDOTH_vCM6S0g9v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Sync the program registry before routing to W2 This result routes the next decisive workstream to USD-W2-ALT-VOCAB, but the governing program registry still records USD-W1' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json` (SHA-256 efcfc6ba6064891d24b59ba6c5a70426dc1909a5ccbcc77986715313ad2782b7).
  - Current repository evidence at `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json:54`: '"next_decisive_workstream": "USD-W2-ALT-VOCAB",'.
  - The later-change audit compared `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR24:PRRT_kwDOTH_vCM6OXXCe

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md:253`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR24:PRRT_kwDOTH_vCM6OXXCe found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not mark Phase 3 complete while application is stale The audit lists frameworks/FAR/application.md as reviewed, but that document was not updated for this Phase 3 polic' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md` (SHA-256 fbb051973e105bc6334a4eb6d2f83c2554c03795bdc1e8bb27ee2e4562ade44d).
  - Current repository evidence at `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md:253`: 'All Phase 3 corrections have been implemented.'.
  - The later-change audit compared `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR24:PRRT_kwDOTH_vCM6OXXCg

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FAR/workflow.md:121`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FAR/workflow.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR24:PRRT_kwDOTH_vCM6OXXCg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require revision records in the canonical workflow The new stability criterion says FAR shall require revision records whenever an investigation revisits an earlier stage ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FAR/workflow.md` (SHA-256 e32e425b80159da92925eb1a103fdc56db21b8166bc0a185dadf5c3b23ae81bb).
  - Current repository evidence at `frameworks/FAR/workflow.md:121`: 'Every return to an earlier stage should record:'.
  - The later-change audit compared `frameworks/FAR/workflow.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR250:PRRT_kwDOTH_vCM6S0qkt

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:63`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR250:PRRT_kwDOTH_vCM6S0qkt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record the missing GREL/ARG-HIST comparison With four candidates, the completed pairwise ledger needs six unordered comparisons, but this array records only five and omits' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json` (SHA-256 dac279da465a183bcf40c23497a9ac07988227ddaa0e648a415117fca7dad209).
  - Current repository evidence at `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:63`: '"pairwise_results": ['.
  - The later-change audit compared `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR250:PRRT_kwDOTH_vCM6S0qkx

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:68`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR250:PRRT_kwDOTH_vCM6S0qkx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reclassify LTS-PROV versus ARG-HIST consistently Under the dominance rule recorded in the audit, LTS-PROV-001 is no worse on coverage/preservation (pass vs partial) and ha' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json` (SHA-256 dac279da465a183bcf40c23497a9ac07988227ddaa0e648a415117fca7dad209).
  - Current repository evidence at `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:68`: '{"left": "LTS-PROV-001", "right": "ARG-HIST-001", "classification": "incomparable_tradeoff"}'.
  - The later-change audit compared `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR251:PRRT_kwDOTH_vCM6S0zhD

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json:19`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Add the missing semantic-interface transform The governing POST-W5-USD-001 definition for USD-W3-INVARIANCE requires the semantic-interface replacement class, but this con' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json` (SHA-256 ca7cc08899fc0b34ba9b3900c9d1b09e5bb013f29a63a9cd4a4b3ec3f0343605).
  - Current repository evidence at `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json:19`: '"transformations": ['.
  - The later-change audit compared `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR251:PRRT_kwDOTH_vCM6S0zhH

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:38`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w3-representation-invariance-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Test GREL before preserving its dominance relations These vsGREL outcomes are published even though GREL-001 is omitted from both contract and result testedvocabularies, a' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json` (SHA-256 6389334c3e1ec1dedc26ea1ad5ffb5d8032fce0e11aed95fd31961fe58a9ef0a).
  - Current repository evidence at `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:38`: '"LTS_PROV_vs_GREL": "bounded_dominance_preserved"'.
  - The later-change audit compared `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR251:PRRT_kwDOTH_vCM6S0zhL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:50`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/usd-w3-representation-invariance-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR251:PRRT_kwDOTH_vCM6S0zhL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use the registered USD-W4-NECESSITY workstream id Repo-wide search finds USD-W4-ABLATION only in this new W3 package, while the governing POST-W5 program registers the nex' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json` (SHA-256 6389334c3e1ec1dedc26ea1ad5ffb5d8032fce0e11aed95fd31961fe58a9ef0a).
  - Current repository evidence at `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:50`: '"next_workstream": "USD-W4-ABLATION",'.
  - The later-change audit compared `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR252:PRRT_kwDOTH_vCM6S1nVJ

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json:61`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR252:PRRT_kwDOTH_vCM6S1nVJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not advance to W5 before W4 controls are run When this result is consumed to schedule the next USD workstream, it skips part of the registered W4 gate: the frozen progr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json` (SHA-256 777d215848223d7dbec744916f1a68bb563d3c86dca383ea61dd479c7245abe2).
  - Current repository evidence at `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json:61`: '"next_workstream": "USD-W5-MIN-EQUIV",'.
  - The later-change audit compared `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR253:PRRT_kwDOTH_vCM6S12uq

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json:8`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR253:PRRT_kwDOTH_vCM6S12uq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include GREL in the successful set When downstream W5 consumers use this contract as the frozen success set, GREL-001 is incorrectly dropped even though the W2 bounded com' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json` (SHA-256 33406af9a859c33774f46087b3a3645a4f99f71cdfa153b31b672be2bf4d92d3).
  - Current repository evidence at `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json:8`: '"successful_candidates": ["FARA-001", "LTS-PROV-001"],'.
  - The later-change audit compared `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR254:PRRT_kwDOTH_vCM6S2A_u

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/usd-w6-independence-result-v1.0.json:17`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/usd-w6-independence-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR254:PRRT_kwDOTH_vCM6S2A_u found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not mark W6 executed without executable artifacts This block records a completed three-path execution with artifact isolation, a separate verifier, deterministic compar' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/usd-w6-independence-result-v1.0.json` (SHA-256 a90bfb289a42681b1fa5a87e18bdd35436cb16516aa25162cef9b1babe1506bb).
  - Current repository evidence at `theory/evaluation/usd-w6-independence-result-v1.0.json:17`: '"deterministic_comparison": "pass",'.
  - The later-change audit compared `theory/evaluation/usd-w6-independence-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR255:PRRT_kwDOTH_vCM6S611M

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:29`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR255:PRRT_kwDOTH_vCM6S611M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep USD-H-DISC within the registered GREL support This terminal disposition broadens reasoning-discrimination support to ARG-HIST, but the USD-W2 source only records USD-' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json` (SHA-256 641f9946dcf29bfdd40eaf88d32974ec3dc6d448fc529e0d26da84001445d48a).
  - Current repository evidence at `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:29`: '"USD-H-DISC": "supported_for_FARA_against_GREL_and_ARG-HIST_but_not_unique_against_LTS-PROV",'.
  - The later-change audit compared `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR255:PRRT_kwDOTH_vCM6S611P

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:47`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR255:PRRT_kwDOTH_vCM6S611P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Synchronize terminal outcome with status registry Declaring this synthesis as the incomparablekernels program outcome adds a completed USD result, but the repository statu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json` (SHA-256 641f9946dcf29bfdd40eaf88d32974ec3dc6d448fc529e0d26da84001445d48a).
  - Current repository evidence at `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:47`: '"valid_program_outcome_mapping": "incomparable_kernels",'.
  - The later-change audit compared `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR256:PRRT_kwDOTH_vCM6S7HDC

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json:15`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR256:PRRT_kwDOTH_vCM6S7HDC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include the EVC parent program in the manifest This programandsynthesis group lists the pre-W5 USD program but omits theory/evaluation/post-w5-usd-next-program-v1.0.json, ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json` (SHA-256 35028a27954124d2c532d2f0e5ed1ddd707fa859fb72901d19034a452150bfcb).
  - Current repository evidence at `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json:15`: '"docs/research/post-w5-usd-terminal-synthesis-v1.0.md",'.
  - The later-change audit compared `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR258:PRRT_kwDOTH_vCM6S8A12

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json:39`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR258:PRRT_kwDOTH_vCM6S8A12 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Gate all twelve adversarial challenges The protocol’s terminal rules are keyed to mandatoryattackdomains, but this list stops before the two corpus domains added as R4-C11' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json` (SHA-256 89f788be840341f3ab6583f1615d1049a5ffcc69f13b06bda3f1ddd432f83585).
  - Current repository evidence at `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json:39`: '"independence labels and universal-structure claim boundaries"'.
  - The later-change audit compared `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR260:PRRT_kwDOTH_vCM6S-n2N

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:12`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR260:PRRT_kwDOTH_vCM6S-n2N found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Wire the IKD queue into canonical planning In the current repo, tools/generatenexttasks.py is still the command behind make plan/docs/planning/next-actions.md, and I check' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:12`: '{"target_pr":264,"workstream":"IKD-W4-CROSS-FEATURE-COMPOSITION","result":"bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions"},'.
  - The later-change audit compared `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR260:PRRT_kwDOTH_vCM6S-n2U

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR260:PRRT_kwDOTH_vCM6S-n2U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Block candidate scoring in the queue The prose registration says PR #261 must freeze admission controls and “must not execute candidate scoring” (docs/research/post-usd-in' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28`: '}'.
  - The later-change audit compared `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR261:PRRT_kwDOTH_vCM6S-3sQ

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json:47`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR261:PRRT_kwDOTH_vCM6S-3sQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Fill mandatory candidate declarations before freezing These objects are admitted as admittedfrozenunscored, but each frozen candidate only has source/primitives/constraint' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json` (SHA-256 a322b30601057a7f7695f65235ed5b59decf84e0d94a372f213de3c8b5441f61).
  - Current repository evidence at `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json:47`: '"conceptual_source": "compositional process semantics and categorical structure",'.
  - The later-change audit compared `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR266:PRRT_kwDOTH_vCM6TBUHR

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_post_usd_internal_discovery_continuation.py:35`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_post_usd_internal_discovery_continuation.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR266:PRRT_kwDOTH_vCM6TBUHR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restore validation for the IKD-W6 queue state Since nextpr still allows 266 above, making the only exact queue-shape check if nextpr==267 means the standalone validator no' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_post_usd_internal_discovery_continuation.py` (SHA-256 cccd7d1c158aa5d38566fd1e4bdf424c3f1155bc5a751eec1dcf60e681d00eaf).
  - Current repository evidence at `tools/check_post_usd_internal_discovery_continuation.py:35`: "assert queue['ordered_followups']==[]".
  - The later-change audit compared `tools/check_post_usd_internal_discovery_continuation.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR267:PRRT_kwDOTH_vCM6TBxUH

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/ikd-w7-lower-bounds-v1.0.json:70`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/ikd-w7-lower-bounds-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR267:PRRT_kwDOTH_vCM6TBxUH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Leave W7 unresolved until all countermodels are closed Because this result is used to move the queue to IKD-W8, marking W7 complete here skips part of the registered W6 ha' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/ikd-w7-lower-bounds-v1.0.json` (SHA-256 3557e505d617553defbda22549aa1cb5460b7fafd0d6d682ec8c973676054c0d).
  - Current repository evidence at `theory/evaluation/ikd-w7-lower-bounds-v1.0.json:70`: '"terminal_result": "all_five_rccd_components_have_conditional_lower_bounds_on_defined_class",'.
  - The later-change audit compared `theory/evaluation/ikd-w7-lower-bounds-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR268:PRRT_kwDOTH_vCM6TDpuf

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json:69`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/ikd-w8-minimal-frontier-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR268:PRRT_kwDOTH_vCM6TDpuf found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record the componentwise frontier evidence For the W8 frontier result, this records only the final kernel and realization sets, but not the componentwise cost ledger, domi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json` (SHA-256 e65eb916b413f80df46a8a7b476dc3f8d13e957fff42b5d368c8da2b1ce5413c).
  - Current repository evidence at `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json:69`: '"interpretation": "the three formerly incomparable architectures are incomparable implementations inside one commitment-equivalence class, not distinct necessary kernels"'.
  - The later-change audit compared `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR268:PRRT_kwDOTH_vCM6TDpum

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR268:PRRT_kwDOTH_vCM6TDpum found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep pre-W9 bounded kernel claims blocked With nextaction now pointing at W9, narrowing the blocked claim to only unrestricted universality leaves a bounded universal/comm' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` (SHA-256 8c3d75177342afe3f826925affc6bcfd0fbd2b74f44f6ac1d628514f9e2ddb38).
  - Current repository evidence at `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:28`: '}'.
  - The later-change audit compared `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR26:PRRT_kwDOTH_vCM6OXzM2

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md:284`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR26:PRRT_kwDOTH_vCM6OXzM2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep FAR status docs synchronized before passing the audit This pass is used to clear the v1.0 gate, but in the repository context I inspected frameworks/FAR/methodology.m' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md` (SHA-256 4fdfa9127df940fa360d2946506d7201d27e14a516f3a95c2c777b5a146f8ecd).
  - Current repository evidence at `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md:284`: '| Methodology, workflow, and application synchronized | Pass |'.
  - The later-change audit compared `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR270:PRRT_kwDOTH_vCM6TEQDL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/research/post-w9-internal-scope-challenge-v1.0.md:1`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/research/post-w9-internal-scope-challenge-v1.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR270:PRRT_kwDOTH_vCM6TEQDL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add an explicit status to the challenge document When this new docs/research artifact is audited directly, it has no ## Status section, so the document itself does not sta' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/research/post-w9-internal-scope-challenge-v1.0.md` (SHA-256 9f35f2235676fcb2b68068a453c14e216f7b26cdbccf3c65295ec1f905b33f2f).
  - Current repository evidence at `docs/research/post-w9-internal-scope-challenge-v1.0.md:1`: '# Post-W9 Internal Scope Challenge'.
  - The later-change audit compared `docs/research/post-w9-internal-scope-challenge-v1.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR277:PRRT_kwDOTH_vCM6TGN_S

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/audits/tue-w1-unknown-boundary-audit.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/tue-w1-unknown-boundary-audit.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR277:PRRT_kwDOTH_vCM6TGN_S found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve the registered uninstrumented boundary When this W1 package is used to authorize advancing the queue to PR 278, changing the inherited creative Unknown to instrum' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/tue-w1-unknown-boundary-audit.md` (SHA-256 4cd0262ec1394f0fb5c2fbf3401f0eb40e28352f218541dc6146a38fb3202a8c).
  - Current repository evidence at `docs/audits/tue-w1-unknown-boundary-audit.md:5`: 'This audit is limited to the three Unknown boundaries inherited from SC-W6: instrumentable creative generation, tacit moral salience, and systems whose relevant reasoning distinctions remain inaccessible.'.
  - The later-change audit compared `docs/audits/tue-w1-unknown-boundary-audit.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR278:PRRT_kwDOTH_vCM6TGhkw

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_tue_w2_defeating_condition_campaign.py:34`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_tue_w2_defeating_condition_campaign.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR278:PRRT_kwDOTH_vCM6TGhkw found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require every frozen attack family to be exercised This check only proves that each defeating condition has at least one case, but the protocol freezes specific precommitt' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_tue_w2_defeating_condition_campaign.py` (SHA-256 2987e250cd22c0342d462fd7b774d7e8811d4da056b7571fe7abc1476b1e868f).
  - Current repository evidence at `tools/check_tue_w2_defeating_condition_campaign.py:34`: 'require(set(item["condition"] for item in cases) == set(conditions), "not all conditions attacked")'.
  - The later-change audit compared `tools/check_tue_w2_defeating_condition_campaign.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR279:PRRT_kwDOTH_vCM6TGrkv

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_tue_w3_deeper_kernel.py:41`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_tue_w3_deeper_kernel.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR279:PRRT_kwDOTH_vCM6TGrkv found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Handle the terminal queue state in W3 checks When PR #280 completes, the repository’s own terminal-queue contract requires status == "complete", nextaction is None, and co' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_tue_w3_deeper_kernel.py` (SHA-256 40fc44cc11d1f8d82c7914e768abc9740e39469e89dbadaa22abc421a8992724).
  - Current repository evidence at `tools/check_tue_w3_deeper_kernel.py:41`: 'require([x["target_pr"] for x in queue["completed_workstreams"]] == [276, 277, 278, 279], "completed sequence incorrect")'.
  - The later-change audit compared `tools/check_tue_w3_deeper_kernel.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR279:PRRT_kwDOTH_vCM6TGrkz

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_tue_w2_defeating_condition_campaign.py:47`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_tue_w2_defeating_condition_campaign.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR279:PRRT_kwDOTH_vCM6TGrkz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Accept completed queues in the W2 live check After PR #280, the authorized queue state has nextaction set to None, but this W2 regression check still dereferences queue["n' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_tue_w2_defeating_condition_campaign.py` (SHA-256 2987e250cd22c0342d462fd7b774d7e8811d4da056b7571fe7abc1476b1e868f).
  - Current repository evidence at `tools/check_tue_w2_defeating_condition_campaign.py:47`: 'require(queue["next_action"]["workstream"] in ("TUE-W3-DEEPER-KERNEL", "TUE-W4-FINAL-QUESTION-ANSWER"), "live queue has unauthorized workstream")'.
  - The later-change audit compared `tools/check_tue_w2_defeating_condition_campaign.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR27:PRRT_kwDOTH_vCM6OX64p

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:104`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR27:PRRT_kwDOTH_vCM6OX64p found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep the FARE expansion rule consistent This broadens the governance rule to allow new FARE definitions when FAR, FARO, or FARA requires them, but the same status document' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:104`: ''.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR27:PRRT_kwDOTH_vCM6OX64q

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md:33`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR27:PRRT_kwDOTH_vCM6OX64q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Update FAR status before freezing it This milestone designates frameworks/FAR/README.md as Stable, but that file's Current Status still says FAR is only eligible for a sta" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md` (SHA-256 f0004f462711a6722ac915273ad090ee128a4807e4ffa2ade77c8a5596b2455d).
  - Current repository evidence at `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md:33`: '- `frameworks/FAR/README.md`'.
  - The later-change audit compared `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR280:PRRT_kwDOTH_vCM6THCUb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json:13`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR280:PRRT_kwDOTH_vCM6THCUb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Clear the live TUE queue when declaring no next action This declares the terminal program closed, but the unchanged theory/evaluation/post-sc-terminal-universality-extensi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json` (SHA-256 594dfec3e11248a292f3784f906dddd9a2c577d37f8cf04c2d0985e4ad3b9ca1).
  - Current repository evidence at `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json:13`: '"next_action":null,'.
  - The later-change audit compared `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR281:PRRT_kwDOTH_vCM6THZ2F

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/research/upp-theorem-target-v1.0.md:22`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/research/upp-theorem-target-v1.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR281:PRRT_kwDOTH_vCM6THZ2F found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Bind S in the sufficiency target When later workstreams mechanize UPP-W12/W15, this sufficiency obligation leaves S free: unlike the necessity target above, it never says ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/research/upp-theorem-target-v1.0.md` (SHA-256 6a9691918e2fd575db70275dd3b8a679bb2b8cc8b78d334ec69bb4b094860b35).
  - Current repository evidence at `docs/research/upp-theorem-target-v1.0.md:22`: '```'.
  - The later-change audit compared `docs/research/upp-theorem-target-v1.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR281:PRRT_kwDOTH_vCM6THZ2G

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_post_tue_universal_proof_program.py:7`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_post_tue_universal_proof_program.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR281:PRRT_kwDOTH_vCM6THZ2G found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate the active queue checkpoint This checker only defines and loads the program artifact, so the new active queue checkpoint can drift undetected. If post-tue-univers' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_post_tue_universal_proof_program.py` (SHA-256 e8895754a871e2d7a0dece3ace97090e2216bf15aaa61b9848f4ef40cac3aa8c).
  - Current repository evidence at `tools/check_post_tue_universal_proof_program.py:7`: 'PROGRAM = ROOT / "theory/evaluation/post-tue-universal-proof-program-v1.0.json"'.
  - The later-change audit compared `tools/check_post_tue_universal_proof_program.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR282:PRRT_kwDOTH_vCM6THfYY

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/foundation/upp_foundation_v1.py:218`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/foundation/upp_foundation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate grounds references before accepting a system When a transition carries a typo or missing id in grounds, ReasoningSystem.validate() still returns success because t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/foundation/upp_foundation_v1.py` (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at `theory/foundation/upp_foundation_v1.py:218`: 'errors.append(f"transition {transition.id} references missing state")'.
  - The later-change audit compared `theory/foundation/upp_foundation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR282:PRRT_kwDOTH_vCM6THfYZ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/foundation/upp_foundation_v1.py:185`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/foundation/upp_foundation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add recovery witnesses to system validation When downstream workstreams attach recovery evidence to a reasoning system, this aggregate model has no RecoveryWitness collect' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/foundation/upp_foundation_v1.py` (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at `theory/foundation/upp_foundation_v1.py:185`: 'observations: Tuple[Observation, ...]'.
  - The later-change audit compared `theory/foundation/upp_foundation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR282:PRRT_kwDOTH_vCM6THfYd

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/foundation/upp_foundation_v1.py:171`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/foundation/upp_foundation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR282:PRRT_kwDOTH_vCM6THfYd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate parsed recovery statuses by value If a witness is hydrated from the machine-readable artifacts, status will commonly be the string "recovered" rather than a Recov' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/foundation/upp_foundation_v1.py` (SHA-256 c5da6c2130a2f8832ed68ca0b73c9719e9dcd15c65ebe0cfd3abb8efb8353a7f).
  - Current repository evidence at `theory/foundation/upp_foundation_v1.py:171`: 'if self.status is RecoveryStatus.RECOVERED and self.output_key is None:'.
  - The later-change audit compared `theory/foundation/upp_foundation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR283:PRRT_kwDOTH_vCM6TIDhg

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/class/upp_target_class_v1.py:42`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/class/upp_target_class_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR283:PRRT_kwDOTH_vCM6TIDhg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Reject the actual RCCD obligation names UPP-W1's W2 handoff says the class-neutrality audit must reject RCCD, R1-R5, their named formulations, and semantic construct loadi" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/class/upp_target_class_v1.py` (SHA-256 4bc562afd914018d488e9ab6ad347fe754785557e02d9fe8c97dcee1ab395c7c).
  - Current repository evidence at `theory/class/upp_target_class_v1.py:42`: '"historical identity", "uniform recovery", "rccd", "r1", "r2", "r3", "r4", "r5",'.
  - The later-change audit compared `theory/class/upp_target_class_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR284:PRRT_kwDOTH_vCM6TIXCy

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/contract/upp_faithfulness_contract_v1.py:44`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/contract/upp_faithfulness_contract_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR284:PRRT_kwDOTH_vCM6TIXCy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Coerce verdict values before validation When assessments are built from JSON/CLI data, verdict will be a plain string such as "pass" or "unknown". These is checks then ski' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/contract/upp_faithfulness_contract_v1.py` (SHA-256 6a6f4fbda19b7eeef6ab3086267bd85d401d06efc7f0ed14681ea6dbb087700d).
  - Current repository evidence at `theory/contract/upp_faithfulness_contract_v1.py:44`: 'if self.verdict is Verdict.UNKNOWN and not self.reason:'.
  - The later-change audit compared `theory/contract/upp_faithfulness_contract_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR284:PRRT_kwDOTH_vCM6TIXCz

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `test-infrastructure`
- Current location: `tests/test_upp_w3_contract.py:10`
- Blocks experiment reconstruction: `false`
- Root cause: `test-infrastructure:tests/test_upp_w3_contract.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR284:PRRT_kwDOTH_vCM6TIXCz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Run the W3 checker from regression tests The new deterministic checker is never invoked by this test module, unlike the W1/W2 test suites, and it is not included in the Ma' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_upp_w3_contract.py` (SHA-256 109b657ec1987a36d3f966952232eec998a1f6125a056e7ff934125a172b3c86).
  - Current repository evidence at `tests/test_upp_w3_contract.py:10`: 'class ContractTests(unittest.TestCase):'.
  - The later-change audit compared `tests/test_upp_w3_contract.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR285:PRRT_kwDOTH_vCM6TIa4M

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/representations/upp_representation_universe_v1.py:52`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/representations/upp_representation_universe_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR285:PRRT_kwDOTH_vCM6TIa4M found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Allow effectively realized oracle support For candidates that include an inventoried oracle claim, the new universe spec lists oracle as a support kind and excludes only o' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/representations/upp_representation_universe_v1.py` (SHA-256 52db7f81287f38faeb279a80593b5d03111ba25b737ba5b57d851436c41d01ff).
  - Current repository evidence at `theory/representations/upp_representation_universe_v1.py:52`: 'raise ValueError("an oracle cannot be treated as effective without a separately effective realization")'.
  - The later-change audit compared `theory/representations/upp_representation_universe_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR286:PRRT_kwDOTH_vCM6TIf5H

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/machinery/upp_machinery_closure_v1.py:41`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/machinery/upp_machinery_closure_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR286:PRRT_kwDOTH_vCM6TIf5H found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Limit effectiveness failures to required support Because validate() runs on every declared node before reachability, this check makes an otherwise closed package open when' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/machinery/upp_machinery_closure_v1.py` (SHA-256 ac2d7516ba1a41dcdbbb82fbeafb6b45667123b5dd8f4b0b85cf0bb15244f15d).
  - Current repository evidence at `theory/machinery/upp_machinery_closure_v1.py:41`: 'errors.append(f"{self.node_id}: present support must be effectively usable")'.
  - The later-change audit compared `theory/machinery/upp_machinery_closure_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR286:PRRT_kwDOTH_vCM6TIf5I

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/machinery/upp_machinery_closure_v1.py:122`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/machinery/upp_machinery_closure_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR286:PRRT_kwDOTH_vCM6TIf5I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Continue through unresolved required targets When a required disclosed edge has evidence=UNKNOWN, this continue prevents traversal into the declared target. If that target' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/machinery/upp_machinery_closure_v1.py` (SHA-256 ac2d7516ba1a41dcdbbb82fbeafb6b45667123b5dd8f4b0b85cf0bb15244f15d).
  - Current repository evidence at `theory/machinery/upp_machinery_closure_v1.py:122`: 'continue'.
  - The later-change audit compared `theory/machinery/upp_machinery_closure_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR287:PRRT_kwDOTH_vCM6TImCR

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/equivalence/upp_representation_equivalence_v1.py:47`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/equivalence/upp_representation_equivalence_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR287:PRRT_kwDOTH_vCM6TImCR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject undeclared dependency facts For a closed package where a dependency tuple mentions a fact that is absent from facts, this validation returns no error; if the corres' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/equivalence/upp_representation_equivalence_v1.py` (SHA-256 a39e929d7f4ce9b120b2b49e14c22adcc4ca0ac49a549b11a3e9fd98206d3089).
  - Current repository evidence at `theory/equivalence/upp_representation_equivalence_v1.py:47`: 'errors.append("empty_fact")'.
  - The later-change audit compared `theory/equivalence/upp_representation_equivalence_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR287:PRRT_kwDOTH_vCM6TImCU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:14`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR287:PRRT_kwDOTH_vCM6TImCU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Keep prior W5 validation reproducible Advancing nextaction to PR 288 here leaves tools/checkuppw5machineryclosure.py still requiring the queue to equal {'targetpr': 287, '" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:14`: '{"target_pr":289,"workstream":"UPP-W8-CONSTRAINED-EVOLUTION","result":"constrained_evolution_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"},'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR288:PRRT_kwDOTH_vCM6TJvkl

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/necessity/upp_recoverable_commitment_v1.py:65`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/necessity/upp_recoverable_commitment_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR288:PRRT_kwDOTH_vCM6TJvkl found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require queries to actually recover commitments When querytocommitment is empty, or when it omits a listed commitment, this all(...) check is vacuously true as long as tot' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/necessity/upp_recoverable_commitment_v1.py` (SHA-256 518ec9f77a8be98889daca5f78d05bdcb032239d562f8829cddc7e911aa42222).
  - Current repository evidence at `theory/necessity/upp_recoverable_commitment_v1.py:65`: '),'.
  - The later-change audit compared `theory/necessity/upp_recoverable_commitment_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR289:PRRT_kwDOTH_vCM6TJ0hQ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/necessity/upp_w8_constrained_evolution_v1.py:90`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/necessity/upp_w8_constrained_evolution_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR289:PRRT_kwDOTH_vCM6TJ0hQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate transition context before returning Unknown When a commitment-changing transition has admissible=Truth.UNKNOWN, these lines return UNKNOWN before the checks that ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/necessity/upp_w8_constrained_evolution_v1.py` (SHA-256 57fe6cc0c5c6ca61c7b10672bf46acdde94a8f213fea608b845e9568f4401674).
  - Current repository evidence at `theory/necessity/upp_w8_constrained_evolution_v1.py:90`: 'return Verdict.UNKNOWN'.
  - The later-change audit compared `theory/necessity/upp_w8_constrained_evolution_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR28:PRRT_kwDOTH_vCM6OYVb4

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARO/architecture.md:84`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARO/architecture.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR28:PRRT_kwDOTH_vCM6OYVb4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add the missing FARE dependency field The architecture checklist says every FARO operation shall specify these dependencies, but it skips the FARE Dependency field that op' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARO/architecture.md` (SHA-256 80e7fa3397249753b7af68b4de8667a2f29da94c1b3c9bf559d65bc1b54d91d3).
  - Current repository evidence at `frameworks/FARO/architecture.md:84`: '- boundary notes.'.
  - The later-change audit compared `frameworks/FARO/architecture.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR28:PRRT_kwDOTH_vCM6OYVb5

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARO/execution.md:40`
- Blocks experiment reconstruction: `true`
- Root cause: `frameworks:frameworks/FARO/execution.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR28:PRRT_kwDOTH_vCM6OYVb5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Clarify whether execution may determine admissibility This exception makes execution operations allowed to determine admissibility when they use a defined FAR reasoning ca' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARO/execution.md` (SHA-256 d843f934cf1896a5c4907e02130acc29a670d109aa8ec4287ad70cd29037167b).
  - Current repository evidence at `frameworks/FARO/execution.md:40`: '- determine admissibility unless explicitly acting under a defined FAR reasoning calculus.'.
  - The later-change audit compared `frameworks/FARO/execution.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR290:PRRT_kwDOTH_vCM6TJ7wQ

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:17`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR290:PRRT_kwDOTH_vCM6TJ7wQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the queue on the registered W10 workstream For the post-W9 state, this advances PR 291 to UPP-W10-SEMANTIC-INTERPRETATION, but the registered universal-proof program ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:17`: '{"target_pr":292,"workstream":"UPP-W11-HISTORICAL-TRACE","result":"historical_trace_necessity_lemma_established_relative_to_frozen_class_contract_representation_closure_and_equivalence"},'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR290:PRRT_kwDOTH_vCM6TJ7wS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/foundation/upp_dependency_structure_v1.py:74`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/foundation/upp_dependency_structure_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR290:PRRT_kwDOTH_vCM6TJ7wS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject duplicate relations before proving the witness When an assessment contains two edges with different edgeids but the same source, target, kind, and temporal scope, t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/foundation/upp_dependency_structure_v1.py` (SHA-256 f258c9dd5f5a7c1d097137ea3e31a87bd3004a4d34c9b6e72d4fd85cf2c7bb25).
  - Current repository evidence at `theory/foundation/upp_dependency_structure_v1.py:74`: 'edge_ids.add(edge.edge_id)'.
  - The later-change audit compared `theory/foundation/upp_dependency_structure_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR291:PRRT_kwDOTH_vCM6TKCL7

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:18`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR291:PRRT_kwDOTH_vCM6TKCL7 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the UPP queue on the registered workstream theory/evaluation/post-tue-universal-proof-program-v1.0.json still registers PR 292 as UPP-W11-R5 for uniform-effective-rec' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:18`: '{"target_pr":293,"workstream":"UPP-W12-COMPONENT-INDEPENDENCE","result":"five_component_relative_independence_established_by_separating_witnesses_and_anti_reduction_controls"},'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR291:PRRT_kwDOTH_vCM6TKCL8

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/foundation/upp_semantic_interpretation_v1.py:126`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/foundation/upp_semantic_interpretation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR291:PRRT_kwDOTH_vCM6TKCL8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require coverage of registered semantic items When all premises are yes, this returns PROVED for any non-empty consistent mapping, but SemanticAssessment only contains the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/foundation/upp_semantic_interpretation_v1.py` (SHA-256 0b5ce68c2a374d0c0efe5bd47e8a6dd0b6e28bacef958c63f9724643eecf7adb).
  - Current repository evidence at `theory/foundation/upp_semantic_interpretation_v1.py:126`: 'return Verdict.PROVED if function else Verdict.UNKNOWN'.
  - The later-change audit compared `theory/foundation/upp_semantic_interpretation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR292:PRRT_kwDOTH_vCM6TKJk3

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/history/upp_historical_trace_v1.py:94`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/history/upp_historical_trace_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR292:PRRT_kwDOTH_vCM6TKJk3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate dependency and reason links chronologically When a trace uses dependencyids or reasonids that point to later events, this loop ignores those references, so obliga' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/history/upp_historical_trace_v1.py` (SHA-256 c0a5f3977476d40c25a9f16a43b8ccb9ed725cee66b04211223e2bf97f4f0672).
  - Current repository evidence at `theory/history/upp_historical_trace_v1.py:94`: 'for predecessor in event.predecessor_ids | event.supersedes_ids:'.
  - The later-change audit compared `theory/history/upp_historical_trace_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR292:PRRT_kwDOTH_vCM6TKJkz

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:19`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR292:PRRT_kwDOTH_vCM6TKJkz found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep PR #293 aligned with registered sufficiency workstream The registered UPP plan assigns target PR 293 to UPP-W12-SUFFICIENCY and puts component independence/irreducibi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:19`: '{"target_pr":294,"workstream":"UPP-W13-SUFFICIENCY-CONSTRUCTION","result":"relative_rccd_sufficiency_established_by_effective_compositional_construction_and_bidirectional_reconstruction"},'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR293:PRRT_kwDOTH_vCM6TKVUC

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/independence/upp_component_independence_v1.py:53`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/independence/upp_component_independence_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR293:PRRT_kwDOTH_vCM6TKVUC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject unregistered reduction sources When a proposed reduction names a source outside the five registered components, this guard still allows it through; for example Redu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/independence/upp_component_independence_v1.py` (SHA-256 40ed8fb5cf5ee9e1c37b2559694393cb7c642d1de99e0c2ab6f67723901b0c57).
  - Current repository evidence at `theory/independence/upp_component_independence_v1.py:53`: 'return Verdict.REFUTED'.
  - The later-change audit compared `theory/independence/upp_component_independence_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR293:PRRT_kwDOTH_vCM6TKVUH

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_upp_w11_historical_trace.py:94`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_upp_w11_historical_trace.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR293:PRRT_kwDOTH_vCM6TKVUH found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Handle terminal queues in the W11 checker This checker is still invoked by tests/testuppw11historicaltrace.py, but the new forward-progress logic assumes nextaction is alw' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_upp_w11_historical_trace.py` (SHA-256 ea2a822f85141863f26765c52710fca3338198ab1a50be1c11bb8b045c55e62c).
  - Current repository evidence at `tools/check_upp_w11_historical_trace.py:94`: 'next_pr = next_action.get("target_pr")'.
  - The later-change audit compared `tools/check_upp_w11_historical_trace.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR294:PRRT_kwDOTH_vCM6TKdMI

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:21`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR294:PRRT_kwDOTH_vCM6TKdMI found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Point the queue at the registered PR #295 workstream When a runner follows this active queue, it is sent to UPP-W14-IRREDUCIBILITY-MAXIMALITY, but the registered universal' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:21`: '{"target_pr":296,"workstream":"UPP-W15-TERMINAL-THEOREM","result":"strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary"}'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR295:PRRT_kwDOTH_vCM6TLOM-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/irreducibility/upp-irreducibility-maximality-v1.0.json:8`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/irreducibility/upp-irreducibility-maximality-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLOM- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Point to an accepted irreducibility result This metadata names UPP-W13-IRREDUCIBILITY as the supporting prior result, but the completed PR #294 artifact is UPP-W13-SUFFICI' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/irreducibility/upp-irreducibility-maximality-v1.0.json` (SHA-256 26d408754095692101f404fb1c1b2cff4f5a9bf9c640583f6e3c4c628f01e578).
  - Current repository evidence at `theory/irreducibility/upp-irreducibility-maximality-v1.0.json:8`: '"supporting_prior_result":"UPP-W13-IRREDUCIBILITY",'.
  - The later-change audit compared `theory/irreducibility/upp-irreducibility-maximality-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR295:PRRT_kwDOTH_vCM6TLONF

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json:28`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLONF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep the W13 audit in sync with the successor Changing the W13 successor here to UPP-W14-MAXIMALITY leaves the W13 audit saying completion advances to UPP-W14-IRREDUCIBILI' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json` (SHA-256 be187c6ef8bbdc30b15a0b8a09d35849a2b355cc07034dad635fa15d86ba1d95).
  - Current repository evidence at `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json:28`: '"next_workstream": {"target_pr": 295, "workstream": "UPP-W14-MAXIMALITY"},'.
  - The later-change audit compared `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR295:PRRT_kwDOTH_vCM6TLONJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/irreducibility/upp_irreducibility_maximality_v1.py:117`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/irreducibility/upp_irreducibility_maximality_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR295:PRRT_kwDOTH_vCM6TLONJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Classify excluded challenges before checking embeddings When a registered challenge is already excluded from the target class and records embedsinrccd=None as not applicab' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/irreducibility/upp_irreducibility_maximality_v1.py` (SHA-256 4dde1eb64f04525fafc1c633fa0ca44f7b5552969e656da50e3ff86e2ad858aa).
  - Current repository evidence at `theory/irreducibility/upp_irreducibility_maximality_v1.py:117`: 'return Verdict.UNKNOWN'.
  - The later-change audit compared `theory/irreducibility/upp_irreducibility_maximality_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR296:PRRT_kwDOTH_vCM6TK9sE

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `canonical-theory`
- Current location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:26`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TK9sE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep historical UPP checkers compatible with terminal closure With this checkpoint now terminal (nextaction: null and the public gate open), the existing W1-W11 validation' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` (SHA-256 26429a1751adbed33db25d7ac2bef82b9f3373dcab2ba8ecd7c5cf82ba89e8ed).
  - Current repository evidence at `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:26`: '"public_evaluation_authorized":false,'.
  - The later-change audit compared `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR296:PRRT_kwDOTH_vCM6TK9sG

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/terminal/upp_terminal_theorem_v1.py:75`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/terminal/upp_terminal_theorem_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TK9sG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Honor blocked-dependency precedence before defeating overclaims For evidence that both contains an unresolved or absent required property and sets an overclaim flag, this ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/terminal/upp_terminal_theorem_v1.py` (SHA-256 94f1909a48aa55452ac813832f1699b90f0e9e9fdfe92b3c7ea2ac47057e5a17).
  - Current repository evidence at `theory/terminal/upp_terminal_theorem_v1.py:75`: 'return Adjudication(Verdict.UNKNOWN, Outcome.BLOCKED, ("proof_standard_not_satisfied",), False)'.
  - The later-change audit compared `theory/terminal/upp_terminal_theorem_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR296:PRRT_kwDOTH_vCM6TLCCD

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/terminal/upp_terminal_theorem_v1.py:87`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/terminal/upp_terminal_theorem_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR296:PRRT_kwDOTH_vCM6TLCCD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Block full proof when terminal composition is absent When evidence has centralsemantictheoremkernelchecked=True but executablecompositionverified=False, this early return ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/terminal/upp_terminal_theorem_v1.py` (SHA-256 94f1909a48aa55452ac813832f1699b90f0e9e9fdfe92b3c7ea2ac47057e5a17).
  - Current repository evidence at `theory/terminal/upp_terminal_theorem_v1.py:87`: 'return Adjudication(Verdict.PROVED, Outcome.FULL, ("all_registered_properties_and_kernel_checked_terminal_theorem",), True)'.
  - The later-change audit compared `theory/terminal/upp_terminal_theorem_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR297:PRRT_kwDOTH_vCM6TRTNk

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post_terminal_public_evaluation_v1.py:40`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post_terminal_public_evaluation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR297:PRRT_kwDOTH_vCM6TRTNk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use registry prohibited-promotion tokens When a submission uses the identifiers published by theory/evaluation/post-terminal-public-evaluation-program-v1.0.json, several b' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post_terminal_public_evaluation_v1.py` (SHA-256 3ff34a0a540ac1174de609a609d22837b4d7bf45a8612f8cb9f412fc104e9d77).
  - Current repository evidence at `theory/evaluation/post_terminal_public_evaluation_v1.py:40`: '"internal_as_independent_replication",'.
  - The later-change audit compared `theory/evaluation/post_terminal_public_evaluation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR297:PRRT_kwDOTH_vCM6TRTNr

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/post_terminal_public_evaluation_v1.py:47`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/post_terminal_public_evaluation_v1.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR297:PRRT_kwDOTH_vCM6TRTNr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject unsupported evidence types The adjudicator stores evidencetype but never checks it against the registered evidence-type vocabulary, so a submission with evidencetyp' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/post_terminal_public_evaluation_v1.py` (SHA-256 3ff34a0a540ac1174de609a609d22837b4d7bf45a8612f8cb9f412fc104e9d77).
  - Current repository evidence at `theory/evaluation/post_terminal_public_evaluation_v1.py:47`: 'evidence_type: str'.
  - The later-change audit compared `theory/evaluation/post_terminal_public_evaluation_v1.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR29:PRRT_kwDOTH_vCM6OYXwk

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:11`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR29:PRRT_kwDOTH_vCM6OYXwk found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update FARO README status for Phase 8 When this status document moves active development to Phase 8, frameworks/FARO/README.md still says FARO has entered Phase 7 architec' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:11`: 'The frozen comparison is complete: v1.0.0 resolved 0/2 runs and v1.0.1 resolved 0/2 runs on the single preregistered task. The observation is `no_observed_resolution_difference`; both the outcome-blind integrity decision and bounded case de'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR306:PRRT_kwDOTH_vCM6TVtkK

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:96`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/model.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR306:PRRT_kwDOTH_vCM6TVtkK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require explicit unknown and authorization fields When a package omits authorizationrequirements or unknowns, these defaults silently coerce the absence to an empty tuple,' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/model.py` (SHA-256 f25f9e8cd0bf1528f65104c2fff166dafcf97cf1d18e484b18dfc824144e9c46).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/model.py:96`: 'trace_completeness=_bounded_number('.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/model.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR307:PRRT_kwDOTH_vCM6TVt_a

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:28`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR307:PRRT_kwDOTH_vCM6TVt_a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require an authorizing edge for authorization requirements When a required authorization node has any edge into the decision root, this treats the requirement as satisfied' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py` (SHA-256 98cdc768e66c458956e73663258d1def15685818a17147865b7108166115c948).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:28`: 'if dependency.target_id == package.decision_root'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR309:PRRT_kwDOTH_vCM6TV50T

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:23`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/cli.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR309:PRRT_kwDOTH_vCM6TV50T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep the legacy audit CLI path working When existing callers invoke far-decision [--output ...], the new subparser treats the package path as an invalid command before the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/cli.py` (SHA-256 f58175d95816402404064510efac2c38006e0945119b7b6d924d204588c6f033).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:23`: 'args = parser.parse_args(argv)'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/cli.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR30:PRRT_kwDOTH_vCM6OYbcS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md:77`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR30:PRRT_kwDOTH_vCM6OYbcS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Rework the failure-mode pass before advancing Phase 8 This pass result is not supported by the referenced category documents: in frameworks/FARO/{execution,reporting,opera' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md` (SHA-256 5460573bb377df8df4f1f14f091e3fbbfd689c3500530eaa60a545117d88f6b5).
  - Current repository evidence at `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md:77`: 'Auditing, reporting, execution, and operational evaluation documents distinguish incomplete, invalid, missing-input, and boundary-related failures at the category level.'.
  - The later-change audit compared `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR311:PRRT_kwDOTH_vCM6TWLBi

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:35`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/cli.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR311:PRRT_kwDOTH_vCM6TWLBi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restore legacy audit path for console invocations When far-decision is invoked through the installed console script, main() is called with argv=None, so arguments stays No' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/cli.py` (SHA-256 f58175d95816402404064510efac2c38006e0945119b7b6d924d204588c6f033).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:35`: 'if __name__ == "__main__":'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/cli.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR311:PRRT_kwDOTH_vCM6TWLBm

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/regression.py:26`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/regression.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR311:PRRT_kwDOTH_vCM6TWLBm found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject non-object run entries as invalid input If a supplied regression suite contains a non-object entry inside baseline or candidate (for example null), this subscript r' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/regression.py` (SHA-256 fda240cf1a245b3b51f6f5795ee59ab8e57517fdb474244d38d601a7ac7ce5b7).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/regression.py:26`: 'raise ValueError("run result must be an object")'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/regression.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR31:PRRT_kwDOTH_vCM6OYchc

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md:135`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR31:PRRT_kwDOTH_vCM6OYchc found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep the audit-record gate in the criteria When the stable milestone relies on this Phase 9 finding, it now claims the criteria document records the required audit records' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md` (SHA-256 439282fac9e38bbbe7a4735960faae8068e0556e42cc283d34d6b89c1de0da26).
  - Current repository evidence at `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md:135`: 'The criteria document records the required architecture, operation categories, interfaces, boundaries, and audit records.'.
  - The later-change audit compared `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR324:PRRT_kwDOTH_vCM6TZUi3

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_universality_remainder_theorem.py:107`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_universality_remainder_theorem.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR324:PRRT_kwDOTH_vCM6TZUi3 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate the completed-work ledger exactly When a frozen completed-work item is removed or renamed but the list is padded back to 15 entries, validateregistry still return' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_universality_remainder_theorem.py` (SHA-256 ecf3cbabda707a62dc06811b97158c19f388b150d8f3a6c69fb3188bd0e46b43).
  - Current repository evidence at `tools/check_universality_remainder_theorem.py:107`: 'errors.append("completed-work nonredundancy ledger is incomplete")'.
  - The later-change audit compared `tools/check_universality_remainder_theorem.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR32:PRRT_kwDOTH_vCM6OYfSA

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `repository-metadata`
- Current location: `README.md:13`
- Blocks experiment reconstruction: `false`
- Root cause: `repository-metadata:README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR32:PRRT_kwDOTH_vCM6OYfSA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update canonical FARO status before declaring stability This declaration conflicts with unchanged canonical FARO docs: frameworks/FARO/README.md:13-15 still says FARO is o' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `README.md` (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at `README.md:13`: ''.
  - The later-change audit compared `README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR333:PRRT_kwDOTH_vCM6TbDy4

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/architecture/repository-convergence-2026-07-23.md:4`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/architecture/repository-convergence-2026-07-23.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR333:PRRT_kwDOTH_vCM6TbDy4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use charter-defined artifact statuses This new audit is introduced with Status: execution baseline, and the companion convergence documents use similarly descriptive statu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/architecture/repository-convergence-2026-07-23.md` (SHA-256 dff4315d49cc32bd3853bc46ed4dd070d8bc73c1e1bc68f81493e75ed282914e).
  - Current repository evidence at `docs/architecture/repository-convergence-2026-07-23.md:4`: 'Status: execution baseline'.
  - The later-change audit compared `docs/architecture/repository-convergence-2026-07-23.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR335:PRRT_kwDOTH_vCM6TbKCT

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:29`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR335:PRRT_kwDOTH_vCM6TbKCT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Don't count contradictory edges as authorization support When a producer records a required node's edge to the root as contradicts (or another non-supporting relation), th" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py` (SHA-256 98cdc768e66c458956e73663258d1def15685818a17147865b7108166115c948).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:29`: '}'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR335:PRRT_kwDOTH_vCM6TbKCX

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:124`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/model.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR335:PRRT_kwDOTH_vCM6TbKCX found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject cyclic dependency graphs before adjudication For packages with two-node or longer cycles, such as auth -> root and root -> auth, this validator accepts the graph be' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/model.py` (SHA-256 f25f9e8cd0bf1528f65104c2fff166dafcf97cf1d18e484b18dfc824144e9c46).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/model.py:124`: 'raise PackageValidationError("self-dependencies are not permitted")'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/model.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR336:PRRT_kwDOTH_vCM6TbQvA

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py:74`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/evidence.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR336:PRRT_kwDOTH_vCM6TbQvA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Verify hashed evidence sources before accepting bundles When a generated bundle is verified after the referenced regression suite is edited or removed, this still returns ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py` (SHA-256 04aceb87bdd17e94524cc6ae5a996ee575ad7220d580f3ce65ad6e22e830925e).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py:74`: 'return sha256_bytes(report_path.read_bytes()) == report.get("sha256")'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR337:PRRT_kwDOTH_vCM6TbmOr

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py:25`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR337:PRRT_kwDOTH_vCM6TbmOr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve observation records from SWE-agent trajectories When the input is a current SWE-agent trajectory that stores tool output as {"messagetype":"observation","content"' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py` (SHA-256 0d604804905a7dab36e904906027445040906a548ff90e176e6dd486a7836c8d).
  - Current repository evidence at `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py:25`: 'observation = record.get("observation") or record.get("result") or record.get("output")'.
  - The later-change audit compared `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR33:PRRT_kwDOTH_vCM6OYgsA

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:64`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR33:PRRT_kwDOTH_vCM6OYgsA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not let unproven FARM drive FARE expansion While the Phase 10 audit still has to decide whether FARM should exist and the milestone says FARM must prove responsibilitie' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:64`: ''.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR340:PRRT_kwDOTH_vCM6Tb8P_

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `research-records`
- Current location: `research/external-validation/trace-candidate-002/protocol.json:4`
- Blocks experiment reconstruction: `true`
- Root cause: `research-records:research/external-validation/trace-candidate-002/protocol.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR340:PRRT_kwDOTH_vCM6Tb8P_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add a charter status to the frozen protocol This status records the execution phase, but the new protocol still lacks one of the charter artifact statuses (Accepted, Resea' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `research/external-validation/trace-candidate-002/protocol.json` (SHA-256 607e35f12bd36270dd143fb188f9d3ae2264c7a6ac0f9a3e7f407b62698ae0ec).
  - Current repository evidence at `research/external-validation/trace-candidate-002/protocol.json:4`: '"status": "frozen-before-outcome-inspection",'.
  - The later-change audit compared `research/external-validation/trace-candidate-002/protocol.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR344:PRRT_kwDOTH_vCM6TcTFp

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/1-0-golden-clean-install.yml:54`
- Blocks experiment reconstruction: `false`
- Root cause: `ci-and-automation:.github/workflows/1-0-golden-clean-install.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR344:PRRT_kwDOTH_vCM6TcTFp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Run the golden tests against the installed wheel This step uses the checkout's default python, and the package tests prepend commercial/far-decision-integrity/src to sys.p" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/1-0-golden-clean-install.yml` (SHA-256 11d4de2470c4e96c1f2fda0ad365763198fc46e5da2436360991ae282cc41e7e).
  - Current repository evidence at `.github/workflows/1-0-golden-clean-install.yml:54`: 'run: python -m unittest discover -s commercial/far-decision-integrity/tests -p "test_*.py"'.
  - The later-change audit compared `.github/workflows/1-0-golden-clean-install.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR344:PRRT_kwDOTH_vCM6TcTFr

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/releases/1.0.0-draft.md:7`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/releases/1.0.0-draft.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR344:PRRT_kwDOTH_vCM6TcTFr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Attach provenance to the cumulative release narrative This new draft immediately summarizes a long 0.4.0→1.0.0 development path and the following sections list research, g' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/releases/1.0.0-draft.md` (SHA-256 15891cfb5e1d22ff9547080564979cccd904795652c85393e4da440c067ce9fd).
  - Current repository evidence at `docs/releases/1.0.0-draft.md:7`: 'Project FAR moved from an early formal-vocabulary research repository into a consolidated research and verification system with explicit claim boundaries, mechanized validation, deterministic decision adjudication, external-trace ingestion,'.
  - The later-change audit compared `docs/releases/1.0.0-draft.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR347:PRRT_kwDOTH_vCM6TcnkK

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:197`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR347:PRRT_kwDOTH_vCM6TcnkK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Escape uploaded values before rendering findings When a user analyzes an uploaded trace whose action contains HTML, that value is copied into finding descriptions and then' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:197`: 'baseline_adjudication.status.value,'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR347:PRRT_kwDOTH_vCM6TcnkO

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:27`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR347:PRRT_kwDOTH_vCM6TcnkO found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate event objects before parsing fields If an uploaded JSON file has an events array containing any non-object value, parse passes it into event and this .get call ra' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:27`: ''.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR348:PRRT_kwDOTH_vCM6Tc-2A

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:210`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR348:PRRT_kwDOTH_vCM6Tc-2A found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Download the analyzed artifact instead of the sample When a user verifies custom packages through runUpload(), the rendered status/changes come from /api/analyze, but this' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:210`: '"candidate": {'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR348:PRRT_kwDOTH_vCM6Tc-2B

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:210`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR348:PRRT_kwDOTH_vCM6Tc-2B found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Render uploaded evidence in the comparison panel For custom uploads, runUpload() updates only the verdict card from /api/analyze, while this side-by-side “Execution compar' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:210`: '"candidate": {'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR350:PRRT_kwDOTH_vCM6Tdsan

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:130`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR350:PRRT_kwDOTH_vCM6Tdsan found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep upload summaries evidence-bound When /api/analyze is used for any package other than the bundled refund sample—e.g. a justified package or an unsupported non-refund d' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:130`: 'structural_changes.append('.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR350:PRRT_kwDOTH_vCM6Tdsas

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:251`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR350:PRRT_kwDOTH_vCM6Tdsas found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Render the actual returned status When the upload flow analyzes a package whose returned status is justified, unverifiable, or underdetermined, this hard-coded label remai' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:251`: '"unknowns": [],'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR351:PRRT_kwDOTH_vCM6TeaVq

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:130`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR351:PRRT_kwDOTH_vCM6TeaVq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep upload summaries evidence-bound Because present() also builds the response for /api/analyze, these hard-coded refund-specific fields are returned after users upload a' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:130`: 'structural_changes.append('.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR353:PRRT_kwDOTH_vCM6TfYV2

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/formats.py:129`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/formats.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR353:PRRT_kwDOTH_vCM6TfYV2 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject XML packages that omit trace completeness For an XML upload that omits tracecompleteness, this line silently inserts 0 before the package reaches DecisionPackage.fr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/formats.py` (SHA-256 245cfde121dbdd9d9e78fd0841ddaa862948912a22d9f7b84f3c75f60fe50726).
  - Current repository evidence at `commercial/far-demo/src/far_demo/formats.py:129`: 'payload["trace_completeness"] = float(payload.get("trace_completeness", 0))'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/formats.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR353:PRRT_kwDOTH_vCM6TfYVy

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:297`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR353:PRRT_kwDOTH_vCM6TfYVy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Wrap parser errors for supported uploads When either upload is a malformed newly supported format, parsepackagefile() can now raise parser-specific exceptions such as yaml' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:297`: 'def example_report() -> Response:'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR354:PRRT_kwDOTH_vCM6Tfu7K

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/app.py:170`
- Blocks experiment reconstruction: `false`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR354:PRRT_kwDOTH_vCM6Tfu7K found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Don't pass releases that remove recorded support When a candidate removes a baseline decision-root dependency that is not in authorizationrequirements, present() still emi" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/app.py` (SHA-256 5b89fa6370c9ece689d60070530cba1188fb84ac0ce1d6794bd6cd60b35a1edd).
  - Current repository evidence at `commercial/far-demo/src/far_demo/app.py:170`: '}[status]'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR355:PRRT_kwDOTH_vCM6Tm8c9

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `commercial-validation`
- Current location: `commercial/far-demo/src/far_demo/validation_app.py:123`
- Blocks experiment reconstruction: `true`
- Root cause: `commercial-validation:commercial/far-demo/src/far_demo/validation_app.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR355:PRRT_kwDOTH_vCM6Tm8c9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Configure feedback logging before returning recorded When the Render deployment starts uvicorn fardemo.validationapp:app, this custom far.validation logger is never config' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-demo/src/far_demo/validation_app.py` (SHA-256 76323b225c44d90c0155deb96e1f08307220b618e999ff9ee84da3e64ff40441).
  - Current repository evidence at `commercial/far-demo/src/far_demo/validation_app.py:123`: 'logger.info("far_validation_feedback %s", canonical)'.
  - The later-change audit compared `commercial/far-demo/src/far_demo/validation_app.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR356:PRRT_kwDOTH_vCM6Tm9zN

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:76`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR356:PRRT_kwDOTH_vCM6Tm9zN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject pre-freeze outcome fields When a pre-freeze manifest gains an outcome field, for example after execution but before the primary hash freeze someone adds {"leakedout' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py` (SHA-256 e1f41e94ef45ccb92650ca5eef578a6430e294082fe239a666b5461cf0aca080).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:76`: '"same_task", "same_model", "same_model_parameters", "same_agent_configuration",'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR357:PRRT_kwDOTH_vCM6Tnjoh

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml:10`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR357:PRRT_kwDOTH_vCM6Tnjoh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Make the frozen SWE-agent config loadable When the four runs follow runcomparison.py’s instruction to use this file, SWE-agent v1.0 will reject this old-style agent.config' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml` (SHA-256 d979eca3fa22afdff57c2894698018649ef94b7c6199ec253f976f2f3f852654).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml:10`: 'retry:'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR357:PRRT_kwDOTH_vCM6Tnjol

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:68`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR357:PRRT_kwDOTH_vCM6Tnjol found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate every frozen model parameter With the validator only checking temperature and reasoningeffort, later edits can change or remove frozen fields like topp, perinstan' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py` (SHA-256 e1f41e94ef45ccb92650ca5eef578a6430e294082fe239a666b5461cf0aca080).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:68`: '"baseline_commit": "8ed382c",'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR359:PRRT_kwDOTH_vCM6Too8m

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:68`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR359:PRRT_kwDOTH_vCM6Too8m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Parse the verbose manifest digest When the fallback is used for a normal single-image manifest, Docker's verbose output exposes the registry digest as a top-level Digest f" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py` (SHA-256 eb56a0a73dcdf1b5bae7326f8d00b8d990cb9f2695c75fd9e9d5b460f4948929).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:68`: ')'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR35:PRRT_kwDOTH_vCM6OYx2-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `frameworks`
- Current location: `frameworks/FARM/README.md:31`
- Blocks experiment reconstruction: `false`
- Root cause: `frameworks:frameworks/FARM/README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR35:PRRT_kwDOTH_vCM6OYx2- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add FARM canonical documents to the canonical map These new FARM files are now presented as canonical documents, but docs/CANONICALMAP.md still has no FARM section or entr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `frameworks/FARM/README.md` (SHA-256 be455ae44fc227c89317c3dffce2f6cc193d6c0dd8f8148cc426a3939c598f30).
  - Current repository evidence at `frameworks/FARM/README.md:31`: '---'.
  - The later-change audit compared `frameworks/FARM/README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR360:PRRT_kwDOTH_vCM6To5d1

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py:73`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Use the SWE-bench installreposcript property In the pinned SWE-bench harness, TestSpec exposes the repository setup script as installreposcript (the image builder writes t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py` (SHA-256 cfb53f6d3bc83232efe019eb5967b2f85b494e2db4a600edd04a2267e669b767).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py:73`: 'text=True,'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR360:PRRT_kwDOTH_vCM6To5d6

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:40`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Verify the local image before accepting the lock For preflight or plan on a fresh GitHub-hosted runner, comparing the committed JSON localimageid to the manifest only prov' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py` (SHA-256 eb56a0a73dcdf1b5bae7326f8d00b8d990cb9f2695c75fd9e9d5b460f4948929).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:40`: 'if lock.get("local_image_id") != frozen["local_image_id"]:'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR360:PRRT_kwDOTH_vCM6To5d8

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/far-swe-agent-execution.yml:11`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/far-swe-agent-execution.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR360:PRRT_kwDOTH_vCM6To5d8 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Update the documented stage name with the workflow rename After this dispatch option is renamed, the setup guide still describes the available stages as resolve-image, pre' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/far-swe-agent-execution.yml` (SHA-256 59e8d37483ac0eaa48dcdb1acfd7b8017906e9e7818210a123f869fa5d10092a).
  - Current repository evidence at `.github/workflows/far-swe-agent-execution.yml:11`: '- prepare-environment'.
  - The later-change audit compared `.github/workflows/far-swe-agent-execution.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR367:PRRT_kwDOTH_vCM6TtX1k

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:183`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1k found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Run trajectories through the registered FAR adapter The comparison reduces each trajectory to scalar, mapping, and list counts, so even a normal completed run produces no ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:183`: '},'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR367:PRRT_kwDOTH_vCM6TtX1m

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:194`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Block primary regeneration after outcome reveal If an operator dispatches freeze-primary after reveal-outcomes, the workflow restores the latest postprocess artifact—inclu' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:194`: 'paths = compile_primary()'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR367:PRRT_kwDOTH_vCM6TtX1o

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:222`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1o found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require the complete primary artifact set When primary-freeze.json is tampered with or restored from an incompatible artifact, a manifest containing artifactcount: 0, arti' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` (SHA-256 1c79c7ec79a3543f89dabf5576c891855fbdc6ccf55fe34b69ff2852b56c8a13).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:222`: 'raise SystemExit("Primary freeze artifact count mismatch")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR367:PRRT_kwDOTH_vCM6TtX1q

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `ci-and-automation`
- Current location: `.github/workflows/validator-assurance.yml:111`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/validator-assurance.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR367:PRRT_kwDOTH_vCM6TtX1q found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Retain independent provenance for the cache bundle The checksum and the cache bundle are generated by the same producer and uploaded in the same artifact, so a substituted' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/validator-assurance.yml` (SHA-256 02fd5b0e92615a85e8dc0d68a62ba19c440bc0fd47eb761798f6a16afbf498d1).
  - Current repository evidence at `.github/workflows/validator-assurance.yml:111`: 'run: sha256sum -c signed-cache.tar.gz.sha256'.
  - The later-change audit compared `.github/workflows/validator-assurance.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR369:PRRT_kwDOTH_vCM6Ttjrd

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `mechanization`
- Current location: `mechanization/far_mechanization/compare_adjudication.py:357`
- Blocks experiment reconstruction: `false`
- Root cause: `mechanization:mechanization/far_mechanization/compare_adjudication.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrd found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Bind findings to referenced package contents When adjudicate receives a comparison from an untrusted or corrupted producer, these embedded claims are normalized but never ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/far_mechanization/compare_adjudication.py` (SHA-256 283353eb65da96f80ae88f5299e41436c970f044f13a3d6de6ba09384faa4f2b).
  - Current repository evidence at `mechanization/far_mechanization/compare_adjudication.py:357`: 'right_claim = None if finding["right"] is None else _normalize_claim(finding["right"], f"{path}.right")'.
  - The later-change audit compared `mechanization/far_mechanization/compare_adjudication.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR369:PRRT_kwDOTH_vCM6Ttjrh

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `mechanization`
- Current location: `mechanization/far_mechanization/compare_adjudication.py:160`
- Blocks experiment reconstruction: `false`
- Root cause: `mechanization:mechanization/far_mechanization/compare_adjudication.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Reject non-finite metadata values When package or adjudication metadata contains NaN, Infinity, or -Infinity, Python's permissive json.loads produces a float and this chec" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `mechanization/far_mechanization/compare_adjudication.py` (SHA-256 283353eb65da96f80ae88f5299e41436c970f044f13a3d6de6ba09384faa4f2b).
  - Current repository evidence at `mechanization/far_mechanization/compare_adjudication.py:160`: 'raise InterfaceError(f"{path}.{key} must be a JSON scalar")'.
  - The later-change audit compared `mechanization/far_mechanization/compare_adjudication.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR369:PRRT_kwDOTH_vCM6Ttjrj

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `repository-metadata`
- Current location: `schemas/far-evidence-comparison-v1.schema.json:26`
- Blocks experiment reconstruction: `false`
- Root cause: `repository-metadata:schemas/far-evidence-comparison-v1.schema.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR369:PRRT_kwDOTH_vCM6Ttjrj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate embedded claims in the comparison schema When consumers validate comparison artifacts using the published JSON Schema rather than the Python CLI, left and right a' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `schemas/far-evidence-comparison-v1.schema.json` (SHA-256 95243bfa7e5514f96d38afc777d5ac562afaa506217321995da4f548a746cd44).
  - Current repository evidence at `schemas/far-evidence-comparison-v1.schema.json:26`: '"right": {"type": ["object", "null"]},'.
  - The later-change audit compared `schemas/far-evidence-comparison-v1.schema.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR36:PRRT_kwDOTH_vCM6OZFPU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:11`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR36:PRRT_kwDOTH_vCM6OZFPU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Sync the FARM README before closing Phase 4 With this update, project status says Phase 3 and Phase 4 are complete, but frameworks/FARM/README.md still says the Phase 3 me' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:11`: 'The frozen comparison is complete: v1.0.0 resolved 0/2 runs and v1.0.1 resolved 0/2 runs on the single preregistered task. The observation is `no_observed_resolution_difference`; both the outcome-blind integrity decision and bounded case de'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR371:PRRT_kwDOTH_vCM6TuK-l

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_repository_truth.py:36`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_repository_truth.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR371:PRRT_kwDOTH_vCM6TuK-l found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Make the checker enforce the manifest authorities When an authority or mirror entry in repository-truth-authority-v1.json changes, this checker validates only the schema s' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_repository_truth.py` (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at `tools/check_repository_truth.py:36`: 'fail("unsupported or missing authority schema")'.
  - The later-change audit compared `tools/check_repository_truth.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR371:PRRT_kwDOTH_vCM6TuK-m

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/governance/repository-truth-revalidation-scope.md:28`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/governance/repository-truth-revalidation-scope.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR371:PRRT_kwDOTH_vCM6TuK-m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Complete the authority inventory before resolving the audit These required categories are absent from both the machine-readable manifest and the audit's authoritative inve" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/governance/repository-truth-revalidation-scope.md` (SHA-256 9c489414865bbf61006f78edb0e6c94780f01d3295f30116ef1f4d286e75f27a).
  - Current repository evidence at `docs/governance/repository-truth-revalidation-scope.md:28`: '- generated or frozen artifacts that embed versions or status;'.
  - The later-change audit compared `docs/governance/repository-truth-revalidation-scope.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR373:PRRT_kwDOTH_vCM6TuR8N

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/releases/project-far-v1.0.0.md:3`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/releases/project-far-v1.0.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8N found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Assign the release record an allowed status Assign this newly introduced canonical artifact exactly one of the charter’s permitted statuses—Accepted, Research, Provisional' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/releases/project-far-v1.0.0.md` (SHA-256 2de11d4186ddf500ba48b9381d9fbdeb545e00be3368a304c1c53be6f19fa7b0).
  - Current repository evidence at `docs/releases/project-far-v1.0.0.md:3`: 'This file records the current published repository release authority.'.
  - The later-change audit compared `docs/releases/project-far-v1.0.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR373:PRRT_kwDOTH_vCM6TuR8O

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_repository_truth.py:66`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_repository_truth.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8O found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate the README release target Validate the anchor target as well as its displayed label. If the README link is changed back to /releases/tag/v0.4.0 while its text rem' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_repository_truth.py` (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at `tools/check_repository_truth.py:66`: 'f"The latest published GitHub repository release is [{latest_release}]",'.
  - The later-change audit compared `tools/check_repository_truth.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR373:PRRT_kwDOTH_vCM6TuR8P

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_repository_truth.py:95`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_repository_truth.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR373:PRRT_kwDOTH_vCM6TuR8P found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require the authoritative repository in the record URL Require the complete canonical GitHub release URL here. The current suffix-only test also accepts a link on another ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_repository_truth.py` (SHA-256 e6a28648de047730b5b9d04c9841569817afc32a72823c34252cfc753efe708c).
  - Current repository evidence at `tools/check_repository_truth.py:95`: 'fail("release record does not link to the authoritative GitHub release")'.
  - The later-change audit compared `tools/check_repository_truth.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR37:PRRT_kwDOTH_vCM6OZK28

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:53`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR37:PRRT_kwDOTH_vCM6OZK28 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align the FARM stable component scope This adds the Phase 1 through Phase 4 audit records to the FARM stable component set, but the new docs/milestones/FARM-v1.0-Stable.md' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:53`: '### Project FAR v0.3.1 Repository Maturity and Automation'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR380:PRRT_kwDOTH_vCM6Txs_H

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py:29`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR380:PRRT_kwDOTH_vCM6Txs_H found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Exercise SWE-agent before declaring the launch boundary reached In the added full-no-model-execution-rehearsal job, whenever parsing succeeds but SWE-agent's runtime initi" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py` (SHA-256 736a0344981d2aad44bea7a07df1b2fffdc7b7ed518f669f151b6e04ece948e8).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py:29`: 'import sys'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR381:PRRT_kwDOTH_vCM6TyRN1

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:190`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRN1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not let transient provider logs override validated success When SWE-agent or LiteLLM logs a transient timeout, 429, or 5xx during one of the configured provider retries' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:190`: 'value["predictions"], task_id, allow_implicit_instance=False'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR381:PRRT_kwDOTH_vCM6TyRNx

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRNx found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Revalidate restored completions before selecting the next run When an execution artifact was produced by the old controller—including the misclassified v1.0.0-r1 that moti' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`: '_core.main()'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR381:PRRT_kwDOTH_vCM6TyRNy

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:16`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR381:PRRT_kwDOTH_vCM6TyRNy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Block progression when a run fails terminally When the new classifier emits failedterminal for an early slot, adding it only to ALLOWEDSTATES makes the state loadable but ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:16`: 'from validated_execution_recovery import install as install_recovery'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR384:PRRT_kwDOTH_vCM6Ty6_k

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py:402`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6Ty6_k found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Align the inherited regression with sequence hardening The required test command in both .github/workflows/far-swe-agent-execution.yml and .github/workflows/far-swebench-e' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py` (SHA-256 fbd56ed307203f7dbf84e34bace4df55c6f4041ee9aaa0d58d729ac101b8753e).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py:402`: 'self.assertEqual(second["state"], "pending")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR384:PRRT_kwDOTH_vCM6Ty6_m

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:239`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6Ty6_m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject malformed noncanonical target predictions When a noncanonical .pred explicitly names the frozen task but omits modelpatch—for example {"instanceid": "", "unexpected' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:239`: 'continue'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR384:PRRT_kwDOTH_vCM6TynPj

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPj found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reconcile before enforcing sequential ordering When restoring the exact bad state produced by the previous controller—a failedterminal slot followed by a complete slot—bas' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`: '_core.main()'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR384:PRRT_kwDOTH_vCM6TynPo

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:222`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPo found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Inspect every prediction file that claims the target If SWE-agent emits the canonical .pred plus another .pred whose payload also declares the target instance, this filter' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:222`: 'aggregate_files = sorted(swe_output.rglob("preds.json"))'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR384:PRRT_kwDOTH_vCM6TynPq

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR384:PRRT_kwDOTH_vCM6TynPq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate the copied trajectory during restoration When a restored artifact is missing trajectories/ or that file no longer matches run["trajectorysha256"], this required-e' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` (SHA-256 5bc2d55758006241a0d09c082714fd9a0d66e26da2f7e4a93bbde22f41b9bf09).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:29`: '_core.main()'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR386:PRRT_kwDOTH_vCM6TzCgi

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:107`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR386:PRRT_kwDOTH_vCM6TzCgi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject malformed keyed target predictions When a noncanonical .pred or preds.json uses the already-supported {taskid: prediction} form, recursion reaches a value without i' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:107`: 'return asdict(self)'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR389:PRRT_kwDOTH_vCM6TzgU-

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:324`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgU- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve retry classification when output is absent When SWE-agent reports a genuine 429/5xx before creating sweagent-output, this early return marks the attempt failedter' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` (SHA-256 cb03c35e878d9fb38997ac61c55424180977a1f87fa6cc1d942733dc98833773).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:324`: ')'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR389:PRRT_kwDOTH_vCM6TzgVA

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:287`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgVA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Roll back artifacts moved before an interrupted return If shutil.move moves an artifact and then raises—for example, a KeyboardInterrupt after the rename/copy but before r' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py` (SHA-256 2a6058ab8d4b58209c9f3e0bbfce2cf8cc7c8d9da27f3697aaf43ac49f07eb57).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:287`: 'moved.append((path, destination))'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR389:PRRT_kwDOTH_vCM6TzgVD

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:272`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR389:PRRT_kwDOTH_vCM6TzgVD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject broken symlinks before archiving When a prior attempt leaves a broken symlink under an artifact name such as instance.json, stdout.log, or sweagent-output, the prec' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py` (SHA-256 2a6058ab8d4b58209c9f3e0bbfce2cf8cc7c8d9da27f3697aaf43ac49f07eb57).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:272`: 'raise SystemExit(f"Attempt artifact is not a local regular path: {path}")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR38:PRRT_kwDOTH_vCM6ObcXR

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:47`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR38:PRRT_kwDOTH_vCM6ObcXR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Recheck placeholder search before recording a pass The repository already contains matches for this search, so the audit records a false preliminary pass. In the parent tr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md` (SHA-256 0a2ec390012393c0c8a66acd689943bf459b40d259247e78b17faef96ee86a3e).
  - Current repository evidence at `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:47`: '- FARM v1.0 Stable.'.
  - The later-change audit compared `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR391:PRRT_kwDOTH_vCM6T0ZLE

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:13`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR391:PRRT_kwDOTH_vCM6T0ZLE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Require model context for NOTFOUND signals When an unsuccessful agent or tool action emits a generic JSON error such as {"status":"NOTFOUND"}—including alongside a genuine' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` (SHA-256 a049c2ae960747f9295089828e8b0e63c125d52b1d79858fe7071e5783c36730).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:13`: 're.compile(r"\\bstatus[\\"\']?\\s*[:=]\\s*[\\"\']?not_found\\b", re.IGNORECASE),'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR391:PRRT_kwDOTH_vCM6T0ZLF

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:35`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR391:PRRT_kwDOTH_vCM6T0ZLF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep standalone provider timeout errors retryable When a provider reports an actual timeout in forms such as Timeout while contacting Gemini or provider request exceeded t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` (SHA-256 a049c2ae960747f9295089828e8b0e63c125d52b1d79858fe7071e5783c36730).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:35`: 're.compile(r"\\btimeout(?:error|exception)\\b", re.IGNORECASE),'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR392:PRRT_kwDOTH_vCM6T0n2T

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json:139`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2T found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Add the required top-level case ID Every workflow stage stops in the initial python casetools.py validate step because validatemanifest() requires m.get("caseid") == CASEI' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json` (SHA-256 3fb0fa29dc3cbc6626c8e0a1e6aa163240acdda4334bc3bff934fd4f5584b65e).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json:139`: '"probe_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent",'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR392:PRRT_kwDOTH_vCM6T0n2V

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json:6`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2V found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Correct the locked controller blob hash After the manifest identity is corrected, every validation still fails in verifysharedimplementation(): the validatedexecutecontrol' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json` (SHA-256 69d60e95952fcdf84eab559347caba94d44894206b04fc6ae0a63851321ea07e).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json:6`: '"validated_execute_controller.py": "ce525ddf6bd3213b80d8d9a01a494c3d9f89f953",'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR392:PRRT_kwDOTH_vCM6T0n2W

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `ci-and-automation`
- Current location: `.github/workflows/far-swe-agent-execution-v2.yml:178`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/far-swe-agent-execution-v2.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Extract restored artifacts at the case directory On the second and subsequent execute dispatches, the uploaded artifact contains both execution-output/... and access-freez' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/far-swe-agent-execution-v2.yml` (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at `.github/workflows/far-swe-agent-execution-v2.yml:178`: 'env:'.
  - The later-change audit compared `.github/workflows/far-swe-agent-execution-v2.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR392:PRRT_kwDOTH_vCM6T0n2X

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py:216`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR392:PRRT_kwDOTH_vCM6T0n2X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Record connection-level access-probe failures When the provider request fails before receiving an HTTP response—for example on DNS, TLS, connection-refusal, or timeout err' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py` (SHA-256 fa5bb3be3dbdf745d091a4e3863010dd4f4540799397fb7939aa7e9804d50971).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py:216`: 'except urllib.error.HTTPError as exc:'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR393:PRRT_kwDOTH_vCM6T2FXp

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:112`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR393:PRRT_kwDOTH_vCM6T2FXp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Validate the decoded HTTP error shape before accessing it When an HTTP error contains valid JSON whose root is not an object, or whose error member is null, a string, or a' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` (SHA-256 7c41039368a85f082d01dc48aa60dd700d08e283dc8d6856ad46174e00e387d5).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:112`: 'provider_error = json.loads(raw).get("error", {})'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR393:PRRT_kwDOTH_vCM6T2FXq

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:108`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR393:PRRT_kwDOTH_vCM6T2FXq found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Record transport failures that occur while reading the body When the provider sends response headers but stalls or disconnects while the body is being read, response.read(' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` (SHA-256 7c41039368a85f082d01dc48aa60dd700d08e283dc8d6856ad46174e00e387d5).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:108`: 'raw = response.read().decode(errors="replace")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR395:PRRT_kwDOTH_vCM6T2PsZ

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md:3`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR395:PRRT_kwDOTH_vCM6T2PsZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Preserve the failed access-probe record When this freeze is merged, the replacement status records only the successful probe and removes the repository's sole account of a" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md` (SHA-256 d81e05527fbe878c22ef9aeef80a43c1b3755bdf832e57878da4d89ada6c43b0).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md:3`: 'Authority: the immutable evidence locks, the completed execution artifact from workflow run `30214963069`, the outcome-blind primary freeze, and the post-freeze reveal bundle in this directory.'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR396:PRRT_kwDOTH_vCM6T2ibE

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `ci-and-automation`
- Current location: `.github/workflows/far-swe-agent-execution-v2.yml:191`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/far-swe-agent-execution-v2.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR396:PRRT_kwDOTH_vCM6T2ibE found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not let failed restores supersede the last checkpoint When this new artifact validation rejects a restore, the if: always() upload at the end of this workflow still pub' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/far-swe-agent-execution-v2.yml` (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at `.github/workflows/far-swe-agent-execution-v2.yml:191`: ''.
  - The later-change audit compared `.github/workflows/far-swe-agent-execution-v2.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR397:PRRT_kwDOTH_vCM6T4r2a

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json:379`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2a found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Preserve the source artifact beyond its expiry The only copy of the 73-file execution source is GitHub artifact 8635674915, and this lock records that it expires on 2026-0' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json` (SHA-256 0653065cbf8cbcf8f911a5ec9c68a4fea66ce73d3b04ed511dad644387d296b9).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json:379`: '"artifact_id": 8635674915,'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR397:PRRT_kwDOTH_vCM6T4r2b

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2b found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Bind the reveal to the currently verified freeze When post-freeze-reveal was generated against an older primary freeze, this verifier accepts it because it checks only the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` (SHA-256 87014ed0fce34411ba57f413414372103094a137a38b9a3e4cccb48d2f1244b4).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`: 'raise SystemExit("Final report reveal binding mismatch")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR397:PRRT_kwDOTH_vCM6T4r2c

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR397:PRRT_kwDOTH_vCM6T4r2c found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Recompute the final report from the revealed outcomes When the derived JSON or Markdown report is accidentally edited, verifyreveal checks only that the final JSON points ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` (SHA-256 87014ed0fce34411ba57f413414372103094a137a38b9a3e4cccb48d2f1244b4).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`: 'raise SystemExit("Final report reveal binding mismatch")'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR398:PRRT_kwDOTH_vCM6T5D8v

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:52`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR398:PRRT_kwDOTH_vCM6T5D8v found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Preserve the evaluation evidence behind these hashes After the workflow artifact's 90-day retention period expires, the committed testoutputsha256 and runinstancelogsha256" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` (SHA-256 0938b41fd28da12af32b586121fff4b105c87fb13a24cee3c4d3685ad0fb3097).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:52`: '"test_output_sha256": "d109c9021e37e8bdd69ab4495022c0f59f835cb7975a4f27665f801e91967f84"'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR398:PRRT_kwDOTH_vCM6T5D8w

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `external-validation`
- Current location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:194`
- Blocks experiment reconstruction: `true`
- Root cause: `external-validation:commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR398:PRRT_kwDOTH_vCM6T5D8w found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Declare a status for each new reveal artifact This new outcome artifact, like the three companion files added by the commit, does not declare whether its status is Accepte' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` (SHA-256 0938b41fd28da12af32b586121fff4b105c87fb13a24cee3c4d3685ad0fb3097).
  - Current repository evidence at `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:194`: '"schema": "far-swe-agent-v2-post-freeze-reveal/1.0",'.
  - The later-change audit compared `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR399:PRRT_kwDOTH_vCM6T5NRD

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `ci-and-automation`
- Current location: `.github/workflows/far-swe-agent-execution-v2.yml:62`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/far-swe-agent-execution-v2.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR399:PRRT_kwDOTH_vCM6T5NRD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Enforce the execution freeze independently of the selected ref When workflowdispatch selects a branch or tag where bundle-sha256.json is absent, this guard inspects that c' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/far-swe-agent-execution-v2.yml` (SHA-256 61767220c9f9c3952c7a29a0f3659585c139529d495992ff2f48e09e804f4ad6).
  - Current repository evidence at `.github/workflows/far-swe-agent-execution-v2.yml:62`: 'if [ -f "$CASE_DIR/post-freeze-reveal/bundle-sha256.json" ]; then'.
  - The later-change audit compared `.github/workflows/far-swe-agent-execution-v2.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR399:PRRT_kwDOTH_vCM6T5NRG

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/far-swe-agent-v2-postprocess.yml:64`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/far-swe-agent-v2-postprocess.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR399:PRRT_kwDOTH_vCM6T5NRG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Refuse reveal evaluation after the final bundle exists On the current completed main, a dispatch with stage=evaluate-reveal and the confirmation phrase passes this new exi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/far-swe-agent-v2-postprocess.yml` (SHA-256 872880280b0831e6d35081ae23a695878645a843c80986916f7b55180eccf259).
  - Current repository evidence at `.github/workflows/far-swe-agent-v2-postprocess.yml:64`: '--output-dir post-freeze-reveal'.
  - The later-change audit compared `.github/workflows/far-swe-agent-v2-postprocess.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR39:PRRT_kwDOTH_vCM6ObfIA

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:63`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR39:PRRT_kwDOTH_vCM6ObfIA found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Reopen the FARE alignment check This pass is inaccurate for the post-v1 stack: in this commit, README.md's navigation/reading order lists framework material for FAR/FARA/F" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md` (SHA-256 0a2ec390012393c0c8a66acd689943bf459b40d259247e78b17faef96ee86a3e).
  - Current repository evidence at `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:63`: 'Assessment: pass.'.
  - The later-change audit compared `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR400:PRRT_kwDOTH_vCM6T5R2m

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/audits/theory-correction-audit-2026-07-26.md:3`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/audits/theory-correction-audit-2026-07-26.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR400:PRRT_kwDOTH_vCM6T5R2m found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Keep correction artifacts provisional until replicated In the reviewed tree, the only new provenance is this single audit and its decision-log entry; no replication record' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/theory-correction-audit-2026-07-26.md` (SHA-256 d7f814a44b7ebc3bfca16ec56e2dc54b3db3be0b7e49da9deeab9bb0f8995da6).
  - Current repository evidence at `docs/audits/theory-correction-audit-2026-07-26.md:3`: 'Status: **Accepted repository correction record**'.
  - The later-change audit compared `docs/audits/theory-correction-audit-2026-07-26.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR400:PRRT_kwDOTH_vCM6T5R2n

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_semantic_consistency.py:54`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_semantic_consistency.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR400:PRRT_kwDOTH_vCM6T5R2n found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Scan all active artifacts before reporting semantic consistency When semantic-check is run on this commit, it reports PASS even though active non-archive artifacts outside' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_semantic_consistency.py` (SHA-256 a6b65a1b57b23b2d70df62bf6abcc810401b8ba9d4fd0ad65aa97802b1c36513).
  - Current repository evidence at `tools/check_semantic_consistency.py:54`: 'errors.append(f"active canonical document promotes legacy terminology: {path.relative_to(ROOT)}")'.
  - The later-change audit compared `tools/check_semantic_consistency.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR401:PRRT_kwDOTH_vCM6T5eUS

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_swe_agent_v2_forensics.py:119`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_swe_agent_v2_forensics.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Validate the evidence inventory against its source locks The validator never loads evidence-inventory.json, so deleting an artifact, changing a hash, or mislabeling extern' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_swe_agent_v2_forensics.py` (SHA-256 cbd3324febe7a37a756ca610265ca87ffaa089d51af010dd57872886a647bb93).
  - Current repository evidence at `tools/check_swe_agent_v2_forensics.py:119`: "if {x.get('code') for x in taxonomy}!=expected: errors.append('taxonomy incomplete')".
  - The later-change audit compared `tools/check_swe_agent_v2_forensics.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR401:PRRT_kwDOTH_vCM6T5eUU

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_swe_agent_v2_forensics.py:112`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_swe_agent_v2_forensics.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Reconcile timeline facts with the frozen run records If a timeline's outcome, call budget, termination reason, patch result, or grader result is changed, validation still " at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_swe_agent_v2_forensics.py` (SHA-256 cbd3324febe7a37a756ca610265ca87ffaa089d51af010dd57872886a647bb93).
  - Current repository evidence at `tools/check_swe_agent_v2_forensics.py:112`: "if any(not required <= set(e) for e in d.get('events',[])): errors.append(f'timeline fields missing: {run}')".
  - The later-change audit compared `tools/check_swe_agent_v2_forensics.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR401:PRRT_kwDOTH_vCM6T5eUV

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json:84`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/audits/swe-agent-v2-forensics/failure-taxonomy.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR401:PRRT_kwDOTH_vCM6T5eUV found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Keep patch-design failure classified as unknown The reveal proves only that each applied patch did not pass the target; it cannot distinguish a design error from implement' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json` (SHA-256 12d311ac7b7c9adadd50c2ced37f57b515abbf38cd0fbce14043751efb02fa53).
  - Current repository evidence at `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json:84`: '"residual_risk": "A failed patch outcome must not be relabeled as a patch-design cause without direct distinguishing evidence.",'.
  - The later-change audit compared `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR402:PRRT_kwDOTH_vCM6T53x-

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_merged_pr_review_inventory.py:104`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_merged_pr_review_inventory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Reject incomplete per-PR manifests When countsperpr is empty, omits an inventoried PR, or reports endpoint counts that disagree with the raw records, this loop merely find' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_merged_pr_review_inventory.py` (SHA-256 ad69652fd4ed51ac7b975aee9edcee5472fc5ed9834cf758c4923297e3f4cfd7).
  - Current repository evidence at `tools/check_merged_pr_review_inventory.py:104`: 'for status in [endpoint.get("status")]'.
  - The later-change audit compared `tools/check_merged_pr_review_inventory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR402:PRRT_kwDOTH_vCM6T53x9

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/audits/merged-pr-review-audit/retrieval-manifest.json:21`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/audits/merged-pr-review-audit/retrieval-manifest.json`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Include standard merge commits in the inventory At the audited SHA, git log --first-parent contains 138 additional commits with subjects such as Merge pull request #395 fr' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/audits/merged-pr-review-audit/retrieval-manifest.json` (SHA-256 04098e9daacfb3e35680b3959fa32cc670dbe473885761a32e0aac9b901aecca).
  - Current repository evidence at `docs/audits/merged-pr-review-audit/retrieval-manifest.json:21`: '"pull_requests": {'.
  - The later-change audit compared `docs/audits/merged-pr-review-audit/retrieval-manifest.json` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR402:PRRT_kwDOTH_vCM6T53x_

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_merged_pr_review_inventory.py:29`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_merged_pr_review_inventory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53x_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reject repeated source and thread IDs If pagination replay or overlapping retrieval produces the same record twice, the equality condition allows both copies because only ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_merged_pr_review_inventory.py` (SHA-256 ad69652fd4ed51ac7b975aee9edcee5472fc5ed9834cf758c4923297e3f4cfd7).
  - Current repository evidence at `tools/check_merged_pr_review_inventory.py:29`: 'elif value in seen and seen[value] != record:'.
  - The later-change audit compared `tools/check_merged_pr_review_inventory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR402:PRRT_kwDOTH_vCM6T53yB

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `test-infrastructure`
- Current location: `tests/test_merged_pr_review_inventory.py:46`
- Blocks experiment reconstruction: `true`
- Root cause: `test-infrastructure:tests/test_merged_pr_review_inventory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR402:PRRT_kwDOTH_vCM6T53yB found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate the checked-in inventory in canonical tests The canonical test path discovers this test, but every assertion validates self.root, which is a synthetic temporary d' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tests/test_merged_pr_review_inventory.py` (SHA-256 73d91818500d917c7ebcfcd7f6efd996693ff10b2be9b8f5cec4bdfb29393933).
  - Current repository evidence at `tests/test_merged_pr_review_inventory.py:46`: 'def test_positive(self): self.assertEqual([], validate(self.root, self.sha))'.
  - The later-change audit compared `tests/test_merged_pr_review_inventory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR403:PRRT_kwDOTH_vCM6T6IS4

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/check_proof_object.py:207`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_proof_object.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS4 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not weaken final theorem-conclusion alignment When a proof-object conclusion is much longer than the registered theorem statement, using the shorter vocabulary as the d' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_proof_object.py` (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at `tools/check_proof_object.py:207`: 'return len(summary_words & statement_words) / min(len(summary_words), len(statement_words)) >= 0.35'.
  - The later-change audit compared `tools/check_proof_object.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR403:PRRT_kwDOTH_vCM6T6IS5

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_orphaned_docs.py:72`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_orphaned_docs.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve the documented orphan-ok exemption When an intentionally standalone document contains the documented orphan-ok marker, it is now included in alldocs and therefore' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_orphaned_docs.py` (SHA-256 d833f93de7a104ccab735bc2bd74119c18c678a16ad9c6c00fda55766efb47ea).
  - Current repository evidence at `tools/check_orphaned_docs.py:72`: 'if "archive" not in path.relative_to(root).parts'.
  - The later-change audit compared `tools/check_orphaned_docs.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR403:PRRT_kwDOTH_vCM6T6IS6

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_proof_object.py:117`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_proof_object.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR403:PRRT_kwDOTH_vCM6T6IS6 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Count distinct metadata sources before suppressing warnings When two inputs inherit the same lemma, theorem, or axiom through separate lineage paths, sourceitems returns t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_proof_object.py` (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at `tools/check_proof_object.py:117`: 'return'.
  - The later-change audit compared `tools/check_proof_object.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR404:PRRT_kwDOTH_vCM6T6taR

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/export_merged_pr_review_inventory.py:394`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/export_merged_pr_review_inventory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taR found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Tie the live API snapshot to the audited SHA When another PR merges before or during an export, this live state=closed enumeration can include or omit repository state new' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/export_merged_pr_review_inventory.py` (SHA-256 2d45122793244bc9e461c23061e8ecff8e16a66eb05a137bd84eb45c883aae73).
  - Current repository evidence at `tools/export_merged_pr_review_inventory.py:394`: 'merged = [normalize_pr(pr) for pr in closed_prs if pr.get("merged_at")]'.
  - The later-change audit compared `tools/export_merged_pr_review_inventory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR404:PRRT_kwDOTH_vCM6T6taT

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/export-merged-pr-review-inventory.yml:29`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/export-merged-pr-review-inventory.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Pin manual inventory runs to main For a workflowdispatch run launched against a non-main ref, actions/checkout checks out that selected ref because no ref is specified. Th' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/export-merged-pr-review-inventory.yml` (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at `.github/workflows/export-merged-pr-review-inventory.yml:29`: 'fetch-depth: 1'.
  - The later-change audit compared `.github/workflows/export-merged-pr-review-inventory.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR404:PRRT_kwDOTH_vCM6T6taU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/export-merged-pr-review-inventory.yml:78`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/export-merged-pr-review-inventory.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR404:PRRT_kwDOTH_vCM6T6taU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Give reruns a new export branch When a failed or incomplete workflow is re-run, GitHub's runid does not change (GitHub context documentation), so this reuses the branch cr" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/export-merged-pr-review-inventory.yml` (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at `.github/workflows/export-merged-pr-review-inventory.yml:78`: 'run: |'.
  - The later-change audit compared `.github/workflows/export-merged-pr-review-inventory.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR405:PRRT_kwDOTH_vCM6T7G3-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/export-merged-pr-review-inventory.yml:67`
- Blocks experiment reconstruction: `true`
- Root cause: `ci-and-automation:.github/workflows/export-merged-pr-review-inventory.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR405:PRRT_kwDOTH_vCM6T7G3- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Report the actual number of export attempts When all four attempts return 2, this unconditional increment changes attempt from 4 to 5 before the loop exits, so the fail-cl' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/export-merged-pr-review-inventory.yml` (SHA-256 69aec4adfafeb689cdf52c9e199423d45b597c83319bb19f4393063aa0c02582).
  - Current repository evidence at `.github/workflows/export-merged-pr-review-inventory.yml:67`: 'attempt=$((attempt + 1))'.
  - The later-change audit compared `.github/workflows/export-merged-pr-review-inventory.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR40:PRRT_kwDOTH_vCM6OcdQT

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/CANONICAL_MAP.md:69`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/CANONICAL_MAP.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR40:PRRT_kwDOTH_vCM6OcdQT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restore the missing FARE canonical components When contributors use this new map as the FARE navigation hub, it drops canonical FARE components that the authoritative FARE' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/CANONICAL_MAP.md` (SHA-256 9fae5238b7a853b517252f364f907623ab8729d92dd94b6aaf98194534f1b76e).
  - Current repository evidence at `docs/CANONICAL_MAP.md:69`: '| FAR Dependency Graph | `../frameworks/FAR/dependency-graph.md` | Records FAR dependency order. |'.
  - The later-change audit compared `docs/CANONICAL_MAP.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR48:PRRT_kwDOTH_vCM6Ofq_j

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/roadmap/v0.2.0-next-phase.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/roadmap/v0.2.0-next-phase.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR48:PRRT_kwDOTH_vCM6Ofq_j found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Align the roadmap version with the active milestone This introduces a new v0.2.0 next-phase roadmap even though the repository already records docs/releases/project-far-v0' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/roadmap/v0.2.0-next-phase.md` (SHA-256 326173f01d0461c792cc3e1b6f25926c094a241bf80b9d8f23cbd2abb8e7b117).
  - Current repository evidence at `docs/roadmap/v0.2.0-next-phase.md:5`: 'This document records the next development phase after the initial public release.'.
  - The later-change audit compared `docs/roadmap/v0.2.0-next-phase.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR49:PRRT_kwDOTH_vCM6Of2J_

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/verify_theory.py:201`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/verify_theory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR49:PRRT_kwDOTH_vCM6Of2J_ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include non-theorem nodes in the cycle graph When proposition/lemma metadata is validated, dependencies involving those IDs are accepted as known dependencies but never in' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/verify_theory.py` (SHA-256 884e3d178d04275f2ea97bdf75f5d1c7d1537f083de222c979bc5a3b889cbf63).
  - Current repository evidence at `tools/verify_theory.py:201`: 'aliases.add(str(alias))'.
  - The later-change audit compared `tools/verify_theory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR49:PRRT_kwDOTH_vCM6Of2KD

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/metadata/generated-proposition-index.md:14`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/metadata/generated-proposition-index.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR49:PRRT_kwDOTH_vCM6Of2KD found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Include P-009 in the generated index theory/metadata/propositions.yaml adds P-009 and the proposition catalog contains it, but the committed generated proposition index st' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/metadata/generated-proposition-index.md` (SHA-256 75d664a4afd5bc4827f267a2e067d8c69cbabd81c6303d933e88bb9c0cdcc26f).
  - Current repository evidence at `theory/metadata/generated-proposition-index.md:14`: '| P-008 | Resolution Dependence | Established | `theory/proofs/P-001-first-propositions.md` | resolution execution under a reasoning calculus | n/a | n/a |'.
  - The later-change audit compared `theory/metadata/generated-proposition-index.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR51:PRRT_kwDOTH_vCM6OgLyL

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/verify_theory.py:154`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/verify_theory.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR51:PRRT_kwDOTH_vCM6OgLyL found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve ID checks for existing catalogs Because this helper is still used for propositions and lemmas, accepting a title match means a metadata entry with a mistyped or s' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/verify_theory.py` (SHA-256 884e3d178d04275f2ea97bdf75f5d1c7d1537f083de222c979bc5a3b889cbf63).
  - Current repository evidence at `tools/verify_theory.py:154`: 'raise VerificationError(f"{prefix} entry missing fields {sorted(missing)}: {item}")'.
  - The later-change audit compared `tools/verify_theory.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR52:PRRT_kwDOTH_vCM6OgR7W

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-001.proof.yaml:30`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-001.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR52:PRRT_kwDOTH_vCM6OgR7W found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add the definition dependency to T-001 metadata This proof object now makes DEF-019 an explicit premise for proving T-001, but theory/metadata/theorems.yaml still lists on' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-001.proof.yaml` (SHA-256 c592af3b04c3af82dad53d23a354e3c9bc414296f7d2756316a2783a7bb518eb).
  - Current repository evidence at `theory/proof-objects/T-001.proof.yaml:30`: 'source: DEF-019'.
  - The later-change audit compared `theory/proof-objects/T-001.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR53:PRRT_kwDOTH_vCM6OgVPb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-002.proof.yaml:42`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-002.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR53:PRRT_kwDOTH_vCM6OgVPb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Model the countermodel obligations as inputs Here p2 is only the conditional proof method and p4 only states L-001's necessity claim; the proof object never establishes th" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-002.proof.yaml` (SHA-256 32032af6bafeea29b6156a3badf2aa230d96a93bf3d88f677d548cbeb797c87b).
  - Current repository evidence at `theory/proof-objects/T-002.proof.yaml:42`: 'statement: Representation is not eliminable in favor of the other four primitives under the current deletion-only reduction standard.'.
  - The later-change audit compared `theory/proof-objects/T-002.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR54:PRRT_kwDOTH_vCM6OgbqU

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-003.proof.yaml:77`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/proof-objects/T-003.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR54:PRRT_kwDOTH_vCM6OgbqU found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Prove T exists before conjoining it When R has no specified transition executions, s6 only establishes a conditional/permission that T may be empty or partial; it does not' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-003.proof.yaml` (SHA-256 dfd643f02cbbdcec0620ffb475a9bd9fc89e3f43d3ca126190c1f1b1e73c5d4e).
  - Current repository evidence at `theory/proof-objects/T-003.proof.yaml:77`: 'statement: R has C and T.'.
  - The later-change audit compared `theory/proof-objects/T-003.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR54:PRRT_kwDOTH_vCM6OgbqY

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-003.proof.yaml:97`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-003.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR54:PRRT_kwDOTH_vCM6OgbqY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use universal generalization for arbitrary R This step derives a universal theorem from the construction for an arbitrary R, but labels the inference as universalinstantia' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-003.proof.yaml` (SHA-256 dfd643f02cbbdcec0620ffb475a9bd9fc89e3f43d3ca126190c1f1b1e73c5d4e).
  - Current repository evidence at `theory/proof-objects/T-003.proof.yaml:97`: 'statement: Every reasoning process within the stated Project FAR scope admits a FAR representation.'.
  - The later-change audit compared `theory/proof-objects/T-003.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR55:PRRT_kwDOTH_vCM6OgvoF

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-005.proof.yaml:53`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-005.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR55:PRRT_kwDOTH_vCM6OgvoF found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve L-008 in the T-005 proof object For T-005, theory/metadata/theorems.yaml lists L-008 as a dependency, and theory/lemmas/core-lemmas.md uses that lemma to require ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-005.proof.yaml` (SHA-256 e37a59886a643d8260b9f094e4c9476d0e16876cf5b77855dca9ef8dc45072d9).
  - Current repository evidence at `theory/proof-objects/T-005.proof.yaml:53`: 'statement: e can be represented in FAR by a transition signature.'.
  - The later-change audit compared `theory/proof-objects/T-005.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR55:PRRT_kwDOTH_vCM6OgvoG

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-006.proof.yaml:19`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/proof-objects/T-006.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR55:PRRT_kwDOTH_vCM6OgvoG found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not add an uncited induction premise T-006 is registry-relative: its documented dependencies are the derived-concept registry and canonical notation, but this proof obj' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-006.proof.yaml` (SHA-256 b7bf4570a43b57da535f9c9e9a1ae32fb06cf9b5a201dc0ed00e2d7ab8052224).
  - Current repository evidence at `theory/proof-objects/T-006.proof.yaml:19`: 'statement: If every concept at registry depth n or lower is constructible from P, then any concept at depth n + 1 deriving from those concepts is constructible from P by substitution.'.
  - The later-change audit compared `theory/proof-objects/T-006.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR56:PRRT_kwDOTH_vCM6OhRaY

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-008.proof.yaml:45`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/proof-objects/T-008.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRaY found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Establish interpretation preservation before concluding semantics For canonical representations where the role pairing has only been shown to preserve structure/admissibil' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-008.proof.yaml` (SHA-256 0e6a778db636a6894d498e92e2c8f6e4f3f95f0b436c4daab13b26e3b7c590e4).
  - Current repository evidence at `theory/proof-objects/T-008.proof.yaml:45`: 'rule: definition_unfolding'.
  - The later-change audit compared `theory/proof-objects/T-008.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR56:PRRT_kwDOTH_vCM6OhRab

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-009.proof.yaml:28`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/proof-objects/T-009.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRab found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Keep L-007's termination precondition explicit For a finite FAR representation whose supplied ordering/labeling/redundancy rules are not known to strictly reduce unresolve" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-009.proof.yaml` (SHA-256 23cb16efa983e035cba420b4795b246594c276fbf2ce20b79446ffed5d924103).
  - Current repository evidence at `theory/proof-objects/T-009.proof.yaml:28`: 'inputs: [s1, s2]'.
  - The later-change audit compared `theory/proof-objects/T-009.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR56:PRRT_kwDOTH_vCM6OhRac

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-010.proof.yaml:49`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/proof-objects/T-010.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR56:PRRT_kwDOTH_vCM6OhRac found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Avoid applying T-009 outside finite normalized cases T-010's premise is only a complete FAR representation, but T-009 is scoped to finite FAR representations with supplied" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-010.proof.yaml` (SHA-256 b815f752169451e6dd4a6d752e1944e10877e968f9f6d2885a6f89c7cd72a697).
  - Current repository evidence at `theory/proof-objects/T-010.proof.yaml:49`: 'justification: Applies the trace/process distinction to avoid reconstructing private, hidden, or otherwise unrepresented features.'.
  - The later-change audit compared `theory/proof-objects/T-010.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR57:PRRT_kwDOTH_vCM6OpqRi

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/proof-objects/T-012.proof.yaml:16`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/proof-objects/T-012.proof.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR57:PRRT_kwDOTH_vCM6OpqRi found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Attribute Q-equivalence definitions to an existing source These premises cite FAR-model-theory, but the model-theory file only defines equivalence as preservation over a p' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/proof-objects/T-012.proof.yaml` (SHA-256 db3a7718bb716aa6debde681e63cec929d5c7805a0d86123e3008b82512beeaf).
  - Current repository evidence at `theory/proof-objects/T-012.proof.yaml:16`: 'statement: "A and B are Q-equivalent exactly when every property in Q holds in A exactly when the corresponding property holds in B."'.
  - The later-change audit compared `theory/proof-objects/T-012.proof.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR58:PRRT_kwDOTH_vCM6Op8yy

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_proof_object.py:123`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_proof_object.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR58:PRRT_kwDOTH_vCM6Op8yy found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require more than word overlap for conclusions When a proof object changes the final step and conclusion to a weaker or contradictory phrase that reuses theorem words, thi' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_proof_object.py` (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at `tools/check_proof_object.py:123`: ''.
  - The later-change audit compared `tools/check_proof_object.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR61:PRRT_kwDOTH_vCM6OrXNb

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/language/statement-schema.md:25`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/language/statement-schema.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR61:PRRT_kwDOTH_vCM6OrXNb found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Allow existing artifact statement kinds When this schema is used to validate current metadata, this allowed set omits the values the repository already stores for statemen' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/language/statement-schema.md` (SHA-256 ec2de2f251a787fb9217d31242792d314f9c386df5d989c7131f2f3acc0f1e61).
  - Current repository evidence at `theory/language/statement-schema.md:25`: 'kind: universal | existential | definitional | conditional | equivalence | preservation | construction | validation | classification | meta'.
  - The later-change audit compared `theory/language/statement-schema.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR64:PRRT_kwDOTH_vCM6OuI1o

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_proof_object.py:329`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_proof_object.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR64:PRRT_kwDOTH_vCM6OuI1o found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Accept symbolic antecedents for ASCII modus ponens When a proof object uses the documented modus-ponens shape P plus P -> Q (the same symbolic content added in the new fix' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_proof_object.py` (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at `tools/check_proof_object.py:329`: 'errors.append(f"step {step_id} conjunction_intro requires at least two inputs")'.
  - The later-change audit compared `tools/check_proof_object.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR64:PRRT_kwDOTH_vCM6OuI1r

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_proof_object.py:311`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_proof_object.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR64:PRRT_kwDOTH_vCM6OuI1r found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve canonical SemanticContent vocabulary matches For a semanticpreservation step whose inputs express semantic content only in canonical notation such as SemanticCont' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_proof_object.py` (SHA-256 8ed80a7462ea89192162fbc91be8d1b4515ec1f2f692c1b7e246ef4c3741de72).
  - Current repository evidence at `tools/check_proof_object.py:311`: 'if not sources:'.
  - The later-change audit compared `tools/check_proof_object.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR66:PRRT_kwDOTH_vCM6OuixP

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/evaluate_reasoning_systems.py:195`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/evaluate_reasoning_systems.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR66:PRRT_kwDOTH_vCM6OuixP found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Fail CI when any fixture fails classification When a reasoning-system fixture is syntactically valid but missing the reasoningsystem mapping or using an unsupported verdic' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/evaluate_reasoning_systems.py` (SHA-256 64d4fd1e7a3dd1f125b8b3020f7be7f01ed552dff7425e477538b286d92fb0de).
  - Current repository evidence at `tools/evaluate_reasoning_systems.py:195`: 'return 0'.
  - The later-change audit compared `tools/evaluate_reasoning_systems.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR70:PRRT_kwDOTH_vCM6OvPip

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/releases/project-far-v0.2.0.md:1`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/releases/project-far-v0.2.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR70:PRRT_kwDOTH_vCM6OvPip found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Declare the release artifact status The root AGENTS.md requires compliance with docs/governance/research-execution-charter.md, whose Repository Rules require every artifac' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/releases/project-far-v0.2.0.md` (SHA-256 d8e9483115dec90575b6e2c73a00124b9d79f1bb4e62a1108f5e93309068fc65).
  - Current repository evidence at `docs/releases/project-far-v0.2.0.md:1`: '# Project FAR v0.2.0'.
  - The later-change audit compared `docs/releases/project-far-v0.2.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR70:PRRT_kwDOTH_vCM6OvPir

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `repository-metadata`
- Current location: `README.md:14`
- Blocks experiment reconstruction: `false`
- Root cause: `repository-metadata:README.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR70:PRRT_kwDOTH_vCM6OvPir found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Synchronize the README release pointers When readers use the README for release navigation, this new section says v0.2.0 is the latest release, but the same README still h' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `README.md` (SHA-256 38bd38fa51ff57a68cdbdc6e281a779999725ebbeafc8cd5650983985cd45ddd).
  - Current repository evidence at `README.md:14`: 'The registered Universal Proof Program `POST-TUE-UPP-001` is complete. Its terminal adjudication is:'.
  - The later-change audit compared `README.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR71:PRRT_kwDOTH_vCM6OvQSt

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/releases/release-publication-instructions-v0.2.0.md:13`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/releases/release-publication-instructions-v0.2.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR71:PRRT_kwDOTH_vCM6OvQSt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Pin the release target to an exact commit If publication happens after any later commit lands on main, this instruction tells the releaser to create the v0.2.0 tag on that' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/releases/release-publication-instructions-v0.2.0.md` (SHA-256 863ca953de9b15fcb8756232c84c124edee014d4fd2808f7d2e3051cd829620d).
  - Current repository evidence at `docs/releases/release-publication-instructions-v0.2.0.md:13`: '- Target: latest `main` after the finalization PR is merged'.
  - The later-change audit compared `docs/releases/release-publication-instructions-v0.2.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR72:PRRT_kwDOTH_vCM6Ovhp9

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/evaluate_primitive_sufficiency.py:73`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/evaluate_primitive_sufficiency.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR72:PRRT_kwDOTH_vCM6Ovhp9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve registry validation output for malformed entries When a registry entry is missing a required field, validateentries() records the error but renderreport() immedia' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/evaluate_primitive_sufficiency.py` (SHA-256 f320561ebe726bb9f251e61174da5d9293ba9a4f434b5f58a1b4e9e32b0c0eff).
  - Current repository evidence at `tools/evaluate_primitive_sufficiency.py:73`: 'classification_counts = Counter(entry["classification"] for entry in entries)'.
  - The later-change audit compared `tools/evaluate_primitive_sufficiency.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR74:PRRT_kwDOTH_vCM6Owd-U

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/evidence-registry.yaml:124`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/evidence-registry.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR74:PRRT_kwDOTH_vCM6Owd-U found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use the fixture classification taxonomy classification is the fixture/evidence classification consumed by the falsification harness, whose documented valid values are fits' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/evidence-registry.yaml` (SHA-256 3a27c03b39e73880f21cdde22addb8dd2bd9bb6d52b1077ac2aaca699377e95c).
  - Current repository evidence at `theory/evaluation/evidence-registry.yaml:124`: 'system: Modal logic'.
  - The later-change audit compared `theory/evaluation/evidence-registry.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR74:PRRT_kwDOTH_vCM6Owd-X

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/primitive-sufficiency-report.md:14`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/primitive-sufficiency-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR74:PRRT_kwDOTH_vCM6Owd-X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Recompute the fits-FAR headline count The registry now has 7 entries with classification: fits FAR and only 2 entries with registryresolution: fits FAR; the reported 9 is ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/primitive-sufficiency-report.md` (SHA-256 1ba707a03ad5ef408d82f54353cec258fd1e3ea919d63513505eaad75c9cfd02).
  - Current repository evidence at `docs/reports/primitive-sufficiency-report.md:14`: '- Fits FAR by registry resolution: 2'.
  - The later-change audit compared `docs/reports/primitive-sufficiency-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR75:PRRT_kwDOTH_vCM6Owjky

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/run_adversarial_suite.py:164`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/run_adversarial_suite.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR75:PRRT_kwDOTH_vCM6Owjky found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Cross-check the pressure registry This runner only loads and validates --suite, so the new theory/falsification/primitive-pressure-registry.yaml is never read. Because tha' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/run_adversarial_suite.py` (SHA-256 07c4a7fdc6f5314088082f5b657fbfcda69a9d0b3237bec96b89cb339295d4c1).
  - Current repository evidence at `tools/run_adversarial_suite.py:164`: 'errors = validate_suite(data)'.
  - The later-change audit compared `tools/run_adversarial_suite.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR76:PRRT_kwDOTH_vCM6OwvGp

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/falsification/adversarial-test-suite.yaml:12`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/falsification/adversarial-test-suite.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR76:PRRT_kwDOTH_vCM6OwvGp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Recognize the new adversarial status labels When the suite is summarized with tools/runadversarialsuite.py, this new label (and the new conservative extension/unresolved p' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/falsification/adversarial-test-suite.yaml` (SHA-256 d45b3463188610731165a4aecda865b713126e6c34ee1afb9407aedfa1f31a93).
  - Current repository evidence at `theory/falsification/adversarial-test-suite.yaml:12`: 'current_status: resolved by existing primitive'.
  - The later-change audit compared `theory/falsification/adversarial-test-suite.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR77:PRRT_kwDOTH_vCM6Ow2uM

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/releases/github-release-v0.3.0.md:7`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/releases/github-release-v0.3.0.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR77:PRRT_kwDOTH_vCM6Ow2uM found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Use release-safe links in GitHub notes If this file is pasted into a GitHub Release body, these ../reports/... and same-directory relative links are no longer resolved rel' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/releases/github-release-v0.3.0.md` (SHA-256 a7859f9984d5b51a2b3b2d9aef03afaf467c6c2e111371c8f44b93ccf541e7c2).
  - Current repository evidence at `docs/releases/github-release-v0.3.0.md:7`: 'Highlights include:'.
  - The later-change audit compared `docs/releases/github-release-v0.3.0.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR80:PRRT_kwDOTH_vCM6Ox91X

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_internal_links.py:46`
- Blocks experiment reconstruction: `true`
- Root cause: `validators-and-tooling:tools/check_internal_links.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR80:PRRT_kwDOTH_vCM6Ox91X found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Restrict YAML extraction to actual path fields For YAML files that contain slash-delimited terms in prose or titles, this extracts those terms as repository paths even whe' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_internal_links.py` (SHA-256 99a381e80ebf20150db1894d6cd90f909bee3b54e48a8ee00160494896d2625a).
  - Current repository evidence at `tools/check_internal_links.py:46`: 'line_no=int(anchor[1:])'.
  - The later-change audit compared `tools/check_internal_links.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR80:PRRT_kwDOTH_vCM6Ox91b

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_internal_links.py:57`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_internal_links.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR80:PRRT_kwDOTH_vCM6Ox91b found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Resolve YAML repository paths from the root When a nested YAML file contains a repository-root-relative path, this resolves it relative to the YAML file's directory and re" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_internal_links.py` (SHA-256 99a381e80ebf20150db1894d6cd90f909bee3b54e48a8ee00160494896d2625a).
  - Current repository evidence at `tools/check_internal_links.py:57`: "print('Internal links OK')".
  - The later-change audit compared `tools/check_internal_links.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR81:PRRT_kwDOTH_vCM6O9Ugn

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-validation-methodology.md:82`
- Blocks experiment reconstruction: `true`
- Root cause: `canonical-theory:theory/evaluation/external-validation-methodology.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR81:PRRT_kwDOTH_vCM6O9Ugn found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Require reproducible evidence in external reports The reporting standard lets an external-system report be complete with only mapping/classification/justification prose, b' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-validation-methodology.md` (SHA-256 54f2f30fe0c9ed6c7c68ff5dea10000e32f7ac75378c4edfdb4d2236c19258cb).
  - Current repository evidence at `theory/evaluation/external-validation-methodology.md:82`: '7. Does it require a conservative extension?'.
  - The later-change audit compared `theory/evaluation/external-validation-methodology.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR81:PRRT_kwDOTH_vCM6O9Ugr

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-validation-registry.yaml:24`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-validation-registry.yaml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR81:PRRT_kwDOTH_vCM6O9Ugr found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Classify Coq consistently as conservative Under the new classification rules, fits FAR is for systems that do not need domain-specific extension machinery, while conservat' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-validation-registry.yaml` (SHA-256 fb34615057c80821d4ff46f7e3586cc15976c4a0056b4cd12c6fb89436b88318).
  - Current repository evidence at `theory/evaluation/external-validation-registry.yaml:24`: 'system: Coq'.
  - The later-change audit compared `theory/evaluation/external-validation-registry.yaml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR82:PRRT_kwDOTH_vCM6PEMp-

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-systems/constraint-solving.md:23`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-systems/constraint-solving.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR82:PRRT_kwDOTH_vCM6PEMp- found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Reclassify constraint solving by the stated rule The report identifies “domain-specific propagation and search” as pressure and says domain-specific propagators are requir' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-systems/constraint-solving.md` (SHA-256 4509bebe11c1bc4b240d17ac25d9db0d157dd61a099c18f71ffba5a6f99e8b27).
  - Current repository evidence at `theory/evaluation/external-systems/constraint-solving.md:23`: '`fits FAR`'.
  - The later-change audit compared `theory/evaluation/external-systems/constraint-solving.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR82:PRRT_kwDOTH_vCM6PEMqC

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `canonical-theory`
- Current location: `theory/evaluation/external-systems/linear-logic.md:31`
- Blocks experiment reconstruction: `false`
- Root cause: `canonical-theory:theory/evaluation/external-systems/linear-logic.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR82:PRRT_kwDOTH_vCM6PEMqC found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add the required remaining-questions sections The reporting standard in theory/evaluation/external-validation-methodology.md says every system report must include remainin' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `theory/evaluation/external-systems/linear-logic.md` (SHA-256 9d6c92724322281af99406e626a28dc4296d25b716eba574b7f7e9cd9eb0a682).
  - Current repository evidence at `theory/evaluation/external-systems/linear-logic.md:31`: 'Provisional.'.
  - The later-change audit compared `theory/evaluation/external-systems/linear-logic.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR84:PRRT_kwDOTH_vCM6PEqVg

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_release_consistency.py:14`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_release_consistency.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR84:PRRT_kwDOTH_vCM6PEqVg found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Anchor release-section detection to the heading In the current README the first occurrence of “Release” is the badge near the top, so this unanchored regex captures the ba' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_release_consistency.py` (SHA-256 8fbb1df37d7d9bae3d75ff91589da316c0d97952b14dac1ca4d4971eb4c61f63).
  - Current repository evidence at `tools/check_release_consistency.py:14`: "latest_section=re.search(r'(?is)(latest release|current release|release)[^\\n]*(?:\\n.{0,200}){0,8}', text)".
  - The later-change audit compared `tools/check_release_consistency.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR84:PRRT_kwDOTH_vCM6PEqVh

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/check_repository_hygiene.py:27`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/check_repository_hygiene.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR84:PRRT_kwDOTH_vCM6PEqVh found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Validate collected registry IDs before passing When a non-adversarial registry file contains duplicate id values, they are collected into registryids here but that map is ' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/check_repository_hygiene.py` (SHA-256 6685979a37a6a30a3ab8a8bda1de8075718b4e992335917f6fbe0d9229ac1a7a).
  - Current repository evidence at `tools/check_repository_hygiene.py:27`: "data=yaml.safe_load(p.read_text(encoding='utf-8'))".
  - The later-change audit compared `tools/check_repository_hygiene.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR85:PRRT_kwDOTH_vCM6PEvgp

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/generate_next_tasks.py:21`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/generate_next_tasks.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR85:PRRT_kwDOTH_vCM6PEvgp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Resolve gap labels to actual editable files When the gap row comes from a registry entry or primitive pressure, g['loc'] is a logical label such as PS-001 or Reasoning Cal" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/generate_next_tasks.py` (SHA-256 4b69c2e4f3ff2e073b9ce5b26266291278d841921c7d3b97c27514fdae6a91c9).
  - Current repository evidence at `tools/generate_next_tasks.py:21`: "if __name__=='__main__': raise SystemExit(main())".
  - The later-change audit compared `tools/generate_next_tasks.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR85:PRRT_kwDOTH_vCM6PEvgt

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/detect_research_gaps.py:55`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/detect_research_gaps.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR85:PRRT_kwDOTH_vCM6PEvgt found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P2 Badge Sort scanned markdown files before assigning gap IDs When regenerating the committed reports, this loop emits TODO gaps in the filesystem's rglob traversal order, which is" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/detect_research_gaps.py` (SHA-256 ef103f9a0d426bc67b8b90f8c74e9de4894942c34bfea1d33f64bf4c67283cbd).
  - Current repository evidence at `tools/detect_research_gaps.py:55`: "if p.get('unresolved_pressures'): add(gaps,'unresolved primitive pressure',prim,'high','Analyze unresolved pressure before promoting stronger sufficiency claims.')".
  - The later-change audit compared `tools/detect_research_gaps.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR86:PRRT_kwDOTH_vCM6PFwgS

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/detect_research_gaps.py:55`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/detect_research_gaps.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR86:PRRT_kwDOTH_vCM6PFwgS found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Sort TODO scans before assigning gap IDs When the planner is rerun via make plan/python tools/selfadvancementplan.py, this filesystem-order traversal feeds directly into t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/detect_research_gaps.py` (SHA-256 ef103f9a0d426bc67b8b90f8c74e9de4894942c34bfea1d33f64bf4c67283cbd).
  - Current repository evidence at `tools/detect_research_gaps.py:55`: "if p.get('unresolved_pressures'): add(gaps,'unresolved primitive pressure',prim,'high','Analyze unresolved pressure before promoting stronger sufficiency claims.')".
  - The later-change audit compared `tools/detect_research_gaps.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR87:PRRT_kwDOTH_vCM6PG65I

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `validators-and-tooling`
- Current location: `tools/update_readme_dashboard.py:68`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/update_readme_dashboard.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR87:PRRT_kwDOTH_vCM6PG65I found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Exclude interpreter caches from generated repository indexes When a developer has Python bytecode under tools/pycache, this recursive scan indexes those local cache files;' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/update_readme_dashboard.py` (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at `tools/update_readme_dashboard.py:68`: "if __name__=='__main__': main()".
  - The later-change audit compared `tools/update_readme_dashboard.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR87:PRRT_kwDOTH_vCM6PG65K

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/update_readme_dashboard.py:34`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/update_readme_dashboard.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR87:PRRT_kwDOTH_vCM6PG65K found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Select only completed releases for the current-release link When a future roadmap document such as docs/releases/project-far-v0.4.md exists, this max-version scan picks it' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/update_readme_dashboard.py` (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at `tools/update_readme_dashboard.py:34`: '- Candidate evidence: complete project-authored internal execution; not independent replication.'.
  - The later-change audit compared `tools/update_readme_dashboard.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR89:PRRT_kwDOTH_vCM6PRccJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `ci-and-automation`
- Current location: `.github/workflows/repository-maintenance.yml:25`
- Blocks experiment reconstruction: `false`
- Root cause: `ci-and-automation:.github/workflows/repository-maintenance.yml`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR89:PRRT_kwDOTH_vCM6PRccJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve failures from piped maintenance commands When any of these maintenance commands fails in the manual workflow, the failure can be masked because this step does not' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `.github/workflows/repository-maintenance.yml` (SHA-256 cb5a911b10c43c9b4dba9c668b084030fcb8d4787d98c60556d04c1984eb1234).
  - Current repository evidence at `.github/workflows/repository-maintenance.yml:25`: 'make dashboard 2>&1 | tee -a maintenance-summary.md'.
  - The later-change audit compared `.github/workflows/repository-maintenance.yml` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR90:PRRT_kwDOTH_vCM6PSOnQ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/update_readme_dashboard.py:36`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/update_readme_dashboard.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR90:PRRT_kwDOTH_vCM6PSOnQ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Anchor release filename matching Because this searches for vX.Y.Z anywhere in every docs/releases/project-far-v.md file, auxiliary documents such as project-far-v0.4.0-the' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/update_readme_dashboard.py` (SHA-256 08eac0a2ccf7ed653ccf116d0fbe9d6a24cd054cd1a8ca6f9d6a13cf70493a55).
  - Current repository evidence at `tools/update_readme_dashboard.py:36`: '## Historical Priority Tasks'.
  - The later-change audit compared `tools/update_readme_dashboard.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR91:PRRT_kwDOTH_vCM6PSncK

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:123`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR91:PRRT_kwDOTH_vCM6PSncK found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Synchronize the v0.4 phase label This changes the status page to say the active target is v0.4 analytical infrastructure, but the canonical README dashboard still says v0.' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:123`: '- FARM defect classification;'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR91:PRRT_kwDOTH_vCM6PSncN

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/project-status.md:135`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/project-status.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR91:PRRT_kwDOTH_vCM6PSncN found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Preserve the removed governance rules This abbreviated development order replaces the former Governance Rules section, including the stable-layer change controls and the r' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/project-status.md` (SHA-256 76618c86611c47d51224b22e4783d2f34261af57d8519dfad5d99ce485ff7f62).
  - Current repository evidence at `docs/project-status.md:135`: 'CRE-002 is complete as a prospective semantic-licensing boundary result under Baseline 1.0, and CRE-002-EXT-001 is complete as a prospective bounded behavioral result under Baseline 1.1. All three official vocabularies completed the extensi'.
  - The later-change audit compared `docs/project-status.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR92:PRRT_kwDOTH_vCM6PTVW9

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `validators-and-tooling`
- Current location: `tools/self_advancement_plan.py:9`
- Blocks experiment reconstruction: `false`
- Root cause: `validators-and-tooling:tools/self_advancement_plan.py`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR92:PRRT_kwDOTH_vCM6PTVW9 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Stage generated dependency artifacts in dashboard workflow When make dashboard runs under the regenerate-dashboard action, this new pipeline now writes docs/reports/depend' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `tools/self_advancement_plan.py` (SHA-256 e7b8e7e3cd75c6b49628936f6c030f2f2f923daa55524a0be64d52526b2fc2b2).
  - Current repository evidence at `tools/self_advancement_plan.py:9`: "GEN=[ROOT/'README.md',ROOT/'docs/planning/dashboard-metrics.md',ROOT/'docs/planning/repository-index.md',ROOT/'docs/reports/project-status-generated.md',ROOT/'docs/reports/research-gap-report.md',ROOT/'docs/planning/next-actions.md',ROOT/'d".
  - The later-change audit compared `tools/self_advancement_plan.py` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR95:PRRT_kwDOTH_vCM6PWt_O

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/foundation-validation-report.md:131`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/foundation-validation-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR95:PRRT_kwDOTH_vCM6PWt_O found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Apply the collective sufficiency criterion In contexts where normativity, semantics, or validity are supplied by FARA or later artifacts, this marks AX-001 as a sufficienc' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/foundation-validation-report.md` (SHA-256 b14995231694ccbf131a10e0d663029db0a79a923752f6bf38a89f31f1a2315f).
  - Current repository evidence at `docs/reports/foundation-validation-report.md:131`: '| Sufficiency | FAIL | Operation alone does not distinguish reasoning from arbitrary manipulation and does not supply normativity, semantic content, inferential relevance, or validity. |'.
  - The later-change audit compared `docs/reports/foundation-validation-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR96:PRRT_kwDOTH_vCM6PXUsp

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/ax001-circularity-investigation.md:394`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/ax001-circularity-investigation.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR96:PRRT_kwDOTH_vCM6PXUsp found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct "P1 Badge Demote AX-001 when the review concludes inconclusive This line explicitly decides not to revise AX-001, but the same report records that AX-001's provisional result is str" at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-circularity-investigation.md` (SHA-256 b968b115ec6e7ca126cb58a682b8c8460e615482d2326eb2bcb6137e6e016689).
  - Current repository evidence at `docs/reports/ax001-circularity-investigation.md:394`: 'No AX-001 revision is applied in this PR.'.
  - The later-change audit compared `docs/reports/ax001-circularity-investigation.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR97:PRRT_kwDOTH_vCM6PXYJT

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/ax001-primitive-candidate-adjudication.md:1`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/ax001-primitive-candidate-adjudication.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR97:PRRT_kwDOTH_vCM6PXYJT found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Add an explicit artifact status The root AGENTS instructions require compliance with docs/governance/research-execution-charter.md, which states that every artifact must h' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-primitive-candidate-adjudication.md` (SHA-256 2489f1a82d48be662bf109070c0ff286e01030e5827a10d7e60eee996ef956f7).
  - Current repository evidence at `docs/reports/ax001-primitive-candidate-adjudication.md:1`: '# AX-001 Primitive Candidate Adjudication'.
  - The later-change audit compared `docs/reports/ax001-primitive-candidate-adjudication.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR97:PRRT_kwDOTH_vCM6PXYJZ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/ax001-primitive-candidate-adjudication.md:222`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/ax001-primitive-candidate-adjudication.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR97:PRRT_kwDOTH_vCM6PXYJZ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Avoid making AX-001 depend on downstream standards If this supported wording is used for the later AX-001 edit, it imports admissibility from the surrounding theory even t' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-primitive-candidate-adjudication.md` (SHA-256 2489f1a82d48be662bf109070c0ff286e01030e5827a10d7e60eee996ef956f7).
  - Current repository evidence at `docs/reports/ax001-primitive-candidate-adjudication.md:222`: '```'.
  - The later-change audit compared `docs/reports/ax001-primitive-candidate-adjudication.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR98:PRRT_kwDOTH_vCM6PXlsJ

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/ax001-wording-revision-report.md:5`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/ax001-wording-revision-report.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR98:PRRT_kwDOTH_vCM6PXlsJ found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Do not mark pending AX-001 evidence as accepted This provenance claim says the canonical AX-001 rewrite was authorized by “accepted” prior reports, but the cited foundatio' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-wording-revision-report.md` (SHA-256 6bddcb44b8a7024843332683d898fa82873cfffa5c67c72d7e78a3f685687721).
  - Current repository evidence at `docs/reports/ax001-wording-revision-report.md:5`: 'This report records the canonical AX-001 wording revision authorized by the accepted prior AX-001 research reports. The revision retains Operation as the AX-001 candidate primitive and changes only the working characterization needed to rem'.
  - The later-change audit compared `docs/reports/ax001-wording-revision-report.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR99:PRRT_kwDOTH_vCM6PXsa1

- Disposition: `still_reproducible`
- Risk/subsystem: `high` / `documentation-and-governance`
- Current location: `docs/reports/ax001-stability-review.md:75`
- Blocks experiment reconstruction: `true`
- Root cause: `documentation-and-governance:docs/reports/ax001-stability-review.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR99:PRRT_kwDOTH_vCM6PXsa1 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P1 Badge Do not pass sufficiency via downstream theory When this gate is used to authorize L-001, resolving AX-001 sufficiency by assigning admissibility, representation, interpret' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-stability-review.md` (SHA-256 e5c8ab51daba59132a57296c714c595566d39afb5a4356e00eff50d4a72de42c).
  - Current repository evidence at `docs/reports/ax001-stability-review.md:75`: 'AX-001 now explicitly records that Operation alone does not supply normativity, semantics, validity, or warrant. This resolves the prior sufficiency pressure as a blocking issue because the primitive is no longer presented as sufficient by '.
  - The later-change audit compared `docs/reports/ax001-stability-review.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

### PR99:PRRT_kwDOTH_vCM6PXsa5

- Disposition: `still_reproducible`
- Risk/subsystem: `medium` / `documentation-and-governance`
- Current location: `docs/reports/ax001-stability-review.md:69`
- Blocks experiment reconstruction: `false`
- Root cause: `documentation-and-governance:docs/reports/ax001-stability-review.md`
- Failure mechanism: Inspection of the current repository evidence against the complete reviewer claim in finding PR99:PRRT_kwDOTH_vCM6PXsa5 found that the reported condition remains. The merged review finding is therefore a confirmed defect. This adjudication records triage only and does not repair it.
- Remediation boundary: Correct 'P2 Badge Carry forward unresolved necessity pressure This Necessity PASS drops the unresolved necessity pressure already recorded in docs/reports/foundation-validation-report.md:76' at its current authoritative source and add or update the focused validator or regression test that demonstrates the claim no longer reproduces.
- Evidence:
  - Current-main commit bb0a6fcbb213bcfa1616106344f50302b819c760 retains `docs/reports/ax001-stability-review.md` (SHA-256 e5c8ab51daba59132a57296c714c595566d39afb5a4356e00eff50d4a72de42c).
  - Current repository evidence at `docs/reports/ax001-stability-review.md:69`: 'Prior evidence found no successful non-circular reduction of Operation. The strongest replacement candidates did not eliminate primitive burden; they shifted it to reasoning states, transitions, rules, licensing, admissibility, or represent'.
  - The later-change audit compared `docs/reports/ax001-stability-review.md` from cb55c50324a9912deb8c73b62d0fbb242f026933 through 5ca27d5c40281771cf74aa29704c2a06868a16ae; no later change removed the evidenced failure mechanism.

