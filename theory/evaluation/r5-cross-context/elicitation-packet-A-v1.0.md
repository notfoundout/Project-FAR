# Elicitation Packet A — primary wording

**FROZEN. Do not reword, abridge, extend, or add examples.** The exact text of §2 and §3 is the experimental instrument. Any change creates a new packet version and a new run.

**Do not attach, quote, summarise, or link any other document from this repository when delivering this packet.** This file is the complete participant-facing material. The delivery checklist in `freeze-procedure-v1.0.md` §2 is binding.

---

## 1. Instructions to the person delivering this packet

Deliver §2 and §3 verbatim and nothing else. Do not answer clarifying questions about what the requester "is looking for", what a good answer resembles, or whether a direction is promising. If asked, reply only with the frozen fallback string, verbatim and without addition:

> *"Answer as you see fit; there is no target answer. Any conclusion you can justify from your own analysis is acceptable."*

This string is registered in `participant-surface-v1.1.json` and is mechanically checked. Any other clarification is an unregistered participant-facing message and makes the run a procedural failure.

Do not disclose who commissioned the work, what body of prior work it relates to, or that any prior answer exists.

Record the delivery timestamp and the delivery channel. Then follow `freeze-procedure-v1.0.md` before anything further is shown to the respondent.

---

## 2. The question

Consider the broad phenomenon of systems that work through a question or problem and arrive at conclusions, judgements, or decisions.

Suppose one episode of such a system is written down in two different ways. Determine what information must carry over between the two descriptions for them to count as descriptions of the same episode in every respect that matters.

---

## 3. Determine independently

Address each of the following. Where you cannot settle an item, say so and say why, rather than supplying a placeholder.

- **A.** The class, or classes, of systems your answer applies to. You decide the scope; do not assume any particular scope is intended.
- **B.** Which observable facts or behaviours matter.
- **C.** Which distinctions may be dropped without loss.
- **D.** What "carries over" should mean.
- **E.** What "the same in every respect that matters" should mean.
- **F.** Which ways of rewriting one description as another are legitimate.
- **G.** What assumptions your answer relies on.
- **H.** Whether there is any natural way to compare competing answers to B–F, and if so what makes it natural.
- **I.** Whether, instead, no single answer to B–F can be justified.

You may also record counterexamples you constructed, approaches you tried and rejected, and anything you regard as unresolved.

### Shapes an answer may take

An answer of any of the following shapes is complete and acceptable. **This list is neither exhaustive nor ranked, and its order carries no preference.** An answer of a shape not listed here is equally acceptable.

- A single set of requirements applies across all the systems you admit.
- A single set applies, under assumptions that you state.
- Several different sets are equally defensible.
- Different kinds of system require different sets.
- No non-trivial set exists; any candidate is empty or arbitrary.
- The question cannot be settled as asked, or you cannot reach a stable answer.

**There is no target answer.** Do not attempt to infer one from the phrasing of the question, and do not optimise for agreement with any body of work you may suspect lies behind it.

### Sources

You may consult any literature you choose. Record every source you actually used, and for each mark whether you regard it as a primary/original work, an authoritative technical reference, or a secondary or expository source. Do not treat the absence of a reading list as a signal about which fields are expected to be relevant.

### Form of the answer

Prose is acceptable. Structure your answer under the headings A–I so it can be read against the schema without interpretation. Say explicitly when an item is unresolved.

---

## 4. Notes retained for the record, not for the respondent

This section must not be delivered.

The wording above was constructed to avoid vocabulary, framing, examples, and structure drawn from the commissioning body of work. It deliberately supplies no examples, because the only example corpus available to the packet author is that body of work's own corpus, and reusing it would prime scope. Item A therefore asks the respondent to fix scope themselves.

The six candidate fields identified by the commissioning analysis are deliberately not named, hinted at, or gestured toward, per the source rule in `preregistration-v1.0.json`. The respondent's independently chosen literature is one of the outputs under test.

Outcome symmetry is deliberate and **balanced**: the list of answer shapes contains two unified-positive, two pluralistic or domain-relative, and two negative or undecidable shapes, is explicitly unranked, and is explicitly non-exhaustive. Neither a positive nor a negative result is signalled as wanted.

An earlier revision of this packet deliberately overrepresented negative and dissolving shapes, on the reasoning that this counters positive-result bias. That reasoning was wrong and the design is superseded; it is preserved as provenance in `package-audit-v1.0.md` §5 and is **not** the rationale for the current list.
