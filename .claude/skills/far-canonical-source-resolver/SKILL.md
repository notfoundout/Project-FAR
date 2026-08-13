---
name: far-canonical-source-resolver
description: "Determines which Project FAR documents, definitions, decisions, and claims are currently authoritative when repository materials conflict, preventing obsolete or superseded material from contaminating active research."
---

Determine the authoritative source for Project FAR concepts before relying on repository content.

For every disputed or duplicated concept:

1. Locate all relevant definitions, claims, decisions, and references.
2. Compare their dates, dependency position, status, and explicit supersession relationships.
3. Prefer explicitly canonical sources over merely newer files.
4. Prefer current decision records over historical prose when they conflict.
5. Follow the project dependency hierarchy:
   foundations
   -> shared theory
   -> FARA
   -> FAR
   -> FARO
   -> downstream implementation
6. Detect when downstream documents incorrectly redefine upstream concepts.
7. Identify legacy terminology and deprecated formulations.
8. Distinguish:
   - authoritative
   - provisional
   - superseded
   - historical
   - contradictory
   - unknown authority
9. Never combine incompatible definitions into a synthetic definition unless explicitly asked.
10. Report unresolved authority conflicts rather than guessing.

For each resolution provide:
- concept
- candidate sources
- authoritative source
- rejected/superseded sources
- reason
- dependency implications
- unresolved conflict, if any

Authority must come from explicit project structure and evidence, not document popularity or wording confidence.
