# CLAUDE TURN 31  
  
Ruling accepted. **Top-level result = candidate; citation inside a result = logged lead only; no recursive bibliography retrieval in $\mathfrak{E}_0$.** RD-01 recorded, with $L_1 = 3$ so far (Uniform Proofs 1991; Miller & Saurin game semantics; Miller monograph). $N_1$ correction accepted as bookkeeping.  
  
I accept the reasoning behind rejecting (iii) — the proposal was conditioned on observed evidence even though its motivation ran against my interest, and "better recall does not override preregistered stopping discipline" is the correct principle. Recorded also: **SOURCE-FAIL under v2 means failure under this bounded retrieval design, not exhaustion of the citation graph.**  
  
Continuing: member 1 Q8, then member 2.  
  
## Member 1 complete — Q8  
  
`"Miller" "LK sequent calculus" "multiset of open sequents"` — 9 results, 4 new candidates: Miller's LKF lecture notes; *Focusing Gentzen's Sequent Calculus* (talk); Chaudhuri, Hetzl & Miller, *A Systematic Approach to Canonicity in the Classical Sequent Calculus* (LKN/LKNF); Miller, *Focused Sequent Calculus Proof Systems* (2018 talk). **All INELIGIBLE** — every one is a focused, polarized, or multi-focused system.  
  
**Two decisive statements surfaced, both from the field's principal author.**  
  
First, on DI3 at the base level, in Miller's own words: Gentzen **used lists** as the left and right contexts and used the exchange rule; *in this talk, contexts will be either multisets or lists: exchange is never used.* The multiset-vs-list choice is made per-presentation, by the author, not fixed by LK.  
  
Second, and more directly against the frozen target: **sequent calculus proofs are *formless*** — any structure they contain must be *pulled out by extensive inference-rule permutation arguments*. The same source illustrates the non-determinism concretely: a single sequent can offer on the order of a thousand choices of left-introduction rule.  
  
This is the DI3 finding stated authoritatively rather than inferred by me: the field's position is that **LK by itself has no proof-search structure**, and that structure must be *imposed* — which is precisely why every formalization retrieved is a focusing discipline. My frozen S1 target asked for the unstructured object, and the literature's considered view is that the unstructured object has no form to formalize.  
  
**Status:** $S1 = \mathbf{OPEN}_{\mathrm{SR\text{-}B2v2}}$. Member 1 complete. **Eight prescribed invocations remain** (members 2–5). $L_1 = 3$ unfollowed leads.  
  
## Question for GPT  
  
A procedural question about candidate evaluation, arising now and recurring for the rest of Channel B.  
  
Member 1's Q8 returned four new top-level documents, all of which I judged INELIGIBLE from their returned snippets alone — each self-describes as a focused or polarized system, which is a discipline added to LK, hence DI3. **I did not retrieve their full texts.**  
  
**Is a snippet-level INELIGIBLE verdict sufficient under K-P1-DI, or does a terminal SOURCE-FAIL require full-text inspection of every non-obviously-ineligible candidate?**  
  
The asymmetry matters and cuts against speed: an EXACT/DIRECT certificate plainly requires full text, since it must exhibit the source's actual definitions. If INELIGIBLE also requires full text, then S1's terminal verdict requires reading on the order of 30–50 documents, and $\mathfrak{E}_0$ becomes very much larger than the retrieval budget alone suggested.  
  
I flag the direction: **snippet-level INELIGIBLE is the faster route to the verdict I expect**, so I should not authorize it. My inclination is that a snippet stating the system's own defining discipline — "LKF is a focused, one-sided sequent calculus," "our focused sequent calculus LKNF" — is self-certifying for INELIGIBLE, since the source itself names the added structure that triggers DI3. But a snippet that is merely *uninformative* about the search-state structure should not be dismissible on that basis, and I have not yet had to distinguish those two cases.  
  
Fix the rule before I continue, and specify what to do with the uninformative-snippet case, since that is where the real cost sits.  
  
## GPT TURN 31 — CANDIDATE-EVIDENCE STANDARD  
## Verdict  
\boxed{\text{Snippet-level evidence can sometimes prove INELIGIBLE, but not merely because the paper's headline system is focused.}}  
A terminal SOURCE-FAIL does **not** require reading every candidate cover-to-cover.  
It does require a **source-level decisive certificate** for every candidate counted as INELIGIBLE.  
The correct middle ground is:  
\boxed{\text{triage by snippet; adjudicate by minimum sufficient source inspection}.}  
   
⸻  
   
## 1. Three candidate states  
For every top-level SR-B2 result K, assign one of:  
\boxed{ \mathrm{INELIGIBLE}, \quad \mathrm{ELIGIBLE}, \quad \mathrm{REQUIRES\ INSPECTION}. }  
Do not convert “snippet did not show the target” into INELIGIBLE.  
Absence from a snippet is almost never evidence of absence from the source.  
   
⸻  
   
## 2. When snippet-level INELIGIBLE is sufficient  
A snippet may terminate the candidate as INELIGIBLE only when it contains an **affirmative source statement that logically excludes K-P1 eligibility**.  
Call this:  
\boxed{\mathrm{SI}\text{-}CERT}  
Snippet-level ineligibility is permitted iff the returned metadata/snippet establishes all three:  
**SI1 — explicit formal identity**  
The source explicitly identifies the formalism it defines.  
For example:  
“We introduce calculus X, a focused polarized extension of…”  
**SI2 — incompatible defining structure**  
The snippet affirmatively states a defining property incompatible with the frozen target.  
**SI3 — no possible K-P1 route follows from the snippet’s own description**  
The incompatibility is such that specialization or source-internal definitional expansion cannot yield the frozen target.  
Only then:  
\boxed{K=\mathrm{INELIGIBLE}_{snippet}}.  
   
⸻  
   
## 3. “This paper is focused” does not automatically satisfy SI3  
This corrects Claude’s current treatment of the four Q8 documents.  
A paper whose principal contribution is:  
\text{focused LK}  
is certainly not an EXACT match to frozen S1.  
But that does **not** prove the entire source is K-P1-ineligible.  
The document might also:  
* formally define ordinary LK before adding focusing;  
* define an unfocused search relation as a comparison object;  
* formally derive focusing from a source-defined unfocused search system;  
* explicitly give the multigoal search structure the experiment needs.  
Therefore:  
\boxed{ \text{“focused system”} \not\Rightarrow \text{whole document INELIGIBLE}. }  
It establishes only:  
\boxed{ \text{the focused formalism itself is not frozen S1}. }  
The source still requires targeted inspection unless its snippet affirmatively excludes any relevant ancestor/definition.  
So the four Q8 documents currently judged solely from “focused/polarized” snippets should be changed to:  
\boxed{\mathrm{REQUIRES\ INSPECTION}}  
unless stronger snippet text satisfies SI1–SI3.  
   
⸻  
   
## 4. What inspection is required  
Do **not** read 40 papers linearly from page 1 to the bibliography.  
For every REQUIRES INSPECTION candidate, perform a fixed **Targeted Source Inspection**:  
\boxed{\mathrm{TSI}\text{-}v1}  
Inspect, when accessible:  
1. abstract;  
2. introduction;  
3. section containing the formal definition of the calculus/formalism;  
4. section containing proof-search semantics/algorithm/operational description, if present;  
5. conclusion only if needed.  
And search within the document for the mechanically fixed terms:  
For S1:  
* proof search  
* search state  
* open sequent  
* open sequents  
* goal  
* goals  
* multiset  
* frontier  
* backward  
* transition  
No other exploratory reading is required unless one of those passages creates a plausible EXACT/DIRECT route needing verification.  
This bounds the cost while making the verdict source-grounded.  
   
⸻  
   
## 5. TSI terminal rules  
After TSI-v1:  
**EXACT**  
The source explicitly defines frozen S1.  
\Rightarrow \mathbf{READY}.  
**DIRECT**  
The source supplies an ancestor satisfying DI1–DI6/SRF-v1.  
\Rightarrow \mathbf{READY}.  
**INELIGIBLE**  
The inspected source positively establishes that:  
* it defines a different search organization; and  
* no exact/direct frozen-S1 formalization appears in the inspected definitional/search sections.  
Then:  
\boxed{\mathrm{INELIGIBLE}_{TSI}}.  
**INSPECTION-OPEN**  
If the document is inaccessible, truncated, or relevant sections cannot be inspected:  
\boxed{\mathrm{INSPECTION\!-\!OPEN}}.  
That candidate cannot be counted as INELIGIBLE.  
If any required candidate remains INSPECTION-OPEN at the end of SR-B2, the target cannot receive SOURCE-FAIL; it remains retrieval/inspection OPEN.  
   
⸻  
   
## 6. Full-document exhaustive negative proof is not required  
We should not require proving:  
nowhere in 200 pages does the desired definition occur.  
That standard would make bounded source retrieval effectively impossible.  
The operational negative certificate is instead:  
the source’s abstract/intro plus formal-definition and proof-search sections were inspected under TSI-v1, the fixed target terms were searched, and no K-P1 route survived.  
That is sufficient **for SOURCE-FAIL relative to SR-B2 v2 + TSI-v1**.  
As with retrieval itself, the claim remains bounded:  
\boxed{ \mathbf{SOURCE\!-\!FAIL}_{SR-B2v2+TSIv1} }  
not:  
no supporting literature exists.  
   
⸻  
   
## 7. Why uninformative snippets require inspection  
If a snippet merely says:  
“we study sequent calculus proof search…”  
that could hide either:  
* the exact frozen formalization;  
* a source-defined ancestor;  
* a focused alternative;  
* no formal state model at all.  
So:  
\boxed{ \text{uninformative snippet} \Rightarrow \mathrm{REQUIRES\ INSPECTION}. }  
Never:  
\text{uninformative} \Rightarrow \mathrm{INELIGIBLE}.  
This is the key anti-false-negative protection.  
   
⸻  
   
## 8. Why positive certificates require source inspection  
Claude is correct here.  
Neither:  
EXACT  
nor:  
DIRECT  
may be awarded from a search-engine snippet alone.  
A positive certificate must identify the actual source definitions and, for DIRECT, satisfy DI1–DI6.  
Therefore:  
\boxed{ EXACT/DIRECT\Rightarrow\text{source inspection mandatory}. }  
   
⸻  
   
## 9. Reclassify the current Q8 batch  
Based on Claude’s description alone:  
* LKF lecture notes;  
* focusing talk;  
* LKN/LKNF paper;  
* focused-sequent-calculus talk  
are clearly **nearby alternative formalisms**.  
But unless their returned snippets explicitly establish SI1–SI3 for the whole source:  
\boxed{ \text{reclassify them from INELIGIBLE to REQUIRES INSPECTION}. }  
The statements Claude already extracted from Miller about:  
* lists versus multisets;  
* exchange;  
* formlessness;  
* large proof-search nondeterminism  
are strong substantive DI3 evidence against deriving frozen S1 from bare LK.  
They do not, by themselves, prove those documents cannot separately contain the required formalization.  
Keep those two questions separate.  
   
⸻  
   
## 10. Uniformity  
TSI-v1 applies identically to:  
S1,\quad S6,\quad S7  
and any other OPEN target evaluated under SR-B2 v2.  
Use target-specific search terms mechanically derived from each frozen disputed component.  
For example, S7 would use terms drawn from:  
* Galois connection;  
* widening;  
* transfer;  
* abstract interpretation;  
* soundness;  
* combined formalism.  
Do not inspect S1 more deeply because it controls R_{\mathrm{primary}}.  
   
⸻  
   
## Binding rule  
Record before continuing Channel B:  
\boxed{ \begin{aligned} &\text{affirmatively self-excluding snippet satisfying SI1–SI3} &&\Rightarrow \mathrm{INELIGIBLE};\\ &\text{uninformative or merely different-headline snippet} &&\Rightarrow \mathrm{REQUIRES\ INSPECTION};\\ &\text{REQUIRES INSPECTION} &&\Rightarrow \mathrm{TSI\text{-}v1};\\ &\text{EXACT/DIRECT} &&\Rightarrow \text{source-level certificate required};\\ &\text{terminal SOURCE-FAIL} &&\Rightarrow \text{every prescribed candidate decisively adjudicated.} \end{aligned} }  
No cover-to-cover reading requirement.  
No snippet-based dismissal merely because the paper looks focused.  
This increases the work, but it prevents the negative result from being manufactured by search-engine summaries rather than the sources themselves.  
  
# CLAUDE TURN 32  
  
## Concession  
  
**Correct, and my error was significant.** "This paper is focused" establishes only that the *focused system* is not frozen S1 — not that the whole document is ineligible. A paper on focused LK is in fact one of the more likely places to find ordinary LK proof search formalized first, as the comparison object focusing is defined against. I was converting "different headline" into INELIGIBLE, which is snippet-based dismissal of exactly the sources most likely to contain the thing.  
  
**Reclassified to REQUIRES INSPECTION:** the four Q8 documents (LKF lecture notes; *Focusing Gentzen's Sequent Calculus* talk; Chaudhuri–Hetzl–Miller LKN/LKNF; *Focused Sequent Calculus Proof Systems* talk), plus all $N_1$ members not yet inspected.  
  
**Kept separate**, per §9: Miller's statements about lists-vs-multisets, exchange, formlessness, and search non-determinism are strong DI3 evidence *against deriving frozen S1 from bare LK*. They are not evidence that those documents lack the required formalization. Two different questions; I had merged them.  
  
## Executability check on TSI-v1, before committing  
  
DF-05 arose because SR-B2 v1 was frozen without checking whether I could run it. I am not repeating that. Testing TSI-v1 on one document now.  
  
Chosen: **Liang & Miller, *Focusing Gentzen's LK Proof System*** — $N_1$ member 2, and on the merits the single candidate most likely to define unfocused LK proof search as the object focusing is introduced against. Choosing the most rescue-favourable document for the feasibility test.  
  
Access denied (bot protection). Retrying on a different host — testing whether arXiv PDFs are fetchable, since several candidates live there. Target: $N_1$ member 1, Miller's survey.  
  
## TSI-v1 executability: partial  
  
- **arXiv PDFs: fetchable in full.** TSI-v1 is executable there.  
- **HAL: blocked** by bot protection (Anubis). Documents available only on HAL will return **INSPECTION-OPEN**, which by the frozen rule blocks SOURCE-FAIL. $N_1$ member 2 (Liang & Miller) is currently HAL-only in my retrieved set; an alternate host may exist.  
  
## TSI-v1 — $N_1$ member 1 (Miller, *Survey*) — complete  
  
Inspected: abstract, §1, §4, §5.1, §5.2, §8.2, conclusion. Fixed terms searched: *proof search, search state, open sequent(s), goal(s), multiset, frontier, backward, transition.*  
  
**"open sequent," "open sequents," and "frontier" do not occur in the document.** "Multiset" occurs throughout, always as *multiset of formulas* within a sequent.  
  
**The decisive passage is §8.2**, and it is not a null result — it is the source's own formalization of proof-search state:  
  
> Sequents are used to capture the **state of a logic programming computation**: the sequent $\Sigma : \mathcal{P} \vdash G$ represents a **configuration** where the current logic program is $\mathcal{P}$, the current goal is $G$, and the current signature of eigenvariables is $\Sigma$.  
  
Corroborated in §1: the proof-search approach views *the state of a computation as a sequent*, with *the changes that take place in sequents capturing the dynamics of computation*.  
  
**So the source does formalize proof-search state — as a *single sequent*, not as a multiset of open sequents.** Its dynamics question is posed over *border sequents* inside the focused system $\mathbf{LL}^f$, and its entire framing is uniform/goal-directed/focused proof.  
  
$$\text{Member 1} = \mathbf{INELIGIBLE}_{\mathrm{TSI}}$$  
  
Not EXACT (different state object). Not DIRECT: reaching the frozen multiset-frontier from "state = one sequent" requires FAR to supply the aggregation of open branches into a frontier — analyst construction, DI3.  
  
**This is more than a negative.** It is a substantive, source-grounded finding: the field's own formalization of proof-search state is a *single sequent configuration*. My frozen S1 posited a **frontier** object that differs from what the literature actually defines — which is DF-04-H with a specific mechanism attached rather than a bare pattern.  
  
## Question for GPT — a DI2 route I must not suppress  
  
The frozen state is *a finite multiset of open sequents*. There is a construction that might make this DI2 rather than DI3, and it runs against my verdict, so I raise it myself.  
  
A **partial derivation** — a proof tree whose leaves need not be axioms — uniquely determines its multiset of open leaves. No analyst choice is involved: the frontier is a function of the tree. And the transition relation "replace one open leaf by the premises of one backward rule instance" is a *relation*, so it requires no selection rule either. Both DI3 tests (*two inequivalent additions compatible with the same source instance*) appear to be passed.  
  
**If an eligible source formally defines partial/incomplete derivations, is the open-leaf multiset a DI2 source-internal definitional expansion — making frozen S1 DIRECT?**  
  
Two things make me unsure. (a) DI2 requires the component be *uniquely definable from the source structure*; the frontier is uniquely definable from a partial derivation, but "partial derivation" must itself be source-defined, and Gentzen-style presentations define *derivations* (complete trees), not partial ones. (b) Even granting the frontier, the frozen target is a transition system whose *objects* are frontiers, which requires taking the frontier as the primary state rather than the tree — a change of primitive that the source may not license.  
  
Rule on this before I continue Channel B. If DI2 applies, my search target changes materially: I should be looking for sources defining **partial derivations**, not sources defining proof-search state, and several documents I would otherwise dismiss become live candidates. If DI2 does not apply, member 1's verdict stands and the same reasoning will dispose of most of the remainder.  
  
## GPT TURN 32 — PARTIAL-DERIVATION / FRONTIER DI2 RULING  
## Verdict  
\boxed{\text{A source defining partial derivations is not, by itself, enough to make frozen S1 DIRECT.}}  
But Claude has identified a genuine DI2 route.  
Frozen S1 becomes DIRECT if an eligible source provides enough source-internal structure that the **frontier and its one-step evolution are definitional consequences**, rather than structures FAR chooses to impose.  
So the answer is conditional:  
\boxed{ \text{partial derivations + source-internal frontier semantics} \Rightarrow \text{potential DIRECT}; }  
\boxed{ \text{partial derivations alone} \not\Rightarrow \text{DIRECT}. }  
Member 1’s present verdict therefore stands.  
   
⸻  
   
## 1. The key distinction is not “tree versus frontier”  
Changing representation is not automatically disqualifying.  
If a source formalism A defines partial derivation trees and also determines a canonical observable:  
\operatorname{Fr}:A\to\mathsf{MSet}(\mathsf{Seq}),  
where:  
\operatorname{Fr}(T) = \text{multiset of open leaves of }T,  
then the fact that frozen S1 uses \operatorname{Fr}(T) rather than T as its state is not necessarily analyst construction.  
The real question is whether the target transition relation:  
M\to M'  
is **well-defined from the source formalism alone**.  
   
⸻  
   
## 2. Exact frontier-DI certificate  
Call this:  
\boxed{\mathrm{FDI}\text{-}v1}  
A partial-derivation source supports frozen S1 DIRECT only if all five conditions hold.  
**FDI1 — partial derivations are source-defined**  
The source must actually formalize finite incomplete/partial LK derivations, not merely complete proofs.  
A complete proof tree does not supply an open frontier:  
\operatorname{Fr}(T)=\varnothing.  
FAR may not invent “partial proof tree” as a new object.  
   
⸻  
   
**FDI2 — open leaves/frontier are source-internal**  
The source must either:  
1. explicitly define open leaves/frontiers; or  
2. provide a formal notion from which the frontier is uniquely definitionally recoverable without any additional convention.  
Merely observing externally that a finite tree has leaves is insufficient if the source does not distinguish:  
\text{closed leaf} \quad\text{from}\quad \text{open leaf}.  
That distinction is load-bearing.  
   
⸻  
   
**FDI3 — frontier multiplicity is fixed**  
Frozen S1 requires a **multiset** of open sequents.  
The source must determine whether repeated identical open sequents remain distinct.  
If the same partial derivation admits equally legitimate frontier representations as:  
* set;  
* sequence;  
* multiset;  
and the source does not fix or definitionally identify one with the frozen multiset representation, DI3 fires.  
So:  
\boxed{ \text{“take the leaves and call them a multiset”} }  
is not automatically DI2.  
   
⸻  
   
**FDI4 — one-step frontier evolution is source-induced**  
The source must determine a relation corresponding to:  
choose one open leaf carrying sequent s, apply one backward LK rule instance with conclusion s, and replace that occurrence by its premises.  
No scheduler is required because frozen S1 uses a relation rather than a deterministic function.  
That is an important point in Claude’s favor.  
Nondeterminism itself does **not** trigger DI3.  
If all applicable expansions are included:  
M\to M',  
no rule-selection policy has been added.  
Thus the earlier argument:  
“LK permits many proof-search choices, therefore no transition relation is determined”  
was too strong if a source-defined partial-derivation extension relation exists.  
Many outgoing transitions can be perfectly well-defined.  
   
⸻  
   
**FDI5 — frontier quotient is behaviorally well-defined**  
This is the hard part.  
Different partial derivation trees can have the same frontier:  
\operatorname{Fr}(T_1) = \operatorname{Fr}(T_2).  
Frozen S1 discards the tree history.  
Therefore the source must guarantee that future one-step possibilities depend only on the frontier, not on hidden tree structure.  
Formally, whenever:  
\operatorname{Fr}(T_1)=\operatorname{Fr}(T_2)=M,  
the induced sets of successor frontiers must agree:  
\{ \operatorname{Fr}(T'):T_1\rightsquigarrow T' \} = \{ \operatorname{Fr}(T'):T_2\rightsquigarrow T' \}.  
If this holds definitionally for ordinary context-free LK rule expansion, then the quotient by frontier is legitimate.  
If tree history, eigenvariable conditions, branch-local annotations, focusing state, or other hidden data can alter legal expansion, then frontier alone is insufficient and frozen S1 is not directly obtained.  
This is the precise test Claude was missing.  
   
⸻  
   
## 3. Nondeterminism does not by itself defeat S1  
This corrects an overstatement in the running DI3 argument.  
A transition system may be highly nondeterministic:  
s\to s_1,\ldots,s_n  
and still be completely determined.  
Therefore statements such as:  
“LK offers thousands of possible rule choices”  
show:  
\boxed{\text{no canonical deterministic search strategy}}  
but do **not** show:  
\boxed{\text{no canonical nondeterministic search relation}}.  
Frozen S1 never required a scheduler.  
It required:  
\text{all one-rule backward applications}.  
So this evidence remains relevant against strategy-based derivations, but it cannot by itself establish DI3 against the frozen relation.  
This correction should enter the audit record now.  
   
⸻  
   
## 4. Lists versus multisets also need narrower treatment  
Likewise:  
LK presentations use lists, sets, or multisets  
does not alone establish that frozen S1 is source-unsupported.  
There are two separate levels:  
**Inside each sequent**  
\Gamma\vdash\Delta.  
This concerns representation of formula contexts.  
**Across open goals**  
\{S_1,\ldots,S_n\}.  
This concerns the frontier representation.  
Variation in the first does not logically prove indeterminacy in the second.  
It may create a corpus/profile issue for the exact LK formalism, but it is not itself a proof that a multiset of open sequents cannot be source-derived.  
Keep those levels separate.  
   
⸻  
   
## 5. Does the source have to literally name the frontier?  
No.  
Requiring the exact term “frontier” would be too strict.  
DI2 permits definitional expansion.  
Thus a source can qualify without using FAR’s terminology if it formally defines, for example:  
* incomplete proof trees;  
* pending leaves;  
* unresolved goals;  
* open branches;  
and those objects uniquely determine the frozen frontier.  
The criterion is:  
\boxed{\text{formal definability without analyst choice}}  
not lexical identity.  
   
⸻  
   
## 6. But merely “trees have leaves” is too loose  
At the other extreme, FAR may not reason:  
Every finite partial tree obviously has leaves, therefore we can manufacture a multiset state space.  
That would make DI2 almost unlimited: any mathematical object has countless uniquely computable derived objects.  
The source-internal requirement therefore remains substantive.  
For this experiment, count a derived component as DI2 only when it is part of the source’s **formal apparatus for the target phenomenon**—explicitly defined, used in its rules/semantics, or definitionally required by those rules.  
Do not admit arbitrary mathematical functions that an analyst can define afterward.  
This is the boundary between:  
\text{definitional expansion}  
and:  
\text{post-hoc construction}.  
   
⸻  
   
## 7. Consequence for Member 1  
Miller’s survey, as Claude reports it, defines proof-search computation state as:  
\Sigma:\mathcal P\vdash G,  
a single sequent/configuration.  
Nothing reported indicates that it formally defines:  
* partial LK derivations;  
* their multiset of pending leaves;  
* a frontier quotient;  
* frontier-level one-rule transitions.  
Therefore:  
\boxed{ \text{Member 1 remains }\mathrm{INELIGIBLE}_{TSI}. }  
The newly recognized theoretical possibility does not retroactively make that source DIRECT.  
   
⸻  
   
## 8. Consequence for remaining Channel B  
Yes: partial derivations are now a live route.  
But do **not** change the prescribed queries.  
That would alter SR-B2 v2 after observing a promising conceptual route.  
Instead, while performing TSI-v1 on candidates already returned, inspect the already-fixed search terms and source sections for formal definitions equivalent to:  
* partial derivation;  
* incomplete proof;  
* pending/open leaves;  
* proof-tree extension;  
* goal collection.  
If such a definition appears naturally in a prescribed candidate, evaluate it under FDI1–FDI5.  
Do not launch new searches for "partial derivation" inside \mathfrak E_0.  
Log that as an RD-01 lead if it arises only bibliographically.  
   
⸻  
   
## 9. Revised exact S1 question  
The source-stage question is now sharper:  
Is there an eligible source, reached by SR-B2 v2, that either directly defines the frozen multiset-frontier LK search system or defines partial LK derivations from which that system follows under FDI1–FDI5?  
This is better than the earlier formulation:  
Does LK itself contain a proof-search discipline?  
The latter accidentally demanded more than frozen S1 requires.  
   
⸻  
   
## 10. Audit correction to DF-02b / DF-04-H  
Do not yet describe S1’s problem as:  
“calculus does not determine search structure.”  
That is still possible, but no longer established.  
Use the narrower current statement:  
\boxed{ \text{No eligible source encountered so far has been certified to determine the frozen frontier-level search structure.} }  
DF-04-H remains a hypothesis.  
If a partial-derivation source satisfies FDI1–FDI5, S1 may become READY and DF-04-H must absorb that result unchanged.  
   
⸻  
   
## Binding ruling  
\boxed{ \begin{aligned} &\text{partial derivations alone} &&\not\Rightarrow DIRECT;\\ &\text{source-defined partial derivations + FDI1--FDI5} &&\Rightarrow DIRECT;\\ &\text{nondeterminism of rule choice} &&\not\Rightarrow DI3;\\ &\text{analyst-created frontier from otherwise unrelated tree structure} &&\Rightarrow INELIGIBLE. \end{aligned} }  
Member 1 remains INELIGIBLE.  
Continue Channel B unchanged, but evaluate any source-defined partial-derivation route under FDI1–FDI5.  
  
# CLAUDE TURN 33  
  
## Concession — and it is a substantial reversal against my expectation  
  
**GPT's §3 correction is right and it defeats my strongest evidence.** Miller's "1000 choices" and "proofs are formless" establish that LK has **no canonical deterministic search strategy**. Frozen S1 never required one — it specifies a *relation* whose transitions are all one-rule backward applications. A highly nondeterministic transition relation is still a completely determined transition relation. My DI3 argument, run across Turns 25, 28, 31, and 32, conflated the two, and I should have caught it when I wrote the frozen target myself.  
  
Also accepted: §4 — variation in *intra-sequent* representation (lists/sets/multisets of formulas) is a different level from *frontier* representation, and I merged them.  
  
**Revised statement of the record, replacing my earlier DF-02b wording:** *No eligible source encountered so far has been certified to determine the frozen frontier-level search structure.* Not "the calculus does not determine search structure."  
  
**And I should say plainly: I now think S1 is more likely to reach READY than I did an hour ago.** FDI1 looks satisfiable — proof theory routinely defines derivations *of* a sequent *from* open premises, which is a partial derivation in all but name. FDI5, the hard condition, looks *favourable for frozen S1 specifically*: the target is **propositional** LK, so each open leaf is expandable by any rule instance with that sequent as conclusion, independently of tree history; the eigenvariable side-conditions that would create hidden dependence are first-order and absent here. If a prescribed candidate turns out to define partial derivations, FDI1–FDI5 may well be met.  
  
I record this because it runs against the outcome I have been anticipating since Turn 25, and I would rather state the update than let it emerge from the evidence looking like a discovery.  
  
FDI-v1 adopted. Prescribed queries unchanged; no new searches for "partial derivation"; such definitions evaluated under FDI1–FDI5 only where a prescribed candidate supplies them. Member 1 remains $\mathbf{INELIGIBLE}_{\mathrm{TSI}}$.  
  
## Channel B — member 2  
  
**Member 2, Q7 — a decisive lead.** The Springer version's snippet contains:  
  
> For this paper, we shall make the following distinction between **proof** and **derivation**. By proof, we mean a tree structure of inference rules and sequents such that all …  
  
That is a source-defined **proof/derivation distinction** — the standard shape of which is that a *derivation* permits leaves that are not axioms. That is FDI1. And it is on an accessible host, unlike the HAL copy.  
  
Running TSI-v1.  
  
# CLAUDE TURN 34 — TSI-v1, $N_1$ member 2  
  
Full text retrieved (Springer). TSI-v1 executed.  
  
## FDI1 and FDI2 are **satisfied** — partial derivations are source-defined  
  
Liang & Miller §2, verbatim:  
  
> For this paper, we shall make the following distinction between **proof** and **derivation**. By proof, we mean a tree structure of inference rules and sequents such that all premises are **closed**, in the sense that the inference rules at the leaves have zero premises (such as the initial rule). By derivation, we mean a similar tree structure of inference rules and sequents, but we do not assume that all leaves are closed: **derivations can have unproved premises**.  
  
This is exactly what I predicted in Turn 33 and it is stronger than I expected: **FDI1** (partial derivations formalized) and **FDI2** (closed vs. unproved leaves explicitly distinguished — the load-bearing distinction) are both met by an eligible source.  
  
Also resolved for this source: the intra-sequent level. §2 states that in Gentzen's system contexts are lists with an exchange rule, while in its Figure 1 **contexts are multisets and exchange is not used**. So the source fixes multisets at the formula level.  
  
## But FDI3–FDI5 fail  
  
Fixed-term search across the full text: **"search state," "open sequent(s)," and "frontier" do not occur.** "Multiset" occurs throughout, always for formulas or polarized formulas — never for a collection of pending sequents. "Transition" occurs only for cut-rule transformations.  
  
- **FDI3 — not fixed by the source.** The paper never states whether the unproved premises of a derivation form a set, multiset, or sequence. *I note the strongest counterargument, since it favours rescue:* leaves of a tree are **occurrences**, so "the unproved premises of a derivation" arguably determines a multiset canonically — a set reading would require identifying distinct occurrences bearing equal sequents, and a sequence reading would require an order neither is given. I think FDI3 may in fact be satisfiable on that basis. It does not change the verdict, because:  
- **FDI4 — fails.** The source defines no derivation-*extension* relation. Derivations exist here to support permutation and cut-elimination arguments, not search. Nothing source-internal says "replace an unproved premise by the premises of a rule instance."  
- **FDI5 — fails.** The frontier-quotient property — that successor frontiers depend only on the frontier and not on tree history — is nowhere addressed. It is plausibly *true* for propositional LK, but plausibility is not a source certificate.  
  
$$\text{Member 2} = \mathbf{INELIGIBLE}_{\mathrm{TSI}}$$  
  
## What this sharpens  
  
The S1 question is now much narrower and much better posed than at any earlier point:  
  
> **The literature does define partial derivations with unproved premises. It does not define the frontier as a state, its evolution relation, or the frontier quotient.** Frozen S1's state object exists in the sources; frozen S1's *dynamics on that object* does not.  
  
This is DF-04-H with the exact seam located. It also retires my Turn 25–31 framing entirely: the problem was never that LK lacks structure for proof search, nor that search is too nondeterministic. It is that the sources supply the *carrier* and FAR supplied the *transition relation on it*.  
  
## Question for GPT  
  
FDI4 is now the sole decisive condition for S1, and I want its bar fixed before I inspect further candidates.  
  
Given a source that defines (i) LK's inference rules and (ii) derivations with unproved premises, **is the extension relation** — *replace one unproved premise $s$ by the premises of a rule instance with conclusion $s$* — **a DI2 source-internal definitional expansion, or an analyst-supplied addition?**  
  
The case for DI2: the relation is *fully determined* by (i) and (ii) jointly. There is no choice — take all rule instances, at all unproved premises. Your Turn 32 §FDI4 already grants that nondeterminism does not trigger DI3, and no scheduler is needed.  
  
The case against: the source defines derivations as static objects for permutation arguments. It never asks how one derivation relates to another by rule application. Under your Turn 32 §6 boundary — *count a derived component as DI2 only when it is part of the source's formal apparatus for the target phenomenon* — a relation the source never forms may be post-hoc construction however forced its definition is.  
  
I cannot call this one, and it decides S1, hence $R_{\mathrm{primary}}$, hence whether $\mathfrak{E}_0$ has a content phase at all. **If DI2, member 2 likely flips to DIRECT once FDI3 and FDI5 are adjudicated, and S1 becomes READY. If analyst-supplied, S1 is heading for SOURCE-FAIL and no remaining candidate is likely to differ**, since the FDI1/FDI2 evidence I just found is about as favourable as the literature is going to get.  
  
**GPT TURN 34 — FDI4 ADJUDICATION; MEMBER 2 FLIPS TO DIRECT**  
  
**Verdict**  
  
\boxed{\text{FDI4 is satisfied by DI2 in this case.}}  
  
The extension relation  
  
replace exactly one unproved leaf by the premises of exactly one LK rule instance having that leaf sequent as conclusion  
  
is a **source-internal definitional expansion, not an analyst-supplied addition, once the source has formally supplied:**  
  
1. LK inference rules; and  
2. derivations as inference-rule/sequent trees allowed to have unproved leaves.  
  
Liang & Miller explicitly provide both of those ingredients: their LK presentation gives the inference rules and defines derivations as proof-tree-like objects whose leaves may remain unproved. Their presentation also fixes sequent contexts as multisets.   
  
More importantly, after tightening the definitions, I now judge:  
  
\boxed{\text{FDI3, FDI4, and FDI5 are all satisfiable for the propositional restriction.}}  
  
Therefore:  
  
\boxed{  
N_1\text{ member 2 is DIRECT under DI1+DI2/FDI-v1}.  
}  
  
and hence:  
  
\boxed{\mathrm{Status}(S1)=\mathbf{READY}.}  
  
This is a substantive reversal from my Turn-32 ruling.  
  
⸻  
  
**1. The boundary we need**  
  
Turn 32 said a derived component counts as DI2 only when it is part of the source’s formal apparatus rather than an arbitrary mathematical construction.  
  
That remains correct.  
  
But I would make a mistake if I interpreted it as:  
  
the source must explicitly name every derived relation FAR uses.  
  
If that were required, DI2 would nearly collapse into EXACT.  
  
A definitional expansion exists precisely to permit structures the source does not name primitively but which its formal definitions **uniquely determine.**  
  
The correct distinction is:  
  
\boxed{  
\text{canonical structural consequence}  
\neq  
\text{analyst-designed additional structure}.  
}  
  
The S1 extension relation is now on the first side of that boundary.  
  
⸻  
  
**2. Canonical-definitional-expansion test**  
  
Freeze the clarification as:  
  
\boxed{\mathrm{CDE}\text{-}v1}  
  
A component X** absent as a named primitive in source formalism **A** is admissible under DI2 if:**  
  
1. X is definable solely from source-defined objects, relations, constructors, and equality;  
2. its definition contains no free methodological parameter;  
3. no choice of scheduler, strategy, ordering convention, equivalence, granularity, or auxiliary semantics is required;  
4. it is invariant under the frozen representation equivalence;  
5. its granularity is anchored by a primitive source constructor rather than chosen by FAR;  
6. if the target quotients/forgets source structure, the induced operation is well-defined on the quotient.  
  
That is exactly the situation we now have.  
  
⸻  
  
**3. Formalize the source object**  
  
Let:  
  
\mathsf{Der}  
  
be Liang–Miller derivations.  
  
A derivation D** is a finite tree whose nodes are sequents and inference-rule instances, where some leaves may be unproved. This is source-defined, not supplied by FAR. **  
  
Let:  
  
\mathsf{Open}(D)  
  
be the finite set of **leaf occurrences that are unproved premises.**  
  
Each occurrence has a sequent label:  
  
\lambda_D:  
\mathsf{Open}(D)\to\mathsf{Seq}.  
  
We can now examine FDI3–FDI5 directly.  
  
⸻  
  
**4. FDI3 — the frontier multiset is canonical**  
  
Claude was too pessimistic here.  
  
Because \mathsf{Open}(D)** consists of occurrences, duplicate leaves carrying the same sequent remain distinct occurrences.**  
  
Therefore there is a uniquely determined finite multiset:  
  
\operatorname{Fr}(D)  
=  
(\lambda_D)_\ast\mathsf{Open}(D),  
  
i.e. the multiset of labels of the open leaf occurrences.  
  
If two different leaves are both labelled S**, then:**  
  
\operatorname{Fr}(D)(S)=2.  
  
No ordering is introduced.  
  
No duplicate occurrences are identified.  
  
No analyst decides between:  
  
* set;  
* list;  
* multiset.  
  
The tree’s occurrence structure already fixes the multiplicities; the multiset merely forgets irrelevant leaf identities while preserving counts.  
  
Thus:  
  
\boxed{\mathrm{FDI3}=PASS.}  
  
This is stronger than “trees obviously have leaves.”  
  
The key is that the source formally gives us a tree of inference-rule/sequent **occurrences, and open versus closed leaves is source-defined. The multiset is then a canonical image of that source-defined structure.**  
  
⸻  
  
**5. FDI4 — one-rule extension is canonical**  
  
Define an elementary extension relation:  
  
D\;\rightsquigarrow_1\;D'  
  
iff D'** is obtained from **D** by:**  
  
1. choosing one open-leaf occurrence \ell;  
2. taking one source-defined LK inference-rule instance \rho whose conclusion equals the sequent labelling \ell;  
3. replacing that open leaf with the inference node \rho and its premise sequents.  
  
The objection was:  
  
Liang & Miller never explicitly define \rightsquigarrow_1.  
  
That does not make it analyst-supplied.  
  
Why?  
  
Because the source has already fixed the atomic constructor from which derivation trees are built:  
  
\text{one inference-rule instance}.  
  
Consequently, “extend a partial derivation by exactly one inference-rule node” is the **cover relation generated by the source’s own tree constructor.**  
  
The step granularity is not chosen because FAR prefers it.  
  
It is anchored to:  
  
\boxed{\text{one source inference-rule instance}.}  
  
There is no scheduler.  
  
There is no priority relation.  
  
There is no focusing discipline.  
  
There is no selection function.  
  
All permitted extensions are retained.  
  
Therefore nondeterminism is irrelevant:  
  
D\rightsquigarrow_1D'_1,\ldots,  
D\rightsquigarrow_1D'_n  
  
is still one completely determined relation.  
  
Thus:  
  
\boxed{\mathrm{FDI4}=PASS.}  
  
⸻  
  
**6. Why this is not the kind of arbitrary construction Turn 32 prohibited**  
  
Compare two constructions.  
  
**Allowed**  
  
From a source-defined partial derivation and source-defined inference rules:  
  
\text{add one inference-rule instance at one unproved leaf}.  
  
Every ingredient and the atomic granularity come from the source.  
  
**Forbidden**  
  
Define:  
  
expand all invertible rules first, then select a noninvertible formula according to some priority ordering.  
  
That introduces:  
  
* phase structure;  
* a classification;  
* scheduling;  
* potentially polarity.  
  
Those are additional choices.  
  
Likewise:  
  
expand every currently open leaf simultaneously  
  
would define a different step granularity not selected by the source.  
  
But:  
  
\boxed{\text{exactly one inference node}}  
  
is privileged by the source’s inductive construction itself.  
  
That is why the current relation passes CDE-v1.  
  
⸻  
  
**7. FDI5 — frontier quotient is well-defined for propositional LK**  
  
This is the decisive proof.  
  
Suppose:  
  
\operatorname{Fr}(D_1)  
=  
\operatorname{Fr}(D_2)  
=  
M.  
  
Take an occurrence of sequent S** in **M** and any propositional LK rule instance:**  
  
\frac{P_1\quad\cdots\quad P_k}{S}\rho.  
  
Expanding that occurrence changes the frontier to:  
  
M'  
=  
M-[S]+[P_1]+\cdots+[P_k].  
  
Crucially, this expression depends only on:  
  
* the current frontier M;  
* the selected occurrence of S;  
* the source-defined rule instance \rho.  
  
It does not depend on the derivation history above that leaf.  
  
Therefore if D_1** and **D_2** have the same frontier, every elementary extension available from **D_1** has a corresponding extension from **D_2** yielding the same successor frontier, and conversely.**  
  
Hence:  
  
\{  
\operatorname{Fr}(D'):  
D_1\rightsquigarrow_1D'  
\}  
=  
\{  
\operatorname{Fr}(D'):  
D_2\rightsquigarrow_1D'  
\}.  
  
Therefore the relation descends to the quotient:  
  
[D]_{\operatorname{Fr}}  
\longmapsto  
\operatorname{Fr}(D).  
  
So:  
  
\boxed{\mathrm{FDI5}=PASS}  
  
for the frozen **propositional target.**  
  
⸻  
  
**8. Why propositionality matters**  
  
For first-order calculi, eigenvariable/freshness conditions can make quotienting by a bare multiset of sequents more delicate because legality can depend on variable context not represented by the naive frontier.  
  
But frozen S1 is propositional.  
  
Liang & Miller’s source treats first-order LK, but DI1 permits restriction to the propositional fragment. Their paper explicitly starts from LK and formalizes its inference rules before constructing LKF.   
  
After propositional restriction, the relevant eigenvariable issue disappears.  
  
Thus the source’s greater generality does not defeat the direct-instantiation certificate.  
  
⸻  
  
**9. The resulting target is exactly the frozen search graph**  
  
Define:  
  
\mathsf{State}  
=  
\mathsf{MSet}_{fin}(\mathsf{Seq}_{prop}).  
  
Initial state for root sequent S_0**:**  
  
M_0=[S_0].  
  
And:  
  
M\to M'  
  
iff there exists:  
  
* an occurrence S\in M;  
* a propositional LK rule instance  
  
\frac{P_1\cdots P_k}{S}  
  
such that:  
  
M'  
=  
M-[S]+[P_1]+\cdots+[P_k].  
  
That is exactly the frozen S1 convention:  
  
finite multiset of open sequents; one backward LK rule application.  
  
No extra search policy appears.  
  
No focusing appears.  
  
No arbitrary aggregation appears.  
  
No FAR operator appears.  
  
Therefore the construction is not merely related to S1.  
  
It is S1.  
  
⸻  
  
**10. Member 2 verdict changes**  
  
Claude gave member 2:  
  
\mathbf{INELIGIBLE}_{TSI}  
  
because FDI4 and FDI5 were not explicitly stated by the paper.  
  
I reverse that adjudication.  
  
The source need not state the theorem:  
  
“the frontier quotient has a well-defined transition relation.”  
  
K-P1-DI permits us to prove a **definitional-expansion certificate from the source’s definitions.**  
  
Otherwise every nontrivial DI2 certificate would require its conclusion already to appear in the source.  
  
So:  
  
\boxed{  
\text{Member 2}  
=  
\mathbf{DIRECT}.  
}  
  
Certificate:  
  
\boxed{  
DI1  
+  
FDI1  
+  
FDI2  
+  
FDI3  
+  
FDI4  
+  
FDI5.  
}  
  
The source supplies FDI1–FDI2 directly; FDI3–FDI5 follow canonically from its source-defined derivation-tree and inference-rule structure under propositional restriction. The source itself explicitly defines derivations with unproved premises, confirming the critical source-side premise of this argument.   
  
⸻  
  
**11. Consequence for S1**  
  
An existential certificate has succeeded.  
  
Therefore the frozen SR-B2 rule fires:  
  
\boxed{  
\mathrm{Status}(S1)=\mathbf{READY}.  
}  
  
The remaining S1 Channel-B invocations are **not required for target-instantiation status.**  
  
Do not run them merely to try to overturn an established existence certificate.  
  
They may be relevant later to K-P4/source-profile enumeration under its separate protocol, but the negative search for S1 stops here.  
  
⸻  
  
**12. Consequence for **c_0  
  
S2 is already provisionally READY.  
  
Now:  
  
S1=\mathbf{READY}.  
  
Therefore, subject to finalization of S2’s already-supported source certificate:  
  
\boxed{  
R_{\mathrm{primary}}  
=  
\mathbf{TRUE}.  
}  
  
Thus the precondition-stop contingency does **not fire on S1.**  
  
And:  
  
\boxed{  
c_0  
\text{ survives the source-instantiation gate}.  
}  
  
A2 remains testable.  
  
No rescue occurred.  
  
The exact target that seemed likely to fail instead survived because the source evidence exposed a derivation object from which the frozen nondeterministic frontier dynamics are definitionally recoverable.  
  
That is the outcome the protocol must accept.  
  
⸻  
  
**13. DF-04-H takes a direct hit**  
  
This matters.  
  
DF-04-H predicted that dialogue-assembled schemas would disproportionately fail K-P1 because the operational content was supplied by FAR.  
  
S1 was its strongest apparent supporting case.  
  
It now passes.  
  
Therefore do not continue describing:  
  
“the three non-READY schemas are exactly the three assembled ones.”  
  
That statement is obsolete.  
  
For S1 specifically, the correct result is almost the opposite:  
  
FAR chose a frontier-level representation not explicitly named by the retrieved source, but the representation and one-step dynamics were nevertheless directly recoverable by definitional expansion from source-native partial derivations and inference rules.  
  
That is evidence **against the strongest form of DF-04-H.**  
  
Its final evaluation still waits for S6 and S7.  
  
Do not rewrite the hypothesis.  
  
⸻  
  
**14. Audit correction**  
  
Record explicitly that the following earlier propositions were withdrawn in sequence:  
  
1. LK nondeterminism implies no native transition relation — **false**.  
2. list/set/multiset variation inside sequents establishes frontier indeterminacy — **false inference**.  
3. a source must explicitly state the derivation-extension relation for FDI4 — **too strong**.  
4. Liang–Miller member 2 is INELIGIBLE — **reversed to DIRECT after canonical-definitional-expansion audit**.  
  
This is exactly why the adversarial loop exists.  
  
⸻  
  
**Next action**  
  
Stop S1’s negative SR-B2 search under the frozen existential-success rule.  
  
Record the full DIRECT certificate.  
  
Then continue in the already-fixed unresolved-target order:  
  
\boxed{S6\rightarrow S7.}  
  
Apply CDE-v1 consistently there.  
  
In particular, do not repeat the S1 mistake:  
  
\boxed{  
\text{a source need not explicitly name every target operation if that operation is uniquely and canonically determined by source-native structure.}  
}  
  
But equally:  
  
\boxed{  
\text{“we can mathematically define something from the source” is insufficient unless CDE-v1 removes every analyst choice.}  
}  
  
## For S1, that bar is now met.   
  
# CLAUDE TURN 33  
  
## Concession — and it is a substantial reversal against my expectation  
  
**GPT's §3 correction is right and it defeats my strongest evidence.** Miller's "1000 choices" and "proofs are formless" establish that LK has **no canonical deterministic search strategy**. Frozen S1 never required one — it specifies a *relation* whose transitions are all one-rule backward applications. A highly nondeterministic transition relation is still a completely determined transition relation. My DI3 argument, run across Turns 25, 28, 31, and 32, conflated the two, and I should have caught it when I wrote the frozen target myself.  
  
Also accepted: §4 — variation in *intra-sequent* representation (lists/sets/multisets of formulas) is a different level from *frontier* representation, and I merged them.  
  
**Revised statement of the record, replacing my earlier DF-02b wording:** *No eligible source encountered so far has been certified to determine the frozen frontier-level search structure.* Not "the calculus does not determine search structure."  
  
**And I should say plainly: I now think S1 is more likely to reach READY than I did an hour ago.** FDI1 looks satisfiable — proof theory routinely defines derivations *of* a sequent *from* open premises, which is a partial derivation in all but name. FDI5, the hard condition, looks *favourable for frozen S1 specifically*: the target is **propositional** LK, so each open leaf is expandable by any rule instance with that sequent as conclusion, independently of tree history; the eigenvariable side-conditions that would create hidden dependence are first-order and absent here. If a prescribed candidate turns out to define partial derivations, FDI1–FDI5 may well be met.  
  
I record this because it runs against the outcome I have been anticipating since Turn 25, and I would rather state the update than let it emerge from the evidence looking like a discovery.  
  
FDI-v1 adopted. Prescribed queries unchanged; no new searches for "partial derivation"; such definitions evaluated under FDI1–FDI5 only where a prescribed candidate supplies them. Member 1 remains $\mathbf{INELIGIBLE}_{\mathrm{TSI}}$.  
  
## Channel B — member 2  
  
**Member 2, Q7 — a decisive lead.** The Springer version's snippet contains:  
  
> For this paper, we shall make the following distinction between **proof** and **derivation**. By proof, we mean a tree structure of inference rules and sequents such that all …  
  
That is a source-defined **proof/derivation distinction** — the standard shape of which is that a *derivation* permits leaves that are not axioms. That is FDI1. And it is on an accessible host, unlike the HAL copy.  
  
Running TSI-v1.  
  
# CLAUDE TURN 34 — TSI-v1, $N_1$ member 2  
  
Full text retrieved (Springer). TSI-v1 executed.  
  
## FDI1 and FDI2 are **satisfied** — partial derivations are source-defined  
  
Liang & Miller §2, verbatim:  
  
> For this paper, we shall make the following distinction between **proof** and **derivation**. By proof, we mean a tree structure of inference rules and sequents such that all premises are **closed**, in the sense that the inference rules at the leaves have zero premises (such as the initial rule). By derivation, we mean a similar tree structure of inference rules and sequents, but we do not assume that all leaves are closed: **derivations can have unproved premises**.  
  
This is exactly what I predicted in Turn 33 and it is stronger than I expected: **FDI1** (partial derivations formalized) and **FDI2** (closed vs. unproved leaves explicitly distinguished — the load-bearing distinction) are both met by an eligible source.  
  
Also resolved for this source: the intra-sequent level. §2 states that in Gentzen's system contexts are lists with an exchange rule, while in its Figure 1 **contexts are multisets and exchange is not used**. So the source fixes multisets at the formula level.  
  
## But FDI3–FDI5 fail  
  
Fixed-term search across the full text: **"search state," "open sequent(s)," and "frontier" do not occur.** "Multiset" occurs throughout, always for formulas or polarized formulas — never for a collection of pending sequents. "Transition" occurs only for cut-rule transformations.  
  
- **FDI3 — not fixed by the source.** The paper never states whether the unproved premises of a derivation form a set, multiset, or sequence. *I note the strongest counterargument, since it favours rescue:* leaves of a tree are **occurrences**, so "the unproved premises of a derivation" arguably determines a multiset canonically — a set reading would require identifying distinct occurrences bearing equal sequents, and a sequence reading would require an order neither is given. I think FDI3 may in fact be satisfiable on that basis. It does not change the verdict, because:  
- **FDI4 — fails.** The source defines no derivation-*extension* relation. Derivations exist here to support permutation and cut-elimination arguments, not search. Nothing source-internal says "replace an unproved premise by the premises of a rule instance."  
- **FDI5 — fails.** The frontier-quotient property — that successor frontiers depend only on the frontier and not on tree history — is nowhere addressed. It is plausibly *true* for propositional LK, but plausibility is not a source certificate.  
  
$$\text{Member 2} = \mathbf{INELIGIBLE}_{\mathrm{TSI}}$$  
  
## What this sharpens  
  
The S1 question is now much narrower and much better posed than at any earlier point:  
  
> **The literature does define partial derivations with unproved premises. It does not define the frontier as a state, its evolution relation, or the frontier quotient.** Frozen S1's state object exists in the sources; frozen S1's *dynamics on that object* does not.  
  
This is DF-04-H with the exact seam located. It also retires my Turn 25–31 framing entirely: the problem was never that LK lacks structure for proof search, nor that search is too nondeterministic. It is that the sources supply the *carrier* and FAR supplied the *transition relation on it*.  
  
## Question for GPT  
  
FDI4 is now the sole decisive condition for S1, and I want its bar fixed before I inspect further candidates.  
  
Given a source that defines (i) LK's inference rules and (ii) derivations with unproved premises, **is the extension relation** — *replace one unproved premise $s$ by the premises of a rule instance with conclusion $s$* — **a DI2 source-internal definitional expansion, or an analyst-supplied addition?**  
  
The case for DI2: the relation is *fully determined* by (i) and (ii) jointly. There is no choice — take all rule instances, at all unproved premises. Your Turn 32 §FDI4 already grants that nondeterminism does not trigger DI3, and no scheduler is needed.  
  
The case against: the source defines derivations as static objects for permutation arguments. It never asks how one derivation relates to another by rule application. Under your Turn 32 §6 boundary — *count a derived component as DI2 only when it is part of the source's formal apparatus for the target phenomenon* — a relation the source never forms may be post-hoc construction however forced its definition is.  
  
I cannot call this one, and it decides S1, hence $R_{\mathrm{primary}}$, hence whether $\mathfrak{E}_0$ has a content phase at all. **If DI2, member 2 likely flips to DIRECT once FDI3 and FDI5 are adjudicated, and S1 becomes READY. If analyst-supplied, S1 is heading for SOURCE-FAIL and no remaining candidate is likely to differ**, since the FDI1/FDI2 evidence I just found is about as favourable as the literature is going to get.  
  
# CLAUDE TURN 35 — AUDIT OF THE S1 CERTIFICATE  
  
## Corrections accepted  
  
Three are defeats of my own claims, recorded as such:  
  
1. **LK nondeterminism ⇒ no determined search relation** — withdrawn (already conceded Turn 33).  
2. **Intra-sequent list/set/multiset variation ⇒ frontier indeterminacy** — withdrawn; category-level conflation.  
3. **FDI4 requires the source to state the extension relation explicitly** — withdrawn. CDE-v1's point is right: requiring a name would collapse DI2 into EXACT.  
4. Member 2 reversed to **DIRECT**.  
  
**And I record the substantive reversal plainly.** Since Turn 25 I have expected S1 to fail. It did not, and the reason is one I raised myself in Turn 32 and then under-weighted: the sources *do* define partial derivations. My expectation was wrong and the procedure corrected it.  
  
## Verification of the certificate — I checked each condition independently  
  
**FDI5.** GPT's argument is correct and I verify it. In propositional LK, which backward rule instances have conclusion $S$ is a function of $S$ and the rule schemata alone. No eigenvariable side-conditions exist (they are first-order), and nothing below a leaf constrains what may be applied at it. Hence for $\mathrm{Fr}(D_1) = \mathrm{Fr}(D_2)$ the successor frontier sets coincide. Correct. *(Minor: the text says "history above that leaf"; leaves are above, history is below. Wording only.)*  
  
**FDI4.** Correct. The elementary constructor of a derivation tree *is* the single rule instance, so one-rule extension inherits its granularity from a source primitive rather than from a choice. Alternatives — simultaneous expansion at all leaves, maximal chains — are non-elementary and therefore not competitors for the canonical step.  
  
**FDI3.** Correct, and stronger than I credited in Turn 34. Multiset is the unique quotient that forgets leaf identity and order while retaining multiplicity; set over-identifies distinct occurrences, sequence adds unsupplied order. The forgetting itself is DI1-licensed, and FDI5 is what makes it legitimate rather than lossy.  
  
**Over-generation check on CDE-v1**, which I ran because a newly widened rule should be tested against cases it must *not* flip: it does **not** reverse $N_1$ member 1 (Miller's survey has no partial-derivation notion, so FDI1 fails at the first step); it does not rescue S7 (whose defect is DI4 cross-source assembly, untouched by definitional expansion); it does not admit the HOL goal-stack (blocked earlier at NM1/SRF-v1); and it does not manufacture transformations for S10 (Dung supplies no constructor generating extensions stepwise). CDE-v1 is wider than DI2 was, but on these four tests it is not unboundedly wide.  
  
## One residual gap, and it runs against the rescue  
  
Liang & Miller's Figure 1 LK is **first-order** — formulas are built with $\wedge, t, \vee, f, \supset$ **and** the quantifiers $\forall, \exists$. Frozen S1 is **propositional**. The certificate therefore depends on a restriction to the quantifier-free fragment, and the source does not formally carve out that fragment; it mentions propositional connectives only in passing.  
  
DI1 permits *restricting to a formally specified subclass* and requires only that the restriction be *stated independently of FAR's results* — which the quantifier-free fragment is. SRF-v1's stricter "source explicitly identifies a fragment $F_0' \cong F$" governs cross-formalism family membership under NM1, a different question from restriction within one formalism.  
  
I judge DI1 controls and the restriction is licensed. But this is precisely the point where the certificate is thinnest, and FDI5 — the load-bearing condition — is **true only because** the target is propositional. So the whole certificate rests on a restriction the source does not itself perform. Flagging it rather than passing over it.  
  
## Process concern, stated for the record  
  
**CDE-v1 was introduced at the moment it rescued the experiment**, and after I had disclosed which way each answer would resolve. That is structurally the same pattern I have objected to eleven times in this dialogue, now running in the preserving direction.  
  
I do not think it is a violation: the substance survives independent verification above, the over-generation check is clean, and the alternative reading of FDI4 was genuinely too strong. But the audit trail should say that CDE-v1's provenance is *"fixed in GPT Turn 34, after member 2's FDI1/FDI2 evidence, and with the direction of its consequence known."* If a later reviewer finds CDE-v1 over-permissive, this is the entry that should surface.  
  
## Status  
  
$$\mathrm{Status}(S1) = \mathbf{READY} \quad \text{(certificate: DI1 + FDI1–FDI5 + CDE-v1, source: Liang \& Miller)}$$  
  
S1 negative search stopped under the frozen existential early-stop. $R_{\mathrm{primary}}$ pending S2 finalization. $c_0$ survives the gate; **A2 remains testable**; PRECONDITION STOP does not fire.  
  
DF-04-H takes a real counter-hit and is not rewritten: *assembled by the dialogue* ≠ *not source-grounded*. Final evaluation still waits on S6, S7.  
  
Next in order: **S6**, then **S7**, under SR-B2 v2 + TSI-v1 + CDE-v1.  
  
## Question for GPT  
  
Before I run S6, fix how CDE-v1 interacts with the **adversarial** panel, because S6 is where it first bites and the answer is not obvious.  
  
S6's frozen target is *backward MLL proof search; state = sequent with resource context*. If an eligible MLL source defines (i) MLL rules and (ii) derivations with unproved premises — and the MLL literature is if anything more explicit about incomplete derivations than the classical literature — then CDE-v1 appears to deliver S6 by the **same** certificate that delivered S1, essentially automatically.  
  
**Two consequences, and I want you to pick before I look:**  
  
**(A)** If CDE-v1 makes every proof-calculus target READY once partial derivations are source-defined, then the K-P1 gate has almost no discriminating power over calculus-based targets, and DF-04-H's evaluation on S6 carries no information — it was predetermined by the rule, not by the evidence.  
  
**(B)** If S6 has a feature that blocks the transfer — and the candidate is **FDI5**: MLL's context-splitting in $\otimes$/$\multimap L$ divides the bounded zone between premises, so whether a given rule instance applies at a leaf may depend on resource accounting that a bare multiset of sequents could retain or lose — then FDI5 must be checked *de novo* for S6 rather than inherited.  
  
I believe (B) is correct and that FDI5 is exactly where the resource-sensitivity that got S6 admitted to $D_{\mathrm{adv}}$ should show up. But I have just been wrong about S1 in the same shape of argument, so I am not confident, and if (A) is right then a frozen gate has less power than we have been attributing to it and that should be recorded now rather than discovered after S6 passes.  
  
**GPT TURN 35 — CDE-v1 DOES NOT TRANSFER AUTOMATICALLY TO S6**  
  
**Verdict**  
  
\boxed{\text{(B) is correct.}}  
  
CDE-v1 is an **admissibility rule for definitional expansion, not a theorem saying:**  
  
\text{source-defined partial derivations}  
\Rightarrow  
\text{every proof-calculus target is READY}.  
  
Every target must re-prove the analogue of FDI3–FDI5 independently.  
  
But I would correct one part of Claude’s proposed mechanism:  
  
\boxed{\text{MLL resource splitting does not itself imply FDI5 failure.}}  
  
A backward multiplicative rule may admit many resource partitions. If the frozen transition relation contains **all admissible rule instances, that is ordinary nondeterminism, exactly as in S1. It is not underdetermination.**  
  
The harder S6 issue is whether the frozen state representation preserves the **joint multi-premise obligation and the resource split that generated it.**  
  
That must be checked de novo.  
  
⸻  
  
**1. CDE-v1 has zero automatic transfer power**  
  
The S1 certificate had this form:  
  
\text{source structure}  
+  
\text{canonical derivation}  
+  
\text{canonical quotient}  
+  
\text{well-defined induced transition}  
\Rightarrow  
S1.  
  
CDE-v1 merely allowed the last structures to be **proved from source definitions rather than literally named by the source.**  
  
It did not establish a general lemma:  
  
\forall\text{ sequent calculi }L,\quad  
\text{partial derivations}(L)  
\Rightarrow  
\text{frozen FAR search system}(L).  
  
No such lemma has been proved.  
  
Thus:  
  
\boxed{\text{S6 starts with no inherited FDI3/4/5 verdicts.}}  
  
FDI1/FDI2-style evidence from an MLL source may look structurally analogous to S1, but everything downstream must be re-certified.  
  
This also means S6 remains informative for DF-04-H. Its result is not predetermined by CDE-v1.  
  
⸻  
  
**2. Resource splitting is not automatically the blocker**  
  
Suppose an MLL multiplicative rule has a backward instance schematically of the form  
  
\frac{\Gamma\vdash A \qquad \Delta\vdash B}  
{\Gamma,\Delta\vdash A\otimes B}.  
  
Backward search may require choosing a partition of the available linear resources between \Gamma** and **\Delta**.**  
  
There may be many such partitions.  
  
But if each partition determines a legitimate rule instance, then the relation can simply contain every such instance:  
  
S\to_{\rho,\Gamma,\Delta}(P_1,P_2).  
  
No scheduler is required.  
  
No favored partition is required.  
  
Thus:  
  
\boxed{  
\text{multiple resource splits}  
\neq  
\text{analyst choice}  
}  
  
provided the source’s MLL rule schema itself determines what counts as an admissible split.  
  
That is the same correction that saved S1 from the “1000 choices” argument.  
  
Linear-logic proof search is indeed classically treated as highly nondeterministic, with focusing introduced to restrict that search space rather than to make the underlying calculus cease to exist.   
  
⸻  
  
**3. The real S6 problem: AND-branching**  
  
This is where S6 differs materially from the frozen S1 state.  
  
For S1, the state was already:  
  
\boxed{\text{multiset of all currently open sequents}.}  
  
So when a binary rule was applied, replacing one frontier occurrence by two premises preserved the fact that **both premises remained obligations.**  
  
Frozen S6, as currently stated, is:  
  
backward MLL proof search; **state = sequent with resource context**.  
  
That creates a question the S1 certificate never faced.  
  
A binary multiplicative rule does not produce one successor obligation.  
  
It produces a **joint premise family:**  
  
(P_1,P_2)  
  
both of which must eventually succeed.  
  
Therefore, if the supposed S6 search graph represents the step merely as:  
  
S\to P_1  
  
and:  
  
S\to P_2,  
  
it has lost essential information.  
  
Those two independent edges could be misread as an OR:  
  
prove either successor.  
  
But the rule requires AND:  
  
prove both successors arising from the same resource partition.  
  
That is not cosmetic.  
  
⸻  
  
**4. Freeze an S6-specific certificate**  
  
Call it:  
  
\boxed{\mathrm{MFDI}\text{-}v1}  
  
for multiplicative-frontier definitional instantiation.  
  
S6 reaches DIRECT through the S1-style CDE route only if all of the following hold.  
  
**MFDI1 — source-defined incomplete derivations**  
  
The eligible source defines MLL derivations/proof structures in which pending premises can remain open.  
  
Same role as S1 FDI1/2.  
  
⸻  
  
**MFDI2 — resource-sensitive rule instances are source-determined**  
  
For every backward multiplicative rule, the source formalism itself determines:  
  
* what resources are available;  
* which partitions/splits are legal;  
* what premise sequents result.  
  
All admissible splits may be retained.  
  
No heuristic split is introduced.  
  
If this holds:  
  
\boxed{\text{resource nondeterminism is harmless}.}  
  
⸻  
  
**MFDI3 — pending obligations retain multiplicity and resource content**  
  
Whatever target representation is derived must preserve each pending sequent together with its allocated linear context.  
  
It may not collapse:  
  
(\Gamma\vdash A,\Delta\vdash B)  
  
into some representation that forgets which resources belong to which obligation.  
  
⸻  
  
**MFDI4 — one-step extension preserves premise grouping**  
  
For an n**-premise rule instance:**  
  
\frac{P_1\;\cdots\;P_n}{S},  
  
the derived transition must preserve the fact that:  
  
\{P_1,\ldots,P_n\}  
  
is **one jointly generated premise family.**  
  
A representation as a hyperedge,  
  
S\to\{P_1,\ldots,P_n\},  
  
or a frontier update,  
  
M\to  
M-[S]+[P_1]+\cdots+[P_n],  
  
can do this.  
  
Independent ordinary edges:  
  
S\to P_i  
  
generally do not.  
  
⸻  
  
**MFDI5 — state sufficiency / quotient well-definedness**  
  
If two source-native partial derivations map to the same frozen S6 state, then they must admit exactly the same induced next-step possibilities—including resource partitions and joint premise families.  
  
Formally, for quotient map q**,**  
  
q(D_1)=q(D_2)  
  
must imply equality of induced successor structures.  
  
This is the true S6 analogue of S1’s FDI5.  
  
⸻  
  
**MFDI6 — no hidden branch history**  
  
Legal future expansion may not depend on information discarded by the frozen state, such as:  
  
* which sibling premise a branch came from;  
* a resource allocation no longer represented;  
* proof-net linkage;  
* focusing phase;  
* branch-local annotations.  
  
If such information affects legal successors, the frozen state is insufficient.  
  
Then CDE-v1 cannot rescue it.  
  
⸻  
  
**5. This exposes a possible typing problem in frozen S6**  
  
Before retrieval, Claude should preserve the exact frozen schema and answer from sources, not silently improve it.  
  
If:  
  
\mathcal S_{6,a}  
  
really has **single sequents as states and an ordinary binary transition relation:**  
  
\to\;\subseteq Seq\times Seq,  
  
then multi-premise multiplicative rules are immediately suspicious.  
  
The native proof-search object may actually be:  
  
* a frontier of open sequents;  
* an AND/OR graph;  
* a hypergraph;  
* or a derivation-extension system,  
  
rather than an ordinary graph on single sequents.  
  
Do not repair S6 now.  
  
Instead ask:  
  
\boxed{  
\text{Does an eligible source certify the frozen single-sequent search structure under MFDI1--6?}  
}  
  
If not, the frozen target takes the failure.  
  
That is exactly what K-P1 is for.  
  
⸻  
  
**6. Important: do not make resource sensitivity fail by definition**  
  
S6 was placed in D_{\mathrm{adv}}** because multiplicative linear logic lacks unrestricted structural copying/deletion and makes resource allocation load-bearing.**  
  
That historical selection rationale must not become an expectation that S6 **must fail.**  
  
Current linear-logic literature explicitly treats focusing as a way of reducing proof-search choices in linear logic; that confirms that substantial search nondeterminism exists, but it does not establish that the underlying unfocused search relation is undefined.   
  
Therefore do not reason:  
  
\text{resource-sensitive}  
\Rightarrow  
\text{FDI5 failure}.  
  
Instead test:  
  
\text{resource-sensitive}  
\Rightarrow  
\text{does frozen state preserve everything needed?}  
  
That is the actual adversarial question.  
  
⸻  
  
**7. Consequence for option A**  
  
Reject A.  
  
Even if S6 eventually passes by almost the same proof as S1, that would be an **evidentiary result, not something predetermined by CDE-v1.**  
  
For it to pass, the evidence would have to establish:  
  
MFDI1,\ldots,MFDI6.  
  
If all six happen to follow straightforwardly from the source-defined MLL derivation structure, then the correct result is:  
  
\boxed{S6=\mathbf{READY}.}  
  
We do not preserve discriminating power by inventing a harder bar for adversarial targets.  
  
Likewise, if MFDI4/5/6 fail:  
  
\boxed{S6\text{ does not inherit S1's rescue}.}  
  
Either outcome is informative.  
  
⸻  
  
**8. DF-04-H remains genuinely live**  
  
CDE-v1 does not predetermine DF-04-H because:  
  
\text{dialogue-assembled target}  
  
can have at least three outcomes:  
  
1. source literally defines it → EXACT;  
2. source canonically determines it → DIRECT;  
3. analyst supplied genuinely extra structure → SOURCE-FAIL/UNDERDETERMINED.  
  
S1 landed in category 2.  
  
S6 and S7 remain unknown.  
  
So the current S1 result weakens the naive version:  
  
“assembled targets should fail.”  
  
But the frozen hypothesis is not to be rewritten.  
  
Evaluate it only after S6/S7 complete.  
  
⸻  
  
**9. One audit note on S1**  
  
Claude’s process concern about CDE-v1 is valid and should remain prominently attached to the certificate.  
  
Record:  
  
**CDE-v1 provenance risk:** introduced in GPT Turn 34 after the Liang–Miller partial-derivation evidence was known and after the direction of its consequence for S1 was disclosed.  
  
That does not invalidate the rule.  
  
But later robustness work should attempt to defeat CDE-v1 on unrelated source/target pairs.  
  
The current over-generation checks are useful but not a proof that the rule is optimally restrictive.  
  
Do not hide that.  
  
⸻  
  
**Binding ruling before S6 retrieval**  
  
\boxed{  
\begin{aligned}  
&\text{Choose (B): S6 must satisfy CDE/FDI conditions de novo.}\\  
&\text{Resource splitting alone does not imply failure.}\\  
&\text{All admissible splits may form one determined nondeterministic relation.}\\  
&\text{The decisive issue is preservation of joint premise/resource structure.}\\  
&\text{Use MFDI1--MFDI6 above.}\\  
&\text{Do not modify the frozen S6 state to help it pass.}  
\end{aligned}  
}  
  
## Proceed with S6 under SR-B2 v2 + TSI-v1 + CDE-v1 + MFDI-v1, then S7.  
