# Frozen merged-PR review findings

Source: `docs/audits/merged-pr-review-audit/raw-review-threads.json`

This report is fail-closed. A resolved GitHub thread is not labeled correctly resolved unless a manual evidence decision proves it.

## Summary

- Total review threads: 450
- `non_actionable`: 0
- `obsolete_after_later_changes`: 0
- `resolved_correctly`: 0
- `resolved_incorrectly`: 0
- `uncertain_manual_review_required`: 24
- `unresolved`: 426

## Findings

### PR12:PRRT_kwDOTH_vCM6OD6bR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/validation/investigations/VI-002-primitive-minimality.md:1349`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891144
- Claim: **P1 Badge Do not mark VI-002 passed before required execution** This file's own methodology requires reconstructing every affected definition/document and verifying that VI-001 remains executable, but the completed result records no suc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR12:PRRT_kwDOTH_vCM6OD6bU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/validation/investigations/VI-002-primitive-minimality.md:229`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891148
- Claim: **P2 Badge Keep the VI-002 result table in sync** This 'Current Results' table still marks Property as pending, but the same file later adds Reduction Investigation 2 and summarizes Property as 'Independent (Provisional)' in the final re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR12:PRRT_kwDOTH_vCM6OD6bV

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/proofs/conjectures.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891149
- Claim: **P2 Badge Keep conjectures in one canonical registry** This declares a Project-wide canonical conjecture registry even though 'theory/theorems/conjectures.md' already records Project FAR conjectures, including Primitive Independence, Pr...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR12:PRRT_kwDOTH_vCM6OD6bY

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/README.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/12#discussion_r3516891152
- Claim: **P2 Badge Restore the research index or update its users** Deleting this index leaves existing repository navigation and audit evidence stale: 'README.md:31' and 'docs/README.md:24' still point readers to 'research/README.md', and 'docs...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR14:PRRT_kwDOTH_vCM6OE6cl

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/proofs/theorem-catalog.md:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/14#discussion_r3517251983
- Claim: **P2 Badge Create proof files before cataloging them** This catalog now records L-001 (and the following L/P/T entries) as draft proof artifacts with canonical file paths, but I checked repo-wide with 'rg --files' for these IDs and for '...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR15:PRRT_kwDOTH_vCM6OOImd

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/definitions/graph-definitions.md:86`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/15#discussion_r3520579015
- Claim: **P2 Badge Define the path used for weak connectivity** When weak connectivity is used by the new dependency-component proof, this definition still relies on a bare 'path' after direction is ignored, but the only path definition introduc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR15:PRRT_kwDOTH_vCM6OOImg

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/proofs/FARE-P012-dependency-components.md:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/15#discussion_r3520579019
- Claim: **P2 Badge Restrict the objective to nodes in the dependency subgraph** For an assessment graph containing an assessment with no dependency edge, or only non-dependency edges, Definition 13 excludes that assessment from the dependency su...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR16:PRRT_kwDOTH_vCM6OPFvc

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/meta/README.md:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/16#discussion_r3520915239
- Claim: **P2 Badge Remove unbacked meta-theorem coverage claims** With this commit the only files in 'frameworks/FARE/meta' are M001 and M002, but this sentence says FARE meta-theorems establish traceability, investigation soundness, and proof s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR17:PRRT_kwDOTH_vCM6OR8-C

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-completion.md:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/17#discussion_r3521925204
- Claim: **P1 Badge Require completions to add missing limits** Because this obligation only covers sequences whose required limit is already represented by the proposed completion, a candidate can omit any problematic convergent sequence and sti...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR19:PRRT_kwDOTH_vCM6OSLhU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-distance.md:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/19#discussion_r3522007433
- Claim: **P2 Badge Make cost models cover every path being measured** This definition allows a transformation cost model to assign costs only to admissible transformations “under consideration,” but the distance definition below still takes the ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR19:PRRT_kwDOTH_vCM6OSLhV

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/mathematics/definitions/evaluation-neighborhood.md:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/19#discussion_r3522007434
- Claim: **P2 Badge Disambiguate 'N(E)' for chosen neighborhood systems** This introduces 'N(E)' as the collection supplied by a particular neighborhood system, but the existing Neighborhood Family section later defines 'N(E)' as every admissible...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR20:PRRT_kwDOTH_vCM6OTp-R

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARE/mathematics/theorem-index.md:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/20#discussion_r3522541518
- Claim: **P1 Badge Keep theorem identifiers unique** These new index entries reuse 'MT-001' through 'MT-003' while the existing active proofs 'frameworks/FARE/mathematics/proofs/T001-identity-path-is-geodesic.md', 'T002-path-composition-preserve...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR21:PRRT_kwDOTH_vCM6OUG3P

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/21#discussion_r3522698007
- Claim: **P2 Badge Consolidate project status into the existing status file** This adds a second current-status artifact while 'docs/PROJECT_STATUS.md' already states that it records the current state and should be updated when a significant mil...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR21:PRRT_kwDOTH_vCM6OUG3Q

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:57`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/21#discussion_r3522698008
- Claim: **P2 Badge Align FARE expansion gates with the freeze policy** This development-order rule allows FARE Mathematics to expand when FARO or FARA require it, but the same new status document's governance rules and the new milestone freeze p...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR22:PRRT_kwDOTH_vCM6OWe3V

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/CANONICAL_MAP.md:295`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/22#discussion_r3523523889
- Claim: **P1 Badge Restore removed canonical theory entries** This rewrite leaves the Theory section ending after 'Propositions', but the parent map also recorded canonical locations for Lemmas, Theorems, Conjectures, Proofs, FARO-specific defin...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR22:PRRT_kwDOTH_vCM6OWe3W

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FAR/README.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/22#discussion_r3523523890
- Claim: **P2 Badge Align FARO status with existing FARO docs** This new status says FARO development should only begin after FAR stabilizes, but the repository already contains an active 'frameworks/FARO/' tree whose README states that FARO cons...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR23:PRRT_kwDOTH_vCM6OWoTz

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/23#discussion_r3523577636
- Claim: **P2 Badge Define candidate generation in the canonical workflow** This closes the earlier gap by saying candidate generation is explicitly placed in Stage 6, but the commit never updates 'frameworks/FAR/workflow.md', which the FAR docs ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR23:PRRT_kwDOTH_vCM6OWoT2

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FAR/README.md:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/23#discussion_r3523577639
- Claim: **P2 Badge Advance FAR status past the completed Phase 2 gate** This updated status is now inconsistent with the same commit's audit record, which marks Phase 2 complete and says FAR is ready to proceed to Phase 3 methodology audit; 'met...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR24:PRRT_kwDOTH_vCM6OXXCe

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md:253`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/24#discussion_r3523827593
- Claim: **P2 Badge Do not mark Phase 3 complete while application is stale** The audit lists 'frameworks/FAR/application.md' as reviewed, but that document was not updated for this Phase 3 policy change: its application requirements still end at...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR24:PRRT_kwDOTH_vCM6OXXCg

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FAR/workflow.md:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/24#discussion_r3523827596
- Claim: **P2 Badge Require revision records in the canonical workflow** The new stability criterion says FAR shall require revision records whenever an investigation revisits an earlier stage ('FAR-v1.0-criteria.md' line 67), but the canonical w...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR26:PRRT_kwDOTH_vCM6OXzM2

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md:284`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/26#discussion_r3523976424
- Claim: **P2 Badge Keep FAR status docs synchronized before passing the audit** This pass is used to clear the v1.0 gate, but in the repository context I inspected 'frameworks/FAR/methodology.md' still says the current work is the Phase 3 method...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR27:PRRT_kwDOTH_vCM6OX64p

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/27#discussion_r3524017502
- Claim: **P2 Badge Keep the FARE expansion rule consistent** This broadens the governance rule to allow new FARE definitions when FAR, FARO, or FARA requires them, but the same status document still says FARE Mathematics v0.1 “shall not expand u...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR27:PRRT_kwDOTH_vCM6OX64q

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md:33`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/27#discussion_r3524017503
- Claim: **P2 Badge Update FAR status before freezing it** This milestone designates 'frameworks/FAR/README.md' as Stable, but that file's Current Status still says FAR is only eligible for a stable freeze after review/merge and that FARO should ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR28:PRRT_kwDOTH_vCM6OYVb4

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARO/architecture.md:84`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/28#discussion_r3524161830
- Claim: **P2 Badge Add the missing FARE dependency field** The architecture checklist says every FARO operation shall specify these dependencies, but it skips the 'FARE Dependency' field that 'operation-interface-standard.md' makes required, inc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR28:PRRT_kwDOTH_vCM6OYVb5

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARO/execution.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/28#discussion_r3524161831
- Claim: **P2 Badge Clarify whether execution may determine admissibility** This exception makes execution operations allowed to determine admissibility when they use a defined FAR reasoning calculus, but the same new document states that “Execut...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR29:PRRT_kwDOTH_vCM6OYXwk

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/29#discussion_r3524174855
- Claim: **P2 Badge Update FARO README status for Phase 8** When this status document moves active development to Phase 8, 'frameworks/FARO/README.md' still says FARO has entered Phase 7 architecture stabilization and its notes still tell readers...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR30:PRRT_kwDOTH_vCM6OYbcS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/30#discussion_r3524194993
- Claim: **P2 Badge Rework the failure-mode pass before advancing Phase 8** This pass result is not supported by the referenced category documents: in 'frameworks/FARO/{execution,reporting,operational-evaluation}.md', there is no category-level f...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR31:PRRT_kwDOTH_vCM6OYchc

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/31#discussion_r3524200707
- Claim: **P2 Badge Keep the audit-record gate in the criteria** When the stable milestone relies on this Phase 9 finding, it now claims the criteria document records the required audit records, but this same commit replaced the prior 'Audit Reco...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR32:PRRT_kwDOTH_vCM6OYfSA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `README.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/32#discussion_r3524214858
- Claim: **P2 Badge Update canonical FARO status before declaring stability** This declaration conflicts with unchanged canonical FARO docs: 'frameworks/FARO/README.md:13-15' still says FARO is only eligible and not formally v1.0 Stable until the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR33:PRRT_kwDOTH_vCM6OYgsA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:64`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/33#discussion_r3524222522
- Claim: **P2 Badge Do not let unproven FARM drive FARE expansion** While the Phase 10 audit still has to decide whether FARM should exist and the milestone says FARM must prove responsibilities before canonical expansion, this effective-immediat...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR34:PRRT_kwDOTH_vCM6OYk4w

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/FARM-PHASE-10-ARCHITECTURE-AUDIT.md:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/34#discussion_r3524245031
- Claim: **P2 Badge Archive the superseded Phase 10 audit record** By deleting this initiated audit instead of archiving or recording it as superseded, the current tree loses the only in-repository provenance that FARM planning originally opened ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR35:PRRT_kwDOTH_vCM6OYx2-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `frameworks/FARM/README.md:31`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/35#discussion_r3524315327
- Claim: **P2 Badge Add FARM canonical documents to the canonical map** These new FARM files are now presented as canonical documents, but 'docs/CANONICAL_MAP.md' still has no FARM section or entries (I checked the map and repo-wide FARM referenc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR36:PRRT_kwDOTH_vCM6OZFPU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/36#discussion_r3524419058
- Claim: **P2 Badge Sync the FARM README before closing Phase 4** With this update, project status says Phase 3 and Phase 4 are complete, but 'frameworks/FARM/README.md' still says the Phase 3 methodology audit is initiated and its next step is t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR37:PRRT_kwDOTH_vCM6OZK28

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/37#discussion_r3524449019
- Claim: **P2 Badge Align the FARM stable component scope** This adds the Phase 1 through Phase 4 audit records to the FARM stable component set, but the new 'docs/milestones/FARM-v1.0-Stable.md' Stable Components section lists only the eight 'fr...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR38:PRRT_kwDOTH_vCM6ObcXR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/38#discussion_r3525237179
- Claim: **P2 Badge Recheck placeholder search before recording a pass** The repository already contains matches for this search, so the audit records a false preliminary pass. In the parent tree, 'git grep -n -i -E '\b(dummy|temp|placeholder|TOD...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR39:PRRT_kwDOTH_vCM6ObfIA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md:63`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/39#discussion_r3525252152
- Claim: **P2 Badge Reopen the FARE alignment check** This pass is inaccurate for the post-v1 stack: in this commit, 'README.md''s navigation/reading order lists framework material for FAR/FARA/FARO/FARM but omits FARE, and 'docs/CANONICAL_MAP.md...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR40:PRRT_kwDOTH_vCM6OcdQT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/CANONICAL_MAP.md:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/40#discussion_r3525600994
- Claim: **P2 Badge Restore the missing FARE canonical components** When contributors use this new map as the FARE navigation hub, it drops canonical FARE components that the authoritative FARE spec defines at 'frameworks/FARE/specification.md' l...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR48:PRRT_kwDOTH_vCM6Ofq_j

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/roadmap/v0.2.0-next-phase.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/48#discussion_r3526754282
- Claim: **P2 Badge Align the roadmap version with the active milestone** This introduces a new 'v0.2.0' next-phase roadmap even though the repository already records 'docs/releases/project-far-v0.4.md' as the active roadmap milestone and lists t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR49:PRRT_kwDOTH_vCM6Of2J_

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/verify_theory.py:201`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/49#discussion_r3526816607
- Claim: **P2 Badge Include non-theorem nodes in the cycle graph** When proposition/lemma metadata is validated, dependencies involving those IDs are accepted as known dependencies but never inserted into the graph passed to 'validate_no_cycles()...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR49:PRRT_kwDOTH_vCM6Of2KD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/metadata/generated-proposition-index.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/49#discussion_r3526816612
- Claim: **P2 Badge Include P-009 in the generated index** 'theory/metadata/propositions.yaml' adds 'P-009' and the proposition catalog contains it, but the committed generated proposition index stops at 'P-008'. Anyone using this generated index...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR51:PRRT_kwDOTH_vCM6OgLyL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/verify_theory.py:154`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/51#discussion_r3526938355
- Claim: **P2 Badge Preserve ID checks for existing catalogs** Because this helper is still used for propositions and lemmas, accepting a title match means a metadata entry with a mistyped or stale 'P-*'/'L-*' id now passes as long as the source ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR52:PRRT_kwDOTH_vCM6OgR7W

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-001.proof.yaml:30`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/52#discussion_r3526972612
- Claim: **P2 Badge Add the definition dependency to T-001 metadata** This proof object now makes 'DEF-019' an explicit premise for proving 'T-001', but 'theory/metadata/theorems.yaml' still lists only 'L-001' through 'L-005' as T-001 dependencie...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR53:PRRT_kwDOTH_vCM6OgVPb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-002.proof.yaml:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/53#discussion_r3526991258
- Claim: **P2 Badge Model the countermodel obligations as inputs** Here 'p2' is only the conditional proof method and 'p4' only states L-001's necessity claim; the proof object never establishes the antecedent that a countermodel with the other f...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR54:PRRT_kwDOTH_vCM6OgbqU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-003.proof.yaml:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/54#discussion_r3527026847
- Claim: **P2 Badge Prove T exists before conjoining it** When 'R' has no specified transition executions, 's6' only establishes a conditional/permission that 'T' may be empty or partial; it does not assert an existing trace component for that ca...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR54:PRRT_kwDOTH_vCM6OgbqY

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-003.proof.yaml:97`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/54#discussion_r3527026851
- Claim: **P2 Badge Use universal generalization for arbitrary R** This step derives a universal theorem from the construction for an arbitrary 'R', but labels the inference as 'universal_instantiation', which goes in the opposite direction: from...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR55:PRRT_kwDOTH_vCM6OgvoF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-005.proof.yaml:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/55#discussion_r3527139355
- Claim: **P2 Badge Preserve L-008 in the T-005 proof object** For T-005, 'theory/metadata/theorems.yaml' lists 'L-008' as a dependency, and 'theory/lemmas/core-lemmas.md' uses that lemma to require source state, target state, rule, and admissibi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR55:PRRT_kwDOTH_vCM6OgvoG

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-006.proof.yaml:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/55#discussion_r3527139356
- Claim: **P2 Badge Do not add an uncited induction premise** T-006 is registry-relative: its documented dependencies are the derived-concept registry and canonical notation, but this proof object introduces 'induction principle over registry dep...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR56:PRRT_kwDOTH_vCM6OhRaY

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-008.proof.yaml:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332927
- Claim: **P2 Badge Establish interpretation preservation before concluding semantics** For canonical representations where the role pairing has only been shown to preserve structure/admissibility/trace order, 's3' is still conditional on the pai...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR56:PRRT_kwDOTH_vCM6OhRab

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-009.proof.yaml:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332931
- Claim: **P2 Badge Keep L-007's termination precondition explicit** For a finite FAR representation whose supplied ordering/labeling/redundancy rules are not known to strictly reduce unresolved items, L-007 does not by itself prove termination; ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR56:PRRT_kwDOTH_vCM6OhRac

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-010.proof.yaml:49`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/56#discussion_r3527332933
- Claim: **P2 Badge Avoid applying T-009 outside finite normalized cases** T-010's premise is only a complete FAR representation, but T-009 is scoped to finite FAR representations with supplied normalization rules. For complete representations th...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR57:PRRT_kwDOTH_vCM6OpqRi

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-012.proof.yaml:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/57#discussion_r3530345511
- Claim: **P2 Badge Attribute Q-equivalence definitions to an existing source** These premises cite 'FAR-model-theory', but the model-theory file only defines equivalence as preservation over a property set ('theory/model-theory/FAR-model-theory....
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR58:PRRT_kwDOTH_vCM6Op8yy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_proof_object.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/58#discussion_r3530450208
- Claim: **P2 Badge Require more than word overlap for conclusions** When a proof object changes the final step and 'conclusion' to a weaker or contradictory phrase that reuses theorem words, this ratio can still pass; for example, a T-003 proof ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR61:PRRT_kwDOTH_vCM6OrXNb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/language/statement-schema.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/61#discussion_r3530966646
- Claim: **P2 Badge Allow existing artifact statement kinds** When this schema is used to validate current metadata, this allowed set omits the values the repository already stores for statement objects ('theorem', 'proposition', 'lemma', 'defini...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR64:PRRT_kwDOTH_vCM6OuI1o

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_proof_object.py:329`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/64#discussion_r3531970829
- Claim: **P2 Badge Accept symbolic antecedents for ASCII modus ponens** When a proof object uses the documented modus-ponens shape 'P' plus 'P -> Q' (the same symbolic content added in the new fixture), the new '->' vocabulary check succeeds but...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR64:PRRT_kwDOTH_vCM6OuI1r

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_proof_object.py:311`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/64#discussion_r3531970832
- Claim: **P2 Badge Preserve canonical SemanticContent vocabulary matches** For a 'semantic_preservation' step whose inputs express semantic content only in canonical notation such as 'SemanticContent(Int1, r)' and do not also cite 'T-004'/'DEF-0...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR66:PRRT_kwDOTH_vCM6OuixP

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/evaluate_reasoning_systems.py:195`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/66#discussion_r3532118049
- Claim: **P2 Badge Fail CI when any fixture fails classification** When a reasoning-system fixture is syntactically valid but missing the 'reasoning_system' mapping or using an unsupported verdict, 'classify_fixture()' reports 'fails fixture', b...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR67:PRRT_kwDOTH_vCM6OuqYN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `examples/far/reasoning-systems/inconsistent-calculus.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162034
- Claim: **P1 Badge Use the accepted inconsistent-calculus classification** When 'tools/evaluate_reasoning_systems.py' evaluates this fixture, 'falsifies FAR' is mapped into 'candidate counterexample', so this line turns the inconsistent-calculus...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR67:PRRT_kwDOTH_vCM6OuqYV

- Disposition: `unresolved`
- Confidence: `high`
- Location: `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162043
- Claim: **P1 Badge Do not classify opaque intuition as a FAR falsification** With this verdict, the evaluator records the opaque-oracle fixture as a 'candidate counterexample', but the repository's existing scope test for private intuition with ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR67:PRRT_kwDOTH_vCM6OuqYa

- Disposition: `unresolved`
- Confidence: `high`
- Location: `examples/far/reasoning-systems/paradox.far.yaml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/67#discussion_r3532162047
- Claim: **P1 Badge Keep paradox as representable boundary evidence** This verdict causes the paradox fixture to be counted as a 'candidate counterexample', but 'theory/tests/falsification-tests-advanced.md' Test A3 explicitly says FAR can repres...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR70:PRRT_kwDOTH_vCM6OvPip

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/releases/project-far-v0.2.0.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/70#discussion_r3532377341
- Claim: **P1 Badge Declare the release artifact status** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to possess exactly one status ('Accepted', 'Res...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR70:PRRT_kwDOTH_vCM6OvPir

- Disposition: `unresolved`
- Confidence: `high`
- Location: `README.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/70#discussion_r3532377343
- Claim: **P2 Badge Synchronize the README release pointers** When readers use the README for release navigation, this new section says v0.2.0 is the latest release, but the same README still has a 'Releases' section listing only v0.1.0 and the t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR71:PRRT_kwDOTH_vCM6OvQSt

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/releases/release-publication-instructions-v0.2.0.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/71#discussion_r3532381647
- Claim: **P2 Badge Pin the release target to an exact commit** If publication happens after any later commit lands on 'main', this instruction tells the releaser to create the 'v0.2.0' tag on that newer tree, so the frozen v0.2.0 evidence baseli...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR72:PRRT_kwDOTH_vCM6Ovhp9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/evaluate_primitive_sufficiency.py:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/72#discussion_r3532480869
- Claim: **P2 Badge Preserve registry validation output for malformed entries** When a registry entry is missing a required field, 'validate_entries()' records the error but 'render_report()' immediately indexes 'entry["classification"]', so the ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR74:PRRT_kwDOTH_vCM6Owd-U

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/evidence-registry.yaml:124`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/74#discussion_r3532823883
- Claim: **P2 Badge Use the fixture classification taxonomy** 'classification' is the fixture/evidence classification consumed by the falsification harness, whose documented valid values are 'fits FAR', 'extends FAR', 'candidate counterexample', ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR74:PRRT_kwDOTH_vCM6Owd-X

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/primitive-sufficiency-report.md:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/74#discussion_r3532823886
- Claim: **P2 Badge Recompute the fits-FAR headline count** The registry now has 7 entries with 'classification: fits FAR' and only 2 entries with 'registry_resolution: fits FAR'; the reported 9 is the sum of those two sets, double-counting PS-02...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR75:PRRT_kwDOTH_vCM6Owjky

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/run_adversarial_suite.py:164`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/75#discussion_r3532856039
- Claim: **P2 Badge Cross-check the pressure registry** This runner only loads and validates '--suite', so the new 'theory/falsification/primitive-pressure-registry.yaml' is never read. Because that registry duplicates the suite’s primitive/syste...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR76:PRRT_kwDOTH_vCM6OwvGp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/falsification/adversarial-test-suite.yaml:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/76#discussion_r3532924506
- Claim: **P2 Badge Recognize the new adversarial status labels** When the suite is summarized with 'tools/run_adversarial_suite.py', this new label (and the new 'conservative extension'/'unresolved pressure' labels) is not in the runner's 'PASSE...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR77:PRRT_kwDOTH_vCM6Ow2uM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/releases/github-release-v0.3.0.md:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/77#discussion_r3532968753
- Claim: **P2 Badge Use release-safe links in GitHub notes** If this file is pasted into a GitHub Release body, these '../reports/...' and same-directory relative links are no longer resolved relative to 'docs/releases'; they resolve from the rel...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR80:PRRT_kwDOTH_vCM6Ox91X

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_internal_links.py:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/80#discussion_r3533389790
- Claim: **P2 Badge Restrict YAML extraction to actual path fields** For YAML files that contain slash-delimited terms in prose or titles, this extracts those terms as repository paths even when they are not links; for example the current repo re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR80:PRRT_kwDOTH_vCM6Ox91b

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_internal_links.py:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/80#discussion_r3533389794
- Claim: **P2 Badge Resolve YAML repository paths from the root** When a nested YAML file contains a repository-root-relative path, this resolves it relative to the YAML file's directory and reports a false broken link; for example 'theory/metada...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR81:PRRT_kwDOTH_vCM6O9Ugn

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-validation-methodology.md:82`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/81#discussion_r3537532171
- Claim: **P2 Badge Require reproducible evidence in external reports** The reporting standard lets an external-system report be complete with only mapping/classification/justification prose, but no source/version, fixture, execution record, obse...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR81:PRRT_kwDOTH_vCM6O9Ugr

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-validation-registry.yaml:24`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/81#discussion_r3537532174
- Claim: **P2 Badge Classify Coq consistently as conservative** Under the new classification rules, 'fits FAR' is for systems that do not need domain-specific extension machinery, while 'conservative extension' is for systems requiring domain-spe...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR82:PRRT_kwDOTH_vCM6PEMp-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-systems/constraint-solving.md:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/82#discussion_r3540029610
- Claim: **P2 Badge Reclassify constraint solving by the stated rule** The report identifies “domain-specific propagation and search” as pressure and says domain-specific propagators are required, but the v0.4.0 external-validation methodology re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR82:PRRT_kwDOTH_vCM6PEMqC

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-systems/linear-logic.md:31`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/82#discussion_r3540029617
- Claim: **P2 Badge Add the required remaining-questions sections** The reporting standard in 'theory/evaluation/external-validation-methodology.md' says every system report must include remaining questions. This new report stops at Confidence, a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR84:PRRT_kwDOTH_vCM6PEqVg

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_release_consistency.py:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/84#discussion_r3540197240
- Claim: **P2 Badge Anchor release-section detection to the heading** In the current README the first occurrence of “Release” is the badge near the top, so this unanchored regex captures the badge/intro block rather than the '## Latest Release' s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR84:PRRT_kwDOTH_vCM6PEqVh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_repository_hygiene.py:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/84#discussion_r3540197241
- Claim: **P2 Badge Validate collected registry IDs before passing** When a non-adversarial registry file contains duplicate 'id' values, they are collected into 'registry_ids' here but that map is never inspected before the script prints success...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR85:PRRT_kwDOTH_vCM6PEvgp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/generate_next_tasks.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/85#discussion_r3540227276
- Claim: **P2 Badge Resolve gap labels to actual editable files** When the gap row comes from a registry entry or primitive pressure, 'g['loc']' is a logical label such as 'PS-001' or 'Reasoning Calculus', not a repository path. This value is the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR85:PRRT_kwDOTH_vCM6PEvgt

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/detect_research_gaps.py:55`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/85#discussion_r3540227280
- Claim: **P2 Badge Sort scanned markdown files before assigning gap IDs** When regenerating the committed reports, this loop emits TODO gaps in the filesystem's 'rglob' traversal order, which is not stable; in this checkout, running the planner ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR86:PRRT_kwDOTH_vCM6PFwgS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/detect_research_gaps.py:55`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/86#discussion_r3540603299
- Claim: **P2 Badge Sort TODO scans before assigning gap IDs** When the planner is rerun via 'make plan'/'python tools/self_advancement_plan.py', this filesystem-order traversal feeds directly into the 'gaps' list and then into 'enumerate(gaps, 1...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR87:PRRT_kwDOTH_vCM6PG65I

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/update_readme_dashboard.py:86`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/87#discussion_r3541030301
- Claim: **P1 Badge Exclude interpreter caches from generated repository indexes** When a developer has Python bytecode under 'tools/__pycache__', this recursive scan indexes those local cache files; the committed 'docs/planning/repository-index....
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR87:PRRT_kwDOTH_vCM6PG65K

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/update_readme_dashboard.py:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/87#discussion_r3541030305
- Claim: **P2 Badge Select only completed releases for the current-release link** When a future roadmap document such as 'docs/releases/project-far-v0.4.md' exists, this max-version scan picks it even though that file is marked as an active roadm...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR89:PRRT_kwDOTH_vCM6PRccJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/repository-maintenance.yml:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/89#discussion_r3544797401
- Claim: **P2 Badge Preserve failures from piped maintenance commands** When any of these maintenance commands fails in the manual workflow, the failure can be masked because this step does not set 'shell: bash' or 'pipefail'; GitHub's workflow s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR90:PRRT_kwDOTH_vCM6PSOnQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/update_readme_dashboard.py:36`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/90#discussion_r3545074995
- Claim: **P2 Badge Anchor release filename matching** Because this searches for 'vX.Y.Z' anywhere in every 'docs/releases/project-far-v*.md' file, auxiliary documents such as 'project-far-v0.4.0-theory-freeze.md' or 'project-far-v0.4.0-roadmap.m...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR91:PRRT_kwDOTH_vCM6PSncK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/91#discussion_r3545213004
- Claim: **P2 Badge Synchronize the v0.4 phase label** This changes the status page to say the active target is v0.4 analytical infrastructure, but the canonical README dashboard still says 'v0.4 external validation preparation', and 'tools/updat...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR91:PRRT_kwDOTH_vCM6PSncN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/project-status.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/91#discussion_r3545213010
- Claim: **P2 Badge Preserve the removed governance rules** This abbreviated development order replaces the former Governance Rules section, including the stable-layer change controls and the rule that draft theorems are not accepted dependencies...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR92:PRRT_kwDOTH_vCM6PTVW9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/self_advancement_plan.py:9`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/92#discussion_r3545471390
- Claim: **P2 Badge Stage generated dependency artifacts in dashboard workflow** When 'make dashboard' runs under the regenerate-dashboard action, this new pipeline now writes 'docs/reports/dependency-report.md', 'docs/reports/dependency-graph.js...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR95:PRRT_kwDOTH_vCM6PWt_O

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-validation-report.md:131`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/95#discussion_r3546692054
- Claim: **P1 Badge Apply the collective sufficiency criterion** In contexts where normativity, semantics, or validity are supplied by FARA or later artifacts, this marks AX-001 as a sufficiency **FAIL** using a stricter test than the repository ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR96:PRRT_kwDOTH_vCM6PXUsp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-circularity-investigation.md:394`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/96#discussion_r3546909128
- Claim: **P1 Badge Demote AX-001 when the review concludes inconclusive** This line explicitly decides not to revise AX-001, but the same report records that AX-001's provisional result is stronger than the evidence warrants and is in tension wi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR97:PRRT_kwDOTH_vCM6PXYJT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-primitive-candidate-adjudication.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/97#discussion_r3546928509
- Claim: **P2 Badge Add an explicit artifact status** The root AGENTS instructions require compliance with 'docs/governance/research-execution-charter.md', which states that every artifact must have exactly one status from Accepted/Research/Provi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR97:PRRT_kwDOTH_vCM6PXYJZ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-primitive-candidate-adjudication.md:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/97#discussion_r3546928515
- Claim: **P2 Badge Avoid making AX-001 depend on downstream standards** If this supported wording is used for the later AX-001 edit, it imports admissibility from the surrounding theory even though 'foundation-validation-report.md' stopped downs...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR98:PRRT_kwDOTH_vCM6PXlsJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-wording-revision-report.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/98#discussion_r3547003884
- Claim: **P2 Badge Do not mark pending AX-001 evidence as accepted** This provenance claim says the canonical AX-001 rewrite was authorized by “accepted” prior reports, but the cited foundation report explicitly records Human Adjudication as pen...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR99:PRRT_kwDOTH_vCM6PXsa1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-stability-review.md:75`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/99#discussion_r3547041586
- Claim: **P1 Badge Do not pass sufficiency via downstream theory** When this gate is used to authorize L-001, resolving AX-001 sufficiency by assigning admissibility, representation, interpretation, structure, calculus, trace, and warrant to sur...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR99:PRRT_kwDOTH_vCM6PXsa5

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/ax001-stability-review.md:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/99#discussion_r3547041592
- Claim: **P2 Badge Carry forward unresolved necessity pressure** This Necessity PASS drops the unresolved necessity pressure already recorded in 'docs/reports/foundation-validation-report.md:76' and 'docs/reports/foundation-validation-report.md:...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR100:PRRT_kwDOTH_vCM6PX2kN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/appendices/l001-blind-formalization-raw.md:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/100#discussion_r3547099165
- Claim: **P1 Badge Use the canonical D-REP in the blind inputs** This blind prompt defines 'representation' as an explicit artifact/structure/expression/object made available for Project FAR analysis, but the canonical D-REP in 'theory/definitio...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR100:PRRT_kwDOTH_vCM6PX2kS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/appendices/l001-adversarial-review-raw.md:148`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/100#discussion_r3547099172
- Claim: **P1 Badge Restore the omitted adversarial objections** Under the 'Complete output' section, the raw adversarial transcript jumps from Objection 2 to Objection 11, while the final defeat table later lists omitted objections such as categ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR101:PRRT_kwDOTH_vCM6PYy6a

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/doctrine/isolation-classification.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/101#discussion_r3547436795
- Claim: **P2 Badge Record provenance before marking doctrine accepted** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', which limits artifact statuses to 'Accepted', 'Research', 'Provisional', 'Arch...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR102:PRRT_kwDOTH_vCM6PZNLb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/lemmas/core-lemmas.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/102#discussion_r3547586005
- Claim: **P2 Badge Define 'participating collection' before canonical use** When downstream users consume 'core-lemmas.md' as the canonical lemma source, this revised statement relies on 'participating collection of representations' as if it wer...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR103:PRRT_kwDOTH_vCM6PZYQQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/l003-validation-report.md:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/103#discussion_r3547648976
- Claim: **P2 Badge Track D-INV as a required L-003 dependency** The revised L-003 statement now makes 'within an investigation' part of the condition, and this row itself says that investigation context is necessary to state the clarified result...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR107:PRRT_kwDOTH_vCM6Paisx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/lemmas/core-lemmas.md:85`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/107#discussion_r3548071734
- Claim: **P1 Badge Propagate L-007's new preconditions downstream** The revised L-007 is now only applicable when each step decreases a finite unresolved-item measure and introduces no new unresolved item, but T-009 still declares a dependency o...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR107:PRRT_kwDOTH_vCM6Pais0

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/l007-validation-report.md:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/107#discussion_r3548071738
- Claim: **P2 Badge Register the new L-007 proof obligations** This report states that the core proof now directly depends on finite unresolved-item measure and the no-new-unresolved-item condition, but it also records that no dependency registry...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR110:PRRT_kwDOTH_vCM6PcQlI

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-validation-consolidation.md:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/110#discussion_r3548711972
- Claim: **P2 Badge Avoid retroactively labeling earlier validations as I1** When readers use this consolidation as the single status artifact for the AX-001→T-001 chain, this sentence overstates the evidence for the first links: the L-001 report...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR111:PRRT_kwDOTH_vCM6PctNL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proofs/T-002-primitive-independence.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/111#discussion_r3548874172
- Claim: **P2 Badge Update theorem catalogs after narrowing T-002** Because this line narrows T-002 from derivability to deletion-only eliminability, the companion catalogs now publish a stronger theorem than the proof establishes: 'theory/theore...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR112:PRRT_kwDOTH_vCM6PcwlR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proofs/P-001-first-propositions.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893237
- Claim: **P2 Badge Align P-002 metadata with the revised proposition** This narrows the canonical P-002 wording, but the machine-readable P-002 entry still records the old scope/claim in 'theory/metadata/propositions.yaml:20-31', so 'theory/meta...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR112:PRRT_kwDOTH_vCM6PcwlS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/p003-validation-report.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893239
- Claim: **P2 Badge Register the semantic-content dependency for P-003** The audit classifies the semantic content definition as logically required, but the next line leaves metadata unchanged; checked 'theory/metadata/propositions.yaml', and P-0...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR112:PRRT_kwDOTH_vCM6PcwlU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/p004-validation-report.md:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/112#discussion_r3548893242
- Claim: **P2 Badge Reconcile the P-004 D-INT dependency** This audit downgrades 'D-INT' to informative and then says no metadata correction is needed, but 'theory/metadata/propositions.yaml:51-54' still declares 'D-INT' as a P-004 dependency. Un...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR113:PRRT_kwDOTH_vCM6PdBj1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/metadata/theorems.yaml:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/113#discussion_r3548990147
- Claim: **P2 Badge Keep DEF-033 while the proof object still uses it** With this dependency list reduced to only 'DEF-030', 'DEF-031', and 'DEF-034', T-004's machine proof object still cites 'DEF-033' as premise 'p4' and routes it through 's4' i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR114:PRRT_kwDOTH_vCM6PdHTG

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/t005-validation-report.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/114#discussion_r3549023686
- Claim: **P1 Badge Stop acceptance until dependencies are validated** When this report is used as the acceptance record for T-005, the 'ACCEPT' recommendation skips required upstream validation: the report later lists L-008 and T-003 as logicall...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR115:PRRT_kwDOTH_vCM6PdLxu

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proofs/T-006-primitive-sufficiency.md:32`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/115#discussion_r3549050385
- Claim: **P2 Badge Restore canonical notation dependency** When T-006 is treated as an Established proof under the repo's documented verification gates, this dependency rewrite drops 'theory/notation/canonical-notation.md' even though 'theory/ve...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR116:PRRT_kwDOTH_vCM6PdVsa

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/t008-validation-report.md:151`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/116#discussion_r3549107828
- Claim: **P1 Badge Resolve the remaining preservation premise** When a shared required-role inventory pairs roles but does not itself define those occupants as preserving structural relation, assigned meaning, admissibility, and trace order, the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR116:PRRT_kwDOTH_vCM6PdVsb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/dependencies/dependency-graph.md:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/116#discussion_r3549107831
- Claim: **P2 Badge Update the stale T-008 circularity audit** After dropping 'T-003' from T-008 here, the current circularity audit still lists 'Dependencies: L-006, T-003, T-004' for T-008 ('theory/audits/circularity-audit-001.md:94') even thou...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR117:PRRT_kwDOTH_vCM6Pdln3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proofs/T-009-canonical-normal-form.md:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/117#discussion_r3549198406
- Claim: **P2 Badge Require terminal zero-unresolved state for normal form** The revised proof uses L-007 to get termination, but termination only says every performed step decreases the finite unresolved-item measure; it does not establish that ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR117:PRRT_kwDOTH_vCM6Pdln5

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/t009-validation-report.md:5`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/117#discussion_r3549198409
- Claim: **P2 Badge Align T-009 status with the REVISE outcome** This report records the final recommendation as REVISE and later says the stopping rule prevents T-010 from beginning, but the same patch leaves T-009 advertised as 'Established' in...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR118:PRRT_kwDOTH_vCM6Pd0Mn

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-010.proof.yaml:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283458
- Claim: **P1 Badge Use a supported proof-step rule** With this new 'prior_proposition' rule, the proof object no longer satisfies the repository's proof-object schema: 'tools/verify_theory.py' and 'tools/check_proof_object.py' only allow the rul...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR118:PRRT_kwDOTH_vCM6Pd0Mr

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-010.proof.yaml:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283463
- Claim: **P1 Badge Cite the completeness definition by a resolvable ID** This premise source is not resolvable by the strict proof-object checker, which accepts metadata IDs/aliases such as 'DEF-038' or approved base sources, not definition titl...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR118:PRRT_kwDOTH_vCM6Pd0Mv

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-010.proof.yaml:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/118#discussion_r3549283467
- Claim: **P1 Badge Make the conclusion match a proved step** The new conclusion text no longer exactly matches any proof step statement after 's7' was removed and 's6' kept a shorter statement. Both 'validate_required_proof_objects()' in 'tools/...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR119:PRRT_kwDOTH_vCM6Pd8Rn

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proofs/T-011-conservative-extension.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/119#discussion_r3549330195
- Claim: **P1 Badge Preserve proposition and lemma inputs before claiming proof preservation** The revised condition still only freezes axioms and theorem statements/dependencies, but established core proofs also use lemmas and propositions: for ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR119:PRRT_kwDOTH_vCM6Pd8Rq

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/metadata/theorems.yaml:234`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/119#discussion_r3549330200
- Claim: **P2 Badge Align D-026 with the revised conservative-extension scope** This narrowed T-011 scope is not propagated to the canonical derived concept it still advertises: 'D-026' in 'theory/derivations/derived-concept-registry.md' still de...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR120:PRRT_kwDOTH_vCM6Pp34s

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/proof-object-schema.yaml:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/120#discussion_r3553611046
- Claim: **P2 Badge Document prior_proposition in the canonical rule list** Adding 'prior_proposition' here makes the checker accept a rule that still has no entry in 'theory/proof-objects/proof-step-rules.md', even though that document says it d...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR123:PRRT_kwDOTH_vCM6PqmUy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-final-consolidation-report.md:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/123#discussion_r3553876154
- Claim: **P2 Badge Don't clear wording mismatches while P-001 still diverges** This blanket conclusion misses an existing canonical catalog/proof mismatch in the audited P-series scope: 'docs/CANONICAL_MAP.md' identifies 'theory/theorems/proposi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR124:PRRT_kwDOTH_vCM6Pq9Nm

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-final-consolidation-report.md:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/124#discussion_r3554005850
- Claim: **P1 Badge Keep status inconsistent until backfills avoid downstream use** This status is not supported by the new backfill artifacts: the reports/raw appendices validate earlier artifacts while supplying 'P-001 through P-008' and 'T-001...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR126:PRRT_kwDOTH_vCM6Pr4ri

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-health-verification.md:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/126#discussion_r3554346049
- Claim: **P2 Badge Include the full warning scope** In this commit, the recorded remaining-warning scope is narrower than the checks actually report: 'python tools/check_orphaned_docs.py' emits orphan warnings for 'docs/*', 'docs/reports/appendi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR127:PRRT_kwDOTH_vCM6Pr_pZ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/foundation-consistency-audit.md:93`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/127#discussion_r3554385195
- Claim: **P2 Badge Link the new audit before calling orphan warnings pre-existing** When 'python tools/validate_docs.py' runs after this commit, 'tools/check_orphaned_docs.py' now reports 'WARN orphaned doc: docs/reports/foundation-consistency-a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR128:PRRT_kwDOTH_vCM6PsH-G

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/canonical-mathematics-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/128#discussion_r3554432485
- Claim: **P2 Badge Include registered derived concepts in the audit** When this report is used as the canonical mathematics inventory, the headline counts and inventory are incomplete: 'theory/derivations/derived-concept-registry.md' registers D...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR129:PRRT_kwDOTH_vCM6PsZxY

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/metadata/axioms.yaml:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/129#discussion_r3554535845
- Claim: **P2 Badge Preserve AX-001 draft status in metadata** When consumers use 'theory/metadata/axioms.yaml' or the generated axiom index as the canonical registry, this marks AX-001 as 'Established' even though its canonical source ('research...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR131:PRRT_kwDOTH_vCM6PuJ6w

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/dependency-audit.md:130`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/131#discussion_r3555177444
- Claim: **P2 Badge Do not make deferred theorems validation blockers** These steps make T-013–T-015 prerequisites for Phase 1 Step 7, but I checked the existing Phase 1 canonicalization resolution and it explicitly handled the fact that local me...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR132:PRRT_kwDOTH_vCM6PubMj

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/l008-validation-report.md:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/132#discussion_r3555277773
- Claim: **P1 Badge Exclude L-008-dependent T-005 from the foundation set** When this report is used as validation evidence for L-008, the stated supplied foundation includes T-001 through T-012; in this repo that includes T-005, whose metadata a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR133:PRRT_kwDOTH_vCM6PueMQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/dependencies/dependency-graph.md:155`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/133#discussion_r3555294440
- Claim: **P2 Badge Update the current circularity audit for T-013** Removing 'T-005' here makes the current dependency sources disagree: 'theory/audits/circularity-audit-001.md' still lists T-013 dependencies as 'D-CALC, T-005' and explains the ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR134:PRRT_kwDOTH_vCM6Pujux

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/dependencies/dependency-graph.md:159`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/134#discussion_r3555325304
- Claim: **P2 Badge Synchronize T-014's circularity audit entry** With this dependency graph now declaring T-014 depends only on D-CALC, the current circularity audit still reports 'Dependencies: D-CALC, T-005' and justifies the pass by saying T-...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR136:PRRT_kwDOTH_vCM6Pus-I

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-014.proof.yaml:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/136#discussion_r3555378849
- Claim: **P2 Badge Use a schema-declared proof-object status** The proof-object schema defines 'status' as an enum with values '[draft, proposed, verified, established, deprecated]' ('theory/proof-objects/proof-object-schema.yaml:17-19'), so set...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR136:PRRT_kwDOTH_vCM6Pus-M

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/dependency-audit-rerun.md:132`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/136#discussion_r3555378854
- Claim: **P2 Badge Correct the proof-object status audit** This audit conclusion is contradicted by the repository: 'theory/proof-objects/T-001.proof.yaml' through 'T-012.proof.yaml' still have 'status: draft', so T-001 through T-013 were not al...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR137:PRRT_kwDOTH_vCM6Pu8t3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/theorem-coverage-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/137#discussion_r3555471226
- Claim: **P2 Badge Reconcile the canonical inventory with accepted audit** This summary says the audit enumerates all canonical mathematical artifacts, but the accepted foundation includes the Canonical Mathematics Audit ('docs/reports/dependenc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR137:PRRT_kwDOTH_vCM6Pu8t7

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/theorem-coverage-audit.md:203`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/137#discussion_r3555471231
- Claim: **P2 Badge Correct the dependency-registry coverage claims** These PASS rows treat 'theory/dependencies/dependency-registry.yaml' as covering every L/P/T artifact, but that registry is explicitly 'scope: repository-structure-only' ('theo...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR138:PRRT_kwDOTH_vCM6Pu_IE

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/proof-objects/T-001.proof.yaml:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/138#discussion_r3555485237
- Claim: **P2 Badge Use a schema-valid proof-object status** For T-001 through T-012 this change writes 'status: accepted', but 'theory/proof-objects/proof-object-schema.yaml' defines the allowed proof-object statuses as only 'draft', 'proposed',...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR139:PRRT_kwDOTH_vCM6PvDtm

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/minimality-audit.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/139#discussion_r3555510614
- Claim: **P1 Badge Include A1–A5 in the minimality inventory** This inventory says the audit covers the accepted foundation, but it omits the five established axiom records A1–A5: both 'theory/metadata/generated-axiom-index.md' and the prior can...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR148:PRRT_kwDOTH_vCM6Pw5hJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/external-validation/philosophy/campaign-method.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/148#discussion_r3556188197
- Claim: **P2 Badge Add Charter status to the new campaign artifacts** The root 'AGENTS.md' requires compliance with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from Ac...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR150:PRRT_kwDOTH_vCM6PxKNR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/reports/external-validation/ai-reasoning/campaign-summary.md:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/150#discussion_r3556281887
- Claim: **P1 Badge Record falsification evidence before passing the campaign** When this summary is used as the Phase 2 validation record, the claim that the campaign falsified representability by testing these AI-specific pressures is not repro...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR151:PRRT_kwDOTH_vCM6PxMgL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/far_mechanization/ir.py:250`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/151#discussion_r3556294779
- Claim: **P2 Badge Include the investigation in duplicate-ID checks** When an IR collection item reuses the 'investigation.identifier', 'FARDocument.validate()' returns no 'DUPLICATE_LOCAL_IDENTIFIER' because the duplicate map starts empty and i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR151:PRRT_kwDOTH_vCM6PxMgM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/far_mechanization/ir.py:178`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/151#discussion_r3556294780
- Claim: **P2 Badge Validate enum fields at runtime** When graph nodes are constructed from untyped parsed data, 'GraphNode(Identifier("N"), "bogus").validate()' reports success because this validator only checks the identifier and source; datacl...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR154:PRRT_kwDOTH_vCM6QJoVS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/governance/repository-certification-standard.md:4`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/154#discussion_r3565194327
- Claim: **P2 Badge Use a Charter-recognized artifact status** Under the root 'AGENTS.md', new work must comply with 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from 'A...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR154:PRRT_kwDOTH_vCM6QKFHI

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/repository-certification-inventory-audit.md:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/154#discussion_r3565358292
- Claim: **P2 Badge Refresh the inventory against the final tree** In the reviewed tree there are 1000 tracked paths ('git ls-tree -r --name-only cdc9897... | wc -l'), and this inventory also omits certification artifacts added later in the same ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR155:PRRT_kwDOTH_vCM6QMr9J

- Disposition: `unresolved`
- Confidence: `high`
- Location: `README.md:99`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/155#discussion_r3566291247
- Claim: **P2 Badge Restore generated TASK-004 metadata** In this generated dashboard block, 'tools/update_readme_dashboard.py::parse_tasks' takes the branch and title from 'docs/planning/next-actions.md', which still records TASK-004 as 'mainten...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR156:PRRT_kwDOTH_vCM6QMZtL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-validation-methodology.md:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/156#discussion_r3566189890
- Claim: **P2 Badge Scope the new requirements before applying them globally** Because this says every external-system investigation must now record the new fields, the 20 already-registered investigations in 'theory/evaluation/external-systems/*...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR157:PRRT_kwDOTH_vCM6QMn8d

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-system-investigations/legal-reasoning.md:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/157#discussion_r3566269404
- Claim: **P2 Badge Reclassify legal reasoning when preservation is unknown** Here the report classifies legal reasoning as 'conservative extension', but its own preservation review leaves semantic, operational, and information preservation as 'u...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR157:PRRT_kwDOTH_vCM6QMn8f

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-system-investigations/cross-investigation-synthesis-001.md:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/157#discussion_r3566269407
- Claim: **P2 Badge Recompute synthesis over all nine investigations** The scope lists nine investigations, including the five adversarial reports, but this aggregate still says 'All four' and summarizes only the original formal/Bayesian/science ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR158:PRRT_kwDOTH_vCM6QQUuU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/external-system-investigations/current-evidence-assessment-001.md:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/158#discussion_r3567578096
- Claim: **P2 Badge Reclassify EV-028 before aggregating counts** When this table counts EV-021 through EV-029 as 3 'conservative extension' and 4 'unresolved', it preserves EV-028's conservative label even though 'legal-reasoning.md' records sem...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR159:PRRT_kwDOTH_vCM6QQ_JH

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/protocol-v1.0.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821905
- Claim: **P1 Badge Record provenance before accepting CRP** In this new protocol, the artifact is promoted to 'Accepted', but the file does not record the charter-required Question → Execution → Observation → Discovery → Replication → Acceptance...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR159:PRRT_kwDOTH_vCM6QQ_JJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiment-registry.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821907
- Claim: **P2 Badge Register only immutable experiment artifacts** The registry pins a concrete scenario/vocabulary/instruction version for CRE-001, but the CRE-001 directory currently contains only a README and a repo-wide search finds no artifa...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR159:PRRT_kwDOTH_vCM6QQ_JM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/159#discussion_r3567821910
- Claim: **P2 Badge Inline the provenance schema reference** When an evaluator submission includes its required 'provenance' object, validation through the repository's bundled JSON Schema implementation fails before checking the instance because...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR160:PRRT_kwDOTH_vCM6QR-_T

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/validate_cre001_submission.py:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181635
- Claim: **P1 Badge Match provenance checks to the submitted template** For real CRE-001 bundles, the 'provenance' object is supposed to be the completed 'provenance/provenance-record.template.json' referenced by the packet manifests and evaluato...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR160:PRRT_kwDOTH_vCM6QR-_V

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/validate_cre001_submission.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181637
- Claim: **P1 Badge Allow assigned vocabulary labels through leakage check** Because the validator scans every string in the entire bundle, listing 'Vocabulary A', 'Vocabulary B', and 'Vocabulary C' as leakage terms rejects submissions that follo...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR160:PRRT_kwDOTH_vCM6QR-_Y

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/validate_cre001_submission.py:135`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/160#discussion_r3568181639
- Claim: **P2 Badge Check mapping provenance against the bundle record** This only verifies the CIR provenance identifier, so a bundle where 'mapping_submission.provenance' points at a different or nonexistent record is still accepted as long as ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR161:PRRT_kwDOTH_vCM6RQoEE

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/repo_health_check.py:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/161#discussion_r3591137832
- Claim: **P2 Badge Run the documented pytest mechanization suite** When 'repo_health_check.py --fast' or '--full' runs in this repository, this 'unittest discover' command exercises only the 51 'unittest.TestCase' cases; the documented mechaniza...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR161:PRRT_kwDOTH_vCM6RQoEG

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_status_consistency.py:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/161#discussion_r3591137834
- Claim: **P2 Badge Preserve negative status before matching supported** For any parsed source whose status is 'Not supported', this loop matches the substring 'supported' first and normalizes the value to 'supported', so the consistency report i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR164:PRRT_kwDOTH_vCM6RRYKW

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/metadata/theorems.yaml:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/164#discussion_r3591417084
- Claim: **P1 Badge Use a verifier-supported theorem status** In the reviewed tree, 'tools/verify_theory.py' accepts only 'Draft', 'Proposed', 'Verified', 'Established', or 'Deprecated' for theorem metadata, so introducing 'Established (Condition...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR164:PRRT_kwDOTH_vCM6RRYKa

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_status_consistency.py:177`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/164#discussion_r3591417087
- Claim: **P2 Badge Update tests for scoped fallback matching** This new scope gate changes the checker so conditional theorem titles no longer fallback-match the broad investigation titles, but 'tests/test_status_consistency.py::test_similarity_...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR165:PRRT_kwDOTH_vCM6RRgpO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.md:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/165#discussion_r3591465879
- Claim: **P2 Badge Record pilot exposure in CRE-001 status** When this pilot artifact is kept under CRE-001, this line records that calibration and experimental materials were exposed to an evaluator, but the existing status sources still say no...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR165:PRRT_kwDOTH_vCM6RRgpS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-001/execution/pilot-artifacts/CRE-001-E01-claude-sonnet-medium-pilot-v1/CRE-001-E01-claude-sonnet-medium-pilot-v1-review.metadata.json:2`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/165#discussion_r3591465884
- Claim: **P2 Badge Add required provenance to pilot metadata** For this new CRE-001 artifact, the metadata omits several immutable provenance identifiers required by CRP v1.0's Provenance rule for every dataset and artifact, including protocol/s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR168:PRRT_kwDOTH_vCM6RSwBn

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/cre001_compile_vocabularies.py:62`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/168#discussion_r3591944859
- Claim: **P1 Badge Verify against the registered reference artifact** In the deterministic comparison path, the verifier uses 'model_from_scenario()' as the reference instead of 'deterministic-verifier/reference-model.json', even though the exis...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR169:PRRT_kwDOTH_vCM6RUGku

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/169#discussion_r3592472967
- Claim: **P2 Badge Use distinct provenance for strategic tasks** When the current gap report contains GAP-001 through GAP-005, these hard-coded tasks reuse both the same task IDs and the same source-gap IDs as the generated gap-derived tasks, so...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR170:PRRT_kwDOTH_vCM6RUPh8

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre001_semantics.py:54`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/170#discussion_r3592525581
- Claim: **P2 Badge Compare semantic docs against the frozen specification** This loop only checks that each semantic doc contains the five status words; it never hashes the docs or compares their primitive definitions/licensing tables to 'semant...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR170:PRRT_kwDOTH_vCM6RUPh-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/170#discussion_r3592525583
- Claim: **P2 Badge Use noncolliding source gaps for strategic tasks** In this repo 'docs/reports/research-gap-report.md' already defines 'GAP-001' through 'GAP-005' as unrelated PS-001/PS-003 maintenance gaps; these hard-coded CRE-002 tasks reus...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR171:PRRT_kwDOTH_vCM6RUQL4

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/generate_next_tasks.py:59`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529395
- Claim: **P1 Badge Use real source gaps for strategic tasks** These hard-coded 'GAP-001' through 'GAP-005' values do not describe the new CRE-002 tasks: in the generated gap report they still point to PS-001/PS-003 unresolved/provisional-system ...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR171:PRRT_kwDOTH_vCM6RUQL5

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/generate_next_tasks.py:73`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529397
- Claim: **P2 Badge Keep generated task identifiers unique** Because 'task_from_gap()' also derives IDs as 'TASK-', prepending strategic tasks named 'TASK-001' through 'TASK-005' makes the generated 'docs/planning/next-actions.md' contain two dif...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR171:PRRT_kwDOTH_vCM6RUQL6

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_cre001_semantics.py:44`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/171#discussion_r3592529398
- Claim: **P2 Badge Guard the FAR-proof non-claim in semantic checks** 'NONCLAIMS' includes 'FAR proof', but this condition explicitly exempts that claim, so 'tools/check_cre001_semantics.py' passes even if the frozen primitive semantics omit the...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR172:PRRT_kwDOTH_vCM6RUxxM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/repository-health.yml:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/172#discussion_r3592726443
- Claim: **P2 Badge Defer PR trigger until full health passes** This new 'pull_request' trigger makes the workflow run the unchanged 'python tools/repo_health_check.py --full' step for every PR targeting 'main'; in this checkout that exact comman...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR172:PRRT_kwDOTH_vCM6RUxxO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/update_readme_dashboard.py:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/172#discussion_r3592726445
- Claim: **P2 Badge Parse strategic tasks in the planner summary too** Now that this parser promotes 'STRATEGIC-*' entries into the README top tasks, the canonical 'make dashboard' workflow becomes inconsistent because 'tools/self_advancement_pla...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR173:PRRT_kwDOTH_vCM6RU20P

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre002_preregistration.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755287
- Claim: **P1 Badge Restore the CRE-002 preregistration check** With this value, the new test fails: 'python -m unittest tests.test_cre002_preregistration' invokes 'tools/check_cre002_preregistration.py' and reports 'missing nonclaim: FAR proof',...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR173:PRRT_kwDOTH_vCM6RU20S

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/scenario/scenario-v1.0.json:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755291
- Claim: **P1 Badge Make the override path reachable before locking the scenario** In this frozen scenario, 'T_override' requires provenance for 'manual_override=true' from the operator, but the initial evidence log is empty and the only evidence...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR173:PRRT_kwDOTH_vCM6RU20U

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/README.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/173#discussion_r3592755293
- Claim: **P2 Badge Register CRE-002 in the canonical experiment registry** This commit introduces CRE-002 as a preregistered experiment package, but 'theory/evaluation/comparative-representation/experiment-registry.json' still contains only CRE-...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR174:PRRT_kwDOTH_vCM6RVB21

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre002_lock.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/174#discussion_r3592819589
- Claim: **P2 Badge Verify the manifest's recorded checksums** When this gate builds 'actual', it uses 'package-manifest.json' only as a path list and ignores each entry's recorded 'sha256' and 'byte_count', so CI still passes if the manifest is ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR174:PRRT_kwDOTH_vCM6RVB22

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre002_lock.py:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/174#discussion_r3592819591
- Claim: **P2 Badge Use a reachable checksum source commit** In the reviewed commit, this hard-coded 'source_commit' is not an ancestor of '2692d8cbd329ff68bb63f2e5dfb1e9c6bf73453b' ('git merge-base --is-ancestor 003f0fda... 2692d8c...' returns n...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR175:PRRT_kwDOTH_vCM6RVFKq

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/175#discussion_r3592838611
- Claim: **P1 Badge Update preregistration validation for the unlock state** In the unlocked state introduced here, the committed CI path still fails: 'tests/test_cre002_preregistration.py' invokes 'tools/check_cre002_preregistration.py', which r...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR176:PRRT_kwDOTH_vCM6RVX-c

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002/package-manifest.json:34`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/176#discussion_r3592946228
- Claim: **P1 Badge Commit the declared CRE-002 result artifacts** With this line set to 'true', a clean checkout is declared to contain official results, but this commit does not track 'theory/evaluation/comparative-representation/experiments/CR...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR176:PRRT_kwDOTH_vCM6RVX-h

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/cre002_execute.py:358`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/176#discussion_r3592946238
- Claim: **P2 Badge Emit the preregistered boundary reports** CRE-002 preregistration requires each vocabulary to emit both a compiler-boundary report and a limitation/unsupported-element report, but this artifact map never writes either artifact...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR177:PRRT_kwDOTH_vCM6RVqC_

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_vocabulary_semantics_baseline_1_1.py:100`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/177#discussion_r3593046970
- Claim: **P2 Badge Restore byte-for-byte CRE-002 result validation** When the original CRE-002 result changes outside the sampled fields, this checker still passes even though the new baseline's freeze requirement says the result must remain byt...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR178:PRRT_kwDOTH_vCM6RV06v

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/178#discussion_r3593108984
- Claim: **P1 Badge Keep the override path reachable** With this scenario as frozen input, 'T_override' can never fire: the initial 'evidence_log' is empty, and the only evidence-producing transitions are 'T_record_a'/'T_record_b', which append o...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR178:PRRT_kwDOTH_vCM6RV06x

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/178#discussion_r3593108987
- Claim: **P2 Badge Require the Baseline 1.1 checksum lock before execution** This unlock prerequisite now only requires Baseline 1.1 to be merged, but the Baseline 1.1 freeze boundary says it becomes usable only after merge and checksum lock ('t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR181:PRRT_kwDOTH_vCM6RWgcF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/execution-lock.json:6`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/181#discussion_r3593355089
- Claim: **P1 Badge Update Baseline 1.1 gates before unlocking** In this authorized state, setting these flags to 'true' breaks the existing Baseline 1.1 health gates: 'tools/check_vocabulary_semantics_baseline_1_1.py' still requires both values ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR182:PRRT_kwDOTH_vCM6RXNCP

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/cre002_ext001_model.py:155`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608670
- Claim: **P1 Badge Require every frozen output before passing candidates** In this execution, 'required_outputs_preserved' is the gate used by 'build()' before marking a candidate complete, but this check never consults the frozen scenario's 'ou...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR182:PRRT_kwDOTH_vCM6RXNCU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/cre002_ext001_native.py:105`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608676
- Claim: **P1 Badge Validate candidate records against derived-field requirements** This audit checks whether the Baseline 1.1 construct definitions themselves have 'required_fields' and 'operational_constraints', but it never checks that the can...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR182:PRRT_kwDOTH_vCM6RXNCb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/cre002_ext001_execute.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/182#discussion_r3593608682
- Claim: **P2 Badge Hash the official vocabulary source packages** The preregistration makes the official Vocabulary A/B/C source definitions frozen inputs and each candidate is supposed to emit source checksums, but this shared 'source_checksums...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR183:PRRT_kwDOTH_vCM6RXZ9j

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/integrate-cre002-ext001-evidence.yml:59`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/183#discussion_r3593681934
- Claim: **P2 Badge Commit the dashboard index after regeneration** When this workflow runs, 'tools/update_readme_dashboard.py' also rewrites 'docs/planning/repository-index.md' via 'generate_index()'. I verified the workflow command sequence on ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR183:PRRT_kwDOTH_vCM6RXZ9l

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/integrate-cre002-ext001-evidence.yml:55`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/183#discussion_r3593681939
- Claim: **P2 Badge Keep the regenerated README phase current** When this integration workflow reaches the README step, 'tools/update_readme_dashboard.py' still renders the old post-CRE-001 / CRE-002-preparation phase and roadmap lines. Because t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR184:PRRT_kwDOTH_vCM6Rc-OK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/decision-rules.json:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/184#discussion_r3595705807
- Claim: **P1 Badge Require all clean counted submissions to pass** When there are multiple eligible uncontaminated submissions and one completes while another fails, these rules can still classify the vocabulary and overall replication as succes...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR185:PRRT_kwDOTH_vCM6RefEA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre002_ext001_rep001_preregistration.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/185#discussion_r3596251334
- Claim: **P2 Badge Require the checksum-locked phase** After this commit promotes the package to 'checksum_state: locked', the preregistration checker still accepts 'pending'. If a bad merge or later edit reverts the manifest to 'pending', this ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR186:PRRT_kwDOTH_vCM6Revz1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_cre002_ext001_rep001_team_registry.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/186#discussion_r3596346625
- Claim: **P1 Badge Reject shared repositories in registry validation** When eligible registrations have disjoint personnel but reuse the same 'repository_identity', this checker still appends them to the eligible implementation/verifier counts a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR188:PRRT_kwDOTH_vCM6Rfduh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/cre002_ext001_robustness.py:93`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/188#discussion_r3596608255
- Claim: **P1 Badge Preserve empty arrays in the third implementation** When the frozen scenario contains empty arrays ('initial_state.evidence_log' and 'initial_state.action_history'), 'json.loads(..., object_pairs_hook=list)' represents those a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR188:PRRT_kwDOTH_vCM6Rfdum

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001/package-manifest.json:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/188#discussion_r3596608260
- Claim: **P2 Badge Keep the superseded manifest state accepted by checks** Changing the package checksum state to this new value leaves the existing preregistration gate out of sync: 'tools/check_cre002_ext001_rep001_preregistration.py' still re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR189:PRRT_kwDOTH_vCM6RgFpD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/parse_far.py:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833875
- Claim: **P2 Badge Reject non-string scalars instead of coercing them** In files that use non-string YAML scalars for 'string+' fields, such as 'id: 1' or 'kind: true', this coerces them to strings before validation, so 'python tools/parse_far.p...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR189:PRRT_kwDOTH_vCM6RgFpI

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/parse_far.py:85`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833882
- Claim: **P2 Badge Validate unknown keys inside statement mappings** When a representation uses a mapped 'statement', this delegates to 'Statement.from_value' without checking the grammar's statement allow-list, so 'statement: {kind: claim, clai...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR189:PRRT_kwDOTH_vCM6RgFpM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/parse_far.py:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/189#discussion_r3596833889
- Claim: **P2 Badge Remove lowercase aliases from primitive key allow-list** With these lowercase keys allowed, a 'reasoning_system.far_primitives' block containing only 'investigation', 'representation', 'structure', 'interpretation', and 'calcu...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR191:PRRT_kwDOTH_vCM6Rg6qO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/lean/FARCore.lean:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/191#discussion_r3597138599
- Claim: **P2 Badge Carry the required transition-signature fields** When a scoped process has specified transition executions, this type treats a bare label as a complete transition signature. The accepted definitions say a transition signature ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR191:PRRT_kwDOTH_vCM6Rg6qW

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/lean/FARCore.lean:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/191#discussion_r3597138611
- Claim: **P2 Badge Tie trace transitions to the governing calculus** For a process whose 'specifiedTransitions' includes a signature that 'premises.calculus R hScope' rejects, the construction still succeeds because the representation only store...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR192:PRRT_kwDOTH_vCM6RipTt

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_t003_adequacy_audit.py:42`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/192#discussion_r3597775989
- Claim: **P1 Badge Align the audit wording checked by the test** Running 'python -m unittest tests.test_t003_adequacy_audit' fails here because the audit document never contains this exact phrase: it says the examples “do not establish universal...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR192:PRRT_kwDOTH_vCM6RipTx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_t003_adequacy_audit.py:49`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/192#discussion_r3597775995
- Claim: **P1 Badge Restrict the axiom/admission scan to declarations** This test currently scans the entire Lean source as raw text, so it fails on existing comments rather than new proof admissions: 'FARCore.lean' already contains “as an axiom”...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR193:PRRT_kwDOTH_vCM6Rj0PR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/specification-export.yml:23`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/193#discussion_r3598208533
- Claim: **P1 Badge Install pytest before running the workflow tests** In the added workflow, the only setup before this command is checkout, 'actions/setup-python', the exporter run, and 'git diff'; neither 'pyproject.toml' nor 'requirements.txt...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR193:PRRT_kwDOTH_vCM6Rj0PX

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/export_specification.py:118`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/193#discussion_r3598208540
- Claim: **P2 Badge Recompute VCS metadata instead of preserving it** When the exporter runs over the committed export directory, 'existing_vcs_metadata()' returns the old manifest values and this early return keeps them, so the exact CI regenera...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR197:PRRT_kwDOTH_vCM6RpiBK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/independence/primitive-independence-evaluation.schema.json:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/197#discussion_r3600351085
- Claim: **P1 Badge Separate per-test records from aggregate decisions** This schema validates only a single 'test_type', but 'locally-independent' and 'tested-space-independent' are aggregate outcomes that the framework allows only after every m...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR197:PRRT_kwDOTH_vCM6RpiBO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/README.md:15`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/197#discussion_r3600351090
- Claim: **P2 Badge Register the new theory child domain** Adding 'theory/independence/' here creates a new canonical theory area, but the frozen Repository Domain Registry remains the authoritative list of 'theory/' child domains and still omits...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR198:PRRT_kwDOTH_vCM6R1HgZ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/independence/executions/PIE-001/attempts.csv:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/198#discussion_r3604642189
- Claim: **P2 Badge Record required preservation and complexity judgments** For PIE-001 rows, the protocol requires each attempted reduction to record per-dimension preservation judgments and complexity accounting before success/failure can be ad...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR199:PRRT_kwDOTH_vCM6R1VGh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_alternative_vocabulary_competition.py:68`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/199#discussion_r3604720523
- Claim: **P1 Badge Fix the self-matching global-minimality assertion** This assertion makes the newly added test suite fail because the report intentionally contains the negated sentence 'AVC-001 does **not** establish that FAR is globally minim...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR200:PRRT_kwDOTH_vCM6R1kcF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/independence/global-minimality/GMA-001/README.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/200#discussion_r3604808061
- Claim: **P1 Badge Use one charter-approved artifact status** 'AGENTS.md' directs all automated work to 'docs/governance/research-execution-charter.md', whose Repository Rules require every artifact to have exactly one status from 'Accepted', 'R...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR200:PRRT_kwDOTH_vCM6R1kcJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/independence/global-minimality/GMA-001/README.md:45`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/200#discussion_r3604808065
- Claim: **P2 Badge Do not label unresolved counts as demonstrated** I checked the referenced AVC-001 results: only the FAR control is all-'Pass', while every three-primitive candidate is either 'unresolved' or 'not-admissible'. Calling the minim...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR201:PRRT_kwDOTH_vCM6R1r2E

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/scope/ISD-001/scope-registry.json:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/201#discussion_r3604850584
- Claim: **P2 Badge Preserve frozen-benchmark gate in the registry rule** If future scope-expansion tooling or reviewers use this machine-readable 'inclusion_rule', a class can be marked demonstrated from any single explicit instance, even when n...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR201:PRRT_kwDOTH_vCM6R1r2G

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/scope/ISD-001/scope-registry.json:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/201#discussion_r3604850587
- Claim: **P2 Badge Include standalone universality in registry exclusions** If downstream checks consume 'excluded_from_current_claims' as the machine-readable claim boundary, this list still does not exclude the standalone universality claim ('...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR202:PRRT_kwDOTH_vCM6R1vYI

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:32`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871140
- Claim: **P1 Badge Keep CRE-003-I's investigation fixed** When CRE-003-I is used as the interpretation-only case, this changes the investigation objective from determining whether the alarm is permitted to determining whether withdrawal is permi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR202:PRRT_kwDOTH_vCM6R1vYK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871144
- Claim: **P1 Badge Do not add new facts to the calculus case** When CRE-003-C is evaluated as the reasoning-calculus-only variation, adding 'exception_q' to 'system_b' also changes the represented material and its interpretation, despite both be...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR202:PRRT_kwDOTH_vCM6R1vYM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-003/preregistration.json:96`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/202#discussion_r3604871147
- Claim: **P1 Badge Keep the calculus constant in CRE-003-R** When CRE-003-R is used to test representation/structure variation, changing the calculus from 'modus_ponens' to 'support_edge_propagation' conflicts with the case's 'held_constant' dec...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR203:PRRT_kwDOTH_vCM6R12qG

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_cre003_execution.py:66`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/203#discussion_r3604912577
- Claim: **P1 Badge Fix the assertion string so the test suite passes** When I ran 'python -m unittest tests.test_cre003_preregistration tests.test_cre003_execution', this assertion failed because 'execution.md' contains the phrase "remained unre...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR204:PRRT_kwDOTH_vCM6R2SrO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/scoring.py:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/204#discussion_r3605073881
- Claim: **P1 Badge Require a registered carrier before passing** When an evaluator selects only 'difference_carriers=["other"]' and answers 'other_function="none"', execution falls through to this 'pass' even though there are no registered funct...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR204:PRRT_kwDOTH_vCM6R2SrT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/response.schema.json:38`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/204#discussion_r3605073887
- Claim: **P2 Badge Make 'cannot_determine' exclusive in the schema** For translated systems marked distinguishable, the schema currently accepts 'difference_carriers' such as '["cannot_determine", "assigns_meaning"]' because 'cannot_determine' i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR205:PRRT_kwDOTH_vCM6R2llN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/decision_tree.md:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/205#discussion_r3605183243
- Claim: **P2 Badge Use the schema field in the decision tree** For implementations following this frozen tree, 'translated_distinction' is not a response field: 'response.schema.json', 'preregistration.json', and 'scoring.py' all use 'translated...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR205:PRRT_kwDOTH_vCM6R2llV

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/hidden_reintroduction.md:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/205#discussion_r3605183253
- Claim: **P2 Badge Align hidden-reintroduction outcomes with scorer** When 'other' is selected with 'other_function = cannot_determine', this frozen rule says to output 'hidden_reintroduction = unknown', but the normative implementation in 'scor...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR206:PRRT_kwDOTH_vCM6R22Dm

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/protocol_lock.json:10`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278314
- Claim: **P1 Badge Fix the locked evaluator packet hash** This lock entry does not match the checked-in 'evaluator_packet.md': 'verify_protocol_lock()' computes git blob SHA-1 '1ea5043ccb3a10aa0f350237ec1b4b3ce558c7ff' for the file in this commi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR206:PRRT_kwDOTH_vCM6R22Dp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:86`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278317
- Claim: **P2 Badge Validate responses against the frozen schema** This only checks labels and 'submitted_at' are non-empty strings, so a manifest and response using values such as 'case_label: "CASE 001"' or 'submitted_at: "not-a-date"' are acce...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR206:PRRT_kwDOTH_vCM6R22Ds

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py:179`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/206#discussion_r3605278320
- Claim: **P2 Badge Report the required per-evaluator and per-case aggregates** The frozen automatic-scoring spec requires results at response, evaluator, case, candidate, and overall levels, but this summary only emits the overall counts and 'by...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR208:PRRT_kwDOTH_vCM6R_ofk

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/README.md:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/208#discussion_r3608557370
- Claim: **P1 Badge Enforce the closed intake gates before scoring** Because this rule is only documented here, it does not actually protect RUN-001: the inspected CRE-004 replay path ('execution_pipeline.replay' → 'validate_manifest') accepts on...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR209:PRRT_kwDOTH_vCM6SASkl

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/comparative-representation/experiments/CRE-004/runs/CRE-004-RUN-001/coordinator_candidate_key.json:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/209#discussion_r3608793206
- Claim: **P2 Badge Use non-predictable candidate labels** The frozen key preserves the source numbering ('CANDIDATE_001' maps to 'AV-001', and so on), even though CRE-004’s blinding rules require randomized opaque candidate identities and AVC-00...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR211:PRRT_kwDOTH_vCM6SAc_1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/candidate-architecture-registry.json:9`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/211#discussion_r3608851714
- Claim: **P2 Badge Allow equivalence-conjectured in the registry** The standard introduced in this same change says valid bidirectional translations let two candidates be marked 'equivalence-conjectured', but this machine-readable status list om...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR217:PRRT_kwDOTH_vCM6SCBSx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_pbts001_replication_package.py:259`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418609
- Claim: **P1 Badge Keep the package validator passing its own frozen protocol** For this commit, running 'python tools/check_pbts001_replication_package.py' fails because the protocol’s nonclaim is written as 'This package does not establish:' f...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR217:PRRT_kwDOTH_vCM6SCBS0

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/pbts001-independent-replication-registry.json:71`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418612
- Claim: **P2 Badge Rename the calibration metadata key to preserve the path** This second 'calibration' member duplicates the path-valued 'calibration' key at line 7. Standard JSON parsers keep only one value, and Python's loader used by the new...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR217:PRRT_kwDOTH_vCM6SCBS4

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/pbts001-independent-replication-response-schema.json:89`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/217#discussion_r3609418616
- Claim: **P2 Badge Require distinct coverage entries in the response schema** The schema's exact item counts only limit array length; they do not require the eight entries to cover PA-01 through PA-08. A schema-valid submission can repeat 'PA-01...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR218:PRRT_kwDOTH_vCM6SG4vx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/research/pbts001-replication-run-001-coordinator-controls.md:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/218#discussion_r3611191513
- Claim: **P2 Badge Use the slot-specific seed in the frozen controls** This seed text does not match the run registry's frozen 'seed_template' ('PBTS-001-REP-001-RUN-001|{slot_id}|order-v1'). If the coordinator follows this human-facing control ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR220:PRRT_kwDOTH_vCM6SIkht

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/update_readme_dashboard.py:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/220#discussion_r3611798075
- Claim: **P1 Badge Close the README dashboard task append call** In the target commit, running 'python -m py_compile tools/update_readme_dashboard.py' fails with 'SyntaxError: '(' was never closed' at this appended task tuple. Any path that invo...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR221:PRRT_kwDOTH_vCM6SIzy3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `README.md:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/221#discussion_r3611882907
- Claim: **P1 Badge Keep research-check aligned with README wording** In this commit the README changes the required wording to “The project is deduction-first,” but 'tools/check_deduction_first_program.py' still asserts the exact old phrase 'The...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR221:PRRT_kwDOTH_vCM6SIzy4

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_thm_target_001.py:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/221#discussion_r3611882909
- Claim: **P1 Badge Avoid rejecting the registered nonclaim as a claim** When this new checker is invoked directly, and from the Makefile after the prior gate is fixed, it fails against the committed theorem document because the prohibited substr...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR224:PRRT_kwDOTH_vCM6SWc46

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/faithful-representation-specification-v1.0.json:156`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/224#discussion_r3616820802
- Claim: **P2 Badge Sync the faithful source artifact before advancing W0** This registry now advances FAITHFUL-REP-001 to the W0 proof package, but its declared 'source_artifact' ('docs/research/faithful-representation-specification-v1.0.md') st...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR225:PRRT_kwDOTH_vCM6SXDn8

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/s_core_w0_reference.py:186`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/225#discussion_r3617043347
- Claim: **P2 Badge Restrict canonical codes to the material closure** When a finite contract contains declared nodes outside 'Cl(material_seed)', this loop canonicalizes every 'self.nodes' entry rather than the theorem-facing material restrictio...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR225:PRRT_kwDOTH_vCM6SXDn-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/s_core_w0_reference.py:171`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/225#discussion_r3617043351
- Claim: **P2 Badge Do not infer sort preservation from labels** For a valid sort-preserving renaming whose fresh target name happens to start with another fixture prefix, 'renamed()' raises before constructing the renamed contract, even though l...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR226:PRRT_kwDOTH_vCM6SXowJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_s_core_w1.py:112`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/226#discussion_r3617256618
- Claim: **P1 Badge Use the path constant for the W1 registry lookup** When 'python tools/check_s_core_w1.py' runs, this line always raises 'AttributeError' because 'reg' was rebound above to the loaded JSON dict, so it no longer has 'relative_to...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR226:PRRT_kwDOTH_vCM6SXowM

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/s_core_w1_reference.py:72`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/226#discussion_r3617256620
- Claim: **P2 Badge Reject shared elements with conflicting denotations** For the case where the same source element id appears in multiple direct axes with a different 'denotation', this validation only enforces sort consistency. 'construct_targ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR229:PRRT_kwDOTH_vCM6SaGam

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_faithful_representation.py:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/229#discussion_r3618166626
- Claim: **P1 Badge Keep the faithful-representation check aligned with the spec** With this new phrase guard, 'make research-check'/'make health-fast' fails on the committed tree: the faithful spec contains the other checked phrases, but not 'so...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR229:PRRT_kwDOTH_vCM6SaGao

- Disposition: `unresolved`
- Confidence: `high`
- Location: `README.md:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/229#discussion_r3618166629
- Claim: **P2 Badge Regenerate the README dashboard from the updated generator** This section is inside the 'BEGIN GENERATED PROJECT FAR DASHBOARD' block, but it was not regenerated from the updated 'tools/update_readme_dashboard.py': running tha...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR231:PRRT_kwDOTH_vCM6ScNF3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `far_validation/engine.py:565`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/231#discussion_r3618991940
- Claim: **P2 Badge Decode timeout output before serializing results** When a checker times out after emitting output, 'subprocess.TimeoutExpired.stdout' and 'stderr' are 'bytes' even though 'text=True' was passed, so storing them directly here m...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR231:PRRT_kwDOTH_vCM6ScNF9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `far_validation/engine.py:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/231#discussion_r3618991947
- Claim: **P2 Badge Treat globstar inputs as covering direct files** In changed-file mode, 'fnmatch'/'Path.match' both return false for direct-file cases such as 'README.md' vs '**/*.md' and 'tools/run_tests.py' vs 'tools/**/*.py', even though th...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR232:PRRT_kwDOTH_vCM6Sd90_

- Disposition: `unresolved`
- Confidence: `high`
- Location: `far_validation/weakening.py:137`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/232#discussion_r3619656400
- Claim: **P1 Badge Compare the old path when auditing renames** When Git reports a rename such as 'R059 tests/test_old.py tests/test_new.py', this keeps only the new path, so '_show(base, path)' looks for 'tests/test_new.py' in the base commit a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR232:PRRT_kwDOTH_vCM6Sd91A

- Disposition: `unresolved`
- Confidence: `high`
- Location: `far_validation/tracing.py:145`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/232#discussion_r3619656401
- Claim: **P2 Badge Account for dirfd-relative traced file accesses** When a traced syscall is 'openat'/'newfstatat' against a directory fd, for example 'openat(3, "secret.txt", ...)', this branch returns 'None' and drops the access entirely. A c...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR233:PRRT_kwDOTH_vCM6Sfq25

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_w3_5_corpus_freeze.py:77`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/233#discussion_r3620279924
- Claim: **P1 Badge Enforce required instance versions before freezing** When 'RCS-001' marks 'version' as a required instance field, this per-record validation never checks for it; all 18 new source/registry records are accepted without a per-in...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR234:PRRT_kwDOTH_vCM6Srbte

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/w3_5_grel.py:79`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/234#discussion_r3624592982
- Claim: **P2 Badge Reject unreachable carriers in GREL validation** When validating externally supplied GREL packages, this only checks that the declared root exists; it never verifies that all entities, values, attributes, and relations are rea...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR234:PRRT_kwDOTH_vCM6Srbti

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_w3_5_factorization.py:117`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/234#discussion_r3624592986
- Claim: **P2 Badge Require every frozen runtime check to be present** If a future change drops a required runtime check such as 'no_hidden_interpreter' but leaves the remaining checks as 'pass', this condition still accepts the record because it...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR236:PRRT_kwDOTH_vCM6Sv2G6

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_w3_5_corpus_freeze.py:58`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/236#discussion_r3626232359
- Claim: **P2 Badge Don't hard-code the withdrawn candidate outcome** When 'W3.5' later moves to 'in_progress_candidate_complete', this checker will only accept 'current_results.candidate_invariants == "complete_no_indispensable_candidate"'. The ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR237:PRRT_kwDOTH_vCM6SwTry

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_w3_5_candidate_tests.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/237#discussion_r3626404989
- Claim: **P1 Badge Load preserved trial records before accepting completion** For the completed candidate package, this regenerates 'trials' from the current Python module and the result only hashes that same module, so updating the generator an...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR237:PRRT_kwDOTH_vCM6SwTr0

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/w3_5_candidate_execution.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/237#discussion_r3626404991
- Claim: **P2 Badge Score information in equivalence comparisons** For reconstructable trials, the equivalence vector can declare 'commitment_equivalent' without scoring the 'information' dimension, even though the preservation dimensions used fo...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR238:PRRT_kwDOTH_vCM6Swy9x

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/project_status_report.py:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/238#discussion_r3626587376
- Claim: **P2 Badge Update the dashboard generators with W5 authorization** When this status report starts declaring W3.5 resolved and W5 authorized, the canonical planner path still rewrites the repository back to the old state: 'make dashboard'...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR238:PRRT_kwDOTH_vCM6Swy90

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/w3-5-claim-impact-result-v1.0.json:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/238#discussion_r3626587380
- Claim: **P2 Badge Synchronize the central claim registry during claim-impact closure** This new claim-impact artifact completes the 'central_claim_impact_audit' and authorizes W5, but the canonical 'theory/evaluation/central-claim-registry.json...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR239:PRRT_kwDOTH_vCM6SxUIT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/s-core-construction-obstruction-ledger.json:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782560
- Claim: **P1 Badge Update the authoritative ledger before marking W5 complete** This promotes the machine-readable ledger to W5-complete, but the same registry still declares 'statement_authority' as 'source_artifact', and 'docs/research/s-core-...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR239:PRRT_kwDOTH_vCM6SxUIX

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_thm_target_001.py:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782564
- Claim: **P1 Badge Register W5 as satisfying the scoped proof gate** After this commit marks the bounded S_core theorem proved, this assertion locks 'research-gates.json' in the old pre-W5 state: 'scoped-representation-proof' remains 'not_satisf...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR239:PRRT_kwDOTH_vCM6SxUIb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_thm_target_001.py:122`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/239#discussion_r3626782568
- Claim: **P2 Badge Align central claims with the bounded W5 theorem** With W5 now proving 'THM-CORE-COMMON-001' and 'THM-CORE-REP-001', the central claim registry is left contradictory: 'CLM-EXISTENCE', 'CLM-SUFFICIENCY', and 'CLM-REP-CAPACITY' ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR240:PRRT_kwDOTH_vCM6Sxc8r

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/lean/SCoreW5.lean:55`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/240#discussion_r3626834839
- Claim: **P1 Badge Make FaithfulSplit enforce the frozen contract** The new registry/doc present this as machine-checking the registered W5 'Faithful_split', but this definition only requires a constructor id and a few list equalities; it omits ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR240:PRRT_kwDOTH_vCM6Sxc8v

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/s-core-w5-lean-mechanization.json:30`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/240#discussion_r3626834843
- Claim: **P2 Badge Reconcile the canonical W5 gate with this claim** When this new artifact marks 'bounded_faithful_representation' as 'machine_checked', the canonical theorem target it names is left inconsistent: 'theory/evaluation/thm-target-0...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR241:PRRT_kwDOTH_vCM6Sx4fi

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/s-core-w5-independent-review-package-v1.0.json:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/241#discussion_r3626998461
- Claim: **P2 Badge Register all mandatory proof dependencies** The frozen source list jumps directly from the construction-obstruction ledger to the W5 assembly, but the review package’s own artifact map requires reviewers to inspect W0-W4 and W...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR241:PRRT_kwDOTH_vCM6Sx4fk

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_s_core_w5_review_package.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/241#discussion_r3626998465
- Claim: **P2 Badge Compare frozen hashes to file contents** This check only compares the JSON-declared 'git_blob_sha' to another hard-coded string, so if the protected artifact changes while the registry still carries the old hash, the validator...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR242:PRRT_kwDOTH_vCM6Sy_r1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/planning/architecture-neutral-research-roadmap.md:119`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/242#discussion_r3627420080
- Claim: **P2 Badge Align the generated task queue with USD W1** This roadmap now makes 'USD-W1-SCOPE-EXT' the immediate next action, but the generated planning pipeline still contradicts it: 'make plan' runs 'tools/self_advancement_plan.py', whi...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR243:PRRT_kwDOTH_vCM6SzFwm

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-partial-observability-fixtures-v1.0.json:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/243#discussion_r3627455024
- Claim: **P2 Badge Make positive fixtures satisfy S_po_fin** When this history-sensitive fixture is used to support the registered 'pass', it is not an admitted 'S_po_fin' source presentation: the scope contract added in this commit requires an ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR243:PRRT_kwDOTH_vCM6SzFwo

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-partial-observability-extension-result-v1.0.json:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/243#discussion_r3627455026
- Claim: **P2 Badge Use canonical USD theorem IDs** These theorem-effect keys do not match the frozen target registry: 'theory/evaluation/universal-structure-discovery-target-v1.0.json' defines the parameterized IDs as 'THM-US-INV-001[K]' and 'TH...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR244:PRRT_kwDOTH_vCM6SzTq5

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-infinite-carriers-scope-v1.0.json:24`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/244#discussion_r3627535726
- Claim: **P1 Badge Preserve admitted observations in the obligations** The scope admits 'observations' as part of 'S_inf_eff', but the registered/proved obligations never require observation relations or evidential-status distinctions to be pres...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR245:PRRT_kwDOTH_vCM6Szcon

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json:16`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/245#discussion_r3627588070
- Claim: **P1 Badge Require computable guard-crossing certificates** For admitted sources where a guard has isolated crossings but the source does not declare computable brackets, separation/transversality data, or a finite event enumerator, the ...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR245:PRRT_kwDOTH_vCM6Szcoo

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tests/test_usd_w1_continuous_dynamics.py:19`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/245#discussion_r3627588072
- Claim: **P2 Badge Put these tests on the canonical unittest path** When the project’s canonical 'tools/run_tests.py'/'make test' path is used, 'unittest.TestLoader.loadTestsFromModule' only collects 'unittest.TestCase' tests, so these top-level...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR246:PRRT_kwDOTH_vCM6SzrWU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-open-ended-histories-scope-v1.0.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/246#discussion_r3627674001
- Claim: **P2 Badge Exclude completed finite histories from the scope** When the admitted history domain includes 'a finite ... sequence', a completed finite trace with a fixed terminal event count is in scope, but the same contract/proof claims ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR249:PRRT_kwDOTH_vCM6S0g9r

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-actual-process-correspondence-scope-v1.0.json:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/249#discussion_r3627993773
- Claim: **P2 Badge Add the measurement-to-source mapping to the scope** The report freezes a future positive APC package that includes “a mapping from measurements to source states and transitions” (docs/research/usd-w1-actual-process-correspond...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR249:PRRT_kwDOTH_vCM6S0g9v

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w1-actual-process-correspondence-result-v1.0.json:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/249#discussion_r3627993780
- Claim: **P2 Badge Sync the program registry before routing to W2** This result routes the next decisive workstream to 'USD-W2-ALT-VOCAB', but the governing program registry still records 'USD-W1-SCOPE-EXT' as 'registered_unexecuted' and 'next_d...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR250:PRRT_kwDOTH_vCM6S0qkt

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:63`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/250#discussion_r3628051855
- Claim: **P2 Badge Record the missing GREL/ARG-HIST comparison** With four candidates, the completed pairwise ledger needs six unordered comparisons, but this array records only five and omits 'GREL-001' vs 'ARG-HIST-001'. Any downstream audit o...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR250:PRRT_kwDOTH_vCM6S0qkx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w2-alternative-vocabulary-competition-v1.0.json:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/250#discussion_r3628051860
- Claim: **P2 Badge Reclassify LTS-PROV versus ARG-HIST consistently** Under the dominance rule recorded in the audit, 'LTS-PROV-001' is no worse on coverage/preservation ('pass' vs 'partial') and has lower registered costs on every numeric cost ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR251:PRRT_kwDOTH_vCM6S0zhD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w3-representation-invariance-contract-v1.0.json:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104186
- Claim: **P1 Badge Add the missing semantic-interface transform** The governing 'POST-W5-USD-001' definition for 'USD-W3-INVARIANCE' requires the semantic-interface replacement class, but this contract's exhaustive 'transformations' list has no ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR251:PRRT_kwDOTH_vCM6S0zhH

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:38`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104192
- Claim: **P2 Badge Test GREL before preserving its dominance relations** These '*_vs_GREL' outcomes are published even though 'GREL-001' is omitted from both contract and result 'tested_vocabularies', and the checker asserts exactly that two-voc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR251:PRRT_kwDOTH_vCM6S0zhL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w3-representation-invariance-result-v1.0.json:50`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/251#discussion_r3628104195
- Claim: **P2 Badge Use the registered USD-W4-NECESSITY workstream id** Repo-wide search finds 'USD-W4-ABLATION' only in this new W3 package, while the governing POST-W5 program registers the next W4 id as 'USD-W4-NECESSITY'. Emitting the unregis...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR252:PRRT_kwDOTH_vCM6S1nVJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w4-ablation-reconstruction-result-v1.0.json:61`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/252#discussion_r3628403071
- Claim: **P1 Badge Do not advance to W5 before W4 controls are run** When this result is consumed to schedule the next USD workstream, it skips part of the registered W4 gate: the frozen program defines Workstream 4 as 'USD-W4-NECESSITY' and req...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR253:PRRT_kwDOTH_vCM6S12uq

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w5-minimality-equivalence-contract-v1.0.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/253#discussion_r3628492372
- Claim: **P2 Badge Include GREL in the successful set** When downstream W5 consumers use this contract as the frozen success set, 'GREL-001' is incorrectly dropped even though the W2 bounded competition records that all candidates except 'ARG-HI...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR254:PRRT_kwDOTH_vCM6S2A_u

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/usd-w6-independence-result-v1.0.json:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/254#discussion_r3628552153
- Claim: **P1 Badge Do not mark W6 executed without executable artifacts** This block records a completed three-path execution with artifact isolation, a separate verifier, deterministic comparison, and mutation pass, but the commit only adds JSO...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR255:PRRT_kwDOTH_vCM6S611M

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/255#discussion_r3630313815
- Claim: **P2 Badge Keep USD-H-DISC within the registered GREL support** This terminal disposition broadens reasoning-discrimination support to 'ARG-HIST', but the USD-W2 source only records 'USD-H-DISC' as 'supported_boundedly_against_GREL_001' ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR255:PRRT_kwDOTH_vCM6S611P

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/255#discussion_r3630313820
- Claim: **P2 Badge Synchronize terminal outcome with status registry** Declaring this synthesis as the 'incomparable_kernels' program outcome adds a completed USD result, but the repository status surfaces still report the old state: 'theory/eva...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR256:PRRT_kwDOTH_vCM6S7HDC

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json:15`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/256#discussion_r3630412997
- Claim: **P2 Badge Include the EVC parent program in the manifest** This 'program_and_synthesis' group lists the pre-W5 USD program but omits 'theory/evaluation/post-w5-usd-next-program-v1.0.json', even though the new protocol declares 'parent_p...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR258:PRRT_kwDOTH_vCM6S8A12

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json:39`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/258#discussion_r3630743615
- Claim: **P2 Badge Gate all twelve adversarial challenges** The protocol’s terminal rules are keyed to 'mandatory_attack_domains', but this list stops before the two corpus domains added as R4-C11 and R4-C12 ('candidate_universe' and 'correspond...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR260:PRRT_kwDOTH_vCM6S-n2N

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:12`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/260#discussion_r3631702770
- Claim: **P2 Badge Wire the IKD queue into canonical planning** In the current repo, 'tools/generate_next_tasks.py' is still the command behind 'make plan'/'docs/planning/next-actions.md', and I checked it still hard-codes the old W3.5 STRATEGIC...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR260:PRRT_kwDOTH_vCM6S-n2U

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:37`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/260#discussion_r3631702779
- Claim: **P2 Badge Block candidate scoring in the queue** The prose registration says PR #261 must freeze admission controls and “must not execute candidate scoring” ('docs/research/post-usd-internal-discovery-continuation-v1.0.md:63'), but the ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR261:PRRT_kwDOTH_vCM6S-3sQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/261#discussion_r3631793680
- Claim: **P1 Badge Fill mandatory candidate declarations before freezing** These objects are admitted as 'admitted_frozen_unscored', but each frozen candidate only has source/primitives/constraint fields and omits the rest of 'admission_rule.req...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR266:PRRT_kwDOTH_vCM6TBUHR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_post_usd_internal_discovery_continuation.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/266#discussion_r3632706842
- Claim: **P2 Badge Restore validation for the IKD-W6 queue state** Since 'next_pr' still allows 266 above, making the only exact queue-shape check 'if next_pr==267' means the standalone validator no longer rejects an IKD-W6-active queue with the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR267:PRRT_kwDOTH_vCM6TBxUH

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/ikd-w7-lower-bounds-v1.0.json:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/267#discussion_r3632877103
- Claim: **P2 Badge Leave W7 unresolved until all countermodels are closed** Because this result is used to move the queue to IKD-W8, marking W7 complete here skips part of the registered W6 handoff: docs/audits/ikd-w6-global-reconstruction-audit...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR268:PRRT_kwDOTH_vCM6TDpuf

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/ikd-w8-minimal-frontier-v1.0.json:69`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/268#discussion_r3633577183
- Claim: **P2 Badge Record the componentwise frontier evidence** For the W8 frontier result, this records only the final kernel and realization sets, but not the componentwise cost ledger, dominance/incomparability matrix, or a precise reference ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR268:PRRT_kwDOTH_vCM6TDpum

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json:39`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/268#discussion_r3633577187
- Claim: **P2 Badge Keep pre-W9 bounded kernel claims blocked** With 'next_action' now pointing at W9, narrowing the blocked claim to only unrestricted universality leaves a bounded universal/common-kernel claim unblocked before terminal adjudica...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR270:PRRT_kwDOTH_vCM6TEQDL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/research/post-w9-internal-scope-challenge-v1.0.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/270#discussion_r3633800226
- Claim: **P2 Badge Add an explicit status to the challenge document** When this new 'docs/research' artifact is audited directly, it has no '## Status' section, so the document itself does not state whether it is accepted, research, provisional,...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR277:PRRT_kwDOTH_vCM6TGN_S

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/tue-w1-unknown-boundary-audit.md:5`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/277#discussion_r3634548449
- Claim: **P1 Badge Preserve the registered uninstrumented boundary** When this W1 package is used to authorize advancing the queue to PR 278, changing the inherited creative Unknown to 'instrumentable creative generation' means the completed wor...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR278:PRRT_kwDOTH_vCM6TGhkw

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_tue_w2_defeating_condition_campaign.py:34`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/278#discussion_r3634662053
- Claim: **P1 Badge Require every frozen attack family to be exercised** This check only proves that each defeating condition has at least one case, but the protocol freezes specific 'precommitted_attack_families'. In the current artifacts, searc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR279:PRRT_kwDOTH_vCM6TGrkv

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_tue_w3_deeper_kernel.py:41`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/279#discussion_r3634720987
- Claim: **P2 Badge Handle the terminal queue state in W3 checks** When PR #280 completes, the repository’s own terminal-queue contract requires 'status == "complete"', 'next_action is None', and completed workstreams '[276, 277, 278, 279, 280]' ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR279:PRRT_kwDOTH_vCM6TGrkz

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_tue_w2_defeating_condition_campaign.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/279#discussion_r3634720991
- Claim: **P2 Badge Accept completed queues in the W2 live check** After PR #280, the authorized queue state has 'next_action' set to 'None', but this W2 regression check still dereferences 'queue["next_action"]' and only allows the in-progress P...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR280:PRRT_kwDOTH_vCM6THCUb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-sc-terminal-universality-extension-closure-v1.0.json:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/280#discussion_r3634855220
- Claim: **P2 Badge Clear the live TUE queue when declaring no next action** This declares the terminal program closed, but the unchanged 'theory/evaluation/post-sc-terminal-universality-extension-queue-v1.0.json' still has 'status: "frozen"' wit...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR281:PRRT_kwDOTH_vCM6THZ2F

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/research/upp-theorem-target-v1.0.md:22`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/281#discussion_r3634995151
- Claim: **P2 Badge Bind S in the sufficiency target** When later workstreams mechanize UPP-W12/W15, this sufficiency obligation leaves 'S' free: unlike the necessity target above, it never says 'forall S in C*' or otherwise fixes the domain. Tha...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR281:PRRT_kwDOTH_vCM6THZ2G

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_post_tue_universal_proof_program.py:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/281#discussion_r3634995152
- Claim: **P2 Badge Validate the active queue checkpoint** This checker only defines and loads the program artifact, so the new active queue checkpoint can drift undetected. If 'post-tue-universal-proof-queue-checkpoint-v1.0.json' skips W1, adver...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR282:PRRT_kwDOTH_vCM6THfYY

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/foundation/upp_foundation_v1.py:218`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027651
- Claim: **P2 Badge Validate grounds references before accepting a system** When a transition carries a typo or missing id in 'grounds', 'ReasoningSystem.validate()' still returns success because this loop only resolves the source and target stat...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR282:PRRT_kwDOTH_vCM6THfYZ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/foundation/upp_foundation_v1.py:185`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027652
- Claim: **P2 Badge Add recovery witnesses to system validation** When downstream workstreams attach recovery evidence to a reasoning system, this aggregate model has no 'RecoveryWitness' collection, so the system validator cannot enforce that ea...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR282:PRRT_kwDOTH_vCM6THfYd

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/foundation/upp_foundation_v1.py:171`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/282#discussion_r3635027656
- Claim: **P2 Badge Validate parsed recovery statuses by value** If a witness is hydrated from the machine-readable artifacts, 'status' will commonly be the string '"recovered"' rather than a 'RecoveryStatus' instance; because this uses identity ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR283:PRRT_kwDOTH_vCM6TIDhg

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/class/upp_target_class_v1.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/283#discussion_r3635243050
- Claim: **P2 Badge Reject the actual RCCD obligation names** UPP-W1's W2 handoff says the class-neutrality audit must reject RCCD, R1-R5, their named formulations, and semantic construct loading (docs/research/upp-w1-foundation-v1.0.md:36), and ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR284:PRRT_kwDOTH_vCM6TIXCy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/contract/upp_faithfulness_contract_v1.py:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/284#discussion_r3635359587
- Claim: **P2 Badge Coerce verdict values before validation** When assessments are built from JSON/CLI data, 'verdict' will be a plain string such as '"pass"' or '"unknown"'. These 'is' checks then skip the evidence/reason requirements, while enu...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR284:PRRT_kwDOTH_vCM6TIXCz

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_upp_w3_contract.py:10`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/284#discussion_r3635359589
- Claim: **P2 Badge Run the W3 checker from regression tests** The new deterministic checker is never invoked by this test module, unlike the W1/W2 test suites, and it is not included in the Makefile health targets. CI can therefore pass if the W...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR285:PRRT_kwDOTH_vCM6TIa4M

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/representations/upp_representation_universe_v1.py:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/285#discussion_r3635382804
- Claim: **P2 Badge Allow effectively realized oracle support** For candidates that include an inventoried oracle claim, the new universe spec lists 'oracle' as a support kind and excludes only oracle use without an effective realization ('theory...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR286:PRRT_kwDOTH_vCM6TIf5H

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/machinery/upp_machinery_closure_v1.py:41`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/286#discussion_r3635412254
- Claim: **P2 Badge Limit effectiveness failures to required support** Because 'validate()' runs on every declared node before reachability, this check makes an otherwise closed package open whenever it declares optional present-but-ineffective s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR286:PRRT_kwDOTH_vCM6TIf5I

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/machinery/upp_machinery_closure_v1.py:122`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/286#discussion_r3635412255
- Claim: **P2 Badge Continue through unresolved required targets** When a required disclosed edge has 'evidence=UNKNOWN', this 'continue' prevents traversal into the declared target. If that target has its own required missing or concealed depend...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR287:PRRT_kwDOTH_vCM6TImCR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/equivalence/upp_representation_equivalence_v1.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/287#discussion_r3635447837
- Claim: **P2 Badge Reject undeclared dependency facts** For a closed package where a dependency tuple mentions a fact that is absent from 'facts', this validation returns no error; if the correspondence adds extra 'fact_map' entries for that und...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR287:PRRT_kwDOTH_vCM6TImCU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:14`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/287#discussion_r3635447841
- Claim: **P2 Badge Keep prior W5 validation reproducible** Advancing 'next_action' to PR 288 here leaves 'tools/check_upp_w5_machinery_closure.py' still requiring the queue to equal '{'target_pr': 287, 'workstream': 'UPP-W6-EQUIVALENCE'}'; after...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR288:PRRT_kwDOTH_vCM6TJvkl

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/necessity/upp_recoverable_commitment_v1.py:65`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/288#discussion_r3635879012
- Claim: **P2 Badge Require queries to actually recover commitments** When 'query_to_commitment' is empty, or when it omits a listed commitment, this 'all(...)' check is vacuously true as long as 'total_on_registered_queries' is true. That lets '...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR289:PRRT_kwDOTH_vCM6TJ0hQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/necessity/upp_w8_constrained_evolution_v1.py:90`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/289#discussion_r3635907650
- Claim: **P2 Badge Validate transition context before returning Unknown** When a commitment-changing transition has 'admissible=Truth.UNKNOWN', these lines return 'UNKNOWN' before the checks that reject empty IDs, erased 'history_prefix', or mis...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR290:PRRT_kwDOTH_vCM6TJ7wQ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:17`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/290#discussion_r3635950301
- Claim: **P1 Badge Keep the queue on the registered W10 workstream** For the post-W9 state, this advances PR 291 to 'UPP-W10-SEMANTIC-INTERPRETATION', but the registered universal-proof program still defines target PR 291 as 'UPP-W10-R4' with pu...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR290:PRRT_kwDOTH_vCM6TJ7wS

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/foundation/upp_dependency_structure_v1.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/290#discussion_r3635950306
- Claim: **P2 Badge Reject duplicate relations before proving the witness** When an assessment contains two edges with different 'edge_id's but the same source, target, kind, and temporal scope, this validation passes and 'assess_dependency_struc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR291:PRRT_kwDOTH_vCM6TKCL7

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:18`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/291#discussion_r3635987842
- Claim: **P1 Badge Keep the UPP queue on the registered workstream** 'theory/evaluation/post-tue-universal-proof-program-v1.0.json' still registers PR 292 as 'UPP-W11-R5' for uniform-effective-recovery, but this queue update sends PR 292 to 'UPP...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR291:PRRT_kwDOTH_vCM6TKCL8

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/foundation/upp_semantic_interpretation_v1.py:126`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/291#discussion_r3635987843
- Claim: **P2 Badge Require coverage of registered semantic items** When all premises are yes, this returns 'PROVED' for any non-empty consistent mapping, but 'SemanticAssessment' only contains the supplied interpretations and no registered item/...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR292:PRRT_kwDOTH_vCM6TKJkz

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:19`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/292#discussion_r3636029948
- Claim: **P1 Badge Keep PR #293 aligned with registered sufficiency workstream** The registered UPP plan assigns target PR 293 to 'UPP-W12-SUFFICIENCY' and puts component independence/irreducibility at target PR 294 ('theory/evaluation/post-tue-...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR292:PRRT_kwDOTH_vCM6TKJk3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/history/upp_historical_trace_v1.py:94`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/292#discussion_r3636029955
- Claim: **P2 Badge Validate dependency and reason links chronologically** When a trace uses 'dependency_ids' or 'reason_ids' that point to later events, this loop ignores those references, so 'obligations()' can still mark the structural obligat...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR293:PRRT_kwDOTH_vCM6TKVUC

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/independence/upp_component_independence_v1.py:53`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/293#discussion_r3636098309
- Claim: **P2 Badge Reject unregistered reduction sources** When a proposed reduction names a source outside the five registered components, this guard still allows it through; for example 'ReductionAttempt("recoverable_commitment", frozenset({"h...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR293:PRRT_kwDOTH_vCM6TKVUH

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_upp_w11_historical_trace.py:94`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/293#discussion_r3636098314
- Claim: **P2 Badge Handle terminal queues in the W11 checker** This checker is still invoked by 'tests/test_upp_w11_historical_trace.py', but the new forward-progress logic assumes 'next_action' is always an object. When the UPP queue reaches a ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR294:PRRT_kwDOTH_vCM6TKdMI

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:21`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/294#discussion_r3636143762
- Claim: **P1 Badge Point the queue at the registered PR #295 workstream** When a runner follows this active queue, it is sent to 'UPP-W14-IRREDUCIBILITY-MAXIMALITY', but the registered universal proof program has no such workstream; I checked 't...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR295:PRRT_kwDOTH_vCM6TLOM-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/irreducibility/upp-irreducibility-maximality-v1.0.json:8`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440071
- Claim: **P2 Badge Point to an accepted irreducibility result** This metadata names 'UPP-W13-IRREDUCIBILITY' as the supporting prior result, but the completed PR #294 artifact is 'UPP-W13-SUFFICIENCY-CONSTRUCTION' and it explicitly lists 'does_n...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR295:PRRT_kwDOTH_vCM6TLONF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/upp-w13-sufficiency-construction-result-v1.0.json:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440081
- Claim: **P2 Badge Keep the W13 audit in sync with the successor** Changing the W13 successor here to 'UPP-W14-MAXIMALITY' leaves the W13 audit saying completion advances to 'UPP-W14-IRREDUCIBILITY-MAXIMALITY' ('docs/audits/upp-w13-sufficiency-c...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR295:PRRT_kwDOTH_vCM6TLONJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/irreducibility/upp_irreducibility_maximality_v1.py:117`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/295#discussion_r3636440085
- Claim: **P2 Badge Classify excluded challenges before checking embeddings** When a registered challenge is already excluded from the target class and records 'embeds_in_rccd=None' as not applicable, this check returns 'UNKNOWN' before line 118 ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR296:PRRT_kwDOTH_vCM6TK9sE

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json:26`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636341762
- Claim: **P1 Badge Keep historical UPP checkers compatible with terminal closure** With this checkpoint now terminal ('next_action: null' and the public gate open), the existing W1-W11 validation tools still read the same checkpoint as if it wer...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR296:PRRT_kwDOTH_vCM6TK9sG

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/terminal/upp_terminal_theorem_v1.py:75`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636341765
- Claim: **P2 Badge Honor blocked-dependency precedence before defeating overclaims** For evidence that both contains an unresolved or absent required property and sets an overclaim flag, this branch returns 'REFUTED/DEFEATED' before the unresolv...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR296:PRRT_kwDOTH_vCM6TLCCD

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `theory/terminal/upp_terminal_theorem_v1.py:87`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/296#discussion_r3636367923
- Claim: **P2 Badge Block full proof when terminal composition is absent** When evidence has 'central_semantic_theorem_kernel_checked=True' but 'executable_composition_verified=False', this early return selects 'FULL/PROVED' before the later miss...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR297:PRRT_kwDOTH_vCM6TRTNk

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post_terminal_public_evaluation_v1.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/297#discussion_r3638690913
- Claim: **P2 Badge Use registry prohibited-promotion tokens** When a submission uses the identifiers published by 'theory/evaluation/post-terminal-public-evaluation-program-v1.0.json', several banned overclaims bypass the executable check becaus...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR297:PRRT_kwDOTH_vCM6TRTNr

- Disposition: `unresolved`
- Confidence: `high`
- Location: `theory/evaluation/post_terminal_public_evaluation_v1.py:47`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/297#discussion_r3638690922
- Claim: **P2 Badge Reject unsupported evidence types** The adjudicator stores 'evidence_type' but never checks it against the registered evidence-type vocabulary, so a submission with 'evidence_type="not_a_type"' and otherwise-confirming flags i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR299:PRRT_kwDOTH_vCM6TUCdN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/decision.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/299#discussion_r3639707213
- Claim: **P2 Badge Check open closure before returning review** When 'candidate_closure' is 'OPEN' and any confirmed-medium or inferred high/critical finding is active, this early return prevents the later open-closure check from running. That c...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR300:PRRT_kwDOTH_vCM6TUJa1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/adversarial.py:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/300#discussion_r3639747352
- Claim: **P1 Badge Import the existing closure API** In this repo 'closure.py' only defines/exports 'assess_closure'; 'compute_closure' is not present, so importing 'far_release_assurance.adversarial' raises 'ImportError' before any scenario can...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR301:PRRT_kwDOTH_vCM6TU77g

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/cli.py:56`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039795
- Claim: **P1 Badge Include observed machinery in inventory closure** When a package includes an 'event.machinery_refs' entry for machinery that is not also listed as a root or dependency (for example, a disclosed undeclared tool used by an event...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR301:PRRT_kwDOTH_vCM6TU77m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/io.py:80`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039804
- Claim: **P1 Badge Reject missing declared flags instead of assuming true** When an external package omits 'declared' or sends a non-boolean value such as '"false"', this expression coerces it to 'True', even though the schema makes 'declared' a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR301:PRRT_kwDOTH_vCM6TU77t

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/io.py:211`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/301#discussion_r3640039813
- Claim: **P2 Badge Reject non-standard JSON constants** For package files containing Python's accepted 'NaN'/'Infinity' constants inside attributes or metrics, 'json.loads' succeeds even though the input is not valid JSON; 'validate' then exits ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR302:PRRT_kwDOTH_vCM6TVB66

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075282
- Claim: **P1 Badge Review declared consequential additions** This added-machinery branch emits findings only for undeclared items and mutable policies, so a candidate that adds a declared/confirmed 'memory', 'external-state', or 'benchmark' depe...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR302:PRRT_kwDOTH_vCM6TVB6-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:137`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075291
- Claim: **P1 Badge Review changed required machinery** When a required item changes but remains declared and confirmed, this condition only creates a finding for mutable or unversioned policies; changed model/tool/policy versions otherwise fall ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR302:PRRT_kwDOTH_vCM6TVB7E

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:188`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075297
- Claim: **P1 Badge Match withdrawals by event order** Because withdrawals are collapsed into an unordered set by subject, any earlier or unrelated 'commitment_withdrawn' for the same commitment suppresses the invalidated-support finding for a la...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR302:PRRT_kwDOTH_vCM6TVB7N

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/compare.py:206`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/302#discussion_r3640075307
- Claim: **P1 Badge Match identity revalidation by event order** These global counts treat any 'identity_revalidated' event as covering any 'identity_changed' event, even if the revalidation happened before the change or for a different identity ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR303:PRRT_kwDOTH_vCM6TVMqb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/cli.py:20`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/303#discussion_r3640138711
- Claim: **P2 Badge Return the documented gate exit codes** The commercial CLI contract still defines exact gate codes as 2/3/4 for review-required/blocked/unknown (commercial/far-release-assurance/ARCHITECTURE.md:258-263), but this table makes t...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR303:PRRT_kwDOTH_vCM6TVMqf

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/src/far_release_assurance/report.py:98`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/303#discussion_r3640138717
- Claim: **P2 Badge Escape package strings before rendering Markdown** For packages whose 'release_id' or 'source_commit' contains Markdown control characters such as backticks or newlines, this raw interpolation can break out of the inline code ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR305:PRRT_kwDOTH_vCM6TVbST

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-release-assurance-e2e-gate.yml:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/305#discussion_r3640224198
- Claim: **P2 Badge Fetch full history for evidence checkout** The release-assurance CI design I checked requires this job to check out full history before producing evidence ('commercial/far-release-assurance/ARCHITECTURE.md:321-334'), but this ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR306:PRRT_kwDOTH_vCM6TVtkK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:96`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/306#discussion_r3640330535
- Claim: **P2 Badge Require explicit unknown and authorization fields** When a package omits 'authorization_requirements' or 'unknowns', these defaults silently coerce the absence to an empty tuple, so a payload that never declared “no requiremen...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR307:PRRT_kwDOTH_vCM6TVt_a

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/307#discussion_r3640332959
- Claim: **P2 Badge Require an authorizing edge for authorization requirements** When a required authorization node has any edge into the decision root, this treats the requirement as satisfied without checking 'dependency.relation'; because the ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR308:PRRT_kwDOTH_vCM6TVyWI

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/docs/refund-authorization-v0.1.md:1`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/308#discussion_r3640357185
- Claim: **P1 Badge Add an explicit artifact status** This new reference-domain artifact has no 'Status' or '## Status', so its required single status cannot be audited and readers cannot tell whether it is Accepted, Research, Provisional, Archiv...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR308:PRRT_kwDOTH_vCM6TVyWK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/refund.py:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/308#discussion_r3640357187
- Claim: **P2 Badge Reject pre-purchase refund windows** When 'days_since_purchase' is negative, this check still marks the 30-day window requirement as satisfied, so an otherwise complete request with 'days_since_purchase=-1' adjudicates as 'jus...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR309:PRRT_kwDOTH_vCM6TV50T

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:23`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/309#discussion_r3640400953
- Claim: **P1 Badge Keep the legacy audit CLI path working** When existing callers invoke 'far-decision [--output ...]', the new subparser treats the package path as an invalid command before the audit code or invalid-package handling can run. I ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR309:PRRT_kwDOTH_vCM6TV50X

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/authorization.py:43`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/309#discussion_r3640400960
- Claim: **P2 Badge Reject boolean values for refund amounts** For inputs that serialize 'amount' as JSON 'true' or 'false', this coercion treats the boolean as '1.0' or '0.0' instead of invalid input, and a request with all other requirements tr...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR310:PRRT_kwDOTH_vCM6TV9Kf

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/policy_impact.py:128`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/310#discussion_r3640420134
- Claim: **P1 Badge Block escalate-to-allow policy changes** When a candidate removes a required evidence check, a request that previously escalated because the fact was unknown can become allowed, but this branch only treats 'BLOCK -> ALLOW' as ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR310:PRRT_kwDOTH_vCM6TV9Ki

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/policy_cli.py:33`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/310#discussion_r3640420138
- Claim: **P2 Badge Validate case JSON before building refund requests** When cases are loaded from JSON, constructing 'RefundRequest' directly bypasses the validation used by the runtime loader, so malformed fixture types can be evaluated as rea...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR311:PRRT_kwDOTH_vCM6TWLBi

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/cli.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/311#discussion_r3640500302
- Claim: **P2 Badge Restore legacy audit path for console invocations** When 'far-decision' is invoked through the installed console script, 'main()' is called with 'argv=None', so 'arguments' stays 'None' and this compatibility branch is skipped...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR311:PRRT_kwDOTH_vCM6TWLBm

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/regression.py:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/311#discussion_r3640500307
- Claim: **P2 Badge Reject non-object run entries as invalid input** If a supplied regression suite contains a non-object entry inside 'baseline' or 'candidate' (for example 'null'), this subscript raises 'TypeError' before 'regression_cli.main()...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR312:PRRT_kwDOTH_vCM6TWZeA

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/trace_ingest.py:58`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/312#discussion_r3640583396
- Claim: **P1 Badge Filter ingestion to the selected trace** This loop normalizes every span in the export after choosing one root, but OTLP exports commonly contain batches with spans from multiple traces. If the file has one FAR root for 'trace...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR313:PRRT_kwDOTH_vCM6TWucb

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/instrumentation.py:179`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/313#discussion_r3640708680
- Claim: **P2 Badge Reserve provenance keys before emitting node attributes** When callers record a node attribute named '_far_source', this flattening emits it as 'far.node.attribute._far_source', but the existing ingester unconditionally replac...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR314:PRRT_kwDOTH_vCM6TW6hD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:75`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777758
- Claim: **P2 Badge Serialize evidence writes before hashing** When two identical '/v1/authorize' POSTs are handled concurrently, they intentionally resolve to the same 'evidence_id', and 'serve()' runs them in a 'ThreadingHTTPServer'; these dige...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR314:PRRT_kwDOTH_vCM6TW6hF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:168`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777761
- Claim: **P2 Badge Bound the decision-id path component** For an otherwise valid package with a long 'decision_id', this unbounded sanitized value becomes a single directory-name component, so common filesystems raise 'OSError: File name too lon...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR314:PRRT_kwDOTH_vCM6TW6hJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/service.py:126`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/314#discussion_r3640777766
- Claim: **P2 Badge Reject non-standard JSON constants** When a client sends 'NaN', 'Infinity', or '-Infinity' inside payload fields that are not validated as bounded numbers, such as 'proposed_action' or 'metadata', Python's default 'json.loads'...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR315:PRRT_kwDOTH_vCM6TXCNN

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/store.py:121`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/315#discussion_r3640823725
- Claim: **P1 Badge Reject path traversal in evidence IDs** Because 'evidence_id' comes directly from the source manifest, 'self.blob_root / evidence_id' allows values like '../escape' or an absolute path to place the canonical blob directory out...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR315:PRRT_kwDOTH_vCM6TXCNX

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/store.py:70`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/315#discussion_r3640823736
- Claim: **P2 Badge Support the advertised runtime evidence format** At this point 'put_directory()' rejects manifests that do not contain 'evidence_id' and 'input_type'. The FAR runtime path advertised in 'EVIDENCE_STORE.md' still writes 'far-au...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR316:PRRT_kwDOTH_vCM6TXIZT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/security.py:190`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/316#discussion_r3640859442
- Claim: **P2 Badge Sanitize tenant evidence identifiers before returning** When tenant IDs or evidence IDs contain path separators or absolute-path prefixes, this helper returns them unchanged around the digest. The new contract recommends using...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR316:PRRT_kwDOTH_vCM6TXIZX

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/security.py:48`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/316#discussion_r3640859449
- Claim: **P2 Badge Reject dots in key IDs before storing credentials** A key registered with a 'key_id' containing '.' is accepted here, but 'authenticate()' parses bearer tokens with 'token.split('.', 1)', so 'key.with.dot.secret' is looked up ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR317:PRRT_kwDOTH_vCM6TXS0G

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/317#discussion_r3640920597
- Claim: **P1 Badge Use exact tenant ownership for evidence reads** When one tenant ID is another tenant ID followed by '-' (for example 'tenant' and 'tenant-a'), this prefix check authorizes the shorter tenant to read the longer tenant's evidenc...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR317:PRRT_kwDOTH_vCM6TXS0N

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:44`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/317#discussion_r3640920604
- Claim: **P2 Badge Include the policy binding in secured evidence IDs** For the same tenant and decision payload, 'raw_evidence_id' is deterministic only from the FAR input, so changing the active 'policy_id'/version produces the same 'secured_i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR318:PRRT_kwDOTH_vCM6TX-ii

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/operations.py:234`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/318#discussion_r3641176869
- Claim: **P1 Badge Reject missing blob roots during backup** When an operator passes a nonexistent '--blob-root' (for example a typo, unmounted volume, or wrong deployment path), this branch silently skips copying evidence blobs and writes a man...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR319:PRRT_kwDOTH_vCM6TYhUh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:82`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/319#discussion_r3641382514
- Claim: **P2 Badge Preserve idempotent evidence manifests across upgrade** Deployments with evidence already written by secured-service 0.1 can no longer retry the same authorization after this change: the secured evidence id is still derived on...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR319:PRRT_kwDOTH_vCM6TYhUi

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:118`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/319#discussion_r3641382515
- Claim: **P2 Badge Validate admin JSON field types before mutation** The new admin HTTP adapter lets malformed JSON change behavior before 'OperationsStore' validation: 'tuple(...)' raises an uncaught 'TypeError' for '"scopes": null', while 'boo...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR320:PRRT_kwDOTH_vCM6TYpZx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/hardening.py:60`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/320#discussion_r3641428944
- Claim: **P1 Badge Require database files before reporting restore success** For a backup whose manifest omits 'security.db'/'evidence.db', 'verify_backup()' currently returns valid because its SQLite integrity check opens missing paths and crea...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR320:PRRT_kwDOTH_vCM6TYpZy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/hardening.py:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/320#discussion_r3641428946
- Claim: **P2 Badge Report retention failure when blob deletion fails** When an expired blob directory cannot be removed, for example because of permissions or filesystem errors, 'ignore_errors=True' suppresses the failure after the database rows...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR321:PRRT_kwDOTH_vCM6TYtSh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/EXTERNAL_IDENTITY.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/321#discussion_r3641451725
- Claim: **P2 Badge Add required provenance before promoting the adapter contract** Because this new document promotes the external identity/observability adapter as a package contract without a status/provenance record or link to the execution/o...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR321:PRRT_kwDOTH_vCM6TYtSp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/external_identity.py:127`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/321#discussion_r3641451733
- Claim: **P2 Badge Reject malformed temporal claims without crashing** When a token is correctly signed but omits or uses a non-integer 'iat'/'exp', these conversions run outside the parsing error path, so 'verify()' raises raw 'TypeError'/'Valu...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR322:PRRT_kwDOTH_vCM6TY-OJ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/oidc.py:110`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552494
- Claim: **P1 Badge Reject unsafe OIDC tenant identifiers** When OIDC mode is enabled and the identity provider can issue a tenant claim containing path separators or '..', this accepts that value unchanged as the 'Principal.tenant_id'. The secur...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR322:PRRT_kwDOTH_vCM6TY-OL

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/secured_service.py:42`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552499
- Claim: **P2 Badge Avoid revalidating assertions with the default clock** When an OIDC deployment configures 'clock_skew_seconds' above the default 30 seconds, 'verify()' first validates the token with that configured skew, but this call to 'pri...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR322:PRRT_kwDOTH_vCM6TY-OR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/oidc.py:97`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/322#discussion_r3641552505
- Claim: **P2 Badge Convert missing time claims into auth failures** When a correctly signed OIDC JWT omits 'iat' or 'exp' or provides a non-integer object for either claim, these 'int(payload.get(...))' calls raise 'TypeError' outside any OIDC e...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR323:PRRT_kwDOTH_vCM6TZIq9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/deploy/kubernetes.yaml:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613886
- Claim: **P1 Badge Preserve image CMD arguments in the manifest** Per the Kubernetes docs, defining 'args' without 'command' keeps the entrypoint but uses “your new arguments”, so this manifest replaces the Dockerfile CMD that sets '--security-d...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR323:PRRT_kwDOTH_vCM6TZIrB

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/distributed.py:109`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613891
- Claim: **P1 Badge Make evidence inserts idempotent under contention** When two replicas receive the same evidence record before either transaction commits, both 'SELECT ... FOR UPDATE' queries can see no row because PostgreSQL cannot lock a mis...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR323:PRRT_kwDOTH_vCM6TZIrD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/distributed.py:181`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/323#discussion_r3641613892
- Claim: **P2 Badge Convert probe exceptions into failed checks** When a real metadata, object-storage, or counter probe raises on a timeout/auth failure, this eager construction aborts before returning a readiness payload, so callers do not get ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR324:PRRT_kwDOTH_vCM6TZUi3

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_universality_remainder_theorem.py:107`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/324#discussion_r3641683971
- Claim: **P2 Badge Validate the completed-work ledger exactly** When a frozen completed-work item is removed or renamed but the list is padded back to 15 entries, 'validate_registry' still returns no errors because this check only enforces list ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR333:PRRT_kwDOTH_vCM6TbDy4

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/architecture/repository-convergence-2026-07-23.md:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/333#discussion_r3642340123
- Claim: **P2 Badge Use charter-defined artifact statuses** This new audit is introduced with 'Status: execution baseline', and the companion convergence documents use similarly descriptive statuses ('canonical convergence guidance', 'active exec...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR335:PRRT_kwDOTH_vCM6TbKCT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/adjudicate.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/335#discussion_r3642378612
- Claim: **P1 Badge Don't count contradictory edges as authorization support** When a producer records a required node's edge to the root as 'contradicts' (or another non-supporting relation), this comprehension still adds the source to 'incoming...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR335:PRRT_kwDOTH_vCM6TbKCX

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/model.py:124`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/335#discussion_r3642378614
- Claim: **P1 Badge Reject cyclic dependency graphs before adjudication** For packages with two-node or longer cycles, such as 'auth -> root' and 'root -> auth', this validator accepts the graph because it only rejects self-dependencies; adjudica...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR336:PRRT_kwDOTH_vCM6TbQvA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/evidence.py:74`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/336#discussion_r3642422084
- Claim: **P2 Badge Verify hashed evidence sources before accepting bundles** When a generated bundle is verified after the referenced regression suite is edited or removed, this still returns true as long as the report file is unchanged, because...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR337:PRRT_kwDOTH_vCM6TbmOr

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-decision-integrity/src/far_decision_integrity/swe_agent.py:25`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/337#discussion_r3642550453
- Claim: **P2 Badge Preserve observation records from SWE-agent trajectories** When the input is a current SWE-agent trajectory that stores tool output as '{"message_type":"observation","content":...}' (as shown in the official trajectory docs: h...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR340:PRRT_kwDOTH_vCM6Tb8P_

- Disposition: `unresolved`
- Confidence: `high`
- Location: `research/external-validation/trace-candidate-002/protocol.json:4`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/340#discussion_r3642681741
- Claim: **P2 Badge Add a charter status to the frozen protocol** This 'status' records the execution phase, but the new protocol still lacks one of the charter artifact statuses (Accepted, Research, Provisional, Archive, or Unknown). Because Can...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR344:PRRT_kwDOTH_vCM6TcTFp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/1-0-golden-clean-install.yml:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/344#discussion_r3642814795
- Claim: **P2 Badge Run the golden tests against the installed wheel** This step uses the checkout's default 'python', and the package tests prepend 'commercial/far-decision-integrity/src' to 'sys.path', so the behavioral tests exercise the worki...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR344:PRRT_kwDOTH_vCM6TcTFr

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/releases/1.0.0-draft.md:7`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/344#discussion_r3642814797
- Claim: **P2 Badge Attach provenance to the cumulative release narrative** This new draft immediately summarizes a long 0.4.0→1.0.0 development path and the following sections list research, governance, and validation claims, but the artifact co...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR347:PRRT_kwDOTH_vCM6TcnkK

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:197`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/347#discussion_r3642936015
- Claim: **P2 Badge Escape uploaded values before rendering findings** When a user analyzes an uploaded trace whose 'action' contains HTML, that value is copied into finding descriptions and then interpolated into 'innerHTML' here, so opening the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR347:PRRT_kwDOTH_vCM6TcnkO

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:27`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/347#discussion_r3642936021
- Claim: **P2 Badge Validate event objects before parsing fields** If an uploaded JSON file has an 'events' array containing any non-object value, '_parse' passes it into '_event' and this '.get' call raises 'AttributeError', which is not caught ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR348:PRRT_kwDOTH_vCM6Tc-2A

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:210`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/348#discussion_r3643074604
- Claim: **P2 Badge Download the analyzed artifact instead of the sample** When a user verifies custom packages through 'runUpload()', the rendered status/changes come from '/api/analyze', but this CTA always requests '/api/example/report'. In th...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR348:PRRT_kwDOTH_vCM6Tc-2B

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:210`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/348#discussion_r3643074607
- Claim: **P2 Badge Render uploaded evidence in the comparison panel** For custom uploads, 'runUpload()' updates only the verdict card from '/api/analyze', while this side-by-side “Execution comparison” remains the hard-coded refund sequence. Any...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR350:PRRT_kwDOTH_vCM6Tdsan

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:130`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/350#discussion_r3643345247
- Claim: **P2 Badge Keep upload summaries evidence-bound** When '/api/analyze' is used for any package other than the bundled refund sample—e.g. a justified package or an unsupported non-refund decision—'_present()' still returns these refund/app...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR350:PRRT_kwDOTH_vCM6Tdsas

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:251`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/350#discussion_r3643345252
- Claim: **P2 Badge Render the actual returned status** When the upload flow analyzes a package whose returned 'status' is 'justified', 'unverifiable', or 'underdetermined', this hard-coded label remains 'Result: unsupported' because 'render()' o...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR351:PRRT_kwDOTH_vCM6TeaVq

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:130`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/351#discussion_r3643608853
- Claim: **P2 Badge Keep upload summaries evidence-bound** Because '_present()' also builds the response for '/api/analyze', these hard-coded refund-specific fields are returned after users upload arbitrary FAR packages; an unsupported access-con...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR353:PRRT_kwDOTH_vCM6TfYVy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:297`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/353#discussion_r3643957042
- Claim: **P2 Badge Wrap parser errors for supported uploads** When either upload is a malformed newly supported format, 'parse_package_file()' can now raise parser-specific exceptions such as 'yaml.YAMLError', XML parse errors, or zip/package er...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR353:PRRT_kwDOTH_vCM6TfYV2

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/formats.py:129`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/353#discussion_r3643957046
- Claim: **P2 Badge Reject XML packages that omit trace completeness** For an XML upload that omits 'trace_completeness', this line silently inserts '0' before the package reaches 'DecisionPackage.from_dict'. The same missing required field is re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR354:PRRT_kwDOTH_vCM6Tfu7K

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/app.py:170`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/354#discussion_r3644086806
- Claim: **P2 Badge Don't pass releases that remove recorded support** When a candidate removes a baseline decision-root dependency that is not in 'authorization_requirements', '_present()' still emits a high-severity 'decision_dependency_removed...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR355:PRRT_kwDOTH_vCM6Tm8c9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-demo/src/far_demo/validation_app.py:123`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/355#discussion_r3646752560
- Claim: **P1 Badge Configure feedback logging before returning recorded** When the Render deployment starts 'uvicorn far_demo.validation_app:app', this custom 'far.validation' logger is never configured in this repo; under Python/uvicorn default...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR356:PRRT_kwDOTH_vCM6Tm9zN

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:76`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/356#discussion_r3646760091
- Claim: **P1 Badge Reject pre-freeze outcome fields** When a pre-freeze manifest gains an outcome field, for example after execution but before the primary hash freeze someone adds '{"leaked_outcome": {"reward": 1, "grader_output": "..."}}', thi...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR357:PRRT_kwDOTH_vCM6Tnjoh

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/agent-config.yaml:10`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/357#discussion_r3646978999
- Claim: **P1 Badge Make the frozen SWE-agent config loadable** When the four runs follow 'run_comparison.py'’s instruction to use this file, SWE-agent v1.0 will reject this old-style 'agent.config_file' entry before any run starts: the 1.0 migra...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR357:PRRT_kwDOTH_vCM6Tnjol

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validate_manifest.py:68`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/357#discussion_r3646979006
- Claim: **P2 Badge Validate every frozen model parameter** With the validator only checking 'temperature' and 'reasoning_effort', later edits can change or remove frozen fields like 'top_p', 'per_instance_cost_limit_usd', or 'total_cost_limit_us...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR359:PRRT_kwDOTH_vCM6Too8m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:68`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/359#discussion_r3647386256
- Claim: **P2 Badge Parse the verbose manifest digest** When the fallback is used for a normal single-image manifest, Docker's verbose output exposes the registry digest as a top-level 'Digest' field (see the Docker CLI docs' 'docker manifest ins...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR360:PRRT_kwDOTH_vCM6To5d1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/prepare_environment.py:73`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482119
- Claim: **P1 Badge Use the SWE-bench install_repo_script property** In the pinned SWE-bench harness, 'TestSpec' exposes the repository setup script as 'install_repo_script' (the image builder writes that into 'setup_repo.sh'); there is no 'setup...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR360:PRRT_kwDOTH_vCM6To5d6

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/run_comparison.py:40`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482128
- Claim: **P1 Badge Verify the local image before accepting the lock** For 'preflight' or 'plan' on a fresh GitHub-hosted runner, comparing the committed JSON 'local_image_id' to the manifest only proves the lock is self-consistent; the Docker da...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR360:PRRT_kwDOTH_vCM6To5d8

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-swe-agent-execution.yml:11`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/360#discussion_r3647482130
- Claim: **P2 Badge Update the documented stage name with the workflow rename** After this dispatch option is renamed, the setup guide still describes the available stages as 'resolve-image', 'preflight', and 'plan' and tells operators to run 're...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR367:PRRT_kwDOTH_vCM6TtX1k

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:183`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152943
- Claim: **P1 Badge Run trajectories through the registered FAR adapter** The comparison reduces each trajectory to scalar, mapping, and list counts, so even a normal completed run produces no decision dependencies, authorization requirements, un...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR367:PRRT_kwDOTH_vCM6TtX1m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:194`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152946
- Claim: **P1 Badge Block primary regeneration after outcome reveal** If an operator dispatches 'freeze-primary' after 'reveal-outcomes', the workflow restores the latest postprocess artifact—including its 'post-freeze-reveal/outcome-reveal.json'...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR367:PRRT_kwDOTH_vCM6TtX1o

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/evidence_pipeline.py:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152948
- Claim: **P1 Badge Require the complete primary artifact set** When 'primary-freeze.json' is tampered with or restored from an incompatible artifact, a manifest containing 'artifact_count: 0', 'artifacts: []', and the hash of that empty list pas...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR367:PRRT_kwDOTH_vCM6TtX1q

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/validator-assurance.yml:111`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/367#discussion_r3649152950
- Claim: **P1 Badge Retain independent provenance for the cache bundle** The checksum and the cache bundle are generated by the same producer and uploaded in the same artifact, so a substituted bundle can be accompanied by a matching substituted ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR369:PRRT_kwDOTH_vCM6Ttjrd

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/far_mechanization/compare_adjudication.py:357`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223443
- Claim: **P1 Badge Bind findings to referenced package contents** When 'adjudicate' receives a comparison from an untrusted or corrupted producer, these embedded claims are normalized but never checked against the packages identified by 'left_re...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR369:PRRT_kwDOTH_vCM6Ttjrh

- Disposition: `unresolved`
- Confidence: `high`
- Location: `mechanization/far_mechanization/compare_adjudication.py:160`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223447
- Claim: **P2 Badge Reject non-finite metadata values** When package or adjudication metadata contains 'NaN', 'Infinity', or '-Infinity', Python's permissive 'json.loads' produces a 'float' and this check accepts it. 'canonical_json_bytes' then e...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR369:PRRT_kwDOTH_vCM6Ttjrj

- Disposition: `unresolved`
- Confidence: `high`
- Location: `schemas/far-evidence-comparison-v1.schema.json:26`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/369#discussion_r3649223449
- Claim: **P2 Badge Validate embedded claims in the comparison schema** When consumers validate comparison artifacts using the published JSON Schema rather than the Python CLI, 'left' and 'right' accept any object, including '{}' or arbitrary fie...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR371:PRRT_kwDOTH_vCM6TuK-l

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_repository_truth.py:36`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/371#discussion_r3649454375
- Claim: **P1 Badge Make the checker enforce the manifest authorities** When an authority or mirror entry in 'repository-truth-authority-v1.json' changes, this checker validates only the schema string and continues checking the three hard-coded p...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR371:PRRT_kwDOTH_vCM6TuK-m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/governance/repository-truth-revalidation-scope.md:28`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/371#discussion_r3649454378
- Claim: **P2 Badge Complete the authority inventory before resolving the audit** These required categories are absent from both the machine-readable manifest and the audit's authoritative inventory, which cover only package/CLI versions, README ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR373:PRRT_kwDOTH_vCM6TuR8N

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/releases/project-far-v1.0.0.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495818
- Claim: **P1 Badge Assign the release record an allowed status** Assign this newly introduced canonical artifact exactly one of the charter’s permitted statuses—Accepted, Research, Provisional, Archive, or Unknown. The file currently declares it...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR373:PRRT_kwDOTH_vCM6TuR8O

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_repository_truth.py:66`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495821
- Claim: **P2 Badge Validate the README release target** Validate the anchor target as well as its displayed label. If the README link is changed back to '/releases/tag/v0.4.0' while its text remains 'v1.0.0', this phrase still matches and the se...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR373:PRRT_kwDOTH_vCM6TuR8P

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_repository_truth.py:95`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/373#discussion_r3649495822
- Claim: **P2 Badge Require the authoritative repository in the record URL** Require the complete canonical GitHub release URL here. The current suffix-only test also accepts a link on another domain or in a fork, such as 'https://github.com/othe...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR379:PRRT_kwDOTH_vCM6TxgEB

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/sitecustomize.py:30`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/379#discussion_r3650665592
- Claim: **P1 Badge Import the pathlib constructors from reachable code** In the checked 'far-swe-agent-execution.yml' workflow, Python 3.12 runs the regression suite and controller with this directory merely as the working directory; Python does...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR380:PRRT_kwDOTH_vCM6Txs_H

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/rehearse_execute_boundary.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/380#discussion_r3650738324
- Claim: **P1 Badge Exercise SWE-agent before declaring the launch boundary reached** In the added 'full-no-model-execution-rehearsal' job, whenever parsing succeeds but SWE-agent's runtime initialization would fail, this wrapper still reports su...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR381:PRRT_kwDOTH_vCM6TyRNx

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:196`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944620
- Claim: **P1 Badge Revalidate restored completions before selecting the next run** When an execution artifact was produced by the old controller—including the misclassified 'v1.0.0-r1' that motivated this change—its run remains 'complete' even i...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR381:PRRT_kwDOTH_vCM6TyRNy

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:16`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944621
- Claim: **P1 Badge Block progression when a run fails terminally** When the new classifier emits 'failed_terminal' for an early slot, adding it only to 'ALLOWED_STATES' makes the state loadable but leaves it absent from 'base.RESUMABLE_STATES' a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR381:PRRT_kwDOTH_vCM6TyRN1

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:190`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/381#discussion_r3650944624
- Claim: **P2 Badge Do not let transient provider logs override validated success** When SWE-agent or LiteLLM logs a transient timeout, 429, or 5xx during one of the configured provider retries and then successfully submits a non-empty patch, the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR384:PRRT_kwDOTH_vCM6TynPj

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:285`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069591
- Claim: **P1 Badge Reconcile before enforcing sequential ordering** When restoring the exact bad state produced by the previous controller—a 'failed_terminal' slot followed by a 'complete' slot—'base.load_state()' rejects the matrix for frozen s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR384:PRRT_kwDOTH_vCM6TynPo

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:222`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069597
- Claim: **P1 Badge Inspect every prediction file that claims the target** If SWE-agent emits the canonical '.pred' plus another '.pred' whose payload also declares the target instance, this filter ignores the second file solely because its filen...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR384:PRRT_kwDOTH_vCM6TynPq

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller.py:105`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651069599
- Claim: **P2 Badge Validate the copied trajectory during restoration** When a restored artifact is missing 'trajectories/' or that file no longer matches 'run["trajectory_sha256"]', this required-evidence set still allows the run to remain 'comp...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR384:PRRT_kwDOTH_vCM6Ty6_k

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/test_execution_outcome_base.py:402`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651180908
- Claim: **P1 Badge Align the inherited regression with sequence hardening** The required test command in both '.github/workflows/far-swe-agent-execution.yml' and '.github/workflows/far-swebench-environment-smoke.yml' now fails here: 'make_run(.....
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR384:PRRT_kwDOTH_vCM6Ty6_m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:239`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/384#discussion_r3651180910
- Claim: **P1 Badge Reject malformed noncanonical target predictions** When a noncanonical '.pred' explicitly names the frozen task but omits 'model_patch'—for example '{"instance_id": "", "unexpected": ...}'—'_extract_prediction' returns 'found=...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR386:PRRT_kwDOTH_vCM6TzCgi

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:107`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/386#discussion_r3651223164
- Claim: **P1 Badge Reject malformed keyed target predictions** When a noncanonical '.pred' or 'preds.json' uses the already-supported '{task_id: prediction}' form, recursion reaches a value without 'instance_id', so this guard never fires. For e...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR389:PRRT_kwDOTH_vCM6TzgU-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/execution_outcome.py:324`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388775
- Claim: **P1 Badge Preserve retry classification when output is absent** When SWE-agent reports a genuine 429/5xx before creating 'sweagent-output', this early return marks the attempt 'failed_terminal' before the provider-marker logic can class...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR389:PRRT_kwDOTH_vCM6TzgVA

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:287`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388778
- Claim: **P1 Badge Roll back artifacts moved before an interrupted return** If 'shutil.move' moves an artifact and then raises—for example, a 'KeyboardInterrupt' after the rename/copy but before returning—or an interrupt lands between these two ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR389:PRRT_kwDOTH_vCM6TzgVD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execute_controller_core.py:272`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/389#discussion_r3651388783
- Claim: **P2 Badge Reject broken symlinks before archiving** When a prior attempt leaves a broken symlink under an artifact name such as 'instance.json', 'stdout.log', or 'sweagent-output', the preceding '.exists()' filter omits it because that ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR391:PRRT_kwDOTH_vCM6T0ZLE

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:13`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/391#discussion_r3651726623
- Claim: **P1 Badge Require model context for NOT_FOUND signals** When an unsuccessful agent or tool action emits a generic JSON error such as '{"status":"NOT_FOUND"}'—including alongside a genuine HTTP 503—this pattern matches without any model ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR391:PRRT_kwDOTH_vCM6T0ZLF

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1/validated_execution_provider_contract.py:35`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/391#discussion_r3651726625
- Claim: **P1 Badge Keep standalone provider timeout errors retryable** When a provider reports an actual timeout in forms such as 'Timeout while contacting Gemini' or 'provider request exceeded timeout', the delegate detects the bare 'timeout' m...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR392:PRRT_kwDOTH_vCM6T0n2T

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/manifest.json:139`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812789
- Claim: **P1 Badge Add the required top-level case ID** Every workflow stage stops in the initial 'python case_tools.py validate' step because 'validate_manifest()' requires 'm.get("case_id") == CASE_ID', while this manifest has no top-level 'ca...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR392:PRRT_kwDOTH_vCM6T0n2V

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/shared-implementation-lock.json:6`
- GitHub resolved/outdated: `False` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812791
- Claim: **P1 Badge Correct the locked controller blob hash** After the manifest identity is corrected, every validation still fails in 'verify_shared_implementation()': the 'validated_execute_controller.py' blob in the referenced legacy case is ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR392:PRRT_kwDOTH_vCM6T0n2W

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:178`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812793
- Claim: **P1 Badge Extract restored artifacts at the case directory** On the second and subsequent 'execute' dispatches, the uploaded artifact contains both 'execution-output/...' and 'access-freeze/...' relative to their common case-directory r...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR392:PRRT_kwDOTH_vCM6T0n2X

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/case_tools.py:216`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/392#discussion_r3651812794
- Claim: **P2 Badge Record connection-level access-probe failures** When the provider request fails before receiving an HTTP response—for example on DNS, TLS, connection-refusal, or timeout errors—'urlopen()' raises 'urllib.error.URLError', not '...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR393:PRRT_kwDOTH_vCM6T2FXp

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:112`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/393#discussion_r3652336929
- Claim: **P1 Badge Validate the decoded HTTP error shape before accessing it** When an HTTP error contains valid JSON whose root is not an object, or whose 'error' member is 'null', a string, or a list, this expression raises 'AttributeError' ei...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR393:PRRT_kwDOTH_vCM6T2FXq

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/access_probe_v2.py:108`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/393#discussion_r3652336930
- Claim: **P1 Badge Record transport failures that occur while reading the body** When the provider sends response headers but stalls or disconnects while the body is being read, 'response.read()' can raise exceptions such as 'TimeoutError' or 'h...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR395:PRRT_kwDOTH_vCM6T2PsZ

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/EXECUTION-STATUS.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/395#discussion_r3652395862
- Claim: **P1 Badge Preserve the failed access-probe record** When this freeze is merged, the replacement status records only the successful probe and removes the repository's sole account of attempt 1, including its unsuccessful result, 16-token...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR396:PRRT_kwDOTH_vCM6T2ibE

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:191`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/396#discussion_r3652500679
- Claim: **P1 Badge Do not let failed restores supersede the last checkpoint** When this new artifact validation rejects a restore, the 'if: always()' upload at the end of this workflow still publishes the freshly generated, plan-only 'execution-...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR397:PRRT_kwDOTH_vCM6T4r2a

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/primary-freeze/source-artifact-lock.json:379`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269356
- Claim: **P1 Badge Preserve the source artifact beyond its expiry** The only copy of the 73-file execution source is GitHub artifact '8635674915', and this lock records that it expires on 2026-08-25. Both 'verify-source' and 'evaluate-reveal' do...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR397:PRRT_kwDOTH_vCM6T4r2b

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269359
- Claim: **P1 Badge Bind the reveal to the currently verified freeze** When 'post-freeze-reveal' was generated against an older primary freeze, this verifier accepts it because it checks only the reveal schema and never compares 'primary_freeze_s...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR397:PRRT_kwDOTH_vCM6T4r2c

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/evidence_pipeline_v2.py:466`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/397#discussion_r3653269360
- Claim: **P1 Badge Recompute the final report from the revealed outcomes** When the derived JSON or Markdown report is accidentally edited, 'verify_reveal' checks only that the final JSON points to the reveal's byte hash; it never verifies that ...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR398:PRRT_kwDOTH_vCM6T5D8v

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:52`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/398#discussion_r3653404525
- Claim: **P1 Badge Preserve the evaluation evidence behind these hashes** After the workflow artifact's 90-day retention period expires, the committed 'test_output_sha256' and 'run_instance_log_sha256' values cannot be resolved back to the evide...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR398:PRRT_kwDOTH_vCM6T5D8w

- Disposition: `unresolved`
- Confidence: `high`
- Location: `commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2/post-freeze-reveal/outcome-reveal.json:194`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/398#discussion_r3653404528
- Claim: **P1 Badge Declare a status for each new reveal artifact** This new outcome artifact, like the three companion files added by the commit, does not declare whether its status is Accepted, Research, Provisional, Archive, or Unknown. That l...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR399:PRRT_kwDOTH_vCM6T5NRD

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-swe-agent-execution-v2.yml:62`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/399#discussion_r3653456877
- Claim: **P1 Badge Enforce the execution freeze independently of the selected ref** When 'workflow_dispatch' selects a branch or tag where 'bundle-sha256.json' is absent, this guard inspects that checked-out ref and passes; unlike 'access-probe'...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR399:PRRT_kwDOTH_vCM6T5NRG

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/far-swe-agent-v2-postprocess.yml:64`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/399#discussion_r3653456881
- Claim: **P2 Badge Refuse reveal evaluation after the final bundle exists** On the current completed 'main', a dispatch with 'stage=evaluate-reveal' and the confirmation phrase passes this new existence check and continues into the still-enabled...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR400:PRRT_kwDOTH_vCM6T5R2m

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/theory-correction-audit-2026-07-26.md:3`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/400#discussion_r3653482542
- Claim: **P1 Badge Keep correction artifacts provisional until replicated** In the reviewed tree, the only new provenance is this single audit and its decision-log entry; no replication record exists, yet this artifact and the newly introduced a...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR400:PRRT_kwDOTH_vCM6T5R2n

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_semantic_consistency.py:54`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/400#discussion_r3653482543
- Claim: **P1 Badge Scan all active artifacts before reporting semantic consistency** When 'semantic-check' is run on this commit, it reports PASS even though active non-archive artifacts outside this three-file allowlist still use terminology th...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR401:PRRT_kwDOTH_vCM6T5eUS

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_swe_agent_v2_forensics.py:119`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553313
- Claim: **P1 Badge Validate the evidence inventory against its source locks** The validator never loads 'evidence-inventory.json', so deleting an artifact, changing a hash, or mislabeling external evidence still produces the advertised PASS. Thi...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR401:PRRT_kwDOTH_vCM6T5eUU

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_swe_agent_v2_forensics.py:112`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553317
- Claim: **P1 Badge Reconcile timeline facts with the frozen run records** If a timeline's outcome, call budget, termination reason, patch result, or grader result is changed, validation still passes because these checks cover only identity, stag...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR401:PRRT_kwDOTH_vCM6T5eUV

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `docs/audits/swe-agent-v2-forensics/failure-taxonomy.json:84`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/401#discussion_r3653553318
- Claim: **P2 Badge Keep patch-design failure classified as unknown** The reveal proves only that each applied patch did not pass the target; it cannot distinguish a design error from implementation, environment, or oracle causes without the unav...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR402:PRRT_kwDOTH_vCM6T53x9

- Disposition: `unresolved`
- Confidence: `high`
- Location: `docs/audits/merged-pr-review-audit/retrieval-manifest.json:21`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698271
- Claim: **P1 Badge Include standard merge commits in the inventory** At the audited SHA, 'git log --first-parent' contains 138 additional commits with subjects such as 'Merge pull request #395 from ...'; these are explicit, locally available mer...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR402:PRRT_kwDOTH_vCM6T53x-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_merged_pr_review_inventory.py:104`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698273
- Claim: **P1 Badge Reject incomplete per-PR manifests** When 'counts_per_pr' is empty, omits an inventoried PR, or reports endpoint counts that disagree with the raw records, this loop merely finds no failed status and validation can still retur...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR402:PRRT_kwDOTH_vCM6T53x_

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/check_merged_pr_review_inventory.py:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698274
- Claim: **P2 Badge Reject repeated source and thread IDs** If pagination replay or overlapping retrieval produces the same record twice, the equality condition allows both copies because only conflicting duplicates are rejected. Incrementing the...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR402:PRRT_kwDOTH_vCM6T53yB

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tests/test_merged_pr_review_inventory.py:46`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/402#discussion_r3653698276
- Claim: **P2 Badge Validate the checked-in inventory in canonical tests** The canonical test path discovers this test, but every assertion validates 'self.root', which is a synthetic temporary directory; repository-wide inspection of the validat...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR403:PRRT_kwDOTH_vCM6T6IS4

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_proof_object.py:207`
- GitHub resolved/outdated: `True` / `True`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792971
- Claim: **P1 Badge Do not weaken final theorem-conclusion alignment** When a proof-object conclusion is much longer than the registered theorem statement, using the shorter vocabulary as the denominator allows the conclusion to add arbitrary uns...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.
  - GitHub records the diff location as outdated.

### PR403:PRRT_kwDOTH_vCM6T6IS5

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_orphaned_docs.py:72`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792972
- Claim: **P2 Badge Preserve the documented orphan-ok exemption** When an intentionally standalone document contains the documented 'orphan-ok' marker, it is now included in 'all_docs' and therefore fails '--strict' unless linked. The repository'...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR403:PRRT_kwDOTH_vCM6T6IS6

- Disposition: `uncertain_manual_review_required`
- Confidence: `high`
- Location: `tools/check_proof_object.py:117`
- GitHub resolved/outdated: `True` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/403#discussion_r3653792973
- Claim: **P2 Badge Count distinct metadata sources before suppressing warnings** When two inputs inherit the same lemma, theorem, or axiom through separate lineage paths, 'source_items' returns the same source tuple twice, so 'len(sources) != 1'...
- Rationale: Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.
- Evidence:
  - GitHub review-thread metadata records is_resolved=true.

### PR404:PRRT_kwDOTH_vCM6T6taR

- Disposition: `unresolved`
- Confidence: `high`
- Location: `tools/export_merged_pr_review_inventory.py:394`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007699
- Claim: **P1 Badge Tie the live API snapshot to the audited SHA** When another PR merges before or during an export, this live 'state=closed' enumeration can include or omit repository state newer than '--audited-sha', yet the manifest still lab...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR404:PRRT_kwDOTH_vCM6T6taT

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:29`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007701
- Claim: **P2 Badge Pin manual inventory runs to main** For a 'workflow_dispatch' run launched against a non-main ref, 'actions/checkout' checks out that selected ref because no 'ref' is specified. The resulting 'audit/authenticated-review-data-*...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR404:PRRT_kwDOTH_vCM6T6taU

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:78`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/404#discussion_r3654007702
- Claim: **P2 Badge Give reruns a new export branch** When a failed or incomplete workflow is re-run, GitHub's 'run_id' does not change (GitHub context documentation), so this reuses the branch created by the first attempt. Because the exporter e...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

### PR405:PRRT_kwDOTH_vCM6T7G3-

- Disposition: `unresolved`
- Confidence: `high`
- Location: `.github/workflows/export-merged-pr-review-inventory.yml:67`
- GitHub resolved/outdated: `False` / `False`
- Review URL: https://github.com/notfoundout/Project-FAR/pull/405#discussion_r3654155071
- Claim: **P2 Badge Report the actual number of export attempts** When all four attempts return '2', this unconditional increment changes 'attempt' from 4 to 5 before the loop exits, so the fail-closed step reports that five attempts ran even tho...
- Rationale: The frozen evidence directly establishes that the thread remained unresolved at export time.
- Evidence:
  - GitHub review-thread metadata records is_resolved=false.

