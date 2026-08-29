# Citation and Zotero control v1.0

Status: **Repository infrastructure; no theorem or novelty promotion**

Project FAR uses a two-part citation system:

1. [`project-far.bib`](../../research/bibliography/project-far.bib) holds stable citation keys
   and portable bibliographic metadata suitable for import, export, and reconciliation with
   Zotero.
2. [`citation-links-v1.0.json`](../../research/registry/citation-links-v1.0.json) is the
   GitHub-governed map from bibliographic identity to an exact claim, research artifact,
   relationship, prior-art interpretation, scope, and locator.

Zotero may manage collections, attachments, deduplication, metadata repair, and citation-key
workflow. GitHub remains canonical for what a source supports, disputes, contextualizes,
anticipates, limits, or does not establish. Neither a Zotero item nor a citation changes truth,
proof, independent-review, formalization, empirical, governance, or novelty status.

The older [`bibliography.md`](../../research/bibliography/bibliography.md) remains a broad
historical working list. The structured bibliography does not duplicate every historical name;
it begins with sources that already carry exact claim-level relationships. New sources should
reuse an existing identity/key when one exists.

Validation checks JSON Schema, unique keys and relationships, one matching BibTeX entry for
every source, no unregistered BibTeX key, known claim or research-question targets, exact
artifact existence, and permitted relationship vocabulary. A missing or ambiguous source is a
failure/Unknown to resolve, never evidence of novelty.
