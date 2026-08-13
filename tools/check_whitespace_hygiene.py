#!/usr/bin/env python3
"""Whitespace hygiene gate.

Enforces exactly two rules on eligible text files:

1. no line ends with trailing whitespace, except where that whitespace is
   content: Markdown, where two or more trailing spaces encode a hard line
   break, and multi-line Python string literals, which carry such Markdown;
2. a non-empty file ends with a newline.

This gate deliberately enforces nothing else: no code formatting, no Markdown
normalization, and no JSON/YAML reserialization.

Files under integrity or provenance control are exempt. Exemption is decided
two ways:

- by path, for archives, external-validation bundles, freeze directories,
  generated artifacts, conformance and test fixtures, and manifest/lock files;
- by digest, for any file whose own SHA-256, SHA-1, or Git blob SHA-1 is
  recorded somewhere in the repository. Verifiers here use all three forms.
  This is derived from repository content rather than a maintained list, so a
  newly frozen file becomes exempt as soon as its digest is recorded.

Usage:
    python tools/check_whitespace_hygiene.py            # report violations
    python tools/check_whitespace_hygiene.py --fix      # repair violations
    python tools/check_whitespace_hygiene.py --list-exempt
"""
from __future__ import annotations
import argparse, hashlib, os, re
from pathlib import Path
from common_health import ROOT, SKIP_DIRS, rel

ELIGIBLE_SUFFIXES = {'.cff', '.html', '.js', '.json', '.lean', '.md', '.py', '.sh', '.toml', '.txt', '.yaml', '.yml'}

# Markdown encodes a hard line break as two or more trailing spaces, so trailing
# whitespace is content there rather than cruft. Markdown is subject to the
# final-newline rule only.
TRAILING_WHITESPACE_EXEMPT_SUFFIXES = {'.md'}

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


def content_digests(blob: bytes) -> tuple[str, str, str]:
    """The digest forms this repository's verifiers record for a file."""
    git_blob = b'blob ' + str(len(blob)).encode('ascii') + b'\0' + blob
    return (hashlib.sha256(blob).hexdigest(),
            hashlib.sha1(blob).hexdigest(),
            hashlib.sha1(git_blob).hexdigest())


def candidate_files():
    for path in walk_repository():
        if path.suffix.lower() in ELIGIBLE_SUFFIXES:
            yield path


def protected_lines(text: str, suffix: str) -> set[int]:
    """1-based line numbers whose trailing whitespace is string content.

    A multi-line Python string literal can carry meaningful trailing spaces --
    for example a Markdown hard break in a report template -- so those lines
    are not cruft. Unparseable Python is treated as fully protected.
    """
    if suffix != '.py':
        return set()
    import io, token as token_module, tokenize
    protected = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type in (token_module.STRING, getattr(token_module, 'FSTRING_MIDDLE', -1)):
                if tok.end[0] > tok.start[0]:
                    protected.update(range(tok.start[0], tok.end[0] + 1))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return set(range(1, len(text.split('\n')) + 1))
    return protected


def violations(text: str, trim_trailing: bool = True, suffix: str = '') -> list[str]:
    # Split on '\n' only: splitlines() also breaks on form feed and U+2028,
    # which would corrupt content rather than repair whitespace.
    lines = text.split('\n')
    found = []
    if trim_trailing:
        protected = protected_lines(text, suffix)
        for number, line in enumerate(lines, 1):
            if line != line.rstrip() and number not in protected:
                found.append(f'{number}: trailing whitespace')
    if text and not text.endswith('\n'):
        found.append(f'{len(lines)}: missing final newline')
    return found


def repair(text: str, trim_trailing: bool = True, suffix: str = '') -> str:
    if trim_trailing:
        protected = protected_lines(text, suffix)
        repaired = '\n'.join(line if number in protected else line.rstrip()
                             for number, line in enumerate(text.split('\n'), 1))
    else:
        repaired = text
    if repaired and not repaired.endswith('\n'):
        repaired += '\n'
    return repaired


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
        if is_path_exempt(relative):
            exempt.append((relative, 'path'))
            continue
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        if any(digest in digests for digest in content_digests(blob)):
            exempt.append((relative, 'digest-recorded'))
            continue
        try:
            text = blob.decode('utf-8')
        except UnicodeDecodeError:
            continue
        suffix = path.suffix.lower()
        trim_trailing = suffix not in TRAILING_WHITESPACE_EXEMPT_SUFFIXES
        found = violations(text, trim_trailing, suffix)
        if not found:
            continue
        if args.fix:
            path.write_text(repair(text, trim_trailing, suffix), encoding='utf-8')
            repaired.append(relative)
        else:
            failures.extend(f'{relative}:{item}' for item in found)

    if args.list_exempt:
        for relative, reason in sorted(exempt):
            print(f'EXEMPT {relative} ({reason})')

    print(f'whitespace hygiene: {len(exempt)} exempt file(s)')
    if args.fix:
        for relative in repaired:
            print(f'FIXED {relative}')
        print(f'repaired {len(repaired)} file(s)')
        return 0
    for item in failures:
        print(f'FAIL {item}')
    if failures:
        print(f'{len(failures)} whitespace hygiene violation(s); run: python tools/check_whitespace_hygiene.py --fix')
        return 1
    print('Whitespace hygiene OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
