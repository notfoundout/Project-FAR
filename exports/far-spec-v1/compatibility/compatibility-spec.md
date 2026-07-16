# Project FAR Specification Compatibility Policy

Version: 1.0.0

## Supported integration surface

External projects may rely only on files exported in `exports/far-spec-v1` and recorded in `manifest.json` and `checksums.json`. Project FAR internal paths, implementation modules, tests, and repository layout are not supported integration surfaces.

## Stable content

The stable surface consists of exported grammar, normative schemas, canonical semantic contracts, canonical terminology, compatibility policy, and representative examples. Stability means changes are intentional, versioned, checksummed, and represented by a new export artifact set.

## Semantic versioning

Export versions use `MAJOR.MINOR.PATCH`. MAJOR changes may alter or remove stable contracts. MINOR changes may add backward-compatible artifacts or constraints. PATCH changes correct packaging, metadata, or documentation without changing Project FAR semantics.

## Compatibility guarantees

For a fixed major export version, artifact paths, schema identifiers, documented grammar references, and checksum verification remain reproducible. Consumers must verify checksums before use and must treat the manifest as authoritative for the export contents.

## Deprecation policy

Deprecated artifacts remain present for at least one minor release within the same major version unless removal is necessary to avoid publishing obsolete or experimental material as normative. Deprecations are announced in this compatibility specification or a successor compatibility artifact.

## Unsupported assumptions

Consumers must not depend on Project FAR source tree paths, Python APIs, test fixtures outside the export, generated file ordering not recorded in the manifest, unexported schemas, research notes, archived artifacts, or inferred semantics not stated by exported canonical artifacts.
