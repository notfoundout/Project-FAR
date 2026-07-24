# Environment smoke-test scope

The pull-request smoke workflow validates the exact pinned SWE-bench source checkout, required fixture files, frozen task availability, `TestSpec` interface, and generated script properties before merge.

The manual `prepare-environment` stage remains responsible for the full Docker build and environment-lock artifact because GitHub Actions does not expose manual workflow dispatch through the connected repository tool.
