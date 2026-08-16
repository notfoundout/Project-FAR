# Versioned successor procedures

Separately versioned, executed **outside** frozen $\mathfrak{E}_0$ and never counted as an
in-order $\mathfrak{E}_0$ result. Each was preregistered in full before execution and is
outcome-independent: nothing in the procedure branches on what it finds.

---

## `E0-c0-only-v1` — calibration-fragment computation

**Motivation.** $\mathfrak{E}_{0a}$'s staging rule (`TR-11:4956`) requires
$\mathcal{K}_0$, $U_0$ and $\Pi_0$ to be hashed before $W^\ast$ begins. $\mathfrak{E}_{0b}$ and
$\mathfrak{E}_{0c}$ are permanently blocked in this environment (no reachable scholarly host,
so K4 verbatim quotation is impossible). Under the frozen rule, $W^\ast$ therefore never
begins and $\mathfrak{E}_0$ yields no content result at all.

However, exactly one fragment is **independent of $U_0$**: the calibration fragment
$c_0=(\{S1,S2\},L_\to)$. Its language $L_\to$ is dialogue-constructed and frozen in
$\mathfrak{E}_{0a}$; it contains no registry item. Both its targets' native structures are
fully determined by $\mathfrak{E}_{0a}$, and its frame was fixed at $\Gamma_{c_0}=\varnothing$
in $\mathfrak{E}_{0a}$ (`TR-11:4179`).

**Procedure, fixed before execution.**

1. Exhibit a joint certificate $\mathbf{J}$ for $c_0$ at grammar $G_1$, naming the semantic
   resolution profile for each target and proving $E$-factorization and $O$-respect.
2. Report $\mathrm{Status}(c_0)\in\{$JOINT-YES, JOINT-NO, JOINT-OPEN$\}$. Do not claim
   JOINT-COMPLETE.
3. Search for a sentence in $\mathcal{T}_{c_0,\mathbf{J}}\setminus\mathrm{Cn}(\varnothing)$ and,
   independently, attempt a proof that none exists. Whichever succeeds first closes the
   fragment; if both succeed, halt for CERTIFICATE INCONSISTENCY audit.
4. Report the result **with** its grammar index, joint-profile index, and corpus-profile index.
5. Attempt the corresponding computation under every S1 corpus profile identified; where a
   profile is not resolvable within budget, return UNRESOLVED for that profile.
6. Return novelty as UNRESOLVED unless $\Pi_0$ is exactly fixed and its translation certified.

**Prohibitions.** Do not extend to any fragment containing a $U_0$ item. Do not modify any
frozen object. Do not treat the outcome as satisfying $\mathfrak{E}_0$'s stop conditions.

**Executed.** Results in `PROOFS.md` T4. Outcome: JOINT-YES; A2 falsified at
$(\mathbf{J}_0, G_1, K_{1,\mathrm{L\&M}})$ by $\varphi_{\mathrm{irr}}=\forall x\,\neg(x\to x)$;
UNRESOLVED under a list-with-exchange S1 corpus profile; novelty UNRESOLVED.

---

## `E0-supplied-v1` — SOURCE-SUPPLIED primary-document procedure

**Motivation.** Primary documents were supplied directly as local files. SR-B2 v2 governs
*retrieval*; it says nothing about documents that arrive without retrieval. TSI-v1 governs
*inspection* and is fully executable on a local file. A supplied document that is already in a
frozen near-match set is therefore ordinary frozen execution; a supplied document that is not
requires a separately versioned procedure so that the frozen candidate set is not retrofitted.

**Procedure, fixed before any supplied document was opened.**

1. Hash every supplied file. Verify bibliographic identity **from the document's own front
   matter or embedded metadata**, never from recall or from the filename.
2. Determine membership in the frozen near-match set $N_i$ for the target concerned.
   - **In $N_i$** ⇒ inspect under the **original** frozen procedure. The verdict is an
     $\mathfrak{E}_0$ verdict.
   - **Not in $N_i$** ⇒ inspect under this successor procedure. The verdict is an
     `E0-supplied-v1` verdict and is reported **separately** from the original
     $\mathfrak{E}_0$ verdict, which is left unchanged.
3. Apply TSI-v1 unchanged, with the target's already-fixed search terms.
4. Apply the already-frozen adjudication order K-P1 → DI1–DI6 (with SRF-v1, CDE-v1) →
   target-specific certificate (FDI-v1 / MFDI-v1) → K-P2 → K-P4. **No criterion is altered,
   relaxed, or added.**
5. Extract K4 records under U-a, U-b, U-c, U-e unchanged.
6. Where the two procedures disagree for one target, record the difference as
   **source-supply / search-provider sensitivity** and attribute it to the retrieval design,
   never to the target or to the literature.
7. Preserve the evidence cutoff. A supplied document already eligible at the cutoff is
   admissible; delivery date is not publication date.

**Outcome-independence.** Steps 1–7 branch on *membership in $N_i$* and on *the frozen
criteria*, never on what a document turns out to say. The procedure was fixed before either
document was opened and was applied unchanged to both, including where it produced the verdict
least favourable to the programme's own registered hypothesis (DF-04-H).

**Executed.** `SS-CC92` fell in $N_7$ ⇒ original procedure ⇒ **S7 READY** as an
$\mathfrak{E}_0$ verdict. `SS-GP94` fell outside $N_6$ ⇒ successor procedure ⇒ **S6 READY**
under `E0-supplied-v1`, with S6 remaining **OPEN** under original $\mathfrak{E}_0$, and the
difference recorded as **DF-07**.

---

## Procedures considered and **rejected**

### Rejected: `TSI-v2-snippet` — replace TSI-v1 with a snippet-level evidentiary standard

Rejected. GPT Turn 26 §4 permits replacing an inexecutable *retrieval* procedure only because
(i) it was a post-freeze operational completion procedure, (ii) its infeasibility surfaced
before it produced any terminal verdict, and (iii) the replacement is uniform and not chosen
for its consequences. Conditions (i)–(iii) could arguably be met here. The proposal is
nevertheless rejected because the replacement would **weaken the evidentiary standard in the
exact way TSI-v1 was written to prevent**: GPT Turn 31 adopted TSI-v1 precisely so that a
negative result could not be "manufactured by search-engine summaries rather than the sources
themselves" (`TR-31:228`), and made EXACT/DIRECT contingent on source inspection
(`TR-31:183`). Replacing it with snippet adjudication would let *both* verdicts be produced by
the very mechanism the rule excludes. Blocked-environment convenience is not a licence.

### Rejected: bibliography-following to reach an accessible mirror

Rejected. GPT Turn 30 fixed documents-only candidacy and forbade recursive bibliography
retrieval in $\mathfrak{E}_0$ (`TR-11:10966`). Host-substitution search to find a reachable
copy of a blocked document is a new retrieval channel, and here it would be adopted after
observing which specific documents are decisive — outcome-informed procedure expansion, the
error rejected as option (iii) in Turn 30.

### Rejected: asserting source content from training recall

Rejected on the shell's own terms: *"I will not assign READY from training recall. K-P5
requires retrieved source evidence, and 'I am confident Fikes & Nilsson defines STRIPS' is not
a certificate"* (`TR-11:6898`). No source content anywhere in these artifacts is asserted from
recall, and no passage is quoted as verbatim unless it was returned by an executed invocation —
in which case it is marked *attribution unverified* if the host could not be inspected.
