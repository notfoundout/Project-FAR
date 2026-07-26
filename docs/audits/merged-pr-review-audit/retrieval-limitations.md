# Retrieval limitations

- GitHub REST `GET /repos/notfoundout/Project-FAR` returned HTTP 404 at `2026-07-26T23:20:09Z` without authentication.
- No GitHub token or authenticated client was available, so merged-PR search, review submissions, inline review comments, review threads (GraphQL), and issue comments were inaccessible.
- Pagination did not begin. Page count is zero; no page is represented as successfully retrieved.
- The 130 locally inferred PR records are not a substitute for GitHub's merged-PR total. Deleted PRs, non-main bases, merge strategies without a numbered subject, and unavailable comments cannot be measured.
- Actionability and severity cannot be evaluated when comment bodies are unavailable.
- Completeness is therefore `INCOMPLETE`, not `COMPLETE` or `REVIEW_REQUIRED`: known review-material omissions exist.
- Re-execution requires credentials able to read the repository and review-thread GraphQL fields. No API error was silently ignored.
