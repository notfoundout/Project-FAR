#!/usr/bin/env python3
"""Final-newline gate.

Enforces exactly one rule on eligible text files: a non-empty file ends with a
newline. Nothing else. No trailing-whitespace repair, no code formatting, no
Markdown normalization, no JSON/YAML reserialization.

The rule is byte-level and format-agnostic, so it carries no assumptions about
what any file's content means. Trailing whitespace is deliberately out of
scope: in Markdown two or more trailing spaces encode a hard line break, and
the same sequence appears inside string literals that generate Markdown, so
repairing it is a content change rather than hygiene.

Files under integrity or provenance control are exempt. Exemption is decided
two ways:

- by path, for archives, external-validation bundles, freeze directories,
  generated artifacts, conformance and test fixtures, and manifest/lock files;
- by digest, for any file whose own SHA-256, SHA-1, or Git blob SHA-1 is
  recorded somewhere in the repository. Verifiers here use all three forms.
  This is derived from repository content rather than a maintained list, so a
  newly frozen file becomes exempt as soon as its digest is recorded.

Usage:
    python tools/check_final_newline.py            # report violations
    python tools/check_final_newline.py --fix      # repair violations
    python tools/check_final_newline.py --list-exempt
"""
from __future__ import annotations
import argparse, hashlib, os, re
from pathlib import Path
from common_health import ROOT, SKIP_DIRS, rel

ELIGIBLE_SUFFIXES = {'.cff', '.html', '.js', '.json', '.lean', '.md', '.py', '.sh', '.toml', '.txt', '.yaml', '.yml'}

# Generated output, historical archives, and byte-exact fixture corpora.
EXEMPT_ROOTS = ('archive/', 'artifacts/', 'conformance/', 'exports/', 'tests/fixtures/')

DIGEST_RE = re.compile(rb'[0-9a-fA-F]{64}|[0-9a-fA-F]{40}')
DIGEST_SCAN_MAX_BYTES = 8_000_000


def walk_repository():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def is_path_exempt(relative: str) -> bool:
    if relative.startswith(EXEMPT_ROOTS):
        return True
    parts = relative.split('/')
    directories, name = parts[:-1], parts[-1]
    # Frozen evidence packages and the bundles that carry them.
    if any(segment == 'external-validation' or 'freeze' in segment for segment in directories):
        return True
    # Digest manifests and lock files.
    if name.endswith('.sha256'):
        return True
    if name.endswith('.json') and ('manifest' in name or 'lock' in name):
        return True
    return False


def content_digests(blob: bytes) -> tuple[str, str, str]:
    """The digest forms this repository's verifiers record for a file.

    Git blob SHA-1 is included because the target-category-discovery verifier
    registers file identity that way; a SHA-256-only rule silently broke it.
    """
    git_blob = b'blob ' + str(len(blob)).encode('ascii') + b'\0' + blob
    return (hashlib.sha256(blob).hexdigest(),
            hashlib.sha1(blob).hexdigest(),
            hashlib.sha1(git_blob).hexdigest())


def exemption_reason(relative: str, blob: bytes, digests: set[str]) -> str | None:
    """Why this file is exempt, or None if the rule applies to it."""
    if is_path_exempt(relative):
        return 'path'
    if any(digest in digests for digest in content_digests(blob)):
        return 'digest-recorded'
    return None


def recorded_digests() -> set[str]:
    """Every 40- and 64-hex token appearing anywhere in the repository."""
    digests = set()
    for path in walk_repository():
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        if len(blob) > DIGEST_SCAN_MAX_BYTES:
            continue
        for token in DIGEST_RE.findall(blob):
            digests.add(token.decode('ascii').lower())
    return digests


def candidate_files():
    for path in walk_repository():
        if path.suffix.lower() in ELIGIBLE_SUFFIXES:
            yield path


def is_violation(blob: bytes) -> bool:
    return bool(blob) and not blob.endswith(b'\n')


def repair(blob: bytes) -> bytes:
    return blob + b'\n' if is_violation(blob) else blob


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fix', action='store_true', help='repair violations in place')
    parser.add_argument('--list-exempt', action='store_true', help='list exempt files and why')
    args = parser.parse_args()

    digests = recorded_digests()
    failures = []
    repaired = []
    exempt = []

    for path in sorted(candidate_files()):
        relative = rel(path)
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        reason = exemption_reason(relative, blob, digests)
        if reason:
            exempt.append((relative, reason))
            continue
        if not is_violation(blob):
            continue
        if args.fix:
            path.write_bytes(repair(blob))
            repaired.append(relative)
        else:
            failures.append(relative)

    if args.list_exempt:
        for relative, reason in sorted(exempt):
            print(f'EXEMPT {relative} ({reason})')

    print(f'final newline: {len(exempt)} exempt file(s)')
    if args.fix:
        for relative in repaired:
            print(f'FIXED {relative}')
        print(f'repaired {len(repaired)} file(s)')
        return 0
    for relative in failures:
        print(f'FAIL {relative}: missing final newline')
    if failures:
        print(f'{len(failures)} file(s) missing a final newline; '
              f'run: python tools/check_final_newline.py --fix')
        return 1
    print('Final newline OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
