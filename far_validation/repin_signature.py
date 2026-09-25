#!/usr/bin/env python3
"""Owner-signed protected-repin authorizations (AgePony Secure Enclave P-256 profile).

A repin authorization is a canonical JSON payload that the owner signs as a file in AgePony on
their iPhone, with a Secure Enclave P-256 identity generated only for FAR. AgePony emits a
detached, standard SSHSIG (``ecdsa-sha2-nistp256``, message hash ``sha512``) under its fixed
namespace ``agepony``. Authority comes from that signature under the public key pinned in
``ALLOWED_SIGNERS_PATH`` on trusted ``main``, never from where the bytes are stored or which
GitHub account pushed them. Candidate code can copy a valid authorization; it cannot alter or
manufacture one.

The SSHSIG namespace cannot separate FAR from anything else the owner signs in AgePony: every
AgePony signature uses ``agepony``. Domain separation therefore lives inside the signed bytes. A
signature authorizes nothing unless the signed file is, byte for byte, the canonical encoding of
an object with exactly ``PAYLOAD_FIELDS``, ``schema`` ``SCHEMA`` and ``domain`` ``DOMAIN``. Any
other AgePony-signed file (a photo, a note, a differently spelled or older-schema JSON) is
rejected, even under the pinned key.

Verification delegates the curve arithmetic to OpenSSH (``ssh-keygen -Y verify``) and adds strict
policy around it:

* the allowed-signers file must pin exactly one ``ecdsa-sha2-nistp256`` key (a valid uncompressed
  point on P-256) for ``PRINCIPAL``, restricted to ``NAMESPACE``, with no other option;
* the signature must be the canonical armor of an SSHSIG v1 blob by exactly that key, for
  ``NAMESPACE``, with an empty reserved field, hash ``sha512``, and an ``ecdsa-sha2-nistp256``
  signature whose ``r`` and ``s`` are minimal positive mpints in ``[1, n-1]``, with nothing
  trailing anywhere.

ECDSA signatures are malleable: ``(r, n - s)`` verifies whenever ``(r, s)`` does, and Secure
Enclave signatures are not documented to be low-S normalized, so rejecting either form could reject genuine
signatures. Nothing is keyed on signature bytes: single use is enforced on the payload ``id``.

FAR can verify possession of the pinned key. It cannot prove that the key was generated in, or
is confined to, a Secure Enclave, or that the owner was present when it signed: plain ECDSA
SSHSIG carries no attestation or presence flags. Those properties rest on the enrollment
ceremony and on AgePony; see ``docs/governance/protected-repin-procedure.md``.

Subcommands help prepare, inspect, and bundle authorizations; none needs repository code to be
trusted, and ``digest`` reads git objects directly (no checkout).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA = "far-repin-authorization/3"
# In-payload domain separation: the SSHSIG namespace below is shared by every AgePony signature.
DOMAIN = "far-protected-repin-authorization"
# AgePony's fixed SSHSIG namespace. It is not FAR-specific and cannot be changed in the app.
NAMESPACE = "agepony"
PRINCIPAL = "far-repin-owner"
ALLOWED_SIGNERS_PATH = "validation_bootstrap/repin-allowed-signers"
ASSURANCE_LOCK_PATH = "validation_bootstrap/assurance-lock.json"
LOCK_CONTRACT_PATH = ASSURANCE_LOCK_PATH + "#contract"
PAYLOAD_FIELDS = frozenset({
    "schema", "domain", "id", "repository", "repository_id", "path", "old_sha256", "new_sha256", "target_pr", "base_sha",
    "reason", "issued_at", "expires_at",
})
KEY_TYPE = "ecdsa-sha2-nistp256"
CURVE = "nistp256"
HASH_ALGORITHM = "sha512"  # AgePony's (and ssh-keygen's) default; sha256 SSHSIGs are refused
MAX_VALIDITY = timedelta(days=30)
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX32 = re.compile(r"[0-9a-f]{32}")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
ARMOR_BEGIN = "-----BEGIN SSH SIGNATURE-----"
ARMOR_END = "-----END SSH SIGNATURE-----"
ARMOR_WIDTH = 70  # ssh-keygen and AgePony both wrap at 70 columns
SIGNERS_LINE = re.compile(
    rf'{re.escape(PRINCIPAL)} namespaces="{re.escape(NAMESPACE)}" (\S+) ([A-Za-z0-9+/]+={{0,2}})'
)
PUBLIC_KEY_LINE = re.compile(r"(\S+) ([A-Za-z0-9+/]+={0,2})(?: [\x21-\x7e][\x20-\x7e]*)?")
# NIST P-256 (SEC 2 secp256r1): field prime, curve coefficient b (a = -3), group order.
P256_P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
P256_B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
P256_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


class SignatureError(ValueError):
    """An authorization is malformed, unsigned, or not signed by the trusted key."""


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise SignatureError("authorization payload repeats a key")
    return dict(pairs)


def _time(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise SignatureError(f"{field} must be a UTC timestamp string")
    try:
        parsed = datetime.strptime(value, TIME_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise SignatureError(f"{field} must use {TIME_FORMAT}") from exc
    if parsed.strftime(TIME_FORMAT) != value:
        raise SignatureError(f"{field} is not canonical")
    return parsed


def parse_payload(text: Any) -> dict[str, Any]:
    """Parse and schema-check a payload string; it must be its own canonical encoding."""
    if not isinstance(text, str):
        raise SignatureError("authorization payload must be a string")
    try:
        payload = json.loads(text, object_pairs_hook=_no_duplicates)
    except json.JSONDecodeError as exc:
        raise SignatureError(f"authorization payload is not JSON: {exc}") from exc
    if not isinstance(payload, dict) or set(payload) != PAYLOAD_FIELDS:
        raise SignatureError(f"authorization payload must have exactly fields {sorted(PAYLOAD_FIELDS)}")
    if canonical_bytes(payload) != text.encode("utf-8"):
        raise SignatureError("authorization payload is not in canonical encoding")
    if payload["schema"] != SCHEMA:
        raise SignatureError(f"authorization schema must be {SCHEMA}")
    if payload["domain"] != DOMAIN:
        raise SignatureError(f"authorization domain must be {DOMAIN} (FAR's domain separation inside the signed bytes)")
    if not isinstance(payload["id"], str) or not HEX32.fullmatch(payload["id"]):
        raise SignatureError("id must be 32 lowercase hex digits (128-bit nonce)")
    if not isinstance(payload["repository"], str) or not REPOSITORY.fullmatch(payload["repository"]):
        raise SignatureError("repository must be owner/name")
    repository_id = payload["repository_id"]
    if not isinstance(repository_id, int) or isinstance(repository_id, bool) or repository_id <= 0:
        raise SignatureError("repository_id must be the repository's positive numeric GitHub id (immutable across renames)")
    path = payload["path"]
    if (not isinstance(path, str) or not path or path.startswith("/") or "\\" in path
            or any(part in ("", ".", "..") for part in path.split("#")[0].split("/"))):
        raise SignatureError("path must be a normalized repository-relative path")
    for key in ("old_sha256", "new_sha256"):
        if not isinstance(payload[key], str) or not HEX64.fullmatch(payload[key]):
            raise SignatureError(f"{key} must be 64 lowercase hex digits")
    if payload["old_sha256"] == payload["new_sha256"]:
        raise SignatureError("authorization permits no change")
    target = payload["target_pr"]
    if not isinstance(target, int) or isinstance(target, bool) or target <= 0:
        raise SignatureError("target_pr must be a positive integer")
    if not isinstance(payload["base_sha"], str) or not HEX40.fullmatch(payload["base_sha"]):
        raise SignatureError("base_sha must be a 40-hex commit")
    reason = payload["reason"]
    if not isinstance(reason, str) or not 20 <= len(reason.strip()) <= 500 or not reason.isprintable():
        raise SignatureError("reason must be 20-500 printable characters")
    issued, expires = _time(payload["issued_at"], "issued_at"), _time(payload["expires_at"], "expires_at")
    if not issued < expires <= issued + MAX_VALIDITY:
        raise SignatureError(f"validity window must be positive and at most {MAX_VALIDITY.days} days")
    return payload


def _read_string(data: bytes, offset: int) -> tuple[bytes, int]:
    if offset + 4 > len(data):
        raise SignatureError("truncated SSH wire data")
    length = int.from_bytes(data[offset:offset + 4], "big")
    end = offset + 4 + length
    if end > len(data):
        raise SignatureError("truncated SSH wire data")
    return data[offset + 4:end], end


def _read_mpint(data: bytes, offset: int) -> tuple[int, int]:
    """A strictly minimal, positive SSH mpint (RFC 4251 section 5)."""
    value, offset = _read_string(data, offset)
    if not value or value[0] & 0x80:
        raise SignatureError("ECDSA signature component is zero or negative")
    if value[0] == 0 and (len(value) == 1 or not value[1] & 0x80):
        raise SignatureError("ECDSA signature component is not minimally encoded")
    return int.from_bytes(value, "big"), offset


def parse_public_key(blob: bytes) -> bytes:
    """Return the uncompressed point of a strict ``ecdsa-sha2-nistp256`` public-key blob."""
    kind, offset = _read_string(blob, 0)
    curve, offset = _read_string(blob, offset)
    point, offset = _read_string(blob, offset)
    if offset != len(blob) or kind != KEY_TYPE.encode() or curve != CURVE.encode():
        raise SignatureError(f"pinned key must be a plain {KEY_TYPE} key")
    if len(point) != 65 or point[0] != 0x04:
        raise SignatureError("pinned key must be an uncompressed P-256 point")
    x, y = int.from_bytes(point[1:33], "big"), int.from_bytes(point[33:], "big")
    if x >= P256_P or y >= P256_P or (y * y - (x * x * x - 3 * x + P256_B)) % P256_P:
        raise SignatureError("pinned key is not a point on P-256")
    return point


def validate_allowed_signers(data: bytes) -> tuple[str, str]:
    """Return (key type, key) of the single pinned key; reject anything that weakens verification."""
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise SignatureError("allowed-signers file must be ASCII") from exc
    lines = text.split("\n")
    if len(lines) != 2 or lines[1] != "":
        raise SignatureError("allowed-signers file must contain exactly one newline-terminated line")
    match = SIGNERS_LINE.fullmatch(lines[0])
    if match is None:
        raise SignatureError(
            f'allowed-signers line must be: {PRINCIPAL} namespaces="{NAMESPACE}" {KEY_TYPE} <key>'
        )
    if match.group(1) != KEY_TYPE:
        raise SignatureError(f"pinned key type must be {KEY_TYPE} (the AgePony Secure Enclave profile)")
    try:
        blob = base64.b64decode(match.group(2), validate=True)
    except ValueError as exc:
        raise SignatureError("pinned key is not valid base64") from exc
    if base64.b64encode(blob).decode("ascii") != match.group(2):
        raise SignatureError("pinned key is not canonical base64")
    parse_public_key(blob)
    return match.group(1), match.group(2)


def armor(blob: bytes) -> str:
    """The one canonical armor of an SSHSIG blob, as ``ssh-keygen -Y sign`` and AgePony write it."""
    encoded = base64.b64encode(blob).decode("ascii")
    lines = [encoded[i:i + ARMOR_WIDTH] for i in range(0, len(encoded), ARMOR_WIDTH)]
    return "\n".join([ARMOR_BEGIN, *lines, ARMOR_END]) + "\n"


def dearmor(text: str) -> bytes:
    """Decode an armored signature that may have been re-wrapped in transit (CRLF, blank lines)."""
    lines = [line.strip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n") if line.strip()]
    if len(lines) < 3 or lines[0] != ARMOR_BEGIN or lines[-1] != ARMOR_END:
        raise SignatureError("signature must be an armored SSH signature")
    try:
        return base64.b64decode("".join(lines[1:-1]), validate=True)
    except ValueError as exc:
        raise SignatureError("signature is not valid base64") from exc


def _check_sshsig(armored: str, key: str) -> None:
    """Every structural rule OpenSSH does not enforce, on exactly the canonical armor."""
    blob = dearmor(armored)
    if armored != armor(blob):
        raise SignatureError("signature is not in canonical armor (70-column base64, LF line ends, final LF)")
    if blob[:6] != b"SSHSIG" or blob[6:10] != (1).to_bytes(4, "big"):
        raise SignatureError("signature is not an SSHSIG v1 blob")
    public, offset = _read_string(blob, 10)
    namespace, offset = _read_string(blob, offset)
    reserved, offset = _read_string(blob, offset)
    hash_algorithm, offset = _read_string(blob, offset)
    signature, offset = _read_string(blob, offset)
    if offset != len(blob):
        raise SignatureError("signature has trailing data")
    if public != base64.b64decode(key) or namespace != NAMESPACE.encode():
        raise SignatureError("signature is not by the pinned key in the AgePony namespace")
    if reserved:
        raise SignatureError("signature reserved field must be empty")
    if hash_algorithm != HASH_ALGORITHM.encode():
        raise SignatureError(f"signature message hash must be {HASH_ALGORITHM}")
    kind, offset = _read_string(signature, 0)
    if kind != KEY_TYPE.encode():
        raise SignatureError("signature algorithm does not match the pinned key")
    components, offset = _read_string(signature, offset)
    if offset != len(signature):
        raise SignatureError("ECDSA signature has trailing data")
    r, offset = _read_mpint(components, 0)
    s, offset = _read_mpint(components, offset)
    if offset != len(components):
        raise SignatureError("ECDSA signature components have trailing data")
    if not (1 <= r < P256_N and 1 <= s < P256_N):
        raise SignatureError("ECDSA signature component out of range [1, n-1]")


def verify_signature(message: bytes, signature: Any, allowed_signers: bytes) -> None:
    """Verify an armored SSHSIG over ``message`` under the single pinned key, or raise."""
    _key_type, key = validate_allowed_signers(allowed_signers)
    if not isinstance(signature, str):
        raise SignatureError("signature must be an armored SSH signature")
    _check_sshsig(signature, key)
    with tempfile.TemporaryDirectory() as tmp:
        signers, sig = Path(tmp) / "allowed_signers", Path(tmp) / "authorization.sig"
        signers.write_bytes(allowed_signers)
        sig.write_text(signature, encoding="ascii")
        try:
            completed = subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", str(signers), "-I", PRINCIPAL, "-n", NAMESPACE, "-s", str(sig)],
                input=message, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "HOME": tmp},
            )
        except FileNotFoundError as exc:
            raise SignatureError("ssh-keygen (OpenSSH >= 8.9) is required to verify authorizations") from exc
    expected = f'Good "{NAMESPACE}" signature for {PRINCIPAL} with {KEY_TYPE.split("-")[0].upper()} key '
    if completed.returncode != 0 or not completed.stdout.decode("utf-8", "replace").startswith(expected):
        detail = (completed.stderr or completed.stdout).decode("utf-8", "replace").strip()
        raise SignatureError(f"signature does not verify under the pinned key ({detail or 'no detail'})")


def fingerprint(key: str) -> str:
    """OpenSSH-style ``SHA256:`` fingerprint, as AgePony shows for a verified signer."""
    return "SHA256:" + base64.b64encode(hashlib.sha256(base64.b64decode(key)).digest()).decode("ascii").rstrip("=")


def verify_entry(entry: Any, allowed_signers: bytes) -> dict[str, Any]:
    """Verify one ledger entry ``{"payload": <canonical str>, "signature": <armored SSHSIG>}``."""
    if not isinstance(entry, dict) or set(entry) != {"payload", "signature"}:
        raise SignatureError('authorization entry must be exactly {"payload", "signature"}')
    payload = parse_payload(entry["payload"])
    verify_signature(entry["payload"].encode("ascii"), entry["signature"], allowed_signers)
    return payload


def _git(repo: Path, *args: str) -> bytes:
    completed = subprocess.run(["git", "-C", str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        raise SignatureError(completed.stderr.decode("utf-8", "replace").strip() or f"git {args[0]} failed")
    return completed.stdout


def contract_digest(lock: dict[str, Any]) -> str:
    contract = {key: value for key, value in lock.items() if key != "files"}
    return hashlib.sha256(
        json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def object_digest(repo: Path, revision: str, path: str) -> str:
    """SHA-256 of ``path`` (or the lock contract) as stored in git at ``revision``; no checkout."""
    if path == LOCK_CONTRACT_PATH:
        return contract_digest(json.loads(_git(repo, "cat-file", "blob", f"{revision}:{ASSURANCE_LOCK_PATH}")))
    return hashlib.sha256(_git(repo, "cat-file", "blob", f"{revision}:{path}")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = parser.add_subparsers(dest="command", required=True)
    digest = sub.add_parser("digest", help="SHA-256 of a path (or the lock #contract) at a git revision")
    digest.add_argument("--repo", type=Path, default=Path.cwd())
    digest.add_argument("--rev", required=True)
    digest.add_argument("--path", required=True)
    prepare = sub.add_parser("prepare", help="write the canonical payload the owner will sign")
    prepare.add_argument("--repository", required=True)
    prepare.add_argument("--repository-id", type=int, required=True, help="gh api repos/<owner>/<name> --jq .id")
    prepare.add_argument("--path", required=True)
    prepare.add_argument("--old", required=True)
    prepare.add_argument("--new", required=True)
    prepare.add_argument("--target-pr", type=int, required=True)
    prepare.add_argument("--base-sha", required=True)
    prepare.add_argument("--reason", required=True)
    prepare.add_argument("--valid-days", type=int, default=14)
    prepare.add_argument("--out", type=Path, required=True)
    show = sub.add_parser("show", help="print a payload file for review before signing")
    show.add_argument("payload", type=Path)
    bundle = sub.add_parser("bundle", help="combine a payload and its returned .sig into a ledger entry")
    bundle.add_argument("payload", type=Path)
    bundle.add_argument("--signature", type=Path)
    bundle.add_argument("--allowed-signers", type=Path, required=True)
    bundle.add_argument("--append-to", type=Path, help="consumption ledger to append the entry to")
    pin = sub.add_parser("pin-key", help="write the allowed-signers file from AgePony's copied public key and move its lock pin")
    pin.add_argument("public_key", type=Path, help="file holding the line AgePony shows: ecdsa-sha2-nistp256 <base64> [comment]")
    pin.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        if args.command == "digest":
            print(object_digest(args.repo, args.rev, args.path))
        elif args.command == "prepare":
            issued = datetime.now(timezone.utc).replace(microsecond=0)
            payload = {
                "schema": SCHEMA, "domain": DOMAIN, "id": secrets.token_hex(16), "repository": args.repository,
                "repository_id": args.repository_id, "path": args.path,
                "old_sha256": args.old, "new_sha256": args.new, "target_pr": args.target_pr,
                "base_sha": args.base_sha, "reason": args.reason, "issued_at": issued.strftime(TIME_FORMAT),
                "expires_at": (issued + timedelta(days=args.valid_days)).strftime(TIME_FORMAT),
            }
            data = canonical_bytes(payload)
            parse_payload(data.decode("ascii"))
            args.out.write_bytes(data)
            print(json.dumps(payload, indent=2, sort_keys=True))
        elif args.command == "show":
            print(json.dumps(parse_payload(args.payload.read_text(encoding="ascii")), indent=2, sort_keys=True))
        elif args.command == "bundle":
            returned = (args.signature or args.payload.with_name(args.payload.name + ".sig")).read_text(encoding="ascii")
            # Transport (share sheets, uploads) may re-wrap the armor; the ledger stores only its canonical form.
            entry = {"payload": args.payload.read_text(encoding="ascii"), "signature": armor(dearmor(returned))}
            verify_entry(entry, args.allowed_signers.read_bytes())
            if args.append_to:
                ledger = json.loads(args.append_to.read_text(encoding="utf-8"))
                ledger["consumptions"].append(entry)
                args.append_to.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(entry, indent=2))
        elif args.command == "pin-key":
            match = PUBLIC_KEY_LINE.fullmatch(args.public_key.read_text(encoding="ascii").strip())
            if match is None:
                raise SignatureError("public key must be one line: ecdsa-sha2-nistp256 <base64> [comment]")
            kind, key = match.groups()
            line = f'{PRINCIPAL} namespaces="{NAMESPACE}" {kind} {key}\n'.encode("ascii")
            validate_allowed_signers(line)
            (args.repo / ALLOWED_SIGNERS_PATH).write_bytes(line)
            lock_path = args.repo / ASSURANCE_LOCK_PATH
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            lock["files"] = dict(sorted({**lock["files"], ALLOWED_SIGNERS_PATH: hashlib.sha256(line).hexdigest()}.items()))
            lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
            print(f"pinned {kind} key {fingerprint(key)}")
    except (OSError, SignatureError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"FAR-VAL-REPIN-SIG: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
