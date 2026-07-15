# PR 163 Recovery Note

PR 163 reused a branch that already contained the work merged through PR 162. Its unique scoped-status changes were isolated from the preserved backup branch and restored on a clean branch based on current `main`.

Recovered changes:

- conditional versus global primitive minimality and independence distinctions;
- VI-002 and VI-003 research-status clarifications;
- theorem catalog and theorem metadata conditional scope;
- scope-aware status-consistency matching;
- README and project-status synchronization;
- regression tests for the scoped status resolution.

The obsolete duplicate CI, tooling, and mechanization changes from PR 163 were not restored because they are already present in `main` through PR 162.
