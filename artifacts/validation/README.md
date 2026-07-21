# Validation artifacts

This tracked directory is the stable GitHub Actions upload root for unified validation diagnostics.

Runtime content is staged under `artifacts/validation/runtime/` only after a failed workflow step. Runtime files, caches, certificates, and logs are not committed. The validator's local working state remains under the ignored `.far/` directory.
