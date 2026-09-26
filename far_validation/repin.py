#!/usr/bin/env python3
"""Protected-artifact repin evaluation against offline-signed authorizations; fails closed.

Every path listed in the comparison base's assurance lock is a protected artifact; the lock's
non-file sections are the pseudo-artifact ``LOCK_CONTRACT_PATH``. Changing one (and moving its
pin) is a *protected transition*. A transition from ``base`` to ``head`` is permitted only when the
candidate appends to the consumption ledger exactly one authorization for it that:

1. carries a valid SSH signature under the **trusted** allowed-signers key supplied by the caller
   (the gate's deployment key, which must equal the key pinned on the comparison base; never the
   candidate's copy of the key file);
2. names this repository, this path, the base pin as ``old_sha256``, the candidate's new pin as
   ``new_sha256``, and (when evaluating a pull request) this pull request;
3. was issued against a ``base_sha`` in the comparison base's lineage at which the path was pinned
   to ``old_sha256``;
4. is within its validity window and has an id never recorded in the base ledger (single use,
   including after a revert);

and every appended authorization is used by exactly one transition. The ledger is append-only and
deliberately not in the lock. Removing a path from the lock is not a supported transition.

All bytes are read from git objects (``ls-tree``/``cat-file``), never from a checkout, so
``.gitattributes`` conversions, symlinks, and working-tree state cannot make stored content
differ from what is hashed. Protected paths must be regular files. Standard library plus
``git`` and ``ssh-keygen``; candidate code is never imported or executed.

The report lists every protected transition with full digests. The gate App publishes that list in
its check output, which is the reference an owner without a computer compares an authorization
file against before signing it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from . import repin_signature as signature
except ImportError:  # Loaded as a standalone file (gate deployment or the weakening fallback).
    import importlib.util

    _spec = importlib.util.spec_from_file_location(
        "_far_validation_repin_signature", Path(__file__).resolve().with_name("repin_signature.py"))
    assert _spec is not None and _spec.loader is not None
    signature = sys.modules.setdefault(_spec.name, importlib.util.module_from_spec(_spec))
    _spec.loader.exec_module(signature)

ASSURANCE_LOCK_PATH = signature.ASSURANCE_LOCK_PATH
LOCK_CONTRACT_PATH = signature.LOCK_CONTRACT_PATH
ALLOWED_SIGNERS_PATH = signature.ALLOWED_SIGNERS_PATH
CONSUMPTIONS_PATH = "validation/protected-repin-consumptions.json"
LEDGER_SCHEMA = "2.0"
REGULAR_MODES = frozenset({"100644", "100755"})
CLOCK_SKEW = timedelta(minutes=5)


class LedgerError(ValueError):
    """A lock, ledger, or tree entry is malformed; the evaluation must fail closed."""


@dataclass
class RepinReport:
    base: str
    head: str
    failures: dict[str, list[str]] = field(default_factory=dict)
    used: list[str] = field(default_factory=list)
    # Every protected transition in the change, with full digests: what an authorization must name.
    transitions: list[dict[str, str]] = field(default_factory=list)

    def fail(self, path: str, message: str) -> None:
        self.failures.setdefault(path, []).append(message)

    @property
    def successful(self) -> bool:
        return not self.failures

    def to_dict(self) -> dict[str, Any]:
        return {"base": self.base, "head": self.head, "successful": self.successful,
                "failures": self.failures, "used": self.used, "transitions": self.transitions}


class GitObjects:
    """Read-only access to commits and blobs of one repository (bare or not); no checkout."""

    def __init__(self, repo: Path) -> None:
        self.repo = repo
        self._trees: dict[str, dict[str, tuple[str, str]]] = {}

    def _run(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(["git", "-C", str(self.repo), "-c", "core.hooksPath=/dev/null", *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def commit(self, revision: str) -> str:
        completed = self._run("rev-parse", "--verify", "--quiet", "--end-of-options", f"{revision}^{{commit}}")
        if completed.returncode != 0:
            raise LedgerError(f"cannot resolve commit {revision!r}")
        return completed.stdout.decode().strip()

    def tree(self, commit: str) -> dict[str, tuple[str, str]]:
        """Map path -> (mode, object id) for every entry of ``commit``'s tree."""
        if commit not in self._trees:
            completed = self._run("ls-tree", "-r", "-z", "--full-tree", commit)
            if completed.returncode != 0:
                raise LedgerError(f"cannot list tree of {commit}")
            entries: dict[str, tuple[str, str]] = {}
            for record in completed.stdout.split(b"\0"):
                if record:
                    meta, _, path = record.partition(b"\t")
                    mode, _kind, oid = meta.decode().split(" ")
                    entries[path.decode("utf-8", "surrogateescape")] = (mode, oid)
            self._trees[commit] = entries
        return self._trees[commit]

    def blob(self, commit: str, path: str, *, label: str) -> bytes | None:
        """Bytes of a regular file at ``commit``; None if absent; LedgerError if not a regular file."""
        entry = self.tree(commit).get(path)
        if entry is None:
            return None
        if entry[0] not in REGULAR_MODES:
            raise LedgerError(f"{label} {path} is not a regular file (mode {entry[0]})")
        completed = self._run("cat-file", "blob", entry[1])
        if completed.returncode != 0:
            raise LedgerError(f"cannot read {path} at {commit}")
        return completed.stdout

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        return self._run("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LedgerError(f"{label} is not valid UTF-8 JSON: {exc}") from exc


def _lock(data: bytes | None, label: str) -> tuple[dict[str, str], str]:
    if data is None:
        raise LedgerError(f"{label} is missing")
    payload = _json(data, label)
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), dict):
        raise LedgerError(f"{label} must be an object with a files map")
    files = payload["files"]
    if not all(isinstance(k, str) and isinstance(v, str) and len(v) == 64 for k, v in files.items()):
        raise LedgerError(f"{label} files map must bind paths to SHA-256 digests")
    return dict(files), signature.contract_digest(payload)


def _ledger(data: bytes | None, label: str) -> list[Any]:
    if data is None:
        return []
    payload = _json(data, label)
    if (not isinstance(payload, dict) or set(payload) != {"schema_version", "consumptions"}
            or payload["schema_version"] != LEDGER_SCHEMA or not isinstance(payload["consumptions"], list)):
        raise LedgerError(f"{label} must be {{schema_version: {LEDGER_SCHEMA}, consumptions: [...]}}")
    return payload["consumptions"]


def _recorded_id(entry: Any) -> str | None:
    """Id of a base ledger entry. Base entries were admitted by the gate when they were appended;
    their signatures are not re-checked, so rotating the key never invalidates history."""
    try:
        return signature.parse_payload(entry.get("payload"))["id"] if isinstance(entry, dict) else None
    except signature.SignatureError:
        return None


def _when(value: str) -> datetime:
    return datetime.strptime(value, signature.TIME_FORMAT).replace(tzinfo=timezone.utc)


def evaluate(git: GitObjects, base: str, head: str, *, allowed_signers: bytes, repository: str,
             repository_id: int | None, target_pr: int | None, now: datetime | None = None) -> RepinReport:
    """Evaluate ``head`` against comparison base ``base`` using the trusted ``allowed_signers``.

    ``repository_id`` (GitHub's immutable numeric id) and ``target_pr`` bind authorizations to this
    repository and pull request; the gate always supplies both, taking the id from the GitHub API.
    ``None`` (local advisory use only) skips that one binding.
    """
    now = now or datetime.now(timezone.utc)
    base, head = git.commit(base), git.commit(head)
    report = RepinReport(base=base, head=head)
    trusted_key = True  # without a usable trusted key nothing verifies, but every transition is still reported
    try:
        signature.validate_allowed_signers(allowed_signers)
        if git.blob(base, ALLOWED_SIGNERS_PATH, label="base") != allowed_signers:
            raise LedgerError(f"the trusted key differs from {ALLOWED_SIGNERS_PATH} on the comparison base "
                              "(redeploy the gate after an authorized key rotation)")
    except (LedgerError, signature.SignatureError) as exc:
        report.fail(ASSURANCE_LOCK_PATH, f"{exc}; no authorization can verify, failing closed")
        trusted_key = False
    try:
        base_files, base_contract = _lock(git.blob(base, ASSURANCE_LOCK_PATH, label="base"), "base assurance lock")
        head_files, head_contract = _lock(git.blob(head, ASSURANCE_LOCK_PATH, label="candidate"), "candidate assurance lock")
        base_entries = _ledger(git.blob(base, CONSUMPTIONS_PATH, label="base"), "base consumption ledger")
        head_entries = _ledger(git.blob(head, CONSUMPTIONS_PATH, label="candidate"), "candidate consumption ledger")
    except (LedgerError, signature.SignatureError) as exc:
        report.fail(ASSURANCE_LOCK_PATH, f"{exc}; failing closed")
        return report
    if CONSUMPTIONS_PATH in base_files:
        report.fail(CONSUMPTIONS_PATH, "the consumption ledger must not be protected by the lock it records (deadlock)")

    transitions: list[tuple[str, str, str]] = []
    base_tree, head_tree = git.tree(base), git.tree(head)
    for path in sorted(set(base_files) | set(head_files)):
        before, after = base_files.get(path), head_files.get(path)
        if after is None:
            report.fail(path, f"protected artifact {path} was dropped from {ASSURANCE_LOCK_PATH}; removal is not a supported transition")
            continue
        entry = head_tree.get(path)
        if before == after and entry is not None and entry == base_tree.get(path) and entry[0] in REGULAR_MODES:
            continue  # same pin, same stored object: already verified when it reached the base
        try:
            if before is not None:
                stored = git.blob(base, path, label="base")
                if stored is None or _sha256(stored) != before:
                    report.fail(path, f"base content of {path} does not match its base pin; failing closed")
            candidate = git.blob(head, path, label="candidate")
        except LedgerError as exc:
            report.fail(path, str(exc))
            continue
        actual = _sha256(candidate) if candidate is not None else None
        if actual != after:
            report.fail(path, f"candidate content of {path} hashes to {actual or '<missing>'} but its pin is {after}")
        if before is not None and after != before:
            transitions.append((path, before, after))
    if head_contract != base_contract:
        transitions.append((LOCK_CONTRACT_PATH, base_contract, head_contract))
    report.transitions = [{"path": p, "old_sha256": b, "new_sha256": a} for p, b, a in transitions]

    if head_entries[: len(base_entries)] != base_entries:
        report.fail(CONSUMPTIONS_PATH, "consumption ledger is append-only; base history was changed, reordered, or dropped")
    recorded = {i for i in map(_recorded_id, base_entries) if i}
    appended: list[dict[str, Any]] = []
    for index, entry in enumerate(head_entries[len(base_entries):]):
        label = f"appended authorization {index}"
        try:
            if not trusted_key:
                raise signature.SignatureError("no trusted key is available to verify it")
            payload = signature.verify_entry(entry, allowed_signers)
        except signature.SignatureError as exc:
            report.fail(CONSUMPTIONS_PATH, f"{label}: {exc}")
            continue
        problems = []
        if payload["repository"] != repository:
            problems.append(f"is for repository {payload['repository']}, not {repository}")
        if repository_id is not None and payload["repository_id"] != repository_id:
            problems.append(f"is for repository id {payload['repository_id']}, not {repository_id}")
        if target_pr is not None and payload["target_pr"] != target_pr:
            problems.append(f"is bound to pull request {payload['target_pr']}, not {target_pr}")
        if payload["id"] in recorded or any(p["id"] == payload["id"] for p in appended):
            problems.append("was already consumed or is duplicated; authorizations are single-use")
        if not _when(payload["issued_at"]) - CLOCK_SKEW <= now <= _when(payload["expires_at"]):
            problems.append(f"is outside its validity window {payload['issued_at']}..{payload['expires_at']}")
        problems.extend(_lineage_problems(git, payload, base))
        if problems:
            report.fail(CONSUMPTIONS_PATH, f"{label} ({payload['id']}) " + "; ".join(problems))
            continue
        appended.append(payload)

    used: set[str] = set()
    for path, before, after in transitions:
        matches = [p for p in appended if (p["path"], p["old_sha256"], p["new_sha256"]) == (path, before, after)]
        if len(matches) != 1:
            report.fail(path, (f"protected artifact {path} transition {before[:12]}->{after[:12]} requires exactly one "
                               f"valid signed authorization appended to {CONSUMPTIONS_PATH} (found {len(matches)}); "
                               "a candidate may not authorize its own protected-artifact repin"))
            continue
        used.add(matches[0]["id"])
    for payload in appended:
        if payload["id"] not in used:
            report.fail(CONSUMPTIONS_PATH, f"appended authorization {payload['id']} for {payload['path']} matches no "
                                           "protected transition in this change; the ledger records exactly the transitions made")
    report.used = sorted(used)
    return report


def _lineage_problems(git: GitObjects, payload: dict[str, Any], base: str) -> list[str]:
    try:
        issued_base = git.commit(payload["base_sha"])
    except LedgerError:
        return [f"base_sha {payload['base_sha'][:12]} is not a known commit"]
    if not git.is_ancestor(issued_base, base):
        return [f"base_sha {payload['base_sha'][:12]} is not in the comparison base's lineage (stale or foreign)"]
    try:
        files, contract = _lock(git.blob(issued_base, ASSURANCE_LOCK_PATH, label="issuing base"), "issuing base lock")
    except LedgerError as exc:
        return [str(exc)]
    pinned = contract if payload["path"] == LOCK_CONTRACT_PATH else files.get(payload["path"])
    if pinned != payload["old_sha256"]:
        return [f"{payload['path']} was not pinned to old_sha256 at base_sha {payload['base_sha'][:12]}"]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Evaluate protected-artifact repins against signed authorizations. Advisory when run "
        "locally or in CI; authoritative only as the protected-repin-gate App check."))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True, help="comparison base commit (current main)")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--allowed-signers", type=Path, help="trusted key file; defaults to the base commit's pinned file")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", "notfoundout/Project-FAR"))
    parser.add_argument("--repository-id", type=int,
                        default=int(os.environ["GITHUB_REPOSITORY_ID"]) if os.environ.get("GITHUB_REPOSITORY_ID") else None)
    parser.add_argument("--target-pr", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    git = GitObjects(args.repo)
    try:
        if args.allowed_signers:
            trusted = args.allowed_signers.read_bytes()
        else:
            trusted = git.blob(git.commit(args.base), ALLOWED_SIGNERS_PATH, label="base") or b""
        report = evaluate(git, args.base, args.head, allowed_signers=trusted, repository=args.repository,
                          repository_id=args.repository_id, target_pr=args.target_pr)
    except (OSError, LedgerError) as exc:
        print(f"FAR-VAL-REPIN-001: {exc}")
        return 2
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"protected-repin comparison base {report.base}, head {report.head}")
        for path, messages in sorted(report.failures.items()):
            print(f"[FAIL] {path}")
            for message in messages:
                print(f"  - {message}")
        print(f"authorizations used: {', '.join(report.used) or 'none'}")
        print("Result:", "PASS" if report.successful else "FAIL")
    return 0 if report.successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
