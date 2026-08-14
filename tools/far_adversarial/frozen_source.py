"""Frozen evidence access.

A campaign declares its source once. Every byte a lane sees afterwards comes
from that declaration, read out of the frozen object store or verified against
a content manifest. Editing the working tree mid-campaign cannot change what a
model was shown, and cannot silently change what a replay reconstructs.

Two backends:

- ``GitFrozenSource`` reads blobs from a registered commit via ``git cat-file``.
  The working tree is never consulted.
- ``ManifestFrozenSource`` reads files from disk but verifies each against a
  recorded SHA-256 before returning it.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .safety import resolve_within, sha256_hex


class SourceIntegrityError(RuntimeError):
    """Raised when frozen evidence cannot be produced exactly as registered."""


class UndeclaredPathError(SourceIntegrityError):
    """Raised when a path outside the campaign's declared evidence is requested."""


@dataclass
class FrozenSource:
    """Interface: an identity string plus verified reads of declared paths."""

    def identity(self) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def read(self, path: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def verify(self) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class GitFrozenSource(FrozenSource):
    def __init__(self, repo_root: Path, commit: str, declared_paths: list[str]):
        self.repo_root = Path(repo_root)
        self.commit = commit
        self.declared = set(declared_paths)
        self._tree: str | None = None

    # -- git plumbing -----------------------------------------------------

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=self.repo_root, capture_output=True, text=True, check=False
        )

    def verify(self) -> None:
        """Resolve and pin the commit and its root tree.

        A commit that does not exist, or an identifier that does not name a
        commit object, fails here rather than producing partial evidence later.
        """
        kind = self._git("cat-file", "-t", self.commit)
        if kind.returncode != 0 or kind.stdout.strip() != "commit":
            raise SourceIntegrityError(
                f"frozen source {self.commit!r} does not resolve to a commit object"
            )
        resolved = self._git("rev-parse", f"{self.commit}^{{tree}}")
        if resolved.returncode != 0:
            raise SourceIntegrityError(f"cannot resolve tree for {self.commit!r}")
        self._tree = resolved.stdout.strip()

    def identity(self) -> str:
        if self._tree is None:
            self.verify()
        return f"git:{self.commit}:{self._tree}"

    def read(self, path: str) -> str:
        """Read one declared path out of the frozen commit.

        Never touches the working tree. A path the campaign did not declare is
        refused even if it exists in the commit.
        """
        if path not in self.declared:
            raise UndeclaredPathError(f"{path} is not declared frozen evidence")
        # Reject traversal and absolute paths before they reach git.
        resolve_within(self.repo_root, path)
        if self._tree is None:
            self.verify()
        blob = subprocess.run(
            ["git", "cat-file", "blob", f"{self.commit}:{path}"],
            cwd=self.repo_root, capture_output=True, check=False,
        )
        if blob.returncode != 0:
            raise SourceIntegrityError(
                f"{path} is missing from frozen commit {self.commit}"
            )
        return blob.stdout.decode("utf-8", "replace")


class ManifestFrozenSource(FrozenSource):
    def __init__(self, root: Path, manifest: dict[str, str]):
        self.root = Path(root)
        self.manifest = dict(manifest)

    def identity(self) -> str:
        return "manifest:" + sha256_hex(
            json.dumps(self.manifest, sort_keys=True, ensure_ascii=False)
        )

    def verify(self) -> None:
        for path in sorted(self.manifest):
            self._verified_bytes(path)

    def _verified_bytes(self, path: str) -> bytes:
        target = resolve_within(self.root, path)
        if not target.is_file():
            raise SourceIntegrityError(f"{path} is missing from the frozen manifest root")
        data = target.read_bytes()
        actual = sha256_hex(data)
        if actual != self.manifest[path]:
            raise SourceIntegrityError(
                f"{path} does not match its frozen digest "
                f"(expected {self.manifest[path]}, got {actual})"
            )
        return data

    def read(self, path: str) -> str:
        if path not in self.manifest:
            raise UndeclaredPathError(f"{path} is not declared frozen evidence")
        return self._verified_bytes(path).decode("utf-8", "replace")


def build_manifest(root: Path, paths: list[str]) -> dict[str, str]:
    """Content-address a set of files for a non-Git frozen input set."""
    manifest: dict[str, str] = {}
    for path in sorted(paths):
        target = resolve_within(root, path)
        if not target.is_file():
            raise SourceIntegrityError(f"cannot manifest missing file: {path}")
        manifest[path] = sha256_hex(target.read_bytes())
    return manifest


def load_campaign(path: Path, repo_root: Path) -> tuple[FrozenSource, dict[str, Any]]:
    """Load a campaign manifest and construct its frozen source.

    The campaign file is the only place a source commit becomes authoritative.
    There is no path by which the current ``HEAD`` becomes the campaign source
    implicitly: an unregistered HEAD is an error, not a default.
    """
    campaign = json.loads(Path(path).read_text(encoding="utf-8"))
    kind = campaign.get("source_kind")
    declared = list(campaign.get("declared_evidence_paths", []))
    if kind == "git":
        commit = campaign.get("source_commit")
        if not commit:
            raise SourceIntegrityError("campaign declares source_kind git with no commit")
        source: FrozenSource = GitFrozenSource(repo_root, commit, declared)
    elif kind == "manifest":
        source = ManifestFrozenSource(repo_root, campaign.get("manifest", {}))
    else:
        raise SourceIntegrityError(f"unknown campaign source_kind: {kind!r}")
    source.verify()
    recorded = campaign.get("source_identity")
    if recorded and recorded != source.identity():
        raise SourceIntegrityError(
            f"campaign source identity drifted: recorded {recorded}, "
            f"resolved {source.identity()}"
        )
    return source, campaign
